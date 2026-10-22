"""
Autore: Luca Tarallo
Data: 22/09/2026
Titolo: Scrivere un programma Python per dividere una data lista in due parti in cui
        viene data la lunghezza della prima parte della lista.

Esempio:
Lista originale: [1, 1, 2, 3, 4, 4, 5, 1]
Lunghezza della prima parte della lista: 3
Output: Prima parte: [1, 1, 2] , Seconda parte: [3, 4, 4, 5, 1]
"""
# Sezione di input Dati
lista_originale = [1, 1, 2, 3, 4, 4, 5, 1]
lunghezza_prima_parte = 3

# Elaborazione con controllo del dominio
if lunghezza_prima_parte < 0 or lunghezza_prima_parte > len(lista_originale):
    print("Errore: lunghezza non valida per questa lista")
else:
    prima_parte = lista_originale[:lunghezza_prima_parte]
    seconda_parte = lista_originale[lunghezza_prima_parte:]

    # Sezione di output
    print("Lista originale:", lista_originale)
    print("Lunghezza della prima parte della lista:", lunghezza_prima_parte)
    print("Output: Prima parte:", prima_parte, ", Seconda parte:", seconda_parte)
