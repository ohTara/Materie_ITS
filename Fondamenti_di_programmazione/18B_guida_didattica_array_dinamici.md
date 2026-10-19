# GUIDA DIDATTICA - LEZIONE 20
## Array Dinamici in C: malloc e calloc

### DURATA TOTALE: 5 ORE (con realloc)

---

## STRUTTURA DELLA LEZIONE

### Parte 1: MOTIVAZIONE (30 minuti)
- Limite degli array statici
- Concetto di allocazione dinamica
- Stack vs Heap

### Parte 2: MALLOC (60 minuti)
- Sintassi e parametri
- sizeof e calcolo dei byte
- Controllo NULL
- free e buone pratiche

### Parte 3: CALLOC (45 minuti)
- Sintassi e differenze da malloc
- Quando usare calloc
- Esempi pratici

### Parte 4: REALLOC (45 minuti)
- Ridimensionare la memoria
- Sintassi e comportamento
- Array dinamici che crescono

### Parte 5: PRATICA GUIDATA (60 minuti)
- Tre esercizi costruiti insieme alla classe

### Parte 6: ERRORI COMUNI E RIEPILOGO (45 minuti)
- Memory leak
- Dangling pointer
- Double free
- Riepilogo e domande

---

## PARTE 1: MOTIVAZIONE (30 minuti)

### 1.1 Il Problema degli Array Statici (10 min)

Scrivi questo codice alla lavagna e chiedi alla classe cosa non va:

```c
int voti[30];  // Cosa succede se ho 31 studenti?
               // Cosa succede se ho solo 5 studenti?
```

**Problema 1 — Dimensione fissa troppo piccola:**
```c
#define MAX 30
int voti[MAX];

// Arriva il 31° studente...
// Non c'è spazio! Non possiamo fare nulla.
```

**Problema 2 — Spreco di memoria:**
```c
int voti[1000];  // Alloco spazio per 1000 studenti

// Oggi ci sono solo 5 studenti.
// 995 spazi allocati per nulla!
```

**Problema 3 — Dimensione non nota a priori:**
```c
// L'utente decide quanti elementi vuole a runtime.
// Con un array statico non possiamo saperlo
// prima di eseguire il programma.

printf("Quanti voti? ");
int n;
scanf("%d", &n);

int voti[n];  // ⚠️ VLA: tecnicamente permesso in C99
              // ma sconsigliato: non funziona su tutti i compilatori
              // e non è mai sicuro per dimensioni grandi
```

> "Ci serve un modo per allocare la **quantità esatta** di memoria necessaria, decidendo **durante l'esecuzione**."

---

### 1.2 Memoria Statica vs Dinamica (10 min)

**Dove vivono le variabili in C?**

```
┌──────────────────────────────────────────┐
│                MEMORIA                   │
├──────────────────────────────────────────┤
│  STACK (pila delle chiamate)             │
│  • Variabili locali                      │
│  • Parametri delle funzioni              │
│  • Gestita automaticamente               │
│  • Dimensione limitata (~1-8 MB)         │
│                                          │
│  int x = 10;      → qui                  │
│  int arr[5];      → qui                  │
├──────────────────────────────────────────┤
│  HEAP (memoria libera)                   │
│  • Allocazione dinamica con malloc/calloc│
│  • Gestita MANUALMENTE dal programmatore │
│  • Dimensione molto grande (GB)          │
│  • Deve essere liberata con free()       │
│                                          │
│  malloc(...)      → alloca qui           │
│  calloc(...)      → alloca qui           │
└──────────────────────────────────────────┘
```

**Schema con esempio concreto:**

```
Codice:                   Memoria durante l'esecuzione:

int n = 5;                STACK:
int* arr = malloc(...);   ┌─────────────────┐
                          │ n      = 5      │
                          │ arr    = 0x2A00 │ → punta alla heap
                          └─────────────────┘

                          HEAP (indirizzo 0x2A00):
                          ┌────┬────┬────┬────┬────┐
                          │  ? │  ? │  ? │  ? │  ? │
                          └────┴────┴────┴────┴────┘
                          (malloc: valori casuali)
```

---

### 1.3 Cosa Serve per l'Allocazione Dinamica (10 min)

**Libreria necessaria:**
```c
#include <stdlib.h>  // stdlib = standard library
```

**Le due funzioni:**

| Funzione | Significato | Inizializza? |
|----------|-------------|-------------|
| `malloc` | Memory ALLOCation | ❌ No |
| `calloc` | Contiguous ALLOCation | ✅ Sì (tutto a zero) |

**La funzione per liberare:**
```c
free(puntatore);  // OBBLIGATORIO quando hai finito
```

