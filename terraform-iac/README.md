# Terraform Infrastructure as Code (IaC) for GCP/GCS/BigQuery

## Overview
This folder contains Terraform configuration files used to provision and manage cloud infrastructure on Google Cloud Platform (GCP). Specifically, it is designed to set up resources such as Google Cloud Storage (GCS) buckets and BigQuery datasets. Terraform is an open-source Infrastructure as Code (IaC) tool that allows you to define and manage your cloud infrastructure in a declarative manner.

## What is Terraform?
Terraform is a tool for building, changing, and versioning infrastructure safely and efficiently. It uses configuration files to describe the desired state of your infrastructure, and it ensures that the actual state matches the desired state through a process called "terraform apply."

## Why Use Infrastructure as Code (IaC)?
Using IaC provides several benefits:

1. **Consistency**: IaC ensures that your infrastructure is consistent across environments (e.g., development, staging, production).
2. **Version Control**: Since IaC files are text-based, they can be stored in version control systems like Git, enabling you to track changes and collaborate with your team.
3. **Automation**: IaC automates the provisioning and management of infrastructure, reducing manual errors and saving time.
4. **Scalability**: IaC makes it easier to scale your infrastructure by simply updating the configuration files and reapplying them.

## How to Use This Folder
1. **Install Terraform**: Ensure that Terraform is installed on your system. You can download it from [Terraform's official website](https://www.terraform.io/).

2. **Initialize Terraform**: Run the following command to initialize the Terraform working directory:
   ```bash
   terraform init
   ```

3. **Plan the Infrastructure**: Use the `terraform plan` command to preview the changes that Terraform will make to your infrastructure:
   ```bash
   terraform plan
   ```

4. **Apply the Configuration**: Apply the configuration to create or update the infrastructure:
   ```bash
   terraform apply
   ```

5. **Destroy the Infrastructure**: If you need to tear down the infrastructure, use the `terraform destroy` command:
   ```bash
   terraform destroy
   ```

## Files in This Folder
- `main.tf`: The main configuration file that defines the GCP resources to be created.
- `variables.tf`: Contains variable definitions for the Terraform configuration.
- `terraform.tfstate`: The state file that tracks the current state of your infrastructure (auto-generated).
- `terraform.tfstate.backup`: A backup of the state file (auto-generated).

## Best Practices
- **Use Variables**: Define variables in `variables.tf` to make your configuration reusable and easier to manage.
- **Secure Sensitive Data**: Avoid hardcoding sensitive information like credentials. Use environment variables or secret management tools.
- **Version Control**: Commit your Terraform files to a version control system like Git to track changes and collaborate with your team.
