# 🌍 TFM - Ingesta de datos meteorológicos de MeteoGalicia

Este módulo forma parte del proyecto de TFM:  
**"Modelización de impactos climáticos en la gestión de riesgos para seguros"**  
Equipo: Gala Villodres, Inés Sabaté, Cesc Ortega

---

## ✅ ¿Por qué Delta Lake?

[Delta Lake](https://delta.io) es una **capa de almacenamiento open-source** que se ejecuta sobre sistemas de archivos como HDFS, S3, Azure o local, y **extiende el formato Parquet** con funcionalidades avanzadas como:

- ✅ **Transacciones ACID** (seguras y consistentes al leer/escribir datos)
- ✅ **Control de versiones y rollback**
- ✅ **Evolución del esquema** (soporta cambios en columnas sin romper la tabla)
- ✅ **Altísimo rendimiento** con compatibilidad total con Apache Spark
- ✅ **Consultas SQL y visualización inmediata de los datos**

Esto lo convierte en una **alternativa moderna a data lakes tradicionales**, ideal para arquitecturas tipo *medallion* o *lakehouse*, donde se integran múltiples fuentes de datos en una única plataforma flexible.

---

## 🎯 Objetivo

Implementar una **pipeline de ingesta batch** para almacenar y estructurar datos meteorológicos en una **landing zone basada en Delta Lake**, con el fin de facilitar su posterior análisis geoespacial y predictivo.

---

## 📦 Datos fuente

- **Origen**: API MeteoGalicia (GeoJSON)
- **Tipo**: Estaciones meteorológicas con atributos y geometría
- **Formato original**: JSON con estructura `FeatureCollection`

---

## 🔄 Flujo de ingesta

1. **Carga del archivo JSON estructurado (multi-línea)**
2. **Explosión del array `features`**
3. **Normalización del esquema (flatten de atributos y geometría)**
4. **Escritura en formato Delta Lake (`.parquet + _delta_log`)**

---

## 🛠️ Tecnologías utilizadas

- Python 3.12
- pyspark 3.5.1
- delta-spark 3.1.0
- Apache Spark (modo local)
- Delta Lake como arquitectura de *landing zone*

---

## 🗂️ Estructura del proyecto

```
tfm_input_data/
├── data/
│   ├── raw/
│   │   └── meteogalicia/
│   │       └── METEOGALICIA_stations.json
│   └── delta/
│       └── meteogalicia_estaciones/  ← tabla Delta
│
├── src/
│   └── ingestion/
│       └── meteogalicia_ingestion.py
│
├── requirements.txt
└── README.md
```

---

---

## 🧪 Cómo ejecutar

1. Instalar entorno virtual y dependencias:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Asegurarse de tener Java 11 instalado:
   ```bash
   sudo apt install openjdk-11-jdk
   export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
   ```

3. Ejecutar el script:
   ```bash
   python src/ingestion/meteogalicia_ingestion.py
   ```

---

## ✅ Resultado y posibilidades

Los datos se almacenan como una tabla Delta Lake en `data/delta/meteogalicia_estaciones`, compuesta por archivos `.parquet` más un registro de cambios `_delta_log`.

Con esta tabla se puede:

- Visualizar fácilmente los datos:
  ```python
  df = spark.read.format("delta").load("data/delta/meteogalicia_estaciones")
  df.show()
  ```
- Consultar con **SQL directamente en Spark**:
  ```python
  spark.sql("SELECT * FROM delta.`data/delta/meteogalicia_estaciones` WHERE provincia = 'A Coruña'")
  ```
- Unir con otras fuentes de datos (e.g. alertas en tiempo real)
- Desarrollar mapas interactivos y análisis por zona
- Entrenar modelos predictivos basados en localización
- Servir los datos a dashboards como Power BI, Superset o Databricks

Este módulo actúa como base del sistema de datos climáticos del proyecto.

---

## 📋 Tabla final generada (muestra)

| idEstacion | nombre         | concello            | idConcello | provincia  | x_coord | y_coord |
|------------|----------------|----------------------|-------------|-------------|----------|----------|
| 10045      | Mabegondo       | ABEGONDO             | 15001       | A Coruña    | 559899   | 4787883  |
| 10046      | Marco da Curra  | MONFERO              | 15050       | A Coruña    | 589613   | 4799508  |
| 10047      | Pedro Murias    | RIBADEO              | 27051       | Lugo        | 654874   | 4822648  |
| 10048      | O Invernadeiro  | VILARIÑO DE CONSO    | 32092       | Ourense     | 636839   | 4664377  |
| 10049      | Corrubedo       | RIBEIRA              | 15073       | A Coruña    | 497652   | 4711419  |