output "bucket_name" {
  description = "Name of the GCS bucket"
  value       = google_storage_bucket.static_site.name
}

output "bucket_url" {
  description = "Public URL to access the site"
  value       = "http://storage.googleapis.com/${google_storage_bucket.static_site.name}/index.html"
}

output "cname_target" {
  description = "CNAME target for DNS configuration"
  value       = "c.storage.googleapis.com"
}

output "dns_instructions" {
  description = "DNS configuration instructions"
  value       = <<-EOT
    Configure your DNS with this CNAME record:
    
    Name: www
    Type: CNAME
    Value: c.storage.googleapis.com
    TTL: 300
    
    After DNS propagates, access your site at:
    http://www.danphillips.cloud
  EOT
}