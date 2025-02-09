from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, lower
from pyspark.sql.types import StringType, MapType
import re
from collections import Counter

# Crear sesión de Spark
spark = SparkSession.builder.appName("PerformAnalysis").getOrCreate()

# Ruta de entrada y salida (Cloud Storage)
input_path = "gs://buckets-aws/processed_data/cleaned_data.parquet"
output_path = "gs://buckets-aws/processed_data/analyzed_data.parquet"

# Leer datos desde Cloud Storage
df = spark.read.parquet(input_path)

# 🛠 Funciones de análisis
def extract_keywords(summary):
    """Extrae las 5 palabras más comunes del resumen."""
    words = re.findall(r'\w+', summary.lower()) if summary else []
    common_words = Counter(words).most_common(5)
    return ", ".join([word for word, _ in common_words])

def classify_article(summary):
    """Clasifica el artículo en Launch, Rocket, Space o General."""
    if "launch" in summary.lower():
        return "Launch"
    elif "rocket" in summary.lower():
        return "Rocket"
    elif "space" in summary.lower():
        return "Space"
    else:
        return "General"

def identify_entities(summary):
    """Identifica compañías y lugares mencionados en el resumen."""
    companies = ["NASA", "SpaceX", "Boeing", "Blue Origin"]
    places = ["Florida", "Texas", "California", "Mars"]
    summary_lower = summary.lower() if summary else ""
    found_companies = [c for c in companies if c.lower() in summary_lower]
    found_places = [p for p in places if p.lower() in summary_lower]
    return {"companies": ", ".join(found_companies), "places": ", ".join(found_places)}

# Registrar las funciones como UDFs (User Defined Functions)
spark.udf.register("extract_keywords", extract_keywords, StringType())
spark.udf.register("classify_article", classify_article, StringType())
spark.udf.register("identify_entities", identify_entities, MapType(StringType(), StringType()))

# Aplicar las UDFs para el análisis
analyzed_df = (
    df.withColumn("keywords", udf(extract_keywords, StringType())(df.summary))
      .withColumn("category", udf(classify_article, StringType())(df.summary))
      .withColumn("entities", udf(identify_entities, MapType(StringType(), StringType()))(df.summary))
)

# Mostrar el resultado
analyzed_df.show(truncate=False)

# Guardar el resultado en formato Parquet en Cloud Storage
analyzed_df.write.mode("overwrite").parquet(output_path)

print(f"Análisis completado. Datos guardados en: {output_path}")

# Finalizar la sesión de Spark
spark.stop()

