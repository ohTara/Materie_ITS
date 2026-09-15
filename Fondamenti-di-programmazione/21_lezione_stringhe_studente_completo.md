# Lezione G13: Ordinamento e Stringhe — Operazioni su stringhe con `string.h`

**Durata totale:** 4 ore
**Teoria:** 3 ore | **Esercizi:** 1 ora
**Data:** _______________
**Ambiente:** CLion (JetBrains)
**Giornata:** G13 di 19 — Ore corso: 48/76

---

## PARTE 1 — TEORIA (3 ore)

### 1.1 Introduzione e motivazione

Nella vita reale i dati non sono solo numeri: nomi, cognomi, città, codici fiscali, email — tutto è testo. Un programma che sa gestire e ordinare stringhe è molto più vicino a un'applicazione reale.

Pensiamo a una rubrica telefonica: vogliamo visualizzare l'elenco in ordine alfabetico. Pensiamo a un motore di ricerca: deve trovare una parola all'interno di un testo. Pensiamo a un form di registrazione: deve verificare che la password abbia almeno 8 caratteri e contenga un numero.

Tutte queste operazioni richiedono la manipolazione di stringhe. In C le stringhe non sono un tipo primitivo: sono **array di `char`** terminati da un carattere speciale, il **terminatore nullo `'\0'`**. La libreria `string.h` fornisce le funzioni standard per operare su di esse in modo efficiente e sicuro.

---

### 1.2 Spiegazione dell'argomento

#### Le stringhe in C: struttura interna

Una stringa in C è un array di caratteri che termina obbligatoriamente con `'\0'` (valore ASCII 0):

```
char nome[10] = "Mario";

Indice:  [0]  [1]  [2]  [3]  [4]  [5]  [6]  [7]  [8]  [9]
Valore:  'M'  'a'  'r'  'i'  'o'  '\0'  ?    ?    ?    ?
                                    ↑
                              terminatore nullo
                              (OBBLIGATORIO)
```

Il terminatore `'\0'` è fondamentale: senza di esso le funzioni non sanno dove finisce la stringa e leggono dati in memoria casuali (comportamento indefinito).

---

#### Dichiarazione e inizializzazione

```c
// Metodo 1: dimensione esplicita con inizializzazione letterale
char s1[20] = "Ciao";
// Memoria: 'C' 'i' 'a' 'o' '\0' ? ? ? ? ? ...

// Metodo 2: dimensione automatica (conta i char + '\0')
char s2[] = "Mondo";
// Dimensione = 6 (5 caratteri + '\0')

// Metodo 3: array non inizializzato
char s3[50];
// Contenuto imprevedibile — va scritto prima di essere letto

// Lettura da tastiera
char s4[50];
scanf("%s", s4);         // legge fino al primo spazio
fgets(s4, 50, stdin);    // legge l'intera riga (inclusi spazi)
```

**Regola critica — NON si usa `=` per assegnare dopo la dichiarazione:**
```c
char s[20];
s = "Ciao";        // ❌ ERRORE di compilazione
s = s2;            // ❌ ERRORE di compilazione
strcpy(s, "Ciao"); // ✅ corretto
strcpy(s, s2);     // ✅ corretto
```

---

#### `strlen` — lunghezza della stringa

```c
#include <string.h>
size_t strlen(const char *s);
```

Conta i caratteri fino a `'\0'` (escluso). Restituisce un `size_t` (intero senza segno).

```
"Mario"   →   strlen = 5
"Ciao"    →   strlen = 4
""        →   strlen = 0   (stringa vuota: solo '\0')
```

```c
char nome[] = "Giovanni";
int len = strlen(nome);          // len = 8
char ultimo = nome[len - 1];     // ultimo = 'i'
```

**Uso frequente:** rimuovere `'\n'` da `fgets`:
```c
char s[100];
fgets(s, sizeof(s), stdin);
if (s[strlen(s) - 1] == '\n')
    s[strlen(s) - 1] = '\0';
```

---

#### `strcpy` — copia di stringa