---

## PARTE 2: MALLOC (60 minuti)

### 2.1 Sintassi e Significato (15 min)

```c
void* malloc(size_t numero_di_byte);
```

Decomposizione della sintassi:

```
void*         → tipo del valore restituito
               → "puntatore generico" (non tipizzato)
               → va convertito al tipo corretto con il cast

size_t        → tipo del parametro
               → è un intero senza segno (per contare i byte)

numero_di_byte → quanti byte contigui allocare nell'heap
```

**Come si usa:**
```c
int* arr = (int*) malloc(n * sizeof(int));
//          ↑              ↑      ↑
//        cast           quanti  quanti byte
//      al tipo          elementi occupa un int
//      corretto
```

**Scrivi alla lavagna il calcolo:**
```
Se n = 5 e sizeof(int) = 4 byte:
→ malloc(5 * 4) = malloc(20)
→ Alloca 20 byte contigui nell'heap
→ Abbastanza per 5 interi
```

---

### 2.2 sizeof — Calcolo Automatico dei Byte (10 min)

**Perché usare `sizeof` invece di un numero fisso?**

```c
// ❌ Sbagliato: numero fisso
int* arr = (int*) malloc(n * 4);  // E se int fosse 8 byte?

// ✅ Corretto: sizeof si adatta al sistema
int* arr = (int*) malloc(n * sizeof(int));
```

**`sizeof` per i tipi più comuni:**

```c
printf("%lu\n", sizeof(int));     // Di solito 4
printf("%lu\n", sizeof(float));   // Di solito 4
printf("%lu\n", sizeof(double));  // Di solito 8
printf("%lu\n", sizeof(char));    // Sempre 1
```

**Esempi di calcolo:**
```c
// Array di 10 interi
int* a = (int*) malloc(10 * sizeof(int));       // 40 byte

// Array di 10 float
float* b = (float*) malloc(10 * sizeof(float)); // 40 byte

// Array di 10 double
double* c = (double*) malloc(10 * sizeof(double)); // 80 byte

// Array di 10 caratteri
char* d = (char*) malloc(10 * sizeof(char));    // 10 byte
```

---

### 2.3 Controllo NULL — Mai Saltarlo (10 min)

> "Se il sistema non ha abbastanza memoria libera, `malloc` restituisce `NULL`."

**Senza controllo — PERICOLOSO:**
```c
int* arr = (int*) malloc(n * sizeof(int));
arr[0] = 10;  // ❌ Se malloc ha fallito, arr è NULL!
              //    → CRASH (segmentation fault)
```

**Con controllo — CORRETTO:**
```c
int* arr = (int*) malloc(n * sizeof(int));

if (arr == NULL) {
    printf("ERRORE: Memoria insufficiente!\n");
    return 1;  // Termina con codice di errore
}

// Da qui in poi arr è sicuramente valido
arr[0] = 10;  // ✅ Sicuro
```

**Regola da ripetere alla classe:**
> "Ogni volta che chiami `malloc` o `calloc`, la riga subito dopo è il controllo `if (ptr == NULL)`."

---

### 2.4 Usare l'Array Dinamico (10 min)

**Buona notizia:** Una volta allocato, si usa esattamente come un array normale!

```c
int n = 5;
int* arr = (int*) malloc(n * sizeof(int));
if (arr == NULL) { return 1; }

// Scrittura — identica agli array normali
arr[0] = 10;
arr[1] = 20;
arr[2] = 30;

// Lettura — identica agli array normali
printf("%d\n", arr[0]);   // 10
printf("%d\n", arr[1]);   // 20

// Ciclo — identico agli array normali
for (int i = 0; i < n; i++) {
    arr[i] = i * 10;
}

// Con puntatori — come abbiamo già visto
int* p = arr;
while (p < arr + n) {
    printf("%d ", *p);
    p++;
}
```

---

### 2.5 free — Liberare la Memoria (15 min)

> "La memoria allocata dinamicamente NON viene liberata automaticamente. Devi farlo tu con `free()`."

**Uso corretto:**
```c
int* arr = (int*) malloc(n * sizeof(int));
if (arr == NULL) { return 1; }

// ... usa arr ...

free(arr);       // 1. Libera la memoria nell'heap
arr = NULL;      // 2. Azzera il puntatore (buona pratica)
```

**Perché `arr = NULL` dopo `free`?**
```c
free(arr);
// arr contiene ancora l'indirizzo di prima!
// Ma quella memoria non ci appartiene più.

*arr = 10;  // ❌ CRASH: stai scrivendo in memoria altrui
            //    (dangling pointer = puntatore pendente)

// Se però fai arr = NULL:
arr = NULL;

*arr = 10;  // Segmentation fault chiaro e immediato
            // Più facile da diagnosticare
if (arr != NULL) { ... }  // Il controllo funziona correttamente
```

