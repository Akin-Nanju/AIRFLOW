from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd


def extract_callable():
    print("EXTRACTING DATA")
    return {
        'date': '2024-08-18',
        'location': 'Bhaktapur',
        'temp': {
            'max': '32',
            'min': '20',
            'condition': 'rain'
        }
    }


def transform_callable(ti):
    extracted_data = ti.xcom_pull(task_ids='extract')
    return {
        'date': extracted_data.get('date'),
        'location': extracted_data.get('location'),
        'temp': extracted_data.get('temp').get('max'),
        'condition': extracted_data.get('temp').get('condition')
    }


def load_callable(ti):
    transformed_data = ti.xcom_pull(task_ids='transform')
    df = pd.DataFrame([transformed_data])
    df.columns = ['date', 'location', 'temp', 'condition']
    print(df)


default_args = {
    'owner': 'Akin',
    'start_date': datetime(2024, 8, 18),
    'retries': 2,
}

with DAG('weather',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False
         ) as dag:

    extract = PythonOperator(
        task_id='extract',
        python_callable=extract_callable
    )

    transform = PythonOperator(
        task_id='transform',
        python_callable=transform_callable,
        provide_context=True
    )

    load = PythonOperator(
        task_id='load',
        python_callable=load_callable,
        provide_context=True
    )

    extract >> transform >> load  # Set task dependencies
