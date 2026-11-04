'''
Autore: Luca Tarallo
Data: 27/10/2026
Titolo: Scrivere una procedura che dato un percorso elenchi tutte le directories presenti.
'''
import os

##
## Funzioni:
##
def elenca_directory(percorso: str) -> list:
    '''
    Funzione: elenca_directory
    Restituisce i nomi delle sole directory contenute direttamente in un percorso.

    Parametri formali:
    str percorso -> percorso della directory da esaminare

    Valore di ritorno:
    list -> lista di str con i nomi delle sottodirectory (vuota se non ce ne sono)
    '''
    directories = []  # Nomi delle directory trovate
    for nome in os.listdir(percorso):
        if os.path.isdir(os.path.join(percorso, nome)):
            directories.append(nome)
    return directories


'''
Programma principale
Chiede un percorso e ne stampa le sottodirectory di primo livello.
'''
# Sezione di input Dati
percorso_input = input("Percorso da esaminare: ").strip()  # Percorso scelto dall'utente

# Elaborazione
if not os.path.isdir(percorso_input):
    print("Errore: il percorso non esiste o non e' una directory.")
else:
    try:
        elenco = elenca_directory(percorso_input)  # Sottodirectory trovate
        # Sezione di output
        if len(elenco) == 0:
            print("Nessuna directory presente.")
        else:
            print(f"Directory presenti ({len(elenco)}):")
            for d in elenco:
                print(" -", d)
    except PermissionError:
        print("Errore: permessi insufficienti per leggere il percorso.")
