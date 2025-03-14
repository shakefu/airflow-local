from datetime import datetime

from airflow.decorators import dag
from airflow.operators.bash import BashOperator


@dag(start_date=datetime(2021, 1, 1), schedule="@once", catchup=False)
def sleep_dag():
    t1 = BashOperator(
        task_id="sleep_2_seconds",
        bash_command="sleep 2",
    )
    t2 = BashOperator(
        task_id="sleep_3_seconds",
        bash_command="sleep 3",
    )
    t1 >> t2


sleep_dag()
