# MeteoGalicia Project – Trusted Zone and Exploitation Zone

This repository is part of the Master’s Thesis on modeling climate impacts in insurance risk management. The goal is to build a big data architecture capable of processing meteorological data from weather stations in Galicia using the MeteoGalicia API.

## Project Structure

```
/data
  /raw/meteogalicia/                    # Original data in JSON format
  /trusted/meteogalicia_estaciones/     # Cleaned data in Delta format
  /exploitation/
     /meteogalicia_estaciones/          # Partitioned data by province
     /meteogalicia_kpis/                # KPIs generated with Spark
/outputs/                               # CSV exports generated with DuckDB
/src/ingestion_trusted_exploitation/
  001_meteogalicia_ingestion_trusted_zone.py
  002_meteogalicia_exploitation_zone.py
  003_meteogalicia_view_results_Spark.py
  003_meteogalicia_view_results_duckdb.py
```

## Step-by-step Execution

### 1. Trusted Zone (cleaning and validation)
```bash
python src/ingestion_trusted_exploitation/001_meteogalicia_ingestion_trusted_zone.py
```
- Loads the station data in GeoJSON format
- Explodes and flattens the features
- Applies type, null, and duplicate validations
- Saves the cleaned Delta table to `/data/trusted/`

### 2. Exploitation Zone + KPIs with Spark
```bash
python src/ingestion_trusted_exploitation/002_meteogalicia_exploitation_zone.py
```
- Loads the cleaned data
- Partitions by province
- Calculates aggregated KPIs by municipality and province
- Saves Delta tables to `/data/exploitation/meteogalicia_kpis/`

### 3. KPI Visualization with Spark
```bash
python src/ingestion_trusted_exploitation/003_meteogalicia_view_results_Spark.py
```
- Displays the KPIs stored using Spark

### 4. Lightweight Analysis with DuckDB
```bash
python src/ingestion_trusted_exploitation/003_meteogalicia_view_results_duckdb.py
```
- Reads the `.parquet` files from the exploitation zone
- Executes SQL queries with DuckDB
- Exports KPI results as CSV to `/outputs/`

## Requirements
- Python 3.12+
- PySpark
- delta-spark
- duckdb
- pandas

## Authors
This project was developed as part of the Master's in Big Data Management, Technologies and Analytics (UPC), academic year 2024–2025.
