provider "google" {
  project = var.project_id
  region  = var.region
}

# Storage bucket for static site
resource "google_storage_bucket" "static_site" {
  name          = var.bucket_name
  location      = "US"
  force_destroy = true

  uniform_bucket_level_access = true

  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }

  # CORS configuration for future API calls (visitor counter)
  cors {
    origin          = ["https://${var.www_domain_name}"]
    method          = ["GET", "HEAD", "POST"]
    response_header = ["Content-Type"]
    max_age_seconds = 3600
  }
}

# Note: Public access will be handled via Cloudflare
# Bucket can remain private - Cloudflare will proxy requests