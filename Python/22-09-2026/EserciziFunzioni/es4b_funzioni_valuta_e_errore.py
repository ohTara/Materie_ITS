"""
Autore: Luca Tarallo
Data: 22/09/2026
Titolo: Punto 4.b - Supponendo di porre il numero di Nepero = 2.718281828459045, si dica
        errore = calcola_e(N) - Nepero, sia l'errore che si commette nella valutazione di e.
        Modificare la funzione che restituisce la valutazione di e con N termini in modo
        che restituisca anche l'errore commesso nella valutazione. Il numero di Nepero è
        memorizzato in una variabile globale.

Esempio:
valuta_e(3) restituisce il valore calcolato al punto 4.a (2.5) e l'errore commesso
(0.218281828459045), che rappresenta la differenza tra 2.718281828459045 e 2.5.

Nota: l'errore viene restituito in valore assoluto (abs), coerente con l'esempio del testo,
che mostra un risultato positivo anche se calcola_e(3) è minore del numero di Nepero.
"""

# Variabile globale
NEPERO = 2.718281828459045


def fattoriale(n):
    """Calcola n! in modo ricorsivo."""
    if n <= 1:
        return 1
    else:
        return n * fattoriale(n - 1)


def calcola_e(n):
    """Restituisce il valore approssimato di e con n termini della serie."""
    somma = 0
    for i in range(n):
        somma += 1 / fattoriale(i)
    return somma


def valuta_e(n):
    """Restituisce una coppia (valore approssimato di e, errore commesso in valore assoluto)."""
    valore = calcola_e(n)
    errore = abs(valore - NEPERO)
    return valore, errore


# Sezione di input Dati
N = int(input("Inserisci il numero di termini N: "))

# Elaborazione
valore_e, errore_e = valuta_e(N)

# Sezione di output
print("Valore approssimato di e con", N, "termini:", valore_e)
print("Errore commesso rispetto al numero di Nepero:", errore_e)