```c
char *strcpy(char *dest, const char *src);
```

Copia `src` in `dest`, incluso il `'\0'` finale. Il buffer `dest` deve essere abbastanza grande.

```
src:  'C' 'i' 'a' 'o' '\0'
              ↓ copia tutto
dest: 'C' 'i' 'a' 'o' '\0'
```

```c
char originale[] = "Programmazione";
char copia[20];
strcpy(copia, originale);
printf("%s\n", copia);  // stampa: Programmazione
```

**Attenzione al buffer overflow:**
```c
char piccolo[5];
strcpy(piccolo, "Programmazione");  // ❌ PERICOLOSO: scrive fuori dall'array!
```

---

#### `strcat` — concatenazione

```c
char *strcat(char *dest, const char *src);
```

Aggiunge `src` alla fine di `dest`, sovrascrivendo il `'\0'` di `dest`.

```
Prima:   dest = "Ciao, \0"       src = "Mondo\0"
                       ↑ qui inizia la scrittura
Dopo:    dest = "Ciao, Mondo\0"
```

```c
char saluto[50] = "Ciao, ";
char nome[] = "Maria";
strcat(saluto, nome);
strcat(saluto, "!");
printf("%s\n", saluto);  // stampa: Ciao, Maria!
```

**Regola pratica:** la dimensione di `dest` deve essere ≥ `strlen(dest) + strlen(src) + 1`.

---

#### `strcmp` — confronto di stringhe

```c
int strcmp(const char *s1, const char *s2);
```

Confronta carattere per carattere secondo il codice ASCII. Restituisce:

```
┌─────────────────┬──────────────────────────────────────────┐
│ Valore ritorno  │ Significato                              │
├─────────────────┼──────────────────────────────────────────┤
│      0          │ s1 e s2 sono identiche                  │
│    < 0          │ s1 viene prima di s2 (ordine alfab.)    │
│    > 0          │ s1 viene dopo di s2 (ordine alfab.)     │
└─────────────────┴──────────────────────────────────────────┘
```

**Come funziona internamente:**
```
strcmp("Anna", "Carlo"):
  'A' (65) vs 'C' (67)  →  65 - 67 = -2  →  risultato negativo

strcmp("Luca", "Luca"):
  tutti i char uguali fino a '\0'  →  0

strcmp("Zara", "Zorro"):
  'Z'='Z', 'a'(97) vs 'o'(111)  →  risultato negativo
```

**Errore classico — non usare `==` per le stringhe:**
```c
char s1[] = "Ciao";
char s2[] = "Ciao";

if (s1 == s2)            // ❌ SBAGLIATO: confronta indirizzi di memoria!
    printf("Uguali\n");

if (strcmp(s1, s2) == 0) // ✅ CORRETTO: confronta il contenuto
    printf("Uguali\n");
```

---

#### `strchr` — ricerca di un carattere

```c
char *strchr(const char *s, int c);
```

Cerca la **prima occorrenza** del carattere `c` nella stringa `s`. Restituisce un puntatore al carattere trovato, oppure `NULL` se non esiste.

```c
char frase[] = "Programmazione";
char *ptr = strchr(frase, 'a');

if (ptr != NULL) {
    printf("Trovata 'a' alla posizione %ld\n", ptr - frase);
}
```

**Uso pratico — verificare la presenza di un carattere:**
```c
char email[] = "utente@esempio.it";
if (strchr(email, '@') != NULL)
    printf("Email valida (contiene @)\n");
else
    printf("Email non valida\n");
```

---

#### `strstr` — ricerca di una sottostringa

```c
char *strstr(const char *haystack, const char *needle);
```

Cerca la **prima occorrenza** della sottostringa `needle` all'interno di `haystack`. Restituisce un puntatore all'inizio della sottostringa trovata, oppure `NULL`.

```c
char testo[] = "Il linguaggio C è potente";
char *ptr = strstr(testo, "linguaggio");

if (ptr != NULL) {
    printf("Trovato a posizione %ld\n", ptr - testo);  // posizione 3
    printf("Da lì: %s\n", ptr);  // stampa: linguaggio C è potente
}
```

