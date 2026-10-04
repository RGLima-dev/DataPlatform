from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, input_file_name
import time

spark = (
    SparkSession.builder
    .appName("weather-bronze")
    .getOrCreate()
)

RAW_PATH = "/opt/spark/data/raw/weather/*.json"
BRONZE_PATH = "/opt/spark/data/bronze/weather"


print("\n=== READING RAW JSON ===\n")

df = (
    spark.read
    .option("multiLine", True)
    .json(RAW_PATH)
)


print("\n=== RAW SCHEMA ===\n")

df.printSchema()


print("\n=== RAW DATA ===\n")

df.show(
    n=1,
    truncate=False
)


bronze_df = (
    df
    .withColumn(
        "ingestion_timestamp",
        current_timestamp()
    )
    .withColumn(
        "source_file",
        input_file_name()
    )
)

(
    bronze_df.write
    .mode("overwrite")
    .parquet(BRONZE_PATH)
)

bronze_df.show(5)

print(f"\nBronze successfully written to: {BRONZE_PATH}")
spark.stop()