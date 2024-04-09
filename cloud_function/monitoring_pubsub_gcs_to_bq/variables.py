author__       = "Cedric YAO"
__copyright__  = "Copyright 2023."
__license__    = "Propriétaire"
__version__    = "1.0.0"
__maintainer__ = "DataTeam"

from google.cloud import bigquery
from google.cloud import storage

project_id     = 'sandbox-cyao'
source_dataset = 'test'
table_name     = 'ORDER_SELL_THROUGH_MARKETS'

client_cloudStorage = storage.Client(project_id)
client_bigquery     = bigquery.Client(project_id)

destination_dataset = 'data_quality'
destination_table   = 'monitoring'

sql_folder_path= "/home/jupyter/"

#bucket_path ='gs://data_quality_bucket_cyao'
bucket_name = 'data_quality_bucket_cyao'

schema       = [
                  bigquery.SchemaField("indicator_id", "STRING"), #, mode="REQUIRED"),
                  bigquery.SchemaField("indicator_description", "STRING"),
                  bigquery.SchemaField("country_code", "STRING"),
                  bigquery.SchemaField("dataset", "STRING"),
                  bigquery.SchemaField("table_name", "STRING"),
                  bigquery.SchemaField("results", "STRING"),
                  bigquery.SchemaField("status", "STRING"),
                  bigquery.SchemaField("evaluation_criteria", "STRING"),
                  bigquery.SchemaField("execution_date", "DATE")
                  ]

#table_monitoring    = f'{project_id}.{destination_dataset}.{destination_table}'
table_monitoring = 'sandbox-cyao.data_quality.monitoring'
