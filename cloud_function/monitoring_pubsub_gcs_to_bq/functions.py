author__       = "Cedric YAO"
__copyright__  = "Copyright 2023."
__license__    = "Propriétaire"
__version__    = "1.0.0"
__maintainer__ = "DataTeam"

# Import Librairy
from google.cloud import bigquery
from google.cloud import storage
import datetime
import yaml
import os
import re

# Import variables
from variables import project_id, source_dataset, table_name, destination_table, destination_dataset, table_monitoring,schema
from variables import client_cloudStorage, client_bigquery

################################### List_of_queries_from_sqlFiles  ###########################
def list_of_queries_from_sqlFiles(sql_folder_path) :
    sql_queries=[]
    for sql_filename in os.listdir(sql_folder_path):
        # Check if fil has sql extension
        if sql_filename.endswith(".sql"):
            sql_file_path = os.path.join(sql_folder_path,sql_filename)
            #print(sql_file_path)
            with open(sql_file_path,'r') as file :
                query_string = file.read()
                #print(type(query_string))
                query_string = query_string.format(project_id = project_id, source_dataset=source_dataset,table_name=table_name)
                #print(type(query_string))
                # Split the file content by SQL query separator
                queries  = re.split(r'/*.*/', query_string)
                print(queries)
                # Remove Empty argument from List
                queries  = list(filter(None,queries))
                print(queries)
                # Replace all \n
                for i in range (len(queries)):
                    queries[i]  = queries[i].replace('\n',' ')
                    queries[i]  = queries[i].replace('Â\xa0',' ')
                    print(queries)
                    sql_queries.append(queries)
    return sql_queries

########## Show list of queries from sql file on cloud_storage directory with function ############
def list_of_sqlQueries_from_bucket(bucket_name):
    sql_queries=[]
    # Get all the buckets in the project
    buckets = client_cloudStorage.list_buckets()
    # Print the name of each bucket
    for bucket in buckets:
        bucket_name=bucket.name
        #print(bucket_name)
        if bucket_name == 'data_quality_bucket_cyao' :
            # List the blobs (files) in the bucket
            bucket = client_cloudStorage.get_bucket(bucket_name)
            blobs = bucket.list_blobs()
            # Print the name of each blob
            for blob in blobs:
                if blob.name.endswith(".sql"):
                    # Download the contents of the blob
                    contents = blob.download_as_string()
                    # Decode the contents to a string
                    content_str = contents.decode('utf-8')
                    #Replace variable in queries by real value
                    query_string = content_str.format(project_id = project_id, source_dataset=source_dataset,table_name=table_name)
                    # Split the file content by SQL query separator
                    queries  = re.split(r'/*.*/', query_string)
                    # comments = re.split(r"/\*.*?\/", query_string)
                    # Remove Empty argument from List
                    queries  = list(filter(None,queries))
                    # comments = list(filter(None,comments))
                    # Replace all \n
                    for i in range (len(queries)):
                        queries[i]  = queries[i].replace('\n',' ')
                        queries[i]  = queries[i].replace('\xa0',' ')
                        # comments[i] = comments[i].replace('/*','')
                        # comments[i] = comments[i].replace('*/','')
                    sql_queries.append(queries)
    return sql_queries

######################### create_newTable_ifNotExist ###########################
def create_newTable_ifNotExist(table_id):
    try:
        # Check if table exists
        table = client_bigquery.get_table(table_id)
        print(f"Table {table} already exists.")

    except :
        # Create table if it not exist
        table = bigquery.Table(table_id, schema=schema)
        table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY, field='execution_date')
        table = client_bigquery.create_table(table)

        print(f"Exception : Table {table.table_id} created with success.")

    return print(f"Check on {table} done !")

#################### insert_data_to_monitoringTable##########################
def insert_data_to_monitoringTable(list_queries):

    # Get the destination table
    dataset_ref = client_bigquery.dataset(destination_dataset)
    table_ref   = dataset_ref.table(destination_table)
    destination_dataset_table = client_bigquery.get_table(table_ref)

    # Get the execution date
    execution_date = datetime.datetime.today().strftime('%Y-%m-%d')

    # Delete the partition of the execution date
    query_truncate_current_partition = f"DELETE FROM `{destination_dataset_table}` WHERE execution_date = '{execution_date}'"

    query_job_current_job = client_bigquery.query(query_truncate_current_partition)
    print(f"Remove data for partition of the running day : {query_truncate_current_partition}.")

    for list_of_query in list_queries :

        for query in list_of_query :
            print(query)  # Move the print statement outside of the nested loop
            try :
                # Insert the query results into the table
                job_config = bigquery.QueryJobConfig(destination=destination_dataset_table,write_disposition='WRITE_APPEND',
                                                     time_partitioning=bigquery.TimePartitioning(
                                                     type_=bigquery.TimePartitioningType.DAY,
                                                     field= "execution_date",
                                                     require_partition_filter=True)
                                                    )
                # Execute the query and insert the results into the destination table
                query_job = client_bigquery.query(query, job_config=job_config)

                # Wait for the load job to complete
                query_result = query_job.result()

            except Exception as error :
                    print("An error has occurred :", error)

    return  print(f"End of insertion in table `{destination_dataset_table}` !")
