"""
Autore: Luca Tarallo
Data: 21/09/2026
Titolo: Si hanno in input N saldi di conti correnti bancari. Si vuole in output la media
        aritmetica dei soli conti correnti che hanno un saldo negativo.
"""
# Sezione di input Dati
N = int(input("Numero di conti correnti: "))

# Inizializzazioni variabili
somma = 0
conteggio = 0

# Elaborazione
for i in range(N):
    saldo = float(input("Saldo conto " + str(i + 1) + ": "))
    if saldo < 0:
        somma += saldo
        conteggio += 1

# Sezione di output
if conteggio > 0:
    media = somma / conteggio
    print("La media dei saldi negativi è:", media)
else:
    print("Nessun conto con saldo negativo")
