"""
Autore: Luca Tarallo
Data: 15/09/2026
Titolo: Si hanno in input due numeri reali A e B e una successione di numeri reali positivi che
        termina con il valore 0. Si vuole in output la media dei soli numeri compresi tra A e B.
        Esempio:
        INPUT: A=2 B= 3.5 Successione: -3.4 4 2.5 3 10 0
        OUTPUT: 2.75 [ perchè media=(2.5+3)/2=2.75]
"""

# Sezione di input dati

a = float(input("Inserisci il valore di A: "))
b = float(input("Inserisci il valore di B: "))

# Inizializzazioni variabili

somma = 0
conta = 0

# Elaborazione

numero = float(input("Inserisci un numero della successione (0 per terminare): "))

while numero != 0:

    # Eventuali sotto processi di Elaborazione

    if a <= numero <= b:
        somma = somma + numero
        conta = conta + 1

    numero = float(input("Inserisci un numero della successione (0 per terminare): "))

# Sezione di output

if conta > 0:
    media = somma / conta
    print("La media dei numeri compresi tra", a, "e", b, "è:", media)
else:
    print("Nessun numero della successione è compreso tra", a, "e", b)
print("Fine elaborazione")