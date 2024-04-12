from google.cloud import bigquery
import pandas as pd

# Définir les informations d'identification de votre projet
project_id = 'project_id'

# Initialiser le client BigQuery
client = bigquery.Client(project=project_id)

# ID du jeu de données (dataset)
dataset_id = 'dataset_id'

# Liste des noms de tables dont vous voulez extraire les schémas
tables_list = ['table1', 'table2']

# Nom du fichier Excel de sortie
output_excel = 'schema_tables.xlsx'

# Fonction pour extraire le schéma de chaque table et écrire dans une feuille distincte du fichier Excel
def export_table_schemas_to_excel(tables_list, output_excel):
    with pd.ExcelWriter(output_excel) as writer:
        for table_name in tables_list:
            table_ref = client.dataset(dataset_id).table(f'{table_name}')
            table = client.get_table(table_ref)

            # Créer un DataFrame à partir du schéma de la table
            schema_data = []
            for field in table.schema:
                schema_data.append([field.name, field.field_type, field.mode,field.description])
            schema_df = pd.DataFrame(schema_data, columns=['Champ', 'Type', 'Mode', 'Description'])

            # Écrire le DataFrame dans une feuille du fichier Excel
            schema_df.to_excel(writer, sheet_name=table_name, index=False)

# Appeler la fonction pour exporter les schémas dans le fichier Excel avec des feuilles distinctes
export_table_schemas_to_excel(tables_list, output_excel)
