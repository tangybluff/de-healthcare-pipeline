import os
import glob
import zipfile
import kaggle
from google.cloud import storage, bigquery

#— CONFIG (via env vars) —#
# GOOGLE_APPLICATION_CREDENTIALS must point at your GCP service account JSON
BUCKET_NAME = os.getenv("BUCKET_NAME")            # e.g. your-project-id-data-lake
BQ_DATASET  = os.getenv("BQ_DATASET", "bronze")   # e.g. bronze
BQ_TABLE    = os.getenv("BQ_TABLE", "covid_raw")  # e.g. covid_raw

DOWNLOAD_DIR = "tmp"

def download_from_kaggle(dataset: str, download_dir: str) -> str:
    kaggle.api.authenticate()
    os.makedirs(download_dir, exist_ok=True)
    kaggle.api.dataset_download_files(dataset, path=download_dir, unzip=True)
    # Assume one CSV in the root after unzip
    csvs = glob.glob(f"{download_dir}/*.csv")
    if not csvs:
        raise FileNotFoundError("No CSV found after Kaggle download")
    return csvs[0]

def upload_to_gcs(bucket_name: str, source_file: str, dest_blob: str):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(dest_blob)
    blob.upload_from_filename(source_file)
    print(f"✔ Uploaded {source_file} to gs://{bucket_name}/{dest_blob}")

def load_csv_to_bq(bucket_name: str, blob_name: str, dataset_id: str, table_id: str):
    client = bigquery.Client()
    uri = f"gs://{bucket_name}/{blob_name}"
    table_ref = client.dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )
    load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)
    load_job.result()  # wait
    table = client.get_table(table_ref)
    print(f"✔ Loaded {table.num_rows} rows into {dataset_id}.{table_id}")

if __name__ == "__main__":
    # 1. Download from Kaggle
    dataset = "meirnizri/covid19-dataset"
    csv_path = download_from_kaggle(dataset, DOWNLOAD_DIR)

    # 2. Upload to GCS
    blob_name = f"raw/{os.path.basename(csv_path)}"
    upload_to_gcs(BUCKET_NAME, csv_path, blob_name)

    # 3. Load into BigQuery
    load_csv_to_bq(BUCKET_NAME, blob_name, BQ_DATASET, BQ_TABLE)