---

#### Ordinamento alfabetico con `strcmp` e Bubble Sort

Applicare l'ordinamento alfabetico richiede solo due cambiamenti rispetto al Bubble Sort numerico:

```
ORDINAMENTO NUMERICO          ORDINAMENTO ALFABETICO
─────────────────────         ──────────────────────────────────
Confronto:                    Confronto:
  if (a[i] > a[i+1])           if (strcmp(a[i], a[i+1]) > 0)

Scambio:                      Scambio:
  int temp = a[i];              char temp[MAX];
  a[i] = a[i+1];                strcpy(temp, a[i]);
  a[i+1] = temp;                strcpy(a[i], a[i+1]);
                                strcpy(a[i+1], temp);
```

**Schema del processo:**
```
Array iniziale:  ["Zara", "Anna", "Marco", "Giulia"]

Passata 1:
  strcmp("Zara","Anna") > 0  →  SCAMBIA  →  ["Anna", "Zara", "Marco", "Giulia"]
  strcmp("Zara","Marco") > 0 →  SCAMBIA  →  ["Anna", "Marco", "Zara", "Giulia"]
  strcmp("Zara","Giulia") > 0 → SCAMBIA  →  ["Anna", "Marco", "Giulia", "Zara"]

Passata 2:
  strcmp("Anna","Marco") < 0  →  no scambio
  strcmp("Marco","Giulia") > 0 → SCAMBIA →  ["Anna", "Giulia", "Marco", "Zara"]

Risultato: ["Anna", "Giulia", "Marco", "Zara"] ✅
```

---

#### Array bidimensionale di stringhe

```c
char nomi[5][30];
//        ↑   ↑
//   quante   lunghezza massima
//   stringhe  di ogni stringa (incluso '\0')
```

**Visualizzazione in memoria:**
```
nomi[0]: 'A' 'n' 'n' 'a' '\0' ? ? ...
nomi[1]: 'M' 'a' 'r' 'c' 'o' '\0' ? ...
nomi[2]: 'G' 'i' 'u' 'l' 'i' 'a' '\0' ...
```

Ogni riga è una stringa indipendente, accessibile con `nomi[i]`.

---

### 1.3 Esempi di codice commentati

#### Esempio 1 — Funzioni base di `string.h`

```c
#include <stdio.h>
#include <string.h>

int main() {
    char s1[50] = "Ciao";
    char s2[50] = "Mondo";
    char s3[50];

    printf("Lunghezza di '%s': %zu\n", s1, strlen(s1));

    strcpy(s3, s1);
    printf("s3 dopo strcpy: %s\n", s3);

    strcat(s1, ", ");
    strcat(s1, s2);
    strcat(s1, "!");
    printf("s1 dopo strcat: %s\n", s1);

    int cmp = strcmp("Anna", "Carla");
    if (cmp < 0)
        printf("Anna viene prima di Carla\n");
    else if (cmp > 0)
        printf("Anna viene dopo Carla\n");
    else
        printf("Stringhe uguali\n");

    return 0;
}
```

**Output atteso:**
```
Lunghezza di 'Ciao': 4
s3 dopo strcpy: Ciao
s1 dopo strcat: Ciao, Mondo!
Anna viene prima di Carla
```

---

#### Esempio 2 — Ricerca con `strchr` e `strstr`

```c
#include <stdio.h>
#include <string.h>

int main() {
    char frase[] = "Programmazione in C";
    char *ptr;

    ptr = strchr(frase, 'z');
    if (ptr != NULL)
        printf("'z' trovata alla posizione %ld\n", ptr - frase);
    else
        printf("'z' non trovata\n");

    if (strchr(frase, 'C') != NULL)
        printf("La frase contiene 'C'\n");

    ptr = strstr(frase, "in C");
    if (ptr != NULL)
        printf("Sottostringa 'in C' trovata: \"%s\"\n", ptr);

    ptr = strstr(frase, "Python");
    if (ptr == NULL)
        printf("'Python' non presente\n");

    return 0;
}
```

