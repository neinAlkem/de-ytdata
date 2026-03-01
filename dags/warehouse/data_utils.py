from airflow.providers.postgres.hooks.postgres import PostgresHook  
from psycopg2.extras import RealDictCursor

table = 'yt_api'

def get_db_conn():
    hook = PostgresHook(postgres_conn_id='POSTGRES_DB_YT_ELT', database='elt_db')
    conn = hook.get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    return conn, cur

def close_db_conn(conn , cur) -> None:
    cur.close()
    conn.close()
    
def create_schema(schema_name: str) -> None:
    conn, curr = get_db_conn()
    schema_query = f'CREATE SCHEMA IF NOT EXISTS {schema_name};'
    curr.execute(schema_query)
    conn.commit()
    close_db_conn(conn, curr)

def create_table(schema_name: str) -> None:
    conn, curr = get_db_conn()
    if schema_name == 'stg':
        table_query = f"""
        CREATE TABLE IF NOT EXISTS {schema_name}.{table} (
            video_id VARCHAR(255) PRIMARY KEY NOT NULL,
            title TEXT NOT NULL,
            published_at TIMESTAMP NOT NULL,
            duration VARCHAR(255) NOT NULL,
            view_count INTEGER,
            like_count INTEGER,
            comment_count INTEGER
        );
        """
    else:
        table_query = f"""
        CREATE TABLE IF NOT EXISTS {schema_name}.{table} (
            video_id VARCHAR(255) PRIMARY KEY NOT NULL,
            title TEXT NOT NULL,
            published_at TIMESTAMP NOT NULL,
            duration TIME NOT NULL,
            video_type VARCHAR(50) NOT NULL,
            view_count INTEGER,
            like_count INTEGER,
            comment_count INTEGER
        );
        """
    curr.execute(table_query)
    conn.commit()
    close_db_conn(conn, curr)

def get_video_ids(cur, schema_name: str) -> list:
    query = f'SELECT video_id FROM {schema_name}.{table};'
    cur.execute(query)
    result = cur.fetchall()
    
    return [row['video_id'] for row in result]
        