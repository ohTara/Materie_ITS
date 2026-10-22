# Laboratorio Docker Compose - Nginx Load Balancer

## Obiettivi

In questo laboratorio impareremo a:

- utilizzare Docker Compose per orchestrare più container
- creare una rete Docker automatica
- utilizzare Nginx come Reverse Proxy
- utilizzare Nginx come Load Balancer
- distribuire il traffico tra più istanze FastAPI

---

## Architettura

                Browser
                    |
                 Nginx
                /     \
               /       \
           API1       API2

L'utente vede un solo servizio, ma dietro lavorano due applicazioni FastAPI.

---

## Struttura del progetto

```text
docker-nginx-lb/

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

# Costruzione e avvio del laboratorio

## Verifica prerequisiti

Verificare che Docker sia installato:

```bash
docker --version
```

Verificare che Docker Compose sia disponibile:

```bash
docker compose version
```

---

## Posizionarsi nella directory del progetto

```bash
cd docker-nginx-lb
```

---

## Struttura del progetto

```text
docker-nginx-lb/

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

## Costruzione delle immagini

```bash
docker compose build
```

Docker costruirà:

```text
api1
api2
```

utilizzando i rispettivi Dockerfile.

---

## Avvio dei container

```bash
docker compose up
```

oppure:

```bash
docker compose up --build
```

Il parametro:

```text
--build
```

obbliga Docker a ricostruire le immagini prima dell'avvio.

---

## Verifica dei container attivi

```bash
docker ps
```

Dovrebbero comparire:

```text
nginx
api1
api2
```

---

## Test dell'applicazione

Browser:

```text
http://localhost
```

oppure:

```bash
curl localhost
```

Possibili risposte:

```json
{
  "server":"api1",
  "msg":"API pronta"
}
```

oppure

```json
{
  "server":"api2",
  "msg":"API pronta"
}
```

---

## Visualizzazione log

```bash
docker compose logs
```

oppure:

```bash
docker compose logs -f
```

---

## Arresto dell'infrastruttura

```bash
docker compose down
```
