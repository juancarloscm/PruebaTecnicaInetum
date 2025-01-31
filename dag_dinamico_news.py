from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from datetime import datetime, timedelta
import requests
import json
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_exponential

def verificar_api():
    """Verifica si la API está disponible antes de extraer datos."""
    url = "https://api.spaceflightnewsapi.net/v4/blogs/"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("La API no está disponible")

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10))
def extraer_blogs():
    url = "https://api.spaceflightnewsapi.net/v4/blogs/"
    response = requests.get(url)
    data = response.json()
    
    blogs = []
    for blog in data.get("results", []):
        blogs.append({
            "id": blog["id"],
            "title": blog["title"],
            "authors": blog.get("news_site", ""),
            "published_at": blog["published_at"],
            "summary": blog["summary"]
        })
    
    with open("/tmp/blogs.json", "w") as f:
        json.dump(blogs, f)

def convertir_json_a_csv():
    df = pd.read_json("/tmp/blogs.json")
    df.to_csv("/tmp/blogs.csv", index=False, quoting=1, escapechar='\\')

def contar_registros_a_insertar():
    df = pd.read_csv("/tmp/blogs.csv")
    print(f"Registros a insertar: {len(df)}")

definir_parametros_dag = {
    'dag_id': 'dag_blogs_bigquery',
    'schedule_interval': '@daily',
    'start_date': datetime(2024, 1, 1),
    'catchup': False,
    'default_args': {
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
}

with DAG(**definir_parametros_dag) as dag:
    verificar_api_tarea = PythonOperator(
        task_id='verificar_api',
        python_callable=verificar_api
    )
    
    extraer_blogs_tarea = PythonOperator(
        task_id='extraer_blogs',
        python_callable=extraer_blogs
    )
    
    convertir_a_csv = PythonOperator(
        task_id='convertir_json_a_csv',
        python_callable=convertir_json_a_csv
    )
    
    contar_registros = PythonOperator(
        task_id='contar_registros_a_insertar',
        python_callable=contar_registros_a_insertar
    )
    
    subir_a_gcs = LocalFilesystemToGCSOperator(
        task_id='subir_a_gcs',
        src='/tmp/blogs.csv',
        dst='blogs.csv',
        bucket='us-central1-flujotransacion-9cfbfa36-bucket',
        mime_type='text/csv'
    )
    
    subir_a_bigquery = GCSToBigQueryOperator(
        task_id='subir_datos_a_bigquery',
        bucket='us-central1-flujotransacion-9cfbfa36-bucket',
        source_objects=['blogs.csv'],
        destination_project_dataset_table='analitica-contact-center-dev.transacional_linea.blogs',
        write_disposition='WRITE_TRUNCATE',
        source_format='CSV',
        skip_leading_rows=1,
        autodetect=False,
        schema_fields=[
            {"name": "id", "type": "STRING", "mode": "NULLABLE"},
            {"name": "title", "type": "STRING", "mode": "NULLABLE"},
            {"name": "authors", "type": "STRING", "mode": "NULLABLE"},
            {"name": "published_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
            {"name": "summary", "type": "STRING", "mode": "NULLABLE"}
        ]
    )
    
    verificar_api_tarea >> extraer_blogs_tarea >> convertir_a_csv >> contar_registros >> subir_a_gcs >> subir_a_bigquery



