"""
Autore: Luca Tarallo
Data: 19/10/2026

Titolo: Scrivere un programma che, leggendo da tastiera una stringa, la salvi su file
        "stringa.txt". Successivamente aprire il file "stringa.txt" e verificare il salvataggio.
"""
from pathlib import Path

##
## Funzioni:
##

def salva_stringa(percorso: Path, testo: str) -> None:
    """
    Funzione: salva_stringa
    Scrive la stringa sul file indicato (se il file esiste già viene sovrascritto).
    Parametri formali:
        Path percorso -> percorso del file da scrivere
        str testo -> stringa da salvare
    Valore di ritorno:
        None
    """
    with open(percorso, "w", encoding="utf-8") as file:
        file.write(testo)


def leggi_file(percorso: Path) -> str:
    """
    Funzione: leggi_file
    Legge e restituisce l'intero contenuto di un file di testo.
    Parametri formali:
        Path percorso -> percorso del file da leggere
    Valore di ritorno:
        str -> contenuto del file
    """
    with open(percorso, "r", encoding="utf-8") as file:
        contenuto = file.read()
    return contenuto


"""
Programma principale
Legge una stringa da tastiera, la salva su "stringa.txt", riapre il file e verifica che
il contenuto letto coincida con la stringa inserita.
"""
# Sezione di input Dati
stringa = input("Inserisci la stringa da salvare: ")

# Inizializzazioni variabili
percorso_file = Path(__file__).resolve().parent / "stringa.txt"  # file creato accanto allo script

# Elaborazione
try:
    salva_stringa(percorso_file, stringa)
    contenuto_letto = leggi_file(percorso_file)

    # Sezione di output
    print("Stringa salvata in:", percorso_file)
    print("Contenuto letto dal file:", contenuto_letto)
    if contenuto_letto == stringa:
        print("Verifica riuscita: il contenuto del file coincide con la stringa inserita")
    else:
        print("Verifica fallita: il contenuto del file è diverso dalla stringa inserita")
except OSError as errore:
    print("Errore di accesso al file:", errore)
