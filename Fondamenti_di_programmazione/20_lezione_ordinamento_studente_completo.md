# Lezione: Algoritmi di Ordinamento
**Durata totale:** 4 ore
**Teoria:** 1.5 ore | **Esercizi:** 2.5 ore
**Data:** _______________
**Ambiente:** CLion (JetBrains)

---

## PARTE 1 — TEORIA (1.5 ore)

---

### 1.1 Introduzione e Motivazione

#### Perché ordinare?

Immagina di avere una rubrica telefonica con 1000 contatti in ordine casuale. Cercare "Verdi Mario" richiede di leggere ogni nome, uno per uno, fino a trovarlo — nel caso peggiore, tutti e 1000. Se invece la rubrica è in ordine alfabetico, si apre direttamente nella sezione "V" e in pochi secondi il contatto è trovato.

**Questo è il potere dell'ordinamento:** rendere i dati più facili da consultare, cercare e gestire.

Nella programmazione, ordinare un array è una delle operazioni più frequenti:
- Visualizzare una classifica di punteggi dal più alto al più basso
- Mostrare prodotti dal più economico al più costoso
- Trovare il valore minimo o massimo
- Preparare i dati per algoritmi più efficienti

#### Definizione

Ordinare un array significa riorganizzare i suoi elementi in modo che rispettino un criterio — tipicamente **crescente** (dal più piccolo al più grande) o **decrescente** (dal più grande al più piccolo).

```
Prima:  [64, 25, 12, 22, 11]
Dopo:   [11, 12, 22, 25, 64]   ← ordine crescente
```

---

### 1.2 Spiegazione degli Algoritmi

In questa lezione studiamo tre algoritmi classici, tutti con complessità **O(n²)**: adatti a dataset piccoli e ottimi per capire i principi fondamentali dell'ordinamento.

---

#### 🫧 Bubble Sort — Ordinamento a Bolle

**Idea di base:** confronta coppie di elementi adiacenti e scambiali se sono nell'ordine sbagliato. Ripeti finché l'array non è ordinato. Gli elementi grandi "affondano" verso destra come bolle che salgono.

**Visualizzazione passo-passo su `[64, 25, 12, 22, 11]`:**

```
PASSATA 1:
[64, 25, 12, 22, 11]
 ↑   ↑
 64 > 25 → SCAMBIA
[25, 64, 12, 22, 11]
     ↑   ↑
     64 > 12 → SCAMBIA
[25, 12, 64, 22, 11]
         ↑   ↑
         64 > 22 → SCAMBIA
[25, 12, 22, 64, 11]
             ↑   ↑
             64 > 11 → SCAMBIA
[25, 12, 22, 11, 64]  ← 64 è al suo posto!

PASSATA 2:
[25, 12, 22, 11 | 64]
 ↑   ↑
 25 > 12 → SCAMBIA
[12, 25, 22, 11 | 64]
     ↑   ↑
     25 > 22 → SCAMBIA
[12, 22, 25, 11 | 64]
         ↑   ↑
         25 > 11 → SCAMBIA
[12, 22, 11, 25 | 64]  ← 25 è al suo posto!

... continua fino a ordinamento completo ...

RISULTATO: [11, 12, 22, 25, 64]
```

**Struttura del codice:**
```
Per ogni passata i da 0 a n-2:
    Per ogni posizione j da 0 a n-2-i:
        Se arr[j] > arr[j+1]:
            scambia arr[j] e arr[j+1]
```

**Caratteristiche:**
- Complessità: O(n²) — due cicli annidati
- Stabile: sì (elementi uguali non vengono scambiati)
- Semplice da capire e implementare

---

#### 🎯 Selection Sort — Ordinamento per Selezione

**Idea di base:** trova il minimo nell'array non ancora ordinato e mettilo nella posizione corretta. Ripeti riducendo ogni volta la porzione da esaminare.

**Visualizzazione passo-passo su `[64, 25, 12, 22, 11]`:**

