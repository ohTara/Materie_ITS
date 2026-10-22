"""
Autore: Luca Tarallo
Data: 22/09/2026
Titolo: Creare una funzione che abbia come parametri formali un numero arbitrario di valori
        numerici. Si vuole che restituisca la somma dei soli numeri pari e il prodotto dei
        soli numeri dispari. Successivamente creare un programma che richiami tale funzione
        e che stampi in output i risultati. No standard input.
"""


def somma_pari_prodotto_dispari(*numeri):
    """Restituisce (somma dei numeri pari, prodotto dei numeri dispari) tra quelli passati."""
    somma_pari = 0
    prodotto_dispari = 1
    for n in numeri:
        if n % 2 == 0:
            somma_pari += n
        else:
            prodotto_dispari *= n
    return somma_pari, prodotto_dispari


# Programma principale (nessun input da tastiera, valori predefiniti nel codice)
valori = (3, 4, 7, 10, 15, 2, 9)
somma, prodotto = somma_pari_prodotto_dispari(*valori)

# Sezione di output
print("Numeri considerati:", valori)
print("Somma dei numeri pari:", somma)
print("Prodotto dei numeri dispari:", prodotto)
