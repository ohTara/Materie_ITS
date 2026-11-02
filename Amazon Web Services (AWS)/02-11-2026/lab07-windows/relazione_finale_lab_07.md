# Relazione Finale - Lab 07: Containerizzazione e Orchestrazione su AWS EC2

**Studente / Sigla:** CSP  
**Ambiente:** AWS EC2 (`t3.medium`, Ubuntu 26.04)  
**Tecnologie utilizzate:** Docker, K3s (Kubernetes single-node), SQLite, Bash  
**Applicazione:** Officina Ticket (Python HTTP Server)

---

## 1. Obiettivo del Laboratorio

L'obiettivo principale del laboratorio è stato validare la transizione di un'applicazione web Python ("Officina Ticket") da un ambiente di sviluppo locale ad una gestione containerizzata con Docker, fino all'orchestrazione avanzata su un cluster Kubernetes (K3s) distribuito su un'istanza AWS EC2.

Le attività svolte hanno permesso di verificare:

* Il ciclo di vita delle immagini Docker (passaggio da V1.0 a V2.0).
* La persistenza dei dati e la prevenzione della perdita d'informazioni tramite Volumi Docker e volumi persistenti (PVC) su Kubernetes.
* La resilienza dell'infrastruttura tramite l'impiego di probe di disponibilità (`readinessProbe`) e di ripristino (`livenessProbe`).

---

## 2. Sezione 1 & 2: Preparazione dell'Ambiente e Docker V1

### Attività di Preparazione e Avvio

1. **Configurazione dell'Istanza EC2 su AWS:**
   * Creazione dell'istanza `lab07-CSP` (`t3.medium`, Ubuntu 26.04).
   * Configurazione del Security Group (`lab07-CSP-sg`) con l'apertura delle porte:
     * `8080/TCP`: per l'accesso diretto ai container Docker.
     * `30080/TCP`: per l'accesso NodePort al servizio Kubernetes.

2. **Costruzione e Avvio di Officina V1.0:**
   * Creazione della rete Docker locale `officina07-net`.
   * Building dell'immagine `officina07:1.0`.
   * Avvio del container V1 senza volumi associati sulla porta 8080.

---

## 3. Sezione 3 & 4: Transizione a V2.0 e Gestione della Persistenza (Docker)

### Attività di Orchestrazione Svolte

1. **Analisi della Perdita Dati (V1 -> V2 senza volume):**
   * Aggiornamento dell'applicazione all'immagine `officina07:2.0` (caratterizzata dalla grafica viola e nuove funzionalità).
   * Verificato che, senza l'uso di volumi persistenti, l'eliminazione del container V1 comporta la perdita totale dei ticket salvati nel database SQLite interno (`/data/tickets.db`).

2. **Configurazione della Persistenza con Docker Volume:**
   * Creazione del volume gestito da Docker `officina07-data`.
   * Avvio della versione V2.0 con il montaggio del volume su `/data`:

     ```bash
     sudo docker run -d --name officina07 --network officina07-net -p 8080:8000 \
       --mount source=officina07-data,target=/data \
       -e APP_TITLE="Officina persistente - CSP" officina07:2.0
     ```

   * **Integrità dei Dati:** Verificato che fermando e riavviando i container (o passando da V2 a V1 sullo stesso volume), i ticket salvati rimangono persistenti ed accessibili.
   * **Backup Sola Lettura:** Eseguito il backup hot via SQLite API su `/tmp/tickets-backup.db` e verificato il contenuto in modalità read-only.

---

## 4. Sezione 5: Orchestrazione su Kubernetes (K3s)

### Attività di Test Svolte

1. **Installazione ed Inizializzazione Cluster K3s:**

   * Rimozione del container Docker locale per liberare la porta 8080/8000.
   * Installazione del cluster Kubernetes K3s a singolo nodo su AWS EC2.
   * Importazione dell'immagine Docker `officina07:2.0` all'interno del runtime Containerd di K3s:

     ```bash
     sudo docker save officina07:2.0 | sudo k3s ctr images import -
     ```