```
PASSO 1: cerca il minimo in [64, 25, 12, 22, 11]
         minimo = 11 (indice 4)
         scambia posizione 0 con posizione 4
[11 | 25, 12, 22, 64]
 ↑ ordinato

PASSO 2: cerca il minimo in [25, 12, 22, 64]
         minimo = 12 (indice 2)
         scambia posizione 1 con posizione 2
[11, 12 | 25, 22, 64]
     ↑ ordinato

PASSO 3: cerca il minimo in [25, 22, 64]
         minimo = 22 (indice 3)
         scambia posizione 2 con posizione 3
[11, 12, 22 | 25, 64]
         ↑ ordinato

PASSO 4: cerca il minimo in [25, 64]
         minimo = 25 (indice 3)
         nessuno scambio necessario
[11, 12, 22, 25 | 64]
             ↑ ordinato

RISULTATO: [11, 12, 22, 25, 64]
```

**Struttura del codice:**
```
Per ogni posizione i da 0 a n-2:
    Trova l'indice del minimo tra i e n-1
    Se il minimo non è già in posizione i:
        scambia arr[i] con arr[indice_minimo]
```

**Caratteristiche:**
- Complessità: O(n²) — sempre, anche su array già ordinato
- Numero di scambi: O(n) — al massimo n-1 scambi (vantaggio!)
- Non stabile: può scambiare elementi uguali distanti

---

#### 🃏 Insertion Sort — Ordinamento per Inserimento

**Idea di base:** considera l'array diviso in una parte sinistra ordinata e una parte destra non ancora ordinata. Prende ogni nuovo elemento dalla parte destra e lo "inserisce" nella posizione giusta a sinistra. È come ordinare le carte da gioco in mano.

**Visualizzazione passo-passo su `[64, 25, 12, 22, 11]`:**

```
Stato iniziale: [64 | 25, 12, 22, 11]
                 ↑ ordinato (1 elemento)

PASSO 1: prendo 25, lo confronto con 64
         25 < 64 → sposto 64 a destra
         inserisco 25 in posizione 0
[25, 64 | 12, 22, 11]
 ↑   ↑ ordinato

PASSO 2: prendo 12, lo confronto con 64 → sposto 64
         12 < 25 → sposto 25
         inserisco 12 in posizione 0
[12, 25, 64 | 22, 11]
 ↑   ↑   ↑ ordinato

PASSO 3: prendo 22, lo confronto con 64 → sposto 64
         22 < 25 → sposto 25
         22 > 12 → stop, inserisco 22 in posizione 2
[12, 25, 64 | 22, 11]  →  [12, 22, 25, 64 | 11]

PASSO 4: prendo 11, lo confronto con tutti → sposto tutto
         inserisco 11 in posizione 0
[11, 12, 22, 25, 64]

RISULTATO: [11, 12, 22, 25, 64]
```

**Struttura del codice:**
```
Per ogni posizione i da 1 a n-1:
    chiave = arr[i]
    j = i - 1
    Mentre j >= 0 e arr[j] > chiave:
        arr[j+1] = arr[j]   (sposta a destra)
        j--
    arr[j+1] = chiave       (inserisci)
```

**Caratteristiche:**
- Complessità: O(n²) peggiore, O(n) su array già ordinato
- Stabile: sì
- Ottimo per array piccoli o quasi ordinati

---

### 1.3 Esempi di Codice Commentati

#### Esempio 1 — Bubble Sort

```c
#include <stdio.h>

// Funzione che stampa gli elementi di un array
void stampa_array(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

// Funzione che ordina l'array con Bubble Sort
void bubble_sort(int arr[], int n) {
    int temp;
    // i = numero di passata (ogni passata mette a posto un elemento)
    for (int i = 0; i < n - 1; i++) {
        // j = indice di confronto (si ferma prima degli elementi già ordinati)
        for (int j = 0; j < n - 1 - i; j++) {
            // Se l'elemento corrente è maggiore del successivo, scambia
            if (arr[j] > arr[j + 1]) {
                temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

int main() {
    int numeri[] = {64, 25, 12, 22, 11};
    int n = 5;

    printf("Prima: ");
    stampa_array(numeri, n);

    bubble_sort(numeri, n);

    printf("Dopo:  ");
    stampa_array(numeri, n);

    return 0;
}
```

**Output atteso:**
```
Prima: 64 25 12 22 11
Dopo:  11 12 22 25 64
```

---

#### Esempio 2 — Selection Sort

