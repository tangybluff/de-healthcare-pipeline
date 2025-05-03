# Install required packages
# %pip install --quiet kaggle pandas dlt[bigquery] google-cloud-storage gcsfs google-cloud-bigquery google-cloud-bigquery-storage

import os
import sys
import zipfile
import glob
import shutil
import pandas as pd
import dlt
import subprocess
import traceback
from pathlib import Path
from google.cloud import storage

def main():
    try:
        print("Starting kaggle_dlt_extract_load.py")
        # Get the base directory path
        base_dir = Path(__file__).parent.parent.absolute()
        print(f"Base directory: {base_dir}")
        
        # Step 1: Set up Kaggle credentials
        kaggle_credentials_path = os.path.join(base_dir, "dlt-gcp-ingestion", "kaggle", "kaggle.json")
        print(f"Looking for Kaggle credentials at: {kaggle_credentials_path}")
        
        # Try a more direct path if the above doesn't work
        if not os.path.exists(kaggle_credentials_path):
            print("Kaggle credentials not found at computed path, trying direct path...")
            kaggle_credentials_path = "c:/Users/ahmed/Desktop/de-healthcare-pipeline/dlt-gcp-ingestion/kaggle/kaggle.json"
            print(f"Looking for Kaggle credentials at direct path: {kaggle_credentials_path}")
        
        os.makedirs(os.path.expanduser("~/.kaggle"), exist_ok=True)
        
        if not os.path.exists(kaggle_credentials_path):
            raise FileNotFoundError(f"Kaggle credentials not found at: {kaggle_credentials_path}")
            
        print(f"Copying Kaggle credentials from {kaggle_credentials_path}")
        shutil.copy(kaggle_credentials_path, os.path.expanduser("~/.kaggle/kaggle.json"))
        os.chmod(os.path.expanduser("~/.kaggle/kaggle.json"), 0o600)

        # Step 2: Set up GCP credentials
        gcp_credentials_path = os.path.join(base_dir, "secretkeys", "credentials.json")
        print(f"Looking for GCP credentials at: {gcp_credentials_path}")
        
        # Try a more direct path if the above doesn't work
        if not os.path.exists(gcp_credentials_path):
            print("GCP credentials not found at computed path, trying direct path...")
            gcp_credentials_path = "c:/Users/ahmed/Desktop/de-healthcare-pipeline/secretkeys/credentials.json"
            print(f"Looking for GCP credentials at direct path: {gcp_credentials_path}")
        
        if not os.path.exists(gcp_credentials_path):
            raise FileNotFoundError(f"GCP credentials not found at: {gcp_credentials_path}")
            
        print(f"Setting GCP credentials from {gcp_credentials_path}")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_credentials_path

        # Step 3: Create tmp directory
        tmp_dir = os.path.join(Path(__file__).parent, "tmp")
        print(f"Creating tmp directory at: {tmp_dir}")
        os.makedirs(tmp_dir, exist_ok=True)
        
        # Check if Kaggle is installed
        try:
            print("Checking if kaggle CLI is installed...")
            check_result = subprocess.run(["kaggle", "--version"], capture_output=True, text=True)
            print(f"Kaggle CLI version: {check_result.stdout.strip()}")
        except Exception as e:
            print(f"Error checking kaggle CLI: {e}")
            print("Installing kaggle CLI...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "kaggle"], check=True)
            except Exception as pip_e:
                print(f"Failed to install kaggle: {pip_e}")
        
        # Step 4: Download dataset from Kaggle using subprocess for better error handling
        print("Downloading dataset from Kaggle...")
        
        # Check if COVID data already exists in the tmp directory
        existing_files = glob.glob(os.path.join(tmp_dir, "*.csv"))
        if existing_files:
            print(f"CSV file(s) already exist in tmp directory: {existing_files}")
            # Skip download step
        else:
            # Try the kaggle command
            try:
                kaggle_command = ["kaggle", "datasets", "download", "-d", "meirnizri/covid19-dataset", "-p", tmp_dir, "--unzip"]
                print(f"Running command: {' '.join(kaggle_command)}")
                result = subprocess.run(kaggle_command, capture_output=True, text=True, check=True)
                print(f"Kaggle download output: {result.stdout}")
            except subprocess.CalledProcessError as e:
                print(f"Error downloading dataset: {e}")
                print(f"Error output: {e.stderr}")
                
                # Try using a direct URL as fallback
                try:
                    print("Attempting download from direct URL as fallback...")
                    import requests
                    url = "https://raw.githubusercontent.com/MeirNizri/COVID-19-Vaccine-Finder/main/data/covid%20data.csv"
                    response = requests.get(url)
                    
                    if response.status_code == 200:
                        with open(os.path.join(tmp_dir, "Covid Data.csv"), 'wb') as f:
                            f.write(response.content)
                        print("Downloaded CSV file from GitHub")
                    else:
                        print(f"Failed to download from URL: {response.status_code}")
                        raise
                except Exception as url_e:
                    print(f"Failed to download from URL: {url_e}")
                    raise
        
        # Step 5: Locate the downloaded CSV file
        csv_patterns = [
            os.path.join(tmp_dir, "covid data.csv"),
            os.path.join(tmp_dir, "Covid Data.csv"),
            os.path.join(tmp_dir, "*.csv")
        ]
        
        print(f"Looking for CSV files using patterns: {csv_patterns}")
        
        csv_path = None
        for pattern in csv_patterns:
            matches = glob.glob(pattern)
            if matches:
                csv_path = matches[0]
                break
                
        if not csv_path:
            raise FileNotFoundError(f"No CSV file found in {tmp_dir}")
            
        print(f"Found CSV file: {csv_path}")
        
        # Check file contents
        try:
            df = pd.read_csv(csv_path)
            print(f"CSV file loaded successfully: {len(df)} rows, {len(df.columns)} columns")
            print(f"Column names: {df.columns.tolist()}")
        except Exception as csv_e:
            print(f"Error reading CSV file: {csv_e}")
            raise

        # Step 6: Set BigQuery destination location
        os.environ["DESTINATION__BIGQUERY__LOCATION"] = "EU"
        print("Set BigQuery destination location to EU")

        # Step 7: Upload CSV to Google Cloud Storage
        bucket_name = "covidepidemetrics-bucket"  # Replace with your GCS bucket name
        gcs_path = "raw/covid19_data.csv"  # Path in GCS

        print(f"Uploading to GCS bucket: {bucket_name}/{gcs_path}")
        try:
            client = storage.Client()
            
            # Check if bucket exists
            print(f"Checking if bucket {bucket_name} exists...")
            try:
                bucket = client.get_bucket(bucket_name)
                print(f"Bucket {bucket_name} exists")
            except Exception as bucket_e:
                print(f"Bucket {bucket_name} doesn't exist: {bucket_e}")
                print("Creating bucket...")
                bucket = client.create_bucket(bucket_name, location="EU")
                
            blob = bucket.blob(gcs_path)
            blob.upload_from_filename(csv_path)
            print("Upload to GCS complete")
        except Exception as gcs_e:
            print(f"Error uploading to GCS: {gcs_e}")
            raise

        # Step 8: Define DLT resource to read data from GCS
        print("Setting up DLT resource")
        @dlt.resource
        def covid_data_from_gcs():
            df = pd.read_csv(f"gs://{bucket_name}/{gcs_path}")
            for row in df.itertuples(index=False, name=None):
                yield dict(zip(df.columns, row))

        # Step 9: Create and run the DLT pipeline
        print("Creating and running DLT pipeline...")
        try:
            pipeline = dlt.pipeline(
                pipeline_name="covid_data_pipeline",
                destination="bigquery",
                dataset_name="covid19_dataset",  # BigQuery dataset name
                dev_mode=False  # Disable dev_mode for production-like behavior
            )

            load_info = pipeline.run(covid_data_from_gcs())
            # Remove emoji to prevent encoding issues
            print("Data loaded to BigQuery successfully.")
            print(f"Load info: {load_info}")
            return load_info
        except Exception as dlt_e:
            print(f"Error in DLT pipeline: {dlt_e}")
            raise
        
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        print("Full traceback:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise

if __name__ == "__main__":
    main()