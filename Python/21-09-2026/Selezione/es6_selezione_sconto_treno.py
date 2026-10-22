"""
Autore: Luca Tarallo
Data: 21/09/2026
Titolo: Su una linea ferroviaria, rispetto alla tariffa piena, gli utenti pensionati usufruiscono di uno
        sconto del 10%, gli studenti del 15% e i disoccupati del 25%. Codificando i pensionati con
        un 1, gli studenti con un 2 e i disoccupati con un 3, scrivere un programma che, richiesto il
        costo di un biglietto e l'eventuale condizione particolare dell'utente, visualizzi l'importo da pagare.
"""
# Sezione di input Dati
costo = float(input("Costo del biglietto: "))
codice = int(input("Condizione (1=pensionato, 2=studente, 3=disoccupato, 0=nessuna): "))

# Inizializzazioni variabili
sconto = 0
importo_finale = 0

# Elaborazione
if costo <= 0:
    print("Errore: il costo del biglietto deve essere positivo")
else:
    if codice == 1:
        sconto = 0.10
    elif codice == 2:
        sconto = 0.15
    elif codice == 3:
        sconto = 0.25
    elif codice == 0:
        sconto = 0
    else:
        print("Errore: codice condizione non valido")

    # Eventuali sotto processi di Elaborazione
    if codice in (0, 1, 2, 3):
        importo_finale = costo * (1 - sconto)

        # Sezione di output
        print("Sconto applicato:", sconto * 100, "%. Importo da pagare:", importo_finale, "€")
