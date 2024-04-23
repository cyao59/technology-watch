# Here you can add read access to others projects
# for bigquery
resource "google_project_iam_member" "bigquery_data_viewer_role" {
  project  = var.project_id
  role     = "roles/bigquery.dataViewer"
  for_each = toset(var.bigquery_viewers)
  member   = each.value
}

# for cloud storage
resource "google_project_iam_member" "composer_gcs_viewer" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "${var.composer_connection_manager_service_account}"
}
