# Table Checker for Non-Refreshed BigQuery Tables

## Overview

This Python script is designed to check for non-refreshed tables in a BigQuery project. It utilizes the Google Cloud BigQuery Python client library and exports the results to a CSV file. The script identifies tables that haven't been modified in the last 60 days.

## Prerequisites

- Python (3.6 or higher)
- Google Cloud SDK installed and configured
- Required Python packages installed (`google-cloud-bigquery`, `argparse`)

## Installation

1. Install the required Python packages:

    ```bash
    pip install google-cloud-bigquery argparse
    ```

2. Configure the Google Cloud SDK:

    ```bash
    gcloud auth login
    ```

## Usage

```bash
python script_name.py --project_id YOUR_PROJECT_ID
```

## Functionality

1. **Retrieve Metadata:**
   - Utilizes the BigQuery Python client to retrieve metadata (creation and modification times) for each table in each dataset.

2. **Check for Non-Refreshed Tables:**
   - Compares the last modification time with the current date and identifies tables that haven't been modified in the last 60 days.

3. **Export Results:**
   - Writes the results (dataset name, table name, creation time, last modified time, and a boolean indicating whether the table has been modified in the last 60 days) to a CSV file named `resultats_tables_non_refreshed.csv`.

## Usage Example

```bash
python script_name.py --project_id my-bigquery-project
```