import base64
from google.cloud import bigquery

def copy_tables_from_dataset (event, context):
    # Décoder le message Pub/Sub
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')

    # Remplacez ces valeurs par les vôtres
    source_project = "	sandbox-cyao"
    source_dataset = "test"

    destination_project = "	sandbox-cyao"
    destination_dataset = "toto"

    # Initialisez le client BigQuery
    client = bigquery.Client('sandbox-cyao')

    # Liste toutes les tables dans l'ensemble de données source
    source_dataset_ref = client.dataset(source_dataset)
    source_tables = [table.table_id for table in client.list_tables(source_dataset_ref)]

    # Itération sur toutes les tables et les copier dans l'ensemble de données destination
    for source_table in source_tables:
        # Construisez les références de table source et destination
        source_table_ref = source_dataset_ref.table(source_table)
        destination_table_ref = client.dataset(destination_dataset).table(source_table)

        # Effectuez la copie
        job_config = bigquery.CopyJobConfig()
        job = client.copy_table(source_table_ref, destination_table_ref, job_config=job_config)

        # Attendez la fin de la tâche
        job.result()

    print(f"Copie de toutes les tables terminée avec succès! Message Pub/Sub : {pubsub_message}")
