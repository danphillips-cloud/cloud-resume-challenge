variable "gcp_credentials" {
  description = "GCP service account credentials JSON"
  type        = string
  sensitive   = true
}

variable "project_id" {
  description = "GCP Project ID"
  type        = string
  default     = "danphillips-cloud-crc"
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-east1"
}

variable "bucket_name" {
  description = "Name of the GCS bucket for static site (must be globally unique)"
  type        = string
  default     = "danphillips.cloud"
}