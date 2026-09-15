"""
Autore: Luca Tarallo
Data: 14/09/2026
Titolo: Scrivere un programma che legga il raggio r di una circonferenza e ne calcoli l'area e la lunghezza.
"""
# Sezione di input Dati
r = float(input("r= "))
# Inizializzazioni variabili
area = 0
lunghezza = 0
# Elaborazione
if r > 0:
    area = 3.14 * r**2
    lunghezza = 2 * 3.14 * r
    # Sezione di output
    print("Area:", area)
    print("Lunghezza:", lunghezza)
else:
    print("Il raggio deve essere maggiore di 0") 