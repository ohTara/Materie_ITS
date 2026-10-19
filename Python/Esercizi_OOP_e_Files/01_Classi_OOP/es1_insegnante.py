"""
Autore: Luca Tarallo
Data: 19/10/2026

Titolo: Creare una classe Insegnante con attributi nome, età e stipendio, dove stipendio deve
        essere un attributo privato. Costruire tutti i metodi getter e setter per gli attributi
        (anche per quelli pubblici). Effettuare l'overriding del metodo __str__ in maniera tale
        che restituisca gli attributi nome e età. Provare la classe istanziando almeno due oggetti.
"""

##
## Classi:
##

class Insegnante:
    """
    Classe: Insegnante
    Rappresenta un insegnante.
    Attributi:
        str nome -> nome dell'insegnante (pubblico)
        int eta -> età dell'insegnante (pubblico)
        float __stipendio -> stipendio mensile dell'insegnante (privato)
    """

    def __init__(self, nome: str, eta: int, stipendio: float) -> None:
        """
        Funzione: __init__
        Costruttore: crea un insegnante validando i valori tramite i setter.
        Parametri formali:
            str nome -> nome dell'insegnante (non vuoto)
            int eta -> età dell'insegnante (compresa tra 18 e 100)
            float stipendio -> stipendio mensile (maggiore o uguale a zero)
        Valore di ritorno:
            None -> il costruttore non restituisce valori
        """
        self.set_nome(nome)
        self.set_eta(eta)
        self.set_stipendio(stipendio)

    def get_nome(self) -> str:
        """
        Funzione: get_nome
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> nome dell'insegnante
        """
        return self.nome

    def set_nome(self, nome: str) -> None:
        """
        Funzione: set_nome
        Modifica il nome dell'insegnante (solleva ValueError se vuoto).
        Parametri formali:
            str nome -> nuovo nome
        Valore di ritorno:
            None
        """
        if nome.strip() == "":
            raise ValueError("il nome non può essere vuoto")
        self.nome = nome

    def get_eta(self) -> int:
        """
        Funzione: get_eta
        Parametri formali:
            nessuno
        Valore di ritorno:
            int -> età dell'insegnante
        """
        return self.eta

    def set_eta(self, eta: int) -> None:
        """
        Funzione: set_eta
        Modifica l'età dell'insegnante (solleva ValueError se fuori dall'intervallo 18-100).
        Parametri formali:
            int eta -> nuova età
        Valore di ritorno:
            None
        """
        if eta < 18 or eta > 100:
            raise ValueError("l'età deve essere compresa tra 18 e 100 anni")
        self.eta = eta

    def get_stipendio(self) -> float:
        """
        Funzione: get_stipendio
        Parametri formali:
            nessuno
        Valore di ritorno:
            float -> stipendio mensile (unico modo per leggere l'attributo privato)
        """
        return self.__stipendio

    def set_stipendio(self, stipendio: float) -> None:
        """
        Funzione: set_stipendio
        Modifica lo stipendio (solleva ValueError se negativo).
        Parametri formali:
            float stipendio -> nuovo stipendio mensile
        Valore di ritorno:
            None
        """
        if stipendio < 0:
            raise ValueError("lo stipendio non può essere negativo")
        self.__stipendio = stipendio

    def __str__(self) -> str:
        """
        Funzione: __str__
        Overriding: rappresentazione testuale con nome ed età.
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> stringa nel formato "Insegnante: nome, età: N anni"
        """
        return f"Insegnante: {self.nome}, età: {self.eta} anni"


"""
Programma principale
Istanzia due oggetti Insegnante, usa getter, setter e __str__ e verifica i casi limite
(accesso diretto all'attributo privato, valori non validi).
"""
# Sezione di input Dati
# (nessun input da tastiera: gli oggetti sono istanziati con valori predefiniti)

# Inizializzazioni variabili
insegnante1 = Insegnante("Mario Rossi", 45, 2100.50)   # primo oggetto di prova
insegnante2 = Insegnante("Anna Bianchi", 38, 1850.00)  # secondo oggetto di prova

# Elaborazione
insegnante2.set_nome("Anna Bianchi Verdi")
insegnante2.set_eta(39)
insegnante2.set_stipendio(1900.00)

# Sezione di output
print(insegnante1)
print("Stipendio di", insegnante1.get_nome(), ":", insegnante1.get_stipendio(), "€")
print(insegnante2)
print("Stipendio di", insegnante2.get_nome(), ":", insegnante2.get_stipendio(), "€")

# Eventuali sotto processi di Elaborazione: casi limite
print("--- Casi limite ---")
try:
    print(insegnante1.__stipendio)
except AttributeError:
    print("Accesso diretto a __stipendio non consentito: l'attributo è privato")

try:
    insegnante1.set_eta(-5)
except ValueError as errore:
    print("Errore:", errore)

try:
    insegnante1.set_stipendio(-100)
except ValueError as errore:
    print("Errore:", errore)

try:
    Insegnante("", 40, 1500)
except ValueError as errore:
    print("Errore:", errore)
