"""
Autore: Luca Tarallo
Data: 15/09/2026
Titolo: Si hanno in input N saldi di conti correnti bancari. Si vuole in output la media aritmetica dei
        soli conti correnti che hanno un saldo negativo.

"""

# Sezione di input dati

n = int(input("Inserisci il numero di conti correnti: "))

# Inizializzazioni variabili

somma = 0
conta = 0

# Elaborazione

for i in range(n):

    saldo = float(input("Inserisci il saldo del conto corrente: "))

    # Eventuali sotto processi di Elaborazione

    if saldo < 0:
        somma = somma + saldo
        conta = conta + 1

# Sezione di output

if conta > 0:
    media = somma / conta
    print("La media dei saldi negativi è:", media)
else:
    print("Non ci sono conti correnti con saldo negativo")

print("Fine elaborazione")