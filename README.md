

#  Pipeline de Analisis de Tendencias en la Industria Espacial 
#  Proyecto: ETL y Análisis de Noticias en GCP

## 📌 Descripción
Este proyecto implementa un pipeline de **ETL (Extract, Transform, Load)** en **Google Cloud Platform (GCP)** para extraer datos de la API de **Spaceflight News**, transformarlos con **Apache Spark en Dataproc**, y almacenarlos en **Google BigQuery** para análisis y visualización.

**OPCION 1:**

## ⚙️ Tecnologias Utilizadas
- **Google Cloud Composer (Airflow)** - Orquestación del pipeline.
- **Google Cloud Storage (GCS)** - Almacenamiento intermedio de datos.
- **Google BigQuery** - Data Warehouse para análisis y reportes.
- **Google Dataproc (Spark)** - Transformación y procesamiento de datos.
- **Looker Studio** - Visualización de datos.

## 📁 Estructura del Proyecto
```
├── Dags/
│   ├── Dag_blogs_Biquery_Dinamico # etl_almacen_datos_noticias.py-DAG principal en Airflow
│   ├── PipelineSpark # PipelineSpark.py # Automatización del flujo de trabajo, desde la extracción de datos hasta la carga en BigQuery y la generación de insights diarios.
│── Data_Warehouse_Bigquery/
│   ├── Fuentes_Noticias_mas_Influyentes.sql  
│   ├── Tablas.sql  # sql creacion de tablas 
│   ├── Tendencias_Temas_mes.sql  # sql Tendencias
│── sql/
│   ├── Relacion_tablas.sql
│   ├── dim_fuentes_noticias.sql
│   ├── dim_temas.sql
│   ├── noticias_procesadas.sql
│── scripts/
│   ├── procesamiento_spark.py  # Transformaciones con Spark en Dataproc
│── test_Unitarios/
│   ├── test_conectividad_bigquery.py  # Test de integridad del DAG
│   ├── test_dag.py  # Test de validación en BigQuery
│── arquitecturas/
│   ├── Parte1_Arquitectura_Pipeline
│   ├── test_bigquery.py  # Test de validación en BigQuery
│── procesamiento/
│   ├── comandos.txt  #
│   ├── procesamiento_spark.py  #
│   ├── procesamiento_spark_funciones.py  #
│   ├── procesamiento_spark_optimizado.py  #
│   ├── limpia_y_deduplica.py  # Herramienta: Apache Spark en Google Cloud Dataproc,Función: Limpieza y deduplicación de datos extraídos (articles, blogs, reports).Almacenamiento: Cloud Storage (cleaned_data.parquet)
│   ├── proceso_analysis.py  # Herramienta: Apache Spark en Google Cloud Dataproc,Función: Extracción de palabras clave Clasificación por temas (Launch, Rocket, Space) Identificación de compañías y lugares mencionados Almacenamiento: Cloud Storage (analyzed_data.parquet)
│   ├── identfica__topics.py  # Herramienta: Apache Spark en Google Cloud Dataproc Función: Análisis de tendencias por temas Conteo de menciones de compañías y lugares Almacenamiento: Google BigQuery (topic_trends, company_mentions, place_mentions)
│── README.md  # Documentación
```

##  Flujo del Pipeline
1️⃣ **Extracción de Datos**: Se extraen noticias desde la API de **Spaceflight News**, manejando paginación y rate limits.
2️⃣ **Almacenamiento en GCS**: Los datos se guardan en formato **JSON y Parquet** en Google Cloud Storage.
3️⃣ **Procesamiento en Dataproc (Spark)**: Limpieza, deduplicación y análisis de contenido y tendencias.
4️⃣ **Carga en BigQuery**: Se insertan datos normalizados en un modelo dimensional.
5️⃣ **Análisis SQL**: Se ejecutan consultas optimizadas para tendencias y reportes.
6️⃣ **Visualización en Looker Studio**: Se crean dashboards para análisis de datos.

