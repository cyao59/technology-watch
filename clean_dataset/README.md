# Dataset Cleanup Script

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

## License

This script is licensed under the [CYAO License](LICENSE).
