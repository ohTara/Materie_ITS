"""
Autore: Luca Tarallo
Data: 19/10/2026

Titolo: Si definisca una classe Persona con attributi nome, indirizzo ed età, con costruttore,
        overriding del metodo __str__ e tutti i metodi getter e setter. Si derivino da Persona
        le classi Studente (attributi aggiuntivi: scuola, media voti) e Lavoratore (attributi
        aggiuntivi: azienda, stipendio), con relativi getter e setter, overriding dei costruttori
        e del metodo __str__. Provare le tre classi istanziando almeno un oggetto per classe
        e provando qualche metodo.
"""
from typing import List

##
## Classi:
##

class Persona:
    """
    Classe: Persona
    Classe base che rappresenta una persona.
    Attributi:
        str _nome -> nome e cognome
        str _indirizzo -> indirizzo di residenza
        int _eta -> età (tra 0 e 120)
    """

    def __init__(self, nome: str, indirizzo: str, eta: int) -> None:
        """
        Funzione: __init__
        Costruttore: crea una persona validando i valori tramite i setter.
        Parametri formali:
            str nome -> nome e cognome (non vuoto)
            str indirizzo -> indirizzo (non vuoto)
            int eta -> età (tra 0 e 120)
        Valore di ritorno:
            None
        """
        self.set_nome(nome)
        self.set_indirizzo(indirizzo)
        self.set_eta(eta)

    def get_nome(self) -> str:
        """
        Funzione: get_nome
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> nome della persona
        """
        return self._nome

    def set_nome(self, nome: str) -> None:
        """
        Funzione: set_nome
        Parametri formali:
            str nome -> nuovo nome (non vuoto, altrimenti ValueError)
        Valore di ritorno:
            None
        """
        if nome.strip() == "":
            raise ValueError("il nome non può essere vuoto")
        self._nome = nome

    def get_indirizzo(self) -> str:
        """
        Funzione: get_indirizzo
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> indirizzo della persona
        """
        return self._indirizzo

    def set_indirizzo(self, indirizzo: str) -> None:
        """
        Funzione: set_indirizzo
        Parametri formali:
            str indirizzo -> nuovo indirizzo (non vuoto, altrimenti ValueError)
        Valore di ritorno:
            None
        """
        if indirizzo.strip() == "":
            raise ValueError("l'indirizzo non può essere vuoto")
        self._indirizzo = indirizzo

    def get_eta(self) -> int:
        """
        Funzione: get_eta
        Parametri formali:
            nessuno
        Valore di ritorno:
            int -> età della persona
        """
        return self._eta

    def set_eta(self, eta: int) -> None:
        """
        Funzione: set_eta
        Parametri formali:
            int eta -> nuova età (tra 0 e 120, altrimenti ValueError)
        Valore di ritorno:
            None
        """
        if eta < 0 or eta > 120:
            raise ValueError("l'età deve essere compresa tra 0 e 120 anni")
        self._eta = eta

    def __str__(self) -> str:
        """
        Funzione: __str__
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> descrizione con nome, indirizzo ed età
        """
        return f"Nome: {self._nome}, Indirizzo: {self._indirizzo}, Età: {self._eta}"


class Studente(Persona):
    """
    Classe: Studente
    Estende Persona con i dati scolastici.
    Attributi aggiuntivi:
        str _scuola -> scuola frequentata
        float _media_voti -> media dei voti (tra 0 e 10)
    """

    def __init__(self, nome: str, indirizzo: str, eta: int, scuola: str, media_voti: float) -> None:
        """
        Funzione: __init__
        Overriding del costruttore: inizializza la parte Persona e gli attributi aggiuntivi.
        Parametri formali:
            str nome -> nome e cognome
            str indirizzo -> indirizzo
            int eta -> età
            str scuola -> scuola frequentata (non vuota)
            float media_voti -> media dei voti (tra 0 e 10)
        Valore di ritorno:
            None
        """
        super().__init__(nome, indirizzo, eta)
        self.set_scuola(scuola)
        self.set_media_voti(media_voti)

    def get_scuola(self) -> str:
        """
        Funzione: get_scuola
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> scuola frequentata
        """
        return self._scuola

    def set_scuola(self, scuola: str) -> None:
        """
        Funzione: set_scuola
        Parametri formali:
            str scuola -> nuova scuola (non vuota, altrimenti ValueError)
        Valore di ritorno:
            None
        """
        if scuola.strip() == "":
            raise ValueError("la scuola non può essere vuota")
        self._scuola = scuola

    def get_media_voti(self) -> float:
        """
        Funzione: get_media_voti
        Parametri formali:
            nessuno
        Valore di ritorno:
            float -> media dei voti
        """
        return self._media_voti

    def set_media_voti(self, media_voti: float) -> None:
        """
        Funzione: set_media_voti
        Parametri formali:
            float media_voti -> nuova media (tra 0 e 10, altrimenti ValueError)
        Valore di ritorno:
            None
        """
        if media_voti < 0 or media_voti > 10:
            raise ValueError("la media dei voti deve essere compresa tra 0 e 10")
        self._media_voti = media_voti

    def __str__(self) -> str:
        """
        Funzione: __str__
        Overriding: aggiunge scuola e media voti alla descrizione della Persona.
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> descrizione completa dello studente
        """
        return f"{super().__str__()}, Scuola: {self._scuola}, Media voti: {self._media_voti}"


