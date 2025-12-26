output "bucket_name" {
  description = "Name of the GCS bucket"
  value       = google_storage_bucket.static_site.name
}

output "bucket_url" {
  description = "Public URL to access the site"
  value       = "https://storage.googleapis.com/${google_storage_bucket.static_site.name}/index.html"
}

output "website_endpoint" {
  description = "Direct bucket website endpoint"
  value       = google_storage_bucket.static_site.url
}