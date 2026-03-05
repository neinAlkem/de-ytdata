import requests
import pytest

def test_youtube_api_response(airflow_variable):
    api_key = airflow_variable('API_KEY')
    channel_handler = airflow_variable('CHANNEL_HANDLER')
    
    url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forUsername={channel_handler}&key={api_key}"
    
    try:
        response = requests.get(url)
        assert response.status_code == 200
    except Exception as e:
        pytest.fail(f"API request failed: {e}")
        
def test_database_conn(real_postgres_connection):
    try:
        conn = real_postgres_connection.cursor()
        conn.execute('select 1')
        result = conn.fetchone()
        assert result[0] == 1
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")
    finally:
        real_postgres_connection.close()