**Schema completo del ciclo di vita:**
```
int* arr = (int*) malloc(n * sizeof(int));
     ↓
if (arr == NULL) → ERRORE
     ↓
Usa arr[0], arr[1], ..., arr[n-1]
     ↓
free(arr)   → Memoria restituita al sistema
     ↓
arr = NULL  → Puntatore sicuro
```

---

### 2.6 Esempio Completo con malloc (riassunto) (10 min)

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;

    printf("Quanti numeri? ");
    scanf("%d", &n);

    // 1. Alloca
    int* arr = (int*) malloc(n * sizeof(int));
    if (arr == NULL) {
        printf("Errore: memoria insufficiente!\n");
        return 1;
    }

    // 2. Usa
    for (int i = 0; i < n; i++) {
        printf("arr[%d] = ", i);
        scanf("%d", &arr[i]);
    }

    printf("Array: [ ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("]\n");

    // 3. Libera
    free(arr);
    arr = NULL;

    return 0;
}
```

---

## PARTE 3: CALLOC (45 minuti)

### 3.1 Sintassi e Differenza da malloc (15 min)

```c
void* calloc(size_t numero_elementi, size_t dimensione_elemento);
```

Confronto immediato:
```c
// malloc: un solo parametro (byte totali), NON inizializza
int* a = (int*) malloc(n * sizeof(int));

// calloc: due parametri separati, inizializza a ZERO
int* b = (int*) calloc(n, sizeof(int));
//                     ↑      ↑
//               quanti    quanto è grande
//               elementi  ciascuno
```

**Visualizzazione della differenza:**

```
Dopo malloc(5 * sizeof(int)):
┌──────┬──────┬──────┬──────┬──────┐
│  ?   │  ?   │  ?   │  ?   │  ?   │
└──────┴──────┴──────┴──────┴──────┘
  valori casuali (garbage)

Dopo calloc(5, sizeof(int)):
┌──────┬──────┬──────┬──────┬──────┐
│  0   │  0   │  0   │  0   │  0   │
└──────┴──────┴──────┴──────┴──────┘
  tutto a zero, garantito
```

**Mostra alla classe con codice concreto:**
```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n = 5;

    // Con calloc → tutto a zero
    int* arr = (int*) calloc(n, sizeof(int));
    if (arr == NULL) { return 1; }

    printf("Valori dopo calloc:\n[ ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);   // Stampa: 0 0 0 0 0
    }
    printf("]\n");

    free(arr);
    arr = NULL;
    return 0;
}
```

---

### 3.2 Tabella Comparativa malloc vs calloc (10 min)

| | `malloc` | `calloc` |
|---|---|---|
| **Parametri** | `(byte_totali)` | `(n_elementi, dim_elemento)` |
| **Inizializzazione** | ❌ Valori casuali | ✅ Tutto a zero |
| **Velocità** | Leggermente più veloce | Leggermente più lenta |
| **Uso tipico** | Scrivi subito tutti i valori | Vuoi partire da zero |
| **Controllo NULL** | ✅ Sempre necessario | ✅ Sempre necessario |
| **free** | ✅ Sempre necessario | ✅ Sempre necessario |

**Sono equivalenti per lo spazio:**
```c
// Questi due allocano la stessa quantità di byte:
int* a = (int*) malloc(5 * sizeof(int));   // 20 byte, casuali
int* b = (int*) calloc(5, sizeof(int));    // 20 byte, tutti 0
```

---

### 3.3 Quando Usare Quale (10 min)

**Usa `malloc` quando:**
```c
// Stai per sovrascrivere subito tutti i valori
int* arr = (int*) malloc(n * sizeof(int));
for (int i = 0; i < n; i++) {
    scanf("%d", &arr[i]);  // Scrivo subito → non importa il valore iniziale
}
```

**Usa `calloc` quando:**
```c
// Vuoi che tutti i valori partano da zero
// (es: contatori, accumulatori, flag)
int* contatori = (int*) calloc(n, sizeof(int));
// contatori[i] parte già da 0 → pronto per essere incrementato

