from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'limpieza_blogs_bigquery',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)
 
# PARTITION BY title, published_at → Agrupa por título y fecha de publicación.
# ORDER BY published_at DESC → Se queda con el artículo más reciente.
# WHERE row_num = 1 → Filtra solo la primera aparición de cada grupo.


query = """
CREATE OR REPLACE TABLE `analitica-contact-center-dev.transacional_linea.blogs_cleaned` AS
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY title, published_at ORDER BY published_at DESC) AS row_num
    FROM `analitica-contact-center-dev.transacional_linea.blogs`
)
WHERE row_num = 1;
"""

limpiar_blogs = BigQueryInsertJobOperator(
    task_id="limpiar_blogs",
    configuration={
        "query": {
            "query": query,
            "useLegacySql": False,
        }
    },
    dag=dag,
)

limpiar_blogs
