import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import json
from google.cloud import language_v1

class FiltrarPorEndpoint(beam.DoFn):
    """Filtra y enriquece los datos por endpoint."""
    def process(self, element):
        mensaje = json.loads(element.decode('utf-8'))
        endpoint = mensaje["endpoint"]
        data = mensaje["data"]
        if endpoint in ["/articles", "/blogs", "/reports"]:
            data["keywords"], data["entities"] = analizar_contenido(data.get("summary", ""))
            data["topic"] = clasificar_tema(data.get("summary", ""))
        yield beam.pvalue.TaggedOutput(endpoint.strip("/"), data)

def analizar_contenido(texto):
    """Extrae palabras clave y entidades usando Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=texto, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(document=document)
    keywords = [entity.name for entity in response.entities]
    entities = [entity.type_.name for entity in response.entities]
    return keywords, entities

def clasificar_tema(texto):
    """Clasifica el texto en temas simples."""
    if "space" in texto.lower() or "nasa" in texto.lower():
        return "science"
    elif "technology" in texto.lower():
        return "technology"
    elif "government" in texto.lower():
        return "politics"
    return "general"

def ejecutar_pipeline():
    options = PipelineOptions(streaming=True, project="mi-proyecto", region="us-central1")
    with beam.Pipeline(options=options) as p:
        resultados = (p
                     | "Leer desde Pub/Sub" >> beam.io.ReadFromPubSub(topic="projects/mi-proyecto/topics/ingesta-noticias")
                     | "Filtrar y Analizar" >> beam.ParDo(FiltrarPorEndpoint()).with_outputs(
                         "articles", "blogs", "reports", "info")
                     )
        resultados.articles | "Escribir en BigQuery - Articles" >> beam.io.WriteToBigQuery(
            "mi-proyecto.dataset_noticias.articles",
            schema="id:STRING, title:STRING, url:STRING, image_url:STRING, news_site:STRING, "
                   "summary:STRING, published_at:TIMESTAMP, updated_at:TIMESTAMP, "
                   "keywords:ARRAY<STRING>, entities:ARRAY<STRING>, topic:STRING",
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
