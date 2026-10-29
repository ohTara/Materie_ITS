# Relazione di Consegna - Lab 06: From container to site on AWS

**Corso:** Cloud Specialist  
**Studente / Squadra:** Luca Tarallo (squadra CSP)  
**Data:** 29 Ottobre 2026  
**Regione AWS:** `us-east-1` (N. Virginia)  

---

## 1. Dati Tecnici dell'Infrastruttura

* **ID Istanza EC2:** `i-01d325fa8dbe223f6`
* **IPv4 Pubblico EC2:** `54.165.235.159`
* **VPC:** `lab06-CSP-vpc` (`vpc-0d438b5f48c0e3672`)
* **Ruolo IAM / Profile:** `LabRole` / `LabInstanceProfile`
* **URI Repository Amazon ECR:** `605933472379.dkr.ecr.us-east-1.amazonaws.com/lab06-csp`

---

## 2. Immagini Container e Digest SHA-256

* **Versione 1 (`1.0`):**
  * Tag: `605933472379.dkr.ecr.us-east-1.amazonaws.com/lab06-csp:1.0`
  * Image Digest: `sha256:8a11602922ab51ad80dc523171ca80c33c077cca0a3c0d1b3982bf30b286d547`
  * Local Image ID: `sha256:9275768ca9cc51069f141437ae8d336ed3daad0d2f6b2185d33f627b70822f1a`

* **Versione 2 (`2.0`):**
  * Tag: `605933472379.dkr.ecr.us-east-1.amazonaws.com/lab06-csp:2.0`
  * Image Digest: `sha256:e95dab848544779441ea9992c9194b15ad1e17213d76e0af1f4368faa182cb92`
  * Local Image ID: `sha256:ebf6c4899464a71d1e681495a68f20a07bc19bf9fd56a6e9dd1b62314948159d`

---

## 3. Legenda Screenshot di Verifica (4/4)

1. **Screenshot 1 — Registry Amazon ECR (`screenshot_01_ecr.png`):**
   Mstra la console AWS su Amazon ECR con il repository `lab06-csp` contenente le due immagini caricate con tag `1.0` e `2.0` e i relativi digest SHA-256.

2. **Screenshot 2 — Sito Pubblico Versione 1 (`screenshot_02_site_v1.png`):**
   Mostra l'accesso via browser all'indirizzo `http://54.165.235.159:8080` con il rendering corretto dell'applicazione in Versione 1 per la squadra CSP.

3. **Screenshot 3 — Aggiornamento del Sito Versione 2 (`screenshot_03_site_v2.png`):**
   Mostra l'accesso via browser allo stesso endpoint dopo il deployment dell'immagine `2.0`, verificando la presenza del nuovo servizio *"Gestione ticket"*.

4. **Screenshot 4 — Verification Rollback & Inspect (`screenshot_04_rollback_inspect.png`):**
   Mostra il terminale Session Manager con l'output del comando `sudo docker inspect lab06-sito` che conferma il ripristino riuscito alla versione `1.0`.

---

## 4. Simulazione Guasti e Risoluzione

* **Guasto A (Arresto del Container):**
  Simulato l'arresto del processo con `docker stop lab06-sito`. Verificata l'inaccessibilità (`Connection refused`) e ripristinato il servizio con `docker start lab06-sito`.

* **Guasto B (Blocco di Rete / Security Group):**
  Rimossa la regola Inbound per la porta 8080 dal Security Group `lab06-CSP-sg`. Verificato il timeout da browser del PC (`ERR_CONNECTION_TIMED_OUT`) a fronte del corretto funzionamento locale via `curl`. Ripristinata la regola inbound per confermare il ripristino della connettività.

---

## 5. Cleanup Finale Risorse

Tutte le risorse create sono state correttamente deallocate per aderire ai vincoli di budget del Learner Lab:

* Contenitori ed immagini Docker rimossi sulla EC2 (`docker system prune -a --volumes`).
* Repository `lab06-csp` ed immagini eliminate da Amazon ECR.
* Istanza EC2 `lab06-CSP` terminata (`Terminated`).
* Componenti di rete VPC (`lab06-CSP-vpc`, subnet, Security Group, Route Table e Internet Gateway) eliminate con successo.