## 🛠 Configuración y Despliegue
### 1️⃣ Subir el DAG a Composer
```sh
gsutil cp dags/etl_almacen_datos_noticias.py gs://us-central1-flujotransacion-9cfbfa36-bucket/dags/
```

### 2️⃣ Subir Script de Spark a GCS
```sh
gsutil cp scripts/procesamiento_spark.py gs://us-central1-flujotransacion-9cfbfa36-bucket/scripts/
```

### 3️⃣ Reiniciar Airflow para Aplicar Cambios
```sh
gcloud composer environments restart-web-server flujotransacional --location us-central1
```

### 4️⃣ Ejecutar el DAG en Airflow
1. Ir a **Composer → Abrir Airflow**  
2. Activar y Ejecutar el DAG **`etl_almacen_datos_noticias`**  
3. Monitorear la ejecución en **BigQuery**  

## 🧪 Tests Unitarios
Ejecutar pruebas en Airflow y BigQuery:
```sh
pytest tests/
```

## 📊 Análisis SQL
### 🔹 **Tendencias de temas por mes**
```sql
SELECT FORMAT_DATE('%Y-%m', fecha_publicacion) AS mes, nombre, COUNT(*) AS total
FROM `analitica-contact-center-dev.Entorno_Pruebas_modelo.fact_articulos`
JOIN `analitica-contact-center-dev.Entorno_Pruebas_modelo.dim_temas`
ON fact_articulos.topic_id = dim_temas.topic_id
GROUP BY mes, nombre ORDER BY mes DESC, total DESC;
```

### 🔹 **Fuentes de noticias mas influyentes**
```sql
SELECT f.nombre AS fuente, COUNT(a.article_id) AS total_articulos,
       SUM(a.visitas) AS total_visitas, SUM(a.compartidos) AS total_compartidos,
       (SUM(a.visitas) + SUM(a.compartidos)) AS impacto_total
FROM `analitica-contact-center-dev.Entorno_Pruebas_modelo.fact_articulos` a
JOIN `analitica-contact-center-dev.Entorno_Pruebas_modelo.dim_fuentes_noticias` f
ON a.source_id = f.source_id
GROUP BY fuente
ORDER BY impacto_total DESC
LIMIT 10;
```

## 📈 Visualización en Looker Studio
Conectar **BigQuery** con **Looker Studio** para crear un dashboards interactivo y visualizar tendencias en los datos.

## 📌 Conclusión
✔ **Pipeline optimizado con particionamiento y clustering en BigQuery**  
✔ **Procesamiento escalable en Dataproc con Apache Spark**  
✔ **Orquestación eficiente con Airflow en Cloud Composer**  
✔ **Visualización intuitiva en Looker Studio**  



**OPCION 2**

## Mejora del Modelo
## 📌 Descripción
📌 Pipeline Completo en Google Cloud
Este pipeline extrae noticias espaciales de la API de Spaceflight News, las procesa y las limpia con Apache Beam (Dataflow), las almacena en BigQuery y las visualiza con Looker Studio.

## ⚙️ Tecnologias Utilizadas

- ** 1️⃣ Cloud Functions → Ingesta de datos desde la API y publicación en Pub/Sub (100% serverless).
- ** 2️⃣ Pub/Sub → Sistema de mensajería para manejar datos en tiempo real y desacoplar procesos.
- ** 3️⃣ Dataflow (Apache Beam) → Procesa y enriquece los datos (palabras clave, clasificación) antes de enviarlos a BigQuery.
- ** 4️⃣ BigQuery → Almacena y analiza grandes volúmenes de datos, con particionamiento y clustering para consultas rápidas.
- ** 5️⃣ Cloud Composer (Airflow) → Orquesta el pipeline completo, programa tareas y monitorea fallos.
- ** 6️⃣ Google Cloud Natural Language API → Análisis de texto para extraer entidades y temas principales.
- ** 7️⃣ Looker Studio → Dashboards dinámicos para visualizar tendencias y patrones clave.

