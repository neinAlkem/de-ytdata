import logging
from airflow.operators.bash import BashOperator

logger = logging.getLogger(__name__)

SODA_PATH = "/opt/airflow/include/soda"
DATA_SOURCE_NAME = "pg_datasource"

def check_data_quality(schema_name: str) -> BashOperator:
    try:
        return BashOperator(
            task_id=f"check_data_quality_{schema_name}",
            bash_command=f'soda scan -d {DATA_SOURCE_NAME} -c {SODA_PATH}/configuration.yml -v SCHEMA_NAME={schema_name} {SODA_PATH}/checks.yml'
        )
    except Exception as e:
        logger.error(f"Error creating data quality check task: {e}")
        raise