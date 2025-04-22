# Install required packages
# %pip install --quiet kaggle pandas dlt[bigquery] google-cloud-storage gcsfs google-cloud-bigquery google-cloud-bigquery-storage

import os
import zipfile
import glob
import shutil
import pandas as pd
import dlt
from google.cloud import storage

# Step 1: Set up Kaggle credentials
os.makedirs(os.path.expanduser("~/.kaggle"), exist_ok=True)
shutil.copy("c:/Users/ahmed/Desktop/de-healthcare-pipeline/dlt-gcp-ingestion/kaggle/kaggle.json", os.path.expanduser("~/.kaggle/kaggle.json"))
os.chmod(os.path.expanduser("~/.kaggle/kaggle.json"), 0o600)

# Step 2: Set up GCP credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "c:/Users/ahmed/Desktop/de-healthcare-pipeline/secretkeys/credentials.json"

# Step 3: Download dataset from Kaggle
os.makedirs("tmp", exist_ok=True)
os.system("kaggle datasets download -d meirnizri/covid19-dataset -p tmp --unzip")

# Step 4: Locate the downloaded CSV file
csv_path = glob.glob("tmp/covid data.csv")[0]

# Step 5: Set BigQuery destination location
os.environ["DESTINATION__BIGQUERY__LOCATION"] = "EU"

# Step 6: Upload CSV to Google Cloud Storage
bucket_name = "covidepidemetrics-bucket"  # Replace with your GCS bucket name
gcs_path = "raw/covid19_data.csv"  # Path in GCS

client = storage.Client()
bucket = client.bucket(bucket_name)
blob = bucket.blob(gcs_path)
blob.upload_from_filename(csv_path)

# Step 7: Define DLT resource to read data from GCS
@dlt.resource
def covid_data_from_gcs():
    df = pd.read_csv(f"gs://{bucket_name}/{gcs_path}")
    for row in df.itertuples(index=False, name=None):
        yield dict(zip(df.columns, row))

# Step 8: Create and run the DLT pipeline
pipeline = dlt.pipeline(
    pipeline_name="covid_data_pipeline",
    destination="bigquery",
    dataset_name="covid19_dataset",  # BigQuery dataset name
    dev_mode=False  # Disable dev_mode for production-like behavior
)

load_info = pipeline.run(covid_data_from_gcs())
print("✅ Data loaded to BigQuery.", load_info)