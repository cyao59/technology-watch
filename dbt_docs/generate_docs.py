from google.cloud import bigquery
import ruamel.yaml
import os
import sys
import logging  # Added logging module

def convert_data_type(data_type):
    return {'INTEGER': 'INT64', 'FLOAT': 'FLOAT64'}.get(data_type, data_type)

def get_tables(client, dataset_id, table_name=None):
    dataset_ref = client.dataset(dataset_id)
    if table_name:
        return [table_name]
    else:
        return [table.table_id for table in client.list_tables(dataset_ref)]

def get_table_schema(client, dataset_id, table_id):
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)
    return table.schema

def prepare_field_info(field):
    """
    Prepare field information for YAML output.

    Parameters:
    - field: BigQuery field object

    Returns:
    - dict: Prepared field information
    """
    description_columns = f'{{{{ doc("{field.name}") }}}}'
    tests = [
        'not_null',
        {
            'dbt_expectations.expect_column_values_to_be_of_type': {
                'column_type': convert_data_type(field.field_type),
            }
        }
    ]
    return {
        'name': field.name,
        'description': description_columns, #field.description if field.description is not None else description_columns,
        'tests': tests
    }

def prepare_table_info(client, dataset_id, table_id):
    table_description = f'{{{{ doc("{table_id}") }}}}'
    table = client.get_table(client.dataset(dataset_id).table(table_id))
    return {
        'name': table_id,
        'description': table_description, #table.description if table.description is not None else table_description,
        'columns': [prepare_field_info(field) for field in get_table_schema(client, dataset_id, table_id)]
    }

def write_yaml(output_yaml_path, output_structure):
    with open(output_yaml_path, 'w') as output_file:
        yaml = ruamel.yaml.YAML()
        yaml.indent(offset=2)
        yaml.dump(output_structure, output_file)

def generate_table_description(client, dataset_id, table_name):
    descriptions = []
    try:
        tables = get_tables(client, dataset_id, table_name)
        for table_id in tables:
            table_name = f'{table_id}'
            descriptions.append(f'{table_name}')

    except Exception as e:
        logging.error(f"Error generating table description: {e}")
        sys.exit(1)
    return descriptions

def generate_table_description_file(output_folder, tables, client, dataset_id):
    table_desc_path = os.path.join(output_folder, 'tables_description.md')
    with open(table_desc_path, 'w') as table_desc_file:
        table_desc_file.write(f'# Overview\n')
        table_desc_file.write('This document exposes a custom macro to establish standardized and consistent descriptions for tables.\nThis approach streamlines the documentation process, ensuring clarity and uniformity in describing data structures and attributes throughout the project.\n\n')
        table_desc_file.write(f'# Table description \n\n')

        for table_name in tables:
            table_desc_file.write(f'## Description {table_name} table\n')
            table_desc_file.write(f'{{% docs {table_name} %}}\n')
            
            # Get the table description from BigQuery
            table_description = get_table_description(client, dataset_id, table_name)
 
            if table_description is not None:
                table_desc_file.write(f'{table_description}\n')
            else:
                table_desc_file.write(f'. \n')
            
            table_desc_file.write(f'{{% enddocs %}}\n\n')

def generate_columns_description(output_folder, output_structure, client, dataset_id):
    columns_desc_path = os.path.join(output_folder, 'columns_description.md')
    with open(columns_desc_path, 'w') as columns_desc_file:
        columns_desc_file.write(f'# Overview\n')
        columns_desc_file.write('This document exposes a custom macro to establish standardized and consistent descriptions for respective columns from the table and their accepted_valued test.\nThis approach streamlines the documentation process, ensuring clarity and uniformity in describing data structures and attributes throughout the project.\n\n')
        columns_desc_file.write('# Accepted values for columns \n\n')
        columns_desc_file.write('# Columns description \n')

        for table_info in output_structure['models']:
            if 'name' not in table_info or 'columns' not in table_info:
                logging.warning(f"Warning: 'name' or 'columns' not found in {table_info}")
                continue
            
            table_name = table_info['name']
            columns_info = table_info['columns']

            if columns_info:
                columns_desc_file.write(f'\n## Columns of {table_name} table\n')
                for column_info in columns_info:
                    column_name = column_info['name']
                    columns_desc_file.write(f'## Columns {column_name}\n')
                    columns_desc_file.write(f'{{% docs {column_name} %}}\n')
                    
                    # Get the field description from BigQuery
                    field_description = get_field_description(client, dataset_id, table_name, column_name)
                    if field_description:
                        columns_desc_file.write(f'{field_description}\n')
                    else:
                        columns_desc_file.write(f'. \n')
                    
                    columns_desc_file.write(f'{{% enddocs %}}\n')

def get_field_description(client, dataset_id, table_name, column_name):
    try:
        table_ref = client.dataset(dataset_id).table(table_name)
        table = client.get_table(table_ref)
        field_description = next((field.description for field in table.schema if field.name == column_name), None)
        return field_description
    except Exception as e:
        logging.error(f"Error getting field description: {e}")
        return None

def get_table_description(client, dataset_id, table_name):
    try:
        table_ref = client.dataset(dataset_id).table(table_name)
        table = client.get_table(table_ref)
        return table.description
    except Exception as e:
        logging.error(f"Error getting table description: {e}")
        return None

def export_bigquery_schema_to_yaml(project_id, dataset_id, output_folder, table_name=None):
    try:
        client = bigquery.Client(project=project_id)
        tables = get_tables(client, dataset_id, table_name)

        output_structure = {'version': 2, 'models': []}

        for table_id in tables:
            output_structure['models'].append(prepare_table_info(client, dataset_id, table_id))
            # output_structure['models'].append({})  # Add an empty line after each table schema

        output_yaml_path = os.path.join(output_folder, 'output_file.yml')
        write_yaml(output_yaml_path, output_structure)

        table_descriptions = generate_table_description(client, dataset_id, table_name)

        generate_table_description_file(output_folder, table_descriptions, client, dataset_id)

        generate_columns_description(output_folder, output_structure, client, dataset_id)

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

    except Exception as e:
        logging.error(f"Error exporting BigQuery schema to YAML: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <project_id> <dataset_id> [table_name]")
        sys.exit(1)

    project_id = sys.argv[1]
    dataset_id = sys.argv[2]
    output_folder = os.getcwd()

    table_name = sys.argv[3] if len(sys.argv) > 3 else None

    export_bigquery_schema_to_yaml(project_id, dataset_id, output_folder, table_name)
