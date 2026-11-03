variable "project_id" {
  description = "ID del progetto GCP in cui creare le risorse"
  type        = string
}

variable "region" {
  description = "Regione GCP per le risorse regionali"
  type        = string
  default     = "europe-west6"
}

variable "resource_prefix" {
  description = "Prefisso per i nomi delle risorse. Vuoto = progetto dedicato, valorizzato = progetto condiviso"
  type        = string
  default     = ""

  validation {
    condition     = can(regex("^([a-z][a-z0-9-]*[a-z0-9])?$", var.resource_prefix))
    error_message = "resource_prefix deve essere vuoto oppure contenere solo minuscole, cifre e trattini (inizia con una lettera, non finisce con un trattino)."
  }
}
