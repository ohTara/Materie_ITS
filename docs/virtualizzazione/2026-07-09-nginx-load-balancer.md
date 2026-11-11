# Docker Compose — Nginx come reverse proxy e load balancer (09/07/2026)

**Cartella:** `Sistemi di Virtualizzazione/09-07-2026/nginx-main/nginx-main/`

## Obiettivo
Orchestrare più container con Docker Compose e distribuire il traffico tra due istanze della stessa API.

## Architettura
`Browser → Nginx (porta 80) → api1 | api2` (due servizi FastAPI). L'utente vede un solo indirizzo.

## File chiave
`docker-compose.yaml`
```yaml
services:
  api1: { build: ./api1 }
  api2: { build: ./api2 }
  nginx:
    image: nginx:latest
    ports: ["80:80"]
    volumes: ["./nginx/nginx.conf:/etc/nginx/nginx.conf:ro"]
    depends_on: [api1, api2]
```
`nginx/nginx.conf`
```nginx
events {}
http {
  upstream backend { server api1:8000; server api2:8000; }
  server { listen 80; location / { proxy_pass http://backend; } }
}
```

## Concetti
- Compose crea **una rete** in cui i servizi si raggiungono per **nome** (`api1`, `api2`): è il DNS interno di Docker.
- Un blocco `upstream` con più `server` fa **round-robin** di default.
- Solo Nginx pubblica una porta: le API non sono esposte direttamente.
- Il file di configurazione è montato in **sola lettura** (`:ro`).
- `depends_on` regola l'ordine di avvio, non la *prontezza* del servizio.

## Per riprovarlo
```bash
docker compose version
docker compose up --build
curl http://localhost/          # ripetere più volte: la risposta indica api1 o api2
docker compose down
```
(Comandi dal README del lab; l'output non è riportato perché non è presente nella repo.)

## Domanda di richiamo
Perché dentro `nginx.conf` si può scrivere `api1:8000` invece di un indirizzo IP?

<details><summary>Risposta</summary>Perché Compose crea una rete utente in cui il DNS di Docker risolve il nome del servizio nell'IP del container.</details>
