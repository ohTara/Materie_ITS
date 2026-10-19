"""
Autore: Luca Tarallo
Data: 19/10/2026

Titolo: Creare una classe AritmeticaDue con attributi operando1 e operando2. Definire il
        costruttore utilizzando parametri con valori predefiniti e il metodo __str__. Aggiungere
        due metodi, uno che restituisca la differenza e l'altro il prodotto dei due operandi.
        Implementare un terzo metodo che permetta il confronto tra il prodotto di due oggetti
        AritmeticaDue (indicare se il prodotto è maggiore di quello dell'oggetto passato come
        parametro). Derivare dalla classe AritmeticaDue la classe AritmeticaTre aggiungendo
        l'attributo operando3. Ridefinire il costruttore, il metodo __str__ e i tre metodi
        differenza, prodotto e confronto. Aggiungere un metodo per il calcolo della somma di
        tutti gli attributi. Provare le classi e i metodi implementati.
"""

##
## Classi:
##

class AritmeticaDue:
    """
    Classe: AritmeticaDue
    Gestisce due operandi numerici.
    Attributi:
        float operando1 -> primo operando
        float operando2 -> secondo operando
    """

    def __init__(self, operando1: float = 0, operando2: float = 0) -> None:
        """
        Funzione: __init__
        Costruttore con parametri a valori predefiniti.
        Parametri formali:
            float operando1 -> primo operando (predefinito 0)
            float operando2 -> secondo operando (predefinito 0)
        Valore di ritorno:
            None
        """
        self.operando1 = operando1
        self.operando2 = operando2

    def __str__(self) -> str:
        """
        Funzione: __str__
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> stringa con i valori degli operandi
        """
        return f"operando1 = {self.operando1}, operando2 = {self.operando2}"

    def differenza(self) -> float:
        """
        Funzione: differenza
        Parametri formali:
            nessuno
        Valore di ritorno:
            float -> operando1 - operando2
        """
        return self.operando1 - self.operando2

    def prodotto(self) -> float:
        """
        Funzione: prodotto
        Parametri formali:
            nessuno
        Valore di ritorno:
            float -> operando1 * operando2
        """
        return self.operando1 * self.operando2

    def confronto(self, altro: "AritmeticaDue") -> bool:
        """
        Funzione: confronto
        Confronta il prodotto dell'oggetto chiamante con quello dell'oggetto passato.
        Parametri formali:
            AritmeticaDue altro -> oggetto con cui confrontare il prodotto
        Valore di ritorno:
            bool -> True se il prodotto del chiamante è maggiore di quello di "altro"
        """
        return self.prodotto() > altro.prodotto()


class AritmeticaTre(AritmeticaDue):
    """
    Classe: AritmeticaTre
    Estende AritmeticaDue con un terzo operando.
    Attributi aggiuntivi:
        float operando3 -> terzo operando
    """

    def __init__(self, operando1: float = 0, operando2: float = 0, operando3: float = 0) -> None:
        """
        Funzione: __init__
        Overriding del costruttore con parametri a valori predefiniti.
        Parametri formali:
            float operando1 -> primo operando (predefinito 0)
            float operando2 -> secondo operando (predefinito 0)
            float operando3 -> terzo operando (predefinito 0)
        Valore di ritorno:
            None
        """
        super().__init__(operando1, operando2)
        self.operando3 = operando3

    def __str__(self) -> str:
        """
        Funzione: __str__
        Overriding: aggiunge il terzo operando.
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> stringa con i valori dei tre operandi
        """
        return f"{super().__str__()}, operando3 = {self.operando3}"

    def differenza(self) -> float:
        """
        Funzione: differenza
        Overriding: sottrae in sequenza il secondo e il terzo operando al primo.
        Parametri formali:
            nessuno
        Valore di ritorno:
            float -> operando1 - operando2 - operando3
        """
        return self.operando1 - self.operando2 - self.operando3

    def prodotto(self) -> float:
        """
        Funzione: prodotto
        Overriding: prodotto dei tre operandi.
        Parametri formali:
            nessuno
        Valore di ritorno:
            float -> operando1 * operando2 * operando3
        """
        return self.operando1 * self.operando2 * self.operando3

    def confronto(self, altro: "AritmeticaTre") -> bool:
        """
        Funzione: confronto
        Overriding: confronta il prodotto dei tre operandi con quello dell'oggetto passato.
        Parametri formali:
            AritmeticaTre altro -> oggetto con cui confrontare il prodotto
        Valore di ritorno:
            bool -> True se il prodotto del chiamante è maggiore di quello di "altro"
        """
        return self.prodotto() > altro.prodotto()

    def somma(self) -> float:
        """
        Funzione: somma
        Parametri formali:
            nessuno
        Valore di ritorno:
            float -> somma dei tre operandi
        """
        return self.operando1 + self.operando2 + self.operando3


"""
Programma principale
Prova le due classi con valori ordinari, di default e negativi (casi limite).
"""
# Sezione di input Dati
# (nessun input da tastiera: gli oggetti sono istanziati con valori predefiniti)

# Inizializzazioni variabili
a1 = AritmeticaDue(6, 4)         # prodotto 24
a2 = AritmeticaDue(5, 3)         # prodotto 15
a_default = AritmeticaDue()      # tutti i valori predefiniti (0, 0)
a_negativo = AritmeticaDue(-3, 5)  # operando negativo
t1 = AritmeticaTre(2, 3, 4)      # prodotto 24
t2 = AritmeticaTre(1, 5, 5)      # prodotto 25
t_default = AritmeticaTre(2, 3)  # terzo operando predefinito (0)

# Sezione di output
print("--- AritmeticaDue ---")
print(a1, "| differenza:", a1.differenza(), "| prodotto:", a1.prodotto())
print(a2, "| differenza:", a2.differenza(), "| prodotto:", a2.prodotto())
print("a1 ha prodotto maggiore di a2?", a1.confronto(a2))  # atteso True
print("a2 ha prodotto maggiore di a1?", a2.confronto(a1))  # atteso False
print("Caso limite - valori predefiniti:", a_default, "| prodotto:", a_default.prodotto())
print("Caso limite - operando negativo:", a_negativo, "| prodotto:", a_negativo.prodotto())
print("a1 ha prodotto maggiore del caso negativo?", a1.confronto(a_negativo))

print("--- AritmeticaTre ---")
print(t1, "| differenza:", t1.differenza(), "| prodotto:", t1.prodotto(), "| somma:", t1.somma())
print(t2, "| differenza:", t2.differenza(), "| prodotto:", t2.prodotto(), "| somma:", t2.somma())
print("t1 ha prodotto maggiore di t2?", t1.confronto(t2))  # atteso False (24 < 25)
print("t2 ha prodotto maggiore di t1?", t2.confronto(t1))  # atteso True
print("Caso limite - terzo operando predefinito:", t_default, "| prodotto:", t_default.prodotto())
