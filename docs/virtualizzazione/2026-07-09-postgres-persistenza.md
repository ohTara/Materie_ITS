# Docker Compose — PostgreSQL e persistenza (09/07/2026)

**Cartella:** `Sistemi di Virtualizzazione/09-07-2026/postgres-main/` (evoluzione del lab Nginx)

## Obiettivo
Far usare lo **stesso database** a due API e rendere i dati persistenti con un volume; capire stateless vs stateful.

## Architettura
`Browser → Nginx → api1 | api2 → PostgreSQL → volume pgdata`

## Perché PostgreSQL
Nel lab precedente ogni container aveva il proprio SQLite: due istanze = due database diversi e dati incoerenti. Con un DB condiviso, le API restano **stateless** e lo stato sta in un solo servizio **stateful**.

## Elementi chiave
```yaml
postgres:
  image: postgres:17
  environment: { POSTGRES_USER: admin, POSTGRES_PASSWORD: admin, POSTGRES_DB: repository }
  ports: ["5432:5432"]
  volumes: ["pgdata:/var/lib/postgresql/data"]
volumes: { pgdata: }
```
- Le API si collegano con `psycopg2` all'host **`postgres`** e, finché il DB non è pronto, **ritentano ogni 2 secondi** (`while db is None … sleep(2)`): risolve il fatto che `depends_on` non attende la prontezza.
- Alla partenza creano la tabella `utenti` (`id SERIAL PRIMARY KEY`, `nome`) con `CREATE TABLE IF NOT EXISTS` (idempotente). Endpoint `/` e `/add/{nome}`.
- Il volume nominato `pgdata` sopravvive a `docker compose down` (si perde solo con `down -v`).

## Attenzione (sicurezza)
Credenziali `admin/admin` scritte nel `docker-compose.yaml` e nei `main.py`, e porta `5432` pubblicata: accettabile in un lab locale, **non** in un ambiente reale. In produzione: variabili da file `.env` non versionato o secret manager, porta non esposta.

## Domanda di richiamo
Che differenza c'è tra `docker compose down` e `docker compose down -v` per i dati del DB?

<details><summary>Risposta</summary>`down` rimuove container e rete ma conserva i volumi; `down -v` elimina anche i volumi, quindi i dati.</details>
