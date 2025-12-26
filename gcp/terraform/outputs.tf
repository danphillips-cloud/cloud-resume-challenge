output "bucket_name" {
  description = "Name of the GCS bucket"
  value       = google_storage_bucket.static_site.name
}

output "bucket_url" {
  description = "Direct GCS bucket URL"
  value       = "https://storage.googleapis.com/${google_storage_bucket.static_site.name}/index.html"
}

output "cloudflare_origin" {
  description = "Origin URL for Cloudflare configuration"
  value       = "storage.googleapis.com/${google_storage_bucket.static_site.name}"
}