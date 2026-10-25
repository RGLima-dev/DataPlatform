from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, input_file_name
import os

spark = (
    SparkSession.builder
    .appName("weather-bronze")
    .getOrCreate()
)

S3_BUCKET_NAME = os.environ["S3_BUCKET_NAME"]

RAW_PATH = "s3a://{S3_BUCKET_NAME}/raw/weather/"
BRONZE_PATH = "/opt/spark/data/bronze/weather"


print("\n=== READING RAW JSON ===\n")

df = (
    spark.read
    .option("multiLine", True)
    .option("recursiveFileLookup", "true")
    .option("pathGlobFilter", "*.json")
    .json(RAW_PATH)
)


print("\n=== RAW SCHEMA ===\n")

df.printSchema()


print("\n=== RAW DATA ===\n")


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
bronze_df.show()


(
    bronze_df.write
    .mode("overwrite")
    .parquet(BRONZE_PATH)
)

print(f"\nBronze successfully written to: {BRONZE_PATH}")
spark.stop()