```c
#include <stdio.h>

void stampa_array(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

void selection_sort(int arr[], int n) {
    int indice_min, temp;

    for (int i = 0; i < n - 1; i++) {
        // Supponiamo che il minimo sia nella posizione i
        indice_min = i;

        // Cerca il vero minimo nella parte non ordinata
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[indice_min]) {
                indice_min = j;  // aggiorna l'indice del minimo
            }
        }

        // Scambia solo se il minimo non è già in posizione
        if (indice_min != i) {
            temp = arr[i];
            arr[i] = arr[indice_min];
            arr[indice_min] = temp;
        }
    }
}

int main() {
    int numeri[] = {29, 10, 14, 37, 13};
    int n = 5;

    printf("Prima: ");
    stampa_array(numeri, n);

    selection_sort(numeri, n);

    printf("Dopo:  ");
    stampa_array(numeri, n);

    return 0;
}
```

**Output atteso:**
```
Prima: 29 10 14 37 13
Dopo:  10 13 14 29 37
```

---

#### Esempio 3 — Insertion Sort

```c
#include <stdio.h>

void stampa_array(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

void insertion_sort(int arr[], int n) {
    int chiave, j;

    for (int i = 1; i < n; i++) {
        chiave = arr[i];  // elemento da inserire nella parte ordinata
        j = i - 1;

        // Sposta a destra tutti gli elementi maggiori della chiave
        while (j >= 0 && arr[j] > chiave) {
            arr[j + 1] = arr[j];
            j--;
        }

        // Inserisci la chiave nella posizione corretta
        arr[j + 1] = chiave;
    }
}

int main() {
    int numeri[] = {5, 2, 9, 1, 7};
    int n = 5;

    printf("Prima: ");
    stampa_array(numeri, n);

    insertion_sort(numeri, n);

    printf("Dopo:  ");
    stampa_array(numeri, n);

    return 0;
}
```

**Output atteso:**
```
Prima: 5 2 9 1 7
Dopo:  1 2 5 7 9
```

---

### 1.4 Riepilogo Visivo

```
╔══════════════════════════════════════════════════════════════════╗
║           CONFRONTO ALGORITMI DI ORDINAMENTO O(n²)               ║
╠═══════════════════╦══════════════╦═══════════╦═══════════════════╣
║ Algoritmo         ║ Come funziona║  Stabile? ║ Punto di forza    ║
╠═══════════════════╬══════════════╬═══════════╬═══════════════════╣
║ Bubble Sort       ║ Confronta    ║    SÌ     ║ Semplicità        ║
║                   ║ adiacenti e  ║           ║ Didattico         ║
║                   ║ scambia      ║           ║                   ║
╠═══════════════════╬══════════════╬═══════════╬═══════════════════╣
║ Selection Sort    ║ Cerca il     ║    NO     ║ Pochi scambi      ║
║                   ║ minimo e lo  ║           ║ (utile se scamb.  ║
║                   ║ porta davanti║           ║  sono costosi)    ║
╠═══════════════════╬══════════════╬═══════════╬═══════════════════╣
║ Insertion Sort    ║ Inserisce    ║    SÌ     ║ Veloce su array   ║
║                   ║ ogni elem.   ║           ║ piccoli/quasi     ║
║                   ║ nella pos.   ║           ║ ordinati          ║
║                   ║ corretta     ║           ║                   ║
╚═══════════════════╩══════════════╩═══════════╩═══════════════════╝

Tutti e tre: complessità O(n²), in-place (non servono array extra)
```

**La tecnica dello scambio — da memorizzare:**
```
Per scambiare arr[a] e arr[b]:
    temp   = arr[a]   // salvo arr[a]
    arr[a] = arr[b]   // sovrascrivo arr[a]
    arr[b] = temp     // metto il valore salvato in arr[b]

⚠️ Senza variabile temp, il valore originale andrebbe perso!
```

---

### 1.5 Domande di Verifica Orale

**D1:** Cosa significa che un algoritmo di ordinamento è "stabile"?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Un algoritmo stabile preserva l'ordine relativo degli elementi con lo stesso valore. Se prima dell'ordinamento A viene prima di B e A = B, dopo l'ordinamento A è ancora prima di B. Tra gli algoritmi visti, Bubble Sort e Insertion Sort sono stabili, Selection Sort non lo è.

</details>

