from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime, timedelta
import requests

# Configuración del DAG principal
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_pipeline_with_fallback',
    default_args=default_args,
    description='Pipeline principal con fallback automático',
    schedule_interval='0 3 * * *',  # Ejecución diaria a las 3:00 AM
    start_date=datetime(2025, 2, 1),
    catchup=False
)

# 🛠 Función de ejemplo para simular una tarea crítica
def critical_task():
    response = requests.get("https://api.spaceflightnewsapi.net/v4/articles")
    if response.status_code != 200:
        raise Exception("Error al extraer datos. Activando el fallback...")

# Tarea crítica del DAG principal
critical_task = PythonOperator(
    task_id='critical_task',
    python_callable=critical_task,
    dag=dag
)

# 🔄 Trigger para activar el DAG de recuperación (data_recovery_pipeline)
trigger_fallback = TriggerDagRunOperator(
    task_id='trigger_data_recovery',
    trigger_dag_id='data_recovery_pipeline',  # DAG de recuperación
    dag=dag
)

# 📂 Definir dependencias
critical_task >> trigger_fallback

