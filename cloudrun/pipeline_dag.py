from airflow import DAG
from airflow.providers.google.cloud.operators.functions import CloudFunctionInvokeFunctionOperator
from airflow.providers.google.cloud.operators.dataflow import DataflowCreatePythonJobOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'user',
    'depends_on_past': False,
    'email': ['tu_correo@ejemplo.com'],
    'email_on_failure': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'pipeline_spaceflight_news',
    default_args=default_args,
    description='Pipeline orquestado para procesar datos de Spaceflight News',
    schedule_interval='0 6 * * *',
    start_date=datetime(2024, 2, 1),
    catchup=False,
) as dag:

    ingesta_task = CloudFunctionInvokeFunctionOperator(
        task_id='invocar_ingesta',
        project_id='mi-proyecto',
        location='us-central1',
        function_name='ingesta_todos_endpoints'
    )

    dataflow_task = DataflowCreatePythonJobOperator(
        task_id='procesar_datos_dataflow',
        py_file="gs://mi-bucket/dataflow_pipeline.py",
        job_name='dataflow-pipeline-spaceflight',
        options={'project': 'mi-proyecto', 'region': 'us-central1', 'streaming': True}
    )

    verificar_datos_task = BigQueryExecuteQueryOperator(
        task_id='verificar_datos',
        sql='SELECT COUNT(*) FROM dataset_noticias.articles WHERE DATE(published_at) = CURRENT_DATE()',
        use_legacy_sql=False
    )

    generar_reporte_task = BigQueryExecuteQueryOperator(
        task_id='generar_reporte_tendencias',
        sql="""
            CREATE OR REPLACE TABLE dataset_noticias.reporte_tendencias AS
            SELECT topic, COUNT(*) AS total_articulos, DATE(published_at) AS fecha
            FROM dataset_noticias.articles
            WHERE DATE(published_at) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
            GROUP BY topic, fecha
            ORDER BY fecha DESC, total_articulos DESC;
        """,
        use_legacy_sql=False
    )

    ingesta_task >> dataflow_task >> verificar_datos_task >> generar_reporte_task
