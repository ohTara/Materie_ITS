"""
Autore: Luca Tarallo
Data: 06/10/2026

Titolo: Scrivete un programma Python per ottenere il valore massimo e minimo in un dizionario.
"""

##
## Funzioni:
##

def massimo_minimo_dizionario(diz: dict) -> tuple:
    """
    Funzione: massimo_minimo_dizionario
    Determina il valore massimo e il valore minimo tra i valori di un dizionario non vuoto.
    Parametri formali:
        dict diz -> dizionario di cui calcolare massimo e minimo (non vuoto)
    Valore di ritorno:
        tuple -> coppia (valore massimo, valore minimo) tra i valori del dizionario
    """
    valori = list(diz.values())
    massimo = valori[0]
    minimo = valori[0]
    for v in valori:
        if v > massimo:
            massimo = v
        if v < minimo:
            minimo = v
    return massimo, minimo


"""
Programma principale
Richiama la funzione massimo_minimo_dizionario su un dizionario di esempio
e ne stampa il risultato, verificando prima il dominio (dizionario non vuoto).
"""
# Sezione di input Dati
diz = {'a': 10, 'b': 3, 'c': 27, 'd': 15}

# Inizializzazioni variabili
# massimo = 0  # conterrà il valore massimo trovato
# minimo = 0  # conterrà il valore minimo trovato

# Elaborazione con controllo del dominio
if len(diz) == 0:
    print("Errore: il dizionario non può essere vuoto")
else:
    massimo, minimo = massimo_minimo_dizionario(diz)

    # Sezione di output
    print("Dizionario:", diz)
    print("Valore massimo:", massimo)
    print("Valore minimo:", minimo)
