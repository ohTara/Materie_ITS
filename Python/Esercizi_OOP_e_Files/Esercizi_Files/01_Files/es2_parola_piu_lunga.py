"""
Autore: Luca Tarallo
Data: 19/10/2026

Titolo: Scrivi una classe che legga un file di testo e stampi sul file "output.txt" la parola
        più lunga contenuta. [Facoltativo: stampi sul file "output.txt" le prime N parole più
        lunghe, N è dato in input dall'utente]. Istanziare la classe e provare i metodi
        implementati.
"""
import re
from pathlib import Path
from typing import List

##
## Classi:
##

class AnalizzatoreTesto:
    """
    Classe: AnalizzatoreTesto
    Legge un file di testo e ne analizza le parole (tutte convertite in minuscolo).
    Attributi:
        List[str] __parole -> parole del file, nell'ordine in cui compaiono
    """

    def __init__(self, percorso_file: Path) -> None:
        """
        Funzione: __init__
        Costruttore: legge il file e ne estrae le parole. Un apostrofo separa due parole
        (es. "l'ereditarietà" -> "l", "ereditarietà").
        Parametri formali:
            Path percorso_file -> percorso del file di testo da analizzare
        Valore di ritorno:
            None (solleva FileNotFoundError se il file non esiste)
        """
        with open(percorso_file, "r", encoding="utf-8-sig") as file:
            testo = file.read().lower()
        self.__parole: List[str] = re.findall(r"[^\W\d_]+", testo)

    def parola_piu_lunga(self) -> str:
        """
        Funzione: parola_piu_lunga
        Cerca la parola più lunga (a parità di lunghezza, la prima che compare nel testo).
        Parametri formali:
            nessuno
        Valore di ritorno:
            str -> parola più lunga ("" se il file non contiene parole)
        """
        if len(self.__parole) == 0:
            return ""
        return max(self.__parole, key=len)

    def parole_piu_lunghe(self, n: int) -> List[str]:
        """
        Funzione: parole_piu_lunghe
        Restituisce le prime n parole più lunghe, senza ripetizioni, in ordine di lunghezza
        decrescente (a parità di lunghezza, in ordine di comparsa).
        Parametri formali:
            int n -> quante parole restituire (>= 1)
        Valore di ritorno:
            List[str] -> lista delle parole più lunghe (può avere meno di n elementi)
        """
        parole_distinte = list(dict.fromkeys(self.__parole))
        parole_distinte.sort(key=len, reverse=True)
        return parole_distinte[:n]

    def scrivi_output(self, percorso_output: Path, n: int) -> None:
        """
        Funzione: scrivi_output
        Scrive sul file la parola più lunga e le prime n parole più lunghe.
        Parametri formali:
            Path percorso_output -> file di destinazione (sovrascritto se esiste)
            int n -> quante parole lunghe scrivere (>= 1)
        Valore di ritorno:
            None
        """
        with open(percorso_output, "w", encoding="utf-8") as file:
            file.write(f"Parola più lunga: {self.parola_piu_lunga()}\n")
            file.write(f"Prime {n} parole più lunghe:\n")
            for parola in self.parole_piu_lunghe(n):
                file.write(f"{parola} ({len(parola)} lettere)\n")


"""
Programma principale
Istanzia AnalizzatoreTesto sul file "testo_esempio.txt", chiede N all'utente, scrive i
risultati su "output.txt" e li rilegge per mostrarli a schermo.
"""
# Sezione di input Dati
n = int(input("Quante parole più lunghe vuoi salvare (N)? "))

# Inizializzazioni variabili
cartella = Path(__file__).resolve().parent         # cartella dello script
file_testo = cartella / "testo_esempio.txt"        # file di testo da analizzare
file_output = cartella / "output.txt"              # file su cui scrivere i risultati

# Elaborazione
if n < 1:
    print("Errore: N deve essere maggiore o uguale a 1")
else:
    try:
        analizzatore = AnalizzatoreTesto(file_testo)
        analizzatore.scrivi_output(file_output, n)

        # Sezione di output
        print("Risultati scritti in:", file_output)
        with open(file_output, "r", encoding="utf-8") as file:
            print(file.read())
    except FileNotFoundError:
        print("Errore: file di testo non trovato:", file_testo)
