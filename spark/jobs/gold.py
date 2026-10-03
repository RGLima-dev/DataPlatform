from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg,
    max,
    min,
    sum,
    to_date
)

spark = (
    SparkSession.builder
    .appName("weather-gold")
    .getOrCreate()
)

SILVER_PATH = "/opt/spark/data/silver/weather"
GOLD_PATH = "/opt/spark/data/gold/weather_daily"


silver_df = spark.read.parquet(SILVER_PATH)

gold_df = (
    silver_df
    .withColumn("date", to_date("weather_timestamp"))
    .groupBy("city", "date")
    .agg(
        avg("temperature_c").alias("avg_temperature"),
        max("temperature_c").alias("max_temperature"),
        min("temperature_c").alias("min_temperature"),
        avg("wind_speed_kmh").alias("avg_wind_speed"),
        avg("humidity_pct").alias("avg_humidity")
    )
    .orderBy("date")
)

gold_df.show(truncate=False)

gold_df.write \
    .mode("overwrite") \
    .parquet(GOLD_PATH)