**Output atteso:**
```
'z' trovata alla posizione 8
La frase contiene 'C'
Sottostringa 'in C' trovata: "in C"
'Python' non presente
```

---

#### Esempio 3 — Ordinamento alfabetico con Bubble Sort

```c
#include <stdio.h>
#include <string.h>

#define N 5
#define MAX_LEN 30

void stampa_array(char arr[][MAX_LEN], int n) {
    int i;
    for (i = 0; i < n; i++)
        printf("  [%d] %s\n", i, arr[i]);
}

int main() {
    char nomi[N][MAX_LEN] = {"Zara", "Anna", "Marco", "Giulia", "Bruno"};
    char temp[MAX_LEN];
    int i, j;

    printf("Prima dell'ordinamento:\n");
    stampa_array(nomi, N);

    for (i = 0; i < N - 1; i++) {
        for (j = 0; j < N - 1 - i; j++) {
            if (strcmp(nomi[j], nomi[j+1]) > 0) {
                strcpy(temp,      nomi[j]);
                strcpy(nomi[j],   nomi[j+1]);
                strcpy(nomi[j+1], temp);
            }
        }
    }

    printf("\nDopo l'ordinamento:\n");
    stampa_array(nomi, N);

    return 0;
}
```

**Output atteso:**
```
Prima dell'ordinamento:
  [0] Zara
  [1] Anna
  [2] Marco
  [3] Giulia
  [4] Bruno

Dopo l'ordinamento:
  [0] Anna
  [1] Bruno
  [2] Giulia
  [3] Marco
  [4] Zara
```

---

#### Esempio 4 — Lettura da tastiera con `fgets`

```c
#include <stdio.h>
#include <string.h>

#define MAX_NOMI 4
#define MAX_LEN 50

int main() {
    char nomi[MAX_NOMI][MAX_LEN];
    char temp[MAX_LEN];
    int i, j;

    for (i = 0; i < MAX_NOMI; i++) {
        printf("Inserisci nome %d: ", i + 1);
        fgets(nomi[i], MAX_LEN, stdin);
        if (nomi[i][strlen(nomi[i]) - 1] == '\n')
            nomi[i][strlen(nomi[i]) - 1] = '\0';
    }

    for (i = 0; i < MAX_NOMI - 1; i++) {
        for (j = 0; j < MAX_NOMI - 1 - i; j++) {
            if (strcmp(nomi[j], nomi[j+1]) > 0) {
                strcpy(temp,      nomi[j]);
                strcpy(nomi[j],   nomi[j+1]);
                strcpy(nomi[j+1], temp);
            }
        }
    }

    printf("\nNomi in ordine alfabetico:\n");
    for (i = 0; i < MAX_NOMI; i++)
        printf("  %s\n", nomi[i]);

    return 0;
}
```

**Output atteso (esempio):**
```
Inserisci nome 1: Zara
Inserisci nome 2: Anna
Inserisci nome 3: Marco
Inserisci nome 4: Bruno

Nomi in ordine alfabetico:
  Anna
  Bruno
  Marco
  Zara
```

---

### 1.4 Riepilogo visivo

