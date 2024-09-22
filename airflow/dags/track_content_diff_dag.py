import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import grpc
from delty_grpc import TrackContentDifferenceServiceStub
from delty_grpc import track_content_difference_pb2

default_args = {
    "owner": "dimitris",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

GRPC_SERVER_ADDRESS = os.getenv("GRPC_SERVER_ADDRESS", "localhost:50051")


def trigger_track_content_difference():
    with grpc.insecure_channel(GRPC_SERVER_ADDRESS) as channel:
        stub = TrackContentDifferenceServiceStub(channel)
        response = stub.TriggerTrackContentDifference(
            track_content_difference_pb2.TriggerRequest()
        )
        if response.success:
            print(f"Command executed successfully: {response.message}")
        else:
            print(f"Command failed: {response.message}")


with DAG(
    dag_id="track_content_difference_dag",
    default_args=default_args,
    description="DAG to trigger track_content_difference command in the Delty service via gRPC",
    schedule_interval="*/10 * * * *",  # Runs every minute
    start_date=datetime(2023, 9, 1),
    catchup=False,
) as dag:
    trigger_task = PythonOperator(
        task_id="trigger_track_content_difference",
        python_callable=trigger_track_content_difference,
    )
