"""Airflow DAG for experimental data pipeline.

Schedule: daily at midnight.
"""

# from airflow import DAG
# from airflow.operators.python import PythonOperator


def extract():
    pass


def transform():
    pass


def load():
    pass


# with DAG(
#     "exp_data_dag",
#     start_date=datetime(2024, 1, 1),
#     schedule="0 0 * * *",
# ) as dag:
#     t1 = PythonOperator(task_id="extract", python_callable=extract)
#     t2 = PythonOperator(task_id="transform", python_callable=transform)
#     t3 = PythonOperator(task_id="load", python_callable=load)
#     t1 >> t2 >> t3

if __name__ == '__main__':
    print('DAG placeholder')