// Oppure: scrivi solo alcune posizioni, le altre restano 0
int* arr = (int*) calloc(n, sizeof(int));
arr[2] = 100;  // Solo questa posizione cambia
arr[4] = 200;  // Le altre rimangono 0
```

---

### 3.4 Esempio Completo con calloc (10 min)

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;

    printf("Quanti studenti? ");
    scanf("%d", &n);

    // calloc: partono tutti da 0
    float* voti = (float*) calloc(n, sizeof(float));
    if (voti == NULL) {
        printf("Errore: memoria insufficiente!\n");
        return 1;
    }

    printf("\nVoti iniziali (tutti 0 grazie a calloc):\n[ ");
    for (int i = 0; i < n; i++) {
        printf("%.1f ", voti[i]);
    }
    printf("]\n\n");

    // Inserisci solo alcuni voti
    printf("Inserisci i voti (inserisci -1 per saltare):\n");
    for (int i = 0; i < n; i++) {
        printf("  Studente %d: ", i + 1);
        float v;
        scanf("%f", &v);
        if (v != -1) {
            voti[i] = v;
        }
        // Se -1, rimane 0 (grazie a calloc)
    }

    printf("\nVoti finali:\n[ ");
    for (int i = 0; i < n; i++) {
        printf("%.1f ", voti[i]);
    }
    printf("]\n");

    free(voti);
    voti = NULL;

    return 0;
}
```

---

## PARTE 4: REALLOC — Ridimensionare la Memoria (45 minuti)

### 4.1 Il Problema: Array Troppo Piccolo (10 min)

**Scenario alla lavagna:**

```c
int n = 5;
int* arr = (int*) malloc(n * sizeof(int));

// Riempi l'array...
arr[0] = 10;
arr[1] = 20;
arr[2] = 30;
arr[3] = 40;
arr[4] = 50;

// Ops! Arriva un sesto elemento!
// Come faccio? arr[5] non esiste...
```

**Soluzione ingenua (SBAGLIATA):**
```c
// ❌ NON funziona: malloc alloca un NUOVO blocco
//    I vecchi dati sono PERSI
arr = (int*) malloc(10 * sizeof(int));
// arr[0]...arr[4] adesso contengono valori casuali!
```

**Soluzione manuale (FUNZIONA ma è scomoda):**
```c
// Alloca nuovo array più grande
int* nuovo = (int*) malloc(10 * sizeof(int));

// Copia i vecchi dati
for (int i = 0; i < n; i++) {
    nuovo[i] = arr[i];
}

// Libera il vecchio
free(arr);

// Usa il nuovo
arr = nuovo;
```

> "Questa procedura è così comune che C fornisce `realloc` per farla automaticamente!"

---

### 4.2 Sintassi di realloc (15 min)

```c
void* realloc(void* vecchio_puntatore, size_t nuova_dimensione_in_byte);
```

**Cosa fa `realloc`:**
1. Cerca di **espandere** il blocco di memoria esistente
2. Se non è possibile, **alloca un nuovo blocco** della nuova dimensione
3. **Copia automaticamente** i vecchi dati nel nuovo blocco
4. **Libera automaticamente** il vecchio blocco
5. Ritorna il puntatore al blocco (nuovo o espanso)

**Uso tipico:**
```c
int n = 5;
int* arr = (int*) malloc(n * sizeof(int));
if (arr == NULL) { return 1; }

// ... riempi arr ...

// Devo ingrandire a 10 elementi
n = 10;
int* temp = (int*) realloc(arr, n * sizeof(int));
if (temp == NULL) {
    // Errore: realloc fallita, ma arr è ancora valido!
    free(arr);
    return 1;
}

arr = temp;  // Ora arr punta al blocco ridimensionato
// arr[0]...arr[4] hanno ancora i vecchi valori ✓
// arr[5]...arr[9] hanno valori casuali (come malloc)
```

**⚠️ IMPORTANTE — Usa una variabile temporanea:**

```c
// ❌ SBAGLIATO: se realloc fallisce, arr diventa NULL
//    e perdi l'accesso ai vecchi dati!
arr = (int*) realloc(arr, nuova_dimensione);

// ✅ CORRETTO: usa temp, controlla NULL, poi assegna
int* temp = (int*) realloc(arr, nuova_dimensione);
if (temp == NULL) {
    // arr è ancora valido, puoi fare free
    free(arr);
    return 1;
}
arr = temp;  // Ora sì, sostituisci arr
```

---

### 4.3 Tre Scenari di realloc (10 min)

**Scenario 1: Espansione (ingrandire)**
```c
int* arr = (int*) malloc(5 * sizeof(int));
// ... riempi ...

// Raddoppia la dimensione
int* temp = (int*) realloc(arr, 10 * sizeof(int));
if (temp == NULL) { free(arr); return 1; }
arr = temp;

// arr[0]...arr[4] → dati originali (preservati)
// arr[5]...arr[9] → valori casuali (nuova memoria)
```

