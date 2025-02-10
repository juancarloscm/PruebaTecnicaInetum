#  Pipeline de Analisis de Tendencias en la Industria Espacial 
#  Proyecto: ETL y Análisis de Noticias en GCP

## 📌 Descripción
Este proyecto implementa un pipeline de **ETL (Extract, Transform, Load)** en **Google Cloud Platform (GCP)** para extraer datos de la API de **Spaceflight News**, transformarlos con **Apache Spark en Dataproc**, y almacenarlos en **Google BigQuery** para análisis y visualización.

**OPCION 1:**

## ⚙️ Herramientas Utilizadas
- **Google Cloud Composer (Airflow)** - Orquestación del pipeline.
- **Google Cloud Storage (GCS)** - Almacenamiento intermedio de datos.
- **Google BigQuery** - Data Warehouse para análisis y reportes.
- **Google Dataproc (Spark)** - Transformación y procesamiento de datos.
- **Looker Studio** - Visualización de datos.

## 📁 Estructura del Proyecto
```
├── Dags/
│   ├── Dag_blogs_Biquery_Dinamico # etl_almacen_datos_noticias.py-DAG principal en Airflow
│   ├── PipelineSpark # PipelineSpark.py # Automatización del flujo de trabajo, desde la extracción de datos hasta la carga en BigQuery y la generación de insights diarios.
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
│   ├── limpia_y_deduplica.py  # Herramienta: Apache Spark en Google Cloud Dataproc,Función: Limpieza y deduplicación de datos extraídos (articles, blogs, reports).Almacenamiento: Cloud Storage (cleaned_data.parquet)
│   ├── proceso_analysis.py  # Herramienta: Apache Spark en Google Cloud Dataproc,Función: Extracción de palabras clave Clasificación por temas (Launch, Rocket, Space) Identificación de compañías y lugares mencionados Almacenamiento: Cloud Storage (analyzed_data.parquet)
│   ├── identfica__topics.py  # Herramienta: Apache Spark en Google Cloud Dataproc Función: Análisis de tendencias por temas Conteo de menciones de compañías y lugares Almacenamiento: Google BigQuery (topic_trends, company_mentions, place_mentions)
│── README.md  # Documentación
```

##  Flujo del Pipeline
- ** 1️⃣ **Extracción de Datos**: Se extraen noticias desde la API de **Spaceflight News**, manejando paginación y rate limits.
- ** 2️⃣ **Almacenamiento en GCS**: Los datos se guardan en formato **JSON y Parquet** en Google Cloud Storage.
- ** 3️⃣ **Procesamiento en Dataproc (Spark)**: Limpieza, deduplicación y análisis de contenido y tendencias.
- ** 4️⃣ **Carga en BigQuery**: Se insertan datos normalizados en un modelo dimensional.
- ** 5️⃣ **Análisis SQL**: Se ejecutan consultas optimizadas para tendencias y reportes.
- ** 6️⃣ **Visualización en Looker Studio**: Se crean dashboards para análisis de datos.

## 🛠 Configuración y Despliegue
- ** ### 1️⃣ Subir el DAG a Composer
```sh
gsutil cp dags/etl_almacen_datos_noticias.py gs://us-central1-flujotransacion-9cfbfa36-bucket/dags/
```

- ** ### 2️⃣ Subir Script de Spark a GCS
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


# 🧪 Test Unitarios para el Pipeline de Datos

## 📌 **Objetivo**
Garantizar la calidad y el correcto funcionamiento del pipeline mediante la ejecución de test unitarios en las funciones clave. Esto asegura que cada módulo individual funcione como se espera y facilita la detección temprana de errores.

---
## 🛠️ **Áreas de Prueba**
Los test unitarios cubren las siguientes áreas clave del pipeline:

| **Módulo**                 | **Descripción del Test**                                    |
|----------------------------|-------------------------------------------------------------|
| Extracción de datos         | Verifica la conexión y respuesta de la API.                  |
| Limpieza y deduplicación   | Asegura que no existan registros duplicados y que se eliminen columnas innecesarias. |
| Análisis de palabras clave | Comprueba la correcta extracción de las palabras más frecuentes. |
| Clasificación de artículos  | Verifica la asignación correcta de categorías (`Launch`, `Rocket`, `Space`). |
| Carga a BigQuery           | Asegura que el esquema de datos sea compatible y la carga se realice sin errores. |

---
## 🧑‍💻 **Ejemplos de Test Unitarios**

