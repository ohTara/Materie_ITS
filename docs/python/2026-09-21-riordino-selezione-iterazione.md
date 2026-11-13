# Python — riordino esercizi di selezione e iterazione (21/09/2026)

**Materia:** Python (docente: Massimo Papa) · **Cartella:** `Python/21-09-2026/`

## Obiettivo
Rifinire e riorganizzare gli esercizi del 14/09 con nomi file che descrivono il contenuto (`esN_argomento_descrizione.py`).

## Concetti chiave
- Convenzione di nomi: `es<N>_<tema>_<cosa_fa>.py`, utile per ritrovare un esercizio senza aprirlo.
- Intestazione standard in ogni file: autore, data, titolo/traccia.

## Iterazione
| # | Traccia | Come (funzioni · tecniche) | File |
|---|---|---|---|
| 1 | Si hanno in input due numeri reali A e B e una successione di numeri reali positivi che termina con il valore 0. Si vuole in output la media dei soli numeri compresi tra A e B. Esempio: INPUT: A=2 B=3.5 Successione: -3.4 4 2.5 3… | input(), while | `21-09-2026/Iterazione/es1_iterazione_media_tra_A_B.py` |
| 2 | Si hanno in input N saldi di conti correnti bancari. Si vuole in output la media aritmetica dei soli conti correnti che hanno un saldo negativo. | for, input() | `21-09-2026/Iterazione/es2_iterazione_media_saldi_negativi.py` |
| 3 | Leggere una successione di numeri interi passati dall'utente, fermandosi al primo numero che rende la successione non crescente e restituendo quanti numeri formano la successione inserita. Esempio: INPUT: 2 5 28 10 OUTPUT: 3 INPU… | input(), while | `21-09-2026/Iterazione/es3_iterazione_sequenza_crescente.py` |
| 4 | Scrivere un programma che legga N numeri da tastiera, N dato in input, e ne restituisca il minimo. | for, input() | `21-09-2026/Iterazione/es4_iterazione_minimo_N_numeri.py` |
| 5 | Scrivere un programma che legga le lunghezze dei tre lati di un triangolo a, b, c e ne calcoli il perimetro e l'area S, quest'ultima tramite la formula di Erone: S = sqrt(p(p-a)(p-b)(p-c)), dove p è il semiperimetro. | input() | `21-09-2026/Selezione/es4_selezione_triangolo_erone.py` |
| 6 | Scrivere un programma che chieda quanti alunni ci sono in una classe, poi per ogni alunno fa inserire M voti, M dato in input, e ne scrive la media. | for, input() | `21-09-2026/Iterazione/es5_iterazione_media_voti_classe.py` |

## Selezione
| # | Traccia | Come (funzioni · tecniche) | File |
|---|---|---|---|
| 1 | Scrivere un programma che legga i coefficienti a e b di un'equazione di primo grado ax=b e ne scriva la soluzione (attenzione al dominio del coefficiente a). | input() | `21-09-2026/Selezione/es1_selezione_equazione_primo_grado.py` |
| 2 | Scrivere un programma che legga i coefficienti a, b e c di un'equazione di secondo grado ax^2+bx+c=0 e ne scriva le soluzioni. | input() | `21-09-2026/Selezione/es2_selezione_equazione_secondo_grado.py` |
| 3 | Scrivere un programma che legga il raggio r di una circonferenza e ne calcoli l'area e la lunghezza. | input() | `21-09-2026/Selezione/es3_selezione_circonferenza.py` |
| 4 | Un negoziante per ogni spesa di importo superiore a 100 € effettua uno sconto del 5%, se l'importo risulta superiore a 300€ lo sconto è del 10%. Scrivere un programma che richieda all'utente l'ammontare della spesa e visualizzi q… | input() | `21-09-2026/Selezione/es5_selezione_sconto_negozio.py` |
| 5 | Su una linea ferroviaria, rispetto alla tariffa piena, gli utenti pensionati usufruiscono di uno sconto del 10%, gli studenti del 15% e i disoccupati del 25%. Codificando i pensionati con un 1, gli studenti con un 2 e i disoccupa… | input() | `21-09-2026/Selezione/es6_selezione_sconto_treno.py` |


