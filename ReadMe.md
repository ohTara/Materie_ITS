# 📚 Materie ITS - Cloud Specialist

Repository centrale per la gestione, la conservazione e la sincronizzazione del materiale didattico, dei progetti e dei laboratori del corso **Cloud Specialist**.

---

## 📌 Indice delle Materie e dei Contenuti

Il repository organizza i moduli didattici e i relativi laboratori prattici:

* ☁️ **Amazon Web Services (AWS)**: Configurazione e deployment dei servizi cloud (inclusi i file di lavoro ed esercizi `lab05-servizi`).
* 🔷 **Azure**: Progetti, esercizi e librerie dedicate ai servizi Microsoft Azure.
* 🐍 **Python**: Script, esercitazioni pratiche e moduli di programmazione.
* 🖥️ **Virtualizzazione**: Dispense, documentazione tecnica e guide sull'infrastruttura virtuale.
* ⚡ **C# / .NET**: Progetti applicativi, esercizi di ripasso e basi di programmazione C#.

---

## 🛠️ Note Tecniche e Manutenzione Repository

### 🛑 Regole di Esclusione (`.gitignore`)

Per evitare problemi di push su GitHub e superamento del limite dei file di grandi dimensioni (100MB), la configurazione del repository esclude automaticamente:

- **Terraform Binaries**: `.terraform/` e file eseguibili (`*.exe`) relativi ai provider Terraform.
- **Terraform State Files**: `*.tfstate` e `*.tfstate.backup` per preservare la sicurezza e prevenire conflitti.
- **Node Modules / Dependencies**: `node_modules/` e dipendenze pesanti.

### 🧹 Risoluzione Conflitti e File Bloccati (Windows)

Se durante la pulizia o la cancellazione di vecchie cartelle locali su Windows si presentano errori del tipo `Device or resource busy` (dovuti a handle di sistema attivi su cartelle come `lab05-servizi`), eseguire il seguente comando in **PowerShell**:

```powershell
Remove-Item -Path "C:\Users\luca.tarallo\Desktop\Materie_ItS" -Recurse -Force -ErrorAction SilentlyContinue
