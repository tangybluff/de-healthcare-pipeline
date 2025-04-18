# DE Healthcare Pipeline

## Data Engineering ZoomCamp 2025 Final Project
### Overview
This project implements an end-to-end data pipeline processing COVID-19 data from Kaggle. The pipeline follows a batch processing approach, ingesting data into a data lake on GCP, transforming it using dbt with a medallion architecture, and visualizing insights through Looker dashboards.

### Problem Statement
The COVID-19 pandemic created unprecedented challenges for healthcare systems worldwide. As coronavirus infections spread, healthcare providers faced critical shortages of medical resources and struggled with efficient distribution of limited supplies. Massive volumes of patient data were generated daily in inconsistent formats, making it difficult to derive actionable insights. Healthcare professionals need reliable analytics to identify high-risk patients early, predict resource requirements, and allocate medical attention where it's most urgently needed. Without structured data processing systems, potentially life-saving patterns remain hidden in the data.

### Vision and Impact
This data pipeline aims to create a foundation for pandemic preparedness and response. By transforming raw COVID-19 data into structured, analytics-ready formats, the pipeline enables powerful downstream applications. Machine learning models can be trained on this processed data to predict patient outcomes, forecast resource needs, and identify high-risk populations. These predictive capabilities will be crucial for healthcare systems to respond more effectively to future pandemics, allowing for earlier interventions, better resource allocation, and ultimately, improved patient outcomes. The pipeline's scalable architecture ensures that as new data sources become available, they can be incorporated to continuously enhance predictive accuracy and broaden analytical insights.

### Use Cases
This pipeline serves multiple stakeholders including:
- **Healthcare Providers**: Predict resource needs (ventilators, ICU beds) based on patient risk profiles
- **Hospital Administrators**: Optimize staff and equipment allocation based on predicted patient requirements
- **Public Health Officials**: Identify demographic patterns in high-risk cases to guide preventive measures
- **Researchers**: Analyze correlations between pre-existing conditions and COVID-19 severity outcomes

