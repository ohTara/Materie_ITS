"""
Autore: Luca Tarallo
Data: 22/09/2026
Titolo: Scrivere un programma che date due liste stampi "OK" se hanno almeno un membro
        comune, altrimenti stampi "KO".

Esempio:
lista1=[1,5,8] lista2=[3,1,10]  -> output: "OK"
lista1=[1,5,8] lista2=[3,11,10] -> output: "KO"
"""
# Sezione di input Dati
lista1 = [1, 5, 8]
lista2 = [3, 6, 10]

# Elaborazione (intersezione tramite insiemi)
elementi_comuni = set(lista1) & set(lista2)

# Sezione di output
if len(elementi_comuni) > 0:
    print("OK")
else:
    print("KO")
