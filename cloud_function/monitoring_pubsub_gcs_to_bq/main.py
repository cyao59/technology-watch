import base64
# Import variables
from variables import project_id,table_monitoring, destination_dataset, destination_table
# Import functions
from functions import list_of_sqlQueries_from_bucket, create_newTable_ifNotExist, insert_data_to_monitoringTable

def data_quality_check(event, context):

     """Triggered from a message on a Cloud Pub/Sub topic.
     Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
     """
     pubsub_message = base64.b64decode(event['data']).decode('utf-8')
     print(pubsub_message)

     # Declare variables
     print("Declares variables table_monitoring and bucket_path.")
     #table_monitoring = table_monitoring.format(project_id = project_id, source_dataset=destination_dataset,table_name=destination_table)
     print(f"table_monitoring:{table_monitoring}")

     # From variables import bucket_name
     bucket_name = 'data_quality_bucket_cyao'
     bucket_path =f'gs://{bucket_name}'
     print(f"bucket_path: {bucket_path}")

     # Show list of queries from sqlFiles with function
     list_queries=list_of_sqlQueries_from_bucket(bucket_path)
     print(list_queries)

     # Check if table monitoring exists
     project_dataset_table=create_newTable_ifNotExist(table_monitoring)
     print(project_dataset_table)

     # Call function to insert data inside monitoring table
     final_result = insert_data_to_monitoringTable(list_queries)
     print(final_result)
