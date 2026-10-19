"""
Autore: Luca Tarallo
Data: 19/10/2026

Titolo: Creare una classe Rettangolo con attributi base e altezza. Costruire tutti i metodi
        setter e getter per gli attributi. Aggiungere i metodi per il calcolo dell'area e del
        perimetro. Implementare un metodo di nome "contiene" che ha come parametro un oggetto
        rettangolo. Tale metodo deve restituire True se il rettangolo oggetto chiamante contiene
        il rettangolo oggetto parametro, False se non lo contiene. Un rettangolo "contiene" un
        altro quando la sua base e la sua altezza sono maggiori rispettivamente della base e
        dell'altezza del secondo rettangolo.
"""

##
## Classi:
##

class Rettangolo:
    """
    Classe: Rettangolo
    Rappresenta un rettangolo.
    Attributi:
        float __base -> lunghezza della base (maggiore di zero)
        float __altezza -> lunghezza dell'altezza (maggiore di zero)
    """

    def __init__(self, base: float, altezza: float) -> None:
        """
        Funzione: __init__
        Costruttore: crea un rettangolo validando i valori tramite i setter.
        Parametri formali:
            float base -> base del rettangolo (> 0)
            float altezza -> altezza del rettangolo (> 0)
        Valore di ritorno:
            None -> il costruttore non restituisce valori
        """
        self.set_base(base)
        self.set_altezza(altezza)

    def get_base(self) -> float:
        """
        Funzione: get_base
        Parametri formali:
            nessuno
        Valore di ritorno:
            float -> base del rettangolo
        """
        return self.__base

    def set_base(self, base: float) -> None:
        """
        Funzione: set_base
        Modifica la base (solleva ValueError se non positiva).
        Parametri formali:
            float base -> nuova base
        Valore di ritorno:
            None
        """
        if base <= 0:
            raise ValueError("la base deve essere maggiore di zero")
        self.__base = base

    def get_altezza(self) -> float:
        """
        Funzione: get_altezza
        Parametri formali:
            nessuno
        Valore di ritorno:
            float -> altezza del rettangolo
        """
        return self.__altezza

    def set_altezza(self, altezza: float) -> None:
        """
        Funzione: set_altezza
        Modifica l'altezza (solleva ValueError se non positiva).
        Parametri formali:
            float altezza -> nuova altezza
        Valore di ritorno:
            None
        """
        if altezza <= 0:
            raise ValueError("l'altezza deve essere maggiore di zero")
        self.__altezza = altezza

    def area(self) -> float:
        """
        Funzione: area
        Calcola l'area del rettangolo (base * altezza).
        Parametri formali:
            nessuno
        Valore di ritorno:
            float -> area del rettangolo
        """
        return self.__base * self.__altezza

    def perimetro(self) -> float:
        """
        Funzione: perimetro
        Calcola il perimetro del rettangolo (2 * (base + altezza)).
        Parametri formali:
            nessuno
        Valore di ritorno:
            float -> perimetro del rettangolo
        """
        return 2 * (self.__base + self.__altezza)

    def contiene(self, altro: "Rettangolo") -> bool:
        """
        Funzione: contiene
        Verifica se il rettangolo chiamante contiene il rettangolo passato come parametro:
        base e altezza devono essere entrambe strettamente maggiori di quelle dell'altro.
        Parametri formali:
            Rettangolo altro -> rettangolo da confrontare
        Valore di ritorno:
            bool -> True se il chiamante contiene "altro", False altrimenti
        """
        return self.__base > altro.get_base() and self.__altezza > altro.get_altezza()

    def __str__(self) -> str:
        """
        Funzione: __str__
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> stringa nel formato "Rettangolo(base=B, altezza=H)"
        """
        return f"Rettangolo(base={self.__base}, altezza={self.__altezza})"


"""
Programma principale
Istanzia alcuni rettangoli, ne calcola area e perimetro, prova il metodo contiene
e verifica i casi limite (valori non validi, rettangoli identici).
"""
# Sezione di input Dati
# (nessun input da tastiera: gli oggetti sono istanziati con valori predefiniti)

# Inizializzazioni variabili
grande = Rettangolo(10, 6)    # rettangolo grande
piccolo = Rettangolo(4, 3)    # rettangolo contenuto in "grande"
largo = Rettangolo(12, 5)     # rettangolo più largo ma più basso di "grande"

# Elaborazione
piccolo.set_base(5)           # prova dei setter

# Sezione di output
print(grande, "- area:", grande.area(), "- perimetro:", grande.perimetro())
print(piccolo, "- area:", piccolo.area(), "- perimetro:", piccolo.perimetro())
print("grande contiene piccolo?", grande.contiene(piccolo))   # atteso True
print("piccolo contiene grande?", piccolo.contiene(grande))   # atteso False
print("grande contiene largo?", grande.contiene(largo))       # atteso False (base 10 < 12)
print("grande contiene se stesso?", grande.contiene(grande))  # atteso False (confronto stretto)

# Eventuali sotto processi di Elaborazione: casi limite
print("--- Casi limite ---")
try:
    Rettangolo(0, 5)
except ValueError as errore:
    print("Errore:", errore)

try:
    grande.set_altezza(-2)
except ValueError as errore:
    print("Errore:", errore)
