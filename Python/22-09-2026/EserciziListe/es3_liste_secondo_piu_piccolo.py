"""
Autore: Luca Tarallo
Data: 22/09/2026
Titolo: Scrivi un programma per trovare il secondo numero più piccolo in una lista.

Nota: si considera il secondo valore DISTINTO più piccolo (se la lista contiene
duplicati del minimo, questi non vengono considerati come "secondo" valore).
"""
# Sezione di input Dati
lista = [4, 2, 7, 2, 9, 1, 1]

# Inizializzazioni variabili
valori_distinti = sorted(set(lista))

# Elaborazione con controllo del dominio
if len(valori_distinti) < 2:
    print("Errore: la lista deve contenere almeno due valori distinti")
else:
    secondo_piu_piccolo = valori_distinti[1]

    # Sezione di output
    print("Lista originale:", lista)
    print("Il secondo numero più piccolo è:", secondo_piu_piccolo)
