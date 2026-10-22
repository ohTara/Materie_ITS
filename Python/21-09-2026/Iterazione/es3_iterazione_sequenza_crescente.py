"""
Autore: Luca Tarallo
Data: 21/09/2026
Titolo: Leggere una successione di numeri interi passati dall'utente, fermandosi al primo
        numero che rende la successione non crescente e restituendo quanti numeri formano
        la successione inserita.

Esempio:
INPUT: 2 5 28 10   OUTPUT: 3
INPUT: 2 -2        OUTPUT: 1
"""
# Sezione di input Dati
numero = int(input("Inserisci un numero: "))

# Inizializzazioni variabili
conteggio = 1
precedente = numero
continua = True

# Elaborazione
while continua:
    numero = int(input("Inserisci un numero: "))
    if numero > precedente:
        conteggio += 1
        precedente = numero
    else:
        continua = False

# Sezione di output
print("La successione crescente inserita è formata da", conteggio, "numeri")
