# 🔍 Explicación del Código
# Tokenización (Tokenizer): Divide el contenido del resumen (summary) en palabras.
# Remover Stopwords (StopWordsRemover): Filtra palabras comunes que no aportan valor.
# CountVectorizer: Calcula la frecuencia de las palabras en cada documento.
# TF-IDF (IDF): Calcula la relevancia de cada palabra.
# Selección de Palabras Clave: Se eligen las 5 palabras con mayor valor de TF-IDF para cada resumen.
# 📊 Beneficios de Usar TF-IDF
# Mayor precisión en la identificación de palabras clave.
# Relevancia contextual: Evita que palabras comunes se conviertan en "palabras clave".
#Optimización para análisis avanzado o entrenamiento de modelos de Machine Learning.
   

from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, StopWordsRemover, CountVectorizer, IDF
from pyspark.sql.functions import col


# Crear sesión de Spark
spark = SparkSession.builder.appName("PerformAnalysisTFIDF").getOrCreate()

# Ruta de entrada y salida (Cloud Storage)
input_path = "gs://buckets-aws/processed_data/cleaned_data.parquet"
output_path = "gs://buckets-aws/processed_data/analyzed_data_tfidf.parquet"

# Leer datos desde Cloud Storage
df = spark.read.parquet(input_path)

# Paso 1: Tokenización
tokenizer = Tokenizer(inputCol="summary", outputCol="words")
words_df = tokenizer.transform(df)

# Paso 2: Remover Stopwords
remover = StopWordsRemover(inputCol="words", outputCol="filtered_words")
filtered_df = remover.transform(words_df)

# Paso 3: Calcular frecuencia de términos (CountVectorizer)
vectorizer = CountVectorizer(inputCol="filtered_words", outputCol="raw_features")
vectorized_model = vectorizer.fit(filtered_df)
vectorized_df = vectorized_model.transform(filtered_df)

# Paso 4: Calcular TF-IDF
idf = IDF(inputCol="raw_features", outputCol="tfidf_features")
idf_model = idf.fit(vectorized_df)
tfidf_df = idf_model.transform(vectorized_df)

# Paso 5: Seleccionar las palabras clave más relevantes
def extract_top_keywords(tfidf_vector, vocabulary, num_keywords=5):
    """Extrae las palabras con mayor valor TF-IDF."""
    if tfidf_vector is None:
        return []
    indices = tfidf_vector.indices
    values = tfidf_vector.values
    sorted_indices = sorted(range(len(values)), key=lambda k: -values[k])[:num_keywords]
    keywords = [vocabulary[indices[i]] for i in sorted_indices]
    return ", ".join(keywords)

# Crear una lista de palabras clave basada en TF-IDF
vocabulary = vectorized_model.vocabulary
spark.udf.register("extract_top_keywords", lambda vec: extract_top_keywords(vec, vocabulary), StringType())

# Aplicar la función para generar las palabras clave
tfidf_df = tfidf_df.withColumn("keywords", udf(lambda vec: extract_top_keywords(vec, vocabulary), StringType())(col("tfidf_features")))

# Mostrar el resultado
tfidf_df.select("summary", "keywords").show(truncate=False)

# Guardar el resultado en formato Parquet en Cloud Storage
tfidf_df.write.mode("overwrite").parquet(output_path)

print(f"Análisis completado con TF-IDF. Datos guardados en: {output_path}")

# Finalizar la sesión de Spark
spark.stop()
