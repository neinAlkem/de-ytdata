import os
import pytest
from airflow.models import Variable, Connection, DagBag
from unittest import mock
import psycopg2

@pytest.fixture 
def api_key():
    with mock.patch.dict(os.environ, {"AIRFLOW_VAR_API_KEY": "test_api_key"}):
        yield Variable.get("API_KEY")
    
@pytest.fixture
def channel_handler():
    with mock.patch.dict(os.environ, {"AIRFLOW_VAR_CHANNEL_HANDLER": "test_channel_handler"}):
        yield Variable.get("CHANNEL_HANDLER")
        
@pytest.fixture
def mock_connection():
        conn = Connection(
            login='test_user',
            password='test_password',
            host='test_host',
            port=5432,
            schema='test_schema'
        )
        conn_uri = conn.get_uri()
        with mock.patch.dict(os.environ, {"AIRFLOW_CONN_POSTGRES_DB_YT_ELT": conn_uri}):
            yield Connection.get_connection_from_secrets(conn_id="POSTGRES_DB_YT_ELT")

@pytest.fixture
def dagbag():
    yield DagBag(dag_folder=os.path.join(os.path.dirname(__file__), '../dags'), include_examples=False)

@pytest.fixture
def airflow_variable():
    def get_airflow_variable(var_name):
        env_var = f"AIRFLOW_VAR_{var_name.upper()}"
        return os.getenv(env_var) 

    return get_airflow_variable

@pytest.fixture
def real_postgres_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("ELT_DATABASE_NAME"),
            user=os.getenv("ELT_DATABASE_USERNAME"),
            password=os.getenv("ELT_DATABASE_PASSWORD"),
            host=os.getenv("POSTGRES_CONN_HOST"),
            port=os.getenv("POSTGRES_CONN_PORT")
        )
        yield conn
    finally:
        if conn:
            conn.close()
    