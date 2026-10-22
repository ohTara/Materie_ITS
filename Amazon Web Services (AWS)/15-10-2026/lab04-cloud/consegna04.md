# Consegna Lab 04

Studente: Luca Tarallo
Modalità: esecuzione Academy
Regione e nome bucket: us-east-1 / cloud04-lt2026
Risorse preesistenti da non modificare: vpc-*, subnet-*, role-*, bucket preesistenti dell'account

## Requisiti e schema

### 1. Criteri di Accettazione Osservabili

- **Chi legge:** Solo l'operatore/client autenticato con credenziali IAM della sessione temporanea AWS.
- **Contenuto restituito:** Il file `rapporto04.txt` deve corrispondere esattamente byte per byte (verificato tramite hash SHA256) al file caricato.
- **Evidenza di chiusura:** Il bucket `cloud04-lt2026` e l'oggetto contenuto vengono completamente eliminati (listato bucket vuoto/assente) al termine dell'esercitazione.

### 2. Diagramma del Flusso

`Operatore -> Console o CLI -> API autenticate S3 (PUT/GET) -> Bucket (cloud04-lt2026) -> Oggetto (rapporto04.txt)`

### 3. Modello degli Elementi

| Elemento | Nome nel caso | Funzione | Evidenza necessaria |
| :--- | :--- | :--- | :--- |
| **Servizio** | Amazon S3 | Servizio di Object Storage gestito | Risposta alle API S3 / Console attiva |
| **Risorsa** | `cloud04-lt2026` | Bucket contenitore globale in us-east-1 | Schermata bucket in Console / `aws s3 ls` |
| **Dato** | `rapporto04.txt` | Chiave e contenuto dell'oggetto memorizzato | Hash SHA256 del file caricato/scaricato |
| **Identità** | Sessione AWS Academy | Credenziali temporanee IAM/STS | Output di `aws sts get-caller-identity` |

### 4. Distinzione Chiavi e Privilegi

---

## Registro Prove (P1 - P6)

| Prova | Previsione | Operazione | Risultato osservato | Evidenza | Limite della conclusione |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **P1** | Upload V1 riuscito e scaricabile | Upload `originale-v1/rapporto04.txt` su S3 e download in `scaricato-v1/` | Oggetto creato con chiave `rapporto04.txt`. Download completato con successo | Dimensione file, timestamp e SSE-S3 visibili in Console | Dimostra l'avvenuto trasferimento, non ancora l'integrità binaria |
| **P2** | Hash SHA256 identici tra originale e scaricato | Calcolo SHA256 locale su `originale-v1` e `scaricato-v1` | Gli hash dei due file coincidono perfettamente (`8BDD7B612767D25E05094F85C8305A4219798BC9647AF56B78B33A91AE729A67`) | Output del comando `Get-FileHash` | Conferma l'integrità della sola copia V1 scaricata |
| **P3** | V2 sovrascrive V1; V1 non è più recuperabile su S3 | Upload `originale-v2/rapporto04.txt` sullo stesso bucket/chiave | L'oggetto viene sovrascritto. Il download in `scaricato-v2/` restituisce il testo V2 | Hash V2 coincidente (`7C94EC99654D5DBBF1A18E073A4FCB8BD0F01752CE1CED49090FB9FFCB572BBB`) | Dimostra che senza Versioning attivo la sovrascrittura è distruttiva su S3 |
| **P4** | Ripristino V1 ricaricando dalla copia locale | Upload di `originale-v1/rapporto04.txt` e download in `ripristinato/` | L'oggetto torna ad essere V1. Download verificato | Hash in `ripristinato/` identico a `originale-v1/` | Il ripristino è stato possibile solo grazie al backup locale, non da S3 |

| **P5** | Accesso anonimo negato (403 AccessDenied) | Apertura dell'Object URL in finestra incognito del browser | Il browser mostra errore 403 / AccessDenied | Messaggio XML `AccessDenied` a schermo | Conferma il blocco pubblico anonimo, non censa altre policy autenticate |
| **P6** | Errore di chiave/sessione diagnosticato | Diagnosi ticket (es. chiave errata `Rapporto04.txt`) | La richiesta fallisce con 404 Not Found o 403 AccessDenied | Output HEAD/GET di errore | Identifica la causa specifica senza modificare le policy IAM |

---

## Configurazione e responsabilità

### Proprietà del Bucket e Livelli

- **Object Ownership:** *ACLs disabled / Bucket owner enforced* (Livello: Bucket). Disabilita le ACL e garantisce che il proprietario del bucket possieda tutti gli oggetti.
- **Block Public Access:** *Attivo (Tutte e 4 le opzioni)* (Livello: Bucket). Previene qualsiasi esposizione pubblica accidentale o tramite policy.
- **Versioning:** *Disabled* (Livello: Bucket). Evita il mantenimento dello storico delle versioni.
- **Default Encryption:** *SSE-S3 (AES-256)* (Livello: Oggetto/Bucket). Cifratura at-rest gestita da S3 senza costi di chiavi KMS.
- **Regione / AZ:** Configurato in `us-east-1` (Regional). S3 gestisce la ridondanza su più Availability Zone trasparentemente.

