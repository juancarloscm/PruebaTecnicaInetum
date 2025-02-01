#1 Test de Validación de DAG en Airflow
#Este test verifica que el DAG de Airflow no tenga errores de sintaxis.

import pytest
from airflow.models import DagBag

def test_dag_integridad():
    dag_bag = DagBag(dag_folder="/opt/airflow/dags/", include_examples=False)
    assert 'etl_almacen_datos_noticias' in dag_bag.dags
    dag = dag_bag.get_dag('etl_almacen_datos_noticias')
    assert dag is not None
    assert len(dag.tasks) > 0


