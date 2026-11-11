# Fondamenti di Reti — subnetting e Packet Tracer

**Cartelle:** `Fondamenti_di_Reti/` (nella repo anche come `Fondamenti-di-Reti`, vedi *Manutenzione*).

## File per data (dal nome del file)
| Data | File | Tipo |
|---|---|---|
| 27/01/2026 | `Fondamenti_di_Reti_27-01-2026.pkt` | Packet Tracer |
| 02/02/2026 | `Fondamenti_di_Reti_02-02-2026.pkt` | Packet Tracer |
| 09/02/2026 | `es_9-2-2026.txt` | appunti di subnetting |
| 02/03/2026 | `Fondamenti di reti di calcolatori_02-03-2026.pkt`, `ipv6 2 marzo.pkt` | Packet Tracer (IPv6) |
| 17/03/2026 | `Fondamenti_di_Reti_17-03-2026.pkt` | Packet Tracer |
| 20/03/2026 | `Routing (modulo 8)-20260320.zip` | materiale Cisco |
| 14/04/2026 | `Fondamenti_di_Reti_14-04-2026.pkt` | Packet Tracer |
| 28/04/2026 | `Fondamenti_di_Reti_28-04-2026_incompleto.pkt` | Packet Tracer, **incompleto** |
| senza data | `routing statico.pkt`, `routing dinamico - OSPF.pkt` | routing |
Altri: *Esercizi di subnetting IPv4.pdf*, *Lab – Identifying IPv4 Addresses.pdf*. Il contenuto dei `.pkt` si apre solo con Packet Tracer: gli argomenti sono dedotti dai nomi.

## Subnetting — gli appunti del 09/02 spiegati
**Caso 1:** `192.168.10.0/24` diviso in 16 sottoreti. Servono `2^n = 16` → **n = 4** bit di rete in più → `/28` (maschera `255.255.255.240`), blocchi da 16 indirizzi:
`192.168.10.0/28`, `.16/28`, `.32/28`, `.48/28`, …
**Caso 2:** `172.16.0.0/16`, 2000 host per sottorete. `2^10 = 1024` non basta; `2^11 = 2048` sì (2046 host utilizzabili, togliendo rete e broadcast) → 11 bit host → **`/21`**, maschera `255.255.248.0`; i bit di rete aggiunti sono 21 − 16 = 5 → 2^5 = **32 sottoreti**.
**Regola:** host utilizzabili = `2^h − 2`; sottoreti = `2^(bit presi in prestito)`.

## Domanda di richiamo
Quanti host utilizzabili ha una `/26`?
<details><summary>Risposta</summary>Host bit = 32 − 26 = 6 → 2^6 − 2 = 62.</details>
