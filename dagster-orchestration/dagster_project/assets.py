import os
import subprocess
import sys
from pathlib import Path

from dagster import asset, AssetExecutionContext


@asset
def covid_data_ingestion(context: AssetExecutionContext):
    """
    Asset that executes the Kaggle data extraction and loading to BigQuery.
    This asset runs the kaggle_dlt_extract_load.py script which:
    1. Downloads data from Kaggle
    2. Extracts the CSV file
    3. Uploads it to GCS
    4. Loads it into BigQuery
    """
    # Get the path to the kaggle_dlt_extract_load.py script
    project_root = Path(os.getcwd()).parent
    script_path = str(project_root / "dlt-gcp-ingestion" / "kaggle_dlt_extract_load.py")
    
    context.log.info(f"Running script at path: {script_path}")
    
    # Check if script exists
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Script not found at path: {script_path}")
    
    # Add the directories to Python path to ensure imports work correctly
    env = os.environ.copy()
    
    # Execute the script as a subprocess
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=True,
            env=env
        )
        context.log.info("Script output:")
        for line in result.stdout.split("\n"):
            context.log.info(line)
        return "Data successfully loaded to BigQuery"
    except subprocess.CalledProcessError as e:
        context.log.error(f"Error running script: {e}")
        context.log.error(f"Exit code: {e.returncode}")
        
        # Log stderr in a more readable format
        if e.stderr:
            context.log.error("Error output:")
            for line in e.stderr.split("\n"):
                context.log.error(line)
        
        # Also log stdout as it might contain useful information
        if e.stdout:
            context.log.info("Script stdout before error:")
            for line in e.stdout.split("\n"):
                context.log.info(line)
                
        raise Exception(f"Failed to execute kaggle_dlt_extract_load.py: {e}")