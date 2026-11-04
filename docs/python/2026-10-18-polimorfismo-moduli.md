# Python — polimorfismo, operator overloading e moduli (18/10/2026)

**Materia:** Python (docente: Massimo Papa) · **Cartella:** `Python/Esercizi_OOP_e_Files/03_Polimorfismo_Import/`

## Obiettivo
Far comportare in modo diverso oggetti di classi derivate e dividere un programma in più file.

## Concetti chiave
- **Polimorfismo:** la stessa chiamata (`accendi()`) ha effetti diversi a seconda della classe derivata (`Auto`, `Moto`, `Bicicletta`).
- **Operator overloading:** `__add__`, `__mul__`, `__str__` permettono `a + b` tra `NumeroComplesso` o `Vettore2D`.
- **Moduli:** `media.py` (classe base `Media`, derivate `Libro` e `DVD`), `biblioteca.py` (classe `Biblioteca`) e `main.py` che li importa.

## Esercizi
| # | Traccia | Come (funzioni · tecniche) | File |
|---|---|---|---|
| 1 | Polimorfismo con oggetti veicolo. Classe base Veicolo (marca, modello, accendi(), spegni(), __str__) e classi derivate Auto (numero_porte), Moto (cilindrata) e Bicicletta (tipo) che ridefiniscono accendi() e spegni(). Funzione ge… | classi: `Veicolo`, `Auto(Veicolo)`, `Moto(Veicolo)`, `Bicicletta(Veicolo)` · funzioni: `gestisci_veicolo()` · for, metodo speciale __str__ | `Esercizi_OOP_e_Files/03_Polimorfismo_Import/es6_veicoli.py` |
| 2 | Polimorfismo con operatori e collezioni eterogenee. Classi NumeroComplesso (forma algebrica, somma, prodotto, modulo) e Vettore2D (somma, prodotto per uno scalare, modulo) con overloading degli operatori + e *. Funzione stampa_op… | classi: `NumeroComplesso`, `Vettore2D` · funzioni: `stampa_operazioni()` · for, metodo speciale __add__, metodo speciale __mul__, metodo speciale __str__, round() | `Esercizi_OOP_e_Files/03_Polimorfismo_Import/es7_complessi_vettori.py` |
| 3 | Sistema modulare per gestione biblioteca - File 2: biblioteca.py Definisce la classe Biblioteca, che gestisce un catalogo di oggetti Media. | classi: `Biblioteca` · enumerate(), for, isinstance() | `Esercizi_OOP_e_Files/03_Polimorfismo_Import/es8_biblioteca/biblioteca.py` |
| 4 | Sistema modulare per gestione biblioteca - File 3: main.py Programma principale che importa le classi dai moduli media e biblioteca, crea una biblioteca, aggiunge libri e DVD, prova tutti i metodi e stampa catalogo e statistiche. | for | `Esercizi_OOP_e_Files/03_Polimorfismo_Import/es8_biblioteca/main.py` |
| 5 | Sistema modulare per gestione biblioteca - File 1: media.py Definisce la classe base Media e le classi derivate Libro e DVD. | classi: `Media`, `Libro(Media)`, `DVD(Media)` · funzioni: `formatta_durata()` · metodo speciale __str__ | `Esercizi_OOP_e_Files/03_Polimorfismo_Import/es8_biblioteca/media.py` |
