"""
Autore: Luca Tarallo
Data: 15/09/2026
Titolo: Scrivere un programma che chieda quanti alunni ci sono in una classe poi per ogni alunno fa inserire M voti, M dato in input, e ne scrive la media.
"""

# Sezione di input dati

n_alunni = int(input("Inserisci il numero di alunni della classe: "))
m_voti = int(input("Inserisci il numero di voti per ogni alunno: "))

# Inizializzazioni variabili

# (nessuna inizializzazione globale necessaria: somma e conteggio sono per singolo alunno)

# Elaborazione

for i in range(n_alunni):

    print("Alunno numero", i + 1)
    somma_voti = 0

    # Eventuali sotto processi di Elaborazione

    for j in range(m_voti):

        voto = float(input("Inserisci il voto: "))
        somma_voti = somma_voti + voto

    media_voti = somma_voti / m_voti

    # Sezione di output

    print("La media dei voti dell'alunno numero", i + 1, "è:", media_voti)

print("Fine elaborazione")