**Scenario 2: Riduzione (rimpicciolire)**
```c
int* arr = (int*) malloc(10 * sizeof(int));
// ... usa solo le prime 5 posizioni ...

// Riduci a 5 elementi per risparmiare memoria
int* temp = (int*) realloc(arr, 5 * sizeof(int));
if (temp == NULL) { free(arr); return 1; }
arr = temp;

// arr[0]...arr[4] → dati originali (preservati)
// arr[5]...arr[9] → non esistono più
```

**Scenario 3: realloc(NULL, size)**
```c
// realloc con NULL si comporta come malloc
int* arr = (int*) realloc(NULL, 5 * sizeof(int));
// Equivalente a: malloc(5 * sizeof(int))
```

---

### 4.4 Esempio Completo: Array Dinamico che Cresce (10 min)

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int capacita = 2;  // Capacità iniziale piccola
    int dimensione = 0; // Quanti elementi effettivi

    int* arr = (int*) malloc(capacita * sizeof(int));
    if (arr == NULL) {
        printf("Errore allocazione!\n");
        return 1;
    }

    printf("Inserisci numeri (0 per terminare):\n");

    while (1) {
        int num;
        printf("  Numero: ");
        scanf("%d", &num);

        if (num == 0) break;

        // Se l'array è pieno, raddoppia la capacità
        if (dimensione == capacita) {
            capacita *= 2;
            printf("    → Array pieno! Raddoppio a %d elementi...\n", capacita);

            int* temp = (int*) realloc(arr, capacita * sizeof(int));
            if (temp == NULL) {
                printf("Errore realloc!\n");
                free(arr);
                return 1;
            }
            arr = temp;
        }

        arr[dimensione++] = num;
    }

    // Stampa risultato
    printf("\nArray finale (%d elementi, capacità %d):\n[ ",
           dimensione, capacita);
    for (int i = 0; i < dimensione; i++) {
        printf("%d ", arr[i]);
    }
    printf("]\n");

    free(arr);
    arr = NULL;

    return 0;
}
```

**Output esempio:**
```
Inserisci numeri (0 per terminare):
  Numero: 10
  Numero: 20
  Numero: 30
    → Array pieno! Raddoppio a 4 elementi...
  Numero: 40
  Numero: 50
    → Array pieno! Raddoppio a 8 elementi...
  Numero: 60
  Numero: 0

Array finale (6 elementi, capacità 8):
[ 10 20 30 40 50 60 ]
```

**Concetto chiave da sottolineare:**
> "Questa è la tecnica usata dai vettori dinamici in altri linguaggi (es: `ArrayList` in Java, `vector` in C++, `list` in Python). Quando l'array è pieno, si raddoppia automaticamente!"

---

## PARTE 5: PRATICA GUIDATA (60 minuti)

### Esercizio Guidato 1: Array di float con malloc (15 min)

**Da costruire insieme:**
Chiedere n temperature, calcolare media, trovare la più alta e la più bassa.

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;

    printf("Quante temperature? ");
    scanf("%d", &n);

    float* temp = (float*) malloc(n * sizeof(float));
    if (temp == NULL) {
        printf("Errore allocazione!\n");
        return 1;
    }

    for (int i = 0; i < n; i++) {
        printf("  Temperatura %d: ", i + 1);
        scanf("%f", &temp[i]);
    }

    // Media
    float somma = 0;
    for (int i = 0; i < n; i++) somma += temp[i];
    float media = somma / n;

    // Max e min
    float max = temp[0], min = temp[0];
    for (int i = 1; i < n; i++) {
        if (temp[i] > max) max = temp[i];
        if (temp[i] < min) min = temp[i];
    }

    printf("\nMedia:    %.2f°C\n", media);
    printf("Massima:  %.2f°C\n", max);
    printf("Minima:   %.2f°C\n", min);

    free(temp);
    temp = NULL;

    return 0;
}
```

---

### Esercizio Guidato 2: Contatori con calloc (20 min)

