from google.cloud import bigquery
import ruamel.yaml
import os
import sys

def convert_data_type(data_type):
    if data_type == 'INTEGER':
        return 'INT64'
    elif data_type == 'FLOAT':
        return 'FLOAT64'
    else:
        return data_type

def export_bigquery_schema_to_yaml(project_id, dataset_id, output_folder, table_name=None):
    client = bigquery.Client(project=project_id)
 
    # Get a list of tables in the dataset
    dataset_ref = client.dataset(dataset_id)
    if table_name:  # If table_name is provided, only get schema for that table
        tables = [table_name]
    else:  # Otherwise, get schema for all tables in the dataset
        tables = [table.table_id for table in client.list_tables(dataset_ref)]
        
    # Create output folder if it doesn't exist
    # os.makedirs(output_folder, exist_ok=True)

    # Initialize the output structure
    output_structure = {'version': 2, 'models': []}

    for table_id in tables:
        # Construct a full table reference
        table_ref = client.dataset(dataset_id).table(table_id)
        
        # Get the table schema
        table = client.get_table(table_ref)
        schema = table.schema
        
        # Prepare schema for export
        schema_info = []
        for field in schema:
            # Replace field.description with {{ doc("field.name") }}
            description_columns = f'{{{{ doc("{field.name}") }}}}'
            
            tests = [
                # 'not_null',
                {
                    'dbt_expectations.expect_column_values_to_be_of_type': {
                        'column_type': convert_data_type(field.field_type),
                    }
                }
            ]
            
            field_info = {
                'name': field.name,
                # if not column description in BQ take description from doc
                'description': field.description if field.description is not None else description_columns ,
                'tests': tests
            }
        
            schema_info.append(field_info)

        # Add the model structure to the output
        table_description = f'{{{{ doc("{table_id}") }}}}'

        output_structure['models'].append({
            'name': table_id,
            # if not table description in BQ take description from doc
            'description': table.description if table.description is not None else table_description,
            'columns': schema_info
        })

        # Add an empty line after each table schema
        output_structure['models'].append({})

    # Write the output YAML to a file
    output_path = os.path.join(output_folder, 'output_file.yml')
    with open(output_path, 'w') as output_file:
        yaml = ruamel.yaml.YAML()
        yaml.indent(offset=2)
        yaml.dump(output_structure, output_file)

    # Read the generated YAML file
    with open(output_path, 'r') as file:
        yaml_content = file.read()

   
    replace_dict = {
        # Replace '- {}' with an empty line and adjust the indentation
        # yaml_content = yaml_content.replace('- {}', '')
        '- {}': '',
        # Adjust the indentation
        '    - name:': '      - name:',
        '  description:': '    description:',
        '  columns:': '    columns:',
        '      description:': '        description:',
        '    tests:': '        tests:',
        '      - not_null': '          - not_null',
        '      - dbt_expectations.expect_column_values_to_be_of_type': '          - dbt_expectations.expect_column_values_to_be_of_type',
        '        column_type:': '              column_type:'
    }

    for old_str, new_str in replace_dict.items():
        yaml_content = yaml_content.replace(old_str, new_str)
    
    # Write the modified content back to the file
    with open(output_path, 'w') as file:
        file.write(yaml_content)

if __name__ == "__main__":
    # Use command-line arguments for project_id, dataset_id, and output_folder
    if len(sys.argv) < 3:
        print("Usage: python script.py <project_id> <dataset_id>")
        sys.exit(1)

    project_id = sys.argv[1]
    dataset_id = sys.argv[2]
    # Set output_folder to the current working directory
    output_folder = os.getcwd()

    # Replace with the desired output YAML file
    output_yaml = 'output_file.yml'

    # Check if the optional argument table_name is provided
    table_name = sys.argv[3] if len(sys.argv) > 3 else None

    export_bigquery_schema_to_yaml(project_id, dataset_id, output_folder, table_name)