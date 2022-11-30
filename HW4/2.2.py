from datetime import datetime, timedelta, date
from textwrap import dedent
import time
import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
from csv import writer, reader
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

def fatch_data(**context):
    symbles = ["AAPL", "GOOGL", "META", "MSFT", "AMZN"]
    for s in symbles:
        tickers = yf.Tickers(s)
        data = tickers.tickers[s].info
        open_price = data["open"]
        high_price = data["dayHigh"]
        low_price = data["dayLow"]
        close_price = data["previousClose"]
        volume = data["volume"]
        context['ti'].xcom_push(key=s, value=[open_price, high_price, low_price, close_price, volume])

def train_model(**context):
    symbles = ["AAPL", "GOOGL", "META", "MSFT", "AMZN"]
    all_predict = []
    for s in symbles:
        todayPrice = context['ti'].xcom_pull(key=s,task_ids="fatch_data")
        data = yf.download(tickers = s, period = "11d", interval = "1d")
        data = data.drop(columns=["Adj Close"])
        x = data[:-1]
        y = data["High"][1:]
        reg = LinearRegression().fit(x, y)
        print(f"Current model accuracy: {reg.score(x, y)}")
        features = pd.DataFrame([todayPrice])
        prediction = reg.predict(features)[0]
        print(f"Prediction for next day's high: {prediction}")
        all_predict.append(prediction)
        context['ti'].xcom_push(key=s, value=prediction)
    today = date.today()
    d = today.strftime("%m/%d/%y")
    write = [d] + all_predict
    with open(f'predict.csv','a') as file:
        writer_object = writer(file)
        writer_object.writerow(write)
        file.close()

def caculate_error(**context):
    symbles = ["AAPL", "GOOGL", "META", "MSFT", "AMZN"]
    errors = []
    predictions = []
    today = date.today()
    d = today.strftime("%m/%d/%y")
    yesterday = today - timedelta(days = 1)
    yesterday = yesterday.strftime("%m/%d/%y")
    with open('predict.csv', 'r') as file:
        reader_object = reader(file)
        for row in reader_object:
            if row and row[0] == yesterday:
                predictions = row[1:]
                break
    print(f"Yesterday's prediction: {predictions}")
    for i in range(len(symbles)):
        high_price = context['ti'].xcom_pull(key=symbles[i],task_ids="fatch_data")[1]
        error = (float(predictions[i]) - float(high_price)) / float(high_price)
        errors.append(error)
    write = [d] + errors
    with open(f'errors.csv','a') as file:
        writer_object = writer(file)
        writer_object.writerow(write)
        file.close()
    print(f"Today's error: {write}")

default_args = {
    'owner': 'yutao',
    'depends_on_past': False,
    'email': ['yz4359@columbia.edu'],
    'email_on_failure': True,
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
    'Q2.2',
    default_args=default_args,
    description='Stock price fetching, prediction, and storage every day.',
    schedule_interval='0 7 * * *',
    start_date=datetime(2022, 11, 24),
    catchup=False,
    tags=['homework'],
) as dag:

    fatch_data = PythonOperator(
        task_id='fatch_data',
        python_callable=fatch_data,
        retries=3,
        provide_context=True
    )

    caculate_error = PythonOperator(
        task_id='caculate_error',
        python_callable=caculate_error,
        retries=3,
        provide_context=True
    )

    train_model = PythonOperator(
        task_id='train_model',
        python_callable=train_model,
        retries=3,
        provide_context=True
    )

    fatch_data >> train_model
    train_model >> caculate_error