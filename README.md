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

# 📦 Sistema de Recuperación y Backup para el Pipeline de Datos

## 📌 **Objetivo**
Garantizar la disponibilidad de datos y la continuidad operativa del pipeline mediante un sistema de recuperación rápida y backups automáticos.

---
## ⚠️ **Identificación de Riesgos**
| **Riesgo**                        | **Descripción**                                        |
|------------------------------------|--------------------------------------------------------|
| Fallo en la extracción de datos    | La API no responde o cambia su estructura.             |
| Pérdida de datos en Cloud Storage  | Archivos borrados o corrompidos.                       |
| Fallo en Dataproc (Spark)          | Error en la ejecución de tareas o falta de recursos.   |
| Fallo en la carga a BigQuery       | Datos incompletos o errores de formato.                |
| Error en la automatización (Airflow)| DAGs fallidos o problemas de conectividad.             |

---
## 🛡️ **Estrategia de Backup y Recuperación**

### 🔄 **Backup Automático**
1. **Cloud Storage:** Backup diario de datos intermedios (`cleaned_data.parquet`) y JSON originales.
2. **BigQuery:** Exportación de tablas procesadas (`topic_trends`, `company_mentions`, `place_mentions`) en formato Parquet.
3. **Automatización con Airflow:** Las tareas de backup se ejecutan automáticamente mediante DAGs.

### ⚙️ **Restauración de Datos**
1. **Cloud Storage:** Restauración desde el backup más reciente.
2. **BigQuery:** Importación de datos respaldados en formato Parquet.
3. **Fallback Automático:** DAG de recuperación en Airflow que se activa si una tarea crítica falla.

---
## 🧑‍💻 **Procedimientos de Recuperación**

### 1️⃣ **Fallo en la extracción de datos (API no responde)**
- **Acción:** Reintentar la tarea después de 5 minutos.
- **Fallback:** Recuperar datos de una fuente alternativa si está disponible.

### 2️⃣ **Pérdida de datos en Cloud Storage**
- **Acción:** Restaurar desde el backup más reciente.
- **Prevención:** Activar Object Versioning en Cloud Storage para mantener versiones anteriores.

### 3️⃣ **Fallo en Dataproc (Spark)**
- **Acción:** Reintentar el trabajo hasta 3 veces.
- **Fallback:** Escalar el cluster de Dataproc o reprogramar la tarea.

### 4️⃣ **Error en la carga a BigQuery**
- **Acción:** Corregir el formato de datos y reintentar.
- **Prevención:** Validar el esquema de datos antes de cargar.

---
## 📈 **Monitoreo y Alertas**
1. **Google Cloud Monitoring:** Detecta fallos críticos y notifica en tiempo real.
2. **Alertas personalizadas:** Por correo, Slack o Google Chat.
3. **Notificaciones Automáticas:** Activación de alertas en Airflow mediante `TriggerDagRunOperator`.

---
## 📊 **Visualización del Sistema**
### Resumen del Flujo de Backup y Recuperación:
1. **Backup Automático Diario** → 2. **Monitoreo Continuo** → 3. **Detección de Fallos** → 4. **Restauración Automática** → 5. **Notificación al Equipo**

---
## ✅ **Conclusión**
El sistema de recuperación y backup garantiza la continuidad operativa del pipeline de datos, reduciendo el riesgo de pérdida y tiempos de recuperación. La combinación de Cloud Storage, BigQuery y Airflow permite una solución escalable y confiable.





# Plan de Contingencia para el Pipeline de Datos

## 📌 Objetivo del Plan
El objetivo de este plan de contingencia es garantizar la continuidad operativa del pipeline de datos, minimizando el tiempo de inactividad y reduciendo el riesgo de pérdida de datos. Esto se logra mediante la identificación de riesgos, la implementación de medidas preventivas, y la definición de procedimientos claros para la recuperación rápida.

## ⚠️ Identificación de Riesgos
A continuación, se describen los principales riesgos que podrían afectar el pipeline de datos:

| **Riesgo**                        | **Descripción**                                        | **Impacto**  |
|------------------------------------|--------------------------------------------------------|--------------|
| Fallo en la extracción de datos    | La API no responde o cambia su estructura.             | Alto         |
| Pérdida de datos en Cloud Storage  | Archivos borrados o corrompidos.                       | Alto         |
| Fallo en Dataproc (Spark)          | Error en la ejecución de tareas o falta de recursos.   | Medio        |
| Fallo en la carga a BigQuery       | Datos incompletos o errores de formato.                | Alto         |
| Error en la automatización (Airflow)| DAGs fallidos o problemas de conectividad.             | Medio        |

## 🛡️ Medidas Preventivas y Correctivas

### 🔄 Backup y Recuperación
- **Backup Diario en Cloud Storage:** Respaldo automatizado de datos intermedios y tablas de BigQuery.
- **Plan de Restauración:** Restaurar datos desde el backup más reciente en caso de pérdida.

### ⚙️ Redundancia y Alta Disponibilidad
- **Google Cloud Storage:** Múltiples réplicas para asegurar alta disponibilidad.
- **BigQuery:** Redundancia interna para datos estructurados.

### 📈 Monitoreo y Alertas (Cloud Monitoring)
- Configuración de alertas para detectar fallos en el pipeline.
- Notificaciones en tiempo real por correo, Slack o Google Chat.
- Políticas de alertas personalizadas basadas en tiempo de ejecución y errores críticos.

