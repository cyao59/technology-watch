resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = "example_dataset"
  friendly_name               = "test"
  description                 = "This is a test description"
  location                    = "eu"
  gcp_project_id              = var.project_id
  env                         = var.env
}

locals {
  cleaned_folder_list = [for folder in var.folder_list : replace(folder, "/", "")]

  combined_folder_tables = flatten([
    for folder in local.cleaned_folder_list : [
      for table in var.tables : {
        table_id       = table.table_id
        folder         = folder
        schema_file    = table.schema_file
        source_pattern = table.source_pattern
      }
    ]
  ])
}

# Create the Google BigQuery table resources using a for loop.
resource "google_bigquery_table" "tables" {
  for_each = { for idx, table in local.combined_folder_tables : idx => table }

  project             = var.project_id
  dataset_id          = module.bigquery-dataset.dataset_id
  table_id            = "${each.value.table_id}_${each.value.folder}"
  deletion_protection = false

  external_data_configuration {
    autodetect            = false
    ignore_unknown_values = true

    schema                = file(each.value.schema_file)
    source_format         = "CSV"

    csv_options {
      skip_leading_rows      = 1
      field_delimiter        = ","
      quote                  = "\""
      allow_quoted_newlines  = true
    }

    source_uris = [
      "gs://${module.landing-storage.landing_bucket_name}/${each.value.folder}/${each.value.source_pattern}",
    ]
  }
}