Arquitectura PIPELINE 

https://lucid.app/documents/embedded/230b2762-6f66-4fe1-8dac-260179ab6aaf

Inteligencia Artificial utilizada
Modelo Ia-ops
Ver PDF


1️⃣ Ingesta de Datos con Cloud Functions
📌 Objetivo:

Extraer noticias de Spaceflight News API.
Enviar los datos a Pub/Sub para su procesamiento.
📌 Código en Python para Cloud Functions:

import requests
import json
import time
from google.cloud import pubsub_v1
from datetime import datetime

# Configuración de la API y Pub/Sub
BASE_URL = "https://api.spaceflightnewsapi.net/v4"
ENDPOINTS = ["/articles", "/blogs", "/reports", "/info"]
PROJECT_ID = "mi-proyecto"
TOPIC_NAME = "ingesta-noticias"

# Sistema de Logs detallado
def log_event(event):
    """Logea eventos del sistema."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {event}")

def obtener_datos(endpoint):
    """Obtiene todos los datos de un endpoint con paginación y manejo de rate limits."""
    url = f"{BASE_URL}{endpoint}"
    datos = []
    seen_ids = set()  # Para deduplicar artículos

    while url:
        response = requests.get(url)
        
        # Manejo de rate limit (espera 5 segundos y reintenta)
        if response.status_code == 429:
            log_event("⚠️ Rate limit alcanzado. Esperando 5 segundos...")
            time.sleep(5)
            continue
        
        # Verificación de respuesta correcta
        if response.status_code == 200:
            json_data = response.json()
            for item in json_data["results"]:
                # Deduplicación basada en el ID del artículo
                if item["id"] not in seen_ids:
                    datos.append(item)
                    seen_ids.add(item["id"])
            
            # Obtener la URL de la siguiente página
            url = json_data.get("next")
            log_event(f"✅ Página procesada para {endpoint}.")
        else:
            log_event(f"⚠️ Error al obtener datos de {endpoint}: {response.status_code}")
            break
    
    return datos

def publicar_en_pubsub(datos, endpoint):
    """Publica los datos en Pub/Sub."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)
    
    for item in datos:
        mensaje = {
            "endpoint": endpoint,
            "data": item
        }
        publisher.publish(topic_path, data=json.dumps(mensaje).encode("utf-8"))
    
    log_event(f"✅ {len(datos)} registros del endpoint {endpoint} publicados en Pub/Sub.")

def main(request):
    """Función principal de Cloud Function."""
    log_event("🚀 Inicio de la ingesta de datos.")
    
    for endpoint in ENDPOINTS:
        datos = obtener_datos(endpoint)
        if datos:
            publicar_en_pubsub(datos, endpoint)
        else:
            log_event(f"⚠️ No se encontraron datos para {endpoint}.")
    
    log_event("🎯 Ingesta completada para todos los endpoints.")
    return "✅ Ingesta finalizada."

🔹 Mejoras Implementadas
1️⃣ Sistema de Paginación Eficiente: La función obtener_datos gestiona la paginación automática con el campo next de la API.
2️⃣ Manejo de Rate Limits: Si se recibe el código 429 (rate limit), el sistema espera 5 segundos y vuelve a intentar la solicitud.
3️⃣ Deduplicación de Artículos: Se utiliza un conjunto (set) de IDs para evitar duplicados al recopilar datos.
4️⃣ Sistema de Logs: Cada acción importante se registra con un timestamp para facilitar la auditoría y depuración.
5️⃣ Código preparado para Tests Unitarios: Las funciones son modulares y reutilizables, lo que facilita la creación de tests.

📌 ¿Cómo sería un Test Unitario para esta función?
test unitario para la función obtener_datos utilizando unittest.

📌 Código de Test Unitario :
import unittest
from unittest.mock import patch
import requests

