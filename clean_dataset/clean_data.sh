#!/bin/bash

## Set value for project_id and dataset_id
echo "Set value for project_id and dataset_id."
project_id=''
dataset_id=''

echo "Set list of tables from $dataset_id."
tables=$(bq ls "$project_id:$dataset_id" | awk '{print $1}' | tail +3 )

# Check if dataset contains tables
if [ -z "$tables" ]; then
    echo "No table found in dataset $dataset_id."
    exit 0
fi

## Remove all tables from dataset  to another dataset
for table in $tables
do  
    echo "$table deleted."
    bq rm -f "$project_id:$dataset_id.$table" 
done

echo "All tables from dataset $dataset_id has been deleted."
