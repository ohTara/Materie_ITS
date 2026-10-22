# Consegna Lab 01

- **Sistema operativo:** Windows
- **Data/ora:** 06/10/2026, ore 17:10
- **Tipo di collegamento:** Ethernet (Ethernet0, vmxnet3)
- **Indirizzo IPv4:** 172.20.127.114/24
- **Gateway predefinito IPv4:** 172.20.127.254
- **Server DNS IPv4:** 172.20.103.10, 172.20.103.11

| Elemento | Valore | Evidenza |
| --- | --- | --- |
| Interfaccia | Ethernet0 (vmxnet3) | configurazione.txt |
| IPv4 | 172.20.127.114 | configurazione.txt |
| Prefisso | /24 | configurazione.txt |
| Gateway | 172.20.127.254 | percorso.txt (hop 1), ping-gateway.txt |
| DNS | 172.20.103.10, 172.20.103.11 | dns.txt (server interrogato: 172.20.103.10) |
| Latenza media gateway | < 1 ms (0% persi) | ping-gateway.txt |
| Latenza media Internet | 9 ms (25% persi, 1 su 4) | ping-internet.txt |
| Primo hop | 172.20.127.254 (< 1 ms) | percorso.txt |
| Ultimo hop visibile | ae1.cr4-nyc12.ip4.gtt.net [89.149.142.226], 87 ms (hop 8) | percorso.txt |

## Note e interpretazione

- **Rete locale:** il gateway è nella stessa subnet dell'host (172.20.127.0/24), risponde in meno di 1 ms senza perdite ed è il primo hop del percorso.
- **DNS:** la risoluzione di amazon.com è riuscita (3 indirizzi restituiti dal server 172.20.103.10).
- **Perdita verso Internet:** su 4 richieste a 1.1.1.1 una è scaduta (25%). Con un solo test non è possibile concludere che ci sia un problema.
- **Percorso:** dall'hop 9 in poi non ci sono risposte (`Richiesta scaduta`) e il tracert risulta interrotto all'hop 25 senza raggiungere la destinazione. Il test TCP sulla porta 443 (`tcp443.txt`) però riesce (`TcpTestSucceeded: True`), quindi amazon.com è raggiungibile: il silenzio è compatibile con router che non rispondono a ICMP.
- **Latenza:** il salto da 1 ms (hop 7) a 87 ms (hop 8) è compatibile con un collegamento intercontinentale (hop `nyc12`).

## Diagnosi simulata

- **Gateway raggiungibile ma ICMP esterno senza risposta:** se il gateway locale risponde correttamente ma i nodi esterni non rispondono al ping o interrompono il `tracert`, la connettività di livello 3 (IP) verso l'esterno potrebbe essere comunque attiva; l'assenza di risposte lascia aperte ipotesti di filtraggio del traffico ICMP da parte di firewall/router lungo il percorso o problemi di routing sulla rete del provider.
- **IP esterno raggiungibile ma `nslookup` fallito:** suggerisce un problema specifico legato al servizio DNS (es. resolver non raggiungibile, porta 53 bloccata o configurazione errata del server DNS), mentre la connettività IP generale verso Internet funziona regolarmente.
- **Ping fallito verso un nome:** da solo non dimostra in modo univoco un guasto al server DNS, poiché la mancata risposta può essere causata da un fallimento della risoluzione oppure da un blocco del traffico ICMP/IP verso l'host di destinazione.