```
┌──────────────────────────────────────────────────────────────────────┐
│                    FUNZIONI DI string.h                              │
├──────────────────┬─────────────────┬───────────────────────────────  │
│ FUNZIONE         │ RESTITUISCE     │ USO TIPICO                      │
├──────────────────┼─────────────────┼───────────────────────────────  │
│ strlen(s)        │ size_t          │ Lunghezza, accesso ultimo char  │
│ strcpy(dst, src) │ char* (dst)     │ Copia / assegnazione            │
│ strcat(dst, src) │ char* (dst)     │ Concatenazione                  │
│ strcmp(s1, s2)   │ int <0, 0, >0   │ Confronto / ordinamento         │
│ strchr(s, c)     │ char* o NULL    │ Presenza/posizione di un char   │
│ strstr(s, sub)   │ char* o NULL    │ Presenza/posizione sottostringa │
└──────────────────┴─────────────────┴───────────────────────────────  ┘

BUBBLE SORT STRINGHE
─────────────────────────────────────────────
  for (i = 0; i < n-1; i++)
    for (j = 0; j < n-1-i; j++)
      if (strcmp(nomi[j], nomi[j+1]) > 0) {
        strcpy(temp,       nomi[j]);
        strcpy(nomi[j],    nomi[j+1]);
        strcpy(nomi[j+1],  temp);
      }

ERRORI FREQUENTI
─────────────────────────────────────────────
  ❌  s1 == s2           ✅  strcmp(s1, s2) == 0
  ❌  s1 = "testo"       ✅  strcpy(s1, "testo")
  ❌  s1 = s2            ✅  strcpy(s1, s2)
  ❌  s1 + s2            ✅  strcat(s1, s2)
  ❌  temp = nomi[i]     ✅  strcpy(temp, nomi[i])
```

---

### 1.5 Domande di verifica orale

**D1:** Cos'è il terminatore nullo `'\0'`? Perché è indispensabile?

<details>
<summary><b>💡 RISPOSTA</b></summary>

È il carattere con valore ASCII 0 che marca la fine di ogni stringa in C. Tutte le funzioni di `string.h` si basano su di esso per sapere dove si ferma la stringa: senza `'\0'`, `strlen`, `strcpy`, `printf` con `%s` continuerebbero a leggere oltre i limiti della stringa, con risultati imprevedibili.

</details>

---

**D2:** Perché non si può usare `==` per confrontare due stringhe? Cosa confronta realmente?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Il nome di un array in C è un puntatore al suo primo elemento. Usare `==` confronta quindi gli *indirizzi di memoria* delle due stringhe, non il loro contenuto. Due array diversi hanno sempre indirizzi diversi, anche se contengono gli stessi caratteri. Si deve usare `strcmp()` che confronta carattere per carattere.

</details>

---

**D3:** `strcmp("Banana", "Ananas")` restituisce un valore positivo o negativo? Perché?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Positivo. `strcmp` confronta il primo carattere diverso: `'B'` (ASCII 66) vs `'A'` (ASCII 65). Poiché `'B' > 'A'`, il risultato è positivo, indicando che "Banana" viene *dopo* "Ananas" in ordine alfabetico.

</details>

---

**D4:** Ho un array `char nomi[10][50]`. Quanta memoria totale occupa? E quante stringhe può contenere?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Occupa `10 × 50 = 500 byte`. Può contenere al massimo 10 stringhe, ciascuna lunga al massimo 49 caratteri (il cinquantesimo è riservato al `'\0'`).

</details>

---

**D5:** Perché nel Bubble Sort per stringhe non posso scrivere `temp = nomi[i]`?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Perché `nomi[i]` è un array e in C non si possono assegnare array con `=`. L'operatore `=` copierebbe solo il puntatore (l'indirizzo), non il contenuto. È necessario usare `strcpy(temp, nomi[i])` per copiare effettivamente tutti i caratteri.

</details>

---

**D6:** Cosa restituisce `strchr("Hello", 'l')`? E se il carattere non c'è?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Restituisce un puntatore alla *prima* occorrenza di `'l'` nella stringa, che si trova all'indice 2. Se il carattere non fosse presente, restituirebbe `NULL`. Il valore `NULL` va sempre controllato prima di usare il puntatore restituito.

</details>

---

**D7:** `fgets` include il carattere `'\n'` nella stringa letta? Come si rimuove?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Sì, `fgets` include il `'\n'` se c'è spazio nel buffer. Lo si rimuove controllando l'ultimo carattere: `if (s[strlen(s)-1] == '\n') s[strlen(s)-1] = '\0';` — si sovrascrive il `'\n'` con il terminatore nullo.

</details>

---

## PARTE 2 — ESERCIZI (1 ora)

---

### 🟢 Esercizio 1 — Analisi di una stringa (Base)

