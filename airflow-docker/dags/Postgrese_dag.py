from airflow import DAG
from datetime import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator

# Default arguments for the DAG
default_args = {
    'owner': 'Akin3',
    'start_date': datetime(2024, 8, 14),
    'retries': 2,
}

# Define the DAG
with DAG(
    'Post',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:
    
    # Define the task
    create_table_task = PostgresOperator(
        task_id='create_default',
        postgres_conn_id='postgres_default',
        sql='''
        CREATE TABLE IF NOT EXISTS TRY(
            ID INT PRIMARY KEY,
            NAME VARCHAR(50)
        );
        '''
    )
