from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower
import sys

# Crear sesión de Spark
spark = SparkSession.builder.appName("CleanAndDeduplicate").getOrCreate()

# Ruta de entrada y salida (Cloud Storage)
input_path = "gs://buckets-aws/raw_data/"
output_path = "gs://buckets-aws/processed_data/cleaned_data.parquet"

# Leer archivos JSON desde Cloud Storage
articles_df = spark.read.json(f"{input_path}articles.json")
blogs_df = spark.read.json(f"{input_path}blogs.json")
reports_df = spark.read.json(f"{input_path}reports.json")

# Unificar los tres DataFrames
combined_df = articles_df.unionByName(blogs_df).unionByName(reports_df)

# Eliminar duplicados basados en el campo 'id'
deduplicated_df = combined_df.dropDuplicates(["id"])

# Limpiar las columnas innecesarias
cleaned_df = deduplicated_df.select(
    "id",
    "title",
    "summary",
    "published_at",
    lower(col("news_site")).alias("news_site"),  # Convertir el nombre del sitio de noticias a minúsculas
    "url"
)

# Guardar el resultado en formato Parquet en Cloud Storage
cleaned_df.write.mode("overwrite").parquet(output_path)

print(f"Datos limpiados y deduplicados guardados en: {output_path}")

# Finalizar la sesión de Spark
spark.stop()

