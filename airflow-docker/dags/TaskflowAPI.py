from airflow import DAG
from airflow.decorators import task
from datetime import datetime
import pandas as pd

default_args = {
    'owner': 'Akin',
    'start_date': datetime(2024, 8, 18),
    'retries': 2,
}

with DAG('etl_dag',
         default_args=default_args,
         start_date=datetime(2024, 8, 18, hour=9, minute=30),
         schedule_interval='@daily',
         catchup=False
         ) as dag:

    @task
    def extract():
        print("EXTRACTING DATA")
        return {
            "Name": 'Akin',
            "email": 'akinnnaju4@gmail.com',
            "address": {
                "city": 'Bhaktapur',
                "town": 'Kamalbinayak'
            },
            "university": 'Tribhuvan University',
            "college": 'Swastik'
        }

    @task
    def transform(data):
        return {
            "Name": data.get('Name'),
            "email": data.get('email'),
            "address": data.get('address').get('city'),
            "university": data.get('university'),
            "college": data.get('college')
        }

    @task
    def load(data):
        # Convert the data dictionary to a DataFrame
        df = pd.DataFrame([data])
        # Define column names
        df.columns = ['NAME', 'EMAIL', 'ADDRESS', 'UNI', 'COLLEGE']
        print(df)

    # Define the task dependencies
    data = extract()
    transformed_data = transform(data)
    load(transformed_data)
