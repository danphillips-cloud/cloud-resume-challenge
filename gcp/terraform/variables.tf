variable "project_id" {
  description = "danphillips-cloud-crc"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-east1"
}

variable "bucket_name" {
  description = "Name of the GCS bucket for static site (must be globally unique)"
  type        = string
}

variable "domain_name" {
  description = "Primary domain name"
  type        = string
  default     = "danphillips.cloud"
}

variable "www_domain_name" {
  description = "WWW subdomain"
  type        = string
  default     = "www.danphillips.cloud"
}