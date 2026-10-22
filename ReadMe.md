# 📚 Corso ITS Cloud Specialist — Mappa Completa Repository

![Branch](https://img.shields.io/badge/Branch-main-blue?style=flat-square&logo=git)
![Status](https://img.shields.io/badge/Status-Attivo-brightgreen?style=flat-square)
![Repo](https://img.shields.io/badge/Repo-Materie__ITS-orange?style=flat-square&logo=github)

> Repository centrale per l'organizzazione, il tracciamento e la sincronizzazione di tutti i moduli didattici, laboratori pratici, dispense e documenti del corso **Cloud Specialist**.

---

## 🗺️ Panoramica Generale dei Moduli Didattici

| Icona | Modulo / Materia | Argomenti & Focus Didattico | Laboratori & Moduli Presenti |
| :---: | :--- | :--- | :--- |
| ☁️ | **Amazon Web Services (AWS)** | Fundamentals Cloud, Reti, VPN, Protocolli Web, S3, Provisioning Infrastructure as Code | `lab01-networking`, `lab02-wifi-vpn`, `lab03-protocolli`, `lab04-cloud`, `lab05-servizi` |
| ⚡ | **C# / .NET** | Object Oriented Programming (OOP), Incapsulamento, Classi, Modelli e Strutture Dati | `ClasseEmail`, `ClasseProdotto`, `ClasseAuto`, `ClasseHardDisk`, `ClassePersona`, `LibroAutoriEditore`, `Rubrica` |
| 🎓 | **Borsa di Studio** | Documentazione e allegati amministrativi | `Allegato_2_Tarallo.pdf`, `Allegato_3_Tarallo.pdf` |

---

## 🔍 Dettaglio Cronologico ed Analitico per Materia

### ☁️ Amazon Web Services (AWS) — Reti & Cloud Infrastructure

| Data Lezione | Modulo / Laboratorio | Contenuti & File Rilevati | Note & Argomenti Trattati |
| :--- | :--- | :--- | :--- |
| **06-10-2026** | `lab01-networking` | `configurazione.txt`, `dns.txt`, `ping-gateway.txt`, `ping-internet.txt`, `percorso.txt`, `consegna01.md` | **Basi di Networking**: Analisi indirizzamento IP, test di connettività, gateway predefinito e risoluzione DNS. |
| **09-10-2026** | `lab02-wifi-vpn` | `wifi.txt`, `schema-wifi.md`, `configurazione-senza-vpn.txt`, `configurazione-attuale.txt`, `caso-vpn-sintetico.md`, `consegna02.md` | **Wireless & Tunneling VPN**: Analisi del traffico di rete con e senza VPN, routing e sicurezza Wi-Fi. |
| **14-10-2026** | `lab03-protocolli` | `sito/messaggio.txt`, `evidenze/log-server.txt`, `cleanup.txt`, evidenze p1–p7, `consegna03.md` | **Protocolli di Rete & Server**: Analisi log, ispezione pacchetti, gestione ticket ed evidenze di ripristino servizio. |
| **15-10-2026** | `lab04-cloud` | `originale-v1/`, `originale-v2/`, `scaricato-v1/`, `scaricato-v2/`, `ripristinato/`, `consegna04.md` | **Storage & Versioning Cloud**: Test di backup, versionamento dati, scaricamento e ripristino report in ambiente cloud. |
| **22-10-2026** | `lab05-servizi` | `architettura05.md`, `consegna05.md` | **Servizi AWS & IaC**: Architettura dei servizi cloud scalabili e provisioning dell'infrastruttura. |

### ⚡ C# / .NET — Programmazione ad Oggetti (OOP)

| Data / Modulo | Progetto / Soluzione | File Sorgente Principali | Argomenti & Concetti Implementati |
| :--- | :--- | :--- | :--- |
| **07-04-2026** | `ClasseEmail` | `Program.cs`, `Email.cs`, `Priorità.cs`, `ClasseEmail.csproj` | Gestione messaggi, incapsulamento, enumerazioni (`Priorità`) e costruttori. |
| **07-04-2026** | `ClasseProdotto` | `Program.cs`, `Prodotto.cs`, `ClasseProdotto.csproj` | Modellazione entità Prodotto, proprietà get/set, calcolo prezzi e sconti. |
| **08-04-2026** | `ClasseAuto` | `Program.cs`, `Auto.cs`, `TipoCarburante.cs`, `ClasseAuto.csproj` | Modellazione veicoli, gestione stato, tipo di carburante (enum) e metodi. |
| **08-04-2026** | `ClasseHardDisk` | `Program.cs`, `HardDisk.cs`, `ClasseHardDisk.csproj` | Modellazione componenti hardware, capacità, spazio disponibile e gestione lettura/scrittura. |
| **08-04-2026** | `ClassePersona` | `Program.cs`, `Persona.cs`, `TipoSesso.cs`, `ClassePersona.csproj` | Gestione dati anagrafici, metodi di formattazione output e tipi enumerati. |
| **08-04-2026** | `LibroAutoriEditore` | `Program.cs`, `Libro.cs`, `Autore.cs`, `Editore.cs`, `Indirizzo.cs` | **Associazione & Composizione**: Relazioni avanzate tra oggetti legati a libri, autori ed editori. |
| **08-04-2026** | `Rubrica` | `Program.cs`, `Contatto.cs`, `Indirizzo.cs`, `Diagram1.cd` | **Diagramma delle Classi**: Gestione contatti con supporto visuale alle relazioni tra oggetti (`Diagram1.cd`). |

### 🎓 Borsa di Studio & Documentazione Personale

| File | Descrizione |
| :--- | :--- |
| `Borsa_di_studi/Allegato_2_Tarallo.pdf` | Documento amministrativo allegato 2 |
| `Borsa_di_studi/Allegato_3_Tarallo.pdf` | Documento amministrativo allegato 3 |

---

## ⚙️ Regole di Gestione Repository & Pulizia Git

Per garantire un repository snello e sicuro conforme agli standard di sviluppo:

* 🛑 **Artifacts di Build C#**: Cartelle temporanee `.vs/`, file `bin/` e `obj/` dovrebbero essere esclusi tramite `.gitignore` per non appesantire il tracciamento di Git.
* 🛑 **Terraform State & Binaries**: Esclusione automatica di `.terraform/`, `*.tfstate` ed eseguibili `*.exe`.
* 🟢 **Branch Principale**: `main` costantemente sincronizzato con `origin/main`.

---

## 🚀 Stato della Sincronizzazione

* **Remote URL**: `https://github.com/ohTara/Materie_ITS.git`
* **Branch**: `main`
* **Stato**: 🟢 *Allineato e tracciato al 100%*