### Data Dictionary
Data can be found on Kaggle from this [COVID19 Dataset](https://www.kaggle.com/datasets/meirnizri/covid19-dataset).
| Feature | Description | Values |
|---------|-------------|--------|
| sex | Patient's biological sex | 1 = female, 2 = male |
| age | Age of the patient | Numeric value |
| classification | COVID test result category | 1-3 = positive (different degrees), 4+ = negative/inconclusive |
| patient_type | Care type received | 1 = outpatient (returned home), 2 = hospitalization |
| pneumonia | Air sacs inflammation | 1 = yes, 2 = no |
| pregnancy | Pregnancy status | 1 = yes, 2 = no |
| diabetes | Diabetes status | 1 = yes, 2 = no |
| copd | Chronic obstructive pulmonary disease | 1 = yes, 2 = no |
| asthma | Asthma status | 1 = yes, 2 = no |
| inmsupr | Immunosuppression status | 1 = yes, 2 = no |
| hypertension | Hypertension status | 1 = yes, 2 = no |
| cardiovascular | Heart or blood vessel disease | 1 = yes, 2 = no |
| renal_chronic | Chronic renal disease | 1 = yes, 2 = no |
| other_disease | Other disease presence | 1 = yes, 2 = no |
| obesity | Obesity status | 1 = yes, 2 = no |
| tobacco | Tobacco use | 1 = yes, 2 = no |
| usmr | Medical unit level | Values representing 1st, 2nd, or 3rd level |
| medical_unit | National Health System institution type | Categorical values |
| intubed | Ventilator use | 1 = yes, 2 = no |
| icu | Intensive Care Unit admission | 1 = yes, 2 = no |
| date_died | Date of death if applicable | Date format or 9999-99-99 if survived |

### Project File Structure
```
de-healthcare-pipeline/
│
├── terraform/                  # Infrastructure as code
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── storage.tf
│   ├── bigquery.tf
│   └── service-accounts.tf
│
├── dlt_pipelines/              # Data ingestion components
│   ├── config.py
│   ├── kaggle_covid_pipeline.py
│   ├── schema_mapping.py
│   └── requirements.txt
│
├── kestra/                     # Workflow orchestration
│   ├── pipelines/
│   │   └── covid_pipeline.yaml
│   ├── config/
│   │   └── application.yml
│   └── scripts/
│       └── start_kestra.bat
│
├── dbt/                        # Data transformation
│   ├── profiles.yml
│   ├── dbt_project.yml
│   ├── models/
│   │   ├── bronze/
│   │   │   └── sources.yml
│   │   ├── silver/
│   │   │   └── covid_cleaned.sql
│   │   └── gold/
│   │       ├── covid_daily_metrics.sql
│   │       ├── covid_regional_analysis.sql
│   │       └── vaccination_effectiveness.sql
│   └── tests/
│       └── data_quality_tests.yml
│
└── dashboard/                  # Data visualization
    ├── covid_spread_dashboard.json
    ├── vaccination_metrics_dashboard.json
    └── looker_connection.yml
```

### Technological Components

#### Data Pipeline Architecture
Our COVID-19 data pipeline follows a modern data lakehouse approach with a medallion architecture (bronze, silver, gold layers). Data from Kaggle is ingested through DLT into GCS (bronze), cleaned and standardized using dbt in BigQuery (silver), and then transformed into analytics-ready datasets (gold). The entire workflow is orchestrated by Kestra, with infrastructure managed through Terraform.
#### Technological Components

| Component | Description | Usage | Benefits |
|-----------|------------|-------|----------|
| **Google Cloud Platform (GCP)** | Cloud computing platform providing infrastructure and managed services | Hosting all components of our data pipeline | Offers seamless integration between services, scalability, and managed solutions for big data |
| **Terraform** | Infrastructure as Code (IaC) tool | Provisioning and managing cloud resources | Ensures reproducible infrastructure setup, version control for infrastructure, and reduced configuration errors |
| **Kestra** | Workflow orchestration platform | Scheduling and monitoring pipeline execution | Provides reliable task scheduling, error handling, and dependency management for data workflows |
| **Data Load Tool (DLT)** | Python-based data ingestion framework | Extracting data from Kaggle and loading into GCS | Simplifies data extraction with built-in schema handling and incremental loading capabilities |
| **Google Cloud Storage (GCS)** | Object storage service | Data lake storage (bronze layer) | Scalable, durable storage for raw data files with strong integration to BigQuery |
| **BigQuery** | Serverless, scalable data warehouse | Storing processed data and enabling fast analytics | Handles large-scale data processing with columnar storage and SQL interface |
| **dbt (Data Build Tool)** | Transformation tool following ELT (Extract, Load, Transform) pattern | Implementing medallion architecture and transformations | Enables version-controlled, testable data transformations using SQL |
| **PySpark** | Python API for Apache Spark | Complex data processing tasks | Distributed computing capabilities for handling large datasets |
| **Looker Studio** | Business intelligence and data visualization platform | Creating interactive dashboards | Direct integration with BigQuery and powerful visualization capabilities |



### Implementation Guide: Step-by-Step Pipeline Creation

This implementation guide will walk you through building a complete COVID-19 data pipeline from scratch, explaining each step's purpose and how they interconnect to create meaningful insights.

#### 1. Infrastructure Setup with Terraform
**Purpose**: Establish the foundation of our pipeline by provisioning cloud resources in a consistent, reproducible way.

**Key Files**:
- `terraform/main.tf`: Defines GCP project and region settings
- `terraform/variables.tf`: Customizable input parameters
- `terraform/storage.tf`: Creates GCS buckets for our data lake
- `terraform/bigquery.tf`: Sets up datasets and tables for warehousing
- `terraform/service-accounts.tf`: Manages security permissions

**Local Setup**:
1. Install Terraform and authenticate with GCP
2. Create a service account with appropriate permissions

**Execution**:
```bash
# Navigate to terraform directory
cd terraform

# Initialize Terraform
terraform init

# Preview changes
terraform plan

# Apply infrastructure changes
terraform apply
```

**Success Indicators**: You'll see GCS buckets and BigQuery datasets created in your GCP console. Note the output values for use in subsequent steps.

#### 2. Data Ingestion with DLT
**Purpose**: Extract COVID-19 data from Kaggle and load it into our bronze layer (raw data lake) while maintaining data lineage.

**Key Files**:
- `dlt_pipelines/config.py`: Stores credentials and connection parameters
- `dlt_pipelines/kaggle_covid_pipeline.py`: Defines extraction logic and loading destinations
- `dlt_pipelines/schema_mapping.py`: Ensures consistent data structure

**Local Setup**:
1. Create a Kaggle API key from your Kaggle account settings
2. Store key in `config.py` or as environment variables

**Execution**:
```bash
# Navigate to pipeline directory
cd dlt_pipelines

# Install dependencies
pip install -r requirements.txt

# Run the ingestion pipeline
python kaggle_covid_pipeline.py
```

**Success Indicators**: Raw COVID-19 data files will appear in your GCS bronze layer bucket. Verify their existence using the GCP console or `gsutil ls` command.

#### 3. Workflow Orchestration with Kestra
**Purpose**: Schedule and monitor pipeline execution, ensuring all steps run reliably and in the correct sequence.

**Key Files**:
- `kestra/pipelines/covid_pipeline.yaml`: Defines workflow steps and dependencies
- `kestra/config/application.yml`: Sets Kestra server configuration
- `kestra/scripts/start_kestra.bat`: Windows startup script

**Local Setup**:
1. Ensure Java 11+ is installed
2. Configure `application.yml` with appropriate storage settings

**Execution**:
```bash
# For Windows users
cd kestra\scripts
start_kestra.bat

# Access Kestra UI
# Open http://localhost:8080 in your browser
```

**Success Indicators**: The Kestra UI will show your pipeline with green status indicators when runs complete successfully. You can monitor task execution times and logs from the interface.

#### 4. Data Transformation with dbt
**Purpose**: Transform raw data into analytics-ready datasets using the medallion architecture pattern.

**Key Files**:
- `dbt/profiles.yml`: Connects to BigQuery
- `dbt/models/bronze/sources.yml`: Maps to raw data
- `dbt/models/silver/covid_cleaned.sql`: Standardizes and cleans data
- `dbt/models/gold/covid_daily_metrics.sql`: Creates aggregated metrics

**Local Setup**:
1. Install dbt (`pip install dbt-bigquery`)
2. Configure `profiles.yml` with your BigQuery credentials

**Execution**:
```bash
# Navigate to dbt directory
cd dbt

# Install dependencies
dbt deps

# Run all models
dbt build

# Test data quality
dbt test
```

**Success Indicators**: The command output will show successful model creation. You'll see new tables in BigQuery with transformed data following our medallion structure.

#### 5. Data Visualization with Looker Studio
**Purpose**: Create interactive dashboards that enable stakeholders to explore data and derive insights.

**Key Files**:
- `dashboard/covid_spread_dashboard.json`: Geographic spread visualization
- `dashboard/vaccination_metrics_dashboard.json`: Vaccination effectiveness metrics

**Local Setup**:
No specific local setup required - Looker Studio is web-based.

**Execution**:
1. Navigate to [Looker Studio](https://lookerstudio.google.com/)
2. Create a new data source connected to your BigQuery gold layer tables
3. Import dashboard configurations or build custom visualizations
4. Share dashboard links with stakeholders

**Success Indicators**: Interactive dashboards showing COVID-19 trends, regional patterns, and vaccination metrics are accessible to stakeholders, completing the data-to-insights journey.

### End-to-End Pipeline Flow

This pipeline takes raw COVID-19 data from Kaggle through a complete lifecycle:
1. **Infrastructure** (Terraform): Creates the environment
2. **Ingestion** (DLT): Extracts and loads raw data into the bronze layer
3. **Orchestration** (Kestra): Ensures reliable execution
4. **Transformation** (dbt): Cleans and structures data through silver to gold layers
5. **Visualization** (Looker): Presents insights for decision-making

Following this guide will create a production-ready data pipeline that transforms pandemic data into actionable healthcare insights.


//////////////////////////////////////////////////////
# COVID-19 Data Pipeline Implementation Guide

This guide walks you through building a complete data pipeline for COVID-19 analysis using modern data engineering tools. Each section explains not only the technical steps but also why they're important and how they connect to create a comprehensive analytics solution.

## Prerequisites

Before starting, ensure you have:

- [Git Bash](https://gitforwindows.org/) (for Windows users)
- [Python 3.8+](https://www.python.org/downloads/)
- [Terraform](https://www.terraform.io/downloads) (v1.0+)
- [dbt](https://docs.getdbt.com/dbt-cli/installation)
- A Google Cloud Platform account with billing enabled
- Kaggle account and API key

## Pipeline Overview

This implementation follows the medallion architecture:
1. **Extract**: Pull COVID-19 data from Kaggle using DLT
2. **Load**: Store raw data in GCS (bronze layer)
3. **Transform**: Process data through dbt into silver (cleaned) and gold (aggregated) layers
4. **Visualize**: Create dashboards in Looker to analyze the processed data

Each step builds on the previous one, creating a robust end-to-end analytics platform.

## Detailed Implementation Steps

### 1. Infrastructure Setup with Terraform

**Why this matters**: Infrastructure-as-Code ensures consistent, reproducible environments and prevents configuration drift. This step creates all the cloud resources we'll need for the pipeline.

#### Key Files:
- `terraform/main.tf`: Defines the GCP project and region
- `terraform/storage.tf`: Creates GCS buckets for our bronze layer data
- `terraform/bigquery.tf`: Sets up datasets that will hold our silver and gold layer data
- `terraform/service-accounts.tf`: Establishes proper security permissions

#### Steps:
```bash
# Navigate to terraform directory
cd terraform

# Initialize Terraform (downloads providers and sets up backend)
terraform init

# Preview changes before applying
terraform plan

# Create infrastructure (you'll need to confirm with 'yes')
terraform apply
```

**What to expect**: After successful completion, you'll see output variables with GCS bucket names and BigQuery dataset IDs that will be used in subsequent steps. Make note of these values.

### 2. Data Ingestion with DLT (Data Loading Tool)

**Why this matters**: We need a reliable way to extract data from Kaggle and load it into our data lake with consistent schema enforcement. DLT handles this while maintaining data lineage.

#### Key Files:
- `dlt_pipelines/config.py`: Stores your Kaggle API key and GCS destination details
- `dlt_pipelines/kaggle_covid_pipeline.py`: Defines extraction logic and loads to GCS
- `dlt_pipelines/schema_mapping.py`: Ensures data quality by enforcing schemas

#### Steps:
```bash
# Navigate to DLT directory
cd dlt_pipelines

# Install required Python packages
pip install -r requirements.txt

# IMPORTANT: Edit config.py to add your Kaggle API key before proceeding

# Run the pipeline to extract and load data
python kaggle_covid_pipeline.py
```

**What to expect**: The script will download COVID-19 datasets from Kaggle and upload them to the GCS bucket (bronze layer) created in step 1. The console will show progress and confirm successful completion.

### 3. Workflow Orchestration with Kestra

**Why this matters**: Real data pipelines need scheduling, monitoring, and error handling. Kestra orchestrates our pipeline execution and provides visibility into the process.

#### Key Files:
- `kestra/pipelines/covid_pipeline.yaml`: Defines the workflow that coordinates data movement
- `kestra/config/application.yml`: Configures the Kestra server
- `kestra/scripts/start_kestra.bat`: Simplifies launching Kestra on Windows

#### Steps:
```bash
# Navigate to Kestra scripts directory
cd kestra\scripts

# Start the Kestra server
start_kestra.bat
```

**What to expect**: A browser window will open at http://localhost:8080 with the Kestra UI. Navigate to "Flows" and you should see the covid_pipeline. You can trigger it manually or wait for the scheduled execution.

### 4. Data Transformation with dbt

**Why this matters**: Raw data needs cleaning and business logic applied to be useful for analysis. dbt transforms our bronze data into silver (cleaned) and gold (aggregated metrics) layers.

#### Key Files:
- `dbt/models/bronze/sources.yml`: Connects to our raw data in BigQuery
- `dbt/models/silver/covid_cleaned.sql`: Applies cleaning logic like deduplication
- `dbt/models/gold/covid_daily_metrics.sql`: Creates time-series aggregations
- `dbt/models/gold/covid_regional_analysis.sql`: Provides geographic insights

#### Steps:
```bash
# Navigate to dbt directory
cd dbt

# IMPORTANT: Edit profiles.yml to add your BigQuery connection details

# Install dependencies
dbt deps

# Run all models and tests
dbt build
```

**What to expect**: dbt will connect to BigQuery, process the models in sequence (bronze → silver → gold), and run tests to validate data quality. The console will show each model's execution status.

### 5. Data Visualization with Looker

**Why this matters**: Data insights need to be accessible to stakeholders. Looker dashboards visualize our processed data for easy analysis of COVID-19 trends.

#### Key Files:
- `dashboard/covid_spread_dashboard.json`: Geographic visualization of infection rates
- `dashboard/vaccination_metrics_dashboard.json`: Tracks vaccination effectiveness

#### Steps:
1. Log in to your Looker instance (or set up Looker Studio)
2. Navigate to Connections and create a new BigQuery connection using `dashboard/looker_connection.yml`
3. Import the dashboard JSON files:
   - Go to Dashboards > New > Import
   - Select each dashboard file to import

**What to expect**: After import, you'll have interactive dashboards showing COVID-19 spread patterns and vaccination metrics. These dashboards connect directly to your gold-layer BigQuery tables.

## Troubleshooting Common Issues

- **Terraform permission errors**: Ensure your GCP credentials are properly set up with `gcloud auth application-default login`
- **DLT extraction failures**: Verify your Kaggle API key in `config.py` and check internet connectivity
- **dbt connection issues**: Confirm your BigQuery credentials and project ID in `profiles.yml`

## Extending the Pipeline

This pipeline can be extended by:
1. Adding more data sources to the DLT extraction
2. Creating additional dbt models for different analysis angles
3. Setting up alerts and monitoring in Kestra
4. Implementing CI/CD for the dbt transformations


# DRAFT
### End-to-End Pipeline Flow

This pipeline takes raw COVID-19 data from Kaggle through a complete lifecycle:
1. **Infrastructure** (Terraform): Creates the environment
2. **Ingestion** (DLT): Extracts and loads raw data into the bronze layer
3. **Orchestration** (Kestra): Ensures reliable execution
4. **Transformation** (dbt): Cleans and structures data through silver to gold layers
5. **Visualization** (Looker): Presents insights for decision-making

Following this guide will create a production-ready data pipeline that transforms pandemic data into actionable healthcare insights.


//////////////////////////////////////////////////////
# COVID-19 Data Pipeline Implementation Guide

This guide walks you through building a complete data pipeline for COVID-19 analysis using modern data engineering tools. Each section explains not only the technical steps but also why they're important and how they connect to create a comprehensive analytics solution.

## Prerequisites

Before starting, ensure you have:

- [Git Bash](https://gitforwindows.org/) (for Windows users)
- [Python 3.8+](https://www.python.org/downloads/)
- [Terraform](https://www.terraform.io/downloads) (v1.0+)
- [dbt](https://docs.getdbt.com/dbt-cli/installation)
- A Google Cloud Platform account with billing enabled
- Kaggle account and API key

## Pipeline Overview

This implementation follows the medallion architecture:
1. **Extract**: Pull COVID-19 data from Kaggle using DLT
2. **Load**: Store raw data in GCS (bronze layer)
3. **Transform**: Process data through dbt into silver (cleaned) and gold (aggregated) layers
4. **Visualize**: Create dashboards in Looker to analyze the processed data

Each step builds on the previous one, creating a robust end-to-end analytics platform.

## Detailed Implementation Steps

### 1. Infrastructure Setup with Terraform

**Why this matters**: Infrastructure-as-Code ensures consistent, reproducible environments and prevents configuration drift. This step creates all the cloud resources we'll need for the pipeline.

#### Key Files:
- `terraform/main.tf`: Defines the GCP project and region
- `terraform/storage.tf`: Creates GCS buckets for our bronze layer data
- `terraform/bigquery.tf`: Sets up datasets that will hold our silver and gold layer data
- `terraform/service-accounts.tf`: Establishes proper security permissions

#### Steps:
```bash
# Navigate to terraform directory
cd terraform

# Initialize Terraform (downloads providers and sets up backend)
terraform init

# Preview changes before applying
terraform plan

# Create infrastructure (you'll need to confirm with 'yes')
terraform apply
```

**What to expect**: After successful completion, you'll see output variables with GCS bucket names and BigQuery dataset IDs that will be used in subsequent steps. Make note of these values.

### 2. Data Ingestion with DLT (Data Loading Tool)

**Why this matters**: We need a reliable way to extract data from Kaggle and load it into our data lake with consistent schema enforcement. DLT handles this while maintaining data lineage.

#### Key Files:
- `dlt_pipelines/config.py`: Stores your Kaggle API key and GCS destination details
- `dlt_pipelines/kaggle_covid_pipeline.py`: Defines extraction logic and loads to GCS
- `dlt_pipelines/schema_mapping.py`: Ensures data quality by enforcing schemas

#### Steps:
```bash
# Navigate to DLT directory
cd dlt_pipelines

# Install required Python packages
pip install -r requirements.txt

# IMPORTANT: Edit config.py to add your Kaggle API key before proceeding

# Run the pipeline to extract and load data
python kaggle_covid_pipeline.py
```

**What to expect**: The script will download COVID-19 datasets from Kaggle and upload them to the GCS bucket (bronze layer) created in step 1. The console will show progress and confirm successful completion.

### 3. Workflow Orchestration with Kestra

**Why this matters**: Real data pipelines need scheduling, monitoring, and error handling. Kestra orchestrates our pipeline execution and provides visibility into the process.

#### Key Files:
- `kestra/pipelines/covid_pipeline.yaml`: Defines the workflow that coordinates data movement
- `kestra/config/application.yml`: Configures the Kestra server
- `kestra/scripts/start_kestra.bat`: Simplifies launching Kestra on Windows

#### Steps:
```bash
# Navigate to Kestra scripts directory
cd kestra\scripts

# Start the Kestra server
start_kestra.bat
```

**What to expect**: A browser window will open at http://localhost:8080 with the Kestra UI. Navigate to "Flows" and you should see the covid_pipeline. You can trigger it manually or wait for the scheduled execution.

### 4. Data Transformation with dbt

**Why this matters**: Raw data needs cleaning and business logic applied to be useful for analysis. dbt transforms our bronze data into silver (cleaned) and gold (aggregated metrics) layers.

#### Key Files:
- `dbt/models/bronze/sources.yml`: Connects to our raw data in BigQuery
- `dbt/models/silver/covid_cleaned.sql`: Applies cleaning logic like deduplication
- `dbt/models/gold/covid_daily_metrics.sql`: Creates time-series aggregations
- `dbt/models/gold/covid_regional_analysis.sql`: Provides geographic insights

#### Steps:
```bash
# Navigate to dbt directory
cd dbt

# IMPORTANT: Edit profiles.yml to add your BigQuery connection details

# Install dependencies
dbt deps

# Run all models and tests
dbt build
```

**What to expect**: dbt will connect to BigQuery, process the models in sequence (bronze → silver → gold), and run tests to validate data quality. The console will show each model's execution status.

### 5. Data Visualization with Looker

**Why this matters**: Data insights need to be accessible to stakeholders. Looker dashboards visualize our processed data for easy analysis of COVID-19 trends.

#### Key Files:
- `dashboard/covid_spread_dashboard.json`: Geographic visualization of infection rates
- `dashboard/vaccination_metrics_dashboard.json`: Tracks vaccination effectiveness

#### Steps:
1. Log in to your Looker instance (or set up Looker Studio)
2. Navigate to Connections and create a new BigQuery connection using `dashboard/looker_connection.yml`
3. Import the dashboard JSON files:
   - Go to Dashboards > New > Import
   - Select each dashboard file to import

**What to expect**: After import, you'll have interactive dashboards showing COVID-19 spread patterns and vaccination metrics. These dashboards connect directly to your gold-layer BigQuery tables.

## Troubleshooting Common Issues

- **Terraform permission errors**: Ensure your GCP credentials are properly set up with `gcloud auth application-default login`
- **DLT extraction failures**: Verify your Kaggle API key in `config.py` and check internet connectivity
- **dbt connection issues**: Confirm your BigQuery credentials and project ID in `profiles.yml`

## Extending the Pipeline

This pipeline can be extended by:
1. Adding more data sources to the DLT extraction
2. Creating additional dbt models for different analysis angles
3. Setting up alerts and monitoring in Kestra
4. Implementing CI/CD for the dbt transformations