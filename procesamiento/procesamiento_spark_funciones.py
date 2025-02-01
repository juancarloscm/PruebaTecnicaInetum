from pyspark.sql import SparkSession
from pyspark.sql.functions import col, monotonically_increasing_id, udf, count, date_format
from pyspark.sql.types import StringType, TimestampType
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, HashingTF, IDF
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import json


#✅ Explicación de Mejoras en el Código
#🔹 Análisis de Contenido
#✔ Extracción de palabras clave con TF-IDF
#✔ Identificación de entidades (compañías, personas, lugares) usando NLTK
#✔ Clasificación de artículos por tema con palabras clave

#🔹 Análisis de Tendencias
#✔ Detección de tendencias en el tiempo con agrupación por fecha
#✔ Identificación de fuentes de noticias más activas


# 📌 1️⃣ Inicia sesion de Spark
spark = SparkSession.builder \
    .appName("AnalisisNoticias") \
    .getOrCreate()

# 📌 2️⃣ Configuración de Variables
BUCKET_NAME = "us-central1-flujotransacion-9cfbfa36-bucket"
RAW_PATH = f"gs://{BUCKET_NAME}/datos_raw/articles.json"
PROCESSED_PATH = f"gs://{BUCKET_NAME}/datos_procesados/articles_cleaned.parquet"
BIGQUERY_TABLE = "analitica-contact-center-dev.Entorno_Pruebas_modelo.noticias_procesadas"

# 📌 3️⃣ Cargar Datos desde Cloud Storage
df = spark.read.json(RAW_PATH)

# 📌 4️⃣ Limpieza de Datos
df_cleaned = df.dropDuplicates(["id"]) \
               .filter(col("title").isNotNull()) \
               .withColumnRenamed("news_site", "fuente") \
               .withColumnRenamed("published_at", "fecha_publicacion")

# 📌 5️⃣ Convertir `published_at` a TIMESTAMP
df_cleaned = df_cleaned.withColumn("fecha_publicacion", col("fecha_publicacion").cast(TimestampType()))

# 📌 6️⃣ Agregar ID Único
df_cleaned = df_cleaned.withColumn("id_articulo", monotonically_increasing_id())

# 📌 7️⃣ Extracción de Palabras Clave con TF-IDF
tokenizer = RegexTokenizer(inputCol="title", outputCol="words", pattern="\\W")
df_tokenized = tokenizer.transform(df_cleaned)

remover = StopWordsRemover(inputCol="words", outputCol="filtered_words")
df_filtered = remover.transform(df_tokenized)

hashingTF = HashingTF(inputCol="filtered_words", outputCol="raw_features", numFeatures=20)
df_featurized = hashingTF.transform(df_filtered)

idf = IDF(inputCol="raw_features", outputCol="features")
idf_model = idf.fit(df_featurized)
df_tf_idf = idf_model.transform(df_featurized)

# 📌 8️⃣ Identificación de Entidades (Organizaciones, Personas, Lugares)
nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def extract_entities(text):
    words = word_tokenize(text)
    tagged = pos_tag(words)
    chunked = ne_chunk(tagged)
    
    entities = []
    for chunk in chunked:
        if isinstance(chunk, Tree):
            entity_name = " ".join(c[0] for c in chunk)
            entity_type = chunk.label()
            entities.append(f"{entity_name} ({entity_type})")
    return ", ".join(entities)

extract_entities_udf = udf(extract_entities, StringType())
df_entities = df_cleaned.withColumn("entidades", extract_entities_udf(col("title")))

# 📌 9️⃣ Clasificación de Artículos por Tema
TOPICS = {
    "Ciencia": ["NASA", "SpaceX", "ciencia", "investigación"],
    "Economía": ["mercado", "acciones", "inversión"],
    "Exploración": ["Marte", "lanzamiento", "misión", "astronauta"]
}

def classify_article(title):
    for topic, keywords in TOPICS.items():
        if any(keyword.lower() in title.lower() for keyword in keywords):
            return topic
    return "Otro"

classify_udf = udf(classify_article, StringType())
df_classified = df_cleaned.withColumn("tema", classify_udf(col("title")))

# 📌 🔟 Análisis de Tendencias
df_tendencias = df_cleaned.groupBy(date_format("fecha_publicacion", "yyyy-MM-dd").alias("fecha")) \
                          .agg(count("id").alias("total_articulos")) \
                          .orderBy("fecha")

df_fuentes_activas = df_cleaned.groupBy("fuente") \
                               .agg(count("id").alias("cantidad_articulos")) \
                               .orderBy(col("cantidad_articulos").desc())

# 📌 1️⃣1️⃣ Guardar Datos Limpios en Cloud Storage
df_classified.write.mode("overwrite").parquet(PROCESSED_PATH)

# 📌 1️⃣2️⃣ Cargar Datos a BigQuery
df_classified.write \
    .format("bigquery") \
    .option("table", BIGQUERY_TABLE) \
    .option("temporaryGcsBucket", BUCKET_NAME) \
    .mode("overwrite") \
    .save()

print(f"✅ Procesamiento finalizado. Datos guardados en {BIGQUERY_TABLE}")

# 📌 1️⃣3️⃣ Guardar Reportes de Tendencias y Fuentes Más Activas
df_tendencias.write.format("bigquery") \
    .option("table", "analitica-contact-center-dev.Entorno_Pruebas_modelo.tendencias_temas") \
    .mode("overwrite").save()

df_fuentes_activas.write.format("bigquery") \
    .option("table", "analitica-contact-center-dev.Entorno_Pruebas_modelo.fuentes_activas") \
    .mode("overwrite").save()

print(f"✅ Reportes de tendencias y fuentes activas guardados en BigQuery.")

# 📌 1️⃣4️⃣ Finalizar Sesión de Spark
spark.stop()

