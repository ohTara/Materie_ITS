"""
Autore: Luca Tarallo
Data: 14/09/2026
Titolo: Scrivere un programma che legga le lunghezze dei tre lati di un triangolo
        a, b, c e ne calcoli il perimetro e l'area S, quest'ultima tramite
        la formula di Erone: S = sqrt(p(p-a)(p-b)(p-c)), dove p è il semiperimetro.
"""
import math

# Sezione di input Dati
a = float(input("a= "))
b = float(input("b= "))
c = float(input("c= "))

# Inizializzazioni variabili
perimetro = 0
p = 0
s = 0

# Elaborazione
if a > 0 and b > 0 and c > 0 and (a + b > c) and (a + c > b) and (b + c > a):
    perimetro = a + b + c
    p = perimetro / 2

    # Eventuali sotto processi di Elaborazione
    s = math.sqrt(p * (p - a) * (p - b) * (p - c))

    # Sezione di output
    print("Perimetro:", perimetro)
    print("Area:", s)
else:
    print("Errore: i valori inseriti non formano un triangolo valido")