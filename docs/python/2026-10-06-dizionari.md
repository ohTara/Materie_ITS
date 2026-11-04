# Python — dizionari (06/10/2026)

**Materia:** Python (docente: Massimo Papa) · **Cartella:** `Python/06-10-2026/`

## Obiettivo
Usare coppie chiave→valore per contare, deduplicare e unire dati.

## Concetti chiave
- Le chiavi sono uniche: unire dizionari = sovrascrivere le chiavi ripetute.
- Contare occorrenze: si controlla se la chiave esiste e poi `diz[c] += 1`.
- Una funzione può ricevere un numero indefinito di dizionari con `*args`.

## Esercizi
| # | Traccia | Come (funzioni · tecniche) | File |
|---|---|---|---|
| 1 | Progettare una funzione che accetti un numero indefinito di dizionari e restituisca un dizionario che è la concatenazione di tutti i dizionari indicati come parametro formale alla funzione. Scrivete uno script che utilizzi tale f… | funzioni: `concatena_dizionari()` · *args, for | `06-10-2026/EserciziDizionari/es1_dizionari_concatena.py` |
| 2 | Scrivete uno script Python per generare e stampare un dizionario che contenga un numero (compreso tra 1 e n) nella forma (x, x*x). Esempio: n = 5 Dizionario: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25} | funzioni: `genera_quadrati()` · for, input() | `06-10-2026/EserciziDizionari/es2_dizionari_genera_quadrati.py` |
| 3 | Scrivete un programma Python per ottenere il valore massimo e minimo in un dizionario. | funzioni: `massimo_minimo_dizionario()` · for | `06-10-2026/EserciziDizionari/es3_dizionari_massimo_minimo.py` |
| 4 | Scrivete un programma Python per rimuovere i duplicati dal dizionario. | funzioni: `rimuovi_duplicati()` · for | `06-10-2026/EserciziDizionari/es4_dizionari_rimuovi_duplicati.py` |
| 5 | Scrivete un programma Python per creare un dizionario da una stringa. Le lettere della stringa rappresentano le chiavi, i valori rappresentano le occorrenze della chiave nella stringa. Esempio: stringa = "ciao mamma" Dizionario:… | funzioni: `conta_occorrenze_stringa()` · for, input() | `06-10-2026/EserciziDizionari/es5_dizionari_conta_occorrenze_stringa.py` |
