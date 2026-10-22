"""
Autore: Luca Tarallo
Data: 06/10/2026

Titolo: Scrivete uno script Python per generare e stampare un dizionario che contenga un
        numero (compreso tra 1 e n) nella forma (x, x*x).

Esempio:
n = 5
Dizionario: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
"""

##
## Funzioni:
##

def genera_quadrati(n: int) -> dict:
    """
    Funzione: genera_quadrati
    Genera un dizionario contenente, per ogni numero x compreso tra 1 e n,
    la coppia chiave-valore (x, x*x).
    Parametri formali:
        int n -> valore massimo (incluso) dell'intervallo di generazione
    Valore di ritorno:
        dict -> dizionario con chiave x e valore x*x, per x da 1 a n
    """
    diz = {}
    for x in range(1, n + 1):
        diz[x] = x * x
    return diz


"""
Programma principale
Chiede in input il valore di n, richiama la funzione genera_quadrati
e ne stampa il risultato.
"""
# Sezione di input Dati
n = int(input("Inserisci il valore di n: "))

# Inizializzazioni variabili
diz_quadrati = {}  # conterrà il dizionario {x: x*x}

# Elaborazione con controllo del dominio
if n < 1:
    print("Errore: n deve essere maggiore o uguale a 1")
else:
    diz_quadrati = genera_quadrati(n)

    # Sezione di output
    print("Dizionario:", diz_quadrati)
