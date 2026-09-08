import pendulum

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator


with DAG(
    dag_id="weather_pipeline",
    start_date=pendulum.datetime(2026, 9, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["weather", "spark"],
) as dag:

    extract = BashOperator(
        task_id="extract_weather",
        bash_command="python3 /opt/spark/jobs/extract.py",
    )

    bronze = SparkSubmitOperator(
        task_id="bronze",
        application="/opt/spark/jobs/bronze.py",
        conn_id="spark_default",
        name="weather-bronze",
        verbose=True,
        conf={
            "spark.hadoop.fs.permissions.umask-mode":"002"
        }
    )

    silver = SparkSubmitOperator(
        task_id="silver",
        application="/opt/spark/jobs/silver.py",
        conn_id="spark_default",
        name="weather-silver",
        verbose=True,
        conf={
                    "spark.hadoop.fs.permissions.umask-mode":"002"
                }
    )

    extract >> bronze >> silver