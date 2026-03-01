import logging

logger = logging.getLogger(__name__)
table = 'yt_api'

def insert_row(cur, conn, schema_name, row) -> None :
    try:
        if schema_name == 'stg':
            insert_query = f"""
                INSERT INTO {schema_name}.{table} (video_id, title, published_at, duration, view_count, like_count, comment_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        else:
            insert_query = f"""
                INSERT INTO {schema_name}.{table} (video_id, title, published_at, duration, view_count, like_count, comment_count)
                VALUES (%s, %s, %s, %s::time, %s, %s, %s)
            """
        cur.execute(insert_query, row)
        conn.commit()
        logger.info(f"Inserting row with video_id '{row[0]}' into schema '{schema_name}' successful.")
    except Exception as e:
        logger.error(f"Error inserting row into schema with video id '{row[0]}': {e}")
        conn.rollback()
        raise e

def update_row(cur, conn, schema_name, row) -> None:
    try:
        if schema_name == 'stg':
            update_query = f"""
                UPDATE {schema_name}.{table}
                SET title = %s, view_count = %s, like_count = %s, comment_count = %s
                WHERE video_id = %s AND duration = %s
            """ 
        else:
            update_query = f"""
                UPDATE {schema_name}.{table}
                SET title = %s, view_count = %s, like_count = %s, comment_count = %s
                WHERE video_id = %s AND duration = %s::time
            """
        params = (row[1], row[4], row[5], row[6], row[0], row[3])
        cur.execute(update_query, params)
        conn.commit()
        logger.info(f"Updating row with video_id '{row[0]}' in schema '{schema_name}' successful.")
    except Exception as e:
        logger.error(f"Error updating row in schema with video id '{row[0]}': {e}")
        conn.rollback()
        raise e
    
def delete_row(cur, conn, schema_name, video_id) -> None:
    try:
        placeholders = ','.join(['%s'] * len(video_id))
        cur.execute(f"DELETE FROM {schema_name}.{table} WHERE video_id IN ({placeholders});", tuple(video_id))
        conn.commit()
        logger.info(f"Deleting rows with video_id in '{video_id}' from schema '{schema_name}' successful.")
    except Exception as e:
        logger.error(f"Error deleting rows from schema with video ids in '{video_id}': {e}")
        conn.rollback()
        raise e