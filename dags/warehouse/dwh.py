from  warehouse.data_modified import insert_row, update_row, delete_row
from warehouse.data_utils import get_db_conn, close_db_conn, create_schema, create_table, get_video_ids
from warehouse.data_load import load_path  
from warehouse.data_transformation import transform_data, parse_duration
from datetime import datetime
import logging
from airflow.decorators import task

logger = logging.getLogger(__name__)
table = 'yt_api'

@task
def stg_table() -> None:
    schema = 'stg'
    conn, cur = None, None
    try:
        conn, cur = get_db_conn()
        data = load_path()
        create_schema(schema)
        create_table(schema)
        table_ids = get_video_ids(cur, schema)
        
        for row in data:
            if len(table_ids) == 0:
                insert_row(cur, conn, schema, [row['video_id'], row['title'], row['published_at'], row['duration'], row['view_count'], row['like_count'], row['comment_count']])
            elif row['video_id'] in table_ids:
                update_row(cur, conn, schema, [row['video_id'], row['title'], row['published_at'], row['duration'], row['view_count'], row['like_count'], row['comment_count']])
        
        ids_in_json = {row['video_id'] for row in data}
        ids_to_delete = set(table_ids) - ids_in_json
        if ids_to_delete:
            delete_row(cur, conn, schema, ids_to_delete)
        logger.info(f"Staging table '{schema}.{table}' updated successfully with data from file.")  
        
    except Exception as e:
        logger.error(f"Error updating staging table '{schema}.{table}': {e}")
        
    finally:
        close_db_conn(conn, cur)

@task
def dbo_table() -> None:
    schema = 'dbo'
    conn, cur = None, None
    try:
        conn, cur = get_db_conn()
        create_schema(schema)
        create_table(schema)
        table_ids = get_video_ids(cur, schema)
        current_video_ids = set()
        cur.execute(f'SELECT * FROM stg.{table};')
        rows = cur.fetchall()
        
        for row in rows:
            current_video_ids.add(row['video_id'])
            if len(table_ids) == 0:
                transform_row = transform_data(row)
                insert_row(cur, conn, schema, [row['video_id'], transform_row['title'], transform_row['published_at'], (transform_row['duration']), transform_row['video_type'], transform_row['view_count'], transform_row['like_count'], transform_row['comment_count']])
            
            else:
                transform_row = transform_data(row)
                if row['video_id'] in table_ids:
                    update_row(cur, conn, schema, [row['video_id'], transform_row['title'], transform_row['published_at'], transform_row['duration'], transform_row['video_type'], transform_row['view_count'], transform_row['like_count'], transform_row['comment_count']])
                else:
                    insert_row(cur, conn, schema, [row['video_id'], transform_row['title'], transform_row['published_at'], transform_row['duration'], transform_row['video_type'], transform_row['view_count'], transform_row['like_count'], transform_row['comment_count']])
        
        ids_to_delete = set(table_ids) - current_video_ids
        if ids_to_delete:
            delete_row(cur, conn, schema, ids_to_delete)
        
        logger.info(f"Data warehouse table '{schema}.{table}' updated successfully with transformed data from staging table.")
        
    except Exception as e:
        logger.error(f"Error updating data warehouse table '{schema}.{table}': {e}")
        
    finally:
        close_db_conn(conn, cur)
        
        