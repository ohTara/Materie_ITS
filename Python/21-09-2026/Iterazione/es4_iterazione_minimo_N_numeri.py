"""
Autore: Luca Tarallo
Data: 21/09/2026
Titolo: Scrivere un programma che legga N numeri da tastiera, N dato in input,
        e ne restituisca il minimo.
"""
# Sezione di input Dati
N = int(input("Quanti numeri vuoi inserire? "))

# Inizializzazioni variabili
minimo = 0

# Elaborazione
for i in range(N):
    numero = float(input("Inserisci un numero: "))
    if i == 0:
        minimo = numero
    elif numero < minimo:
        minimo = numero

# Sezione di output
print("Il minimo tra i numeri inseriti è:", minimo)
