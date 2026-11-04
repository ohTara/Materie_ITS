'''
Autore: Luca Tarallo
Data: 27/10/2026
Titolo: Esaminare tutte le directories sotto un dato percorso e contare tutti i files
        con una determinata estensione data in input (primo livello di profondita').
'''
import os

##
## Funzioni:
##
def normalizza_estensione(estensione: str) -> str:
    '''
    Funzione: normalizza_estensione
    Rende l'estensione confrontabile: minuscola e con il punto iniziale.

    Parametri formali:
    str estensione -> estensione inserita dall'utente ("txt" oppure ".TXT")

    Valore di ritorno:
    str -> estensione normalizzata (es. ".txt")
    '''
    ext = estensione.strip().lower()  # Estensione ripulita
    if ext != "" and not ext.startswith("."):
        ext = "." + ext
    return ext


def conta_file_in_directory(directory: str, estensione: str) -> int:
    '''
    Funzione: conta_file_in_directory
    Conta i file (non le cartelle) di una directory con l'estensione data.

    Parametri formali:
    str directory -> percorso della directory da esaminare
    str estensione -> estensione normalizzata (es. ".txt")

    Valore di ritorno:
    int -> numero di file con quell'estensione
    '''
    conteggio = 0  # File trovati
    for nome in os.listdir(directory):
        percorso_completo = os.path.join(directory, nome)
        if os.path.isfile(percorso_completo) and nome.lower().endswith(estensione):
            conteggio += 1
    return conteggio


def conta_in_sottodirectory(percorso: str, estensione: str) -> dict:
    '''
    Funzione: conta_in_sottodirectory
    Per ogni sottodirectory di primo livello conta i file con l'estensione data.

    Parametri formali:
    str percorso -> percorso base
    str estensione -> estensione normalizzata (es. ".txt")

    Valore di ritorno:
    dict -> {nome sottodirectory: numero di file}
    '''
    risultati = {}  # Conteggio per ogni sottodirectory
    for nome in os.listdir(percorso):
        sotto = os.path.join(percorso, nome)
        if os.path.isdir(sotto):
            try:
                risultati[nome] = conta_file_in_directory(sotto, estensione)
            except PermissionError:
                risultati[nome] = 0  # Directory non leggibile: non contata
    return risultati


'''
Programma principale
Chiede un percorso e un'estensione, conta i file per ogni sottodirectory
di primo livello e stampa il dettaglio e il totale.
'''
# Sezione di input Dati
percorso_input = input("Percorso da esaminare: ").strip()      # Percorso base
estensione_input = input("Estensione da cercare (es. txt): ")  # Estensione richiesta

# Inizializzazioni variabili
estensione = normalizza_estensione(estensione_input)  # Estensione normalizzata

# Elaborazione
if not os.path.isdir(percorso_input):
    print("Errore: il percorso non esiste o non e' una directory.")
elif estensione == "":
    print("Errore: estensione vuota.")
else:
    per_directory = conta_in_sottodirectory(percorso_input, estensione)  # Dettaglio
    totale = sum(per_directory.values())                                 # Somma complessiva
    # Sezione di output
    for nome, n in per_directory.items():
        print(f" - {nome}: {n}")
    print(f"Totale file '{estensione}' nelle sottodirectory: {totale}")
