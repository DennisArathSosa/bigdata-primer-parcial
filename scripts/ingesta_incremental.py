"""
ingesta_incremental.py
======================
Script de ingesta incremental de datos de calidad del aire.
Descarga datos de la API pública de OpenAQ y los guarda localmente
en data/raw/, solo añadiendo los registros nuevos (ingesta incremental).

Uso:
    python scripts/ingesta_incremental.py

Requiere:
    pip install requests pandas
"""

import os
import json
import requests
import pandas as pd
from datetime import datetime, timedelta

# ─────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────

BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR     = os.path.join(BASE_DIR, "data", "raw")
PROC_DIR    = os.path.join(BASE_DIR, "data", "processed")
CHECKPOINT  = os.path.join(RAW_DIR, "ultimo_registro.json")

API_URL     = "https://api.openaq.org/v2/measurements"
CIUDAD      = "Tegucigalpa"          # Cambia a tu ciudad de interés
PARAMETRO   = "pm25"                 # pm25 | pm10 | co | no2 | o3
LIMITE      = 1000                   # Máximo de registros por llamada


# ─────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────

def cargar_checkpoint() -> str:
    """Lee la fecha del último registro descargado."""
    if os.path.exists(CHECKPOINT):
        with open(CHECKPOINT, "r") as f:
            data = json.load(f)
            return data.get("ultima_fecha", None)
    return None


def guardar_checkpoint(fecha: str):
    """Guarda la fecha del último registro descargado."""
    with open(CHECKPOINT, "w") as f:
        json.dump({"ultima_fecha": fecha}, f, indent=2)
    print(f"  ✅ Checkpoint actualizado: {fecha}")


