# Provider configuration
provider "google" {
  credentials = var.gcp_credentials
  project     = var.project_id
  region      = var.region
}

# Storing our state in HCP Cloud
terraform { 
  cloud { 
    organization = "SluggerField" 

    workspaces { 
      name = "gcp-danphillips-cloud" 
    } 
  } 
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
    origin          = ["https://danphillips.cloud", "https://www.danphillips.cloud"]
    method          = ["GET", "HEAD", "POST"]
    response_header = ["Content-Type"]
    max_age_seconds = 3600
  }
}

# Make bucket publicly readable
resource "google_storage_bucket_iam_member" "public_read" {
  bucket = google_storage_bucket.static_site.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}