"""
Autore: Luca Tarallo
Data: 19/10/2026

Titolo: Scrivere un programma che permetta di copiare il contenuto di un file in un altro file.
"""
from pathlib import Path

##
## Funzioni:
##

def copia_file(sorgente: Path, destinazione: Path, dimensione_blocco: int = 4096) -> int:
    """
    Funzione: copia_file
    Copia il contenuto di un file in un altro, a blocchi di byte (funziona con qualsiasi tipo
    di file, anche non di testo). Se la destinazione esiste viene sovrascritta.
    Parametri formali:
        Path sorgente -> file da copiare (deve esistere)
        Path destinazione -> file da creare
        int dimensione_blocco -> byte letti per volta (predefinito 4096)
    Valore di ritorno:
        int -> numero di byte copiati
    """
    byte_copiati = 0
    with open(sorgente, "rb") as file_in, open(destinazione, "wb") as file_out:
        blocco = file_in.read(dimensione_blocco)
        while blocco:
            file_out.write(blocco)
            byte_copiati += len(blocco)
            blocco = file_in.read(dimensione_blocco)
    return byte_copiati


def contenuti_uguali(file1: Path, file2: Path) -> bool:
    """
    Funzione: contenuti_uguali
    Verifica che due file abbiano lo stesso contenuto.
    Parametri formali:
        Path file1 -> primo file
        Path file2 -> secondo file
    Valore di ritorno:
        bool -> True se i contenuti coincidono byte per byte, False altrimenti
    """
    return file1.read_bytes() == file2.read_bytes()


"""
Programma principale
Chiede il nome del file sorgente e di quello di destinazione (Invio per usare i valori
predefiniti), copia il contenuto e verifica che la copia sia identica.
"""
# Sezione di input Dati
nome_sorgente = input("File da copiare [sorgente.txt]: ").strip() or "sorgente.txt"
nome_destinazione = input("File di destinazione [copia.txt]: ").strip() or "copia.txt"

# Inizializzazioni variabili
cartella = Path(__file__).resolve().parent     # cartella dello script
file_sorgente = cartella / nome_sorgente       # percorso del file da copiare
file_destinazione = cartella / nome_destinazione  # percorso della copia

# Elaborazione
if not file_sorgente.exists():
    print("Errore: il file sorgente non esiste:", file_sorgente)
elif file_sorgente.resolve() == file_destinazione.resolve():
    print("Errore: sorgente e destinazione coincidono")
else:
    try:
        byte = copia_file(file_sorgente, file_destinazione)

        # Sezione di output
        print(f"Copiati {byte} byte da {file_sorgente.name} a {file_destinazione.name}")
        if contenuti_uguali(file_sorgente, file_destinazione):
            print("Verifica riuscita: i due file hanno lo stesso contenuto")
        else:
            print("Verifica fallita: i due file sono diversi")
    except OSError as errore:
        print("Errore di accesso al file:", errore)
