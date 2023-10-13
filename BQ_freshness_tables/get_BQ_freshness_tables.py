import argparse
from google.cloud import bigquery
from datetime import datetime, timedelta, date
import csv

def get_table_creation_time(client, dataset_id, table_id):
    # Récupération des métadonnées de la table
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)

    # Retourne la date de création de la table
    return table.created

def get_last_modified_time(client, dataset_id, table_id):
    # Récupération des métadonnées de la table
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)

    # Retourne la date de création de la table
    return table.modified

# # Fonction not good for the moment
# def get_last_modified_time(client, dataset_id, table_id):
#     # Récupération de la date de modification de la table depuis INFORMATION_SCHEMA
#     query = f"""
#     SELECT last_modified_time
#     FROM `{client.project}.{dataset_id}.__TABLES__`
#     WHERE table_id = '{table_id}'
#     """
#     query_job = client.query(query)
#     result = query_job.result()

#     for row in result:
#         last_modified_microseconds = row.last_modified_time
#         # Convertir les microsecondes en objet date
#         last_modified_time = datetime.utcfromtimestamp(last_modified_microseconds / 1e6)
#         return last_modified_time

#     # Si la table n'a pas de date de modification, retourner None
#     return None

def main(project_id):
    # Initialisation du client BigQuery
    client = bigquery.Client(project=project_id)

    # Récupération de la liste des datasets dans le projet
    datasets = client.list_datasets()

    # Nom du fichier CSV
    csv_filename = 'resultats_tables_non_refreshed.csv'

    # Obtenez la date actuelle
    maintenant = date.today()

    # Ouverture du fichier CSV en mode écriture
    with open(csv_filename, 'w', newline='') as csv_file:
        # Création d'un objet writer CSV
        csv_writer = csv.writer(csv_file)

        # Écriture de l'en-tête dans le fichier CSV
        csv_writer.writerow(['Dataset', 'Table', 'Creation_Time', 'Last_Modified_Time', 'Last_Refresh > 60 Days'])

        # Boucle sur tous les datasets du projet
        for dataset in datasets:
            dataset_id = dataset.dataset_id

            # Récupération de la liste des tables dans le dataset
            tables = client.list_tables(dataset_id)

            # Vérification de la date de création de chaque table
            for table in tables:
                creation_time = get_table_creation_time(client, dataset_id, table.table_id)
                last_modified_time = get_last_modified_time(client, dataset_id, table.table_id)

                if last_modified_time is not None:
                    # Écriture du résultat dans le fichier CSV
                    csv_writer.writerow([dataset_id, table.table_id, creation_time, last_modified_time, last_modified_time.date() < (maintenant - timedelta(days=60))])

    print(f"Résultats enregistrés dans le fichier CSV : {csv_filename}")

if __name__ == '__main__':
    # Configuration de l'analyseur d'arguments
    parser = argparse.ArgumentParser(description='Script pour vérifier les tables non rafraîchies dans BigQuery.')
    parser.add_argument('--project_id', required=True, help='ID du projet BigQuery')

    # Analyse des arguments
    args = parser.parse_args()

    # Appel de la fonction principale avec le project_id passé en argument
    main(args.project_id)