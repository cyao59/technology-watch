variable "service_account_config" {
  type = object({
    email      = string,
    project_id = string
  })
  description = "the service account used to execute the terraform script"
}

variable "location" {
  description = "GCP location"
  type = string
  default = "europe-west1"
}

variable "project_id" {
    type = string
}

variable "env" {
    type = string
}

variable "bigquery_viewers" {
  type = list(string)
}

variable "composer_connection_manager_service_account" {
  type        = string
  description = "Composer connection manager Service Account"
}

variable "folder_list" {
  type = set(string)
  default = ["folder_1/", "folder_2/", "folder_3/", "folder_4/"]
}

# Define a list of tables with their configurations.
variable "tables" {
  type = list(object({
    table_id       = string
    schema_file    = string
    source_pattern = string
  }))
  default = [
    {
      table_id       = "TABLE_1"
      schema_file    = "resources/bq_templates/table_1.json"
      source_pattern = "table_1*.csv"
    },
    {
      table_id       = "TABLE_2"
      schema_file    = "resources/bq_templates/table_2.json"
      source_pattern = "table_2*.csv"
    },
    # Add additional tables with their configurations
  ]
}
