moved {
  from = google_cloud_run_v2_service.api
  to   = google_cloud_run_v2_service.sage
}

moved {
  from = google_cloud_run_v2_service_iam_member.public
  to   = google_cloud_run_v2_service_iam_member.sage_public
}

moved {
  from = google_storage_bucket.docs
  to   = google_storage_bucket.sage_docs
}

moved {
  from = google_bigquery_dataset.analytics
  to   = google_bigquery_dataset.sage_analytics
}

moved {
  from = google_service_account.run
  to   = google_service_account.sage_run
}

moved {
  from = google_bigquery_dataset_iam_member.run_editor
  to   = google_bigquery_dataset_iam_member.sage_run_editor
}

moved {
  from = google_storage_bucket_iam_member.run_docs_reader
  to   = google_storage_bucket_iam_member.sage_run_docs_reader
}

moved {
  from = google_project_iam_member.run["roles/aiplatform.user"]
  to   = google_project_iam_member.sage_run["roles/aiplatform.user"]
}

moved {
  from = google_project_iam_member.run["roles/bigquery.jobUser"]
  to   = google_project_iam_member.sage_run["roles/bigquery.jobUser"]
}

moved {
  from = google_project_iam_member.run["roles/datastore.user"]
  to   = google_project_iam_member.sage_run["roles/datastore.user"]
}
