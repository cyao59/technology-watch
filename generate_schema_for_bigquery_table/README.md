__author__       = "Cedric YAO"
__copyright__  = "Copyright 2023"
__version__    = "1.0.0"
__maintainer__ = "Cedric YAO"

# BigQuery Schema Exporter

This script exports the schema of BigQuery tables to a YAML file following the dbt (data build tool) model structure. The generated YAML file can be used as part of a dbt project for testing and documentation purposes.

## Prerequisites
- Python 3
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

## Installation
1. Install the required Python packages:
    ```bash
    pip install google-cloud-bigquery ruamel.yaml
    ```

2. Authenticate the Google Cloud SDK:
    ```bash
    gcloud auth application-default login
    ```

## Usage
Run the script with the following command:

```bash
python script.py <project_id> <dataset_id> [table_name]
```

- **`<project_id>`** : Your Google Cloud project ID.
- **`<dataset_id>`** : The BigQuery dataset ID.
- **`<output_folder>`** : The folder where the generated YAML files will be saved.
- **`<[table_name]>`** (optional) : If provided, it exports the schema for the specified table. If not provided, it exports the schema for all tables in the dataset.

## Example
Export schema for a specific table:

```bash
python script.py my-project my-dataset my-table
```

Export schema for all tables in a dataset:

```bash
python script.py my-project my-dataset 
```

# Generated Output

The script generates YAML files for each table in the specified output folder. The structure follows the dbt model structure, including the 
**`name`**, **`description`**, and **`columns`** attributes with associated metadata and tests.

**`Note`**: Empty lines are added between the schema of each table for better readability.

# Output Modification

After running the script, you can read the generated YAML file and modify the content if needed. The script automatically removes lines containing **`'- {}'`** to replace them with empty lines for improved formatting.

# Modify Output

```bash
python script.py my-project my-dataset 
```

# License
This project is licensed under the MIT License - see the  [LICENSE](dwh-pnl-by-channel/) file for details.

```css
Feel free to use and customize this README content for your project.
```