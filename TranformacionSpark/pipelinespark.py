from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta
import requests

# Configuración del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_analysis_pipeline',
    default_args=default_args,
    description='Pipeline para extracción, análisis y carga de datos',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2025, 2, 1),
    catchup=False
)

# 🛠️ Funciones de extracción de datos
def extract_articles():
    response = requests.get("https://api.spaceflightnewsapi.net/v4/articles")
    with open('/tmp/articles.json', 'w') as f:
        f.write(response.text)

def extract_blogs():
    response = requests.get("https://api.spaceflightnewsapi.net/v4/blogs")
    with open('/tmp/blogs.json', 'w') as f:
        f.write(response.text)

def extract_reports():
    response = requests.get("https://api.spaceflightnewsapi.net/v4/reports")
    with open('/tmp/reports.json', 'w') as f:
        f.write(response.text)

# 🧩 Operadores de extracción
extract_articles = PythonOperator(
    task_id='extract_articles',
    python_callable=extract_articles,
    dag=dag
)

extract_blogs = PythonOperator(
    task_id='extract_blogs',
    python_callable=extract_blogs,
    dag=dag
)

extract_reports = PythonOperator(
    task_id='extract_reports',
    python_callable=extract_reports,
    dag=dag
)

# 🧹 Limpieza y deduplicación con Spark
limpia_y_deduplica = SparkSubmitOperator(
    task_id='limpia_y_deduplica',
    application='gs://buckets-aws/scripts/clean_and_deduplicate.py',
    name='limpia_y_deduplica-job',
    conn_id='spark_default',
    dag=dag
)

# 📊 Análisis y temas con Spark
proceso_analisis = SparkSubmitOperator(
    task_id='proceso_analisis',
    application='gs://buckets-aws/scripts/perform_analysis.py',
    name='proceso_analisis-job',
    conn_id='spark_default',
    dag=dag
)

identifica_topics = SparkSubmitOperator(
    task_id='identifica_topics',
    application='gs://buckets-aws/scripts/identify_topics.py',
    name='identifica_topics-job',
    conn_id='spark_default',
    dag=dag
)

# 📥 Carga de datos procesados y generación de insights
def load_data_to_bigquery():
    # Aquí se implementa la lógica para cargar los datos en BigQuery
    print("Cargando datos en BigQuery...")

def generate_daily_insights():
    # Aquí se generan los insights diarios basados en los datos procesados
    print("Generando insights diarios...")

def update_dashboards():
    # Aquí se actualizan los dashboards con la información más reciente
    print("Actualizando dashboards...")

cargue_datos_procesados = PythonOperator(
    task_id='cargue_datos_procesados',
    python_callable=load_data_to_bigquery,
    dag=dag
)

generate_daily_insights = PythonOperator(
    task_id='generate_daily_insights',
    python_callable=generate_daily_insights,
    dag=dag
)

update_dashboards = PythonOperator(
    task_id='update_dashboards',
    python_callable=update_dashboards,
    dag=dag
)

# 🔗 Definición de dependencias entre tareas
[extract_articles, extract_blogs, extract_reports] >> limpia_y_deduplica
limpia_y_deduplica >> [proceso_analisis, identica_topics]
[proceso_analisis, identifica_topics] >> cargue_datos_procesados
cargue_datos_procesados >> generate_daily_insights >> update_dashboards