**D2:** Perché nel Bubble Sort il ciclo interno arriva fino a `n - 1 - i` invece di `n - 1`?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Perché dopo ogni passata i, l'elemento più grande della porzione esaminata è già "affondato" nella posizione corretta in fondo all'array. Non ha senso ricontrollarlo. In questo modo si risparmia qualche confronto inutile.

</details>

**D3:** Quanti scambi esegue al massimo il Selection Sort su un array di n elementi?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Al massimo n-1 scambi, uno per ogni passata. È il suo punto di forza: esegue pochi scambi rispetto al Bubble Sort che può farne molti di più.

</details>

**D4:** Perché nella tecnica dello scambio è necessaria una variabile temporanea `temp`?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Perché se scrivessi direttamente `arr[a] = arr[b]`, perderei il valore originale di `arr[a]` prima di averlo salvato da qualche parte. La variabile `temp` funge da deposito temporaneo che permette di non perdere nessun valore.

</details>

**D5:** In quale situazione Insertion Sort è particolarmente efficiente? Perché?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Su array già ordinati o quasi ordinati. Perché il ciclo `while` interno non esegue quasi nessun passo: ogni nuovo elemento è già nella posizione giusta (o molto vicino), quindi non servono spostamenti. In questo caso la complessità diventa O(n) invece di O(n²).

</details>

**D6:** Quale dei tre algoritmi visti sceglieresti per ordinare un array di soli 5 elementi? Ha importanza la scelta?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Per 5 elementi qualsiasi dei tre va benissimo — le differenze di prestazione sono trascurabili. In generale, Insertion Sort è considerato il migliore per array molto piccoli. Su dataset così ridotti l'importante è la correttezza del codice, non l'efficienza.

</details>

**D7:** Cosa succederebbe se dimenticassimo la variabile `temp` e scrivessimo `arr[j] = arr[j+1]; arr[j+1] = arr[j];`?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Entrambi gli elementi finirebbero per avere lo stesso valore (quello di `arr[j+1]`), perdendo il valore originale di `arr[j]`. Lo scambio non avverrebbe correttamente.

</details>

---

## PARTE 2 — ESERCIZI (2.5 ore)

---

### 🟢 Livello Base

---

#### Esercizio B1 — Simulazione manuale del Bubble Sort (15-20 min)

**Testo:**
Scrivi un programma che esegue il Bubble Sort su un array di 6 interi inseriti dall'utente, stampando lo stato dell'array dopo ogni passata completa.

**Esempio input/output:**
```
Inserisci 6 numeri: 5 3 8 1 9 2

Passata 1: 3 5 1 8 2 9
Passata 2: 3 1 5 2 8 9
Passata 3: 1 3 2 5 8 9
Passata 4: 1 2 3 5 8 9
Passata 5: 1 2 3 5 8 9

Array ordinato: 1 2 3 5 8 9
```

**💡 Hint:**
1. Usa `scanf` in un ciclo per leggere i 6 elementi
2. Aggiungi una `printf` dentro il ciclo esterno del Bubble Sort (dopo il ciclo interno) per stampare l'array a ogni passata
3. Crea una funzione `stampa_array` separata per non ripetere codice
4. Il numero di passate è sempre `n - 1`

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

#define N 6

