# Python — selezione e iterazione (14–15/09/2026)

**Materia:** Python (docente: Massimo Papa) · **Cartella:** `Python/14-09-2026`

## Obiettivo
Controllare il flusso con condizioni e cicli, partendo da problemi con input da tastiera.

## Concetti chiave
- **Selezione:** `if/elif/else`; occhio ai casi limite (es. `a = 0` nell'equazione `ax = b`, discriminante negativo).
- **Iterazione:** `while` per sequenze con **sentinella** (la successione termina con `0`), `for` quando il numero di passi è noto.
- **Accumulatori e contatori:** media = somma / quantità, con controllo del divisore a zero.
- Metodo del docente: *input → output → sottoproblemi → funzione per sottoproblema → programma principale*.

## Selezione (`if / elif / else`)
| # | Traccia | Come (funzioni · tecniche) | File |
|---|---|---|---|
| 1 | Scrivere un programma che legga i coefficienti a e b di un'equazione di primo grado ax=b e ne scriva la soluzione (attenzione al dominio del coefficiente a). | input() | `14-09-2026/Selezione - Testo Esercizi/PrimoEsercizio.py` |
| 2 | Scrivere un programma che legga le lunghezze dei tre lati di un triangolo a, b, c e ne calcoli il perimetro e l'area S, quest'ultima tramite la formula di Erone: S = sqrt(p(p-a)(p-b)(p-c)), dove p è il semiperimetro. | input() | `14-09-2026/Selezione - Testo Esercizi/QuartoEsercizio.py` |
| 3 | Un negoziante per ogni spesa di importo superiore a 100 € effettua uno sconto del 5%, se l'importo risulta superiore a 300€ lo sconto è del 10%. Scrivere un programma che richieda all'utente l'ammontare della spesa e visualizzi q… | input() | `14-09-2026/Selezione - Testo Esercizi/QuintoEsercizio.py` |
| 4 | Scrivere un programma che legga i coefficienti a, b e c di un'equazione di secondo grado ax^2+bx+c=0 e ne scriva le soluzioni. | input() | `14-09-2026/Selezione - Testo Esercizi/SecondoEsercizio.py` |
| 5 | Su una linea ferroviaria, rispetto alla tariffa piena, gli utenti pensionati usufruiscono di uno sconto del 10%, gli studenti del 15% e i disoccupati del 25%. Codificando i pensionati con un 1, gli studenti con un 2 e i disoccupa… | input() | `14-09-2026/Selezione - Testo Esercizi/SestoEsercizio.py` |
| 6 | Scrivere un programma che legga il raggio r di una circonferenza e ne calcoli l'area e la lunghezza. | input() | `14-09-2026/Selezione - Testo Esercizi/TerzoEsercizio.py` |

## Iterazione (`while` / `for`)
| # | Traccia | Come (funzioni · tecniche) | File |
|---|---|---|---|
| 1 | Si hanno in input due numeri reali A e B e una successione di numeri reali positivi che termina con il valore 0. Si vuole in output la media dei soli numeri compresi tra A e B. Esempio: INPUT: A=2 B= 3.5 Successione: -3.4 4 2.5 3… | input(), while | `14-09-2026/Iterazione - Testo Esercizi/PrimoEsercizio.py` |
| 2 | Scrivere un programma che legga N numeri da tastiera, N dato in input, e ne restituisca il minimo. | for, input() | `14-09-2026/Iterazione - Testo Esercizi/QuartoEsercizio.py` |
| 3 | Scrivere un programma che chieda quanti alunni ci sono in una classe poi per ogni alunno fa inserire M voti, M dato in input, e ne scrive la media. | for, input() | `14-09-2026/Iterazione - Testo Esercizi/QuintoEsercizio.py` |
| 4 | Si hanno in input N saldi di conti correnti bancari. Si vuole in output la media aritmetica dei soli conti correnti che hanno un saldo negativo. | for, input() | `14-09-2026/Iterazione - Testo Esercizi/SecondoEsercizio.py` |
| 5 | Leggere una successione di numeri interi passati dall’utente, fermandosi al primo numero che rende la successione non crescente e restituendo quanti numeri formano la successione inserita. Esempio: INPUT: 2 5 28 10 OUTPUT: 3 INPU… | input(), while | `14-09-2026/Iterazione - Testo Esercizi/TerzoEsercizio.py` |

> **Nota di ordine:** il 21/09 gli stessi esercizi sono stati riorganizzati con nomi descrittivi (vedi `2026-09-21-riordino-selezione-iterazione.md`).

