#  Pipeline de Analisis de Tendencias en la Industria Espacial 
#  Proyecto: ETL y Análisis de Noticias en GCP

## 📌 Descripción
Este proyecto implementa un pipeline de **ETL (Extract, Transform, Load)** en **Google Cloud Platform (GCP)** para extraer datos de la API de **Spaceflight News**, transformarlos con **Apache Spark en Dataproc**, y almacenarlos en **Google BigQuery** para análisis y visualización.

**OPCION 1:**

## ⚙️ Herramientas Utilizadas
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
- ** 1️⃣ **Extracción de Datos**: Se extraen noticias desde la API de **Spaceflight News**, manejando paginación y rate limits.
- ** 2️⃣ **Almacenamiento en GCS**: Los datos se guardan en formato **JSON y Parquet** en Google Cloud Storage.
- ** 3️⃣ **Procesamiento en Dataproc (Spark)**: Limpieza, deduplicación y análisis de contenido y tendencias.
- ** 4️⃣ **Carga en BigQuery**: Se insertan datos normalizados en un modelo dimensional.
- ** 5️⃣ **Análisis SQL**: Se ejecutan consultas optimizadas para tendencias y reportes.
- ** 6️⃣ **Visualización en Looker Studio**: Se crean dashboards para análisis de datos.

## 🛠 Configuración y Despliegue
- ** ### 1️⃣ Subir el DAG a Composer
```sh
gsutil cp dags/etl_almacen_datos_noticias.py gs://us-central1-flujotransacion-9cfbfa36-bucket/dags/
```

- ** ### 2️⃣ Subir Script de Spark a GCS
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
### 🔹 **Tendencias de temas por mes** analisis_tendencias.sql 

### 🔹 **Fuentes de noticias mas influyentes** fuentes_mas_influyentes.sql

## 📈 Visualización en Looker Studio
Conectar **BigQuery** con **Looker Studio** para crear un dashboards interactivo y visualizar tendencias en los datos.

## 📌 Conclusión
✔ **Pipeline optimizado con particionamiento y clustering en BigQuery**  
✔ **Procesamiento escalable en Dataproc con Apache Spark**  
✔ **Orquestación eficiente con Airflow en Cloud Composer**  
✔ **Visualización intuitiva en Looker Studio**  



**OPCION 2**

## Propuesta de Mejora del Modelo con 100% serveless
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

##  Sistema de Backup y Recuperación
- ** Backup de datos críticos (almacenados en Cloud Storage, BigQuery, y metadatos del pipeline).
- ** Automatización de backups periódicos.
- ** Recuperación rápida en caso de fallo o pérdida de datos.

## 📊 Resumen de la Arquitectura de Backup
- ** Cloud Storage para respaldar datos intermedios y JSON de entrada.
- ** BigQuery Export para respaldar tablas finales.
- ** Cloud Scheduler para ejecutar tareas automáticas.
- ** Google Cloud Monitoring para detectar y alertar sobre errores.


 ## 🛠 Estrategia de Implementación
- ** 1. Backup en Google Cloud Storage
- ** 📦 Datos a respaldar:
- ** Datos intermedios (cleaned_data.parquet, analyzed_data.parquet).
- ** Archivos JSON de entrada (articles.json, blogs.json).
- ** 💡 Cómo implementarlo:
- ** Configura versiones de objetos en tu bucket (Object Versioning).
- ** Automatiza los backups con un script y programa la tarea en Cloud Scheduler.

- ** 2. Backup de BigQuery
- ** 📦 Datos a respaldar:
- ** Tablas finales (topic_trends, company_mentions, place_mentions).
- ** 💡 Cómo implementarlo:
- ** Exporta las tablas a Cloud Storage en formato Avro o Parquet.

- ** 3. Recuperación de Datos
- ** Datos en Cloud Storage:
- ** Si tienes versiones anteriores, puedes restaurarlas directamente.
- **  gsutil cp gs://buckets-aws-backup/processed_data_20250201 gs://buckets-aws/processed_data

- ** Datos en BigQuery:
- ** Si las tablas se perdieron, puedes volver a importarlas desde el backup en Cloud Storage.
- ** bq load \
- **   --source_format=PARQUET \
- **  "analitica-contact-center-dev:pos_analitica_ANALISIS.topic_trends" \
- **  "gs://buckets-aws-backup/bigquery/topic_trends_20250201.parquet"

- ** 4. Monitorización y Alertas
- ** Se Configura Google Cloud Monitoring para recibir alertas en caso de:
- ** Fallos en las tareas de backup.
- ** Falta de espacio en Cloud Storage.
- ** Fallos de importación en BigQuery.





## IDE de Entendimiento del API
http://190.26.178.21/IDETestGCP/menu.php