**Testo:** Scrivi un programma che legge una stringa dall'utente (max 100 caratteri) e stampa:
- La lunghezza della stringa
- Il primo e l'ultimo carattere
- Se contiene la lettera `'a'` (maiuscola o minuscola)

**Esempio input/output:**
```
Inserisci una stringa: Programmazione
Lunghezza: 14
Primo carattere: P
Ultimo carattere: e
Contiene 'a': SI
```

**💡 Hint:**
1. Usa `fgets` per leggere e rimuovi il `'\n'`
2. `strlen(s)` dà la lunghezza; l'ultimo char è `s[strlen(s)-1]`
3. `strchr(s, 'a') != NULL` controlla la presenza

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <string.h>

int main() {
    char s[101];
    int len;

    printf("Inserisci una stringa: ");
    fgets(s, sizeof(s), stdin);
    if (s[strlen(s)-1] == '\n')
        s[strlen(s)-1] = '\0';

    len = strlen(s);
    printf("Lunghezza: %d\n", len);
    printf("Primo carattere: %c\n", s[0]);
    printf("Ultimo carattere: %c\n", s[len-1]);

    if (strchr(s, 'a') != NULL || strchr(s, 'A') != NULL)
        printf("Contiene 'a': SI\n");
    else
        printf("Contiene 'a': NO\n");

    return 0;
}
```

</details>

---

### 🟡 Esercizio 2 — Ordinamento alfabetico di nomi (Intermedio)

**Testo:** Il programma legge N nomi dall'utente (max 20, max 50 caratteri ciascuno), li ordina in ordine alfabetico con il Bubble Sort e li stampa ordinati.

**Esempio input/output:**
```
Quanti nomi? 4
Nome 1: Zara
Nome 2: Anna
Nome 3: Marco
Nome 4: Giulia

Nomi ordinati:
  Anna
  Giulia
  Marco
  Zara
```

**💡 Hint:**
1. Dichiara `char nomi[20][51]` e `char temp[51]`
2. Dopo ogni `fgets`, rimuovi il `'\n'`
3. Confronto: `strcmp(nomi[j], nomi[j+1]) > 0`
4. Scambio: tre `strcpy` con `temp`

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <string.h>

#define MAX_NOMI 20
#define MAX_LEN  51

int main() {
    char nomi[MAX_NOMI][MAX_LEN];
    char temp[MAX_LEN];
    int n, i, j;

    printf("Quanti nomi? ");
    scanf("%d", &n);
    getchar();

    if (n > MAX_NOMI) n = MAX_NOMI;

    for (i = 0; i < n; i++) {
        printf("Nome %d: ", i + 1);
        fgets(nomi[i], MAX_LEN, stdin);
        if (nomi[i][strlen(nomi[i])-1] == '\n')
            nomi[i][strlen(nomi[i])-1] = '\0';
    }

    for (i = 0; i < n - 1; i++) {
        for (j = 0; j < n - 1 - i; j++) {
            if (strcmp(nomi[j], nomi[j+1]) > 0) {
                strcpy(temp,       nomi[j]);
                strcpy(nomi[j],    nomi[j+1]);
                strcpy(nomi[j+1],  temp);
            }
        }
    }

    printf("\nNomi ordinati:\n");
    for (i = 0; i < n; i++)
        printf("  %s\n", nomi[i]);

    return 0;
}
```

</details>

---

### 🔴 Esercizio 3 — Mini rubrica con ricerca (Avanzato)

**Testo:** Il programma gestisce una mini rubrica di massimo 10 contatti (nome max 30 char, telefono max 15 char). Deve:
1. Leggere N contatti dall'utente
2. Ordinarli alfabeticamente per nome (ricorda: scambia anche i telefoni!)
3. Stampare la rubrica ordinata
4. Chiedere un nome da cercare e stampare il risultato (ricerca lineare con `strcmp`)

**Esempio input/output:**
```
Quanti contatti? 3
Nome: Rossi Luca
Tel:  3331234567
Nome: Bianchi Mario
Tel:  3337654321
Nome: Verdi Anna
Tel:  3339876543

Rubrica ordinata:
  Bianchi Mario       3337654321
  Rossi Luca          3331234567
  Verdi Anna          3339876543

Cerca: Rossi Luca
Trovato → Rossi Luca: 3331234567
```

