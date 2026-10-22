# Registrazione Parametri Radio

| Parametro | Valore | Fonte |
| :--- | :--- | :--- |
| SSID | LAB-DIPENDENTI | Sintetico |
| Banda | 5 GHz | Sintetico |
| Canale | 36 | Sintetico |
| Segnale | 78% | Sintetico |
| Autenticazione | WPA2-Enterprise | Sintetico |
| Velocità di collegamento | 433 Mbit/s | Sintetico |

## Risposte ai quesiti

1. **Quali dati descrivono il collegamento radio e quali la configurazione IP?**
   - **Collegamento radio:** SSID, banda (2.4/5 GHz), canale, intensità/potenza del segnale (%), metodo di autenticazione/sicurezza (WPA2/WPA3), velocità di collegamento (link rate).
   - **Configurazione IP:** Indirizzo IPv4/IPv6, subnet mask, Default Gateway, server DNS.

2. **Perché un'interrogazione WLAN bloccata non dimostra l'assenza di connettività?**
   - Perché il blocco dell'interrogazione è dovuto a permessi di sistema o privacy (es. errore di autorizzazione sulla posizione), non a un guasto hardware o all'assenza di connessione di rete.

3. **Come distinguere servizio WLAN fermo, permesso di posizione negato e scheda Wi-Fi non rilevata?**
   - **Servizio fermo:** `Get-Service WlanSvc` restituisce lo stato `Stopped`.
   - **Permesso negato:** Il comando WLAN fallisce con un errore di permessi/accesso (Errore 5).
   - **Scheda non rilevata:** `Get-NetAdapter -Physical` non elenca interfacce Wi-Fi tra i dispositivi fisici.

4. **Un segnale forte garantisce autenticazione riuscita e accesso a Internet? Motivare.**
   - No. Il segnale indica la qualità della connessione radio (Layer 1). L'autenticazione può fallire per credenziali errate (Layer 2) e l'accesso a Internet può mancare per problemi di IP, gateway o DNS (Layer 3+).

5. **La velocità di collegamento equivale alla velocità di un download? Motivare.**
   - No. La velocità di collegamento è la capacità teorica massima della radiofrequenza. La velocità di download effettiva dipende da overhead dei protocolli, congestione di rete e limiti del server remoto.

---

## Checklist

### Checklist 1: SSID visibile ma autenticazione fallita

- [ ] **Segnale:** Verificare la potenza del segnale radio.
- [ ] **Autenticazione:** Controllo di credenziali, password e certificati.
- [ ] **Indirizzamento:** N/D (avviene dopo l'autenticazione).
- [ ] **Rotta / DNS / Autorizzazione:** N/D.

### Checklist 2: VPN connessa ma risorsa privata non raggiungibile

- [ ] **Segnale / Autenticazione:** Sessione VPN già stabilita.
- [ ] **Indirizzamento:** Verificare l'IP privato assegnato al tunnel.
- [ ] **Rotta:** Verificare la presenza della rotta verso la rete remota (es. `10.20.0.0/16`).
- [ ] **DNS:** Verificare la risoluzione del nome della risorsa.
- [ ] **Autorizzazione:** Verificare regole di firewall o ACL.
