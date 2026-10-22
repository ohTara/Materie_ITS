"""
Autore: Luca Tarallo
Data: 06/10/2026

Titolo: Progettare una funzione che accetti un numero indefinito di dizionari e restituisca
        un dizionario che è la concatenazione di tutti i dizionari indicati come parametro
        formale alla funzione. Scrivete uno script che utilizzi tale funzione.

Esempio:
diz1 = {'v1':1,'v2':2,'v3':3}
diz2 = {'v4':4,'v5':5,'v6':6}
diz3 = {'v7':7,'v8':8}
Dizionario restituito: {'v1': 1, 'v2': 2, 'v3': 3, 'v4': 4, 'v5': 5, 'v6': 6, 'v7': 7, 'v8': 8}
"""

##
## Funzioni:
##

def concatena_dizionari(*dizionari: dict) -> dict:
    """
    Funzione: concatena_dizionari
    Accetta un numero indefinito di dizionari e restituisce un unico dizionario
    risultante dall'unione delle loro coppie chiave-valore.
    Parametri formali:
        dict *dizionari -> numero arbitrario di dizionari da concatenare
    Valore di ritorno:
        dict -> dizionario risultante dall'unione di tutti i dizionari passati
    """
    risultato = {}
    for d in dizionari:
        for chiave in d:
            risultato[chiave] = d[chiave]
    return risultato


"""
Programma principale
Richiama la funzione concatena_dizionari su tre dizionari di esempio
e ne stampa il risultato.
"""
# Sezione di input Dati
diz1 = {'v1': 1, 'v2': 2, 'v3': 3}
diz2 = {'v4': 4, 'v5': 5, 'v6': 6}
diz3 = {'v7': 7, 'v8': 8}

# Inizializzazioni variabili
diz_finale = {}  # conterrà il dizionario risultante dalla concatenazione

# Elaborazione
diz_finale = concatena_dizionari(diz1, diz2, diz3)

# Sezione di output
print("Dizionario 1:", diz1)
print("Dizionario 2:", diz2)
print("Dizionario 3:", diz3)
print("Dizionario restituito:", diz_finale)
