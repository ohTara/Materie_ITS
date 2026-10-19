"""
Autore: Luca Tarallo
Data: 19/10/2026

Titolo: Progetta una classe che legga un file di testo. Tale classe deve avere un metodo che
        restituisca la parola con frequenza maggiore. [Suggerimento: si consideri l'esercizio
        che contava le frequenze delle lettere in una stringa utilizzando i dictionary].
        Provare il programma con testi classici come la Divina Commedia di Dante Alighieri
        reperibile sul sito del progetto Gutenberg.
"""
import re
from pathlib import Path
from typing import Dict, Tuple

##
## Classi:
##

class ContatoreParole:
    """
    Classe: ContatoreParole
    Legge un file di testo e conta quante volte compare ciascuna parola (in minuscolo).
    Attributi:
        Dict[str, int] __frequenze -> dizionario {parola: numero di occorrenze}
    """

    def __init__(self, percorso_file: Path) -> None:
        """
        Funzione: __init__
        Costruttore: legge il file (eliminando l'intestazione e il piè di pagina del
        Progetto Gutenberg, se presenti) e costruisce il dizionario delle frequenze.
        Parametri formali:
            Path percorso_file -> percorso del file di testo da analizzare
        Valore di ritorno:
            None (solleva FileNotFoundError se il file non esiste)
        """
        with open(percorso_file, "r", encoding="utf-8-sig") as file:
            testo = file.read()
        testo = self.__rimuovi_note_gutenberg(testo).lower()
        self.__frequenze: Dict[str, int] = {}
        for parola in re.findall(r"[^\W\d_]+", testo):
            if parola in self.__frequenze.keys():
                self.__frequenze[parola] += 1
            else:
                self.__frequenze[parola] = 1

    def __rimuovi_note_gutenberg(self, testo: str) -> str:
        """
        Funzione: __rimuovi_note_gutenberg
        Elimina le note legali che il Progetto Gutenberg aggiunge prima della riga
        "*** START OF ..." e dopo la riga "*** END OF ...", così non alterano il conteggio.
        Parametri formali:
            str testo -> contenuto completo del file
        Valore di ritorno:
            str -> solo il testo dell'opera (invariato se i marcatori non ci sono)
        """
        inizio = testo.find("*** START OF")
        if inizio != -1:
            fine_riga = testo.find("\n", inizio)
            if fine_riga != -1:
                testo = testo[fine_riga + 1:]
        fine = testo.find("*** END OF")
        if fine != -1:
            testo = testo[:fine]
        return testo

    def parola_piu_frequente(self) -> Tuple[str, int]:
        """
        Funzione: parola_piu_frequente
        Cerca nel dizionario la parola con più occorrenze (a parità, la prima comparsa).
        Parametri formali:
            nessuno
        Valore di ritorno:
            Tuple[str, int] -> coppia (parola, numero di occorrenze); ("", 0) se il file
                               non contiene parole
        """
        parola_max = ""
        occorrenze_max = 0
        for parola in self.__frequenze.keys():
            if self.__frequenze[parola] > occorrenze_max:
                parola_max = parola
                occorrenze_max = self.__frequenze[parola]
        return parola_max, occorrenze_max

    def numero_parole_distinte(self) -> int:
        """
        Funzione: numero_parole_distinte
        Parametri formali:
            nessuno
        Valore di ritorno:
            int -> quante parole diverse sono presenti nel testo
        """
        return len(self.__frequenze)


"""
Programma principale
Analizza "divina_commedia.txt" (da scaricare dal Progetto Gutenberg e salvare accanto allo
script). Se il file non c'è, usa il testo di prova "testo_esempio.txt".
"""
# Sezione di input Dati
# (nessun input da tastiera: il file da analizzare è scelto automaticamente)

# Inizializzazioni variabili
cartella = Path(__file__).resolve().parent             # cartella dello script
file_divina_commedia = cartella / "divina_commedia.txt"  # testo classico da analizzare
file_prova = cartella / "testo_esempio.txt"            # testo di prova incluso nella cartella

# Elaborazione
if file_divina_commedia.exists():
    file_scelto = file_divina_commedia
else:
    file_scelto = file_prova
    print("File divina_commedia.txt non trovato: uso il testo di prova", file_prova.name)

try:
    contatore = ContatoreParole(file_scelto)
    parola, occorrenze = contatore.parola_piu_frequente()

    # Sezione di output
    print("File analizzato:", file_scelto.name)
    print("Parole distinte:", contatore.numero_parole_distinte())
    if occorrenze == 0:
        print("Il file non contiene parole")
    else:
        print(f'Parola più frequente: "{parola}" ({occorrenze} occorrenze)')
except FileNotFoundError:
    print("Errore: file non trovato:", file_scelto)
