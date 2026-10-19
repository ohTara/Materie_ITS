"""
Autore: Luca Tarallo
Data: 18/10/2026

Titolo: Sistema modulare per gestione biblioteca - File 1: media.py
        Definisce la classe base Media e le classi derivate Libro e DVD.
"""

##
## Funzioni:
##

def formatta_durata(minuti: int) -> str:
    """
    Funzione: formatta_durata
    Converte una durata in minuti nel formato "X ore e Y minuti".
    Parametri formali:
        int minuti -> durata in minuti (>= 0)
    Valore di ritorno:
        str -> durata nel formato "X ore e Y minuti"
    """
    ore = minuti // 60
    minuti_residui = minuti % 60
    return f"{ore} ore e {minuti_residui} minuti"


##
## Classi:
##

class Media:
    """
    Classe: Media
    Classe base di tutti gli elementi del catalogo.
    Attributi:
        str titolo -> titolo dell'opera
        str autore -> autore (o regista) dell'opera
        int anno -> anno di pubblicazione
    """

    def __init__(self, titolo: str, autore: str, anno: int) -> None:
        """
        Funzione: __init__
        Parametri formali:
            str titolo -> titolo dell'opera
            str autore -> autore dell'opera
            int anno -> anno di pubblicazione
        Valore di ritorno:
            None
        """
        self.titolo = titolo
        self.autore = autore
        self.anno = anno

    def get_info(self) -> str:
        """
        Funzione: get_info
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> informazioni base nel formato '"titolo" di autore (anno)'
        """
        return f'"{self.titolo}" di {self.autore} ({self.anno})'

    def __str__(self) -> str:
        """
        Funzione: __str__
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> rappresentazione testuale (coincide con get_info())
        """
        return self.get_info()


class Libro(Media):
    """
    Classe: Libro
    Libro del catalogo.
    Attributi aggiuntivi:
        int numero_pagine -> numero di pagine del libro
    """

    def __init__(self, titolo: str, autore: str, anno: int, numero_pagine: int) -> None:
        """
        Funzione: __init__
        Parametri formali:
            str titolo -> titolo del libro
            str autore -> autore del libro
            int anno -> anno di pubblicazione
            int numero_pagine -> numero di pagine
        Valore di ritorno:
            None
        """
        super().__init__(titolo, autore, anno)
        self.numero_pagine = numero_pagine

    def get_info(self) -> str:
        """
        Funzione: get_info
        Overriding: aggiunge il tipo e il numero di pagine.
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> informazioni complete del libro
        """
        return f"Libro: {super().get_info()} - {self.numero_pagine} pagine"

    def tempo_lettura(self) -> str:
        """
        Funzione: tempo_lettura
        Calcola il tempo di lettura stimato (1 pagina = 2 minuti).
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> tempo di lettura nel formato "M minuti (X ore e Y minuti)"
        """
        minuti = self.numero_pagine * 2
        return f"{minuti} minuti ({formatta_durata(minuti)})"


class DVD(Media):
    """
    Classe: DVD
    DVD del catalogo.
    Attributi aggiuntivi:
        int durata_minuti -> durata del film in minuti
    """

    def __init__(self, titolo: str, autore: str, anno: int, durata_minuti: int) -> None:
        """
        Funzione: __init__
        Parametri formali:
            str titolo -> titolo del film
            str autore -> regista
            int anno -> anno di uscita
            int durata_minuti -> durata in minuti
        Valore di ritorno:
            None
        """
        super().__init__(titolo, autore, anno)
        self.durata_minuti = durata_minuti

    def get_info(self) -> str:
        """
        Funzione: get_info
        Overriding: aggiunge il tipo e la durata.
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> informazioni complete del DVD
        """
        return f"DVD: {super().get_info()} - {self.durata_minuti} minuti"

    def tempo_visione(self) -> str:
        """
        Funzione: tempo_visione
        Restituisce la durata del DVD in ore e minuti.
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> durata nel formato "X ore e Y minuti" (come nell'esempio di output del testo)
        """
        return formatta_durata(self.durata_minuti)
