# Consegna Lab 03

Studente: Luca Tarallo
Sistema operativo e versioni Python/curl: Windows 11 / Python 3.14.7 / curl 8.16.0
Porta usata: 8080
Attività 5: modello sintetico (Percorso B)
Attività 6: query reale

## Schema e URL

### Diagramma del Flusso

`client curl -> TCP/IP su loopback -> server Python -> sito/messaggio.txt`
*(Nota: Tutti i componenti risiedono su un unico computer locale; nessun dispositivo di rete intermedio come router o switch è coinvolto).*

### Scomposizione URL (`http://127.0.0.1:8080/messaggio.txt`)

- **Schema:** `http` (protocollo di livello applicativo non cifrato)
- **Host:** `127.0.0.1` (indirizzo IP di loopback locale)
- **Porta:** `8080` (porta di ascolto del servizio web)
- **Percorso:** `/messaggio.txt` (risorsa richiesta sul server)

---

## Registro delle prove

| ID | Unica variabile modificata | Previsione PRIMA del test | Stato HTTP o errore | Uscita curl | Corpo | File di evidenza e log server | Conclusione |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **P1** | Nessuna (File presente) | Risposta 200 OK e testo "LAB03-OK" | 200 OK | 0 | LAB03-OK | `evidenze/p1-presente.txt` | Il server trova ed eroga correttamente la risorsa richiesta. |
| **P2** | Percorso (`/assente.txt`) | Errore 404 Not Found, il server risponde | 404 Not Found | 0 | HTML di errore | `evidenze/p2-assente.txt` | Il server è raggiungibile, ma la risorsa specificata non esiste. |
| **P3** | Contenuto del file (`LAB03-VERSIONE-2`) | Risposta 200 OK con testo aggiornato e Content-Length maggiore | 200 OK | 0 | LAB03-VERSIONE-2 | `evidenze/p3-modificato.txt` | La risposta riflette immediatamente la modifica al file su disco (Content-Length passa a 21). |
| **P4** | Dettagli estesi (`-v`) | Invio di richieste GET complete di intestazioni | 200 OK | 0 | LAB03-VERSIONE-2 | `evidenze/p4-traccia.txt` | Mostra l'handshake e le intestazioni HTTP scambiate. |
| **P5** | Metodo HTTP (`HEAD` tramite `-I`) | Risposta 200 OK con solo intestazioni, senza corpo | 200 OK | 0 | (Vuoto) | `evidenze/p5-head.txt` | HEAD restituisce i metadati (Content-Length: 21) senza trasferire il carico utile. |
| **P6** | Server spento | Connessione rifiutata, nessuna risposta HTTP | Nessuno (Errore TCP) | 7 | Nessuno | `evidenze/p6-fermato.txt` | L'impossibilità di stabilire la connessione TCP genera un errore di rifiuto (code 7). |
| **P7** | Riavvio del server | Ripristino della risposta 200 OK e corpo V1 | 200 OK | 0 | LAB03-OK | `evidenze/p7-ripristino.txt` | La riattivazione del servizio ripristina la funzionalità. |

---

## Confronto GET/HEAD

| Elemento | GET di P4 | HEAD di P5 |
| --- | --- | --- |
| Metodo nel log server | GET | HEAD |
| Stato HTTP | 200 OK | 200 OK |
| Content-Type | text/plain | text/plain |
| Content-Length | 21 | 21 |
| Corpo ricevuto | LAB03-VERSIONE-2 | (Assente) |

**Spiegazione:** `HEAD` richiede al server di restituire le stesse intestazioni di una richiesta `GET`, incluso il `Content-Length`, ma senza inviare il corpo del messaggio.

---

## Analisi TCP (Modello Sintetico)

| Evento sintetico | Sorgente | Destinazione | Informazione / Flag |
| --- | --- | --- | --- |
| **A** | 127.0.0.1:53563 | 127.0.0.1:8080 | SYN (Inizio connessione dal client) |
| **B** | 127.0.0.1:8080 | 127.0.0.1:53563 | SYN, ACK (Conferma e sincronizzazione dal server) |
| **C** | 127.0.0.1:53563 | 127.0.0.1:8080 | ACK (Completamento Handshake 3-way) |
| **D** | Client | Server | GET /messaggio.txt (Richiesta HTTP) |
| **E** | Server | Client | Risposta 200 OK e corpo |

---

## Nomi e DNS

- **URL testato:** `http://127.0.0.1:8080/messaggio.txt`
- **Interpretazione:** L'host è espresso come indirizzo IP letterale; pertanto, il sistema non effettua alcuna query al servizio DNS.
- **Sostituzione con localhost:** Usare `localhost` può fare sì che il sistema risolva il nome tramite il file host locale (in IPv4 `127.0.0.1` o IPv6 `::1`), potendo causare comportamenti diversi se il server è in ascolto solo su IPv4.

---

## Ticket di diagnosi

- **Sintomo:** L'URL originale non restituisce più `LAB03-OK`.
- **Ipotesi iniziale e livello coinvolto:** Livello Applicativo - File mancante o rinominato nella cartella servita.
- **Prova scelta:** Esecuzione di `curl` sull'URL e controllo del log/stato HTTP.
- **Risultato osservato:** Stato HTTP `404 Not Found` (uscita curl `0`).
- **Correzione:** Rinomimato `messaggio-backup.txt` in `messaggio.txt` nella cartella `sito/`.
- **Controprova di ripristino:** Richiesta `curl` riuscita con esito `200 OK` (uscita curl `0`) e corpo `LAB03-OK`.

---

## Risposte finali e cleanup

1. **Evidenza P2:** Il log del server e la risposta HTTP 404 dimostrano che il server HTTP era attivo e raggiungibile.
2. **Uscita curl 0 e HTTP 404:** Il codice di uscita `0` indica che il protocollo di trasporto/trasferimento ha avuto successo; il 404 è una risposta valida a livello applicativo HTTP.
3. **Differenza HEAD/GET:** HEAD restituisce solo le intestazioni senza corpo, mentre GET include il payload.
4. **Distinzione estremi TCP:** Gli estremi sono identificati dalla coppia `(IP, Porta)`. La porta temporanea dinamica del client (es. 53563) lo distingue dal server (porta 8080).
5. **DNS vs HTTP:** DNS dimostra la risoluzione del nome in indirizzo IP, ma non garantisce che sulla porta di destinazione vi sia un server HTTP attivo.
6. **Connessione rifiutata vs Timeout:** Connessione rifiutata (RST) indica che l'host è attivo ma nessun processo ascolta sulla porta; Timeout indica perdita di pacchetti o silenzio di un firewall.
7. **Controprova:** La ricezione di uno stato `200 OK` unitamente al corpo `LAB03-OK`.
8. **Limiti delle osservazioni:** Essendo un test su loopback, non si possono trarre conclusioni su prestazioni Wi-Fi, routing, NAT o cifratura HTTPS.

### Cleanup

Server arrestato correttamente (esito curl `7`, connessione rifiutata registrato in `evidenze/cleanup.txt`).
