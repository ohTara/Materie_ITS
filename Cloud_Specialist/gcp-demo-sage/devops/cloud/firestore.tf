# RECUPERATO dalla Local History di VS Code (versione del 13/10 ore 12:43).
resource "google_firestore_database" "db" {
  project     = var.project_id
  name        = local.firestore_database_name
  location_id = var.region
  type        = "FIRESTORE_NATIVE"

  depends_on = [google_project_service.apis]
}

resource "google_firestore_index" "chunks_embedding" {
  project     = var.project_id
  database    = google_firestore_database.db.name
  collection  = "chunks"
  query_scope = "COLLECTION"

  fields {
    field_path = "__name__"
    order      = "ASCENDING"
  }

  fields {
    field_path = "embedding"
    vector_config {
      dimension = 768
      flat {}
    }
  }
}
