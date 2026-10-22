"""
Autore: Luca Tarallo
Data: 21/09/2026
Titolo: Scrivere un programma che chieda quanti alunni ci sono in una classe, poi per ogni
        alunno fa inserire M voti, M dato in input, e ne scrive la media.
"""
# Sezione di input Dati
n_alunni = int(input("Quanti alunni ci sono nella classe? "))
M = int(input("Quanti voti per alunno (M)? "))

# Elaborazione (ciclo esterno sugli alunni, ciclo interno sui voti)
for i in range(n_alunni):
    somma = 0
    print("Alunno", i + 1)
    for j in range(M):
        voto = float(input("  Voto " + str(j + 1) + ": "))
        somma += voto
    media = somma / M

    # Sezione di output
    print("  Media dell'alunno", i + 1, "è:", media)
