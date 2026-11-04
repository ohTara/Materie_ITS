'''
Autore: Luca Tarallo
Data: 27/10/2026
Titolo: Eliminare tutti i files che contengono nel nome una sequenza di caratteri data in input.
'''
import os

##
## Funzioni:
##
def trova_file(percorso: str, sequenza: str) -> list:
    '''
    Funzione: trova_file
    Cerca i file (non le cartelle) del solo primo livello il cui nome
    contiene la sequenza data (confronto che distingue maiuscole/minuscole).

    Parametri formali:
    str percorso -> directory in cui cercare
    str sequenza -> sequenza di caratteri da cercare nel nome

    Valore di ritorno:
    list -> lista di str con i percorsi completi dei file trovati
    '''
    trovati = []  # File che contengono la sequenza
    for nome in os.listdir(percorso):
        completo = os.path.join(percorso, nome)
        if os.path.isfile(completo) and sequenza in nome:
            trovati.append(completo)
    return trovati


def elimina_file(elenco: list) -> int:
    '''
    Funzione: elimina_file
    Elimina i file indicati; un errore su un file non blocca gli altri.

    Parametri formali:
    list elenco -> percorsi completi dei file da eliminare

    Valore di ritorno:
    int -> numero di file effettivamente eliminati
    '''
    eliminati = 0  # Contatore delle eliminazioni riuscite
    for percorso_file in elenco:
        try:
            os.remove(percorso_file)
            eliminati += 1
        except OSError as errore:
            print(f"Impossibile eliminare {percorso_file}: {errore}")
    return eliminati


'''
Programma principale
Chiede percorso e sequenza, mostra i file che verrebbero eliminati e li
cancella solo dopo conferma esplicita (l'eliminazione e' irreversibile).
'''
# Sezione di input Dati
percorso_input = input("Percorso in cui cercare: ").strip()  # Directory di lavoro
sequenza_input = input("Sequenza di caratteri nel nome: ")   # Testo da cercare

# Elaborazione
if not os.path.isdir(percorso_input):
    print("Errore: il percorso non esiste o non e' una directory.")
elif sequenza_input == "":
    # Caso limite: una sequenza vuota e' contenuta in ogni nome -> cancellerebbe tutto
    print("Errore: sequenza vuota non ammessa.")
else:
    candidati = trova_file(percorso_input, sequenza_input)  # File da eliminare
    # Sezione di output
    if len(candidati) == 0:
        print("Nessun file corrispondente.")
    else:
        print("File che verranno eliminati:")
        for f in candidati:
            print(" -", f)
        risposta = input("Confermi l'eliminazione? (s/N): ").strip().lower()  # Conferma
        if risposta == "s":
            n = elimina_file(candidati)  # Eliminati
            print(f"Eliminati {n} file su {len(candidati)}.")
        else:
            print("Operazione annullata.")
