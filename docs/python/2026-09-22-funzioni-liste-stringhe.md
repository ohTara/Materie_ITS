# Python — funzioni, liste e stringhe (22/09/2026)

**Materia:** Python (docente: Massimo Papa) · **Cartella:** `Python/22-09-2026/`

## Obiettivo
Scomporre i problemi in funzioni e lavorare con le sequenze mutabili (liste) e immutabili (stringhe).

## Concetti chiave
- **Funzioni:** parametri formali, valore di ritorno, numero variabile di argomenti con `*args`; una funzione = un compito.
- **Liste:** mutabili; rimozione duplicati, intersezione, secondo minimo *distinto*, divisione in due parti con lo slicing.
- **Stringhe:** immutabili; per "rimuovere" un carattere si costruisce una nuova stringa. Palindromo = uguale a se stessa invertita.

## Funzioni
| # | Traccia | Come (funzioni · tecniche) | File |
|---|---|---|---|
| 1 | Creare una funzione che riceva una quantità di tempo in formato ore, minuti e secondi e la restituisca espressa solamente in secondi. Successivamente creare un programma principale che chieda in input due quantità di tempo e stam… | funzioni: `tempo_in_secondi()` · input() | `22-09-2026/EserciziFunzioni/es1_funzioni_tempo_in_secondi.py` |
| 2 | Creare una funzione che abbia come parametri formali un numero arbitrario di valori numerici. Si vuole che restituisca la somma dei soli numeri pari e il prodotto dei soli numeri dispari. Successivamente creare un programma che r… | funzioni: `somma_pari_prodotto_dispari()` · *args, for | `22-09-2026/EserciziFunzioni/es2_funzioni_pari_dispari.py` |
| 3 | Conversione temperatura: implementare una funzione convertiCF che converta una temperatura espressa in gradi Fahrenheit in una temperatura espressa in gradi Celsius. Usare la formula: C = (F - 32) * 5 / 9 Creare un programma prin… | funzioni: `convertiCF()` · input() | `22-09-2026/EserciziFunzioni/es3_funzioni_convertiCF.py` |
| 4 | Punto 4.a - Scrivere una funzione che restituisca un valore approssimato di e all'ennesimo termine, dove N è inserito come parametro formale alla funzione. La funzione calcola_e deve richiamare la funzione di calcolo del fattoria… | funzioni: `fattoriale()`, `calcola_e()` · for, input() | `22-09-2026/EserciziFunzioni/es4a_funzioni_calcola_e.py` |
| 5 | Punto 4.b - Supponendo di porre il numero di Nepero = 2.718281828459045, si dica errore = calcola_e(N) - Nepero, sia l'errore che si commette nella valutazione di e. Modificare la funzione che restituisce la valutazione di e con… | funzioni: `fattoriale()`, `calcola_e()`, `valuta_e()` · for, input() | `22-09-2026/EserciziFunzioni/es4b_funzioni_valuta_e_errore.py` |

## Liste
| # | Traccia | Come (funzioni · tecniche) | File |
|---|---|---|---|
| 1 | Scrivere un programma python che rimuova gli elementi duplicati da una lista. Esempio: listaIN = [2, -4, 5, 6, 5, 5, 2] listaOUT = [2, -4, 5, 6] | for | `22-09-2026/EserciziListe/es1_liste_rimuovi_duplicati.py` |
| 2 | Scrivere un programma che date due liste stampi "OK" se hanno almeno un membro comune, altrimenti stampi "KO". Esempio: lista1=[1,5,8] lista2=[3,1,10] -> output: "OK" lista1=[1,5,8] lista2=[3,11,10] -> output: "KO" | set() | `22-09-2026/EserciziListe/es2_liste_elemento_comune.py` |
| 3 | Scrivi un programma per trovare il secondo numero più piccolo in una lista. Nota: si considera il secondo valore DISTINTO più piccolo (se la lista contiene duplicati del minimo, questi non vengono considerati come "secondo" valor… | set(), sorted() | `22-09-2026/EserciziListe/es3_liste_secondo_piu_piccolo.py` |
| 4 | Scrivere un programma Python per dividere una data lista in due parti in cui viene data la lunghezza della prima parte della lista. Esempio: Lista originale: [1, 1, 2, 3, 4, 4, 5, 1] Lunghezza della prima parte della lista: 3 Out… | — | `22-09-2026/EserciziListe/es4_liste_dividi_in_due_parti.py` |

## Stringhe
| # | Traccia | Come (funzioni · tecniche) | File |
|---|---|---|---|
| 1 | Scrivere un programma per rimuovere l'n-esimo carattere da una stringa non vuota. Progettare una funzione che accetti la stringa, la posizione del carattere e restituisca la stringa modificata. | funzioni: `rimuovi_carattere()` · input() | `22-09-2026/EserciziStringhe/es1_stringhe_rimuovi_carattere.py` |
| 2 | Scrivere un programma che dica se una stringa è palindroma. Esempio: str="ABBA" PALINDROMA str="PIPPO" NON PALINDROMA | funzioni: `is_palindroma()` · input() | `22-09-2026/EserciziStringhe/es2_stringhe_palindroma.py` |
