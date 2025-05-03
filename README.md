# COVIDEpidemetrics Healthcare Pipeline

## Data Engineering ZoomCamp 2025 Final Project
### Overview
This project implements an end-to-end data pipeline processing COVID-19 data from Kaggle. The pipeline follows a batch processing approach, ingesting data into a data lake on GCP, transforming it using dbt with a medallion architecture, and visualizing insights through Looker dashboards.

### Problem Statement
The COVID-19 pandemic created unprecedented challenges for healthcare systems worldwide. As coronavirus infections spread, healthcare providers faced critical shortages of medical resources and struggled with efficient distribution of limited supplies. Massive volumes of patient data were generated daily in inconsistent formats, making it difficult to derive actionable insights. Healthcare professionals need reliable analytics to identify high-risk patients early, predict resource requirements, and allocate medical attention where it's most urgently needed. Without structured data processing systems, potentially life-saving patterns remain hidden in the data.

### Vision and Impact
This data pipeline aims to create a foundation for pandemic preparedness and response. By transforming raw COVID-19 data into structured, analytics-ready formats, the pipeline enables powerful downstream applications. Machine learning models can then be trained on this processed data to predict patient outcomes, forecast resource needs, and identify high-risk populations. These predictive capabilities will be crucial for healthcare systems to quickly identify and establish an underlying pattern, resulting in more effective respones to future pandemics and allowing for earlier interventions, better resource allocation, and ultimately, improved patient outcomes. The pipeline's scalable architecture ensures that as new data sources become available, they can be incorporated to continuously enhance predictive accuracy and broaden analytical insights.

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

*Note: This data dictionary is based on the initial CSV file. The final table structure and content may vary depending on the data transformations and cleaning applied during the pipeline process.*


### Project File Structure
```
de-healthcare-pipeline/
│
├── terraform-iac/                  # Infrastructure as code
│   ├── main.tf
│   └── variables.tf
│
├── dlt-gcp-ingestion/              # Data ingestion components
│   ├── kaggle_dlt_extraction_load.py
│   └── kaggle_dlt_extraction_load.jpynb
│
├── kestra-orchestration/                     # Workflow orchestration
│   ├── flows/
│   │   ├── 00_end_to_end_parent.yaml
│   │   ├── 01_iac_setup.yaml
│   │   ├── 02_data_ingestion.yaml
│   │   ├── 03b_dbt_bq_local.yaml
│   │   └── 04_gcp_scheduled.yaml
│   └── docker-compose.yml
│
├── dbt-gcp-transformations/                        # Data transformation
│   ├── dbt_project.yml
│   └── models/
│       ├── staging/
│       │   ├── schema.yml
│       │   ├── sources.yml
│       │   └── stg_stilver__patients.sql
│       ├── intermediate/
│       │   ├── schema.yml
│       │   └── int__normalized_patients.sql
│       └── marts/
│           ├── dimensions/
│           │   ├── schema.yml
│           │   └── dim_date_sql
│           └── facts/
│               ├── schema.yml
│               ├── fct__comorbidites_outcomes.sql
│               ├── fct__deathes_age_time.sql
│               ├── fct__deaths_recoveries_age.sql
│               └── fct__recoveries_risk_age.sql
│    
└── dashboard/                  # Data visualization
    ├── covid_spread_dashboard.json
    ├── vaccination_metrics_dashboard.json
    └── looker_connection.yml
```

### Technological Components

#### Data Pipeline Architecture
The COVID-19 data pipeline follows a modern data lakehouse approach with a pseudo-medallion architecture (bronze, silver, gold layers) but following the format as "staging", "intermediate", and "marts" respectively. Data is first downloaded from Kaggle as a CSV file and then ingested through dlt into the Google Cloud Storage bucket and then into BigQuery (staging), cleaned and standardized using dbt in BigQuery (intermediate), and then transformed into analytics-ready datasets (marts). The entire workflow is orchestrated by Kestra, with cloud infrastructure managed through Terraform.

#### Pipeline Tech Infrastructure

| Component | Description | Usage | Benefits |
|-----------|-------------|-------|----------|
| **Terraform** | Infrastructure as Code (IaC) tool | Provisioning and managing cloud resources | Ensures reproducible infrastructure setup, version control for infrastructure, and reduced configuration errors |
| **Data Load Tool (DLT)** | Python-based data ingestion framework | Extracting data from Kaggle and loading into GCS | Simplifies data extraction with built-in schema handling and incremental loading capabilities |
| **Google Cloud Platform (GCP)** | Cloud computing platform providing infrastructure and managed services | Hosting all components of our data pipeline | Offers seamless integration between services, scalability, and managed solutions for big data |
| **Google Cloud Storage (GCS)** | Object storage service | Data lake storage (bronze layer) | Scalable, durable storage for raw data files with strong integration to BigQuery |
| **BigQuery** | Serverless, scalable data warehouse | Storing processed data and enabling fast analytics | Handles large-scale data processing with columnar storage and SQL interface |
| **dbt (Data Build Tool)** | Transformation tool following ELT (Extract, Load, Transform) pattern | Implementing medallion architecture and transformations | Enables version-controlled, testable data transformations using SQL |
| **Kestra** | Workflow orchestration platform | Scheduling and monitoring pipeline execution | Provides reliable task scheduling, error handling, and dependency management for data workflows |
| **Dagster** | Data orchestrator for modern data platforms | Orchestrating pipeline execution | Provides modular, Python-native workflows with strong observability and debugging capabilities |
| **Looker Studio** | Business intelligence and data visualization platform | Creating interactive dashboards | Direct integration with BigQuery and powerful visualization capabilities |


https://www.youtube.com/watch?v=Mk81kYNPYf8