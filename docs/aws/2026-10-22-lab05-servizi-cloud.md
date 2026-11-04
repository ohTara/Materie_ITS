# Lab 05 — Classificare e scegliere servizi cloud (22/10/2026)

**Cartella:** `Amazon Web Services (AWS)/22-10-2026/lab05-servizi/` (`consegna05.md`, `architettura05.md`)
**Tipo:** analisi e progettazione su carta. **Nessuna risorsa AWS creata.**

## Obiettivo
Scegliere il modello di servizio giusto (IaaS, PaaS, SaaS) per tre casi e sapere **chi è responsabile di cosa**.

## I tre casi e la scelta
| Caso | Requisito chiave | Scelta | Perché non le altre |
|---|---|---|---|
| A — app legacy | migrare senza refactoring, OS e moduli specifici | **VM IaaS** (EC2) | PaaS/SaaS incompatibili con dipendenze non standard |
| B — API per terzi | alta disponibilità, picchi, poca manutenzione | **PaaS** (Elastic Beanstalk) + **RDS** | IaaS = carico sistemistico inutile |
| C — collaborazione aziendale | subito, SSO, zero infrastruttura | **SaaS** | costruire un'app di videoconferenza non ha senso |

La scelta è motivata con una matrice a pesi: tempi 30%, costi operativi 30%, flessibilità 20%, sostenibilità 20% (punteggi finali 7,4 / 8,3 / 8,5).

## Responsabilità condivisa (chi gestisce cosa)
| Livello | VM (IaaS) | Container | PaaS | DB PaaS | SaaS |
|---|:-:|:-:|:-:|:-:|:-:|
| Hardware, datacenter, hypervisor | Provider | Provider | Provider | Provider | Provider |
| Sistema operativo | **Tu** | Provider | Provider | Provider | Provider |
| Runtime/middleware | **Tu** | **Tu** | Provider | Provider | Provider |
| Codice e dati | **Tu** | **Tu** | **Tu** | **Tu** | Provider |
| Configurazione e accessi | **Tu** | **Tu** | **Tu** | **Tu** | **Tu** |

Regola mnemonica: **configurazione e accessi restano sempre al cliente**, qualunque sia il modello.

## Incidenti classificati
| Incidente | Responsabile | Azione |
|---|---|---|
| Patch OS non applicate su VM | Utente (IaaS) | automatizzare le patch |
| Certificato TLS scaduto su API | Utente (PaaS) | rinnovo automatico (Certbot / certificate manager) |
| Outage del datacenter del SaaS | Provider | piano di contingenza, supporto |

Cambio di requisiti (isolamento di rete e conformità stringente per il caso B): si passa a **IaaS su VPC / nodi dedicati** → più controllo su firewall, rotte e cifratura, ma più carico operativo e costi fissi.

## Architettura "Invia manutenzione con allegato" (`architettura05.md`)
`Utente → API (Beanstalk) → RDS (record) + S3 (allegato)`.
1. `POST /manutenzione` con dati e file.
2. L'API valida e crea un `ticket_id`; scrive il record in stato `PENDING` su RDS.
3. Carica l'allegato su S3 con chiave `allegati/{ticket_id}/documento.pdf`.
4. Se tutto va bene aggiorna a `COMPLETED` e risponde `201`.

| Tratta | Identità | Permesso | Errore |
|---|---|---|---|
| Utente → API | token Bearer JWT | ruolo `InviaRichiesta` | 401 / 400 |
| API → RDS | credenziali da Secrets Manager | `INSERT/UPDATE` sullo schema | 500 + rollback |
| API → S3 | ruolo IAM dell'istanza | `s3:PutObject` sul bucket | 500 |

**Stato incompleto:** se il record su RDS è scritto ma l'upload su S3 fallisce, il record passa a `FAILED_ATTACHMENT` e l'API risponde 500; al nuovo tentativo si aggiorna lo stesso record (niente duplicati).
**Cosa "PaaS" non risolve da solo:** permessi IAM verso RDS/S3 e compatibilità delle librerie native del runtime.
**Esportazione completa:** dump del DB + download del bucket + script che verifica che ogni `allegato_path` esista davvero.

## Domande di richiamo
1. Qual è la differenza di responsabilità sul sistema operativo tra IaaS e PaaS?
2. Perché in un flusso DB + S3 serve uno stato come `FAILED_ATTACHMENT`?

<details><summary>Risposte</summary>

1. In IaaS patch e sicurezza dell'OS sono del cliente; in PaaS le gestisce il provider.
2. Perché le due scritture non sono atomiche: senza stato esplicito resterebbe un record senza file e non si saprebbe come riprovare.
</details>
