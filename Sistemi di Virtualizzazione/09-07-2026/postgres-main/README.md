# Laboratorio Docker Compose - PostgreSQL e Persistenza

## Obiettivi

In questo laboratorio impareremo a:

- utilizzare un database PostgreSQL in un container Docker
- collegare più applicazioni FastAPI allo stesso database
- comprendere la differenza tra SQLite e PostgreSQL
- utilizzare Docker Compose per orchestrare più servizi
- implementare la persistenza dei dati tramite Docker Volume
- distinguere applicazioni stateless e stateful

---

# Architettura

```text
                    Browser
                        |
                     Nginx
                    /     \
                   /       \
               API1       API2
                   \       /
                    \     /
                  PostgreSQL
                       |
                     Volume
```

Tutte le richieste HTTP entrano tramite Nginx.

Le richieste vengono distribuite alle due istanze FastAPI.

Entrambe le API utilizzano lo stesso database PostgreSQL.

I dati vengono salvati in un volume Docker persistente.

---

# Perché PostgreSQL?

Nel laboratorio precedente ogni container conteneva il proprio database SQLite.

```text
API1
 |
repository.db

API2
 |
repository.db
```

In questo scenario:

- ogni container possiede un database diverso
- i dati non sono condivisi
- una richiesta potrebbe essere servita da API1
- la successiva da API2

ottenendo risultati incoerenti.

La soluzione consiste nell'utilizzare un database centralizzato.

```text
API1
   \
    \
     PostgreSQL
    /
   /
API2
```

---

# Struttura del progetto

```text
docker-postgres/

├── compose.yaml

├── api1/
│   ├── Dockerfile
│   └── app/
│       ├── main.py
│       └── requirements.txt

├── api2/
│   ├── Dockerfile
│   └── app/
│       ├── main.py
│       └── requirements.txt

└── nginx/
    └── nginx.conf
```

---

# Verifica prerequisiti

Verificare l'installazione di Docker:

```bash
docker --version
```

Verificare Docker Compose:

```bash
docker compose version
```

---

# Costruzione delle immagini

Posizionarsi nella directory del progetto:

```bash
cd docker-postgres
```

Costruire le immagini:

```bash
docker compose build
```

Docker costruirà:

```text
api1
api2
```

e scaricherà automaticamente:

```text
nginx
postgres
```

da Docker Hub.

---

# Avvio dell'infrastruttura

Avviare tutti i servizi:

```bash
docker compose up --build
```

Verranno avviati:

```text
postgres
api1
api2
nginx
```

---

# Verifica dei container

Visualizzare i container attivi:

```bash
docker ps
```

Output atteso:

```text
nginx
api1
api2
postgres
```

---

# Test del sistema

## Verifica home page

Aprire:

```text
http://localhost
```

oppure:

```bash
curl localhost
```

Possibile risposta:

```json
{
  "server":"api1",
  "msg":"API pronta"
}
```

oppure:

```json
{
  "server":"api2",
  "msg":"API pronta"
}
```

---

## Inserimento di un utente

```text
http://localhost/add/paolo
```

Risposta:

```json
{
  "server":"api1",
  "msg":"paolo aggiunto"
}
```

---

## Inserimento di un secondo utente

```text
http://localhost/add/marco
```

---

## Visualizzazione degli utenti

```text
http://localhost/lista
```

oppure:

```bash
curl localhost/lista
```

Risposta possibile:

```json
{
  "server":"api2",
  "utenti":[
    [1,"paolo"],
    [2,"marco"]
  ]
}
```

Osservare che:

- API1 può scrivere
- API2 può leggere

perché entrambe utilizzano lo stesso database PostgreSQL.

---

# PostgreSQL Container

Il database viene eseguito come servizio separato.

```yaml
postgres:
  image: postgres:17
```

FastAPI si collega utilizzando:

```python
host="postgres"
```

Il nome:

```text
postgres
```

viene risolto automaticamente dal DNS interno di Docker Compose.

---

# Persistenza dei dati

I dati PostgreSQL sono salvati nel volume:

```yaml
volumes:
  - pgdata:/var/lib/postgresql/data
```

Il volume contiene:

- database
- tabelle
- record
- configurazioni PostgreSQL

---

# Test della persistenza

Arrestare l'infrastruttura:

```bash
docker compose down
```

Riavviare:

```bash
docker compose up
```

Visualizzare nuovamente:

```text
http://localhost/lista
```

Gli utenti inseriti saranno ancora presenti.

---

# Eliminazione del volume

Attenzione.

Questo comando elimina anche i dati:

```bash
docker compose down -v
```

Alla successiva accensione:

```bash
docker compose up
```

il database sarà vuoto.

---

# Visualizzazione dei log

Tutti i servizi:

```bash
docker compose logs -f
```

Solo PostgreSQL:

```bash
docker compose logs postgres
```

Solo API1:

```bash
docker compose logs api1
```

Solo API2:

```bash
docker compose logs api2
```

---