### 1️⃣ **Test de Extracción de Datos**
```python
import unittest
import requests

class TestDataExtraction(unittest.TestCase):
    def test_api_response(self):
        response = requests.get("https://api.spaceflightnewsapi.net/v4/articles")
        self.assertEqual(response.status_code, 200, "La API no responde correctamente.")

if __name__ == '__main__':
    unittest.main()
```
**Descripción:** Verifica que la API responda con un código `200` (OK).

---
### 2️⃣ **Test de Limpieza y Deduplicación**
```python
import unittest
from pyspark.sql import SparkSession

class TestDataCleaning(unittest.TestCase):
    def setUp(self):
        self.spark = SparkSession.builder.appName("TestCleaning").getOrCreate()
        self.data = [(1, "Article 1"), (1, "Article 1"), (2, "Article 2")]
        self.df = self.spark.createDataFrame(self.data, ["id", "title"])

    def test_remove_duplicates(self):
        cleaned_df = self.df.dropDuplicates(["id"])
        self.assertEqual(cleaned_df.count(), 2, "Eliminación de duplicados fallida.")

if __name__ == '__main__':
    unittest.main()
```
**Descripción:** Verifica que el proceso de limpieza elimine correctamente los registros duplicados.

---
### 3️⃣ **Test de Clasificación de Artículos**
```python
import unittest
from classify import classify_article  # Supongamos que esta función clasifica artículos

class TestClassification(unittest.TestCase):
    def test_classification(self):
        self.assertEqual(classify_article("This is a rocket launch"), "Launch", "Clasificación incorrecta.")
        self.assertEqual(classify_article("Space mission to Mars"), "Space", "Clasificación incorrecta.")

if __name__ == '__main__':
    unittest.main()
```
**Descripción:** Verifica que la función de clasificación asigne la categoría correcta.

---
## 📦 **Estrategia de Ejecución**
1. **Automatización:** Los test unitarios se ejecutan automáticamente en cada nueva versión del pipeline utilizando un sistema de integración continua (CI/CD).
2. **Frecuencia:** Ejecución diaria o en cada cambio significativo en el código.
3. **Resultados:** Los resultados se registran y notifican al equipo.

---
## ✅ **Conclusión**
Los test unitarios son una parte esencial para mantener la calidad del pipeline de datos. Detectan errores tempranamente, aseguran la estabilidad del sistema y facilitan el mantenimiento a largo plazo.



# 📊 Análisis de Datos del Pipeline

## 📌 **Objetivo**
El análisis de datos en el pipeline tiene como finalidad extraer información clave, identificar tendencias y generar insights útiles para la toma de decisiones.

---
## 🛠️ **Áreas de Análisis**
| **Análisis**                   | **Descripción**                                          |
|--------------------------------|----------------------------------------------------------|
| Extracción de palabras clave   | Identificación de las 5 palabras más frecuentes en el contenido. |
| Clasificación de artículos      | Clasificación automática en categorías (`Launch`, `Rocket`, `Space`). |
| Identificación de entidades     | Reconocimiento de compañías y lugares mencionados.        |
| Análisis de tendencias          | Identificación de patrones por categoría y fuente de noticias. |
| Generación de insights diarios  | Reportes automatizados sobre el volumen y la actividad reciente. |

---
## 📈 **Metodología de Análisis**
### 1️⃣ **Extracción de Palabras Clave**
Se utiliza un conteo de frecuencia de palabras para identificar las palabras clave más relevantes en el contenido de cada artículo.

**Ejemplo de código:**
```python
import re
from collections import Counter

def extract_keywords(summary):
    words = re.findall(r'\w+', summary.lower())
    common_words = Counter(words).most_common(5)
    return [word for word, _ in common_words]
```
**Descripción:** Devuelve las 5 palabras más comunes en el resumen del artículo.

---
### 2️⃣ **Clasificación de Artículos por Tema**
Se clasifica cada artículo en una categoría específica basada en palabras clave.

**Ejemplo de código:**
```python
def classify_article(summary):
    if "launch" in summary.lower():
        return "Launch"
    elif "rocket" in summary.lower():
        return "Rocket"
    elif "space" in summary.lower():
        return "Space"
    else:
        return "General"
```
**Descripción:** Clasifica el artículo en `Launch`, `Rocket`, `Space` o `General`.

