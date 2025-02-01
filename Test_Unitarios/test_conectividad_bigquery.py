#2 Test de Conectividad con BigQuery
#Este test verifica que las tablas en BigQuery existen y contienen datos.
from google.cloud import bigquery

client = bigquery.Client()
dataset = "analitica-contact-center-dev.Entorno_Pruebas_modelo"

def test_tablas_existen():
    tablas_requeridas = ["dim_fuentes_noticias", "dim_temas", "fact_articulos"]
    for tabla in tablas_requeridas:
        table_ref = client.dataset(dataset).table(tabla)
        try:
            client.get_table(table_ref)
            print(f" Tabla {tabla} existe.")
        except Exception as e:
            raise AssertionError(f"❌ Tabla {tabla} NO existe. Error: {e}")

def test_tablas_contienen_datos():
    query = f"SELECT COUNT(*) as total FROM `{dataset}.fact_articulos`"
    resultado = client.query(query).to_dataframe()
    assert resultado["total"][0] > 0, " No hay datos en fact_articulos"


