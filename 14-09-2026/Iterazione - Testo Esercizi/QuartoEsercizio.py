"""
Autore: Luca Tarallo
Data: 15/09/2026
Titolo: Scrivere un programma che legga N numeri da tastiera, N dato in input, e ne restituisca il minimo.

"""

# Sezione di input dati

n = int(input("Inserisci il numero di valori da leggere: "))

# Inizializzazioni variabili

minimo = float(input("Inserisci il primo numero: "))

# Elaborazione

for i in range(n - 1):

    numero = float(input("Inserisci il prossimo numero: "))

    # Eventuali sotto processi di Elaborazione

    if numero < minimo:
        minimo = numero

# Sezione di output

print("Il valore minimo inserito è:", minimo)

print("Fine elaborazione")