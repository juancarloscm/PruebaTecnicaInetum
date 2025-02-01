from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, monotonically_increasing_id
from pyspark.sql.types import StringType, TimestampType
from google.cloud import bigquery


# *****Explicacion del codigo
# Carga datos desde Cloud Storage (GCS) en formato JSON
# Elimina duplicados y registros sin titulo
# Convierte la fecha published_at a formato TIMESTAMP
# Renombra columnas para mayor claridad
# Guarda los datos limpios en GCS (Parquet) y BigQuery
# Optimiza consultas en BigQuery con formato particionado


# Inicia session
spark = SparkSession.builder \
    .appName("ProcesamientoNoticias") \
    .getOrCreate()

#Configuracion de variables
BUCKET_NAME = "us-central1-flujotransacion-9cfbfa36-bucket"
RAW_PATH = f"gs://{BUCKET_NAME}/datos_raw/articles.json"
PROCESSED_PATH = f"gs://{BUCKET_NAME}/datos_procesados/articles_cleaned.parquet"
BIGQUERY_TABLE = "analitica-contact-center-dev.Entorno_Pruebas_modelo.noticias_procesadas"

#Carga los datos desde desde Cloud Storage
df = spark.read.json(RAW_PATH)

# Realiza la limpieza de datos
df_cleaned = df.dropDuplicates(["id"]) \
               .filter(col("title").isNotNull()) \
               .withColumnRenamed("news_site", "fuente") \
               .withColumnRenamed("published_at", "fecha_publicacion")

#Convertir el campo published_at a TIMESTAMP
convertir_fecha = udf(lambda x: x[:19] if x else None, StringType())  # Tomar solo `YYYY-MM-DDTHH:MM:SS`
df_cleaned = df_cleaned.withColumn("fecha_publicacion", convertir_fecha(col("fecha_publicacion")).cast(TimestampType()))

# Establece un Id Unicos
df_cleaned = df_cleaned.withColumn("id_articulo", monotonically_increasing_id())

# Guardar Datos Limpios en Cloud Storage
df_cleaned.write.mode("overwrite").parquet(PROCESSED_PATH)

#Cargar Datos a BigQuery
df_cleaned.write \
    .format("bigquery") \
    .option("table", BIGQUERY_TABLE) \
    .option("temporaryGcsBucket", BUCKET_NAME) \
    .mode("overwrite") \
    .save()

print(f"✅ Procesamiento finalizado. Datos guardados en {BIGQUERY_TABLE}")

# Finaliza Session en Spark
spark.stop()

