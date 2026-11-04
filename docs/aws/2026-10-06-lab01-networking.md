# Lab 01 — Networking di base (06/10/2026)

**Materia:** Amazon Web Services (AWS) · **Cartella:** `Amazon Web Services (AWS)/06-10-2026/lab01-networking/`
**Ambiente:** PC Windows del laboratorio, PowerShell. Nessuna risorsa AWS creata.

## Obiettivo
Leggere la configurazione di rete di una macchina e capire, con evidenze, *dove* può rompersi la connettività: interfaccia/IP → gateway → Internet → DNS.

## Cosa è stato fatto
Ogni test ha prodotto un file di evidenza e la relazione `consegna01.md` li collega in una tabella *elemento → valore → evidenza*.

| Verifica | Evidenza | Risultato osservato |
|---|---|---|
| Configurazione interfaccia (IP, gateway, DNS) | `configurazione.txt` | Ethernet0 (vmxnet3), IPv4 `172.20.127.114/24`, gateway `172.20.127.254`, DNS `172.20.103.10` e `.11` |
| Ping al gateway | `ping-gateway.txt` | < 1 ms, 0% persi |
| Ping a Internet (`1.1.1.1`) | `ping-internet.txt` | 9 ms, **1 pacchetto su 4 perso (25%)** |
| Risoluzione DNS (`nslookup amazon.com`) | `dns.txt` | Risolto dal server `172.20.103.10` (risposta *non autorevole*, cioè dalla cache) |
| Percorso (`tracert amazon.com`) | `percorso.txt` | Hop 1 = gateway; salto da 1 ms a 87 ms all'hop 8 (collegamento intercontinentale); dall'hop 9 solo `Richiesta scaduta` |
| Raggiungibilità TCP 443 | `tcp443.txt` (citato nella consegna) | `TcpTestSucceeded: True` |

## Il ragionamento (la parte da ricordare)
- **Il silenzio di `tracert` non significa "irraggiungibile".** Dall'hop 9 non arrivano risposte, ma la porta 443 risponde: molti router non rispondono a ICMP (filtrato). Per decidere serve una *seconda* prova con un protocollo diverso (qui TCP/443).
- **Una perdita del 25% su un solo test non è una conclusione**, è un'osservazione da ripetere.
- **Ping verso un nome che fallisce non prova un guasto DNS**: può fallire la risoluzione oppure l'ICMP verso l'host. Per separare i casi: ping a un IP, poi `nslookup`.
- Schema di diagnosi usato: *IP esterno raggiungibile ma `nslookup` fallito* → problema DNS (resolver, porta 53); *gateway ok ma esterno muto* → filtro ICMP o routing del provider.

## Comandi (Windows)
```powershell
Get-NetIPConfiguration -Detailed        # formato dell'output in configurazione.txt (da verificare)
ping <gateway>
ping 1.1.1.1
nslookup amazon.com
tracert amazon.com
Test-NetConnection amazon.com -Port 443
```

## Domande di richiamo
1. Perché per sapere se amazon.com è raggiungibile non basta un `tracert` interrotto?
2. Che differenza c'è tra "risposta non autorevole" e "risposta autorevole" in `nslookup`?

<details><summary>Risposte</summary>

1. Perché ICMP può essere filtrato dai router intermedi; si conferma con un test su una porta reale (TCP 443).
2. La non autorevole arriva da un resolver che ha la risposta in cache; l'autorevole dal server che ospita la zona del dominio.
</details>

**Collegamenti:** Linux (`ip`, `ping`, `dig`), Fondamenti di Reti (subnetting, gateway), AWS (VPC, Security Group: lo stesso ragionamento a strati).
