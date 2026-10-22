"""
Autore: Luca Tarallo
Data: 21/09/2026
Titolo: Scrivere un programma che legga il raggio r di una circonferenza
        e ne calcoli l'area e la lunghezza.
"""
import math

# Sezione di input Dati
r = float(input("r= "))

# Inizializzazioni variabili
area = 0
lunghezza = 0

# Elaborazione
if r > 0:
    area = math.pi * r**2
    lunghezza = 2 * math.pi * r

    # Sezione di output
    print("L'area è:", area)
    print("La lunghezza è:", lunghezza)
else:
    print("Errore: il raggio deve essere un valore positivo")