## 🚨 Procedimientos de Recuperación

### Escenario 1: Fallo en la extracción de datos (API no responde)
- **Acción inmediata:** Detener el DAG y reintentar después de 5 minutos.
- **Fallback:** Notificar al equipo y recuperar datos de una fuente alternativa si está disponible.

### Escenario 2: Pérdida de datos en Cloud Storage
- **Acción inmediata:** Restaurar los datos desde el backup más reciente.
- **Prevención:** Habilitar Object Versioning en Cloud Storage.

### Escenario 3: Fallo en Dataproc (Spark)
- **Acción inmediata:** Reintentar el trabajo hasta 3 veces.
- **Fallback:** Escalar el cluster de Dataproc o reprogramar la tarea.

### Escenario 4: Error en la carga a BigQuery
- **Acción inmediata:** Corregir el formato de datos y reintentar la carga.
- **Prevención:** Validación previa del esquema de datos antes de cargar.

## 👥 Roles y Responsabilidades

| **Rol**               | **Responsabilidad**                                      |
|-----------------------|---------------------------------------------------------|
| Equipo de Datos       | Gestión y recuperación de datos.                         |
| Equipo de DevOps      | Monitoreo y soporte del entorno de ejecución.             |
| Gerencia              | Evaluación del impacto y toma de decisiones estratégicas. |

## 🔍 Resumen Visual del Plan
Un diagrama de flujo que ilustra el proceso del plan de contingencia, desde la identificación de un fallo hasta la restauración de datos.

---
### 🗂️ Diagrama (sugerido):
1. **Detección de error** → 2. **Verificación de backups** → 3. **Restauración automática** → 4. **Notificación al equipo** → 5. **Reanudación del pipeline**

---

## 📋 Conclusión
Este plan de contingencia establece una estrategia integral para asegurar la continuidad del pipeline de datos. Las medidas descritas minimizan el impacto de los fallos y garantizan la rápida recuperación del sistema, manteniendo la integridad y disponibilidad de los datos.


# 🚀 Mejora Continua del Proyecto

## 📌 **Objetivo**
Identificar mejoras clave para optimizar el rendimiento, escalabilidad y funcionalidad del pipeline de datos, garantizando una operación más eficiente y generando insights más avanzados.

---
## 🔄 **1. Optimización del Pipeline**
### 💡 **Mejoras Técnicas**
1. **Particiones y Clustering en BigQuery**
   - **Particionar** las tablas por fecha (`published_at`) para reducir el volumen de datos escaneados.
   - **Clustering** por `category` y `news_site` para mejorar la velocidad de consulta.

   **Ejemplo:**
   ```sql
   CREATE TABLE topic_trends
   PARTITION BY DATE(published_at)
   CLUSTER BY category, news_site AS (
       SELECT * FROM raw_data
   );
   ```

2. **Spark Structured Streaming (Procesamiento en Tiempo Real)**
   - Procesar datos en tiempo real con **Google Pub/Sub** y **Dataproc Streaming**.
   - **Beneficio:** Respuestas inmediatas ante eventos nuevos.

---
## 📈 **2. Escalabilidad y Rendimiento**
### 💡 **Optimización de Infraestructura**
1. **Autoescalado de Clúster en Dataproc**
   - Ajuste automático del número de nodos según la carga de trabajo.
   - **Beneficio:** Reduce costos y garantiza disponibilidad de recursos.

2. **Sistema de Caché para Consultas Frecuentes**
   - Implementación de **Redis o Memorystore** para almacenar resultados de consultas recurrentes.
   - **Beneficio:** Reducción de la latencia en dashboards.

3. **Compresión Avanzada de Datos**
   - Utilización de formatos como **ORC o Avro** para mejorar el rendimiento de lectura y reducir costos de almacenamiento.

---
## 🚀 **3. Nuevas Funcionalidades y Expansión**
### 💡 **Nuevas Capacidades**
1. **Análisis de Sentimientos y Lenguaje Natural**
   - Integración de **Google Cloud Natural Language** para detectar emociones y valoraciones en artículos.

2. **Dashboards Interactivos Avanzados**
   - Creación de dashboards en **Looker Studio** o **Tableau** con filtros dinámicos.
   - **Beneficio:** Facilita la exploración interactiva de datos.

3. **Machine Learning para Predicción de Tendencias**
   - Modelos de **ML en Vertex AI** para predecir categorías más relevantes y patrones futuros.

4. **Alertas Inteligentes Basadas en Umbrales Dinámicos**
   - Sistema de alertas predictivas para identificar comportamientos anómalos en tiempo real.

---
## 📊 **Resumen Visual de las Mejoras**
| **Categoría**              | **Mejora**                                       | **Beneficio**                          |
|----------------------------|--------------------------------------------------|----------------------------------------|
| Optimización del Pipeline   | Particiones y clustering en BigQuery             | Consultas más rápidas y eficientes     |
| Escalabilidad               | Autoescalado de Dataproc                        | Reducción de costos y mejor rendimiento|
| Nuevas Funcionalidades      | Análisis de sentimientos y predicción de tendencias | Insights avanzados y toma de decisiones proactiva |

---
## ✅ **Conclusión**
Estas mejoras aseguran un pipeline más escalable, eficiente y alineado con las necesidades futuras del proyecto. La implementación gradual permitirá maximizar el valor de los datos y optimizar los recursos.






## IDE de Entendimiento del API
http://190.26.178.21/IDETestGCP/menu.php





