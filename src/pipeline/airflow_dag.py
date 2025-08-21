from airflow import DAG
from datetime import datetime, timedelta

from airflow.providers.standard.operators.python import PythonOperator

from src.pipeline.main import SocialMediaPipeline

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'social_media_analytics',
    default_args=default_args,
    description='Daily social media analytics pipeline',
    schedule_interval='@daily',
    catchup=False,
    tags=['social_media', 'analytics']
)

def run_pipeline():
    pipeline = SocialMediaPipeline()
    pipeline.run()

pipeline_task = PythonOperator(
    task_id='run_social_media_pipeline',
    python_callable=run_pipeline,
    dag=dag
)