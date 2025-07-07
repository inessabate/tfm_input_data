# 🌍 Proyecto TFM – Ingesta y Procesamiento de Datos Meteorológicos

Este proyecto forma parte del Trabajo de Fin de Máster (TFM):  
**"Modelización de impactos climáticos en la gestión de riesgos para seguros"**  
**Autores:** Gala Villodres, Inés Sabaté, Cesc Ortega

---

## 🎯 Objetivo del Proyecto

Desarrollar una aplicación en Python capaz de recolectar, transformar y almacenar datos meteorológicos desde diferentes APIs: **SIAR**, **MeteoGalicia**, **Euskalmet** y **AEMET**, con el fin de facilitar su análisis en el contexto de gestión de riesgos climáticos.

---

## 🧰 Tecnologías Utilizadas

- Python 3.10+
- Apache Spark
- Delta Lake
- DuckDB
- dotenv, requests, pandas

---

## 🌐 APIs Integradas

- **AEMET**: Agencia Estatal de Meteorología  
- **MeteoGalicia**: Datos históricos de estaciones meteorológicas  
- **SIAR**: Sistema de Información Agroclimática  
- **Euskalmet**: Agencia Vasca de Meteorología  

---

## 📁 Estructura del Proyecto

```
tfm_input_data/
├── data/
│   ├── raw/
│   │   └── meteogalicia/
│   │       └── METEOGALICIA_stations.json
│   ├── trusted/
│   │   └── meteogalicia_estaciones/      
│   ├── exploitation/
│   │   └── meteogalicia_estaciones/      
│   └── delta/
│       └── meteogalicia_estaciones/      
│
├── src/
│   └── ingestion_trusted_exploitation/
│   │    └── meteogalicia_ingestion.py
│   ├── clients/
│   │   │   ├── aemet_client.py
│   │   │   ├── base_client.py
│   │   │   ├── siar_client.py
│   │   │   ├── meteogalicia_client.py
│   │   │   └── euskalmet_client.py
│   ├── utils/
│
├── requirements.txt
└── README.md
```
---

## 🔐 Configuración del Entorno

Antes de ejecutar el proyecto, crea un archivo `.env` en la raíz del directorio. Puedes usar el archivo `.env.example` como plantilla.

### Variables de Entorno Requeridas

```plaintext
API_KEY_SIAR 
API_KEY_METEOGALICIA 
API_KEY_EUSKALMET 
API_KEY_AEMET 
```
### Instalación de Dependencias
```bash
pip install -r requirements.txt
```

## 🧱 Arquitectura de Datos

Organizada en tres zonas:
- `raw/`: Datos descargados directamente de las APIs en su formato original (JSON, XML...).
- `trusted/`: Limpieza y validación usando Delta Lake. Se almacenan en formato Delta, permitiendo control de versiones y consistencia.
- `exploitation/`: CLimpieza y validación usando Delta Lake. Se almacenan en formato Delta, permitiendo control de versiones y consistencia.
- `delta/`: Almacena la tabla Delta Lake principal, que sirve de base para el resto de transformaciones y análisis.


### 💡 ¿Por qué Delta Lake?

[Delta Lake](https://delta.io) extiende Parquet con ventajas clave:

- ✅ Transacciones ACID  
- ✅ Control de versiones y rollback  
- ✅ Evolución de esquema  
- ✅ Alto rendimiento con Apache Spark  
- ✅ Consultas SQL eficientes  

Ideal para arquitecturas *medallion* y *lakehouse*.

---

## 🚀 Ejecución Paso a Paso

### 1. Zona Trusted

```bash
python src/ingestion_trusted_exploitation/001_meteogalicia_ingestion_trusted_zone.py
```

Limpia y transforma los datos de estaciones MeteoGalicia.

### 2. Zona de Explotación

```bash
python src/ingestion_trusted_exploitation/002_meteogalicia_exploitation_zone.py
```

Genera KPIs y estructura los datos para análisis.

### 3. Visualización de Resultados

- Con Spark:
```bash
python src/ingestion_trusted_exploitation/003_meteogalicia_view_results_Spark.py
```

- Con DuckDB:
```bash
python src/ingestion_trusted_exploitation/003_meteogalicia_view_results_duckdb.py
```

---

## ⚙️ Comandos Útiles

### 🧹 Eliminar archivos `.idea` del seguimiento de Git

1. **Eliminar `.idea` del índice de Git**:

```bash
git rm -r --cached .
git add .
git commit -m "Cleanup: remove ignored files from Git tracking"
```

2. **Añadir `.idea` al `.gitignore`**:

```
.idea/
```

3. **Confirmar el cambio**:

```bash
git add .gitignore
git commit -m "Add .idea to .gitignore"
```

---
