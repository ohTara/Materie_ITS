'''
Autore: Luca Tarallo
Data: 27/10/2026
Titolo: Eseguire un comando del sistema operativo usando il modulo os.
'''
import os

##
## Funzioni:
##
def esegui_comando(comando: str) -> int:
    '''
    Funzione: esegui_comando
    Esegue un comando nella shell del sistema operativo con os.system.
    L'output del comando appare direttamente nel terminale.

    Parametri formali:
    str comando -> comando da eseguire (es. "dir" su Windows, "ls -l" su Linux)

    Valore di ritorno:
    int -> codice restituito da os.system (0 = successo; su Linux/macOS e'
           lo "status" codificato, il codice di uscita e' status >> 8)
    '''
    codice = os.system(comando)  # Esito dell'esecuzione
    return codice


'''
Programma principale
Chiede un comando, lo esegue e ne mostra l'esito.
ATTENZIONE: os.system passa la stringa alla shell; non usarlo mai con
input di sconosciuti (command injection). Qui l'input e' dell'utente stesso.
'''
# Sezione di input Dati
comando_input = input("Comando da eseguire: ").strip()  # Comando scelto dall'utente

# Elaborazione
if comando_input == "":
    print("Errore: nessun comando inserito.")
else:
    esito = esegui_comando(comando_input)  # Codice di ritorno
    # Sezione di output
    print(f"Codice di ritorno: {esito}")
