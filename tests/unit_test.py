def test_api_key(api_key):
    assert api_key == 'test_api_key'
    
def test_channel_handler(channel_handler):
    assert channel_handler == 'test_channel_handler'
    
def test_postgres_connection(mock_connection):
    conn = mock_connection
    assert conn.login == 'test_user'
    assert conn.password == 'test_password'
    assert conn.host == 'test_host'
    assert conn.port == 5432
    assert conn.schema == 'test_schema'
    