**Scenario:** Hai un array di voti (da 0 a 10). Conta quante volte compare ogni voto.

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;

    printf("Quanti voti? ");
    scanf("%d", &n);

    // Array dei voti
    int* voti = (int*) malloc(n * sizeof(int));
    if (voti == NULL) { return 1; }

    // Contatori per ogni voto da 0 a 10
    // calloc: partono tutti da 0, pronti per il conteggio
    int* contatori = (int*) calloc(11, sizeof(int));
    if (contatori == NULL) {
        free(voti);
        return 1;
    }

    for (int i = 0; i < n; i++) {
        printf("  Voto %d: ", i + 1);
        scanf("%d", &voti[i]);
    }

    // Conta le occorrenze
    for (int i = 0; i < n; i++) {
        if (voti[i] >= 0 && voti[i] <= 10) {
            contatori[voti[i]]++;
        }
    }

    // Stampa distribuzione
    printf("\n=== DISTRIBUZIONE VOTI ===\n");
    for (int v = 0; v <= 10; v++) {
        if (contatori[v] > 0) {
            printf("  Voto %2d: %d volte\n", v, contatori[v]);
        }
    }

    free(voti);
    voti = NULL;
    free(contatori);
    contatori = NULL;

    return 0;
}
```

**Punto chiave da sottolineare:**
> "Senza `calloc`, i contatori avrebbero valori casuali e il conteggio sarebbe sbagliato. Con `calloc` partono tutti da 0, perfetti per essere incrementati."

---

### Esercizio Guidato 3: Due Array Paralleli (25 min)

**Scenario:** Gestisci una classe con nomi e voti in due array dinamici separati.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    int n;

    printf("Quanti studenti? ");
    scanf("%d", &n);
    getchar();

    // Array di puntatori a stringhe (per i nomi)
    char** nomi = (char**) malloc(n * sizeof(char*));
    if (nomi == NULL) { return 1; }

    // Array di voti
    float* voti = (float*) calloc(n, sizeof(float));
    if (voti == NULL) {
        free(nomi);
        return 1;
    }

    // Inserimento
    for (int i = 0; i < n; i++) {
        char buffer[100];
        printf("\nStudente %d:\n", i + 1);

        printf("  Nome: ");
        fgets(buffer, sizeof(buffer), stdin);
        buffer[strcspn(buffer, "\n")] = '\0';

        // Alloca esattamente la dimensione giusta per il nome
        nomi[i] = (char*) malloc((strlen(buffer) + 1) * sizeof(char));
        if (nomi[i] == NULL) {
            // Libera tutto ciò che è già stato allocato
            for (int j = 0; j < i; j++) free(nomi[j]);
            free(nomi);
            free(voti);
            return 1;
        }
        strcpy(nomi[i], buffer);

        printf("  Voto: ");
        scanf("%f", &voti[i]);
        getchar();
    }

    // Calcola media
    float somma = 0;
    for (int i = 0; i < n; i++) somma += voti[i];
    float media = somma / n;

    // Stampa risultati
    printf("\n=== RISULTATI CLASSE ===\n");
    printf("%-20s | %s\n", "NOME", "VOTO");
    printf("%-20s | %s\n", "--------------------", "------");
    for (int i = 0; i < n; i++) {
        printf("%-20s | %.2f  %s\n",
               nomi[i],
               voti[i],
               voti[i] >= media ? "✓" : "");
    }
    printf("\nMedia classe: %.2f\n", media);

    // Libera tutta la memoria
    for (int i = 0; i < n; i++) {
        free(nomi[i]);
        nomi[i] = NULL;
    }
    free(nomi);
    nomi = NULL;
    free(voti);
    voti = NULL;

    return 0;
}
```

---

## PARTE 6: ERRORI COMUNI E RIEPILOGO (45 minuti)

### 5.1 I Tre Errori Più Frequenti (20 min)

---

**Errore 1: MEMORY LEAK (Perdita di Memoria)**

> "Allochi memoria ma non la liberi mai."

```c
// ❌ SBAGLIATO: memory leak
void funzioneConLeak() {
    int* arr = (int*) malloc(100 * sizeof(int));
    // ... usa arr ...
    return;  // La funzione termina senza free!
             // La memoria rimane occupata per sempre
             // (fino alla fine del programma)
}

// ✅ CORRETTO
void funzioneSicura() {
    int* arr = (int*) malloc(100 * sizeof(int));
    if (arr == NULL) return;
    // ... usa arr ...
    free(arr);      // Libera prima di uscire
    arr = NULL;
}
```

**Analogia:**
> "Un memory leak è come affittare una stanza e non restituirla mai. Il sistema alla fine non ha più stanze da affittare."

---

**Errore 2: DANGLING POINTER (Puntatore Pendente)**

> "Usi un puntatore dopo averlo liberato."

```c
// ❌ SBAGLIATO: dangling pointer
int* arr = (int*) malloc(5 * sizeof(int));
arr[0] = 10;

free(arr);     // Memoria liberata

arr[0] = 20;  // ❌ CRASH o comportamento indefinito!
               // arr punta a memoria che non ci appartiene più

// ✅ CORRETTO
free(arr);
arr = NULL;    // Azzera subito

if (arr != NULL) {  // Il controllo ora funziona correttamente
    arr[0] = 20;
}
```

