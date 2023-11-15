import csv
from google.cloud import bigquery

def get_dataset_sizes(project_id):
    # Initializing the BigQuery client
    client = bigquery.Client(project=project_id)

    # Retrieving the list of datasets in the project
    datasets = client.list_datasets()

    # Dictionary to store the sizes of datasets
    dataset_sizes = {}

    # Looping through all datasets in the project
    for dataset in datasets:
        dataset_id = dataset.dataset_id

        # Retrieving the size of the dataset using a SQL query
        dataset_ref = client.dataset(dataset_id)
        dataset_size_query = f"SELECT ROUND(SAFE_DIVIDE(SUM(size_bytes),power(1024 , 3)),2) as total_size FROM `{project_id}.{dataset_id}.__TABLES__`"
        query_job = client.query(dataset_size_query)
        size_bytes = list(query_job)[0]['total_size']

        # Adding the dataset size to the dictionary
        dataset_sizes[dataset_id] = size_bytes

    return dataset_sizes

def save_to_csv(dataset_sizes, csv_filename='dataset_sizes.csv'):
    # Writing the results to a CSV file
    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter='|')
        
        # Writing the header
        csv_writer.writerow(['Dataset', 'Size(GB)'])
        
        # Writing the dataset sizes
        for dataset_id, size_bytes in dataset_sizes.items():
            csv_writer.writerow([dataset_id, size_bytes])

def main():
    # Replace 'your-project-id' with your actual BigQuery project ID
    project_id = 'your-project-id'

    dataset_sizes = get_dataset_sizes(project_id)

    # Save the dataset sizes to a CSV file
    save_to_csv(dataset_sizes)

    print(f"Dataset sizes saved to CSV file: dataset_sizes.csv")

if __name__ == "__main__":
    main()