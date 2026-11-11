# Project Work — Omnia System (submodule Git)

**Collegamento nella repo:** `modulo-omnia-system` → `https://github.com/ohTara/Project-Work---Omnia-System.git` (dichiarato in `.gitmodules`).

## Cos'è un submodule (da ricordare)
Un **submodule** è una repo dentro un'altra repo: la repo principale non contiene i file, ma solo un puntatore a un **commit preciso** della repo collegata. Per questo lo ZIP scaricato da GitHub **non include** la cartella `modulo-omnia-system`, e questa documentazione non ha potuto leggerne i file.

Comandi utili:
```bash
git clone --recurse-submodules https://github.com/ohTara/Materie_ITS.git   # clone completo
git submodule update --init --recursive                                    # su un clone già fatto
git submodule update --remote modulo-omnia-system                          # aggiorna al commit più recente del modulo
```
Dopo l'aggiornamento il puntatore va committato nella repo principale.

## Il progetto (descrizione di alto livello — **non verificata sui file**)
"Costruisci, Attacca e Difendi una Web App": infrastruttura di Cloud Security/DevSecOps su Azure con tre VM — **OWASP Juice Shop** come bersaglio, **Nginx + ModSecurity (WAF)** come reverse proxy e uno stack **Wazuh (SIEM)** — creata con **Terraform**, configurata con **Ansible** e validata da **GitHub Actions** (`devsecops.yml`: validazione Terraform e scansione SAST con **Checkov**).

## Collegamenti con il resto del corso
Terraform e `azurerm` (vedi *Terraform su Azure*), pipeline CI/CD, reverse proxy Nginx (vedi lab Nginx), sicurezza e crittografia (materia Sicurezza informatica).

## Per documentarlo bene
Carica lo ZIP della repo `Project-Work---Omnia-System` (senza `.terraform/`, `*.tfstate`, `.env`): produco lo stesso tipo di documento per lezione/fase.
