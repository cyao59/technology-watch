resource "google_storage_bucket_object" "landing_folder" {
  for_each = { for folder in var.folder_list : folder => folder }
  name   = each.key
  content = " "            # content is ignored but should be non-empty
  bucket = "${var.env}"
}
