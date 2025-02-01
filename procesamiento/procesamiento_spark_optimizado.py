from pyspark.sql import SparkSession
from pyspark.sql.functions import col, monotonically_increasing_id, udf, count, date_format
from pyspark.sql.types import StringType, TimestampType
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, HashingTF, IDF
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import json

# Optimizacion del procesamiento en Spark que incluye
# Particionamiento por fecha_publicacion para mejorar el rendimiento en BigQuery y almacenamiento en GCS.
# Caching de datos con .cache() para evitar recalcular consultas frecuentes.
# Optimización de particiones en Spark (spark.sql.shuffle.partitions = 50).

# 1. Inicio Sesion de Spark
spark = SparkSession.builder \
    .appName("AnalisisNoticias") \
    .config("spark.sql.parquet.enableVectorizedReader", "true") \
    .config("spark.sql.shuffle.partitions", "50") \
    .getOrCreate()

# 2 Configuracion de Variables
BUCKET_NAME = "us-central1-flujotransacion-9cfbfa36-bucket"
RAW_PATH = f"gs://{BUCKET_NAME}/datos_raw/articles.json"
PROCESSED_PATH = f"gs://{BUCKET_NAME}/datos_procesados/articles_cleaned.parquet"
BIGQUERY_TABLE = "analitica-contact-center-dev.Entorno_Pruebas_modelo.noticias_procesadas"

# 3. Cargar Datos desde Cloud Storage
df = spark.read.json(RAW_PATH).cache()  # Cachear resultados para optimizar

# 4.  Limpieza de Datos
df_cleaned = df.dropDuplicates(["id"]) \
               .filter(col("title").isNotNull()) \
               .withColumnRenamed("news_site", "fuente") \
               .withColumnRenamed("published_at", "fecha_publicacion")

# 5. Convertir `published_at` a TIMESTAMP
df_cleaned = df_cleaned.withColumn("fecha_publicacion", col("fecha_publicacion").cast(TimestampType()))

# 6. Agregar ID Unico
df_cleaned = df_cleaned.withColumn("id_articulo", monotonically_increasing_id())

# 7. Particionamiento por Fecha de Publicacion
df_partitioned = df_cleaned.repartition("fecha_publicacion")

# 8 Guardar Datos Limpios en Cloud Storage en Formato Parquet con Particionamiento
df_partitioned.write.mode("overwrite").partitionBy("fecha_publicacion").parquet(PROCESSED_PATH)

# 9. Cargar Datos a BigQuery
df_partitioned.write \
    .format("bigquery") \
    .option("table", BIGQUERY_TABLE) \
    .option("temporaryGcsBucket", BUCKET_NAME) \
    .mode("overwrite") \
    .save()

print(f"✅ Procesamiento optimizado finalizado. Datos guardados en {BIGQUERY_TABLE}")

# 10. Finalizo sesion de Spark
spark.stop()

