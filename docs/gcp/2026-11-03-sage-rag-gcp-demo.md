# Progetto Sage — RAG su Google Cloud (gcp-demo-sage)

**Cartella:** `Cloud_Specialist/gcp-demo-sage/` · **Commit:** 03/11/2026 (*integrate gcp-demo-sage…* e *abilita Firestore Vector Search e Vertex AI embedding reali*)
**Origine:** template del corso (ITS ICT — GCP 2026) adattato al proprio progetto GCP.

## Cos'è
**Sage** risponde a domande in linguaggio naturale su un insieme di documenti con il pattern **RAG** (Retrieval-Augmented Generation). Ogni domanda è indipendente: nessuna memoria di conversazione.

## Flusso di una richiesta
`POST /api/ask → embedding della domanda (Vertex AI) → ricerca dei chunk più simili in Firestore (vector search, find_nearest) → risposta di Gemini basata su quei chunk → log su BigQuery → { answer, sources[] }`

| Componente | Servizio GCP |
|---|---|
| API FastAPI (`/api/ask`, `/health`) | Cloud Run |
| Base di conoscenza + indice vettoriale | Firestore (Native) |
| LLM ed embedding | Vertex AI (Gemini), autenticazione con ADC/service account, **nessuna API key** |
| Documenti sorgente | Cloud Storage |
| Analytics delle domande | BigQuery (`question_log`) |
| Immagini container | Artifact Registry |

Firestore e BigQuery sono **opzionali** per l'avvio: se mancano, l'API non fallisce (salta ricerca o log e scrive un `WARNING`).

## Struttura del codice
`sources/backend/src/sage/` a strati: **webapp** (router HTTP) → **domain/qa** (chunking, retrieval, generation) → **integrations** (client Firestore, BigQuery, Vertex AI). `utils/ingest_documents.py` chunka i `.md` in `data/`, calcola gli embedding e li scrive in Firestore (non gira dentro l'API). Test: `tests/test_chunking.py`, `tests/test_health.py`. Gestione dipendenze con **uv**.

## Infrastruttura (Terraform, `devops/cloud/`)
File `.tf` per: API abilitate (`services.tf`), Firestore e indice vettoriale a **768 dimensioni**, tipo `flat` (`firestore.tf`), dataset BigQuery (`bigquery.tf`), Artifact Registry, bucket documenti con `public_access_prevention = enforced` (`docs.tf`), service account runtime con i soli ruoli `aiplatform.user`, `bigquery.jobUser`, `datastore.user` (+ editor del dataset e viewer del bucket) e servizio Cloud Run (`sage_backend.tf`), nomi centralizzati in `locals.tf` con `resource_prefix` per progetti condivisi, `moved.tf` per rinominare risorse senza distruggerle. Regione `europe-west6` (Zurigo). State remoto su bucket (`backend.hcl`). Pipeline previste: `terraform.yml` (plan → approvazione → apply) e `deploy.yml` (build & deploy).

## Concetti da ricordare
- **Embedding:** testo → vettore; testi simili hanno vettori vicini.
- **RAG:** il modello risponde *solo* sui chunk recuperati → meno invenzioni e fonti citabili.
- **Stateless:** niente stato in Cloud Run; la conoscenza sta in Firestore.
- **Privilegio minimo:** il service account runtime ha solo i ruoli necessari.

## Da verificare / attenzione
- `terraform.tfvars` e `backend.hcl` con i nomi del tuo progetto e bucket sono nella cartella e il `.gitignore` del progetto non li esclude: non sono segreti, ma valuta se tenerli pubblici.
- In `sources/backend/.venv` c'è l'ambiente virtuale creato da uv (migliaia di file): contiene un proprio `.gitignore` con `*`, quindi non dovrebbe finire su Git; verifica con `git status`.

## Domanda di richiamo
Perché usare Firestore con campo vettoriale invece di un database vettoriale separato, in questo progetto?

<details><summary>Risposta</summary>Lo stesso database contiene testo, metadati ed embedding e fa anche la ricerca per similarità: meno componenti da gestire e pagare.</details>
