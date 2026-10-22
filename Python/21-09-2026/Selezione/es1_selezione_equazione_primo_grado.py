"""
Autore: Luca Tarallo
Data: 21/09/2026
Titolo: Scrivere un programma che legga i coefficienti a e b di un'equazione
        di primo grado ax=b e ne scriva la soluzione (attenzione al dominio
        del coefficiente a).
"""
# Sezione di input Dati
print("Inserisci i coefficienti a e b")
a = int(input("a= "))
b = int(input("b= "))

# Inizializzazioni variabili
x = 0

# Elaborazione con gestione del dominio di a
if a != 0:
    x = b / a
    print("La soluzione è:", x)
else:
    if b == 0:
        print("Equazione indeterminata: infinite soluzioni (ogni x è soluzione)")
    else:
        print("Equazione impossibile: nessuna soluzione")
