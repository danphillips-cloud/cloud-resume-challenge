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

  # CORS configuration for API calls from the website
  cors {
    origin          = ["https://danphillips.cloud", "https://www.danphillips.cloud"]
    method          = ["GET", "POST"]
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

# ============================================
# Enable Required APIs
# ============================================

# Enable Cloud Functions API
resource "google_project_service" "cloudfunctions" {
  service            = "cloudfunctions.googleapis.com"
  disable_on_destroy = false
}

# Enable Cloud Run API (required for Functions v2)
resource "google_project_service" "run" {
  service            = "run.googleapis.com"
  disable_on_destroy = false
}

# Enable Cloud Build API (required for function deployment)
resource "google_project_service" "cloudbuild" {
  service            = "cloudbuild.googleapis.com"
  disable_on_destroy = false
}

# Enable Firestore API
resource "google_project_service" "firestore" {
  service            = "firestore.googleapis.com"
  disable_on_destroy = false
}

# ============================================
# Cloud Function v2 for Visitor Counter
# ============================================

# Storage bucket for function source code
resource "google_storage_bucket" "function_bucket" {
  name                        = "${var.project_id}-functions"
  location                    = var.region
  uniform_bucket_level_access = true
  depends_on                  = [google_project_service.cloudfunctions]
}

# Archive the function code
data "archive_file" "function_source" {
  type        = "zip"
  source_dir  = "${path.module}/function"
  output_path = "${path.module}/function.zip"
}

# Upload function to bucket
resource "google_storage_bucket_object" "function_zip" {
  name   = "visitor-counter-${data.archive_file.function_source.output_md5}.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = data.archive_file.function_source.output_path
}

# Service account for Cloud Function
resource "google_service_account" "function_sa" {
  account_id   = "visitor-counter-sa"
  display_name = "Visitor Counter Function Service Account"
}

# Note: Firestore permissions must be granted manually via GCP Console
# due to organization policy restrictions on project-level IAM bindings.
# Grant the service account 'Cloud Datastore User' role in IAM.

# Deploy Cloud Function v2
resource "google_cloudfunctions2_function" "visitor_counter" {
  name     = "visitor-counter"
  location = var.region

  build_config {
    runtime     = "python311"
    entry_point = "visitor_counter"
    source {
      storage_source {
        bucket = google_storage_bucket.function_bucket.name
        object = google_storage_bucket_object.function_zip.name
      }
    }
  }

  service_config {
    available_memory      = "256M"
    timeout_seconds       = 60
    max_instance_count    = 10
    service_account_email = google_service_account.function_sa.email

    environment_variables = {
      PROJECT_ID = var.project_id
    }
  }

  depends_on = [
    google_project_service.cloudfunctions,
    google_project_service.run,
    google_project_service.cloudbuild
  ]
}

# Make function publicly accessible
resource "google_cloud_run_service_iam_member" "public_access" {
  project  = google_cloudfunctions2_function.visitor_counter.project
  location = google_cloudfunctions2_function.visitor_counter.location
  service  = google_cloudfunctions2_function.visitor_counter.name

  role   = "roles/run.invoker"
  member = "allUsers"
}

# ============================================
# Outputs
# ============================================

output "function_url" {
  value = google_cloudfunctions2_function.visitor_counter.service_config[0].uri
}
