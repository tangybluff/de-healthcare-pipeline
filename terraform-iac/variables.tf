# You can create 'terraform.tfvars' file to have the full path of the credentials file
# variable "credentials" {
#   description = "My Credentials"
#   default     = "./secretkeys/credentials.json"
# }
# To avoid hardcoding the credentials file path, you can use environment variables
# export GOOGLE_CREDENTIALS="path/to/your/credentials.json"
# echo $GOOGLE_CREDENTIALS

variable "project_id" {
  description = "Project"
  default     = "covidepidemetrics"
}


variable "region" {
  description = "Region"
  default     = "europe-southwest1"
}


variable "location" {
  description = "Project Location"
  default     = "EU"
}


variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "covid19_dataset"
}


variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "covidepidemetrics-bucket"
}


variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}