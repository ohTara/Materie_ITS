"""
Autore: Luca Tarallo
Data: 15/09/2026
Titolo: Leggere una successione di numeri interi passati dall’utente, fermandosi al primo numero
        che rende la successione non crescente e restituendo quanti numeri formano la
        successione inserita.
        Esempio:
        INPUT: 2 5 28 10 OUTPUT: 3
        INPUT: 2 -2 OUTPUT: 1

"""

# Sezione di input dati

numero = int(input("Inserisci il primo numero della successione: "))

# Inizializzazioni variabili

conta = 1
precedente = numero

# Elaborazione

successione_crescente = True

while successione_crescente:

    numero = int(input("Inserisci il prossimo numero della successione: "))

    # Eventuali sotto processi di Elaborazione

    if numero > precedente:
        conta = conta + 1
        precedente = numero
    else:
        successione_crescente = False

# Sezione di output

print("La successione è formata da", conta, "numeri")
print("Fine elaborazione")