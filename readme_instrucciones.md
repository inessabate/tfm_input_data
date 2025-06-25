# Proyecto MeteoGalicia - Trusted Zone y Zona de Explotación

Este repositorio forma parte del Trabajo de Fin de Máster sobre modelado de riesgos climáticos en el sector asegurador. El objetivo es construir una arquitectura de big data que permita procesar datos meteorológicos de estaciones de Galicia desde la API de MeteoGalicia.

## Estructura del proyecto

```
/data
  /raw/meteogalicia/                    # Datos originales en JSON
  /trusted/meteogalicia_estaciones/     # Datos limpios en Delta
  /exploitation/
     /meteogalicia_estaciones/          # Datos particionados por provincia
     /meteogalicia_kpis/                # KPIs generados por Spark
/outputs/                               # Exportaciones CSV generadas por DuckDB
/src/ingestion_trusted_exploitation/
  001_meteogalicia_ingestion_trusted_zone.py
  002_meteogalicia_exploitation_zone.py
  003_meteogalicia_view_results_Spark.py
  003_meteogalicia_view_results_duckdb.py
```

## Ejecución paso a paso

### 1. Trusted Zone (limpieza y validación)
```bash
python src/ingestion_trusted_exploitation/001_meteogalicia_ingestion_trusted_zone.py
```
- Carga el JSON de estaciones (GeoJSON)
- Explota y aplana los datos
- Aplica validaciones de tipo, nulos y duplicados
- Guarda la tabla Delta limpia en `/data/trusted/`

### 2. Exploitation Zone + KPIs con Spark
```bash
python src/ingestion_trusted_exploitation/002_meteogalicia_exploitation_zone.py
```
- Carga los datos limpios
- Particiona por provincia
- Calcula KPIs agregados por concello y provincia
- Guarda tablas Delta en `/data/exploitation/meteogalicia_kpis/`

### 3. Visualización de resultados con Spark
```bash
python src/ingestion_trusted_exploitation/003_meteogalicia_view_results_Spark.py
```
- Muestra los KPIs guardados usando Spark

### 4. Análisis ligero con DuckDB
```bash
python src/ingestion_trusted_exploitation/003_meteogalicia_view_results_duckdb.py
```
- Lee los `.parquet` de la zona de explotación
- Ejecuta consultas SQL con DuckDB
- Exporta los KPIs como CSV a `/outputs/`

## Requisitos
- Python 3.12+
- PySpark
- delta-spark
- duckdb
- pandas

## Autoría
Trabajo realizado en el marco del Máster de Big Data Management, Technologies and Analytics (UPC), curso 2024-2025.

