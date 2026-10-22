# 📚 Materie ITS — Cloud Specialist

> Repository ufficiale per la raccolta, l'organizzazione e la sincronizzazione del materiale didattico, dei progetti e dei laboratori pratici.

---

## 🛠️ Moduli Didattici

| Modulo | Descrizione & Focus | Argomenti Principali |
| :--- | :--- | :--- |
| **☁️ AWS** | Amazon Web Services & Infrastructure | EC2, S3, IAM, `lab05-servizi`, Cloud Management |
| **🔷 Azure** | Microsoft Azure Cloud Services | Resource Groups, Virtual Networks, App Services |
| **🐍 Python** | Scripting & Automazione | Sintassi, scripting di sistema, esercizi pratici |
| **🖥️ Virtualizzazione** | Infrastrutture & Hypervisor | Concetti base/avanzati, gestione VM, Networking |
| **⚡ C# / .NET** | Programmazione Orientata agli Oggetti | Basi di C#, sviluppo applicativo, esercitazioni |

---

## ⚙️ Configurazione & Politiche Git

### 🛑 Regole `.gitignore`
Per garantire prestazioni ottimali e rispettare i limiti di GitHub (**100 MB max per file**), il repository esclude automaticamente:

* **Terraform Binaries & Cache**: Cartelle `.terraform/` ed eseguibili `*.exe`
* **Terraform State Files**: Files di stato `*.tfstate` e `*.tfstate.backup`
* **Dipendenze e Build**: Cartelle di output e pacchetti (`node_modules/`, `bin/`, `obj/`)

---

## 🧹 Procedure di Manutenzione (Windows)

In caso di file bloccati da processi di sistema (*Device or resource busy*) durante le pulizie locali, eseguire in PowerShell:

```powershell
Remove-Item -Path "C:\Users\luca.tarallo\Desktop\Materie_ItS" -Recurse -Force -ErrorAction SilentlyContinue
