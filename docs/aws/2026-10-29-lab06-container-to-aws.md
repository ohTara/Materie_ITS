# Lab 06 — Dal container al sito su AWS (29/10/2026)

**Cartella:** `Amazon Web Services (AWS)/29-10-2026/lab06-consegna/` · **Regione:** `us-east-1` · **Ambiente:** AWS Learner Lab.

## Obiettivo
Portare un sito containerizzato da una macchina locale a una EC2 pubblica passando da un registry (ECR), aggiornarlo da V1 a V2, fare rollback e simulare due guasti.

## Flusso (ricostruito dalla consegna: i singoli comandi non sono nella repo)
`immagine 1.0 / 2.0 → repository ECR → EC2 (pull + run del container `lab06-sito`) → http://<IP pubblico>:8080`

## Risorse create (e poi eliminate)
- VPC `lab06-CSP-vpc`, subnet, Internet Gateway, route table, Security Group `lab06-CSP-sg`.
- EC2 `lab06-CSP` con instance profile `LabInstanceProfile` (ruolo `LabRole`): l'accesso a ECR avviene **con il ruolo dell'istanza**, senza chiavi nel codice.
- Repository ECR `lab06-csp` con due immagini: tag `1.0` e `2.0` (ognuna ha un *digest* `sha256:` che la identifica in modo immutabile).
- Accesso alla macchina via **Session Manager** (terminale nel browser).

## Aggiornamento V1 → V2 e rollback
V2 aggiunge il servizio "Gestione ticket". Il rollback consiste nel rifare il run con il tag `1.0`; la verifica è `sudo docker inspect lab06-sito` (screenshot 4).
**Idea chiave:** un tag (`1.0`) è un'etichetta mobile, il **digest** è l'identità vera dell'immagine.

## Guasti simulati
| Guasto | Come | Sintomo | Diagnosi |
|---|---|---|---|
| A — processo fermo | `docker stop lab06-sito` | `Connection refused` | nessun processo in ascolto → `docker start` |
| B — rete | tolta la regola inbound 8080 dal Security Group | **timeout** dal browser (`ERR_CONNECTION_TIMED_OUT`) ma `curl` locale sulla EC2 funziona | il filtro è *prima* dell'istanza (SG) → si ripristina la regola |

Rifiutata vs timeout è la stessa distinzione del Lab 03: **rifiutata = host vivo senza servizio; timeout = qualcuno scarta i pacchetti**.

## Cleanup (ordine)
1. `docker system prune -a --volumes` sulla EC2.
2. Eliminati repository e immagini ECR.
3. EC2 terminata.
4. VPC, subnet, SG, route table, IGW eliminati.

## Note di sicurezza per la repo
La relazione originale (`cosegna06.md`) contiene l'**ID account AWS** nell'URI di ECR. Non è una credenziale, ma conviene oscurarlo (`<ACCOUNT_ID>`) nei file pubblici.

## Domande di richiamo
1. Perché la pull da ECR funziona sulla EC2 senza `aws configure`?
2. Che cosa distingue il guasto A dal guasto B guardando solo il sintomo?

<details><summary>Risposte</summary>

1. Perché l'istanza ha un instance profile con un ruolo IAM: le credenziali temporanee arrivano dal servizio metadata.
2. A: connessione rifiutata (immediata). B: timeout (i pacchetti non arrivano) — e `curl` locale funziona, quindi il servizio è vivo.
</details>
