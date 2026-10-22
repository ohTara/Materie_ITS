# Relazione di Consegna - Lab 05: Classificazione e Selezione Servizi Cloud

---

## 1. Mappatura Requisiti Operativi dei Casi Studio

| Caso Studio | Requisito Principale | Vincoli e Dipendenze |
| :--- | :--- | :--- |
| **Caso A (Legacy)** | Migrazione app legacy con minimi cambiamenti | Sistema operativo specifico, moduli custom, nessun refactoring |
| **Caso B (API)** | Esposizione API scalabili per terze parti | Alta disponibilità, gestione picchi di carico, manutenzione ridotta |
| **Caso C (SaaS)** | Strumento di collaborazione per team aziendale | Implementazione immediata, integrazione SSO, zero gestione infrastruttura |

---

## 2. Scheda Tecnico-Operativa dei 5 Servizi Cloud

### 1. Macchina Virtuale IaaS (es. EC2)

- **Modello:** IaaS | **Configurazione:** OS, CPU, RAM, Disk, Security Groups
- **Responsabilità Utente:** Patch OS, sicurezza middleware, backup, scaling manuale
- **Confine Operativo:** L'utente gestisce tutto dall'OS in su; il provider gestisce l'hardware.

### 2. Contenitore IaaS/PaaS (es. ECS/EKS)

- **Modello:** IaaS/PaaS (IaaS per nodi, PaaS per orchestrazione) | **Configurazione:** Dockerfile, task definition, risorse
- **Responsabilità Utente:** Gestione immagini Docker, vulnerabilità app, sizing dei container
- **Confine Operativo:** Il provider gestisce il control plane dell'orchestratore.

### 3. Piattaforma di Esecuzione PaaS (es. Elastic Beanstalk)

- **Modello:** PaaS | **Configurazione:** Codice applicativo, variabili d'ambiente, runtime
- **Responsabilità Utente:** Codice sorgente, dipendenze applicative, configurazione logica
- **Confine Operativo:** Il provider gestisce il provisioning di OS, runtime, web server e auto-scaling.

### 4. Database Relazionale Gestito PaaS (es. RDS)

- **Modello:** PaaS | **Configurazione:** Parametri DB, utenti, schema, retention backup
- **Responsabilità Utente:** Modello dati, query, indici, gestione accessi e privilegi
- **Confine Operativo:** Il provider gestisce patch del motore DB, backup automatici e failover HA.

### 5. Applicazione SaaS (es. Videoconferenza)

- **Modello:** SaaS | **Configurazione:** Utenti, ruoli, integrazione SSO, policy di accesso
- **Responsabilità Utente:** Gestione identità, permessi e corretta fruizione del servizio
- **Confine Operativo:** Il provider gestisce l'intera applicazione, l'infrastruttura e gli aggiornamenti.

---

## 3. Matrice Comparativa della Responsabilità Condivisa

### Matrice

| Componente / Livello | Macchina Virtuale (IaaS) | Contenitore (IaaS/PaaS) | API PaaS | DB PaaS (RDS) | App SaaS |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Hardware e Datacenter** | Provider | Provider | Provider | Provider | Provider |
| **Virtualizzazione / Hypervisor** | Provider | Provider | Provider | Provider | Provider |
| **Sistema Operativo (OS)** | **Utente** | Provider | Provider | Provider | Provider |
| **Runtime / Middleware** | **Utente** | **Utente** | Provider | Provider | Provider |
| **Codice Applicativo / Dati** | **Utente** | **Utente** | **Utente** | **Utente** | Provider |
| **Configurazione / Accessi** | **Utente** | **Utente** | **Utente** | **Utente** | **Utente** |

### Confronti Chiave

1. **VM IaaS vs PaaS:** Nella VM l'utente gestisce patch OS e runtime; nel PaaS il provider mantiene OS e runtime.
2. **PaaS vs SaaS:** Nel PaaS l'utente sviluppa e possiede il codice applicativo; nel SaaS usa un'applicazione pronta gestita dal provider.

---

## 4. Decisioni Motivate per Caso Studio

### Caso A (Legacy) -> **Macchina Virtuale IaaS**

- **Motivazione:** Richiede un OS e moduli specifici senza refactoring.
- **Scarto PaaS/SaaS:** Incompatibili con dipendenze legacy non standard.

### Caso B (API) -> **API PaaS (Elastic Beanstalk) + DB PaaS (RDS)**

- **Motivazione:** Elimina la gestione dell'infrastruttura consentendo al team di focalizzarsi sulle API, con scaling automatico.
- **Scarto IaaS:** Comporterebbe un carico di gestione sistemistica non necessario.

### Caso C (SaaS) -> **Applicazione SaaS**

- **Motivazione:** Servizio di collaborazione pronto all'uso con integrazione SSO immediata.
- **Scarto PaaS/IaaS:** Creare da zero un software di videoconferenza richiede sforzi di sviluppo ingiustificati.

### Matrice Tracciabilità e Pesi

| Caso Studio | Opzione Selezionata | P1: Tempi (30%) | P2: Costi Op. (30%) | P3: Flessibilità (20%) | P4: Sostenibilità (20%) | Punteggio |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Caso A** | VM IaaS | 8 | 6 | 9 | 7 | **7.4** |
| **Caso B** | API PaaS + RDS | 9 | 8 | 7 | 9 | **8.3** |
| **Caso C** | App SaaS | 10 | 9 | 5 | 9 | **8.5** |

---

## 5. Analisi degli Incidenti Operativi

| ID Incident | Causa Radice | Livello di Responsabilità | Azione Correttiva |
| :--- | :--- | :--- | :--- |
| **INC-01 (Patch OS)** | Mancata applicazione patch su VM | **Utente (IaaS)** | Configurazione di automazioni per patch OS |
| **INC-02 (Certificato API)** | Certificato TLS scaduto | **Utente (PaaS)** | Rinnovo e automazione via Certbot / Certificate Manager |
| **INC-03 (Interruzione SaaS)** | Outage del data center provider | **Provider (SaaS)** | Attivazione piano di contingenza / Contatto con il supporto |

---

## 6. Revisione Architetturale per Cambio Requisiti (Caso B)

- **Nuovo Requisito:** Isolamento di rete dedicato e conformità stringente.
- **Nuova Scelta:** **IaaS su Virtual Private Cloud (VPC) / Nodi Dedicati**.
- **Impatto:**
  1. Maggior controllo su regole di firewall, rotte di rete e cifratura.
  2. Incremento del carico operativo per la gestione dei server e della manutenzione.
  3. Aumento dei costi fissi infrastrutturali.

---

## 7. Dichiarazione Risorse e Ambiente Locale

L'analisi e la progettazione sono state completate nell'ambiente locale in `Documenti/lab05-servizi/`. Nessuna risorsa AWS è stata creata sul cloud reale.
