# Terraform su Azure — primo Resource Group (02/07/2026)

**Cartella:** `Microsoft Azure/Terraform 02-07-2026/` (`main.tf`, `variables.tf`, `outputs.tf`, `.terraform.lock.hcl`)

## Obiettivo
Primo giro completo di Infrastructure as Code: dichiarare un **Resource Group** Azure con Terraform e leggerne gli output.

## Cosa contiene
```hcl
terraform {
  required_version = ">= 1.6.0"
  required_providers { azurerm = { source = "hashicorp/azurerm", version = "~> 4.0" } }
  backend "local" { path = "terraform.tfstate" }
}
provider "azurerm" { features {} }
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name   # default "rg-minimal"
  location = var.location              # default "Italy North"
}
```
`outputs.tf` espone `resource_group_name` e `resource_group_location`.

## Come funziona (da ricordare)
- **Provider** = plugin che traduce le risorse HCL in chiamate API di Azure; `~> 4.0` accetta 4.x ma non 5.0. Il file `.terraform.lock.hcl` fissa versione e checksum.
- **State** = Terraform confronta *codice desiderato* ↔ *state* ↔ *realtà* per calcolare il piano. Qui è un backend **locale**.
- **Flusso:** `terraform init` → `terraform plan` → `terraform apply` → `terraform destroy`.
- **Variabili con default** rendono il modulo riutilizzabile senza modificare `main.tf`.

## Attenzione (sicurezza)
Nella cronologia git (commit del 22/10/2026) è stato aggiunto anche `terraformstate.tfstate`. Lo state può contenere ID di sottoscrizione e, in altri casi, valori sensibili: non va committato. Vedi `docs/README.md` → *Manutenzione della repo*.

## Collegamenti
Stesso schema (provider + risorse + variabili + backend) del progetto GCP `gcp-demo-sage`, ma lì lo state è remoto su bucket. Slide correlate: *19) Infrastructure as Code* (vedi `lezioni-slide.md`).

## Domande di richiamo
1. Che cosa succede se esegui due volte `terraform apply` senza cambiare il codice?
2. Perché lo state non va su Git e dove dovrebbe stare in un team?

<details><summary>Risposte</summary>

1. Nulla: il piano è vuoto (infrastruttura già allineata allo state) — è l'idempotenza.
2. Può contenere dati sensibili e va condiviso/bloccato: backend remoto con locking (es. bucket).
</details>
