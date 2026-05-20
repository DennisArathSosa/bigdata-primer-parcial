# 🚀 Instrucciones para configurar Git y GitHub

## Paso 1: Inicializar Git en la carpeta del proyecto

```bash
cd bigdata-primer-parcial
git init
git add .
git commit -m "feat: proyecto inicial calidad del aire"
```

## Paso 2: Crear repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre del repositorio: `bigdata-primer-parcial`
3. Visibilidad: Público o Privado
4. NO marques "Initialize repository" (ya tienes archivos)
5. Click en "Create repository"

## Paso 3: Conectar con GitHub y subir

```bash
git remote add origin https://github.com/TU_USUARIO/bigdata-primer-parcial.git
git branch -M main
git push -u origin main
```

## Paso 4: Instalar dependencias y abrir Jupyter

```bash
pip install -r requirements.txt
jupyter notebook notebooks/01_exploracion_dataset.ipynb
```

## Paso 5: Para futuras actualizaciones

```bash
# Primero ejecuta la ingesta
python scripts/ingesta_incremental.py

# Luego sube los cambios
git add .
git commit -m "datos: actualización ingesta incremental"
git push
```
