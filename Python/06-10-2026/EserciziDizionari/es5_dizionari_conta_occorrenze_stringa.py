"""
Autore: Luca Tarallo
Data: 06/10/2026

Titolo: Scrivete un programma Python per creare un dizionario da una stringa. Le lettere
        della stringa rappresentano le chiavi, i valori rappresentano le occorrenze della
        chiave nella stringa.

Esempio:
stringa = "ciao mamma"
Dizionario: {'c': 1, 'i': 1, 'a': 3, 'o': 1, ' ': 1, 'm': 3}
"""

##
## Funzioni:
##

def conta_occorrenze_stringa(stringa: str) -> dict:
    """
    Funzione: conta_occorrenze_stringa
    Costruisce un dizionario in cui le chiavi sono i caratteri distinti della stringa
    e i valori rappresentano il numero di occorrenze di ciascun carattere nella stringa.
    Parametri formali:
        str stringa -> stringa da analizzare
    Valore di ritorno:
        dict -> dizionario {carattere: numero di occorrenze}
    """
    diz = {}
    for carattere in stringa:
        if carattere in diz:
            diz[carattere] += 1
        else:
            diz[carattere] = 1
    return diz


"""
Programma principale
Chiede in input una stringa, richiama la funzione conta_occorrenze_stringa
e ne stampa il risultato.
"""
# Sezione di input Dati
stringa = input("Inserisci una stringa: ")

# Inizializzazioni variabili
diz_occorrenze = {}  # conterrà il dizionario {carattere: occorrenze}

# Elaborazione
diz_occorrenze = conta_occorrenze_stringa(stringa)

# Sezione di output
print("Stringa:", stringa)
print("Dizionario:", diz_occorrenze)
