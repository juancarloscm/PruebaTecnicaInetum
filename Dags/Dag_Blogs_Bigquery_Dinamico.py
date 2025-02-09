from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateClusterOperator, DataprocDeleteClusterOperator, DataprocSubmitJobOperator
from google.cloud import storage
import requests
import json
import time
from datetime import datetime, timedelta

# Establecer de parametros del DAG
parametros_dag = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definicion del DAG
flujo_datos = DAG(
    'etl_almacen_datos_noticias',
    default_args=parametros_dag,
    schedule_interval='@daily',
    catchup=False
)

# Configuracion de las variables
BUCKET_NAME = "us-central1-flujotransacion-9cfbfa36-bucket"
API_URLS = {
    "articles": "https://api.spaceflightnewsapi.net/v4/articles/",
    "blogs": "https://api.spaceflightnewsapi.net/v4/blogs/",
    "reports": "https://api.spaceflightnewsapi.net/v4/reports/"
}

# Se define una funcion para extraer datos con paginacion, manejo de rate limits y deduplicación
# Manejo de rate limits con espera 5
def extraer_y_guardar(tipo):
    headers = {"User-Agent": "airflow-etl"}
    page = 1
    all_data = []
    seen_ids = set()
    
    while True:
        response = requests.get(f"{API_URLS[tipo]}?page={page}", headers=headers)
        if response.status_code == 429:
            time.sleep(5)  
            continue
        elif response.status_code != 200:
            break
        
        data = response.json()["results"]
        if not data:
            break
        
        # Deduplicación de articulos
        unique_data = [item for item in data if item["id"] not in seen_ids]
        seen_ids.update(item["id"] for item in unique_data)
        
        all_data.extend(unique_data)
        page += 1
    
    # Se guarda el  JSON localmente
    file_path = f"/tmp/{tipo}.json"
    with open(file_path, "w") as f:
        json.dump(all_data, f)
    
    # Se sube a GCS
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"datos_raw/{tipo}.json")
    blob.upload_from_filename(file_path)
    print(f"Archivo {tipo}.json subido a GCS")

# Crear tareas para extraer y guardar los datos
tareas_extraccion = []
for tipo in API_URLS.keys():
    tarea = PythonOperator(
        task_id=f"extraer_{tipo}",
        python_callable=extraer_y_guardar,
        op_kwargs={"tipo": tipo},
        dag=flujo_datos,
    )
    tareas_extraccion.append(tarea)

# Crear cluster de Dataproc con sus parametros
crear_cluster = DataprocCreateClusterOperator(
    task_id="crear_cluster_dataproc",
    project_id="analitica-contact-center-dev",
    cluster_name="cluster-temporal",
    region="us-central1",
    num_workers=2,
    master_machine_type="n1-standard-4",
    worker_machine_type="n1-standard-2",
    dag=flujo_datos,
)

# Procesar datos en Dataproc con Spark
procesar_datos = DataprocSubmitJobOperator(
    task_id="procesar_datos_spark",
    project_id="analitica-contact-center-dev",
    region="us-central1",
    job={
        "reference": {"project_id": "analitica-contact-center-dev"},
        "placement": {"cluster_name": "cluster-temporal"},
        "pyspark_job": {
            #"main_python_file_uri": f"gs://{BUCKET_NAME}/scripts/procesamiento_spark.py"
            #"main_python_file_uri": f"gs://{BUCKET_NAME}/scripts/procesamiento_spark.py"
        }
    },
    dag=flujo_datos,
)

# Luego Elimina el cluster despues del procesamiento
eliminar_cluster = DataprocDeleteClusterOperator(
    task_id="eliminar_cluster_dataproc",
    project_id="analitica-contact-center-dev",
    cluster_name="cluster-temporal",
    region="us-central1",
    dag=flujo_datos,
)

# Cargar la tabla de noticias_procesadas en BigQuery
cargar_datos_bigquery = BigQueryInsertJobOperator(
    task_id="cargar_datos_bigquery",
    configuration={"query": {"query": """
        MERGE INTO `analitica-contact-center-dev.Entorno_Pruebas_modelo.noticias_procesadas` AS destino
        USING (
            SELECT DISTINCT 
                ROW_NUMBER() OVER() AS id_articulo,
                news_site AS fuente,
                TIMESTAMP(published_at) AS fecha_publicacion,
                title AS titulo,
                summary AS resumen,
                url,
                CAST(FLOOR(RAND()*1000) AS INT64) AS visitas,
                CAST(FLOOR(RAND()*500) AS INT64) AS compartidos
            FROM `analitica-contact-center-dev.Entorno_Pruebas_modelo.noticias_raw`
        ) AS fuente
        ON destino.id_articulo = fuente.id_articulo
        WHEN NOT MATCHED THEN
            INSERT (id_articulo, fuente, fecha_publicacion, titulo, resumen, url, visitas, compartidos)
            VALUES (fuente.id_articulo, fuente.fuente, fuente.fecha_publicacion, fuente.titulo, fuente.resumen, fuente.url, fuente.visitas, fuente.compartidos);
    """, "useLegacySql": False}},
    dag=flujo_datos,
)

# Orden de ejecucion de la tareas
tareas_extraccion >> crear_cluster >> procesar_datos >> eliminar_cluster >> cargar_datos_bigquery

