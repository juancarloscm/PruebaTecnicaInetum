import requests
import json
from google.cloud import pubsub_v1
import time
from datetime import datetime

BASE_URL = "https://api.spaceflightnewsapi.net/v4"
ENDPOINTS = ["/articles", "/blogs", "/reports", "/info"]
PROJECT_ID = "mi-proyecto"
TOPIC_NAME = "ingesta-noticias"

def log_event(event):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {event}")

def obtener_datos(endpoint):
    """Obtiene datos de un endpoint con manejo de paginación y rate limit."""
    url = f"{BASE_URL}{endpoint}"
    datos = []
    seen_ids = set()
    
    while url:
        response = requests.get(url)
        if response.status_code == 429:
            log_event("⚠️ Rate limit alcanzado. Esperando 5 segundos...")
            time.sleep(5)
            continue
        if response.status_code == 200:
            json_data = response.json()
            for item in json_data["results"]:
                if item["id"] not in seen_ids:
                    datos.append(item)
                    seen_ids.add(item["id"])
            url = json_data.get("next")
            log_event(f"✅ Página procesada para {endpoint}.")
        else:
            log_event(f"⚠️ Error al obtener datos de {endpoint}: {response.status_code}")
            break
    return datos

def publicar_en_pubsub(datos, endpoint):
    """Publica los datos en Pub/Sub."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)
    
    for item in datos:
        mensaje = {"endpoint": endpoint, "data": item}
        publisher.publish(topic_path, data=json.dumps(mensaje).encode("utf-8"))
    log_event(f"✅ {len(datos)} registros del endpoint {endpoint} publicados en Pub/Sub.")

def main(request):
    log_event("🚀 Inicio de la ingesta de datos.")
    for endpoint in ENDPOINTS:
        datos = obtener_datos(endpoint)
        if datos:
            publicar_en_pubsub(datos, endpoint)
        else:
            log_event(f"⚠️ No se encontraron datos para {endpoint}.")
    log_event("🎯 Ingesta completada para todos los endpoints.")
    return "✅ Ingesta finalizada."

