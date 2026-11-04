# Lab 03 — Protocolli: HTTP, TCP e DNS in locale (14/10/2026)

**Cartella:** `Amazon Web Services (AWS)/14-10-2026/lab03-protocolli/` (`sito/`, `evidenze/`, `consegna03.md`)
**Ambiente:** Windows 11, Python 3.14.7, curl 8.16.0, porta 8080, tutto su loopback (`127.0.0.1`).

## Obiettivo
Osservare una richiesta HTTP vera dall'inizio alla fine cambiando **una sola variabile per volta** e prevedendo il risultato *prima* di eseguire.

## Setup
Un server HTTP di Python serve la cartella `sito/` (contiene `messaggio.txt` con `LAB03-OK`). Il client è `curl`.
Flusso: `curl → TCP su loopback → server Python → sito/messaggio.txt`.
URL `http://127.0.0.1:8080/messaggio.txt` = schema `http` · host `127.0.0.1` · porta `8080` · percorso `/messaggio.txt`.

## Registro delle prove
| ID | Variabile cambiata | Risultato | Cosa dimostra |
|---|---|---|---|
| P1 | nessuna | 200, `LAB03-OK` | il server eroga la risorsa |
| P2 | percorso `/assente.txt` | **404**, curl esce con `0` | server raggiungibile, risorsa inesistente |
| P3 | contenuto del file | 200, `Content-Length` 21 | la risposta segue il file su disco |
| P4 | `-v` | handshake e header visibili | `GET /messaggio.txt HTTP/1.1`, `Host: 127.0.0.1:8080` |
| P5 | metodo `HEAD` (`-I`) | 200, solo header | stessi metadati di GET, senza corpo |
| P6 | server spento | **connessione rifiutata**, curl esce con `7` | nessun processo in ascolto |
| P7 | server riavviato | 200 | servizio ripristinato |

## Concetti da ricordare
- **Exit code di curl ≠ stato HTTP.** `0` con 404 significa "trasferimento riuscito, risposta applicativa 404". `7` significa che la connessione TCP non si è stabilita.
- **Handshake TCP:** SYN → SYN-ACK → ACK, poi la richiesta HTTP. Gli estremi della connessione sono la coppia `(IP, porta)`; la porta del client è effimera (es. 53563), quella del server è 8080.
- **Connessione rifiutata vs timeout:** *rifiutata* (RST) = host vivo ma nessun processo in ascolto; *timeout* = pacchetti persi o firewall che scarta in silenzio.
- **DNS vs HTTP:** con un IP letterale non c'è query DNS. Il DNS prova che un nome diventa un IP, non che sulla porta ci sia un server HTTP. `localhost` può risolvere in `127.0.0.1` o `::1`: se il server ascolta solo IPv4 il comportamento cambia.
- **Limiti:** un test su loopback non dice nulla su Wi-Fi, routing, NAT o HTTPS.

## Ticket di diagnosi svolto
*Sintomo:* l'URL non restituisce più `LAB03-OK`. *Ipotesi:* file mancante o rinominato (livello applicativo). *Prova:* `curl` → 404. *Correzione:* `messaggio-backup.txt` rinominato in `messaggio.txt`. *Controprova:* 200 e `LAB03-OK`.

## Domanda di richiamo
Un `curl` termina con codice `0` ma mostra 404: la rete funziona? Perché?

<details><summary>Risposta</summary>Sì: TCP e HTTP hanno funzionato (c'è stata una risposta valida del server). Il 404 è un errore a livello applicativo: la risorsa non esiste.</details>
