from setuptools import find_packages, setup

setup(
    name="dagster_healthcare_pipeline",
    packages=find_packages(exclude=["dagster_healthcare_pipeline_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-dbt",
        "dagster-gcp",
        "pandas",
        "kaggle",
        "dlt[bigquery]",
        "google-cloud-storage",
        "gcsfs",
        "google-cloud-bigquery",
        "google-cloud-bigquery-storage",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)