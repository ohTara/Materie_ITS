# Architettura e Dipendenze Operative - Lab 05

## 1. Schema Componenti e Confini di Gestione

```text
[ Utente ]
    │
    ▼ (1. Richiesta HTTP / GET/POST)
[ API Manutenzione (PaaS / Elastic Beanstalk) ]
    │
    ├───────────► (3. Scrittura Record DB) ────────────► [ Amazon RDS (PostgreSQL Gestito) ]
    │
    └───────────► (4. Upload Allegato) ────────────────► [ Amazon S3 (Bucket Oggetti) ]

[ Operatore Aziendale ]
    │
    ▼ (Autenticazione SSO)
[ Videoconferenza SaaS ]
```

### Dettaglio dei Componenti e Confini Operativi

* **API Manutenzione (PaaS - Elastic Beanstalk):** Gestisce la logica applicativa, la validazione delle richieste e l'autenticazione. *Confine:* Gestione del codice sorgente e delle dipendenze applicative.
* **Database Relazionale (RDS - PostgreSQL):** Conserva lo stato e i metadati dei ticket di manutenzione. *Confine:* Schema dati, query, indici e utenti DB.
* **Storage ad Oggetti (Amazon S3):** Memorizza gli allegati (immagini, documenti PDF) dei ticket. *Confine:* Gestione degli oggetti, delle chiavi e delle policy di accesso.
* **Videoconferenza SaaS:** Servizio esterno e isolato per le comunicazioni. *Confine:* Gestione delle identità aziendali e permessi di condivisione.

---

## 2. Flusso della Richiesta "Invia Manutenzione con Allegato"

1. **Ingresso:** L'Utente invia una richiesta HTTP `POST /manutenzione` all'API fornendo i dati del ticket e il file allegato.
2. **Validazione:** L'API autentica la richiesta, verifica i dati e la conformità dell'allegato.
3. **Scrittura Record DB:** L'API genera un `ticket_id` univoco e inserisce un nuovo record in stato `PENDING` nel database RDS.
4. **Upload Allegato:** L'API effettua l'upload su Amazon S3 salvando il file con la chiave `allegati/{ticket_id}/documento.pdf`.
5. **Conferma:** A caricamento completato con successo su S3, l'API aggiorna lo stato del record su RDS in `COMPLETED` e risponde all'Utente con codice `201 Created`.

---

## 3. Matrice Interfacce e Autorizzazioni

| Tratta | Identità Usata | Autorizzazione Necessaria | Gestione Errore |
| :--- | :--- | :--- | :--- |
| **Utente -> API** | Token Bearer JWT (OAuth/IAM) | Ruolo Utente `InviaRichiesta` | `401 Unauthorized` / `400 Bad Request` |
| **API -> RDS** | Credenziali DB da Secrets Manager | Privilegio `INSERT/UPDATE` su schema `manutenzione` | `500 Internal Error` / Rollback |
| **API -> S3** | Ruolo IAM dell'istanza Beanstalk | Azione `s3:PutObject` sull'ARN del bucket | `500 Internal Error` / Gestione Inconsistenza |

---

## 4. Gestione dello Stato Incompleto ed Errori Distribuiti

### Scenario di Errore

Il database RDS conferma la scrittura del record, ma l'upload del file su Amazon S3 fallisce (es. errore di rete o permessi).

### Gestione dell'Inconsistenza

* **Stato Incompleto:** Su RDS rimane un record memorizzato privo del file corrispondente su S3.
* **Segnalazione:** L'API intercetta l'errore di S3, aggiorna lo stato del record su RDS in `FAILED_ATTACHMENT` e restituisce all'Utente un errore `500 Internal Server Error` fornendo il codice di tracciamento.
* **Prevenzione Duplicati:** Se l'Utente effettua un nuovo tentativo, l'API verifica la presenza di un ticket in stato `FAILED_ATTACHMENT` per quella richiesta e aggiorna il record esistente senza crearne uno duplicato.

---

## 5. Dipendenze Non Risolte dall'Etichetta PaaS

L'adozione di un modello PaaS non risolve automaticamente le seguenti dipendenze architetturali:

* **Gestione delle Autorizzazioni:** Il PaaS mette a disposizione l'ambiente di esecuzione, ma non definisce quali ruoli IAM o credenziali debbano essere usate per accedere in sicurezza ad RDS ed S3.

* **Compatibilità delle Dipendenze del Runtime:** Il PaaS fornisce il linguaggio di base, ma non compila né mantiene le librerie native o le dipendenze esterne modellate nel codice del cliente.

---

## 6. Procedura di Esportazione Massiva dei Dati

Per esportare l'intero patrimonio informativo:

1. **Estrazione DB:** Dump completo dello schema e delle tabelle del database RDS in formato SQL o CSV.
2. **Download Allegati S3:** Download massivo della struttura di oggetti presente nel bucket S3.
3. **Verifica della Coerenza:** Script di validazione che confronta ogni riferimento salvato nella colonna `allegato_path` del DB con la presenza effettiva del file scaricato da S3
