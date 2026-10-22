"""
Autore: Luca Tarallo
Data: 22/09/2026
Titolo: Scrivere un programma per rimuovere l'n-esimo carattere da una stringa non vuota.
        Progettare una funzione che accetti la stringa, la posizione del carattere e
        restituisca la stringa modificata.
"""


def rimuovi_carattere(stringa, posizione):
    """Restituisce la stringa senza il carattere in posizione 'posizione' (indice da 0)."""
    return stringa[:posizione] + stringa[posizione + 1:]


# Sezione di input Dati
testo = input("Inserisci una stringa non vuota: ")
n = int(input("Inserisci la posizione del carattere da rimuovere (da 0): "))

# Elaborazione con controllo del dominio
if len(testo) == 0:
    print("Errore: la stringa non può essere vuota")
elif n < 0 or n >= len(testo):
    print("Errore: posizione fuori dal range della stringa (0-" + str(len(testo) - 1) + ")")
else:
    risultato = rimuovi_carattere(testo, n)

    # Sezione di output
    print("Stringa originale:", testo)
    print("Stringa modificata:", risultato)
