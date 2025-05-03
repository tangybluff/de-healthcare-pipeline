from dagster import ScheduleDefinition, define_asset_job

# Define a job that will run the covid_data_ingestion asset
covid_data_job = define_asset_job(name="covid_data_job", selection="covid_data_ingestion")

# Define a schedule to run the job daily at 2:00 AM
covid_data_schedule = ScheduleDefinition(
    name="covid_data_daily_schedule",
    job=covid_data_job,
    cron_schedule="0 2 * * *",  # Runs at 2:00 AM daily
    execution_timezone="UTC",
)