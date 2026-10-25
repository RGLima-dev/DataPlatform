from pyspark.sql import SparkSession
import time
from pyspark.sql.functions import (
    avg,
    max,
    min,
    sum,
    to_date,
    round
)

spark = (
    SparkSession.builder
    .appName("weather-gold")
    .getOrCreate()
)

SILVER_PATH = "/opt/spark/data/silver/weather/*"
GOLD_PATH = "/opt/spark/data/gold/weather" 


silver_df = spark.read.parquet(SILVER_PATH)

gold_df = (
    silver_df
    .withColumn("date", to_date("weather_timestamp"))
    .groupBy("city", "date")
    .agg(
        round(avg("temperature_c"),2).alias("avg_temperature"),
        round(max("temperature_c"),2).alias("max_temperature"),
        round(min("temperature_c"),2).alias("min_temperature"),
        round(avg("wind_speed_kmh"),2).alias("avg_wind_speed"),
        round(avg("humidity_pct"),2).alias("avg_humidity")
    )
    .orderBy("date")
)

gold_df.show(truncate=False)

gold_df.write \
    .mode("overwrite") \
    .parquet(GOLD_PATH)