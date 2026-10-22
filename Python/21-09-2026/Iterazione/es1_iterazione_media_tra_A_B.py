"""
Autore: Luca Tarallo
Data: 14/09/2026
Titolo: Si hanno in input due numeri reali A e B e una successione di numeri reali positivi
        che termina con il valore 0. Si vuole in output la media dei soli numeri compresi tra A e B.

Esempio:
INPUT: A=2 B=3.5 Successione: -3.4 4 2.5 3 10 0
OUTPUT: 2.75 [ perché media=(2.5+3)/2=2.75 ]
"""
# Sezione di input Dati
A = float(input("A= "))
B = float(input("B= "))

# Inizializzazioni variabili
somma = 0
conteggio = 0
numero = float(input("Inserisci un numero (0 per terminare): "))

# Elaborazione (ciclo con condizione di uscita in testa)
while numero != 0:
    if A <= numero <= B:
        somma += numero
        conteggio += 1
    numero = float(input("Inserisci un numero (0 per terminare): "))

# Sezione di output
if conteggio > 0:
    media = somma / conteggio
    print("La media dei numeri compresi tra", A, "e", B, "è:", media)
else:
    print("Nessun numero compreso tra", A, "e", B, "è stato inserito")
