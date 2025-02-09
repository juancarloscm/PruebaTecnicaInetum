from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split, count
from google.cloud import bigquery

# Crear sesión de Spark
spark = SparkSession.builder.appName("IdentifyTopics").getOrCreate()

# Ruta de entrada
input_path = "gs://buckets-aws/processed_data/analyzed_data.parquet"

# Leer datos desde Cloud Storage
df = spark.read.parquet(input_path)

# 🛠 Análisis de tendencias por tema
topics_trend = (
    df.groupBy("category")
      .count()
      .withColumnRenamed("count", "article_count")
)

# Mostrar las tendencias por tema
print("Tendencias por tema:")
topics_trend.show(truncate=False)

# 🛠 Contar menciones de compañías
companies_mentions = (
    df.select(explode(split(col("entities.companies"), ", ")).alias("company"))
      .groupBy("company")
      .count()
      .withColumnRenamed("count", "mention_count")
      .filter(col("company") != "")  # Eliminar compañías vacías
)

# Mostrar las menciones de compañías
print("Menciones de compañías:")
companies_mentions.show(truncate=False)

# 🛠 Contar menciones de lugares
places_mentions = (
    df.select(explode(split(col("entities.places"), ", ")).alias("place"))
      .groupBy("place")
      .count()
      .withColumnRenamed("count", "mention_count")
      .filter(col("place") != "")  # Eliminar lugares vacíos
)

# Mostrar las menciones de lugares
print("Menciones de lugares:")
places_mentions.show(truncate=False)

# 📥 Guardar resultados en BigQuery
def save_to_bigquery(spark_df, table_name):
    """Guarda un DataFrame de Spark en BigQuery."""
    spark_df.write.format("bigquery") \
        .option("table", f"analitica-contact-center-dev.pos_analitica_ANALISIS.{table_name}") \
        .option("writeDisposition", "WRITE_TRUNCATE") \
        .save()
    print(f"Datos guardados en BigQuery: {table_name}")

# Guardar las tablas en BigQuery
save_to_bigquery(topics_trend, "topic_trends")
save_to_bigquery(companies_mentions, "company_mentions")
save_to_bigquery(places_mentions, "place_mentions")

# Finalizar la sesión de Spark
spark.stop()