**💡 Hint:**
1. Usa due array paralleli: `char nomi[10][31]` e `char tel[10][16]`
2. Quando scambi due nomi nel Bubble Sort, scambia subito anche i telefoni corrispondenti
3. Per la ricerca, scorri l'array con `strcmp(nomi[i], cerca) == 0`
4. Usa una variabile `trovato = 0` e impostala a `1` quando trovi il contatto

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <string.h>

#define MAX_C   10
#define MAX_N   31
#define MAX_T   16

int main() {
    char nomi[MAX_C][MAX_N];
    char tel[MAX_C][MAX_T];
    char tempN[MAX_N], tempT[MAX_T];
    char cerca[MAX_N];
    int n, i, j, trovato;

    printf("Quanti contatti? ");
    scanf("%d", &n);
    getchar();
    if (n > MAX_C) n = MAX_C;

    for (i = 0; i < n; i++) {
        printf("Nome: ");
        fgets(nomi[i], MAX_N, stdin);
        if (nomi[i][strlen(nomi[i])-1] == '\n') nomi[i][strlen(nomi[i])-1] = '\0';

        printf("Tel:  ");
        fgets(tel[i], MAX_T, stdin);
        if (tel[i][strlen(tel[i])-1] == '\n') tel[i][strlen(tel[i])-1] = '\0';
    }

    for (i = 0; i < n - 1; i++) {
        for (j = 0; j < n - 1 - i; j++) {
            if (strcmp(nomi[j], nomi[j+1]) > 0) {
                strcpy(tempN,    nomi[j]);
                strcpy(nomi[j],  nomi[j+1]);
                strcpy(nomi[j+1], tempN);

                strcpy(tempT,   tel[j]);
                strcpy(tel[j],  tel[j+1]);
                strcpy(tel[j+1], tempT);
            }
        }
    }

    printf("\nRubrica ordinata:\n");
    for (i = 0; i < n; i++)
        printf("  %-20s  %s\n", nomi[i], tel[i]);

    printf("\nCerca: ");
    fgets(cerca, MAX_N, stdin);
    if (cerca[strlen(cerca)-1] == '\n') cerca[strlen(cerca)-1] = '\0';

    trovato = 0;
    for (i = 0; i < n; i++) {
        if (strcmp(nomi[i], cerca) == 0) {
            printf("Trovato → %s: %s\n", nomi[i], tel[i]);
            trovato = 1;
            break;
        }
    }
    if (!trovato)
        printf("Contatto \"%s\" non trovato.\n", cerca);

    return 0;
}
```

</details>

---

## 🎯 Recap finale (5 min)

- **Le stringhe in C sono array di `char` terminati da `'\0'`** — il terminatore è obbligatorio e viene gestito automaticamente da tutte le funzioni di `string.h`.
- **`strcmp` è l'unico modo corretto per confrontare stringhe**: restituisce `0` se uguali, valore negativo se la prima precede la seconda, positivo se la segue — identica logica usata nel Bubble Sort.
- **Ordinare stringhe = Bubble Sort già noto**, con due soli cambiamenti: `strcmp` al posto di `>` per il confronto, e tre `strcpy` al posto dell'assegnazione diretta per lo scambio.
- **`strchr` e `strstr` cercano** rispettivamente un carattere e una sottostringa — restituiscono sempre `NULL` se non trovano nulla, e questo va sempre controllato prima di usare il puntatore.
- ⚠️ **Errore comune da evitare:** usare `s1 = s2` per copiare o `s1 == s2` per confrontare — entrambi operano sugli indirizzi, non sul contenuto. Usare sempre `strcpy` e `strcmp`.
- 📌 **Prossima lezione (G14):** introduzione alle `struct` — come raggruppare dati di tipo diverso (nome, età, stipendio) in un'unica variabile composita, evitando gli array paralleli usati oggi.
