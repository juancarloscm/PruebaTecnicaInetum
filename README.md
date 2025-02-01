#  Pipeline de Analisis de Tendencias en la Industria Espacial 🚀
# 🚀 Proyecto: ETL y Análisis de Noticias en GCP

## 📌 Descripcion
Este proyecto implementa un pipeline de **ETL (Extract, Transform, Load)** en **Google Cloud Platform (GCP)** para extraer datos de la API de **Spaceflight News**, transformarlos con **Apache Spark en Dataproc**, y almacenarlos en **Google BigQuery** para análisis y visualización.

## ⚙️ Tecnologias Utilizadas
- **Google Cloud Composer (Airflow)** - Orquestación del pipeline.
- **Google Cloud Storage (GCS)** - Almacenamiento intermedio de datos.
- **Google BigQuery** - Data Warehouse para análisis y reportes.
- **Google Dataproc (Spark)** - Transformación y procesamiento de datos.
- **Looker Studio** - Visualización de datos.

## 📁 Estructura del Proyecto
```
├── Dags/
│   ├── Dag_blogs_Biquery_Dinamico # etl_almacen_datos_noticias.py-DAG principal en Airflow
│── Data_Warehouse_Bigquery/
│   ├── Fuentes_Noticias_mas_Influyentes.sql  
│   ├── Tablas.sql  # sql creacion de tablas 
│   ├── Tendencias_Temas_mes.sql  # sql Tendencias
│── sql/
│   ├── Relacion_tablas.sql
│   ├── dim_fuentes_noticias.sql
│   ├── dim_temas.sql
│   ├── noticias_procesadas.sql
│── scripts/
│   ├── procesamiento_spark.py  # Transformaciones con Spark en Dataproc
│── test_Unitarios/
│   ├── test_conectividad_bigquery.py  # Test de integridad del DAG
│   ├── test_dag.py  # Test de validación en BigQuery
│── arquitecturas/
│   ├── Parte1_Arquitectura_Pipeline
│   ├── test_bigquery.py  # Test de validación en BigQuery
│── procesamiento/
│   ├── comandos.txt  #
│   ├── procesamiento_spark.py  #
│   ├── procesamiento_spark_funciones.py  #
│   ├── procesamiento_spark_optimizado.py  #
│── README.md  # Documentación
```

## 🚀 Flujo del Pipeline
1️⃣ **Extracción de Datos**: Se extraen noticias desde la API de **Spaceflight News**, manejando paginación y rate limits.
2️⃣ **Almacenamiento en GCS**: Los datos se guardan en formato **JSON y Parquet** en Google Cloud Storage.
3️⃣ **Procesamiento en Dataproc (Spark)**: Limpieza, deduplicación y análisis de contenido y tendencias.
4️⃣ **Carga en BigQuery**: Se insertan datos normalizados en un modelo dimensional.
5️⃣ **Análisis SQL**: Se ejecutan consultas optimizadas para tendencias y reportes.
6️⃣ **Visualización en Looker Studio**: Se crean dashboards para análisis de datos.

## 🛠 Configuración y Despliegue
### 1️⃣ Subir el DAG a Composer
```sh
gsutil cp dags/etl_almacen_datos_noticias.py gs://us-central1-flujotransacion-9cfbfa36-bucket/dags/
```

### 2️⃣ Subir Script de Spark a GCS
```sh
gsutil cp scripts/procesamiento_spark.py gs://us-central1-flujotransacion-9cfbfa36-bucket/scripts/
```

### 3️⃣ Reiniciar Airflow para Aplicar Cambios
```sh
gcloud composer environments restart-web-server flujotransacional --location us-central1
```

### 4️⃣ Ejecutar el DAG en Airflow
1. Ir a **Composer → Abrir Airflow**  
2. Activar y Ejecutar el DAG **`etl_almacen_datos_noticias`**  
3. Monitorear la ejecución en **BigQuery**  

## 🧪 Tests Unitarios
Ejecutar pruebas en Airflow y BigQuery:
```sh
pytest tests/
```

## 📊 Análisis SQL
### 🔹 **Tendencias de temas por mes**
```sql
SELECT FORMAT_DATE('%Y-%m', fecha_publicacion) AS mes, nombre, COUNT(*) AS total
FROM `analitica-contact-center-dev.Entorno_Pruebas_modelo.fact_articulos`
JOIN `analitica-contact-center-dev.Entorno_Pruebas_modelo.dim_temas`
ON fact_articulos.topic_id = dim_temas.topic_id
GROUP BY mes, nombre ORDER BY mes DESC, total DESC;
```

### 🔹 **Fuentes de noticias mas influyentes**
```sql
SELECT f.nombre AS fuente, COUNT(a.article_id) AS total_articulos,
       SUM(a.visitas) AS total_visitas, SUM(a.compartidos) AS total_compartidos,
       (SUM(a.visitas) + SUM(a.compartidos)) AS impacto_total
FROM `analitica-contact-center-dev.Entorno_Pruebas_modelo.fact_articulos` a
JOIN `analitica-contact-center-dev.Entorno_Pruebas_modelo.dim_fuentes_noticias` f
ON a.source_id = f.source_id
GROUP BY fuente
ORDER BY impacto_total DESC
LIMIT 10;
```

## 📈 Visualización en Looker Studio
Conectar **BigQuery** con **Looker Studio** para crear un dashboards interactivo y visualizar tendencias en los datos.

## 📌 Conclusión
✔ **Pipeline optimizado con particionamiento y clustering en BigQuery**  
✔ **Procesamiento escalable en Dataproc con Apache Spark**  
✔ **Orquestación eficiente con Airflow en Cloud Composer**  
✔ **Visualización intuitiva en Looker Studio**  





