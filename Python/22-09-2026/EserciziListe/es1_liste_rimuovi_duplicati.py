"""
Autore: Luca Tarallo
Data: 22/09/2026
Titolo: Scrivere un programma python che rimuova gli elementi duplicati da una lista.

Esempio:
listaIN = [2, -4, 5, 6, 5, 5, 2]
listaOUT = [2, -4, 5, 6]
"""
# Sezione di input Dati
listaIN = [2, -4, 5, 6, 5, 5, 2]

# Inizializzazioni variabili
listaOUT = []

# Elaborazione (mantiene l'ordine di prima apparizione)
for elemento in listaIN:
    if elemento not in listaOUT:
        listaOUT.append(elemento)

# Sezione di output
print("Lista originale:", listaIN)
print("Lista senza duplicati:", listaOUT)
