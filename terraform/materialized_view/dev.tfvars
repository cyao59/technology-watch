//CONFIGURATION VARIABLES
service_account_config = {
  project_id = ""
  email      = "tata-terraform@tata-dev.iam.gserviceaccount.com"
}

location   = "europe-west1"
project_id = ""
env        = "dev"

# Add your external bigquery reader here
bigquery_viewers = [
  "serviceAccount:composer-toto@toto-dev.iam.gserviceaccount.com" # toto-dev
]

# Add your external cloud storage reader
composer_connection_manager_service_account = "serviceAccount:composer-toto@toto-dev.iam.gserviceaccount.com" # toto-dev