2. **Definizione e Applicazione del Manifesto `k8s.yaml`:**
   È stato strutturato un manifesto Kubernetes dichiarativo contenente le seguenti risorse:
   * **Namespace:** `officina07` per l'isolamento delle risorse.
   * **ConfigMap (`officina-config`):** Per la gestione centralizzata delle variabili d'ambiente (`APP_TITLE: "Officina K8s - CSP"`).
   * **PersistentVolumeClaim (`officina-pvc`):** Richiesta di storage di 1Gi gestita dinamicamente da K3s (Local Path Provisioner).
   * **Deployment (`officina-deployment`):** Gestione del Pod con probe di salute:
     * `readinessProbe`: verifica endpoint `/healthz` ogni 5s (ritardo iniziale 3s).
     * `livenessProbe`: verifica endpoint `/healthz` ogni 10s (ritardo iniziale 5s).
   * **Service (`officina-service`):** Esposizione del Deployment all'esterno tramite `NodePort` sulla porta `30080`.

3. **Verifica della Distribuzione:**
   * Applicazione del file con `kubectl apply -f k8s.yaml`.
   * L'applicazione è risultata raggiungibile all'URL `http://<IP-EC2>:30080` mostrando il titolo personalizzato dal ConfigMap.

---

## 5. Sezione 6: Test di Resilienza e Ripristino dei Guasti

### Attività Svolte

1. **Test di Sostituzione del Pod (Persistenza PVC):**
   * Eliminazione del Pod in esecuzione tramite `kubectl delete pod -l app=officina -n officina07`.
   * Kubernetes ha ricreato automaticamente un nuovo Pod per rispettare la specifica `replicas: 1` del Deployment.
   * Al riavvio, il nuovo Pod si è collegato allo stesso `officina-pvc`, confermando la totale persistenza dei ticket preesistenti.

2. **Test della Readiness Probe (Gestione Disservizi):**
   * Simulazione di un guasto interno creando un file di blocco (`/tmp/officina-not-ready`) nel Pod attivi.
   * La `readinessProbe` ha rilevato il codice HTTP 503 e Kubernetes ha temporaneamente rimosso il Pod dagli endpoint del Service (`STATUS: 0/1 READY`).
   * Rimosso il file di blocco (`rm -f /tmp/officina-not-ready`), la probe è tornata in stato di successo (`STATUS: 1/1 READY`) e il traffico web verso il browser è stato ripristinato automaticamente senza perdita dati.

---

## 6. Sezione 7: Cleanup dell'Infrastruttura

Al termine dei test di validazione, l'infrastruttura è stata completamente ripulita per evitare costi residui su AWS:

1. Eliminazione delle risorse Kubernetes: `kubectl delete -f k8s.yaml`.
2. Pulizia del filesystem locale EC2: `rm -rf $HOME/lab07`.
3. Pulizia risorse Docker in cache: `sudo docker system prune -af --volumes`.
4. Terminazione dell'istanza EC2 `lab07-CSP` dalla Console AWS.
5. Eliminazione della VPC (`lab07-CSP-vpc`) e del Security Group (`lab07-CSP-sg`).

---

## 7. Riepilogo Evidenze e Screenshot per la Consegna

Per la validazione finale dell'esercitazione sono stati prodotti e verificati i 4 screenshot ufficiali:

* **Screenshot 1:** Applicazione in Versione 2.0 (grafica viola) su Docker senza volume, indicante lista ticket vuota (dimostrazione perdita dati).
* **Screenshot 2:** Applicazione su Docker in ascolto sulla porta 8080 con volume `officina07-data` montato e 3 ticket salvati (dimostrazione persistenza).
* **Screenshot 3:** Applicazione distribuita su Kubernetes su porta NodePort `30080` con ConfigMap applicato ("Officina K8s - CSP").
* **Screenshot 4:** Applicazione in esecuzione su Kubernetes su porta `30080` con dati integri a seguito della distruzione del Pod e del test superato della `readinessProbe`.