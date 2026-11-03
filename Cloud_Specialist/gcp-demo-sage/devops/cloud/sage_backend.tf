resource "google_service_account" "sage_run" {
  project      = var.project_id
  account_id   = local.sa_account_id
  display_name = "Sage Cloud Run runtime (${local.app_name})"

  depends_on = [google_project_service.apis]
}

resource "google_project_iam_member" "sage_run" {
  for_each = toset([
    "roles/aiplatform.user",
    "roles/bigquery.jobUser",
    "roles/datastore.user",
  ])

  project = var.project_id
  role    = each.value
  member  = google_service_account.sage_run.member
}

resource "google_bigquery_dataset_iam_member" "sage_run_editor" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.sage_analytics.dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = google_service_account.sage_run.member
}

resource "google_storage_bucket_iam_member" "sage_run_docs_reader" {
  bucket = google_storage_bucket.sage_docs.name
  role   = "roles/storage.objectViewer"
  member = google_service_account.sage_run.member
}

resource "google_cloud_run_v2_service" "sage" {
  project  = var.project_id
  name     = local.app_name
  location = var.region

  deletion_protection = false

  lifecycle {
    ignore_changes = [
      scaling,
      template[0].scaling,
    ]
  }

  template {
    service_account = google_service_account.sage_run.email

    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello"

      env {
        name  = "SAGE_PROJECT_ID"
        value = var.project_id
      }
      env {
        name  = "SAGE_REGION"
        value = var.region
      }
      env {
        name  = "SAGE_RESOURCE_PREFIX"
        value = var.resource_prefix
      }
    }
  }

  depends_on = [google_project_service.apis]
}

resource "google_cloud_run_v2_service_iam_member" "sage_public" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.sage.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
