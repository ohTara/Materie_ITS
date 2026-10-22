"""
Autore: Luca Tarallo
Data: 22/09/2026
Titolo: Conversione temperatura: implementare una funzione convertiCF che converta una
        temperatura espressa in gradi Fahrenheit in una temperatura espressa in gradi Celsius.
        Usare la formula: C = (F - 32) * 5 / 9
        Creare un programma principale che richiami la funzione e ne stampi il risultato
        visualizzando solo 3 cifre decimali.
"""


def convertiCF(f):
    """Converte una temperatura da gradi Fahrenheit a gradi Celsius."""
    return (f - 32) * 5 / 9


# Sezione di input Dati
f = float(input("Inserisci la temperatura in gradi Fahrenheit: "))

# Elaborazione
c = convertiCF(f)

# Sezione di output (3 cifre decimali)
print(f"{f}°F equivalgono a {c:.3f}°C")