---

**Errore 3: DOUBLE FREE**

> "Liberi la stessa memoria due volte."

```c
// ❌ SBAGLIATO: double free
int* arr = (int*) malloc(5 * sizeof(int));
free(arr);
free(arr);   // ❌ CRASH! Liberato due volte → corruzione dell'heap

// ✅ CORRETTO
free(arr);
arr = NULL;  // NULL rende il secondo free innocuo

free(arr);   // free(NULL) è sicuro: non fa nulla
```

---

### 6.2 Riepilogo Visivo (10 min)

Scrivi alla lavagna questo schema riassuntivo:

```
CICLO DI VITA DI UN ARRAY DINAMICO
────────────────────────────────────

  1. DICHIARA il puntatore
     int* arr;

  2. ALLOCA la memoria
     arr = (int*) malloc(n * sizeof(int));
          oppure
     arr = (int*) calloc(n, sizeof(int));

  3. CONTROLLA se è riuscita
     if (arr == NULL) { gestisci l'errore }

  4. USA l'array normalmente
     arr[0] = 10;
     arr[i] = valore;
     printf("%d", arr[j]);

  5. (OPZIONALE) RIDIMENSIONA se necessario
     int* temp = (int*) realloc(arr, nuova_dim * sizeof(int));
     if (temp == NULL) { free(arr); return 1; }
     arr = temp;

  6. LIBERA la memoria
     free(arr);
     arr = NULL;

────────────────────────────────────

  malloc   → valori CASUALI, un solo parametro
  calloc   → valori ZERO,    due parametri
  realloc  → RIDIMENSIONA,   preserva i dati esistenti
  free     → SEMPRE, per ogni malloc/calloc/realloc
  = NULL   → SEMPRE dopo free
```

---

### 6.3 Domande di Verifica (15 min)

1. **"Qual è la differenza tra `malloc` e `calloc`?"**
2. **"Perché dobbiamo sempre controllare se il risultato è `NULL`?"**
3. **"Cos'è un memory leak? Come si evita?"**
4. **"Cos'è un dangling pointer? Come si evita?"**
5. **"Cosa succede se chiami `free` due volte sullo stesso puntatore?"**
6. **"Quando usi `realloc` e perché devi usare una variabile temporanea?"**

---

<details>
<summary><b>📝 RISPOSTE PER IL DOCENTE</b></summary>

### 1. Differenza malloc vs calloc

**Risposta:**

**`malloc(n * sizeof(tipo))`:**
- Un solo parametro: il numero totale di byte
- NON inizializza: i valori sono casuali (garbage)
- Leggermente più veloce

**`calloc(n, sizeof(tipo))`:**
- Due parametri separati: numero di elementi e dimensione di ciascuno
- INIZIALIZZA tutto a zero
- Leggermente più lenta (deve scrivere zero ovunque)

**Sono equivalenti per lo spazio allocato:**
```c
malloc(5 * sizeof(int))  ≡  calloc(5, sizeof(int))  // 20 byte
```

