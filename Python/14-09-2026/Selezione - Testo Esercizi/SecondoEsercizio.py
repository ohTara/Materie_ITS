"""
Autore: Luca Tarallo
Data: 14/09/2026
Titolo: Scrivere un programma che legga i coefficienti a, b e c di un'equazione
        di secondo grado ax^2+bx+c=0 e ne scriva le soluzioni.
"""
import math

# Sezione di input Dati
a = int(input("a= "))
b = int(input("b= "))
c = int(input("c= "))

# Inizializzazioni variabili
delta = 0

# Elaborazione
if a == 0:
    # Caso degenere: equazione di primo grado bx + c = 0
    if b != 0:
        x = -c / b
        print("Equazione di primo grado. La soluzione è:", x)
    else:
        if c == 0:
            print("Equazione indeterminata: infinite soluzioni")
        else:
            print("Equazione impossibile: nessuna soluzione")
else:
    # Caso generale: equazione di secondo grado
    delta = b**2 - 4*a*c

    # Eventuali sotto processi di Elaborazione
    if delta > 0:
        x1 = (-b + math.sqrt(delta)) / (2*a)
        x2 = (-b - math.sqrt(delta)) / (2*a)
        print("Due soluzioni reali distinte:")
        print("x1 =", x1)
        print("x2 =", x2)
    elif delta == 0:
        x = -b / (2*a)
        print("Soluzione reale doppia: x =", x)
    else:
        print("Nessuna soluzione reale (discriminante negativo)")