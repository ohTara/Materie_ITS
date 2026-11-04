# Python — classi, ereditarietà e file (19/10/2026)

**Materia:** Python (docente: Massimo Papa) · **Cartella:** `Python/Esercizi_OOP_e_Files/`

## Obiettivo
Modellare oggetti con attributi e metodi, riusare codice con l'ereditarietà e leggere/scrivere file di testo.

## Concetti chiave
- **Incapsulamento:** attributi privati (es. `__stipendio`) con getter e setter.
- **Ereditarietà:** `Studente` e `Lavoratore` derivano da `Persona`; `__str__` in overriding.
- **File:** apertura con `with open(...)`, modalità `r`/`w`, lettura riga per riga; frequenze di parole con un dizionario.

## Classi (OOP)
| # | Traccia | Come (funzioni · tecniche) | File |
|---|---|---|---|
| 1 | Creare una classe Insegnante con attributi nome, età e stipendio, dove stipendio deve essere un attributo privato. Costruire tutti i metodi getter e setter per gli attributi (anche per quelli pubblici). Effettuare l'overriding de… | classi: `Insegnante` · metodo speciale __str__, try/except | `Esercizi_OOP_e_Files/01_Classi_OOP/es1_insegnante.py` |
| 2 | Creare una classe Rettangolo con attributi base e altezza. Costruire tutti i metodi setter e getter per gli attributi. Aggiungere i metodi per il calcolo dell'area e del perimetro. Implementare un metodo di nome "contiene" che ha… | classi: `Rettangolo` · metodo speciale __str__, try/except | `Esercizi_OOP_e_Files/01_Classi_OOP/es2_rettangolo.py` |
| 3 | 1 - Creare una classe Calcolo con un costruttore di default (senza parametri) che consenta di eseguire vari calcoli su numeri interi. 2 - Creare un metodo chiamato Factorial() che permetta di calcolare il fattoriale di un intero.… | classi: `Calcolo` · for, try/except | `Esercizi_OOP_e_Files/01_Classi_OOP/es3_calcolo.py` |

## Ereditarietà
| # | Traccia | Come (funzioni · tecniche) | File |
|---|---|---|---|
| 1 | Si definisca una classe Persona con attributi nome, indirizzo ed età, con costruttore, overriding del metodo __str__ e tutti i metodi getter e setter. Si derivino da Persona le classi Studente (attributi aggiuntivi: scuola, media… | classi: `Persona`, `Studente(Persona)`, `Lavoratore(Persona)` · for, isinstance(), metodo speciale __str__, try/except | `Esercizi_OOP_e_Files/02_Ereditarieta/es4_persona_studente_lavoratore.py` |
| 2 | Creare una classe AritmeticaDue con attributi operando1 e operando2. Definire il costruttore utilizzando parametri con valori predefiniti e il metodo __str__. Aggiungere due metodi, uno che restituisca la differenza e l'altro il… | classi: `AritmeticaDue`, `AritmeticaTre(AritmeticaDue)` · metodo speciale __str__ | `Esercizi_OOP_e_Files/02_Ereditarieta/es5_aritmetica.py` |

## File
| # | Traccia | Come (funzioni · tecniche) | File |
|---|---|---|---|
| 1 | Scrivere un programma che, leggendo da tastiera una stringa, la salvi su file "stringa.txt". Successivamente aprire il file "stringa.txt" e verificare il salvataggio. | funzioni: `salva_stringa()`, `leggi_file()` · input(), open(), try/except, with | `Esercizi_OOP_e_Files/Esercizi_Files/01_Files/es1_salva_stringa.py` |
| 2 | Scrivi una classe che legga un file di testo e stampi sul file "output.txt" la parola più lunga contenuta. [Facoltativo: stampi sul file "output.txt" le prime N parole più lunghe, N è dato in input dall'utente]. Istanziare la cla… | classi: `AnalizzatoreTesto` · for, input(), open(), try/except, with | `Esercizi_OOP_e_Files/Esercizi_Files/01_Files/es2_parola_piu_lunga.py` |
| 3 | Progetta una classe che legga un file di testo. Tale classe deve avere un metodo che restituisca la parola con frequenza maggiore. [Suggerimento: si consideri l'esercizio che contava le frequenze delle lettere in una stringa util… | classi: `ContatoreParole` · for, open(), try/except, with | `Esercizi_OOP_e_Files/Esercizi_Files/01_Files/es3_parola_frequente.py` |
| 4 | Scrivere un programma che permetta di copiare il contenuto di un file in un altro file. | funzioni: `copia_file()`, `contenuti_uguali()` · input(), open(), try/except, while, with | `Esercizi_OOP_e_Files/Esercizi_Files/01_Files/es4_copia_file.py` |

File di prova: `testo_esempio.txt` (per es. 2 e 3) e `sorgente.txt` (per es. 4). Il README della cartella `Esercizi_OOP_e_Files/` descrive come lanciare gli esercizi (l'es. 8 si avvia da `main.py`).
