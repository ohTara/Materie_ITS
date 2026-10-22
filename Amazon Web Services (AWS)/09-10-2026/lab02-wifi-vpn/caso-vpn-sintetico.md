# Analisi Caso Sintetico VPN

**Parametri:**

- Client VPN: `192.0.2.10`
- Gateway VPN Pubblico: `198.51.100.20`
- Rete Privata Remota: `10.20.0.0/16`

| Momento | Destinazione | Uscita |
| :--- | :--- | :--- |
| Prima | 0.0.0.0/0 | Gateway della rete locale |
| Prima | 10.20.0.0/16 | Nessuna rotta specifica |
| Dopo | 0.0.0.0/0 | Gateway della rete locale |
| Dopo | 10.20.0.0/16 | Interfaccia VPN |

## Spiegazione

Si tratta di una configurazione **Split Tunnel IPv4**:

1. Il traffico indirizzato alla rete privata (`10.20.0.0/16`) segue la rotta specifica `/16` verso l'interfaccia VPN.
2. Il traffico generale verso Internet (es. `example.com` o `0.0.0.0/0`) passa dal gateway locale.
3. **Estremi del tunnel:** Client VPN (`192.0.2.10`) e Gateway VPN Pubblico (`198.51.100.20`).
