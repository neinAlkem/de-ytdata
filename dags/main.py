from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from api.extract_video_stats import get_playlist_id, get_video_ids, extract_video_stats, save_stats_to_json

local_timezone = pendulum.timezone("Asia/Jakarta")

default_args = {
    'owner': 'neinAlkem',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'email': 'kaptenbagaz@gmail.com',
    'retries': 3,
    'max_active_runs': 1,
    'dagrun_timeout': timedelta(hours=1),
    'start_date': datetime(2026, 1, 1, tzinfo=local_timezone),
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'produce_video_stats',
    default_args=default_args,
    description='Script to extract video statistics from YouTube Data API and save it as JSON file',
    schedule_interval='0 14 * * *',
    catchup=False,
) as dag:
    
    task_get_playlist = get_playlist_id()
    task_get_video_ids = get_video_ids(task_get_playlist)
    task_get_stats = extract_video_stats(task_get_video_ids)
    task_save_json = save_stats_to_json(task_get_stats, 'video_stats')
    
    task_get_playlist >> task_get_video_ids >> task_get_stats >> task_save_json