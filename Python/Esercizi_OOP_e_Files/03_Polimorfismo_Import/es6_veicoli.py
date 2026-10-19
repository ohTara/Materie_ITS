"""
Autore: Luca Tarallo
Data: 18/10/2026

Titolo: Polimorfismo con oggetti veicolo. Classe base Veicolo (marca, modello, accendi(),
        spegni(), __str__) e classi derivate Auto (numero_porte), Moto (cilindrata) e
        Bicicletta (tipo) che ridefiniscono accendi() e spegni(). Funzione gestisci_veicolo()
        che stampa le informazioni del veicolo e chiama accendi() e spegni(). Programma
        principale che crea un veicolo per tipo (parametri hard-coded), li inserisce in una
        lista e itera su di essa chiamando gestisci_veicolo().
"""
from typing import List

##
## Classi:
##

class Veicolo:
    """
    Classe: Veicolo
    Classe base di tutti i veicoli.
    Attributi:
        str marca -> marca del veicolo
        str modello -> modello del veicolo
    """

    def __init__(self, marca: str, modello: str) -> None:
        """
        Funzione: __init__
        Parametri formali:
            str marca -> marca del veicolo
            str modello -> modello del veicolo
        Valore di ritorno:
            None
        """
        self.marca = marca
        self.modello = modello

    def accendi(self) -> str:
        """
        Funzione: accendi
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> messaggio di accensione generico
        """
        return "Il veicolo si avvia"

    def spegni(self) -> str:
        """
        Funzione: spegni
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> messaggio di spegnimento generico
        """
        return "Il veicolo si spegne"

    def __str__(self) -> str:
        """
        Funzione: __str__
        Usa il nome della classe dell'oggetto, quindi è valido anche per le classi derivate
        (es. "Auto: Fiat Panda").
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> stringa nel formato "Tipo: marca modello"
        """
        return f"{self.__class__.__name__}: {self.marca} {self.modello}"


class Auto(Veicolo):
    """
    Classe: Auto
    Veicolo a quattro ruote.
    Attributi aggiuntivi:
        int numero_porte -> numero di porte dell'auto
    """

    def __init__(self, marca: str, modello: str, numero_porte: int) -> None:
        """
        Funzione: __init__
        Parametri formali:
            str marca -> marca dell'auto
            str modello -> modello dell'auto
            int numero_porte -> numero di porte
        Valore di ritorno:
            None
        """
        super().__init__(marca, modello)
        self.numero_porte = numero_porte

    def accendi(self) -> str:
        """
        Funzione: accendi
        Overriding del metodo della classe base.
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> messaggio di accensione dell'auto
        """
        return "L'auto si avvia con la chiave"

    def spegni(self) -> str:
        """
        Funzione: spegni
        Overriding del metodo della classe base.
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> messaggio di spegnimento dell'auto
        """
        return "L'auto si spegne girando la chiave"


class Moto(Veicolo):
    """
    Classe: Moto
    Veicolo a due ruote a motore.
    Attributi aggiuntivi:
        int cilindrata -> cilindrata in cc
    """

    def __init__(self, marca: str, modello: str, cilindrata: int) -> None:
        """
        Funzione: __init__
        Parametri formali:
            str marca -> marca della moto
            str modello -> modello della moto
            int cilindrata -> cilindrata in cc
        Valore di ritorno:
            None
        """
        super().__init__(marca, modello)
        self.cilindrata = cilindrata

    def accendi(self) -> str:
        """
        Funzione: accendi
        Overriding del metodo della classe base.
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> messaggio di accensione della moto
        """
        return "La moto si avvia premendo il pulsante"

    def spegni(self) -> str:
        """
        Funzione: spegni
        Overriding del metodo della classe base.
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> messaggio di spegnimento della moto
        """
        return "La moto si spegne con l'interruttore"


class Bicicletta(Veicolo):
    """
    Classe: Bicicletta
    Veicolo a pedali.
    Attributi aggiuntivi:
        str tipo -> tipo di bicicletta (es. "mountain bike", "city bike")
    """

    def __init__(self, marca: str, modello: str, tipo: str) -> None:
        """
        Funzione: __init__
        Parametri formali:
            str marca -> marca della bicicletta
            str modello -> modello della bicicletta
            str tipo -> tipo di bicicletta
        Valore di ritorno:
            None
        """
        super().__init__(marca, modello)
        self.tipo = tipo

    def accendi(self) -> str:
        """
        Funzione: accendi
        Overriding del metodo della classe base.
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> messaggio di "accensione" della bicicletta
        """
        return "La bicicletta è sempre pronta!"

    def spegni(self) -> str:
        """
        Funzione: spegni
        Overriding del metodo della classe base.
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> messaggio di "spegnimento" della bicicletta
        """
        return "La bicicletta non si spegne mai"


##
## Funzioni:
##

def gestisci_veicolo(veicolo: Veicolo) -> None:
    """
    Funzione: gestisci_veicolo
    Stampa le informazioni del veicolo, poi lo accende e lo spegne. Grazie al polimorfismo
    funziona con qualunque classe derivata da Veicolo.
    Parametri formali:
        Veicolo veicolo -> veicolo (o oggetto di una classe derivata) da gestire
    Valore di ritorno:
        None
    """
    print(veicolo)
    print(veicolo.accendi())
    print(veicolo.spegni())


"""
Programma principale
Crea un'istanza per ogni tipo di veicolo, le inserisce in una lista e richiama
gestisci_veicolo() per ciascun elemento.
"""
# Sezione di input Dati
# (nessun input da tastiera: i parametri sono scritti nel codice)

# Inizializzazioni variabili
veicoli: List[Veicolo] = []  # lista eterogenea di veicoli

# Elaborazione
veicoli.append(Auto("Fiat", "Panda", 5))
veicoli.append(Moto("Honda", "CBR", 600))
veicoli.append(Bicicletta("Bianchi", "Mountain Bike", "mountain bike"))

# Sezione di output
for veicolo in veicoli:
    gestisci_veicolo(veicolo)
    print("---")
