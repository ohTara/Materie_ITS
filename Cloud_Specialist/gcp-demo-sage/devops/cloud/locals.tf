locals {
  # Progetto condiviso = c'è un prefisso
  shared = var.resource_prefix != ""

  # Cloud Run e Artifact Registry
  app_name = local.shared ? "${var.resource_prefix}-sage" : "sage"

  # Bucket dei documenti sorgente
  docs_bucket_name = local.shared ? "${var.resource_prefix}-sage-docs" : "${var.project_id}-sage-docs"

  # Firestore: un solo (default) per progetto, quindi in condiviso un database per persona
  firestore_database_name = local.shared ? var.resource_prefix : "(default)"

  # BigQuery: i dataset non ammettono trattini
  bigquery_dataset_id = local.shared ? "${replace(var.resource_prefix, "-", "_")}_sage_analytics" : "sage_analytics"

  # Service account: forziamo l'ID esatto presente nello stato GCP per evitare destroy/recreate
  sa_account_id = "its-ict-sage-luc-4137-sage-run"
}