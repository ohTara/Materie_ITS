"""
Autore: Luca Tarallo
Data: 19/10/2026

Titolo: 1 - Creare una classe Calcolo con un costruttore di default (senza parametri) che
            consenta di eseguire vari calcoli su numeri interi.
        2 - Creare un metodo chiamato Factorial() che permetta di calcolare il fattoriale di
            un intero. Testare il metodo istanziando la classe.
        3 - Creare un metodo chiamato Sum() che consenta di calcolare la somma dei primi n
            interi 1 + 2 + 3 + .. + n. Provare questo metodo.
        4 - Creare un metodo tableMult() che crea e visualizza la tabellina di un dato intero.
            Quindi creare un metodo allTablesMult() per visualizzare tutte le tabelline dei
            numeri interi 1, 2, 3, ..., 9.
"""
from typing import List

##
## Classi:
##

class Calcolo:
    """
    Classe: Calcolo
    Raccoglie alcuni calcoli su numeri interi. Non ha attributi: il costruttore è quello
    di default, senza parametri.
    """

    def __init__(self) -> None:
        """
        Funzione: __init__
        Costruttore di default (senza parametri).
        Parametri formali:
            nessuno
        Valore di ritorno:
            None -> il costruttore non restituisce valori
        """

    def Factorial(self, n: int) -> int:
        """
        Funzione: Factorial
        Calcola il fattoriale di un intero (0! = 1). Solleva ValueError se n è negativo.
        Parametri formali:
            int n -> intero non negativo di cui calcolare il fattoriale
        Valore di ritorno:
            int -> n!
        """
        if n < 0:
            raise ValueError("il fattoriale non è definito per i numeri negativi")
        fattoriale = 1
        for i in range(2, n + 1):
            fattoriale *= i
        return fattoriale

    def Sum(self, n: int) -> int:
        """
        Funzione: Sum
        Calcola la somma dei primi n interi: 1 + 2 + 3 + ... + n. Solleva ValueError se n è negativo.
        Parametri formali:
            int n -> ultimo intero della somma (>= 0)
        Valore di ritorno:
            int -> somma dei primi n interi (0 se n = 0)
        """
        if n < 0:
            raise ValueError("n deve essere maggiore o uguale a zero")
        somma = 0
        for i in range(1, n + 1):
            somma += i
        return somma

    def tableMult(self, numero: int) -> List[int]:
        """
        Funzione: tableMult
        Crea e visualizza la tabellina di un intero (moltiplicatori da 1 a 10).
        Parametri formali:
            int numero -> intero di cui costruire la tabellina
        Valore di ritorno:
            List[int] -> lista dei 10 prodotti della tabellina
        """
        prodotti: List[int] = []
        for moltiplicatore in range(1, 11):
            prodotti.append(numero * moltiplicatore)
            print(f"{numero} x {moltiplicatore:2d} = {prodotti[-1]}")
        return prodotti

    def allTablesMult(self) -> None:
        """
        Funzione: allTablesMult
        Visualizza le tabelline di tutti gli interi da 1 a 9, richiamando tableMult().
        Parametri formali:
            nessuno
        Valore di ritorno:
            None
        """
        for numero in range(1, 10):
            print(f"--- Tabellina del {numero} ---")
            self.tableMult(numero)


"""
Programma principale
Istanzia la classe Calcolo e prova tutti i metodi, compresi i casi limite.
"""
# Sezione di input Dati
# (nessun input da tastiera: i valori di prova sono scritti nel codice)

# Inizializzazioni variabili
calcolo = Calcolo()  # oggetto su cui eseguire i calcoli

# Elaborazione e Sezione di output
print("Fattoriale di 5:", calcolo.Factorial(5))   # atteso 120
print("Fattoriale di 0:", calcolo.Factorial(0))   # atteso 1 (caso limite)
print("Somma dei primi 10 interi:", calcolo.Sum(10))  # atteso 55
print("Somma dei primi 0 interi:", calcolo.Sum(0))    # atteso 0 (caso limite)

# Eventuali sotto processi di Elaborazione: casi limite
try:
    calcolo.Factorial(-3)
except ValueError as errore:
    print("Errore:", errore)

try:
    calcolo.Sum(-1)
except ValueError as errore:
    print("Errore:", errore)

print("--- Tabellina del 7 ---")
calcolo.tableMult(7)
print("--- Tutte le tabelline da 1 a 9 ---")
calcolo.allTablesMult()
