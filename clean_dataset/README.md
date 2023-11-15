# Script 1 : Dataset Cleanup Script

This script is designed to remove all tables from a specified dataset in BigQuery.

## Prerequisites

- Ensure that you have the `bq` command-line tool installed.
- Make sure you have the necessary permissions to delete tables in the specified dataset.

## Usage

1. Open the `file.sh` script in a text editor.

2. Set the values for `project_id` and `dataset_id` in the script:

    ```bash
    # Set value for project_id and dataset_id
    echo "Set value for project_id and dataset_id."
    project_id=''
    dataset_id=''
    ```

3. Save the script.

4. Open a terminal and navigate to the directory containing the script.

5. Make the script executable:

    ```bash
    chmod +x file.sh
    ```

6. Run the script:

    ```bash
    ./file.sh
    ```

## Script Overview

- **Set Project and Dataset:**
  - Sets values for `project_id` and `dataset_id`.

- **List Tables in Dataset:**
  - Retrieves a list of tables from the specified dataset.

- **Check if Dataset Contains Tables:**
  - Checks if the dataset contains any tables.

- **Remove Tables from Dataset:**
  - Loops through each table and removes it from the dataset.

- **Completion Message:**
  - Prints a message indicating the successful completion of the script.

## Notes

- Ensure that the variable `$project_id` and  `$dataset_id` are replaced in the loop.

- Review the script output for any errors or unexpected behavior.

- Adjust permissions and installations as needed.


# Script 2: BigQuery Dataset Sizes Retrieval Script

## Overview

This Python script leverages the Google Cloud BigQuery API to retrieve dataset sizes within a specified project. The obtained dataset sizes are then saved to a CSV file with a pipe ('|') as the delimiter.

## Prerequisites

1. **Google Cloud Project:**
   - Ensure you have a Google Cloud project with the necessary permissions to access BigQuery.

2. **Google Cloud SDK:**
   - Install the Google Cloud SDK to authenticate and authorize access to the BigQuery API.

3. **Python Libraries:**
   - Install the required Python libraries using the following:
     ```bash
     pip install google-cloud-bigquery
     ```

## Script Structure

The script is organized into three main functions:

### 1. `get_dataset_sizes(project_id)`

- **Input:**
  - `project_id`: The Google Cloud project ID containing BigQuery datasets.

- **Output:**
  - Returns a dictionary (`dataset_sizes`) mapping dataset IDs to their sizes in gigabytes.

### 2. `save_to_csv(dataset_sizes, csv_filename='dataset_sizes.csv')`

- **Input:**
  - `dataset_sizes`: Dictionary obtained from `get_dataset_sizes`.
  - `csv_filename`: Name of the CSV file to create (default: 'dataset_sizes.csv').

- **Output:**
  - Saves dataset sizes to a CSV file using a pipe ('|') as the delimiter.

### 3. `main()`

- **Usage:**
  - Replace 'your-project-id' with your Google Cloud project ID.
  - Executes the main functionality of the script.

## Execution

1. Replace `'your-project-id'` in the `main()` function with your actual Google Cloud project ID.

2. Run the script using the following command:
   ```bash
   python get_dataset_sizes.py

## License

This script is licensed under the [CYAO License](LICENSE).