**Quando preferire quale:**
- `malloc` → se scrivi subito tutti i valori (l'inizializzazione verrebbe sovrascritta)
- `calloc` → se vuoi partire da zero (contatori, flag, array parzialmente riempiti)

---

### 2. Perché controllare NULL

**Risposta:**

`malloc` e `calloc` restituiscono `NULL` quando il sistema non riesce ad allocare la memoria richiesta (es: memoria insufficiente, richiesta troppo grande).

Se non si controlla e si usa direttamente un puntatore `NULL`:
```c
int* arr = (int*) malloc(n * sizeof(int));
arr[0] = 10;  // Se arr è NULL → SEGMENTATION FAULT → crash del programma
```

Il controllo permette di gestire l'errore in modo controllato:
```c
if (arr == NULL) {
    printf("Errore!\n");
    return 1;  // Termina in modo pulito
}
```

**Analogia:** È come aprire uno sportello bancomat e usare i soldi che escono, senza prima controllare se ne sono effettivamente usciti.

---

### 3. Memory Leak

**Risposta:**

Un **memory leak** (perdita di memoria) si verifica quando si alloca memoria dinamicamente ma non la si libera mai con `free`.

**Conseguenze:**
- La memoria rimane occupata finché il programma è in esecuzione
- In programmi longevi (server, app) porta all'esaurimento della memoria disponibile
- Il sistema operativo recupera la memoria alla chiusura del programma, ma è cattiva pratica

**Come si evita:**
- Regola semplice: per ogni `malloc`/`calloc` ci deve essere un `free`
- Liberare sempre prima di uscire da una funzione
- Liberare sempre prima di rassegnare un puntatore:

```c
// ❌ Leak: il vecchio blocco è perso
arr = (int*) malloc(10 * sizeof(int));
arr = (int*) malloc(20 * sizeof(int));  // Il primo blocco non si può più liberare!

// ✅ Corretto
arr = (int*) malloc(10 * sizeof(int));
free(arr);
arr = (int*) malloc(20 * sizeof(int));
```

---

### 4. Dangling Pointer

**Risposta:**

Un **dangling pointer** (puntatore pendente) è un puntatore che continua a contenere un indirizzo di memoria dopo che quella memoria è stata liberata con `free`.

**Il problema:**
```c
free(arr);   // La memoria è stata restituita al sistema
arr[0] = 5;  // arr punta ancora lì, ma quella memoria
             // potrebbe essere stata assegnata ad altro!
             // → Comportamento indefinito, crash, dati corrotti
```

**Come si evita:**
Subito dopo `free`, assegnare `NULL` al puntatore:
```c
free(arr);
arr = NULL;  // arr non punta più a nulla
             // Qualsiasi accesso a NULL dà segfault immediato
             // → più facile da diagnosticare
```

---

### 5. Double Free

**Risposta:**

Un **double free** si verifica quando si chiama `free` due volte sullo stesso puntatore.

**Il problema:**
```c
free(arr);
free(arr);  // La struttura interna dell'heap viene corrotta
            // → crash, comportamento imprevedibile
```

**Come si evita:**
```c
free(arr);
arr = NULL;  // free(NULL) è definito dallo standard come "non fare nulla"

free(arr);   // Ora è sicuro: free(NULL) viene ignorato
```

Impostare `arr = NULL` dopo `free` rende il double free innocuo.

---

### 6. realloc e variabile temporanea

**Risposta:**

`realloc` si usa quando hai bisogno di **ridimensionare** un array dinamico già allocato (ingrandire o rimpicciolire).

**Cosa fa `realloc`:**
```c
int* temp = (int*) realloc(arr, nuova_dimensione);
```
1. Cerca di espandere il blocco esistente
2. Se non può, alloca un nuovo blocco della nuova dimensione
3. Copia automaticamente i vecchi dati
4. Libera automaticamente il vecchio blocco
5. Ritorna il puntatore al blocco (nuovo o espanso)

**Perché usare una variabile temporanea:**
```c
// ❌ SBAGLIATO
arr = (int*) realloc(arr, nuova_dimensione);
// Se realloc fallisce (ritorna NULL), perdi l'accesso
// ai vecchi dati! arr diventa NULL e non puoi più fare free.

// ✅ CORRETTO
int* temp = (int*) realloc(arr, nuova_dimensione);
if (temp == NULL) {
    // realloc è fallita, ma arr è ancora valido!
    // Puoi gestire l'errore, usare i vecchi dati, o fare free
    free(arr);
    return 1;
}
arr = temp;  // Solo ora sostituisci arr
```

La variabile temporanea protegge il puntatore originale in caso di fallimento.

**Cosa preserva `realloc`:**
- Se ingrandisci: i vecchi dati sono copiati, le nuove posizioni hanno valori casuali
- Se rimpicciolisci: i primi N elementi sono preservati, il resto viene scartato

</details>

---

## NOTE PER IL DOCENTE

### ⚠️ Punti critici da monitorare:

1. **Dimenticare il controllo NULL** — gli studenti tendono a saltarlo
2. **Dimenticare `free`** — abituarsi a scriverlo subito dopo `malloc`
3. **Confondere `malloc` e `calloc`** — i valori iniziali non sono la stessa cosa
4. **Riassegnare un puntatore senza `free`** — il memory leak più comune
5. **Usare array dopo `free`** — dangling pointer difficile da debuggare

### 💡 Suggerimenti didattici:

- Scrivi sempre il `free` subito dopo il `malloc` nel codice, poi aggiungi il codice in mezzo
- Mostra con `valgrind` (se disponibile) i memory leak: è molto efficace
- Fai disegnare la memoria (stack + heap) per ogni programma
- Insisti sul fatto che l'array dinamico si usa **esattamente come uno statico**
- Il punto di forza è la **flessibilità**: mostralo con un programma che funziona per qualsiasi n

### 🎯 Obiettivi minimi per questa lezione:

Lo studente è pronto se:
- Sa allocare un array con `malloc` e `calloc`
- Controlla sempre `NULL`
- Sa usare `free` correttamente
- Capisce la differenza tra array statico e dinamico
- Conosce i tre errori principali (leak, dangling, double free)

---

**Buona lezione! 🚀**