def calcular_rango_fechas(ultima_fecha: str):
    """
    Si hay checkpoint, descarga desde ahí.
    Si no, descarga las últimas 24 horas (primera ejecución).
    """
    ahora = datetime.utcnow()
    if ultima_fecha:
        fecha_desde = ultima_fecha
        print(f"  📅 Ingesta incremental desde: {fecha_desde}")
    else:
        fecha_desde = (ahora - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")
        print(f"  📅 Primera ejecución — descargando últimas 24h desde: {fecha_desde}")
    
    fecha_hasta = ahora.strftime("%Y-%m-%dT%H:%M:%SZ")
    return fecha_desde, fecha_hasta


# ─────────────────────────────────────────
# INGESTA
# ─────────────────────────────────────────

def descargar_datos(fecha_desde: str, fecha_hasta: str) -> list:
    """Llama a la API de OpenAQ y retorna lista de mediciones."""
    params = {
        "city":         CIUDAD,
        "parameter":    PARAMETRO,
        "date_from":    fecha_desde,
        "date_to":      fecha_hasta,
        "limit":        LIMITE,
        "sort":         "asc",
    }

    print(f"\n  🌐 Consultando API OpenAQ...")
    print(f"     Ciudad:    {CIUDAD}")
    print(f"     Parámetro: {PARAMETRO}")
    print(f"     Desde:     {fecha_desde}")
    print(f"     Hasta:     {fecha_hasta}")

    try:
        respuesta = requests.get(API_URL, params=params, timeout=15)
        respuesta.raise_for_status()
        datos = respuesta.json()
        resultados = datos.get("results", [])
        print(f"  📦 Registros recibidos: {len(resultados)}")
        return resultados

    except requests.exceptions.ConnectionError:
        print("  ⚠️  Sin conexión a Internet. Usando datos de muestra...")
        return generar_datos_muestra()

    except requests.exceptions.HTTPError as e:
        print(f"  ❌ Error HTTP: {e}")
        return []


def generar_datos_muestra() -> list:
    """
    Genera datos simulados cuando no hay conexión.
    Útil para desarrollo y pruebas sin internet.
    """
    import random
    ahora = datetime.utcnow()
    datos = []
    for i in range(50):
        ts = ahora - timedelta(minutes=5 * i)
        datos.append({
            "date":      {"utc": ts.strftime("%Y-%m-%dT%H:%M:%SZ")},
            "value":     round(random.uniform(5, 150), 2),
            "parameter": PARAMETRO,
            "unit":      "µg/m³",
            "location":  f"Sensor-{random.randint(1,10):02d}",
            "city":      CIUDAD,
            "country":   "HN",
        })
    return datos


def normalizar_datos(registros: list) -> pd.DataFrame:
    """Convierte la respuesta de la API a un DataFrame limpio."""
    if not registros:
        return pd.DataFrame()

    filas = []
    for r in registros:
        filas.append({
            "fecha_utc":  r.get("date", {}).get("utc", ""),
            "valor":      r.get("value", None),
            "parametro":  r.get("parameter", ""),
            "unidad":     r.get("unit", ""),
            "ubicacion":  r.get("location", ""),
            "ciudad":     r.get("city", ""),
            "pais":       r.get("country", ""),
        })

    df = pd.DataFrame(filas)
    df["fecha_utc"] = pd.to_datetime(df["fecha_utc"], errors="coerce")
    df = df.dropna(subset=["fecha_utc", "valor"])
    df = df.sort_values("fecha_utc").reset_index(drop=True)
    return df


def guardar_datos(df: pd.DataFrame):
    """
    Guarda o concatena los datos nuevos al archivo CSV incremental.
    Si ya existe el archivo, agrega solo los registros nuevos.
    """
    os.makedirs(RAW_DIR, exist_ok=True)
    nombre_archivo = os.path.join(RAW_DIR, f"calidad_aire_{CIUDAD.lower().replace(' ', '_')}.csv")

    if os.path.exists(nombre_archivo):
        df_existente = pd.read_csv(nombre_archivo, parse_dates=["fecha_utc"])
        # Combinar y eliminar duplicados por fecha y ubicación
        df_combinado = pd.concat([df_existente, df], ignore_index=True)
        df_combinado = df_combinado.drop_duplicates(subset=["fecha_utc", "ubicacion"])
        df_combinado = df_combinado.sort_values("fecha_utc").reset_index(drop=True)
        df_combinado.to_csv(nombre_archivo, index=False)
        registros_nuevos = len(df_combinado) - len(df_existente)
        print(f"  💾 Archivo actualizado: +{registros_nuevos} registros nuevos")
        print(f"     Total acumulado: {len(df_combinado)} registros")
    else:
        df.to_csv(nombre_archivo, index=False)
        print(f"  💾 Archivo creado con {len(df)} registros")
        print(f"     Ruta: {nombre_archivo}")

    return nombre_archivo


# ─────────────────────────────────────────
# EJECUCIÓN PRINCIPAL
# ─────────────────────────────────────────

def main():
    print("\n" + "="*55)
    print("  🚀 INGESTA INCREMENTAL — Calidad del Aire")
    print("="*55)

    # 1. Determinar rango de fechas
    ultima_fecha = cargar_checkpoint()
    fecha_desde, fecha_hasta = calcular_rango_fechas(ultima_fecha)

    # 2. Descargar datos
    registros = descargar_datos(fecha_desde, fecha_hasta)

    # 3. Normalizar
    df = normalizar_datos(registros)
    if df.empty:
        print("\n  ⚠️  No se obtuvieron datos válidos. Finalizando.")
        return

    print(f"\n  🧹 Datos normalizados:")
    print(df.head(3).to_string(index=False))

    # 4. Guardar
    guardar_datos(df)

    # 5. Actualizar checkpoint con la fecha más reciente
    fecha_max = df["fecha_utc"].max().strftime("%Y-%m-%dT%H:%M:%SZ")
    guardar_checkpoint(fecha_max)

    print("\n" + "="*55)
    print("  ✅ Ingesta completada exitosamente")
    print("="*55 + "\n")


if __name__ == "__main__":
    main()
