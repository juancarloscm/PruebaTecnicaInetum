Pipeline de Análisis de Tendencias en la Industria Espacial 🚀


* Descripción del Proyecto
Este proyecto implementa un pipeline de datos utilizando la API de Spaceflight News para extraer, procesar y analizar información sobre la industria espacial. Se emplea Google Cloud Composer (Airflow) para orquestar las tareas, BigQuery para almacenamiento y análisis, y Dataproc (Spark) para procesamiento distribuido.



* Arquitectura
🛰 Extracción: Datos de artículos, blogs y reportes desde la API de Spaceflight News.
🛰 Procesamiento: Limpieza, deduplicación y análisis con Apache Spark en Dataproc.
🛰 Almacenamiento: Google Cloud Storage (GCS) para datos crudos y BigQuery para análisis estructurado.
🛰 Orquestación: Cloud Composer (Airflow) para la ejecución automatizada del pipeline.
🛰 Análisis: Queries en BigQuery para identificar tendencias y fuentes más relevantes.

* Tecnologías Utilizadas
🔹 Extracción de datos: Python + Requests + API Spaceflight News
🔹 Procesamiento: Apache Spark sobre Dataproc
🔹 Almacenamiento: Google Cloud Storage (GCS) y BigQuery
🔹 Orquestación: Cloud Composer (Airflow)
🔹 Análisis SQL: Queries en BigQuery

* Flujo del Pipeline
1️⃣ Ingesta: DAG de Airflow extrae datos de la API y los guarda en GCS.
2️⃣ Procesamiento: Job en Dataproc (Spark) limpia, deduplica y clasifica los datos.
3️⃣ Almacenamiento: Los datos transformados se almacenan en BigQuery.
4️⃣ Análisis: Queries para tendencias por mes y ranking de fuentes influyentes.
5️⃣ Automatización: Airflow ejecuta el flujo de trabajo diariamente.

* Instalación y Configuración
1. Clonar el Repositorio
bash
Copiar
Editar
git clone https://github.com/tuusuario/spaceflight-pipeline.git
cd spaceflight-pipeline
2. Configurar Variables de Entorno
bash
Copiar
Editar
export PROJECT_ID="tu-proyecto-gcp"
export BUCKET_NAME="tu-bucket-gcs"
export BIGQUERY_DATASET="tu-dataset-bigquery"
export API_URL="https://api.spaceflightnewsapi.net/v4"
3. Implementar Airflow en Cloud Composer
Crear un entorno de Cloud Composer en GCP:
bash
Copiar
Editar
gcloud composer environments create spaceflight-pipeline \
  --location us-central1 \
  --image-version composer-2-airflow-2
Configurar el DAG en Airflow:
Subir el archivo spaceflight_dag.py al bucket de Cloud Composer:
bash
Copiar
Editar
gsutil cp dags/spaceflight_dag.py gs://tu-bucket-composer/dags/
Verificar la ejecución en la interfaz de Cloud Composer.
4. Ejecutar el Pipeline Manualmente
bash
Copiar
Editar
gcloud composer environments run spaceflight-pipeline \
    --location us-central1 trigger_dag -- spaceflight_dag
Consultas SQL en BigQuery

Ejemplo de consulta para tendencias de temas por mes:

sql
Copiar
Editar
SELECT topic, COUNT(*) as cantidad, DATE_TRUNC(published_at, MONTH) as mes
FROM `tu-proyecto-gcp.tu-dataset.fact_article`
GROUP BY topic, mes
ORDER BY mes DESC, cantidad DESC;

Tareas Pendientes
☑️ Optimizar particionamiento de BigQuery para mejorar consultas.
☑️ Implementar dashboard en Looker Studio.
☑️ Agregar más métricas para evaluar impacto de noticias.

📌 Contacto: juancarloscm@yahoo.com
