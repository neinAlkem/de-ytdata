import os
import pytest
from airflow.models import Variable, Connection
from unittest import mock

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