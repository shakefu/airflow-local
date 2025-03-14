import airflow


def hello_world_task():
    print("Hello, World!")


with airflow.DAG(
    "hello_world_dag",
    description="A simple hello world DAG",
    schedule_interval="@minute",
    start_date=airflow.utils.dates.days_ago(1),
    catchup=False,
) as dag:
    hello_world_task = airflow.operators.python_operator.PythonOperator(
        task_id="hello_world_task",
        python_callable=hello_world_task,
    )
