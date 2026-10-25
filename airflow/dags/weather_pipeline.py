import pendulum

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from extract_layer.extract import run_extraction


with DAG(
    dag_id="weather_pipeline",
    start_date=pendulum.datetime(2026, 9, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["weather", "spark"],
) as dag:

    extract = PythonOperator(
        task_id="extract_weather",
        python_callable=run_extraction
    )

    bronze = SparkSubmitOperator(
        task_id="bronze",
        application="/opt/spark/jobs/bronze_layer/bronze.py",
        conn_id="spark_default",
        name="weather-bronze",
        verbose=True,
        conf={
            "spark.hadoop.fs.permissions.umask-mode":"002"
        }
    )

    silver = SparkSubmitOperator(
        task_id="silver",
        application="/opt/spark/jobs/silver_layer/silver.py",
        conn_id="spark_default",
        name="weather-silver",
        verbose=True,
        conf={
                    "spark.hadoop.fs.permissions.umask-mode":"002"
                }
    )

    gold = SparkSubmitOperator(
        task_id="gold",
        application="/opt/spark/jobs/gold_layer/gold.py",
        conn_id="spark_default",
        name="weather-gold",
        verbose=True,
        conf={
                    "spark.hadoop.fs.permissions.umask-mode":"002"
                }
    )

    extract >> bronze >> silver >> gold