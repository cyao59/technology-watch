# Command useful

### activate dbt
Conda activate dtb
 
### Creation de table dans dbt

dbt run -—profiles-dir profiles —target(environnement) env —models set

dbt run --profiles-dir profiles --profile default --target dev  --models mapping_tables
 
## run seed fule .CSV
dbt seed  --profiles-dir profiles --profile default --target dev
 
## build dbt data Lineage

- dbt docs generate --profiles-dir profile
- dbt docs serve --profiles-dir profile

## install dependancies
dbt deps --profiles-dir profile
 
## run dbt test

### sql
dbt test  --profiles-dir profile --select SAP_CUSTOMER_ID
### mock
dbt test --select tag:toto
 
### dbt coverage ( check doc coverage or test coverage)
https://github.com/slidoapp/dbt-coverage
pip install dbt-coverage
dbt run  # Materialize models
dbt docs generate  # Generate catalog.json and manifest.json
dbt-coverage compute doc --cov-report coverage-doc.json  # Compute doc coverage, print it and write it to coverage-doc.json file
dbt-coverage compute test --cov-report coverage-test.json
