# NECESARIO JAVA 11 INSTALADO

import os
import shutil
from pathlib import Path
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
from pyspark.sql.functions import col, explode

# Crear SparkSession con Delta
builder = SparkSession.builder \
    .appName("Ingesta_MeteoGalicia") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
spark = configure_spark_with_delta_pip(builder).getOrCreate()

# Ruta base del proyecto (2 niveles arriba de este script)
base_path = Path(__file__).resolve().parents[2]

# Ruta del archivo de entrada (JSON)
json_path = base_path / "data" / "raw" / "meteogalicia" / "METEOGALICIA_stations.json"

# Ruta del output en Delta Lake
delta_output_path = base_path / "data" / "delta" / "meteogalicia_estaciones"

# Función para borrar el directorio Delta si ya existe
def reset_output(path: Path):
    if path.exists() and path.is_dir():
        print(f"🧹 Borrando carpeta existente: {path}")
        shutil.rmtree(path)
    else:
        print(f"📂 No existe aún la carpeta Delta: {path}")

# Borrar output anterior si existe ya que sino genera dos logs y dos parquet por cada ejecución
reset_output(delta_output_path)

# Cargar JSON multi-línea
raw_df = spark.read.option("multiLine", True).json(str(json_path))
raw_df.printSchema()
raw_df.show(truncate=False)

# Explodear las features
features_df = raw_df.select(explode(col("features")).alias("feature"))

# Aplanar campos relevantes
flat_df = features_df.select(
    col("feature.attributes.idEstacion").alias("idEstacion"),
    col("feature.attributes.Estacion").alias("nombre"),
    col("feature.attributes.Concello").alias("concello"),
    col("feature.attributes.idConcello").alias("idConcello"),
    col("feature.attributes.provincia").alias("provincia"),
    col("feature.geometry.x").alias("x_coord"),
    col("feature.geometry.y").alias("y_coord")
)

# Guardar en Delta Lake
flat_df.write.format("delta").mode("overwrite").save(str(delta_output_path))
print(f"✅ Datos guardados en formato Delta: {delta_output_path}")

# Leer los datos guardados para visualización
df = spark.read.format("delta").load(str(delta_output_path))
df.show()



