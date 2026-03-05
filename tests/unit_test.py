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
    
def test_dags_integration(dagbag):
    assert dagbag.import_errors == {}, f'DAG import errors: {dagbag.import_errors}'
    print('============')
    print(dagbag.import_errors)
    
    expected_dags_id = ['produce_video_stats', 'update_db', 'data_quality_check']
    loaded_dags_id = list(dagbag.dags.keys())
    print('=============')
    print(dagbag.dags.keys())
    
    for dag_id in expected_dags_id:
        assert dag_id in loaded_dags_id, f'DAG {dag_id} not found in DagBag'
    
    assert len(dagbag.dags) == 3
    print('=============')
    print(len(dagbag.dags))
    
    expected_taks_cound = {
        'produce_video_stats': 4,
        'update_db': 2,
        'data_quality_check': 2
    }
    print('=============')
    for dag_id, expected_count in expected_taks_cound.items():
        dag = dagbag.get_dag(dag_id)
        actual_count = len(dag.tasks)
        print(f'{dag_id}: expected {expected_count}, actual {actual_count}')
        assert actual_count == expected_count, f'DAG {dag_id} has {actual_count} tasks, expected {expected_count}'