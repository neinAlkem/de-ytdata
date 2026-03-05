from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from api.extract_video_stats import get_playlist_id, get_video_ids, extract_video_stats, save_stats_to_json
from warehouse.dwh import stg_table, dbo_table
from data_quality_check.soda import check_data_quality
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

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
) as dag_produce:
    
    task_get_playlist = get_playlist_id()
    task_get_video_ids = get_video_ids(task_get_playlist)
    task_get_stats = extract_video_stats(task_get_video_ids)
    task_save_json = save_stats_to_json(task_get_stats, 'video_stats')
    
    trigger_update_db = TriggerDagRunOperator(
        task_id='trigger_update_db',
        trigger_dag_id='update_db',
        wait_for_completion=True,
        reset_dag_run=True
    )
    
    task_get_playlist >> task_get_video_ids >> task_get_stats >> task_save_json >> trigger_update_db
    
with DAG(
    'update_db',
    default_args=default_args,
    description='Script to update database with video statistics from YouTube Data API',
    schedule_interval='0 15 * * *',
    catchup=False,
) as dag_update_db:
    
    task_stg_table = stg_table()
    task_dbo_table = dbo_table()
    
    trigger_data_qc = TriggerDagRunOperator(
        task_id='trigger_data_quality_check',
        trigger_dag_id='data_quality_check',
        wait_for_completion=True,
        reset_dag_run=True
    )
    
    task_stg_table >> task_dbo_table >> trigger_data_qc

with DAG(
    'data_quality_check',
    default_args=default_args,
    description='Data quality check using Soda for both layer',
    schedule_interval='0 16 * * *',
    catchup=False,
) as dag_quality:
    
    task_stg_table = check_data_quality('stg')
    task_dbo_table = check_data_quality('dbo')
    
    task_stg_table >> task_dbo_table
