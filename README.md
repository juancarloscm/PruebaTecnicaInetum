
Pipeline de Análisis de Tendencias en la Industria Espacial 🚀


Descripción del Proyecto
Este proyecto implementa un pipeline de datos utilizando la API de Spaceflight News para extraer, procesar y analizar información sobre la industria espacial.

Arquitectura
Se diseña un sistema basado en AWS que:
✅ Ingiera datos de artículos, blogs y reportes diariamente.
✅ Clasifique información por temas y fuentes.
✅ Almacene datos históricos para análisis de tendencias.
✅ Use un Data Warehouse optimizado para consultas eficientes.
✅ Automatice procesos con Airflow.

Tecnologías Utilizadas
🔹 Extracción de datos: Python + Requests + API Spaceflight News
🔹 Procesamiento: Apache Spark para limpieza y análisis
🔹 Almacenamiento: AWS S3 + Redshift / BigQuery
🔹 Orquestación: Apache Airflow
🔹 Análisis SQL: Queries para tendencias y fuentes influyentes

Flujo del Pipeline
1️⃣ Ingesta: Extracción de datos con paginación y manejo de errores.
2️⃣ Procesamiento: Limpieza, deduplicación y análisis de contenido.
3️⃣ Almacenamiento: Datos estructurados en un Data Warehouse.
4️⃣ Análisis: Queries para tendencias por mes y ranking de fuentes.
5️⃣ Automatización: DAG de Airflow para ejecutar tareas programadas.

Instalación y Ejecución
1. Clonar el Repositorio
bash
Copiar
Editar
git clone https://github.com/tuusuario/spaceflight-pipeline.git
cd spaceflight-pipeline
2. Crear un Entorno Virtual
bash
Copiar
Editar
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
3. Configurar Variables de Entorno
bash
Copiar
Editar
export API_URL="https://api.spaceflightnewsapi.net/v4"
export AWS_ACCESS_KEY="tu_access_key"
export AWS_SECRET_KEY="tu_secret_key"
4. Ejecutar el Pipeline Manualmente
bash
Copiar
Editar
python run_pipeline.py
Consultas SQL
Ejemplo de consulta para tendencias de temas por mes:

sql
Copiar
Editar
SELECT topic, COUNT(*) as cantidad, DATE_TRUNC('month', published_at) as mes
FROM fact_article
GROUP BY topic, mes
ORDER BY mes DESC, cantidad DESC;

Tareas Pendientes
☑️ Mejorar la clasificación de artículos por IA.
☑️ Optimizar tiempos de ejecución en Spark.
☑️ Implementar dashboard interactivo.

📌 Contacto: juancarloscm@yahoo.com