### Matrice delle Responsabilità (AWS vs Cliente)

| Fase | Responsabilità AWS | Responsabilità Cliente | Evidenza Svolta |
| :--- | :--- | :--- | :--- |
| **Creazione** | Disponibilità dell'infrastruttura S3 e isolamento multi-tenant | Scelta della regione, nome del bucket e configurazione iniziale | Creazione bucket `cloud04-lt2026` in `us-east-1` |
| **Configurazione** | Applicazione ed enforcement delle regole di sicurezza lato servizio | Abilitazione Block Public Access e cifratura SSE-S3 | Verifica opzioni salvate in Properties/Permissions |
| **Uso** | Cifratura at-rest dei dati e integrità fisica dei supporti di memoria | Gestione delle chiavi degli oggetti, controllo degli accessi e uploads | Upload di `rapporto04.txt` e verifica hash P2 |
| **Recupero** | Durabilità del dato memorizzato (99.999999999%) | Abilitazione Versioning / mantenimento copie di backup locali | Ripristino V1 da copia locale (P4) |
| **Rimozione** | Cancellazione fisica dei blocchi di memoria sui dischi sottostanti | Svuotamento dell'oggetto e cancellazione del bucket | Cleanup finale in Console/CLI |

---

## Consumo e disponibilità

### 1. Calcoli del Carico Sintetico

- **Rapporti/giorno:** 12.000 (dimensione: 250 KB decimali ciascuno)
- **Generazione dati/giorno:** $12.000 \times 250\text{ KB} = 3.000.000\text{ KB} = 3\text{ GB/giorno}$
- **Volume a regime (30 giorni):** $3\text{ GB/giorno} \times 30\text{ giorni} = 90\text{ GB}$
- **Richieste PUT/giorno:** 12.000 PUT
- **Richieste GET/giorno:** $12.000 \times 3 = 36.000\text{ GET/giorno}$
- **Traffico scaricato/giorno:** $36.000 \times 250\text{ KB} = 9.000.000\text{ KB} = 9\text{ GB/giorno}$

### 2. Formula del Costo Sintetico

$$\text{Costo Totale} = (\text{GB mese} \times T_{\text{storage}}) + (\text{PUT} \times T_{\text{PUT}}) + (\text{GET} \times T_{\text{GET}}) + (\text{GB Egress} \times T_{\text{egress}})$$
*Dati mancanti per un preventivo reale:* Destinazione del traffico in uscita (Internet vs stessa Regione AWS vs altra Regione), classe di archiviazione (es. Standard vs Infrequent Access), eventuale utilizzo di CloudFront/CDN e tasse/IVA applicabili.

### 3. Archiviazione S3 vs Server Singolo

- Un server singolo con disco locale rappresenta un Single Point of Failure (SPOF) e richiede la gestione manuale dello stato quando si aggiungono istanze in scalabilità orizzontale.
- S3 è un servizio decoppiato, nativamente elastico e distribuito su più Availability Zone della regione `us-east-1`, eliminando la gestione dell'hardware e la sincronizzazione dischi tra server.

---

## Ticket di Diagnosi

- **Sintomo:** Il client riceve `404 Not Found` o `403 AccessDenied` eseguendo `HEAD` / `GET` sull'oggetto.
- **Ipotesi:** La chiave dell'oggetto richiesta (`Rapporto04.txt`) differisce per maiuscole/minuscole rispetto a quella salvata su S3 (`rapporto04.txt`).
- **Verifica:** Confronto tra l'URL/comando invocato dal client e l'elenco esatto delle chiavi restituito da S3 Console o `aws s3 ls`.
- **Correzione:** Modifica della richiesta lato client utilizzando la stringa della chiave esatta `rapporto04.txt`.
- **Controprova:** Re-invocazione del comando GET/HEAD con la chiave corretta e verifica della risposta `200 OK`.

---

## Cleanup

1. **Eliminazione Oggetto:** Selezionato `rapporto04.txt` nel bucket `cloud04-lt2026` -> `Delete` -> Confermata la cancellazione (`permanently delete`).
2. **Verifica Bucket Vuoto:** Aggiornato l'elenco oggetti: 0 oggetti presenti.
3. **Eliminazione Bucket:** Selezionato il solo bucket del lab `cloud04-lt2026` -> `Delete` -> Inserito il nome del bucket per conferma.
4. **Verifica Assenza Bucket:** Aggiornata la lista dei bucket in `us-east-1`: il bucket `cloud04-lt2026` non è più presente nell'account.

*Stato Risorse:* **Nessuna risorsa residua creata dal lab nell'account AWS.*