void stampa_array(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main() {
    int arr[N];
    int temp;

    printf("Inserisci %d numeri: ", N);
    for (int i = 0; i < N; i++) {
        scanf("%d", &arr[i]);
    }

    for (int i = 0; i < N - 1; i++) {
        for (int j = 0; j < N - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
        printf("Passata %d: ", i + 1);
        stampa_array(arr, N);
    }

    printf("\nArray ordinato: ");
    stampa_array(arr, N);

    return 0;
}
```

</details>

---

#### Esercizio B2 — Trova il minimo con Selection Sort (15-20 min)

**Testo:**
Scrivi un programma che ordina un array di 5 numeri interi (definiti direttamente nel codice) usando il Selection Sort, e stampa quale scambio viene effettuato a ogni passo nel formato: `Passo X: scambio arr[i]=V1 con arr[j]=V2`.

**Esempio input/output:**
```
Array iniziale: 29 10 14 37 13

Passo 1: scambio arr[0]=29 con arr[1]=10
Passo 2: scambio arr[1]=29 con arr[4]=13
Passo 3: nessuno scambio necessario
Passo 4: nessuno scambio necessario

Array ordinato: 10 13 14 29 37
```

**💡 Hint:**
1. Tieni traccia dell'indice del minimo durante la ricerca
2. Prima dello scambio, stampa i valori coinvolti
3. Se `indice_min == i` non serve scambiare — stampalo esplicitamente

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

void stampa_array(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main() {
    int arr[] = {29, 10, 14, 37, 13};
    int n = 5;
    int indice_min, temp;

    printf("Array iniziale: ");
    stampa_array(arr, n);
    printf("\n");

    for (int i = 0; i < n - 1; i++) {
        indice_min = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[indice_min]) {
                indice_min = j;
            }
        }

        if (indice_min != i) {
            printf("Passo %d: scambio arr[%d]=%d con arr[%d]=%d\n",
                   i + 1, i, arr[i], indice_min, arr[indice_min]);
            temp = arr[i];
            arr[i] = arr[indice_min];
            arr[indice_min] = temp;
        } else {
            printf("Passo %d: nessuno scambio necessario\n", i + 1);
        }
    }

    printf("\nArray ordinato: ");
    stampa_array(arr, n);

    return 0;
}
```

</details>

---

### 🟡 Livello Intermedio

---

#### Esercizio I1 — Ordinamento decrescente con Insertion Sort (20-25 min)

**Testo:**
Scrivi un programma che legge dall'utente N interi (con N definito come costante a 7) e li ordina in ordine **decrescente** usando Insertion Sort. Stampa l'array prima e dopo l'ordinamento.

**Esempio input/output:**
```
Inserisci 7 numeri: 4 7 2 9 1 6 3

Prima:  4 7 2 9 1 6 3
Dopo:   9 7 6 4 3 2 1
```

**💡 Hint:**
1. L'Insertion Sort decrescente cambia solo la condizione del `while`: invece di `arr[j] > chiave`, usa `arr[j] < chiave`
2. Il resto della logica rimane identico
3. Prova prima a implementare l'Insertion Sort crescente, poi modifica la condizione

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

#define N 7

void stampa_array(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

void insertion_sort_decrescente(int arr[], int n) {
    int chiave, j;
    for (int i = 1; i < n; i++) {
        chiave = arr[i];
        j = i - 1;
        while (j >= 0 && arr[j] < chiave) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = chiave;
    }
}

int main() {
    int arr[N];

    printf("Inserisci %d numeri: ", N);
    for (int i = 0; i < N; i++) {
        scanf("%d", &arr[i]);
    }

    printf("\nPrima:  ");
    stampa_array(arr, N);

    insertion_sort_decrescente(arr, N);

    printf("Dopo:   ");
    stampa_array(arr, N);

    return 0;
}
```

</details>

---

#### Esercizio I2 — Conta gli scambi (20-25 min)

**Testo:**
Scrivi un programma che chiede all'utente 8 numeri interi e li ordina con il Bubble Sort, contando e stampando il numero totale di scambi effettuati. Alla fine stampa anche il numero di passate eseguite prima che l'array risultasse ordinato.

**Esempio input/output:**
```
Inserisci 8 numeri: 3 1 4 1 5 9 2 6

Ordinamento completato in 5 passate.
Numero totale di scambi: 8

Array ordinato: 1 1 2 3 4 5 6 9
```

**💡 Hint:**
1. Usa due variabili contatore: `scambi` e `passate`
2. Per contare le passate realmente utili, aggiungi un flag booleano (intero 0/1) che segnala se è avvenuto almeno uno scambio in una passata — se non è avvenuto nessuno scambio, l'array è già ordinato e si può fermare
3. Inizializza il flag a 0 all'inizio di ogni passata e mettilo a 1 quando avviene uno scambio

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

#define N 8

void stampa_array(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main() {
    int arr[N];
    int temp;
    int scambi = 0;
    int passate = 0;
    int scambio_avvenuto;

    printf("Inserisci %d numeri: ", N);
    for (int i = 0; i < N; i++) {
        scanf("%d", &arr[i]);
    }

    for (int i = 0; i < N - 1; i++) {
        scambio_avvenuto = 0;
        for (int j = 0; j < N - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                scambi++;
                scambio_avvenuto = 1;
            }
        }
        passate++;
        if (!scambio_avvenuto) {
            break;
        }
    }

    printf("\nOrdinamento completato in %d passate.\n", passate);
    printf("Numero totale di scambi: %d\n", scambi);
    printf("\nArray ordinato: ");
    stampa_array(arr, N);

    return 0;
}
```

</details>

---

#### Esercizio I3 — Ordinamento di voti (25-30 min)

**Testo:**
Un professore ha i voti di 10 studenti (interi da 0 a 30) inseriti dall'utente. Scrivi un programma che:
1. Legge i 10 voti
2. Li ordina in ordine crescente con uno dei tre algoritmi visti
3. Stampa i voti ordinati
4. Stampa il voto minimo, massimo e la media (come numero decimale)

**Esempio input/output:**
```
Inserisci 10 voti: 18 27 30 22 15 28 19 24 30 20

Voti ordinati: 15 18 19 20 22 24 27 28 30 30

Voto minimo:  15
Voto massimo: 30
Media:        23.30
```

**💡 Hint:**
1. Dopo l'ordinamento, il minimo è `arr[0]` e il massimo è `arr[n-1]` — non serve cercarli!
2. Per la media, usa una variabile `float` o fai la divisione con `(float)`
3. Usa `%.2f` in `printf` per stampare due decimali
4. Puoi usare qualsiasi algoritmo di ordinamento tra quelli visti

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

#define N 10

void stampa_array(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

void bubble_sort(int arr[], int n) {
    int temp;
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

int main() {
    int voti[N];
    int somma = 0;
    float media;

    printf("Inserisci %d voti: ", N);
    for (int i = 0; i < N; i++) {
        scanf("%d", &voti[i]);
        somma += voti[i];
    }

    bubble_sort(voti, N);

    printf("\nVoti ordinati: ");
    stampa_array(voti, N);

    media = (float)somma / N;

    printf("\nVoto minimo:  %d\n", voti[0]);
    printf("Voto massimo: %d\n", voti[N - 1]);
    printf("Media:        %.2f\n", media);

    return 0;
}
```

</details>

---

### 🔴 Livello Avanzato

---

#### Esercizio A1 — Confronto tra algoritmi (30-40 min)

**Testo:**
Scrivi un programma che chiede all'utente un array di 10 interi e lo ordina con tutti e tre gli algoritmi (Bubble, Selection, Insertion). Per ciascuno, stampa il numero di confronti e di scambi effettuati. Lavora su tre copie dell'array originale in modo che gli algoritmi partano tutti dagli stessi dati.

**Esempio input/output:**
```
Inserisci 10 numeri: 9 3 7 1 5 8 2 6 4 10

=== Bubble Sort ===
Confronti: 45   Scambi: 21
Risultato: 1 2 3 4 5 6 7 8 9 10

=== Selection Sort ===
Confronti: 45   Scambi: 8
Risultato: 1 2 3 4 5 6 7 8 9 10

=== Insertion Sort ===
Confronti: 21   Scambi: 21
Risultato: 1 2 3 4 5 6 7 8 9 10
```

**💡 Hint:**
1. Copia l'array originale in tre array distinti (con un ciclo `for`) prima di applicare gli algoritmi
2. Aggiungi contatori `confronti` e `scambi` come parametri per ogni funzione — oppure usa variabili globali (più semplice, ma meno elegante)
3. Ogni `if (arr[j] > arr[j+1])` è un confronto; ogni successivo scambio è... uno scambio
4. I valori esatti dipendono dall'input: l'importante è che i tre risultati siano tutti ordinati correttamente

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

#define N 10

void stampa_array(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

void copia_array(int src[], int dst[], int n) {
    for (int i = 0; i < n; i++) {
        dst[i] = src[i];
    }
}

void bubble_sort(int arr[], int n, int *confronti, int *scambi) {
    int temp;
    *confronti = 0;
    *scambi = 0;
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            (*confronti)++;
            if (arr[j] > arr[j + 1]) {
                temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                (*scambi)++;
            }
        }
    }
}

void selection_sort(int arr[], int n, int *confronti, int *scambi) {
    int indice_min, temp;
    *confronti = 0;
    *scambi = 0;
    for (int i = 0; i < n - 1; i++) {
        indice_min = i;
        for (int j = i + 1; j < n; j++) {
            (*confronti)++;
            if (arr[j] < arr[indice_min]) {
                indice_min = j;
            }
        }
        if (indice_min != i) {
            temp = arr[i];
            arr[i] = arr[indice_min];
            arr[indice_min] = temp;
            (*scambi)++;
        }
    }
}

void insertion_sort(int arr[], int n, int *confronti, int *scambi) {
    int chiave, j;
    *confronti = 0;
    *scambi = 0;
    for (int i = 1; i < n; i++) {
        chiave = arr[i];
        j = i - 1;
        while (j >= 0 && ((*confronti)++, arr[j] > chiave)) {
            arr[j + 1] = arr[j];
            j--;
            (*scambi)++;
        }
        arr[j + 1] = chiave;
    }
}

int main() {
    int originale[N];
    int a1[N], a2[N], a3[N];
    int confronti, scambi;

    printf("Inserisci %d numeri: ", N);
    for (int i = 0; i < N; i++) {
        scanf("%d", &originale[i]);
    }

    copia_array(originale, a1, N);
    copia_array(originale, a2, N);
    copia_array(originale, a3, N);

    printf("\n=== Bubble Sort ===\n");
    bubble_sort(a1, N, &confronti, &scambi);
    printf("Confronti: %d   Scambi: %d\n", confronti, scambi);
    printf("Risultato: ");
    stampa_array(a1, N);

    printf("\n=== Selection Sort ===\n");
    selection_sort(a2, N, &confronti, &scambi);
    printf("Confronti: %d   Scambi: %d\n", confronti, scambi);
    printf("Risultato: ");
    stampa_array(a2, N);

    printf("\n=== Insertion Sort ===\n");
    insertion_sort(a3, N, &confronti, &scambi);
    printf("Confronti: %d   Scambi: %d\n", confronti, scambi);
    printf("Risultato: ");
    stampa_array(a3, N);

    return 0;
}
```

</details>

---

#### Esercizio A2 — Ordinamento di stringhe (40-45 min)

**Testo:**
Scrivi un programma che legge 5 parole (stringhe di massimo 20 caratteri) e le ordina alfabeticamente usando il Selection Sort. Usa `strcmp` per confrontare le stringhe e `strcpy` per copiarle. Stampa l'elenco prima e dopo l'ordinamento.

**Esempio input/output:**
```
Inserisci 5 parole:
Parola 1: mela
Parola 2: arancia
Parola 3: banana
Parola 4: kiwi
Parola 5: fico

Prima:  mela arancia banana kiwi fico
Dopo:   arancia banana fico kiwi mela
```

**💡 Hint:**
1. Dichiara l'array come `char parole[5][21]` — 5 stringhe, ognuna da max 20 caratteri + terminatore
2. Usa `scanf("%s", parole[i])` per leggere ogni stringa
3. `strcmp(a, b)` restituisce un valore negativo se `a` viene prima di `b` alfabeticamente, 0 se sono uguali, positivo se `a` viene dopo
4. Per scambiare due stringhe, usa un array temporaneo `char temp[21]` e `strcpy`

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <string.h>

#define N 5
#define MAX_LEN 21

void stampa_parole(char parole[][MAX_LEN], int n) {
    for (int i = 0; i < n; i++) {
        printf("%s ", parole[i]);
    }
    printf("\n");
}

void selection_sort_stringhe(char parole[][MAX_LEN], int n) {
    int indice_min;
    char temp[MAX_LEN];

    for (int i = 0; i < n - 1; i++) {
        indice_min = i;
        for (int j = i + 1; j < n; j++) {
            if (strcmp(parole[j], parole[indice_min]) < 0) {
                indice_min = j;
            }
        }
        if (indice_min != i) {
            strcpy(temp, parole[i]);
            strcpy(parole[i], parole[indice_min]);
            strcpy(parole[indice_min], temp);
        }
    }
}

int main() {
    char parole[N][MAX_LEN];

    printf("Inserisci %d parole:\n", N);
    for (int i = 0; i < N; i++) {
        printf("Parola %d: ", i + 1);
        scanf("%s", parole[i]);
    }

    printf("\nPrima:  ");
    stampa_parole(parole, N);

    selection_sort_stringhe(parole, N);

    printf("Dopo:   ");
    stampa_parole(parole, N);

    return 0;
}
```

</details>
