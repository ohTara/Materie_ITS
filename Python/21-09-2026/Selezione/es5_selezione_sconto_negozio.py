"""
Autore: Luca Tarallo
Data: 21/09/2026
Titolo: Un negoziante per ogni spesa di importo superiore a 100 € effettua uno sconto del 5%,
        se l'importo risulta superiore a 300€ lo sconto è del 10%.
        Scrivere un programma che richieda all'utente l'ammontare della spesa
        e visualizzi quindi l'importo effettivo da pagare.
"""
# Sezione di input Dati
spesa = float(input("Spesa: "))

# Inizializzazioni variabili
sconto = 0
spesa_finale = 0

# Elaborazione
if spesa < 0:
    print("Errore: la spesa non può essere negativa")
else:
    if spesa > 300:
        sconto = 0.1
    elif spesa > 100:
        sconto = 0.05

    # Eventuali sotto processi di Elaborazione
    spesa_finale = spesa * (1 - sconto)

    # Sezione di output
    print("Lo sconto è del", sconto * 100, "%. Totale della spesa:", spesa_finale, "€")
