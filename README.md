# 🌫️ Monitoreo de Calidad del Aire con Big Data

## 📌 Descripción del Proyecto

Este proyecto analiza datos reales de calidad del aire urbano utilizando técnicas de Big Data.
Se procesan mediciones de contaminantes atmosféricos (PM2.5, PM10, CO₂, NO₂, Ozono) 
provenientes de redes de sensores distribuidos en ciudades.

## 🎯 Objetivo

Demostrar por qué el análisis de datos de calidad del aire **requiere herramientas de Big Data**
y no puede resolverse con Excel o bases de datos relacionales simples, debido al volumen,
velocidad y variedad de los datos generados.

---

## 📊 Preguntas clave del proyecto

### ¿Qué datos genera?
Sensores distribuidos en la ciudad generan lecturas cada 1–5 minutos de:
- PM2.5 (partículas finas)
- PM10 (partículas gruesas)
- CO₂, NO₂, Ozono
- Temperatura y humedad relativa

**Volumen estimado:** Una red de 500 sensores produce ~150 millones de registros al mes.

### ¿Quién los usa?
| Actor | Uso |
|---|---|
| Gobiernos | Alertas de emergencia y política ambiental |
| Hospitales | Correlación contaminación–ingresos respiratorios |
| Ciudadanos | Apps de calidad del aire en tiempo real |
| Investigadores | Estudios de salud pública a largo plazo |

### ¿Qué problema resuelve?
- Detectar zonas peligrosas en tiempo real
- Predecir crisis de contaminación con modelos ML
- Evaluar impacto de políticas públicas
- Emitir alertas tempranas a poblaciones vulnerables

### ¿Por qué no bastaría Excel?
| Criterio | Excel/SQL | Big Data |
|---|---|---|
| Volumen | Colapsa con +1M filas | Maneja miles de millones |
| Velocidad | Análisis por lotes, lento | Procesamiento en tiempo real |
| Variedad | Solo tablas estructuradas | JSON, series de tiempo, geodatos |
| Complejidad | Sin modelos predictivos | ML integrado |

---

## 📁 Estructura del Proyecto

```
bigdata-primer-parcial/
│
├── data/
│   ├── raw/          ← Datos originales sin modificar
│   └── processed/    ← Datos limpios y transformados
│
├── notebooks/
│   └── 01_exploracion_dataset.ipynb
│
├── scripts/
│   └── ingesta_incremental.py
│
├── docs/
│   └── arquitectura_big_data.png
│
├── requirements.txt
└── README.md
```

---

## 🔧 Instalación

```bash
# 1. Clonar el repositorio
git clone <tu-url-de-github>
cd bigdata-primer-parcial

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Abrir Jupyter
jupyter notebook notebooks/01_exploracion_dataset.ipynb
```

## 🗂️ Fuente de Datos

- **OpenAQ**: https://openaq.org/  
- **Kaggle – Air Quality**: https://www.kaggle.com/datasets/search?q=air+quality

## 👤 Autor

Estudiante: ___________________________  
Curso: Big Data – Primer Parcial  
Fecha: 2026
