# Schema Wi-Fi e Isolamento Rete

> **Nota:** Progetto con dati sintetici, non da applicare alla rete reale.

## Percorsi Rete

- Client interno -> AP -> VLAN interna -> risorse interne/Internet
- Client ospite -> AP -> VLAN ospiti -> solo Internet

## Configurazione Prevista

- **VLAN Interna:** ID 10, Rete `10.10.10.0/24`, SSID `AZIENDA-INTERNA` (WPA2/WPA3-Enterprise)
- **VLAN Ospiti:** ID 20, Rete `10.10.20.0/24`, SSID `AZIENDA-OSPITI` (Isolamento client attivo)
- **Firewall:** Regola che nega il traffico dalla VLAN 20 alla VLAN 10. DNS approvato ed accesso Internet consentiti per entrambe.
