from datetime import datetime, timedelta
from textwrap import dedent
import time

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization


####################################################
# DEFINE PYTHON FUNCTIONS
####################################################

def get_user_name():
    pass

def get_user_tweets():
    pass

def data_processing():
    pass

def model_predict():
    pass

def result_visualize():
    pass

############################################
# DEFINE AIRFLOW DAG (SETTINGS + SCHEDULE)
############################################

default_args = {
    'owner': 'yutao',
    'depends_on_past': False,
    'email': ['yz4359@columbia.edu'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
}

with DAG(
    'Q3.2',
    default_args=default_args,
    description='Q3.2 DAG of my group project',
    schedule_interval=timedelta(days=30),
    start_date=datetime(2022, 11, 1),
    catchup=False,
    tags=['homework'],
) as dag:

##########################################
# DEFINE AIRFLOW OPERATORS
##########################################

    t1 = PythonOperator(
        task_id='get_user_name',
        python_callable=get_user_name,
    )

    t2 = PythonOperator(
        task_id='get_user_tweets',
        python_callable=get_user_tweets,
    )

    t3 = PythonOperator(
        task_id='data_processing',
        python_callable=data_processing,
    )

    t4 = PythonOperator(
        task_id='model_predict',
        python_callable=model_predict,
    )

    t5 = PythonOperator(
        task_id='result_visualize',
        python_callable=result_visualize,
    )

##########################################
# DEFINE TASKS HIERARCHY
##########################################

    t1 >> t2
    t2 >> t3
    t3 >> t4
    t4 >> t5