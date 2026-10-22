"""
Autore: Luca Tarallo
Data: 30/09/2026

Titolo: Scrivere un programma per sostituire l'ultimo valore delle liste in una tupla
        con un valore richiesto in input.

Esempio:
valore: 100
TuplaIN: ([10, 20, 40], 'a', [40, 50, 60], 23, [70, 80, 90])
TuplaOUT: ([10, 20, 100], 'a', [40, 50, 100], 23, [70, 80, 100])
"""

##
## Funzioni:
##

def sostituisci_ultimo_valore_liste(tpl: tuple, valore: int) -> tuple:
    """
    Funzione: sostituisci_ultimo_valore_liste
    Scorre gli elementi di una tupla e, per ogni elemento di tipo lista, sostituisce
    l'ultimo valore della lista con il valore passato come parametro. Gli elementi
    che non sono di tipo lista restano invariati.
    Parametri formali:
        tuple tpl -> tupla di partenza, può contenere elementi di tipo lista
        int valore -> nuovo valore da inserire come ultimo elemento di ogni lista trovata
    Valore di ritorno:
        tuple -> nuova tupla con le liste modificate
    """
    elementi_modificati = []
    for elemento in tpl:
        if isinstance(elemento, list) and len(elemento) > 0:
            nuova_lista = elemento[:-1] + [valore]
            elementi_modificati.append(nuova_lista)
        else:
            elementi_modificati.append(elemento)
    return tuple(elementi_modificati)


"""
Programma principale
Chiede in input il valore da sostituire, richiama la funzione
sostituisci_ultimo_valore_liste su una tupla di esempio e ne stampa il risultato.
"""
# Sezione di input Dati
valore = int(input("Inserisci il nuovo valore da sostituire: "))
TuplaIN = ([10, 20, 40], 'a', [40, 50, 60], 23, [70, 80, 90])

# Inizializzazioni variabili
TuplaOUT = ()  # conterrà la tupla con le liste modificate

# Elaborazione
TuplaOUT = sostituisci_ultimo_valore_liste(TuplaIN, valore)

# Sezione di output
print("Tupla originale:", TuplaIN)
print("Tupla risultante:", TuplaOUT)