---
### 3️⃣ **Identificación de Entidades (Compañías y Lugares)**
Se extraen entidades relevantes mencionadas en el contenido, como compañías (`NASA`, `SpaceX`) y lugares (`Florida`, `Mars`).

**Ejemplo de código:**
```python
def identify_entities(summary):
    companies = ["NASA", "SpaceX", "Boeing"]
    places = ["Florida", "Texas", "Mars"]
    found_companies = [c for c in companies if c.lower() in summary.lower()]
    found_places = [p for p in places if p.lower() in summary.lower()]
    return {"companies": found_companies, "places": found_places}
```
**Descripción:** Devuelve una lista de compañías y lugares mencionados en el resumen.

---
## 📊 **Visualización de Datos y Reportes**
### Herramientas Utilizadas:
- **Google BigQuery** para almacenamiento y consultas rápidas.
- **Google Data Studio** para crear dashboards visuales.

### Ejemplo de Consulta SQL en BigQuery:
```sql
SELECT category, COUNT(*) AS total_articles
FROM `analitica-contact-center-dev.pos_analitica_ANALISIS.topic_trends`
WHERE published_at BETWEEN '2025-01-01' AND '2025-01-31'
GROUP BY category
ORDER BY total_articles DESC;
```
**Descripción:** Consulta el número de artículos por categoría en enero de 2025.

---
## 🔄 **Automatización y Generación de Insights**
1. **Datos diarios:** El pipeline genera reportes diarios automáticamente.
2. **Visualización en tiempo real:** Los resultados se actualizan en dashboards de Google Data Studio.
3. **Alertas y tendencias:** Identificación de patrones emergentes por categoría.

---
## ✅ **Conclusión**
El análisis de datos del pipeline proporciona insights valiosos para comprender mejor las tendencias, detectar patrones clave y mejorar la toma de decisiones. Las herramientas utilizadas, como BigQuery y Data Studio, permiten realizar consultas rápidas y visualizar los resultados de manera efectiva.

**OPCION 2**

## Propuesta de Mejora del Modelo con 100% serveless
## 📌 Descripción
📌 Pipeline Completo en Google Cloud
Este pipeline extrae noticias espaciales de la API de Spaceflight News, las procesa y las limpia con Apache Beam (Dataflow), las almacena en BigQuery y las visualiza con Looker Studio.

## ⚙️ Tecnologias Utilizadas

- ** 1️⃣ Cloud Functions → Ingesta de datos desde la API y publicación en Pub/Sub (100% serverless).
- ** 2️⃣ Pub/Sub → Sistema de mensajería para manejar datos en tiempo real y desacoplar procesos.
- ** 3️⃣ Dataflow (Apache Beam) → Procesa y enriquece los datos (palabras clave, clasificación) antes de enviarlos a BigQuery.
- ** 4️⃣ BigQuery → Almacena y analiza grandes volúmenes de datos, con particionamiento y clustering para consultas rápidas.
- ** 5️⃣ Cloud Composer (Airflow) → Orquesta el pipeline completo, programa tareas y monitorea fallos.
- ** 6️⃣ Google Cloud Natural Language API → Análisis de texto para extraer entidades y temas principales.
- ** 7️⃣ Looker Studio → Dashboards dinámicos para visualizar tendencias y patrones clave.

Arquitectura PIPELINE 

https://lucid.app/documents/embedded/230b2762-6f66-4fe1-8dac-260179ab6aaf

Inteligencia Artificial utilizada
Modelo Ia-ops
Ver PDF

##  Sistema de Backup y Recuperación
- ** Backup de datos críticos (almacenados en Cloud Storage, BigQuery, y metadatos del pipeline).
- ** Automatización de backups periódicos.
- ** Recuperación rápida en caso de fallo o pérdida de datos.

## 📊 Resumen de la Arquitectura de Backup
- ** Cloud Storage para respaldar datos intermedios y JSON de entrada.
- ** BigQuery Export para respaldar tablas finales.
- ** Cloud Scheduler para ejecutar tareas automáticas.
- ** Google Cloud Monitoring para detectar y alertar sobre errores.


 ## 🛠 Estrategia de Implementación
- ** 1. Backup en Google Cloud Storage
- ** 📦 Datos a respaldar:
- ** Datos intermedios (cleaned_data.parquet, analyzed_data.parquet).
- ** Archivos JSON de entrada (articles.json, blogs.json).
- ** 💡 Cómo implementarlo:
- ** Configura versiones de objetos en tu bucket (Object Versioning).
- ** Automatiza los backups con un script y programa la tarea en Cloud Scheduler.

