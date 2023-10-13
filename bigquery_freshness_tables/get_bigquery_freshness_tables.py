import argparse
from google.cloud import bigquery
from datetime import datetime, timedelta, date
import csv

def get_table_creation_time(client, dataset_id, table_id):
    # Retrieving table metadata
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)

    # Returns the table creation date
    return table.created

def get_last_modified_time(client, dataset_id, table_id):
    # Retrieving table metadata
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)

    # Returns the table last modified date
    return table.modified

def main(project_id):
    # Initializing the BigQuery client
    client = bigquery.Client(project=project_id)

    # Retrieving the list of datasets in the project
    datasets = client.list_datasets()

    # CSV file name
    csv_filename = 'non_refreshed_tables_results.csv'

    # Get the current date
    now = date.today()

    # Opening the CSV file in write mode
    with open(csv_filename, 'w', newline='') as csv_file:
        # Creating a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Writing the header to the CSV file
        csv_writer.writerow(['Dataset', 'Table', 'Creation_Time', 'Last_Modified_Time', 'Last_Refresh > 60 Days'])

        # Looping through all datasets in the project
        for dataset in datasets:
            dataset_id = dataset.dataset_id

            # Retrieving the list of tables in the dataset
            tables = client.list_tables(dataset_id)

            # Checking the creation date of each table
            for table in tables:
                creation_time = get_table_creation_time(client, dataset_id, table.table_id)
                last_modified_time = get_last_modified_time(client, dataset_id, table.table_id)

                if last_modified_time is not None:
                    # Writing the result to the CSV file
                    csv_writer.writerow([dataset_id, table.table_id, creation_time, last_modified_time, last_modified_time.date() < (now - timedelta(days=60))])

    print(f"Results saved to CSV file: {csv_filename}")

if __name__ == '__main__':
    # Configuring the argument parser
    parser = argparse.ArgumentParser(description='Script to check non-refreshed tables in BigQuery.')
    parser.add_argument('--project_id', required=True, help='BigQuery project ID')

    # Parsing the arguments
    args = parser.parse_args()

    # Calling the main function with the project_id passed as an argument
    main(args.project_id)