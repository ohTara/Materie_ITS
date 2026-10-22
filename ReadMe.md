# 📚 Corso ITS Cloud Specialist — Repository Didattico Completo

![Branch](https://img.shields.io/badge/Branch-main-blue?style=flat-square&logo=git)
![Status](https://img.shields.io/badge/Status-Attivo-brightgreen?style=flat-square)
![Repo](https://img.shields.io/badge/Repo-Materie__ITS-orange?style=flat-square&logo=github)

> Repository centrale per la conservazione, l'organizzazione e la sincronizzazione di tutto il materiale didattico, esercitazioni, progetti di sviluppo, laboratori e documentazione del corso **Cloud Specialist**.

---

## 🗺️ Indice Generale dei Moduli Didattici

| Icona | Materia / Modulo | Descrizione & Focus Didattico | Sottocartelle & Laboratori |
| :---: | :--- | :--- | :--- |
| ☁️ | **Amazon Web Services (AWS)** | Cloud Infrastructure, Networking, VPN, Protocolli Web, S3, IaC Terraform | `lab01-networking` ➔ `lab05-servizi` |
| ⚡ | **C# / .NET** | Programmazione ad Oggetti (OOP), Incapsulamento, Classi, Gestione Dati e Progetti | Lezioni da `16-03-2026` a `30-04-2026` |
| 🐳 | **Containers (ITS-ICT)** | Architettura Docker, Containerizzazione, Immagini e Orchestrazione | Dispense e Moduli Docker |
| ⚖️ | **Copyright & Norme Giuridiche** | Normative del mondo digitale, licenze software, privacy e diritto d'autore | Dispense e Normative |
| 📊 | **Data Analytics & Visualization** | Analisi dati, Business Intelligence, Data Visualization e Reportistica | Documenti e Dataset |
| 🗄️ | **Fondamenti di Basi Dati** | Progettazione DB, SQL, Gestione tabelle, Backup & Restore | `BackUp & Restore` |
| 💻 | **Fondamenti di Programmazione** | Logica di programmazione, algoritmi e strutture dati base | Lezioni dal `21-01` al `31-03` |
| 🌐 | **Fondamenti di Reti** | Modello ISO/OSI, TCP/IP, Subnetting e Architetture di rete | Dispense e Esercizi |
| 🔀 | **Fondamenti Version Control** | Gestione della versione con Git, branching e workflow collaborativi | `Esercizio-WorkFlow_19-02`, Lezioni |
| 🇬🇧 | **Inglese** | Business English, terminologia tecnica ICT e Cloud | Dispense e Glossari |
| 🐧 | **Linux Server** | Amministrazione di sistema Linux, Shell Scripting e servizi Server | Script e Guide |
| 🔷 | **Microsoft Azure** | Provisioning risorse Azure, Resource Groups e Terraform | `Terraform 02-07-2026` |
| 📦 | **Microsoft 365 (Office)** | Strumenti di produttività aziendale, gestione collaborativa | Guide e dispense |
| ⚖️ | **Pari Opportunità** | Tematiche di inclusione, parità di genere e contesto lavorativo | Documenti di corso |
| 🐍 | **Python** | Scripting, strutture dati (liste, tuple, dizionari), OOP e gestione File | Lezioni dal `10-09` al `06-10`, `Esercizi_OOP_e_Files` |
| 🌐 | **RESTFul API** | Web Services Node.js, Express e gestione DB con SQLite3 | `libreriaOnline`, `libreriaOnlineV2` |
| 🛡️ | **Sicurezza Informatica** | CyberSecurity, Vulnerabilità, Difesa e Misure di protezione | `Fondamenti-Di-CyberSecurity`, Bibliografia |
| 🥽 | **Sicurezza Sul Lavoro** | Normativa D.Lgs 81/08, prevenzione e sicurezza nei luoghi di lavoro | Materiale formativo |
| 🖥️ | **Sistemi di Virtualizzazione** | Hypervisor, Docker, Microservizi, Nginx e PostgreSQL | `09-07-2026` (`nginx-main`, `postgres-main`) |
| 🤝 | **Soft Skills & Agile** | Comunicazione efficace, Time Management, Colloquio, Framework Scrum/Agile | `Moduli_Agile`, Presentazioni |
| 🎓 | **Borsa di Studio** | Documenti e allegati amministrativi personali | `Allegato_2_Tarallo.pdf`, `Allegato_3_Tarallo.pdf` |

---

## 🔍 Dettaglio Strutturale per Materia

<!-- markdownlint-disable MD033 -->
<details open>
<summary><b>☁️ Amazon Web Services (AWS)</b></summary>

| Data Lezione | Laboratorio | Note & Contenuti |
| :--- | :--- | :--- |
| **06-10-2026** | `lab01-networking` | Basi di Networking: IP, DNS, ping e percorsi di rete (`configurazione.txt`, `consegna01.md`). |
| **09-10-2026** | `lab02-wifi-vpn` | Wireless & VPN: Analisi del traffico di rete con e senza tunneling VPN. |
| **14-10-2026** | `lab03-protocolli` | Protocolli Server: Ispezione pacchetti HTTP/HTTPS, log di sistema ed evidenze. |
| **15-10-2026** | `lab04-cloud` | Cloud Storage & S3: Versionamento dei file, backup, download e ripristino dati. |
| **22-10-2026** | `lab05-servizi` | Infrastructure as Code (IaC): Architettura cloud scalabile e provisioning via Terraform. |

</details>

<details open>
<summary><b>⚡ C# / .NET</b></summary>

| Data Lezione | Progetti / Moduli | Argomenti Implementati |
| :--- | :--- | :--- |
| **16-03-2026** | `Benvenuto`, `Cerchio`, `DivisioneDueInteri`, `FatturaAzienda`, `FatturaLiberaProfessione`, `NumeriReali`, `PrezzoQuantitàSconto`, `Quadrato`, `SommaDueInteri`, `Transazione` | Sintassi base, operazioni aritmetiche, I/O da console e calcolo fatture. |
| **25-03-2026** | `ArrayDiNumeriReali`, `ArrayDiStringa`, `ArrayRicercaNumeriRandom`, `Dado`, `EstrazioneNumeroRuotaLotto`, `EtàMedia`, `MaxNInteri`, `MediaNInteri`, `NumeroCasuale`, `PariDispari`, `Stampa100NPariPositivi`, `Triangolo` | Strutture di controllo (cicli, selezioni), gestione Array e generazione numeri casuali. |
| **30-03-2026** | `ArrayParalleli`, `ClasseCerchio`, `ClasseQuadrato`, `ClasseRettangolo`, `ClasseTriangolo` | Array paralleli e prima introduzione alla programmazione ad oggetti (classi geometriche). |
| **07-04-2026** | `ClasseEmail`, `ClasseProdotto` | Incapsulamento, proprietà (get/set), Tipi Enumerati (`Priorità`) e calcolo sconti/imponibili. |
| **08-04-2026** | `ClasseAuto`, `ClasseHardDisk`, `ClassePersona`, `LibroAutoriEditore`, `Rubrica` | Concetti avanzati OOP: composizione, relazioni 1:N tra oggetti e **Diagramma UML delle Classi** (`Diagram1.cd`). |
| **27-04-2026** | `ClasseTesseraSanitaria` | Modellazione e validazione dati anagrafici e sanitari. |
| **30-04-2026** | `EsercizioSolidi` | Calcoli volumetrici ed ereditarietà/modelli geometrici 3D. |

</details>

<details>
<summary><b>🐍 Python</b></summary>

| Data / Modulo | Sottocartelle / Moduli | Argomenti Trattati |
| :--- | :--- | :--- |
| **10-09-2026** / **14-09-2026** | `Iterazione - Testo Esercizi`, `Selezione - Testo Esercizi` | Strutture condizionali (if/else) ed iterative (cicli for/while). |
| **21-09-2026** / **22-09-2026** | `EserciziFunzioni`, `EserciziListe`, `EserciziStringhe` | Definizione di funzioni, manipolazione di stringhe e gestione liste. |
| **30-09-2026** / **06-10-2026** | `EserciziTuple`, `EserciziDizionari` | Strutture dati avanzate: Tuple immutabili e Dizionari chiave-valore. |
| **Esercizi_OOP_e_Files** | `01_Classi_OOP`, `02_Ereditarieta`, `03_Polimorfismo_Import`, `Esercizi_Files` | Programmazione ad Oggetti in Python, ereditarietà, polimorfismo, import moduli e I/O su file. |

</details>

<details>
<summary><b>🌐 RESTFul API & Backend</b></summary>

| Modulo | Progetto | Note Tecniche |
| :--- | :--- | :--- |
| `RESTFul_API` | `libreriaOnline`, `libreriaOnlineV2` | Architettura Web API Node.js/Express con database SQLite3 per la gestione di un catalogo libri. |

</details>

<details>
<summary><b>🖥️ Sistemi di Virtualizzazione & Microservizi</b></summary>

| Modulo / Data | Laboratori | Tecnologie & Architetture |
| :--- | :--- | :--- |
| **09-07-2026** | `nginx-main`, `postgres-main` | Orchestrazione microservizi, Reverse Proxy Nginx, bilanciamento API e database PostgreSQL. |

</details>

<details>
<summary><b>🤝 Soft Skills, Agile & Scrum</b></summary>

| Modulo | Contenuti Principali |
| :--- | :--- |
| `Moduli_Agile` | Guida Scrum 2020, ruoli Product Owner (PO), Scrum Master (SM), Scrum Team e Scaling. |
| `Soft Skills` | Comunicazione efficace, Time Management, gestione delle crisi, lettera di presentazione e preparazione colloquio. |

</details>

---

## ⚙️ Regole di Gestione Repository (`.gitignore`)

Per mantenere il repository pulito e conforme agli standard:

* 🛑 **Node.js**: Cartella `node_modules/` esclusa dal tracciamento Git.
* 🛑 **Build & Temp C#**: Cartelle `.vs/`, `bin/` e `obj/` escluse.
* 🛑 **Terraform**: Cartelle `.terraform/` e file di stato `*.tfstate` esclusi.

---

## 🚀 Stato Repository

* **Remote**: `https://github.com/ohTara/Materie_ITS.git`
* **Branch**: `main`
* **Stato**: 🟢 *Sincronizzato e Mappato al 100%*

<!-- markdownlint-enable MD033 -->