class TestObtenerDatos(unittest.TestCase):

    @patch('requests.get')
    def test_obtener_datos_paginacion(self, mock_get):
        # Simula la respuesta de la API con paginación
        mock_get.side_effect = [
            MockResponse({"results": [{"id": 1, "title": "Artículo 1"}], "next": "next_page_url"}, 200),
            MockResponse({"results": [{"id": 2, "title": "Artículo 2"}], "next": None}, 200)
        ]
        
        datos = obtener_datos("/articles")
        self.assertEqual(len(datos), 2)
        self.assertEqual(datos[0]["title"], "Artículo 1")

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

if __name__ == '__main__':
    unittest.main()
    


📌 Paso 1: Crear las Tablas en BigQuery
Antes de procesar los datos, vamos a crear tablas separadas en BigQuery para almacenar cada tipo de datos (articles, blogs, reports, info).

📌 Tablas en BigQuery:

-- Tabla para artículos
CREATE TABLE dataset_noticias.articles (
    id STRING PRIMARY KEY,
    title STRING,
    url STRING,
    image_url STRING,
    news_site STRING,
    summary STRING,
    published_at TIMESTAMP,
    updated_at TIMESTAMP,
    featured BOOLEAN,
    launches ARRAY<STRING>,
    events ARRAY<STRING>
);

-- Tabla para blogs
CREATE TABLE dataset_noticias.blogs (
    id STRING PRIMARY KEY,
    title STRING,
    url STRING,
    image_url STRING,
    news_site STRING,
    summary STRING,
    published_at TIMESTAMP
);

