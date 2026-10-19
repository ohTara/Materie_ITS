"""
Autore: Luca Tarallo
Data: 18/10/2026

Titolo: Polimorfismo con operatori e collezioni eterogenee. Classi NumeroComplesso (forma
        algebrica, somma, prodotto, modulo) e Vettore2D (somma, prodotto per uno scalare,
        modulo) con overloading degli operatori + e *. Funzione stampa_operazioni(obj1, obj2)
        e programma principale che prova le operazioni e scorre una lista mista di numeri
        complessi e vettori calcolando il modulo di ogni elemento.
"""
import math
from typing import List, Union

##
## Classi:
##

class NumeroComplesso:
    """
    Classe: NumeroComplesso
    Numero complesso in forma algebrica a + ib.
    Attributi:
        float parte_reale -> parte reale (a)
        float parte_immaginaria -> coefficiente della parte immaginaria (b)
        str etichetta -> nome mostrato nelle stampe (attributo di classe)
    """

    etichetta = "Numero complesso"

    def __init__(self, parte_reale: float, parte_immaginaria: float) -> None:
        """
        Funzione: __init__
        Parametri formali:
            float parte_reale -> parte reale a
            float parte_immaginaria -> coefficiente immaginario b
        Valore di ritorno:
            None
        """
        self.parte_reale = parte_reale
        self.parte_immaginaria = parte_immaginaria

    def __str__(self) -> str:
        """
        Funzione: __str__
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> forma algebrica: "a + bi" oppure "a - |b|i" se b è negativo
        """
        if self.parte_immaginaria < 0:
            return f"{self.parte_reale} - {abs(self.parte_immaginaria)}i"
        return f"{self.parte_reale} + {self.parte_immaginaria}i"

    def __add__(self, altro: "NumeroComplesso") -> "NumeroComplesso":
        """
        Funzione: __add__
        Somma: (a+ib) + (c+id) = (a+c) + i(b+d)
        Parametri formali:
            NumeroComplesso altro -> secondo addendo
        Valore di ritorno:
            NumeroComplesso -> somma dei due numeri complessi
        """
        return NumeroComplesso(self.parte_reale + altro.parte_reale,
                               self.parte_immaginaria + altro.parte_immaginaria)

    def __mul__(self, altro: "NumeroComplesso") -> "NumeroComplesso":
        """
        Funzione: __mul__
        Prodotto: (a+ib)(c+id) = (ac - bd) + i(ad + bc)
        Parametri formali:
            NumeroComplesso altro -> secondo fattore
        Valore di ritorno:
            NumeroComplesso -> prodotto dei due numeri complessi
        """
        a = self.parte_reale
        b = self.parte_immaginaria
        c = altro.parte_reale
        d = altro.parte_immaginaria
        return NumeroComplesso(a * c - b * d, a * d + b * c)

    def modulo(self) -> float:
        """
        Funzione: modulo
        Modulo: |a+ib| = radice quadrata di (a² + b²)
        Parametri formali:
            nessuno
        Valore di ritorno:
            float -> modulo del numero complesso
        """
        return math.sqrt(self.parte_reale ** 2 + self.parte_immaginaria ** 2)


class Vettore2D:
    """
    Classe: Vettore2D
    Vettore del piano (x, y).
    Attributi:
        float x -> componente orizzontale
        float y -> componente verticale
        str etichetta -> nome mostrato nelle stampe (attributo di classe)
    """

    etichetta = "Vettore"

    def __init__(self, x: float, y: float) -> None:
        """
        Funzione: __init__
        Parametri formali:
            float x -> componente orizzontale
            float y -> componente verticale
        Valore di ritorno:
            None
        """
        self.x = x
        self.y = y

    def __str__(self) -> str:
        """
        Funzione: __str__
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> stringa nel formato "(x, y)"
        """
        return f"({self.x}, {self.y})"

    def __add__(self, altro: "Vettore2D") -> "Vettore2D":
        """
        Funzione: __add__
        Somma: (a,b) + (c,d) = (a+c, b+d)
        Parametri formali:
            Vettore2D altro -> secondo addendo
        Valore di ritorno:
            Vettore2D -> vettore somma
        """
        return Vettore2D(self.x + altro.x, self.y + altro.y)

    def __mul__(self, scalare: float) -> "Vettore2D":
        """
        Funzione: __mul__
        Prodotto per uno scalare: (a,b) * n = (a*n, b*n)
        Parametri formali:
            float scalare -> numero per cui moltiplicare il vettore
        Valore di ritorno:
            Vettore2D -> vettore moltiplicato per lo scalare
        """
        return Vettore2D(self.x * scalare, self.y * scalare)

    def modulo(self) -> float:
        """
        Funzione: modulo
        Lunghezza del vettore: |(a,b)| = radice quadrata di (a² + b²)
        Parametri formali:
            nessuno
        Valore di ritorno:
            float -> modulo del vettore
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)


##
## Funzioni:
##

def stampa_operazioni(obj1: Union[NumeroComplesso, Vettore2D],
                      obj2: Union[NumeroComplesso, Vettore2D]) -> None:
    """
    Funzione: stampa_operazioni
    Stampa i due oggetti con il loro modulo e la loro somma. Funziona sia con due numeri
    complessi sia con due vettori (polimorfismo).
    Parametri formali:
        NumeroComplesso | Vettore2D obj1 -> primo oggetto
        NumeroComplesso | Vettore2D obj2 -> secondo oggetto (dello stesso tipo del primo)
    Valore di ritorno:
        None
    """
    print(f"{obj1.etichetta}: {obj1}, modulo: {round(obj1.modulo(), 3)}")
    print(f"{obj2.etichetta}: {obj2}, modulo: {round(obj2.modulo(), 3)}")
    print("Somma:", obj1 + obj2)


"""
Programma principale
Crea numeri complessi e vettori, prova le operazioni su ciascun tipo, poi scorre una lista
mista calcolando e stampando il modulo di ogni elemento.
"""
# Sezione di input Dati
# (nessun input da tastiera: i valori sono scritti nel codice)

# Inizializzazioni variabili
c1 = NumeroComplesso(3, 4)    # primo numero complesso
c2 = NumeroComplesso(1, -2)   # secondo numero complesso (parte immaginaria negativa)
v1 = Vettore2D(5, 12)         # primo vettore
v2 = Vettore2D(3, 4)          # secondo vettore
collezione: List[Union[NumeroComplesso, Vettore2D]] = []  # lista mista

# Elaborazione
collezione.append(c1)
collezione.append(v1)
collezione.append(c2)

# Sezione di output
stampa_operazioni(c1, c2)
print("Prodotto:", c1 * c2)
print("---")

stampa_operazioni(v1, v2)
print("Vettore", v1, "per lo scalare 2:", v1 * 2)
print("---")

print("Collezione mista:")
for elemento in collezione:
    print(f"Elemento: {elemento}, modulo: {round(elemento.modulo(), 3)}")
print("---")
