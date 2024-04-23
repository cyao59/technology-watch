resource "google_bigquery_dataset" "ressource_name" {
  for_each                    =  local.versions
  dataset_id                  = "dataser_name"
  location                    = "EU"
}

resource "google_bigquery_table" "table_name_cible" {
  dataset_id  = google_bigquery_dataset.dataset_cible.dataset_id
  table_id    = "table_cible"

  view {
    query          = <<EOF
      SELECT
        *
      FROM `project_id.dataset_source.table_name_source`
      EOF
    use_legacy_sql = false
  }
}
