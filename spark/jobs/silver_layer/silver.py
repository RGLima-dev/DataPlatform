from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import time
import os

spark = (SparkSession.builder.appName("Weather-silver").getOrCreate())

S3_BUCKET_NAME = os.environ["S3_BUCKET_NAME"]

BRONZE_PATH = f"s3a://{S3_BUCKET_NAME}/bronze/weather/"
SILVER_PATH = f"s3a://{S3_BUCKET_NAME}/silver/weather/"

bronze_df = spark.read.parquet(BRONZE_PATH)

zipped_df = bronze_df.withColumn("weather_hour",F.arrays_zip(
    F.col("hourly.time"),
    F.col("hourly.temperature_2m"),
    F.col("hourly.relative_humidity_2m"),
    F.col("hourly.precipitation"),
    F.col("hourly.wind_speed_10m")
))

exploded_df = zipped_df.withColumn("weather_hour",F.explode("weather_hour"))


silver_df = exploded_df.select(
    F.col("city"),
    F.col("latitude"),
    F.col("longitude"),
    F.to_timestamp(F.col("weather_hour.time"),"yyyy-MM-dd'T'HH:mm").alias("weather_timestamp"),
    F.col("weather_hour.temperature_2m").cast("double").alias("temperature_c"),
    F.col("weather_hour.relative_humidity_2m").cast("int").alias("humidity_pct"),
    F.col("weather_hour.precipitation").cast("double").alias("precipitation_mm"),
    F.col("weather_hour.wind_speed_10m").cast("double").alias("wind_speed_kmh"),
    F.col("ingestion_timestamp"),
    F.col("source_file"),
)

#Writing to silver path
silver_df.write.mode("overwrite").parquet(SILVER_PATH)
