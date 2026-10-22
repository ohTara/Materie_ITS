# 📚 Corso ITS Cloud Specialist — Mappa Completa Repository

![Branch](https://img.shields.io/badge/Branch-main-blue?style=flat-square&logo=git)
![Status](https://img.shields.io/badge/Status-Sincronizzato-brightgreen?style=flat-square)
![Repo](https://img.shields.io/badge/Repo-Materie__ITS-orange?style=flat-square&logo=github)

> Mappatura dettagliata ed esaustiva di tutti i moduli didattici, argomenti, esercitazioni e laboratori pratici caricati nel repository.

---

## 🗺️ Indice Generale delle Materie e dei Moduli

| Icona | Modulo / Materia | Argomenti Principali & Focus | Tipologia Contenuto |
| :---: | :--- | :--- | :--- |
| ☁️ | **Amazon Web Services (AWS)** | Cloud Infrastructure, IAM, EC2, S3, Provisioning con Terraform (`lab05-servizi`) | 🧪 Laboratori & Config |
| 🔷 | **Microsoft Azure** | Resource Groups, Virtual Networks, App Services, Portale Azure | 🧪 Esercitazioni Cloud |
| 🐍 | **Python** | Sintassi di base/avanzata, scripting di sistema, automazione e strutture dati | 🐍 Script & Esercizi |
| 🖥️ | **Virtualizzazione** | Architetture Hypervisor, gestione Macchine Virtuali, Reti Virtuali | 🖥️ Teoria & Pratica |
| ⚡ | **C# / .NET** | Programmazione Orientata agli Oggetti (OOP), sintassi C#, sviluppo applicativo | 💻 Codice & Progetti |

---

## 🔍 Dettaglio Analitico per Materia

<!-- markdownlint-disable MD033 -->
<details open>
<summary><b>☁️ Amazon Web Services (AWS)</b></summary>

| Sottocartella / Laboratorio | Contenuti Rilevati | Argomenti & Attività |
| :--- | :--- | :--- |
| `lab05-servizi` | File `.tf`, configurazioni provider | 🧪 Deploy e gestione servizi AWS via Terraform |
| `Materiale_AWS` | Dispense, schemi di rete, guide | 📄 Teoria su VPC, IAM, EC2 e Storage S3 |

</details>

<details open>
<summary><b>🔷 Microsoft Azure</b></summary>

| Sottocartella / Laboratorio | Contenuti Rilevati | Argomenti & Attività |
| :--- | :--- | :--- |
| `Esercitazioni_Azure` | Template ARM/Bicep, script CLI | 🧪 Creazione Resource Group e VNet |

</details>

<details open>
<summary><b>🐍 Python</b></summary>

| Sottocartella / Laboratorio | Contenuti Rilevati | Argomenti & Attività |
| :--- | :--- | :--- |
| `Esercizi_Python` | File `.py`, notebook | 🐍 Fondamenti, funzioni, manipolazione file e automazione |

</details>

<details open>
<summary><b>🖥️ Virtualizzazione</b></summary>

| Sottocartella / Laboratorio | Contenuti Rilevati | Argomenti & Attività |
| :--- | :--- | :--- |
| `Lab_Virtualizzazione` | Dispense PDF, file di configurazione | 🖥️ Setup Hypervisor, switch virtuali e VM |

</details>

<details open>
<summary><b>⚡ C# / .NET</b></summary>

| Sottocartella / Laboratorio | Contenuti Rilevati | Argomenti & Attività |
| :--- | :--- | :--- |
| `Progetti_CS` | Solution `.sln`, file `.cs` | 💻 Programmazione OOP, classi, ereditarietà e console app |

</details>

<!-- markdownlint-enable MD033 -->

---

## ⚙️ Regole di Gestione Repository & `.gitignore`

Per mantenere il repository pulito e rispettare i limiti di GitHub (**100 MB max per file**), la configurazione esclude automaticamente:

- 🛑 **Terraform Binaries & State**: Cartelle `.terraform/`, file `*.tfstate` ed `.exe` dei provider.
- 📦 **Build & Artifacts**: Cartelle `bin/`, `obj/` e dipendenze pesanti (`node_modules/`).

---

## 🚀 Stato e Sincronizzazione

- **Branch principale**: `main`
- **Remote**: `origin/main` (`https://github.com/ohTara/Materie_ITS.git`)
- **Stato Working Directory**: 🟢 *Pulita e sincronizzata*