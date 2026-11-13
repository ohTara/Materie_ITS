# Project Work — Omnia System (submodule Git)

**Cartella:** `modulo-omnia-system/` → `https://github.com/ohTara/Project-Work---Omnia-System.git` (dichiarato in `.gitmodules`) · **Periodo:** novembre 2026 · **Committente:** AizoOn / ITS ICT Piemonte · lavoro di gruppo.
**Fonte:** file della repo collegata, letti il 13/11/2026.

## Obiettivo
"Costruisci, Attacca e Difendi una Web App su Azure": creare l'infrastruttura come codice, attaccare un'applicazione volutamente vulnerabile (Red Team) e poi bloccare e rilevare l'attacco (Blue Team).

## Architettura
Resource Group `rg-lab-cloudsec-devsecops` in `westeurope`, VNet `10.0.0.0/16`, subnet `snet-workload` `10.0.1.0/24`, NSG `nsg-lab-sec`, tre VM Ubuntu 22.04 `Standard_B2s` (utente `azureuser`).

| VM | IP privato | Ruolo | Software |
|---|---|---|---|
| `vm-target` | 10.0.1.10 | bersaglio | OWASP Juice Shop in Docker, porta 3000 |
| `vm-waf` | 10.0.1.20 | reverse proxy | Nginx + ModSecurity + OWASP CRS, porta 80 → `10.0.1.10:3000` |
| `vm-siem` | 10.0.1.30 | SOC | Wazuh single-node (Manager, Indexer, Dashboard) |

## Come è stato risolto
1. **Terraform** (`terraform/`): `main.tf` per rete e NSG, `vms.tf` crea IP pubblici, NIC e VM con un solo blocco e `for_each` su `local.vms` (mappa nome → IP privato), `output.tf` restituisce gli IP pubblici.
2. **Checkov**: scansione statica di `terraform/` e `ansible/` prima del deploy; i controlli falliti e accettati sono motivati in `docs/documentazione_tecnica_cloud_devsecops.md`.
3. **Ansible** (`ansible/site.yml`): ruolo `common` su tutte le VM (apt, Docker), poi `target`, `waf` e `siem` sui rispettivi gruppi dell'inventory.
4. **WAF**: `roles/waf/files/default.conf` attiva ModSecurity e fa da proxy verso il target; una richiesta bloccata restituisce HTTP 403.
5. **SIEM**: `roles/siem/files/custom_rules.xml` con le regole 100001 (SQL Injection segnalata da ModSecurity, MITRE T1190) e 100002 (richieste a `/rest/user/login`).
6. **CI** (`.github/workflows/devsecops.yml`): `terraform validate` e Checkov a ogni push e pull request.
7. **Collaudo** (`scripts/validate_network.sh`): ping, Juice Shop 200, proxy WAF 200, SQL Injection → 403.

## Concetti da ricordare
- **Submodule:** la repo principale contiene solo un puntatore a un commit della repo collegata. Lo ZIP di GitHub non include la cartella.
  ```bash
  git clone --recurse-submodules https://github.com/ohTara/Materie_ITS.git   # clone completo
  git submodule update --init --recursive                                    # su un clone già fatto
  git submodule update --remote modulo-omnia-system                          # porta il puntatore all'ultimo commit
  ```
  Dopo l'aggiornamento il nuovo puntatore va committato nella repo principale.
- **`for_each`:** una sola definizione di risorsa per N oggetti, indirizzati per chiave (`azurerm_linux_virtual_machine.vm["vm-waf"]`).
- **Defense in depth:** NSG a livello di rete, WAF a livello applicativo, SIEM per vedere ciò che passa comunque.
- **Shift left:** Checkov trova le misconfigurazioni nel codice, prima che l'infrastruttura esista.
- **Reverse proxy:** il client parla solo con il WAF; il target non è esposto direttamente.

## Da verificare / attenzione
- Il puntatore del submodule è fermo a un commit precedente all'ultimo `main` della repo collegata.
- L'inoltro dei log di WAF e Juice Shop a Wazuh (agente) non è ancora automatizzato nei ruoli Ansible.

## Collegamenti con il resto del corso
Terraform e `azurerm` (vedi *Terraform su Azure*), reverse proxy Nginx (vedi lab Nginx di Virtualizzazione), container (lab AWS 06–07), sicurezza e SQL Injection (Sicurezza informatica), pipeline CI/CD.

## Domande di richiamo
1. Perché il Red Team non deve poter raggiungere direttamente la porta 3000 del target?
2. Che differenza c'è tra ciò che fa il WAF e ciò che fa il SIEM davanti a una SQL Injection?
3. Perché Checkov viene eseguito prima di `terraform apply` e non dopo?

<details><summary>Risposte</summary>

1. Perché aggirerebbe il WAF: la difesa funziona solo se tutto il traffico web passa dal reverse proxy.
2. Il WAF blocca la richiesta (prevenzione); il SIEM la registra e genera un alert (rilevamento), utile anche per gli attacchi che il WAF non ferma.
3. Perché correggere una riga di codice costa meno che correggere un'infrastruttura già esposta.
</details>
