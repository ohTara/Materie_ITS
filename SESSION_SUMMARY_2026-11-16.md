# Session Summary — 2026-11-16

## Obiettivo
Creare dispense complete Obsidian Markdown per tutte le 23 materie ITS Cloud Specialist (biennio 2025-27) sotto `_Dispensa_Completa/`.

---

## Stato Avanzamento

### ✅ COMPLETATE (6 materie + indice generale)

| Materia | Moduli | File Creati | Note |
|---------|--------|-------------|------|
| **Indice Generale** | 1 | 1 | MOC principale con collegamenti a tutte le materie |
| **Fondamenti_di_Programmazione_C** | 12 | 12 | Moduli 00-11 (puntatori, memoria dinamica, struct, file I/O, algoritmi) |
| **Fondamenti_di_Base_Dati** | 11 | 11 | Moduli 00-10 (ER, relazionale, SQL DDL/DML/DQL, transazioni, NoSQL) |
| **CSharp_Programmazione_Oggetti** | 17 | 17 | Moduli 00-16 + 99 (.NET, C#, OOP, generics, LINQ, async, EF Core, DI, testing, patterns, Web API) |
| **AWS (Cloud Specialist)** | 8 | 8 | Moduli 01-07 (networking, Wi-Fi/VPN, simulazione protocolli, cloud computing, classificazione servizi, container, Docker/K8s) |
| **RESTful_API_Progettazione** | **13** | **13** | Moduli 00-11 + 99 (REST/HTTP, JSON, Node/Express, CRUD, SQLite, architettura a livelli, auth JWT/OAuth2/OIDC, OpenAPI, versioning, testing, deployment) |

**Totale file .md creati oggi: ~62** (solo RESTful_API = 13 nuovi)

---

### 📁 Struttura _Dispensa_Completa/

```
_Dispensa_Completa/
├── 00 - Indice Generale ITS (MOC).md
├── Fondamenti_di_Programmazione_C/           (12 moduli)
├── Fondamenti_di_Base_Dati/                  (11 moduli)
├── CSharp_Programmazione_Oggetti/            (17 moduli)
├── AWS/                                      (8 moduli)
├── RESTful_API_Progettazione/                (13 moduli)  ← NUOVO
│   ├── 00 - Indice RESTful API Progettazione (MOC).md
│   ├── 01 - Introduzione a REST e HTTP.md
│   ├── 02 - JSON Serializzazione e Validazione.md
│   ├── 03 - Node.js ed Express Fundamentals.md
│   ├── 04 - CRUD Completo con Express.md
│   ├── 05 - Database Integration SQLite.md
│   ├── 06 - Architettura a Livelli.md
│   ├── 07 - Autenticazione e Autorizzazione.md
│   ├── 08 - Documentazione OpenAPI Swagger.md
│   ├── 09 - Versioning e Best Practices.md
│   ├── 10 - Testing API.md
│   ├── 11 - Deployment e Produzione.md
│   └── 99 - Cheatsheet, Glossario, Comandi.md
└── [17 materie rimanenti...]
```

---

### 🔄 PROSSIME MATERIE DA FARE (17)

Basato su cartelle sorgente in `Materie_ITS_nuovo/`:

1. **Sicurezza_informatica** — 7 PDF + approfondimenti (crittografia, RSA, AES, DH, certificati, hashing, password mgmt)
2. **Fondamenti_di_Reti** — Packet Tracer (.pkt binari) + appunti testo
3. **Sistemi_di_Virtualizzazione** — Da verificare contenuti
4. **Microsoft_Azure** — Da verificare contenuti
5. **Sage_RAG_Google_Cloud** — Progetto `gcp-demo-sage` (FastAPI, Vertex AI, Firestore, BigQuery, Terraform)
6. **IoT** — Da verificare contenuti
7. **Microsoft_365** — Da verificare contenuti
8. **Data_Analytics_e_Visualization** — Da verificare contenuti
9. **Inglese_tecnico** — Da verificare contenuti
10. **Copyright** — Da verificare contenuti
11. **Soft_Skills** — Da verificare contenuti
12. **Pari_Opportunità** — Da verificare contenuti
13. **Sicurezza_sul_Lavoro** — Da verificare contenuti
14. **Linux_Server** — Da verificare contenuti
15. **Fondamenti_Version_Control** — Da verificare contenuti
16. **Containers_ITS-ICT** — Da verificare contenuti (Docker/Podman/K8s)
17. **Python** — Progetto `Echoes of the Crypt` (pygame-ce, dungeon crawler)

---

### 📋 Standard Applicati

Ogni modulo segue template coerente:
- **YAML frontmatter**: `tags`, `modulo`, `stato: da-ripassare`
- **Navigazione**: Link bidirezionali MOC ←→ moduli
- **Struttura**: Abstract → Teoria (con tabelle, diagrammi ASCII, code block) → Laboratorio guidato (bash commands) → Domande richiamo (details/summary) → Riferimenti progetto
- **Convenzioni**: `*da verificare*` per dati non confermati, nomi italiani, commenti funzioni
- **Obsidian-ready**: Wikilinks `[[...]]`, callouts `> [!note]`, code blocks con syntax highlighting

---

### 🎯 Prossimo Step (al rientro)

1. **Leggere PDF Sicurezza_informatica** (7 file principali + approfondimenti)
2. **Creare dispensa Sicurezza_informatica** con moduli su:
   - Fondamenti Cybersecurity
   - Password Management & Hashing (Argon2id, bcrypt)
   - Crittografia simmetrica (DES, AES, modalità)
   - Diffie-Hellman Key Exchange
   - Crittografia asimmetrica (RSA, ECC)
   - Certificati digitali, PKI, Hashing
   - OWASP Top 10, Secure Coding
3. Procedere con **Fondamenti_di_Reti** (gestire .pkt binari)

---

### 💾 Git Status

```bash
# File nuovi da commitare:
_Dispensa_Completa/RESTful_API_Progettazione/ (13 file)
_Dispensa_Completa/00 - Indice Generale ITS (MOC).md  (aggiornato con link RESTful)
# + eventuali aggiornamenti indici materie esistenti
```

---

*Session interrotta alle ~17:50. Riprendere da Sicurezza_informatica.*