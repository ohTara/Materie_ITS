# Esercizi OOP e File

Autore: Luca Tarallo - Unità formativa: Programmazione Python (docente: Massimo Papa)

## Struttura

```
Esercizi_OOP_e_Files/
|-- 01_Classi_OOP/                        (data: 19/10/2026)
|   |-- es1_insegnante.py
|   |-- es2_rettangolo.py
|   `-- es3_calcolo.py
|-- 02_Ereditarieta/                      (data: 19/10/2026)
|   |-- es4_persona_studente_lavoratore.py
|   `-- es5_aritmetica.py
|-- 03_Polimorfismo_Import/               (data: 18/10/2026)
|   |-- es6_veicoli.py
|   |-- es7_complessi_vettori.py
|   `-- es8_biblioteca/
|       |-- main.py
|       |-- media.py
|       `-- biblioteca.py
`-- 04_Files/                             (data: 19/10/2026)
    |-- es1_salva_stringa.py
    |-- es2_parola_piu_lunga.py
    |-- es3_parola_frequente.py
    |-- es4_copia_file.py
    |-- testo_esempio.txt                 (testo di prova per es2 ed es3)
    `-- sorgente.txt                      (file di prova per es4)
```

## Come eseguirli

Ogni file si lancia da solo, ad esempio:

```
python es1_insegnante.py
```

L'esercizio 8 va lanciato dal file `main.py` (gli altri due file sono moduli importati da lui):

```
python es8_biblioteca/main.py
```

I file creati dagli esercizi sui file (`stringa.txt`, `output.txt`, `copia.txt`) vengono scritti
nella stessa cartella dello script, indipendentemente da dove lanci il comando.

## Esercizio 3 sui file: Divina Commedia

Scarica il testo dal Progetto Gutenberg (formato "Plain Text UTF-8"), salvalo come
`divina_commedia.txt` dentro `04_Files/` e rilancia `es3_parola_frequente.py`. Il programma
elimina in automatico le note legali in inglese di Gutenberg prima di contare le parole.
Se il file non c'è, usa `testo_esempio.txt`.

## Scelte di interpretazione dove il testo era ambiguo

- **Es. 2 (Rettangolo) - metodo `contiene`**: il testo dice "altezza e base maggiori
  rispettivamente di base e altezza". Letta alla lettera sarebbe un confronto incrociato; ho
  implementato quello naturale (base con base, altezza con altezza, confronto stretto).
  Se serve il confronto incrociato basta scambiare i due `get_*` nell'ultima riga del metodo.
- **Es. 7 (Numero complesso)**: il testo parla di forma "a + ib", ma l'esempio di output mostra
  "3 + 4i" e "1 - 2i": ho seguito l'esempio di output.
- **Es. 8 (DVD)**: `tempo_visione()` dovrebbe restituire "ore:minuti", ma l'output di esempio
  mostra "2 ore e 28 minuti": ho seguito l'output di esempio.
- **Es. 8 (main.py)**: le prime righe di output coincidono con l'esempio del testo; in fondo ho
  aggiunto qualche test in più (rimozione, ricerca senza risultati, biblioteca vuota).
