"""
Autore: Luca Tarallo
Data: 30/09/2026

Titolo: Scrivere un programma per invertire una tupla.

Esempio:
tplIN = ('a', 'c', 'f')
tplOUT = ('f', 'c', 'a')
"""

##
## Funzioni:
##

def inverti_tupla(tpl: tuple) -> tuple:
    """
    Funzione: inverti_tupla
    Restituisce una nuova tupla con gli elementi nell'ordine inverso rispetto
    alla tupla di partenza.
    Parametri formali:
        tuple tpl -> tupla di partenza
    Valore di ritorno:
        tuple -> tupla con gli elementi in ordine inverso
    """
    return tpl[::-1]


"""
Programma principale
Richiama la funzione inverti_tupla su una tupla di esempio e ne stampa il risultato.
"""
# Sezione di input Dati
tplIN = ('a', 'c', 'f')

# Inizializzazioni variabili
tplOUT = ()  # conterrà la tupla invertita

# Elaborazione
tplOUT = inverti_tupla(tplIN)

# Sezione di output
print("Tupla originale:", tplIN)
print("Tupla invertita:", tplOUT)
