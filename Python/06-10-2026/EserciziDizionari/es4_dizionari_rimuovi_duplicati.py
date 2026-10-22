"""
Autore: Luca Tarallo
Data: 06/10/2026

Titolo: Scrivete un programma Python per rimuovere i duplicati dal dizionario.
"""

##
## Funzioni:
##

def rimuovi_duplicati(diz: dict) -> dict:
    """
    Funzione: rimuovi_duplicati
    Restituisce un nuovo dizionario in cui, per ogni valore duplicato presente nel
    dizionario di partenza, viene mantenuta solo la prima chiave associata a quel
    valore (seguendo l'ordine di inserimento originale).
    Parametri formali:
        dict diz -> dizionario di partenza, può contenere valori duplicati
    Valore di ritorno:
        dict -> nuovo dizionario privo di valori duplicati
    """
    risultato = {}
    valori_visti = []
    for chiave in diz:
        valore = diz[chiave]
        if valore not in valori_visti:
            risultato[chiave] = valore
            valori_visti.append(valore)
    return risultato


"""
Programma principale
Richiama la funzione rimuovi_duplicati su un dizionario di esempio
contenente valori ripetuti e ne stampa il risultato.
"""
# Sezione di input Dati
diz = {'a': 10, 'b': 20, 'c': 10, 'd': 30, 'e': 20}

# Inizializzazioni variabili
diz_senza_duplicati = {}  # conterrà il dizionario privo di valori duplicati

# Elaborazione
diz_senza_duplicati = rimuovi_duplicati(diz)

# Sezione di output
print("Dizionario originale:", diz)
print("Dizionario senza duplicati:", diz_senza_duplicati)
