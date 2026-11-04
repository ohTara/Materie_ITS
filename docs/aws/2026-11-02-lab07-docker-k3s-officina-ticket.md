# Lab 07 — Docker, volumi e K3s su EC2: "Officina Ticket" (02/11/2026)

**Cartella:** `Amazon Web Services (AWS)/02-11-2026/lab07-windows/` · **Ambiente:** EC2 `t3.medium`, Ubuntu 26.04, Docker, K3s (Kubernetes single-node). Svolto da Windows (PowerShell).
**Nota:** `consegna07.md` nella repo è vuoto (0 byte); questo documento si basa su `relazione_finale_lab_07.md`, `Dockerfile`, `.dockerignore` e `app.py`.

## Obiettivo
Vedere perché i dati di un container si perdono, risolvere con volumi, poi portare la stessa app su Kubernetes con configurazione, storage persistente e health check.

## L'applicazione
`app.py`: server HTTP Python (`ThreadingHTTPServer`) + **SQLite** in `/data/tickets.db`. Endpoint: `/` (UI), `/tickets`, `/api/tickets`, **`/healthz`** (200 se il DB risponde; **503** se esiste il file `/tmp/officina-not-ready`, usato per simulare il guasto). Titolo da variabile `APP_TITLE`.

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY app.py .
RUN mkdir /data && chown 10001:10001 /data
USER 10001:10001          # non gira come root
EXPOSE 8000
CMD ["python", "app.py"]
```
`.dockerignore` esclude `.git`, `.aws`, `.env`, `*.db`, `*.tar`, `*.log`, `k8s.yaml`: **segreti e dati locali non finiscono nell'immagine**.

## Percorso
1. **Docker V1** (`officina07:1.0`) su rete `officina07-net`, porta 8080, senza volume.
2. **V2** (`officina07:2.0`) senza volume: eliminando il container V1 i ticket **spariscono** (il DB era nel filesystem del container).
3. **Volume Docker** `officina07-data` montato su `/data`:
   ```bash
   sudo docker run -d --name officina07 --network officina07-net -p 8080:8000 \
     --mount source=officina07-data,target=/data \
     -e APP_TITLE="Officina persistente - CSP" officina07:2.0
   ```
   Stop/riavvio o passaggio V2 → V1 sullo stesso volume: i ticket restano. Backup a caldo con l'API di SQLite su `/tmp/tickets-backup.db`, verificato in sola lettura.
4. **K3s:** rimosso il container per liberare le porte; installato K3s; immagine importata nel runtime containerd con
   `sudo docker save officina07:2.0 | sudo k3s ctr images import -` (K3s non vede le immagini del Docker locale).
5. **Manifesto `k8s.yaml`:** Namespace `officina07`, ConfigMap `officina-config` (`APP_TITLE`), PVC `officina-pvc` 1Gi (Local Path Provisioner), Deployment con `readinessProbe` (`/healthz`, ogni 5 s) e `livenessProbe` (`/healthz`, ogni 10 s), Service **NodePort 30080**. `kubectl apply -f k8s.yaml`.

## Prove di resilienza
- **Pod eliminato** (`kubectl delete pod -l app=officina -n officina07`): il Deployment ne crea uno nuovo che si riattacca allo stesso PVC → ticket intatti.
- **Readiness:** creato `/tmp/officina-not-ready` nel pod → `/healthz` risponde 503, il pod passa a `0/1 READY` ed esce dagli endpoint del Service; rimosso il file torna `1/1` senza perdere dati.

| Probe | Cosa fa se fallisce |
|---|---|
| readiness | toglie il pod dal traffico, **non** lo riavvia |
| liveness | **riavvia** il container |

## Cleanup
`kubectl delete -f k8s.yaml`, `rm -rf $HOME/lab07`, `docker system prune -af --volumes`, terminazione EC2, eliminazione `lab07-CSP-vpc` e `lab07-CSP-sg`.

## Evidenze (4 screenshot)
V2 senza volume (lista vuota) · Docker con volume (3 ticket) · K8s su `:30080` con ConfigMap · K8s dopo pod eliminato e test readiness.

## Domande di richiamo
1. Perché i ticket si perdono senza volume e restano con un volume?
2. Qual è la differenza operativa tra readiness e liveness?
3. Perché serve `k3s ctr images import`?

<details><summary>Risposte</summary>

1. Senza volume il file `tickets.db` vive nel layer scrivibile del container, distrutto con lui; il volume ha un ciclo di vita separato.
2. Readiness controlla se il pod può ricevere traffico; liveness se va riavviato.
3. K3s usa containerd, che ha un archivio immagini diverso da quello di Docker.
</details>
