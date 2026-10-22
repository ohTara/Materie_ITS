# 📚 Corso ITS Cloud Specialist — Mappa Completa Repository

![Branch](https://img.shields.io/badge/Branch-main-blue?style=flat-square&logo=git)
![Status](https://img.shields.io/badge/Status-Attivo-brightgreen?style=flat-square)
![Repo](https://img.shields.io/badge/Repo-Materie__ITS-orange?style=flat-square&logo=github)

> Repository centrale per l'organizzazione, il tracciamento e la sincronizzazione di tutti i moduli didattici, laboratori pratici, API REST, progetti C# e documentazione del corso **Cloud Specialist**.

---

## 🗺️ Panoramica Generale delle Materie

| Icona | Modulo / Materia | Argomenti & Focus Didattico | Sottocartelle & Moduli |
| :---: | :--- | :--- | :--- |
| ☁️ | **Amazon Web Services (AWS)** | Cloud Infrastructure, Networking, VPN, Protocolli Web, S3 e IaC con Terraform | `lab01-networking` ➔ `lab05-servizi` |
| 🌐 | **RESTFul API** | Web API Node.js/Express, architettura REST, database SQLite3 | `libreriaOnlineV2` |
| ⚡ | **C# / .NET** | Object Oriented Programming (OOP), incapsulamento, associazioni e diagrammi UML | `07-04-2026`, `08-04-2026` |
| 🎓 | **Borsa di Studio** | Documenti e allegati amministrativi | `Allegato_2_Tarallo.pdf`, `Allegato_3_Tarallo.pdf` |

---

## 🔍 Struttura Dettagliata per Materia

### ☁️ Amazon Web Services (AWS) — Reti, Cloud & IaC

| Data Lezione | Modulo / Laboratorio | File Rilevati | Note & Argomenti Trattati |
| :--- | :--- | :--- | :--- |
| **06-10-2026** | `lab01-networking` | `configurazione.txt`, `dns.txt`, `ping-gateway.txt`, `ping-internet.txt`, `percorso.txt`, `consegna01.md` | **Networking Fundamentals**: Analisi IP, gateway predefinito, risoluzione DNS e percorsi di rete. |
| **09-10-2026** | `lab02-wifi-vpn` | `wifi.txt`, `schema-wifi.md`, `configurazione-senza-vpn.txt`, `configurazione-attuale.txt`, `caso-vpn-sintetico.md`, `consegna02.md` | **Wireless & Tunneling VPN**: Analisi del traffico con e senza VPN, sicurezza Wi-Fi e routing. |
| **14-10-2026** | `lab03-protocolli` | `sito/messaggio.txt`, `evidenze/log-server.txt`, `cleanup.txt`, evidenze `p1`–`p7`, `consegna03.md` | **Protocolli Web & Server Log**: Ispezione pacchetti HTTP/HTTPS, gestione log del server e tracciamento ticket. |
| **15-10-2026** | `lab04-cloud` | `originale-v1/`, `originale-v2/`, `scaricato-v1/`, `scaricato-v2/`, `ripristinato/`, `consegna04.md` | **Cloud Storage & Versioning**: Test di backup, versionamento dei dati e procedure di ripristino su S3/Cloud. |
| **22-10-2026** | `lab05-servizi` | `architettura05.md`, `consegna05.md` | **IaC & Provisioning AWS**: Architettura dei servizi cloud scalabili e automazione con Terraform. |

### 🌐 RESTFul API — Web Services & Backend Node.js

| Sottocartella / Progetto | Tecnologie Rilevate | Note & Argomenti Trattati |
| :--- | :--- | :--- |
| `libreriaOnlineV2` | Node.js, Express, SQLite3 (`node-sqlite3`), Nodemon | **Web API Libreria Online**: Sviluppo di endpoint RESTful, operazioni CRUD, integrazione database SQLite e gestione middleware. |

### ⚡ C# / .NET — Programmazione ad Oggetti (OOP)

| Data Lezione | Progetto / Soluzione | File Sorgente Principali | Argomenti & Concetti Implementati |
| :--- | :--- | :--- | :--- |
| **07-04-2026** | `ClasseEmail` | `Program.cs`, `Email.cs`, `Priorità.cs`, `ClasseEmail.csproj` | **Encapsulation & Enum**: Modellazione email, attributi privati, enum `Priorità` e metodi accessor. |
| **07-04-2026** | `ClasseProdotto` | `Program.cs`, `Prodotto.cs`, `ClasseProdotto.csproj` | **Property & Logic**: Calcolo sconti, prezzi imponibili/ivati e gestione stato prodotto. |
| **08-04-2026** | `ClasseAuto` | `Program.cs`, `Auto.cs`, `TipoCarburante.cs`, `ClasseAuto.csproj` | **Domain Modeling**: Modellazione veicoli e gestione del carburante tramite tipi enumerati. |
| **08-04-2026** | `ClasseHardDisk` | `Program.cs`, `HardDisk.cs`, `ClasseHardDisk.csproj` | **Hardware Emulation**: Gestione capacità, memoria residua e operazioni di lettura/scrittura. |
| **08-04-2026** | `ClassePersona` | `Program.cs`, `Persona.cs`, `TipoSesso.cs`, `ClassePersona.csproj` | **Anagrafica**: Metodi di formattazione output, validazione campi e tipi enumerati. |
| **08-04-2026** | `LibroAutoriEditore` | `Program.cs`, `Libro.cs`, `Autore.cs`, `Editore.cs`, `Indirizzo.cs` | **Composizione & Relazioni**: Modellazione di domini complessi con relazioni 1:N e N:M tra oggetti. |
| **08-04-2026** | `Rubrica` | `Program.cs`, `Contatto.cs`, `Indirizzo.cs`, `Diagram1.cd` | **Visual Modeling (UML)**: Gestione contatti in memoria con diagramma delle classi integrato (`Diagram1.cd`). |

### 🎓 Borsa di Studio & Documenti Amministrativi

| File | Descrizione |
| :--- | :--- |
| `Borsa_di_studi/Allegato_2_Tarallo.pdf` | Documento di candidatura e dichiarazione (Allegato 2) |
| `Borsa_di_studi/Allegato_3_Tarallo.pdf` | Documento di candidatura e integrazione (Allegato 3) |

---

## ⚙️ Regole di Gestione Repository (`.gitignore`)

Per garantire un repository snello, sicuro e conforme agli standard di sviluppo software:

* 🛑 **Node.js / Dependencies**: La cartella `node_modules/` è esclusa da Git per prevenire il caricamento di migliaia di pacchetti terzi.
* 🛑 **Build & Intermediate Files**: Cartelle temporanee `.vs/`, `bin/` e `obj/` escluse.
* 🛑 **Terraform State**: File `*.tfstate`, `.terraform/` ed eseguibili `.exe` esclusi per sicurezza.
* 🟢 **Branch Principale**: `main` costantemente sincronizzato con `origin/main`.

---

## 🚀 Stato della Sincronizzazione

* **Remote Repository**: `https://github.com/ohTara/Materie_ITS.git`
* **Branch Attivo**: `main`
* **Stato Working Tree**: 🟢 *Allineato e tracciato al 100%*