class Lavoratore(Persona):
    """
    Classe: Lavoratore
    Estende Persona con i dati lavorativi.
    Attributi aggiuntivi:
        str _azienda -> azienda in cui lavora
        float _stipendio -> stipendio mensile (>= 0)
    """

    def __init__(self, nome: str, indirizzo: str, eta: int, azienda: str, stipendio: float) -> None:
        """
        Funzione: __init__
        Overriding del costruttore: inizializza la parte Persona e gli attributi aggiuntivi.
        Parametri formali:
            str nome -> nome e cognome
            str indirizzo -> indirizzo
            int eta -> età
            str azienda -> azienda (non vuota)
            float stipendio -> stipendio mensile (>= 0)
        Valore di ritorno:
            None
        """
        super().__init__(nome, indirizzo, eta)
        self.set_azienda(azienda)
        self.set_stipendio(stipendio)

    def get_azienda(self) -> str:
        """
        Funzione: get_azienda
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> azienda in cui lavora
        """
        return self._azienda

    def set_azienda(self, azienda: str) -> None:
        """
        Funzione: set_azienda
        Parametri formali:
            str azienda -> nuova azienda (non vuota, altrimenti ValueError)
        Valore di ritorno:
            None
        """
        if azienda.strip() == "":
            raise ValueError("l'azienda non può essere vuota")
        self._azienda = azienda

    def get_stipendio(self) -> float:
        """
        Funzione: get_stipendio
        Parametri formali:
            nessuno
        Valore di ritorno:
            float -> stipendio mensile
        """
        return self._stipendio

    def set_stipendio(self, stipendio: float) -> None:
        """
        Funzione: set_stipendio
        Parametri formali:
            float stipendio -> nuovo stipendio (>= 0, altrimenti ValueError)
        Valore di ritorno:
            None
        """
        if stipendio < 0:
            raise ValueError("lo stipendio non può essere negativo")
        self._stipendio = stipendio

    def __str__(self) -> str:
        """
        Funzione: __str__
        Overriding: aggiunge azienda e stipendio alla descrizione della Persona.
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> descrizione completa del lavoratore
        """
        return f"{super().__str__()}, Azienda: {self._azienda}, Stipendio: {self._stipendio}"


"""
Programma principale
Istanzia un oggetto per ciascuna classe, prova getter e setter e verifica i casi limite.
"""
# Sezione di input Dati
# (nessun input da tastiera: gli oggetti sono istanziati con valori predefiniti)

# Inizializzazioni variabili
persona = Persona("Luca Verdi", "Via Roma 10, Torino", 30)                           # oggetto Persona
studente = Studente("Giulia Neri", "Corso Francia 5, Torino", 19, "Liceo Einstein", 7.8)  # oggetto Studente
lavoratore = Lavoratore("Paolo Gialli", "Via Po 3, Torino", 41, "Acme S.p.A.", 2300.0)    # oggetto Lavoratore
persone: List[Persona] = []  # lista per trattare i tre oggetti in modo uniforme

# Elaborazione
studente.set_media_voti(8.2)
lavoratore.set_stipendio(2400.0)
persone.append(persona)
persone.append(studente)
persone.append(lavoratore)

# Sezione di output
for elemento in persone:
    print(elemento)
print("Media voti aggiornata di", studente.get_nome(), ":", studente.get_media_voti())
print("Stipendio aggiornato di", lavoratore.get_nome(), ":", lavoratore.get_stipendio())
print("Lo studente è anche una Persona?", isinstance(studente, Persona))

# Eventuali sotto processi di Elaborazione: casi limite
print("--- Casi limite ---")
try:
    studente.set_media_voti(11)
except ValueError as errore:
    print("Errore:", errore)

try:
    lavoratore.set_stipendio(-50)
except ValueError as errore:
    print("Errore:", errore)

try:
    persona.set_eta(150)
except ValueError as errore:
    print("Errore:", errore)