-- Tabla para reports
CREATE TABLE dataset_noticias.reports (
    id STRING PRIMARY KEY,
    title STRING,
    url STRING,
    news_site STRING,
    published_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Tabla para metadata (info)
CREATE TABLE dataset_noticias.info (
    version STRING,
    about STRING
);


🔹 Paso 1: Diseño de Tablas Mejorado
las tablas para soportar análisis avanzado de contenido y tendencias de noticias.

1️⃣ Tabla articles optimizada
Incluimos nuevas columnas para almacenar:

Palabras clave (keywords).
Entidades (compañías, personas, lugares) extraídas del contenido.
Clasificación por tema (science, politics, technology, etc.).
Particionamiento por fecha (published_at) para mejorar las consultas históricas.

📌 Esquema de la Tabla articles:
CREATE TABLE dataset_noticias.articles (
    id STRING PRIMARY KEY,
    title STRING,
    url STRING,
    image_url STRING,
    news_site STRING,
    summary STRING,
    published_at TIMESTAMP,
    updated_at TIMESTAMP,
    featured BOOLEAN,
    launches ARRAY<STRING>,
    events ARRAY<STRING>,
    keywords ARRAY<STRING>,                  -- Palabras clave
    entities ARRAY<STRING>,                  -- Entidades identificadas
    topic STRING                             -- Clasificación por tema
)
PARTITION BY DATE(published_at);             -- Particionamiento por fecha

2️⃣ Tabla blogs optimizada
Añadimos columnas para:

Palabras clave y entidades.
Clasificación por tema.
Particionamiento por fecha (published_at).
📌 Esquema de la Tabla blogs:
CREATE TABLE dataset_noticias.blogs (
    id STRING PRIMARY KEY,
    title STRING,
    url STRING,
    image_url STRING,
    news_site STRING,
    summary STRING,
    published_at TIMESTAMP,
    keywords ARRAY<STRING>,                  -- Palabras clave
    entities ARRAY<STRING>,                  -- Entidades identificadas
    topic STRING                             -- Clasificación por tema
)
PARTITION BY DATE(published_at);

🔹 Paso 2: Implementación de Análisis de Contenido
📌 Objetivo:
Extraer palabras clave, entidades y clasificaciones para enriquecer los datos almacenados.

Utilizaremos Google Cloud Natural Language API para el análisis de texto.

📌 Código para Análisis de Contenido (Python):

from google.cloud import language_v1

def analizar_contenido(texto):
    """Extrae palabras clave y entidades del texto usando Natural Language API."""
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=texto, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(document=document)
    
    keywords = [entity.name for entity in response.entities]
    entities = [entity.type_.name for entity in response.entities]

    return keywords, entities

📌 integrar este análisis en el pipeline de Dataflow:

Llama a analizar_contenido para cada summary en los artículos o blogs.
Almacena las palabras clave y entidades en las columnas correspondientes.

🔹 Paso 3: Análisis de Tendencias en BigQuery
📌 Objetivo:
Analizar temas más populares por tiempo y fuentes de noticias más activas.

1️⃣ Tendencias por Tema y Tiempo

SELECT topic, DATE(published_at) as fecha, COUNT(*) as total
FROM dataset_noticias.articles
GROUP BY topic, fecha
ORDER BY fecha DESC, total DESC;
2️⃣ Fuentes de Noticias Más Activas

SELECT news_site, COUNT(*) as total_articulos
FROM dataset_noticias.articles
GROUP BY news_site
ORDER BY total_articulos DESC
LIMIT 10;

🔹 Paso 4: Optimización de Consultas con Particionamiento y Caching
1️⃣ Particionamiento
Ya hemos implementado particionamiento por fecha en las tablas. Esto asegura que las consultas históricas se ejecuten sobre menos datos, reduciendo costos y tiempo de respuesta.

2️⃣ Caching de Resultados Frecuentes
Activa el resultado en caché en BigQuery para consultas que se ejecutan frecuentemente:

SELECT news_site, COUNT(*) as total_articulos
FROM dataset_noticias.articles
GROUP BY news_site
OPTIONS (allow_large_results=true)


📌 Objetivo:
Enriquecer el contenido de artículos, blogs y reportes con palabras clave, entidades y clasificación por tema.
Almacenar estos datos enriquecidos en las tablas de BigQuery optimizadas.
Utilizaremos Google Cloud Natural Language API para analizar el contenido y agregar las columnas keywords, entities y topic.

📌 Paso 1: Actualización del Pipeline de Dataflow
Código Completo para el Pipeline con Análisis de Contenido:

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import json
from google.cloud import language_v1

class FiltrarPorEndpoint(beam.DoFn):
    """Filtra los datos por endpoint y realiza análisis de contenido."""
    
    def process(self, element):
        mensaje = json.loads(element.decode('utf-8'))
        endpoint = mensaje["endpoint"]
        data = mensaje["data"]
        
        # Realiza análisis de contenido solo para artículos, blogs y reports
        if endpoint in ["/articles", "/blogs", "/reports"]:
            data["keywords"], data["entities"] = analizar_contenido(data.get("summary", ""))
            data["topic"] = clasificar_tema(data.get("summary", ""))
        
        yield beam.pvalue.TaggedOutput(endpoint.strip("/"), data)

def analizar_contenido(texto):
    """Extrae palabras clave y entidades usando Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=texto, type_=language_v1.Document.Type.PLAIN_TEXT)
    
    response = client.analyze_entities(document=document)
    keywords = [entity.name for entity in response.entities]
    entities = [entity.type_.name for entity in response.entities]
    
    return keywords, entities

def clasificar_tema(texto):
    """Clasifica el texto en temas simples (science, politics, technology, etc.)."""
    if "space" in texto.lower() or "nasa" in texto.lower():
        return "science"
    elif "technology" in texto.lower() or "AI" in texto.lower():
        return "technology"
    elif "government" in texto.lower() or "election" in texto.lower():
        return "politics"
    return "general"

def ejecutar_pipeline():
    """Pipeline principal para procesar y almacenar datos en BigQuery."""
    options = PipelineOptions(streaming=True, project="mi-proyecto", region="us-central1")

    with beam.Pipeline(options=options) as p:
        resultados = (p
                     | "Leer desde Pub/Sub" >> beam.io.ReadFromPubSub(topic="projects/mi-proyecto/topics/ingesta-noticias")
                     | "Filtrar y Analizar" >> beam.ParDo(FiltrarPorEndpoint()).with_outputs(
                         "articles", "blogs", "reports", "info")
                     )
        
        # Escribir datos enriquecidos en BigQuery para cada endpoint
        (resultados.articles
         | "Escribir en BigQuery - Articles" >> beam.io.WriteToBigQuery(
                "mi-proyecto.dataset_noticias.articles",
                schema="id:STRING, title:STRING, url:STRING, image_url:STRING, news_site:STRING, "
                       "summary:STRING, published_at:TIMESTAMP, updated_at:TIMESTAMP, "
                       "featured:BOOLEAN, launches:ARRAY<STRING>, events:ARRAY<STRING>, "
                       "keywords:ARRAY<STRING>, entities:ARRAY<STRING>, topic:STRING",
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
         )

        (resultados.blogs
         | "Escribir en BigQuery - Blogs" >> beam.io.WriteToBigQuery(
                "mi-proyecto.dataset_noticias.blogs",
                schema="id:STRING, title:STRING, url:STRING, image_url:STRING, news_site:STRING, "
                       "summary:STRING, published_at:TIMESTAMP, keywords:ARRAY<STRING>, "
                       "entities:ARRAY<STRING>, topic:STRING",
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
         )

        (resultados.reports
         | "Escribir en BigQuery - Reports" >> beam.io.WriteToBigQuery(
                "mi-proyecto.dataset_noticias.reports",
                schema="id:STRING, title:STRING, url:STRING, news_site:STRING, "
                       "published_at:TIMESTAMP, updated_at:TIMESTAMP, "
                       "keywords:ARRAY<STRING>, entities:ARRAY<STRING>, topic:STRING",
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
         )

if __name__ == "__main__":
    ejecutar_pipeline()

📌 Explicación del Código
1️⃣ Filtrado y Enriquecimiento de Datos:
La clase FiltrarPorEndpoint analiza el contenido de cada artículo, blog y reporte para extraer palabras clave, entidades y clasificar el tema usando Google Cloud Natural Language API.

2️⃣ Clasificación de Temas:
La función clasificar_tema identifica el tema principal basándose en palabras clave simples (science, technology, etc.).

3️⃣ Almacenamiento en BigQuery:
Los datos enriquecidos se almacenan en tablas separadas (articles, blogs, reports), incluyendo las nuevas columnas (keywords, entities, topic).

📌 Paso 2: Desplegar el Pipeline
1️⃣ Guardar el código como dataflow_pipeline.py.
2️⃣ Ejecutar el pipeline en Dataflow:

python dataflow_pipeline.py
🔹 Paso 3: Verificar y Visualizar los Datos
1️⃣ Consulta los datos enriquecidos en BigQuery:

SELECT title, keywords, entities, topic, published_at
FROM dataset_noticias.articles
WHERE topic = 'science'
ORDER BY published_at DESC;
2️⃣ Crear un Dashboard en Looker Studio:

Visualiza tendencias de temas y fuentes más activas.
Muestra palabras clave más comunes por tema.



🔹 Orquestación con Cloud Composer
📌 Cloud Composer es una versión gestionada de Apache Airflow en Google Cloud. Nos permite:

Automatizar el pipeline completo, desde la ingesta hasta la carga de datos en BigQuery.
Gestionar dependencias entre tareas (ej: solo procesar datos si la ingesta fue exitosa).
Programar tareas para que se ejecuten diariamente o en intervalos específicos.
Monitorear fallos y reintentos automáticos.


[Cloud Functions (Ingesta)] ---> [Dataflow (Procesamiento)] ---> [BigQuery (Almacenamiento)]
          |                             |                                |
          v                             v                                v
    [Cloud Composer (Airflow) Orquesta y Monitorea el flujo completo]



🔹 Paso 1: Crear el DAG de Airflow
Un DAG (Directed Acyclic Graph) en Airflow define el flujo de trabajo y las dependencias entre tareas.

📌 Código para el DAG (pipeline_dag.py):

from airflow import DAG
from airflow.providers.google.cloud.operators.functions import CloudFunctionInvokeFunctionOperator
from airflow.providers.google.cloud.operators.dataflow import DataflowCreatePythonJobOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from datetime import datetime, timedelta

# Definición del DAG
  default_args = {
    'owner': 'user',
    'depends_on_past': False,
    'email': ['juancarloscm@yahoo.com'],  # Correo al que se enviarán las alertas
    'email_on_failure': True,             # Enviar correo si falla la tarea
    'email_on_retry': False,              # No enviar correo en reintentos
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}


with DAG(
    'pipeline_spaceflight_news',
    default_args=default_args,
    description='Pipeline orquestado para procesar datos de Spaceflight News',
    schedule_interval='0 6 * * *',  # Corre todos los días a las 6 AM
    start_date=datetime(2024, 2, 1),
    catchup=False,
) as dag:

    # Tarea 1: Invocar la Cloud Function para la ingesta
    ingesta_task = CloudFunctionInvokeFunctionOperator(
        task_id='invocar_ingesta',
        project_id='mi-proyecto',
        location='us-central1',
        input_data={},
        function_name='ingesta_todos_endpoints'
    )

    # Tarea 2: Ejecutar el job de Dataflow para el procesamiento
    dataflow_task = DataflowCreatePythonJobOperator(
        task_id='procesar_datos_dataflow',
        py_file="gs://mi-bucket/dataflow_pipeline.py",
        job_name='dataflow-pipeline-spaceflight',
        options={
            'project': 'mi-proyecto',
            'region': 'us-central1',
            'streaming': True
        }
    )

    # Tarea 3: Verificación de datos en BigQuery
    verificar_datos_task = BigQueryExecuteQueryOperator(
        task_id='verificar_datos',
        sql='SELECT COUNT(*) FROM dataset_noticias.articles WHERE DATE(published_at) = CURRENT_DATE()',
        use_legacy_sql=False
    )

   generar_reporte_task = BigQueryExecuteQueryOperator(
    task_id='generar_reporte_tendencias',
    sql="""
        CREATE OR REPLACE TABLE dataset_noticias.reporte_tendencias AS
        SELECT 
            topic, 
            COUNT(*) AS total_articulos,
            DATE(published_at) AS fecha
        FROM dataset_noticias.articles
        WHERE DATE(published_at) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
        GROUP BY topic, fecha
        ORDER BY fecha DESC, total_articulos DESC;
    """,
    use_legacy_sql=False
)

    # Definir el flujo de ejecución
    ingesta_task >> dataflow_task >> verificar_datos_task >> generar_reporte_task

2️⃣ se sube el archivo al bucket de Cloud Composer:
gsutil cp pipeline_dag.py gs://BUCKET_DE_COMPOSER/dags/


🔹 Explicación del Código
1️⃣ Definición del DAG:

schedule_interval='0 6 * * *' programa la ejecución todos los días a las 6 AM.
default_args configura parámetros comunes para todas las tareas (reintentos, retraso entre reintentos, etc.).
2️⃣ CloudFunctionInvokeFunctionOperator: Invoca la Cloud Function para la ingesta de datos.

3️⃣ DataflowCreatePythonJobOperator: Ejecuta el script de Dataflow (dataflow_pipeline.py) que procesa y enriquece los datos.

4️⃣ BigQueryExecuteQueryOperator: Ejecuta una consulta en BigQuery para verificar que los datos fueron procesados correctamente.

5️⃣ Flujo de Ejecución (>>): Define las dependencias entre tareas. En este caso:

Primero se ejecuta la ingesta de datos,
Luego se ejecuta el procesamiento en Dataflow,
Finalmente se verifica la existencia de datos en BigQuery.







## IDE de Entendimiento del API
http://190.26.178.21/IDETestGCP/menu.php





