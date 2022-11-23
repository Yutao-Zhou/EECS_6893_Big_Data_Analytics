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

count = 0

def correct_sleeping_function():
    time.sleep(2)

def count_function():
    global count
    count += 1
    print('count_increase output: {}'.format(count))
    time.sleep(2)

def print_function():
    print("This is a print function.")
    time.sleep(2)

def wrong_sleeping_function():
    # this task is t2_1, t1 >> t2_1
    global count
    print('wrong sleeping function output: {}'.format(count))
    assert count == 1
    time.sleep(2)


############################################
# DEFINE AIRFLOW DAG (SETTINGS + SCHEDULE)
############################################

default_args = {
    'owner': 'yutao',
    'depends_on_past': False,
    'email': ['yl4860@columbia.edu'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=3),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

with DAG(
    'Q2.1',
    default_args=default_args,
    description='Task 2 impliment the DAG below',
    schedule_interval=timedelta(minutes=30),
    start_date=datetime(2022, 11, 22, 19, 35),
    catchup=False,
    tags=['homework'],
) as dag:

##########################################
# DEFINE AIRFLOW OPERATORS
##########################################

    # t* examples of tasks created by instantiating operators

    t1 = BashOperator(
        task_id='t1',
        bash_command='sleep 2',
        retries=3,
    )

    t2 = BashOperator(
        task_id='t2',
        bash_command='echo "This is a Bash echo command"',
        retries=3,
    )

    t3 = BashOperator(
        task_id='t3',
        bash_command='echo "This is a Bash echo command"',
        retries=3,
    )

    t4 = PythonOperator(
        task_id='t4',
        python_callable=correct_sleeping_function,
        retries=3,
    )

    t5 = BashOperator(
        task_id='t5',
        bash_command='./dir.sh',
        retries=3,
    )

    t6 = BashOperator(
        task_id='t6',
        bash_command='echo "This is a Bash echo command"',
        retries=3,
    )

    t7 = PythonOperator(
        task_id='t7',
        python_callable=correct_sleeping_function,
        retries=3,
    )

    t8 = PythonOperator(
        task_id='t8',
        python_callable=print_function,
        retries=3,
    )

    t9 = BashOperator(
        task_id='t9',
        bash_command='echo "This is a Bash echo command"',
        retries=3,
    )

    t10 = BashOperator(
        task_id='t10',
        bash_command='./dir.sh',
        retries=3,
    )

    t11 = PythonOperator(
        task_id='t11',
        python_callable=print_function,
        retries=3,
    )

    t12 = PythonOperator(
        task_id='t12',
        python_callable=count_function,
        retries=3,
    )

    t13 = BashOperator(
        task_id='t13',
        bash_command='sleep 2',
        retries=3,
    )

    t14 = BashOperator(
        task_id='t14',
        bash_command='sleep 2',
        retries=3,
    )

    t15 = PythonOperator(
        task_id='t15',
        python_callable=count_function,
        retries=3,
    )

    t16 = PythonOperator(
        task_id='t16',
        python_callable=print_function,
        retries=3,
    )

    t17 = BashOperator(
        task_id='t17',
        bash_command='echo "This is a Bash echo command"',
        retries=3,
    )

    t18 = BashOperator(
        task_id='t18',
        bash_command='./dir.sh',
        retries=3,
    )

    t19 = PythonOperator(
        task_id='t19',
        python_callable=correct_sleeping_function,
        retries=3,
    )
##########################################
# DEFINE TASKS HIERARCHY
##########################################

    # task dependencies 

    t1 >> [t5, t2, t3, t4]
    t5 >> [t8, t9]
    t2 >> t6
    t3 >> t7
    [t9, t3] >> t12
    t8 >> [t10, t15]
    t9 >> t11
    t7 >> t13
    [t10, t11, t12, t7] >> t14
    t14 >> [t16, t17]
    [t17, t15, t7, t13] >> t18
    [t16, t18] >> t19