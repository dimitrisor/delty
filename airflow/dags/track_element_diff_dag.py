from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default args for the DAG
default_args = {
    "owner": "dimitris",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id="track_element_diff_dag",
    default_args=default_args,
    description="DAG to trigger track_element_diff.py in Delty service",
    schedule_interval="*/10 * * * *",  # Runs every 10 minutes
    start_date=datetime(2023, 9, 1),
    catchup=False,
) as dag:
    # Define a task to trigger the script in the Delty container
    run_track_element_diff = BashOperator(
        task_id="run_track_element_diff",
        bash_command="docker exec delty poetry run python track_element_diff.py",
    )
