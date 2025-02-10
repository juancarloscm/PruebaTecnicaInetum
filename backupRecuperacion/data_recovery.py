from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.filesystem_sensor import FileSensor
from datetime import datetime, timedelta
from google.cloud import storage, bigquery
import os

# Configuración del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_recovery_pipeline',
    default_args=default_args,
    description='Recuperación automática de datos desde backups',
    schedule_interval=None,  # Este DAG se ejecuta manualmente o como fallback
    start_date=datetime(2025, 2, 1),
    catchup=False
)

# 🛠 Función para verificar la existencia del backup en Cloud Storage
def check_backup(bucket_name, prefix):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix=prefix))
    if blobs:
        print(f"Backup encontrado: {blobs[-1].name}")
        return True
    else:
        raise Exception(f"No se encontró ningún backup bajo el prefijo: {prefix}")

# 🛠 Función para restaurar datos desde Cloud Storage a la carpeta original
def restore_data_from_backup(bucket_name, backup_prefix, restore_path):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix=backup_prefix))
    
    if not blobs:
        raise Exception(f"No se encontraron backups para restaurar en {backup_prefix}")
    
    for blob in blobs:
        destination_file = os.path.join(restore_path, os.path.basename(blob.name))
        blob.download_to_filename(destination_file)
        print(f"Restaurado: {destination_file}")

# 🛠 Función para restaurar datos de BigQuery
def restore_bigquery_table(table_name, backup_uri):
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(source_format="PARQUET")
    table_ref = f"analitica-contact-center-dev.pos_analitica_ANALISIS.{table_name}"
    
    load_job = client.load_table_from_uri(backup_uri, table_ref, job_config=job_config)
    load_job.result()  # Esperar a que termine
    print(f"Tabla {table_name} restaurada desde {backup_uri}")

# 📂 Verificar existencia del backup en Cloud Storage
check_backup_task = PythonOperator(
    task_id='check_backup',
    python_callable=check_backup,
    op_kwargs={
        'bucket_name': 'buckets-aws-backup',
        'prefix': 'processed_data/'
    },
    dag=dag
)

# 📂 Restaurar datos intermedios desde Cloud Storage
restore_storage_task = PythonOperator(
    task_id='restore_data_from_backup',
    python_callable=restore_data_from_backup,
    op_kwargs={
        'bucket_name': 'buckets-aws-backup',
        'backup_prefix': 'processed_data/',
        'restore_path': '/tmp/restore/'
    },
    dag=dag
)

# 📂 Restaurar tabla `topic_trends` desde BigQuery backup
restore_topic_trends_task = PythonOperator(
    task_id='restore_topic_trends',
    python_callable=restore_bigquery_table,
    op_kwargs={
        'table_name': 'topic_trends',
        'backup_uri': 'gs://buckets-aws-backup/bigquery/topic_trends_*.parquet'
    },
    dag=dag
)

# 📂 Restaurar tabla `company_mentions` desde BigQuery backup
restore_company_mentions_task = PythonOperator(
    task_id='restore_company_mentions',
    python_callable=restore_bigquery_table,
    op_kwargs={
        'table_name': 'company_mentions',
        'backup_uri': 'gs://buckets-aws-backup/bigquery/company_mentions_*.parquet'
    },
    dag=dag
)

# 📂 Restaurar tabla `place_mentions` desde BigQuery backup
restore_place_mentions_task = PythonOperator(
    task_id='restore_place_mentions',
    python_callable=restore_bigquery_table,
    op_kwargs={
        'table_name': 'place_mentions',
        'backup_uri': 'gs://buckets-aws-backup/bigquery/place_mentions_*.parquet'
    },
    dag=dag
)

# 🔗 Definir las dependencias
check_backup_task >> restore_storage_task >> [restore_topic_trends_task, restore_company_mentions_task, restore_place_mentions_task]

