from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
import os

def main():
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("CSV to BigQuery") \
        .getOrCreate()

    # Define GCS bucket and file details
    bucket_name = "covid19_dataset"
    csv_file_path = "covid19_data/Covid Data.csv"
    gcs_file_path = f"gs://{bucket_name}/{csv_file_path}"

    # Define BigQuery details
    bigquery_project = "your-gcp-project-id"
    bigquery_dataset = "your_dataset_name"
    bigquery_table = "your_table_name"

    # Read CSV file from GCS
    schema = StructType([
        StructField("column1", StringType(), True),
        StructField("column2", IntegerType(), True),
        StructField("column3", DoubleType(), True)
        # Add more fields as per your CSV structure
    ])

    df = spark.read.format("csv") \
        .option("header", "true") \
        .schema(schema) \
        .load(gcs_file_path)

    # Write DataFrame to BigQuery
    df.write.format("bigquery") \
        .option("table", f"{bigquery_project}:{bigquery_dataset}.{bigquery_table}") \
        .option("temporaryGcsBucket", bucket_name) \
        .mode("append") \
        .save()

    print("Data successfully written to BigQuery")

if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set in the environment
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")

    main()