- ** 2. Backup de BigQuery
- ** 📦 Datos a respaldar:
- ** Tablas finales (topic_trends, company_mentions, place_mentions).
- ** 💡 Cómo implementarlo:
- ** Exporta las tablas a Cloud Storage en formato Avro o Parquet.

- ** 3. Recuperación de Datos
- ** Datos en Cloud Storage:
- ** Si tienes versiones anteriores, puedes restaurarlas directamente.
- **  gsutil cp gs://buckets-aws-backup/processed_data_20250201 gs://buckets-aws/processed_data

- ** Datos en BigQuery:
- ** Si las tablas se perdieron, puedes volver a importarlas desde el backup en Cloud Storage.
- ** bq load \
- **   --source_format=PARQUET \
- **  "analitica-contact-center-dev:pos_analitica_ANALISIS.topic_trends" \
- **  "gs://buckets-aws-backup/bigquery/topic_trends_20250201.parquet"

- ** 4. Monitorización y Alertas
- ** Se Configura Google Cloud Monitoring para recibir alertas en caso de:
- ** Fallos en las tareas de backup.
- ** Falta de espacio en Cloud Storage.
- ** Fallos de importación en BigQuery.

## Objetivo del DAG de Airflow:
- ** Backup de datos intermedios y tablas de BigQuery.
- ** Almacenar los backups en Cloud Storage.
- ** Automatización diaria para mantener los datos respaldados y seguros.
- ** Restauración manual en caso de fallo.

----------------------------
🛠 2. Estrategia de Almacenamiento y Búsqueda
- ** a. Almacenamiento
- ** Herramientas:

- ** Google Cloud Storage (intermedios y backups)
- ** Google BigQuery (datos estructurados para consultas rápidas)
- ** Formato recomendado:
- ** JSON para almacenamiento bruto (backup).
- ** Parquet para datos procesados y comprimidos (más eficiente para análisis en BigQuery y Spark).


- ** b. Estrategia de Búsqueda
- ** 1. Google BigQuery (para consultas avanzadas):

- ** Consulta rápida: Usa índices y particiones en BigQuery para acelerar las consultas.
- ** Particiona por fecha (published_at) para reducir el volumen escaneado.
- ** Clustering: Clustering por category y news_site para mejorar el rendimiento.

## 🎯 Objetivo del Plan de Contingencia
- ** Identificar riesgos críticos que puedan afectar el pipeline.
- ** Implementar medidas preventivas y correctivas para mitigar los riesgos.
- ** Definir procedimientos de recuperación rápida en caso de fallo.
- ** 🛠️ 1. Identificación de Riesgos
- **        Aquí están los riesgos más relevantes para tu pipeline:

- **        Riesgo	Descripción	Impacto
- **        Fallo en la extracción de datos	La API no responde o cambia su estructura.	Alto
- **        Pérdida de datos en Cloud Storage	Archivos borrados o corrompidos.	Alto
- **        Fallo en Dataproc (Spark)	Error en la ejecución de tareas o falta de recursos.	Medio
- **        Fallo en la carga a BigQuery	Datos incompletos o errores de formato.	Alto
- **        Error en la automatización (Airflow)	DAGs fallidos o problemas de conectividad.	Medio
- **🛡️ 2. Estrategia de Mitigación y Procedimientos Correctivos
- **       a. Backup y Recuperación
- **          Backup Diario en Cloud Storage:
- **          Automatizado mediante Airflow y Cloud Scheduler.
- **          Respalda datos intermedios y tablas de BigQuery.
- ** Plan de Restauración:
- **  Restaurar datos desde el backup más reciente en caso de pérdida (como explicamos en el DAG data_recovery_pipeline).
- **       b. Redundancia y Alta Disponibilidad
- **          Google Cloud Storage asegura alta disponibilidad con múltiples réplicas.
- **          BigQuery es una plataforma sin servidor con redundancia interna.
- **       c. Monitoreo y Alertas (Cloud Monitoring)
- **          Configura Google Cloud Monitoring para detectar fallos en el pipeline.
- **          Notificaciones en tiempo real: Por correo, Slack o Google Chat.
- **          Política de alertas personalizadas basada en:
- **          Tiempo de ejecución prolongado.
- **          Errores en Dataproc o BigQuery.




## IDE de Entendimiento del API
http://190.26.178.21/IDETestGCP/menu.php





