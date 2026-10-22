"""
Autore: Luca Tarallo
Data: 22/09/2026
Titolo: Scrivere un programma che dica se una stringa è palindroma.

Esempio:
str="ABBA" PALINDROMA
str="PIPPO" NON PALINDROMA
"""


def is_palindroma(stringa):
    """Restituisce True se la stringa letta al contrario è uguale a se stessa."""
    return stringa == stringa[::-1]


# Sezione di input Dati
testo = input("Inserisci una stringa: ")

# Elaborazione
if is_palindroma(testo):
    esito = "PALINDROMA"
else:
    esito = "NON PALINDROMA"

# Sezione di output
print('str="' + testo + '"', esito)
