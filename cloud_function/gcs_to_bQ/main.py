from google.cloud import bigquery
from google.cloud import storage
from google.api_core import retry

import pandas as pd

# Define the BigQuery project id
project_id = 'sandbox-cyao'

# Initialize client for BigQuery
bq_client = bigquery.Client(project=project_id)

# Define the BigQuery dataset name
dataset_name = 'test'
dataset_ref = bq_client.dataset(dataset_name)

# Define the job configuration
job_config = bigquery.LoadJobConfig(
    autodetect=False,  # Disable autodetection to use the first row as column names
    source_format=bigquery.SourceFormat.CSV,
    create_disposition=bigquery.CreateDisposition.CREATE_IF_NEEDED,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    skip_leading_rows=1,  # Skip the first row while loading data
)

def gcs_to_bq(data, context):
    # Retrieve the bucket and file information from the trigger event
    bucket_name = data['bucket']
    print(f'{bucket_name}')
    file_name = data['name']

    print(f'{file_name}')
    gsutil_uri_path = f'gs://{bucket_name}/{file_name}'
    print(f'Cloud Storage path: {gsutil_uri_path}')


    # Load the Excel file into a Pandas DataFrame
    # df = pd.read_excel(gsutil_uri_path, engine='openpyxl')
    df = pd.read_csv(gsutil_uri_path, delimiter=',')
    column_names = df.columns.tolist()

    table_name = file_name.split(".")[0]

    print(f'{table_name }')
    table_id = f'{project_id}.{dataset_name}.{table_name}'

    # Create the table reference
    table_ref = dataset_ref.table(table_name)
    #table = bigquery.Table(table_ref)

    # Check if the table exists
    try:
        bq_client.get_table(table_ref)
        table_exists = True
    except Exception as e:
        table_exists = False

    # Delete the existing table if it exists
    if table_exists:
        bq_client.delete_table(table_ref)
        print(f'Table {table_name} in dataset {dataset_name} deleted successfully.')
    else:
        print(f'Table {table_name} in dataset {dataset_name} does not exist.')

    # Construct the SQL statement to drop the table
    #sql = f"DROP TABLE `{project_id}.{dataset_name}.{table_name}` "

    # Execute the SQL statement
    #query_job = bq_client.query(sql)
    #query_job.result()  # Wait for the job to complete

    #print(f'Table {table_name} in dataset {dataset_name} droped successfully.')

    # Create the table in BigQuery with the desired schema
    schema = []
    for col in column_names:
        # Determine the data type based on the values in the column
        column_data = df[col]
        if column_data.dtype == 'int64':
            schema.append(bigquery.SchemaField(col, "INTEGER"))
        elif column_data.dtype == 'float64':
            schema.append(bigquery.SchemaField(col, "FLOAT"))
        elif column_data.dtype == 'bool':
            schema.append(bigquery.SchemaField(col, "BOOLEAN"))
        elif column_data.dtype == 'datetime64[ns]':
            schema.append(bigquery.SchemaField(col, "TIMESTAMP"))
        elif column_data.dtype == 'object':
            schema.append(bigquery.SchemaField(col, "STRING"))
        elif column_data.dtype == 'timedelta64[ns]':
            schema.append(bigquery.SchemaField(col, "TIME"))
        elif column_data.dtype == 'datetime64[ns]':
            schema.append(bigquery.SchemaField(col, "DATETIME"))
        elif column_data.dtype == 'date':
            schema.append(bigquery.SchemaField(col, "DATE"))
        elif column_data.dtype == 'list':
            # Specify the element type of the array, e.g., STRING, INTEGER, FLOAT
            element_type = "STRING"
            schema.append(bigquery.SchemaField(col, "ARRAY", mode="REPEATED", fields=[bigquery.SchemaField("element", element_type)]))
        elif column_data.dtype == 'Int64' or column_data.dtype == 'Int32':
            schema.append(bigquery.SchemaField(col, "NUMERIC"))
        else:
            # Add logic for other data types as needed
            schema.append(bigquery.SchemaField(col, "STRING"))

    table = bigquery.Table(table_ref, schema=schema)

    # Create the table in BigQuery
    bq_client.create_table(table)

    # Load the DataFrame into the table
    job = bq_client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()  # Wait for the job to complete.

    print(f'Excel file {file_name} uploaded to BigQuery table {table_id}')
