# 📚 Materie ITS - Cloud Specialist

Repository ufficiale e centralizzata per il corso **ITS Cloud Specialist**. Raccoglie materiale didattico, dispense PDF, script di laboratorio, progetti IaC, esercitazioni di programmazione e collezioni di test per tutti i moduli del percorso formativo.

---

## 🛠️ Struttura della Repository

```
Materie_ITS_nuovo/
├── ☁️ Amazon Web Services (AWS)/            # Lab pratici (Lab01-07), networking, servizi cloud e slide
├── 📊 Borsa_di_studi/                       # Documentazione e pratiche amministrative
├── 💻 C#/                                  # Programmazione OOP, raccolte esercizi (2026) e modelli C#
├── 🤖 Cloud_Specialist/                     # GCP Demo Sage (RAG con Firestore Vector Search & Vertex AI)
├── 🐳 Containers_ITS-ICT/                  # Docker, containerizzazione e orchestrazione
├── ⚖️ Copyright_e_norme_giuridiche/         # Diritto digitale, privacy e normativa IT
├── 📈 Data_Analytics_e_Visualization/       # Analisi dati, query ed esercitazioni di visualizzazione
├── 📋 docs/                                 # Documentazione di dettaglio organizzata per materia
├── 🗄️ Fondamenti_di_Base_Dati/               # Modelli concettuali/logici, script SQL, backup ed esercizi
├── ⚡ Fondamenti_di_programmazione/         # Logica di programmazione, algoritmi e file C
├── 🌐 Fondamenti_di_Reti/                   # Architetture di rete, subnetting, VPN e protocolli
├── 🔀 Fondamenti_Version_Control/           # Git, branch management ed esercitazioni workflow
├── 🇬🇧 Inglese/                             # Materiale per l'apprendimento dell'inglese tecnico
├── 📡 IoT/                                  # Internet of Things, sensori e materiale d'esame intermedio
├── 🐧 Linux_Server/                         # Amministrazione di sistema Linux e script bash
├── ☁️ Microsoft_Azure/                      # Slide delle lezioni e provisioning IaC con Terraform
├── 📦 Microsoft_365_(Office)/               # Strumenti di produttività M365
├── ⚙️ modulo-omnia-system/                  # Modulo per l'automazione infrastrutturale (Ansible, Terraform, Workflows)
├── ⚖️ Pari_Opportunità/                    # Documentazione tematica e moduli formativi
├── 📮 postman/                              # Collections ed ambienti di test per API REST
├── 🐍 Python/                               # Script Python, esercizi OOP, OS module e progetti (Gioco_Python)
├── 🌐 RESTFul_API/                          # Progetti Web API in Node.js (libreriaOnline, libreriaOnlineV2)
├── 🔒 Sicurezza_informatica/                # Fundamentals di Cybersecurity, analisi delle minacce e report
├── 🦺 Sicurezza_Sul_Lavoro/                 # Formazione e certificazioni sulla sicurezza nei luoghi di lavoro
├── 🖥️ Sistemi di Virtualizzazione/          # Ambienti virtualizzati, stack Nginx e PostgreSQL
└── 🤝 Soft_Skill/                           # Moduli su metodologia Agile, lavoro di squadra e comunicazione
```

---

## ✨ Ultimi Aggiornamenti e Moduli Highlight

* **AWS (Amazon Web Services)**: Aggiornati i laboratori pratici da `lab01-networking` a `lab07-windows`, inclusi schemi di rete, configurazioni cloud e lezioni in formato PDF.
* **Cloud Specialist (GCP Sage RAG)**: Sviluppo del motore RAG con Firestore Vector Search e modelli di embedding reali su Vertex AI.
* **IoT (Internet of Things)**: Inseriti gli appunti di teoria e le prove d'esame intermedio.
* **Modulo Omnia System**: Integrazione di automation playbook Ansible, snippet Terraform e pipeline GitHub Actions.
* **C# & Python**: Espansione dei progetti OOP (Classi, Ereditarietà, Polimorfismo), gestione del File System e il progetto `Gioco_Python/echoes_of_the_crypt`.
* **RESTFul API**: Implementazione completa dell'architettura server Node.js per i progetti `libreriaOnline` e `libreriaOnlineV2`.

---

## 🧹 Hygiene & Regole di Tracciamento (.gitignore)

Per mantenere la repository snella, performante ed evitare la condivisione involontaria di informazioni sensibili, vengono applicate le seguenti regole:

* **Esclusione Artifacts di Build**: `node_modules/`, `.vs/`, `bin/`, `obj/`, `dist/`, `build/`, `__pycache__/`.
* **Esclusione File Temporanei e Sensibili**: File `.env`, stati locali Terraform (`.tfstate`), backup di grandi dimensioni (`*.bak`), log di esecuzione (`log.txt`).

---

## 🚀 Guida Rapida per la Sincronizzazione

```bash
# 1. Controlla lo stato dei file locali
git status

# 2. Aggiungi i file desiderati al tracciamento
git add <percorso-file-o-cartella>

# 3. Crea il commit con un messaggio descrittivo
git commit -m "feat: aggiunge nuovi esercizi e documentazione"

# 4. Invia le modifiche su GitHub
git push origin main
```

Il Project Work Omnia System è un submodule: per scaricarlo insieme alla repo usare `git clone --recurse-submodules`, oppure `git submodule update --init` su un clone già fatto.