# Dagster Orchestration for Healthcare Data Pipeline

This directory contains the Dagster orchestration setup for the healthcare data pipeline. The orchestration is configured to run the Kaggle data extraction and loading process on a schedule.

## Structure

- `dagster_project/`: Python package containing Dagster definitions
  - `assets.py`: Defines the data assets (including the COVID data ingestion asset)
  - `schedules.py`: Defines the schedule for running the data pipeline
  - `__init__.py`: Package initialization
- `workspace.yaml`: Dagster workspace configuration
- `setup.py`: Package setup file
- `requirements.txt`: Dependencies for the project

## Setup

1. Install the required packages:

```bash
pip install -e .
# or
pip install -r requirements.txt
```

2. Start the Dagster UI:

```bash
dagster dev
```

3. Open the UI in your browser (typically at http://localhost:3000)

## What This Does

This Dagster setup orchestrates your COVID data pipeline, which:

1. Downloads the COVID-19 dataset from Kaggle
2. Extracts and processes the data
3. Uploads it to Google Cloud Storage
4. Loads it into BigQuery

The pipeline is scheduled to run daily at 2:00 AM UTC, but you can also trigger it manually from the Dagster UI.

## Modifying the Schedule

To change how often the pipeline runs, edit the `covid_data_schedule` in `schedules.py`. The schedule uses cron syntax:

```python
cron_schedule="0 2 * * *"  # Runs at 2:00 AM daily
```