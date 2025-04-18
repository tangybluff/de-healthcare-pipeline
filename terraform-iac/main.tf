# TERRAFORM CONFIGURATION
# This is a Terraform configuration file for creating a Google Cloud Storage bucket and a BigQuery dataset.


# TERRAFORM BLOCK
# Specifies the required provider and its version
# The Google provider is used to interact with Google Cloud resources
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.19.0"
    }
  }
}


# PROVIDER CONFIGURATION
# Configures the Google Cloud provider with credentials, project ID and region
provider "google" {
#  credentials = file(var.credentials)
  project     = var.project_id
  region      = var.region
}


# GOOGLE CLOUD STORAGE BUCKET CONFIGURATION
# Creates a GCS bucket with lifecycle rules for data storage
resource "google_storage_bucket" "covidepidemetrics-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}


# BIGQUERY DATASET CONFIGURATION
# Creates a BigQuery dataset for storing and analyzing COVID-19 data
resource "google_bigquery_dataset" "covid19_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location 
}


# terraform fmt to format the file
# terraform init to initialize the directory
# terraform validate to validate the file configuration
# export GOOGLE_CREDENTIALS="path/to/your/credentials.json"
# echo $GOOGLE_CREDENTIALS
# terraform plan to see the changes
# terraform apply to apply the changes