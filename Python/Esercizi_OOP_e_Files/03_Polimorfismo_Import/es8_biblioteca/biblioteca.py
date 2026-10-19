"""
Autore: Luca Tarallo
Data: 18/10/2026

Titolo: Sistema modulare per gestione biblioteca - File 2: biblioteca.py
        Definisce la classe Biblioteca, che gestisce un catalogo di oggetti Media.
"""
from typing import List, Tuple

from media import Media, Libro, DVD

##
## Classi:
##

class Biblioteca:
    """
    Classe: Biblioteca
    Catalogo di libri e DVD.
    Attributi:
        List[Media] __elenco_media -> lista (privata) dei media presenti in biblioteca
    """

    def __init__(self) -> None:
        """
        Funzione: __init__
        Costruttore: inizializza una lista vuota di media.
        Parametri formali:
            nessuno
        Valore di ritorno:
            None
        """
        self.__elenco_media: List[Media] = []

    def aggiungi_media(self, media: Media) -> None:
        """
        Funzione: aggiungi_media
        Aggiunge un elemento al catalogo.
        Parametri formali:
            Media media -> libro o DVD da aggiungere
        Valore di ritorno:
            None
        """
        self.__elenco_media.append(media)

    def rimuovi_media(self, titolo: str) -> bool:
        """
        Funzione: rimuovi_media
        Rimuove dal catalogo il primo elemento con il titolo indicato (senza distinguere
        maiuscole e minuscole).
        Parametri formali:
            str titolo -> titolo dell'elemento da rimuovere
        Valore di ritorno:
            bool -> True se l'elemento è stato trovato e rimosso, False altrimenti
        """
        for media in self.__elenco_media:
            if media.titolo.lower() == titolo.lower():
                self.__elenco_media.remove(media)
                return True
        return False

    def cerca_per_autore(self, autore: str) -> List[Media]:
        """
        Funzione: cerca_per_autore
        Cerca gli elementi il cui autore contiene il testo indicato (senza distinguere
        maiuscole e minuscole).
        Parametri formali:
            str autore -> nome (o parte del nome) dell'autore
        Valore di ritorno:
            List[Media] -> lista degli elementi trovati (vuota se nessuno corrisponde)
        """
        risultati: List[Media] = []
        for media in self.__elenco_media:
            if autore.lower() in media.autore.lower():
                risultati.append(media)
        return risultati

    def stampa_catalogo(self) -> None:
        """
        Funzione: stampa_catalogo
        Stampa tutti i media del catalogo con il relativo tempo di lettura o di visione.
        Parametri formali:
            nessuno
        Valore di ritorno:
            None
        """
        print("=== CATALOGO BIBLIOTECA ===")
        if len(self.__elenco_media) == 0:
            print("Il catalogo è vuoto")
            return
        ultimo_indice = len(self.__elenco_media) - 1
        for indice, media in enumerate(self.__elenco_media):
            print(media)
            if isinstance(media, Libro):
                print("Tempo di lettura stimato:", media.tempo_lettura())
            elif isinstance(media, DVD):
                print("Tempo di visione:", media.tempo_visione())
            if indice < ultimo_indice:
                print("---")

    def get_statistiche(self) -> Tuple[int, int]:
        """
        Funzione: get_statistiche
        Conta i libri e i DVD presenti nel catalogo.
        Parametri formali:
            nessuno
        Valore di ritorno:
            Tuple[int, int] -> coppia (numero di libri, numero di DVD)
        """
        numero_libri = 0
        numero_dvd = 0
        for media in self.__elenco_media:
            if isinstance(media, Libro):
                numero_libri += 1
            elif isinstance(media, DVD):
                numero_dvd += 1
        return numero_libri, numero_dvd
