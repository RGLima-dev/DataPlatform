import pendulum

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from extract_layer.extract import run_extraction
import os


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
        packages="org.apache.spark:spark-hadoop-cloud_2.13:4.2.0",
        name="weather-bronze",
        verbose=True,
        env_vars={
        "AWS_ACCESS_KEY_ID": os.environ["AWS_SPARK_ACCESS_KEY_ID"],
        "AWS_SECRET_ACCESS_KEY": os.environ["AWS_SPARK_SECRET_ACCESS_KEY"],
        "AWS_DEFAULT_REGION": os.environ["AWS_SPARK_DEFAULT_REGION"],
        },
        conf={
            "spark.hadoop.fs.permissions.umask-mode":"002",
            "spark.jars.ivy": "/tmp/ivy",

                "spark.executorEnv.AWS_ACCESS_KEY_ID":
                os.environ["AWS_SPARK_ACCESS_KEY_ID"],

                "spark.executorEnv.AWS_SECRET_ACCESS_KEY":
                os.environ["AWS_SPARK_SECRET_ACCESS_KEY"],

                "spark.executorEnv.AWS_DEFAULT_REGION":
                os.environ["AWS_SPARK_DEFAULT_REGION"],
        }
    )

    silver = SparkSubmitOperator(
        task_id="silver",
        application="/opt/spark/jobs/silver_layer/silver.py",
        conn_id="spark_default",
        packages="org.apache.spark:spark-hadoop-cloud_2.13:4.2.0",
        name="weather-silver",
        verbose=True,
        env_vars={
        "AWS_ACCESS_KEY_ID": os.environ["AWS_SPARK_ACCESS_KEY_ID"],
        "AWS_SECRET_ACCESS_KEY": os.environ["AWS_SPARK_SECRET_ACCESS_KEY"],
        "AWS_DEFAULT_REGION": os.environ["AWS_SPARK_DEFAULT_REGION"],
        },
        conf={
            "spark.hadoop.fs.permissions.umask-mode":"002",
            "spark.jars.ivy": "/tmp/ivy",

                "spark.executorEnv.AWS_ACCESS_KEY_ID":
                os.environ["AWS_SPARK_ACCESS_KEY_ID"],

                "spark.executorEnv.AWS_SECRET_ACCESS_KEY":
                os.environ["AWS_SPARK_SECRET_ACCESS_KEY"],

                "spark.executorEnv.AWS_DEFAULT_REGION":
                os.environ["AWS_SPARK_DEFAULT_REGION"],
        }
    )

    gold = SparkSubmitOperator(
        task_id="gold",
        application="/opt/spark/jobs/gold_layer/gold.py",
        conn_id="spark_default",
        packages="org.apache.spark:spark-hadoop-cloud_2.13:4.2.0",
        name="weather-gold",
        verbose=True,
        env_vars={
        "AWS_ACCESS_KEY_ID": os.environ["AWS_SPARK_ACCESS_KEY_ID"],
        "AWS_SECRET_ACCESS_KEY": os.environ["AWS_SPARK_SECRET_ACCESS_KEY"],
        "AWS_DEFAULT_REGION": os.environ["AWS_SPARK_DEFAULT_REGION"],
        },
        conf={
            "spark.hadoop.fs.permissions.umask-mode":"002",
            "spark.jars.ivy": "/tmp/ivy",

                "spark.executorEnv.AWS_ACCESS_KEY_ID":
                os.environ["AWS_SPARK_ACCESS_KEY_ID"],

                "spark.executorEnv.AWS_SECRET_ACCESS_KEY":
                os.environ["AWS_SPARK_SECRET_ACCESS_KEY"],

                "spark.executorEnv.AWS_DEFAULT_REGION":
                os.environ["AWS_SPARK_DEFAULT_REGION"],
        }
    )

    extract >> bronze >> silver >> gold