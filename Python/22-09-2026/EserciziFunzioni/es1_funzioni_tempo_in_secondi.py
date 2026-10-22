"""
Autore: Luca Tarallo
Data: 22/09/2026
Titolo: Creare una funzione che riceva una quantità di tempo in formato ore, minuti e secondi
        e la restituisca espressa solamente in secondi. Successivamente creare un programma
        principale che chieda in input due quantità di tempo e stampi in output quale quantità
        di tempo è maggiore. La funzione deve avere i parametri formali con valori predefiniti.
"""


def tempo_in_secondi(ore=0, minuti=0, secondi=0):
    """Converte una quantità di tempo (ore, minuti, secondi) in secondi totali."""
    return ore * 3600 + minuti * 60 + secondi


# Sezione di input Dati
print("Inserisci la prima quantità di tempo")
ore1 = int(input("Ore: "))
minuti1 = int(input("Minuti: "))
secondi1 = int(input("Secondi: "))

print("Inserisci la seconda quantità di tempo")
ore2 = int(input("Ore: "))
minuti2 = int(input("Minuti: "))
secondi2 = int(input("Secondi: "))

# Elaborazione
tempo1 = tempo_in_secondi(ore1, minuti1, secondi1)
tempo2 = tempo_in_secondi(ore2, minuti2, secondi2)

# Sezione di output
if tempo1 > tempo2:
    print("La prima quantità di tempo è maggiore:", tempo1, "secondi contro", tempo2, "secondi")
elif tempo2 > tempo1:
    print("La seconda quantità di tempo è maggiore:", tempo2, "secondi contro", tempo1, "secondi")
else:
    print("Le due quantità di tempo sono uguali:", tempo1, "secondi")
