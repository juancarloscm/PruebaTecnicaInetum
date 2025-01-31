from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime, timedelta
import requests
import json
import pandas as pd
import csv 

BUCKET_NAME = 'us-central1-flujotransacion-9cfbfa36-bucket'
GCS_FILE_PATH = 'noticias/noticias.csv'
LOCAL_JSON_PATH = '/tmp/noticias.json'
LOCAL_CSV_PATH = '/tmp/noticias.csv'
BQ_TABLE = 'analitica-contact-center-dev.transacional_linea.noticias'

def extraer_noticias():
    url = "https://api.spaceflightnewsapi.net/v4/articles/"
    response = requests.get(url)
    data = response.json()

    noticias = []
    for articulo in data["results"]:
        noticias.append({
            "id": str(articulo["id"]),  # Convertir a string si es necesario
            "title": articulo["title"],
            "news_site": articulo["news_site"],
            "published_at": articulo["published_at"],
            "summary": articulo["summary"][:5000]  # Limitar tamaño a evitar truncamiento
        })

    with open(LOCAL_JSON_PATH, "w") as f:
        json.dump(noticias, f)



def convertir_json_a_csv():
    df = pd.read_json("/tmp/noticias.json")

    # Asegurar que los tipos de datos sean correctos
    df["id"] = df["id"].astype(str)
    df["title"] = df["title"].astype(str)
    df["news_site"] = df["news_site"].astype(str)
    df["published_at"] = pd.to_datetime(df["published_at"])
    df["summary"] = df["summary"].astype(str).str.replace('\n', ' ').str[:5000]  # Eliminar saltos de línea

    # Evitar valores nulos
    df = df.fillna('')

    # Guardar CSV asegurando delimitadores correctos
    df.to_csv("/tmp/noticias.csv", index=False, quoting=csv.QUOTE_ALL, escapechar='\\')


def contar_registros_a_insertar():
    df = pd.read_csv(LOCAL_CSV_PATH)
    print(f"Registros a insertar: {len(df)}")

definir_parametros_dag = {
    'dag_id': 'dag_noticias_bigquery',
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
    extraer_noticias_tarea = PythonOperator(
        task_id='extraer_noticias',
        python_callable=extraer_noticias
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
        src=LOCAL_CSV_PATH,
        dst=GCS_FILE_PATH,
        bucket=BUCKET_NAME,
        mime_type='text/csv'
    )

    subir_a_bigquery = GCSToBigQueryOperator(
        task_id='subir_datos_a_bigquery',
        bucket=BUCKET_NAME,
        source_objects=[GCS_FILE_PATH],
        destination_project_dataset_table=BQ_TABLE,
        write_disposition="WRITE_TRUNCATE",
        create_disposition="CREATE_IF_NEEDED",
        source_format="CSV",
        skip_leading_rows=1,
        autodetect=False,
        schema_fields=[
            {"name": "id", "type": "STRING", "mode": "NULLABLE"},
            {"name": "title", "type": "STRING", "mode": "NULLABLE"},
            {"name": "news_site", "type": "STRING", "mode": "NULLABLE"},
            {"name": "published_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
            {"name": "summary", "type": "STRING", "mode": "NULLABLE"}
        ]
    )

    extraer_noticias_tarea >> convertir_a_csv >> contar_registros >> subir_a_gcs >> subir_a_bigquery
