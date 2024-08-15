from airflow import DAG
from airflow.operators.email import EmailOperator

from datetime import datetime

default_args={
    'owner':'Akin',
    'start_date':datetime(2024,8,11),
    'retries':2,
}

with DAG('Akin02',
         start_date = datetime(2024,8,11),
         schedule_interval = '@daily',
         catchup = False)as dag:
    
    send_email2 = EmailOperator(
        task_id = 'Email2',
        to = 'bagishgautam4@gmail.com',
        subject = 'TRYING AIRFLOW',
        html_content = 'HELLO HI THERE'
        
    )
    send_email2
 