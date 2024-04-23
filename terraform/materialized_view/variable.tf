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