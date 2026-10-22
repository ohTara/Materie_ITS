"""
Autore: Luca Tarallo
Data: 30/09/2026

Titolo: Scrivere un programma per contare gli elementi in una lista finché non si
        incontra un elemento di tipo tupla. [Suggerimento: si usi la funzione isinstance()]
"""

##
## Funzioni:
##

def conta_elementi_fino_a_tupla(lista: list) -> int:
    """
    Funzione: conta_elementi_fino_a_tupla
    Conta gli elementi di una lista scorrendola dall'inizio, fermandosi non appena
    incontra il primo elemento di tipo tupla (che non viene conteggiato).
    Parametri formali:
        list lista -> lista di elementi eterogenei da esaminare
    Valore di ritorno:
        int -> numero di elementi contati prima di incontrare una tupla
               (coincide con la lunghezza della lista se non è presente alcuna tupla)
    """
    conteggio = 0
    for elemento in lista:
        if isinstance(elemento, tuple):
            break
        conteggio += 1
    return conteggio


"""
Programma principale
Richiama la funzione conta_elementi_fino_a_tupla su una lista di esempio
(contenente una tupla al suo interno) e ne stampa il risultato.
"""
# Sezione di input Dati
listaIN = [5, "ciao", 3.14, (1, 2), 10, 20]  # lista di esempio con una tupla al 4° posto

# Inizializzazioni variabili
risultato = 0  # conterrà il numero di elementi contati

# Elaborazione
risultato = conta_elementi_fino_a_tupla(listaIN)

# Sezione di output
print("Lista originale:", listaIN)
print("Numero di elementi contati prima della tupla:", risultato)
