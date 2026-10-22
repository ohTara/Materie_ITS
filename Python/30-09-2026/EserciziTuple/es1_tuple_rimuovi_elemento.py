"""
Autore: Luca Tarallo
Data: 30/09/2026

Titolo: Scrivere un programma per rimuovere l'n-esimo elemento da una tupla non vuota.
"""

##
## Funzioni:
##

def rimuovi_elemento(tpl: tuple, n: int) -> tuple:
    """
    Funzione: rimuovi_elemento
    Rimuove l'elemento in posizione n da una tupla non vuota.
    Parametri formali:
        tuple tpl -> tupla di partenza (non vuota)
        int n -> posizione (indice da 0) dell'elemento da rimuovere
    Valore di ritorno:
        tuple -> nuova tupla priva dell'elemento in posizione n
    """
    nuova_tupla = tpl[:n] + tpl[n + 1:]
    return nuova_tupla


"""
Programma principale
Richiama la funzione rimuovi_elemento su una tupla di esempio e ne stampa il
risultato, verificando prima il dominio (tupla non vuota, posizione valida).
"""
# Sezione di input Dati
tplIN = (10, 20, 30, 40, 50)  # tupla di esempio (non vuota)
n = 2  # posizione dell'elemento da rimuovere

# Inizializzazioni variabili
tplOUT = ()  # conterrà la tupla risultante dopo la rimozione

# Elaborazione
if len(tplIN) == 0:
    print("Errore: la tupla non può essere vuota")
elif n < 0 or n >= len(tplIN):
    print("Errore: posizione fuori dal range della tupla (0-" + str(len(tplIN) - 1) + ")")
else:
    tplOUT = rimuovi_elemento(tplIN, n)

    # Sezione di output
    print("Tupla originale:", tplIN)
    print("Posizione da rimuovere:", n)
    print("Tupla risultante:", tplOUT)
