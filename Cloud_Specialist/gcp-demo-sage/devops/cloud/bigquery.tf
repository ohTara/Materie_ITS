# Dataset BigQuery per gli analytics delle domande/risposte Sage
resource "google_bigquery_dataset" "sage_analytics" {
  project    = var.project_id
  dataset_id = local.bigquery_dataset_id
  location   = var.region

  delete_contents_on_destroy = local.shared

  depends_on = [google_project_service.apis]
}

resource "google_bigquery_table" "question_log" {
  project             = var.project_id
  dataset_id          = google_bigquery_dataset.sage_analytics.dataset_id
  table_id            = "question_log"
  deletion_protection = false

  schema = jsonencode([
    {
      name = "timestamp"
      type = "TIMESTAMP"
      mode = "REQUIRED"
    },
    {
      name = "question"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "sources_count"
      type = "INTEGER"
      mode = "NULLABLE"
    },
    {
      name = "latency_ms"
      type = "INTEGER"
      mode = "NULLABLE"
    }
  ])
}
