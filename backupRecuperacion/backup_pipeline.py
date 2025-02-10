from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from google.cloud import bigquery
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
    'backup_pipeline',
    default_args=default_args,
    description='Backup diario de datos de Cloud Storage y BigQuery',
    schedule_interval='0 3 * * *',  # Corre todos los días a las 3:00 AM
    start_date=datetime(2025, 2, 1),
    catchup=False
)

# 🛠 Función para hacer backup de una tabla de BigQuery
def backup_bigquery_table(table_name, destination_uri):
    client = bigquery.Client()
    job_config = bigquery.ExtractJobConfig(destination_format="PARQUET")
    table_ref = f"analitica-contact-center-dev.pos_analitica_ANALISIS.{table_name}"
    client.extract_table(table_ref, destination_uri, job_config=job_config).result()
    print(f"Backup de {table_name} completado en {destination_uri}")

# 📥 Backup de datos intermedios (Cloud Storage)
backup_storage = BashOperator(
    task_id='backup_cloud_storage',
    bash_command="""
    gsutil cp -r gs://buckets-aws/processed_data gs://buckets-aws-backup/processed_data_{{ ds_nodash }}
    """,
    dag=dag
)

# 📥 Backup de tabla `topic_trends`
backup_topic_trends = PythonOperator(
    task_id='backup_topic_trends',
    python_callable=backup_bigquery_table,
    op_kwargs={
        'table_name': 'topic_trends',
        'destination_uri': 'gs://buckets-aws-backup/bigquery/topic_trends_{{ ds_nodash }}.parquet'
    },
    dag=dag
)

# 📥 Backup de tabla `company_mentions`
backup_company_mentions = PythonOperator(
    task_id='backup_company_mentions',
    python_callable=backup_bigquery_table,
    op_kwargs={
        'table_name': 'company_mentions',
        'destination_uri': 'gs://buckets-aws-backup/bigquery/company_mentions_{{ ds_nodash }}.parquet'
    },
    dag=dag
)

# 📥 Backup de tabla `place_mentions`
backup_place_mentions = PythonOperator(
    task_id='backup_place_mentions',
    python_callable=backup_bigquery_table,
    op_kwargs={
        'table_name': 'place_mentions',
        'destination_uri': 'gs://buckets-aws-backup/bigquery/place_mentions_{{ ds_nodash }}.parquet'
    },
    dag=dag
)

# 🔗 Definir las dependencias
backup_storage >> [backup_topic_trends, backup_company_mentions, backup_place_mentions]

