Mejoras al modelo:

📌 Integración con Machine Learning en GCP 🚀
Integrar Machine Learning (ML) en el pipeline para predecir la popularidad de articulos o clasificarlos automaticamente en categorías con modelos de Vertex AI y BigQuery ML.



Opción 1: Entrenar un Modelo con BigQuery ML
Podemos usar BigQuery ML para predecir la popularidad de los artículos en función de su fuente, título y otros atributos.

-- 🔹 Entrenar un Modelo de Predicción de Popularidad
CREATE OR REPLACE MODEL 
    `analitica-contact-center-dev.Entorno_Pruebas_modelo.modelo_prediccion_popularidad`
OPTIONS(
    model_type='LINEAR_REG',
    input_label_cols=['impacto_total']
) AS
SELECT 
    f.nombre AS fuente,
    a.titulo,
    a.visitas,
    a.compartidos,
    (a.visitas + a.compartidos) AS impacto_total
FROM `analitica-contact-center-dev.Entorno_Pruebas_modelo.fact_articulos` a
JOIN `analitica-contact-center-dev.Entorno_Pruebas_modelo.dim_fuentes_noticias` f
ON a.source_id = f.source_id;

📌 Explicación:
✅ Entrena un modelo de Regresión Lineal con BigQuery ML
✅ Usa datos históricos de visitas y compartidos como etiquetas
✅ Predice el impacto de nuevos artículos


🔹 Hacer Predicciones sobre Nuevos Artículos
SELECT 
    titulo, 
    fuente,
    predicted_impacto_total
FROM ML.PREDICT(
    MODEL `analitica-contact-center-dev.Entorno_Pruebas_modelo.modelo_prediccion_popularidad`,
    (
        SELECT 'Nuevo Artículo sobre Marte' AS titulo, 'NASA' AS fuente, 100 AS visitas, 50 AS compartidos
    )
);

📌 Explicación:
✅ Usa el modelo entrenado para predecir la popularidad de un nuevo artículo
✅ Puede integrarse con Airflow para ejecutarse automáticamente


Opción 2: Clasificación de Artículos con Vertex AI
Otra opción es usar Vertex AI para clasificar automáticamente los artículos en temas relevantes.

🔹 Entrenar un Modelo de Clasificación en Vertex AI
1️⃣ Sube los datos a GCS
bq extract --destination_format CSV \
    analitica-contact-center-dev.Entorno_Pruebas_modelo.fact_articulos \
    gs://us-central1-flujotransacion-9cfbfa36-bucket/ml_data/articulos.csv

2️⃣ Crea un Dataset en Vertex AI y entrena un modelo AutoML
gcloud ai datasets create --display-name="Dataset Noticias" --metadata-schema-uri=gs://google-cloud-aiplatform/schema/dataset/schema-tabular-1.0.0.yaml

3️⃣ Desplegar el modelo y hacer inferencias

gcloud ai endpoints create --display-name="Clasificador Noticias"
gcloud ai models deploy --model=projects/analitica-contact-center-dev/models/clasificador_noticias

🔹 Realizar una Predicción con el Modelo
gcloud ai endpoints predict \
    --endpoint=projects/analitica-contact-center-dev/endpoints/clasificador_noticias \
    --json-request=prediccion.json
📌 Explicación:
✅ Usa AutoML en Vertex AI para clasificar automáticamente los artículos
✅ Se puede conectar con BigQuery para análisis más avanzado


✅ 3️⃣ Integración en el DAG de Airflow
Podemos agregar una tarea en Airflow que ejecute predicciones usando el modelo de Vertex AI.

from airflow.providers.google.cloud.operators.vertex_ai import VertexAIEndpointPredictOperator

predecir_popularidad = VertexAIEndpointPredictOperator(
    task_id='predecir_popularidad_articulos',
    endpoint_id='clasificador_noticias',
    project_id='analitica-contact-center-dev',
    region='us-central1',
    instances=[
        {"titulo": "Nuevo descubrimiento en Marte", "fuente": "NASA"}
    ],
    gcp_conn_id='google_cloud_default'
)

📌 Explicación:
✅ Ejecuta predicciones automáticas dentro del pipeline
✅ Permite automatizar decisiones en base a predicciones ML


🎯 Conclusión
✅ BigQuery ML → Predecir la popularidad de artículos
✅ Vertex AI (AutoML) → Clasificar artículos automáticamente
✅ Airflow → Automatizar predicciones dentro del pipeline






