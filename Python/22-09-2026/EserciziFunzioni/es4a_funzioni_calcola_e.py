"""
Autore: Luca Tarallo
Data: 22/09/2026
Titolo: Punto 4.a - Scrivere una funzione che restituisca un valore approssimato di e
        all'ennesimo termine, dove N è inserito come parametro formale alla funzione.
        La funzione calcola_e deve richiamare la funzione di calcolo del fattoriale.

Esempio:
calcola_e(3) restituirà il valore di e calcolato con tre termini della serie, cioè:
e = 1/0! + 1/1! + 1/2! = 1 + 1 + 0.5 = 2.5
"""


def fattoriale(n):
    """Calcola n! in modo ricorsivo."""
    if n <= 1:
        return 1
    else:
        return n * fattoriale(n - 1)


def calcola_e(n):
    """Restituisce il valore approssimato di e sommando i primi n termini della serie
    e = somma per i da 0 a n-1 di 1/i!"""
    somma = 0
    for i in range(n):
        somma += 1 / fattoriale(i)
    return somma


# Sezione di input Dati
N = int(input("Inserisci il numero di termini N: "))

# Elaborazione
e_approssimato = calcola_e(N)

# Sezione di output
print("Il valore approssimato di e con", N, "termini è:", e_approssimato)
