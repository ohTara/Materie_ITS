# GUIDA DIDATTICA - LEZIONE 19
## Puntatori in C

### DURATA TOTALE: 4 ORE

---

## STRUTTURA DELLA LEZIONE

### Parte 1: INTRODUZIONE E CONCETTO (30 minuti)
- Cos'è un puntatore
- Analogia della memoria
- Perché sono importanti

### Parte 2: SINTASSI E OPERATORI (60 minuti)
- Operatori & e *
- Dichiarazione e inizializzazione
- Puntatori e costanti
- Errori comuni

### Parte 3: PUNTATORI E ARRAY (60 minuti)
- Relazione array-puntatori
- Aritmetica dei puntatori
- Notazione equivalente
- Iterazione con puntatori

### Parte 4: PASSAGGIO PER RIFERIMENTO (45 minuti)
- Problema del passaggio per valore
- Soluzione con puntatori
- Funzioni che modificano variabili
- Restituzione multipli valori

### Parte 5: PUNTATORI E STRINGHE (45 minuti)
- Stringhe come puntatori
- Funzioni con stringhe
- Array di stringhe

---

## PARTE 1: INTRODUZIONE E CONCETTO (30 minuti)

### 1.1 Motivazione (5 min)

**Problema con le funzioni normali:**

```c
void incrementa(int x) {
    x++;
    printf("Dentro funzione: x = %d\n", x);
}

int main() {
    int numero = 10;
    incrementa(numero);
    printf("Fuori funzione: numero = %d\n", numero);
    return 0;
}
```

**Output:**
```
Dentro funzione: x = 11
Fuori funzione: numero = 10  ← Non è cambiato!
```

> "La funzione riceve una COPIA del valore, non può modificare l'originale. I puntatori risolvono questo problema!"

---

### 1.2 Cos'è un Puntatore? (10 min)

**Definizione:**
> Un **puntatore** è una variabile che contiene l'**indirizzo di memoria** di un'altra variabile.

**Analogia dell'edificio:**

```
La memoria è come un EDIFICIO con appartamenti:

┌─────────────┐
│  0x1000     │ ← Appartamento 1000
│  [int x=42] │    Contiene il valore 42
├─────────────┤
│  0x1004     │ ← Appartamento 1004
│  [int y=10] │    Contiene il valore 10
├─────────────┤
│  0x1008     │ ← Appartamento 1008
│  [int* p]   │    Contiene l'indirizzo 0x1000
│  =0x1000    │    (punta ad x!)
└─────────────┘

Un puntatore è come un POST-IT che dice:
"Il valore che cerchi è nell'appartamento 1000"
```

**In sintesi:**
- Una variabile **normale** contiene un **valore**
- Un **puntatore** contiene un **indirizzo**

---

### 1.3 Perché Sono Importanti? (10 min)

**I puntatori permettono di:**

1. **Modificare variabili nelle funzioni** (passaggio per riferimento)
   ```c
   void modifica(int* p) {
       *p = 100;  // Cambia l'originale!
   }
   ```

2. **Gestire array in modo efficiente**
   ```c
   void stampaArray(int* arr, int dim) {
       for (int i = 0; i < dim; i++) {
           printf("%d ", arr[i]);
       }
   }
   ```

3. **Manipolare stringhe**
   ```c
   char* str = "Ciao";
   while (*str != '\0') {
       printf("%c", *str);
       str++;
   }
   ```

4. **Creare strutture dati dinamiche** (liste, alberi, grafi)
   - Vedremo in seguito con `malloc` e allocazione dinamica

5. **Evitare copie di grandi struct**
   ```c
   void stampaStudente(Studente* s) {  // Passa solo l'indirizzo!
       printf("%s\n", s->nome);
   }
   ```

---

### 1.4 Visualizzazione Iniziale (5 min)

Scrivi alla lavagna questo schema:

```
VARIABILE vs PUNTATORE

┌──────────────────┐
│ Variabile int x  │
├──────────────────┤
│ Indirizzo: 0x1000│
│ Valore:    42    │
└──────────────────┘

┌──────────────────┐
│ Puntatore int* p │
├──────────────────┤
│ Indirizzo: 0x1008│
│ Valore:    0x1000│ ← Contiene l'indirizzo di x!
└──────────────────┘

p "punta" a x:
  p      → contiene 0x1000
  *p     → vale 42 (il valore di x)
  &x     → vale 0x1000 (l'indirizzo di x)
```

## PARTE 2: SINTASSI E OPERATORI (60 minuti)

### 2.1 Operatore & (address-of) — 10 min

**Significato:** Ottiene l'**indirizzo** di una variabile.

```c
int x = 42;
printf("Valore di x: %d\n", x);         // 42
printf("Indirizzo di x: %p\n", &x);     // 0x7fff... (esempio)
```

**Sintassi:**
```c
&variabile  → restituisce l'indirizzo
```

**Analogia:**
> "`&x` è come dire: 'Qual è l'indirizzo di casa di x?'"

**Visualizzazione:**

```
int x = 42;

x      → valore 42
&x     → indirizzo 0x1000

┌─────────────┐
│ x           │
│ indirizzo:  │ ← &x restituisce questo
│   0x1000    │
│ valore:     │
│   42        │ ← x restituisce questo
└─────────────┘
```

**⚠️ NOTA:** L'indirizzo `%p` viene stampato in esadecimale.

---

### 2.2 Operatore * (dereference) — 15 min

**Significato:** Accede al **valore** puntato da un puntatore.

```c
int x = 42;
int* p = &x;  // p contiene l'indirizzo di x

printf("Valore di p: %p\n", p);        // 0x1000 (indirizzo di x)
printf("Valore puntato: %d\n", *p);    // 42 (valore di x)
```

**Sintassi:**
```c
*puntatore  → restituisce il valore puntato
```

**Analogia:**
> "`*p` è come dire: 'Vai all'indirizzo scritto su p e leggimi il valore che c'è dentro'"

---

**Visualizzazione completa:**

```c
int numero = 42;
int* puntatore = &numero;
```

```
┌─────────────────┐        ┌─────────────────┐
│ numero          │◄───────│ puntatore       │
│ ind:   0x1000   │        │ ind:   0x1008   │
│ valore: 42      │        │ valore: 0x1000  │
└─────────────────┘        └─────────────────┘

numero          → 42
&numero         → 0x1000
puntatore       → 0x1000
*puntatore      → 42  (stesso di numero!)
&puntatore      → 0x1008
```

**Modifica attraverso puntatore:**

```c
*puntatore = 100;  // Modifica il valore di numero!

printf("numero = %d\n", numero);      // 100
printf("*puntatore = %d\n", *puntatore);  // 100
```

Ora:
```
┌─────────────────┐        ┌─────────────────┐
│ numero          │◄───────│ puntatore       │
│ ind:   0x1000   │        │ ind:   0x1008   │
│ valore: 100     │ ← Modificato!
└─────────────────┘        └─────────────────┘
```


### 2.3 Dichiarazione di Puntatori — 10 min

**Sintassi:**
```c
tipo* nomePuntatore;
```

**Esempi:**

```c
int* p1;       // Puntatore a int
float* p2;     // Puntatore a float
char* p3;      // Puntatore a char (stringa)
double* p4;    // Puntatore a double
```

**⚠️ ATTENZIONE — Dichiarazioni multiple:**

```c
// SBAGLIATO (solo p è puntatore, q è int normale):
int* p, q;

// CORRETTO (entrambi puntatori):
int *p, *q;     // Stile 1
int* p;         // Stile 2 (più chiaro)
int* q;
```

**Stile consigliato:**
```c
int* p;  // Asterisco vicino al tipo
int* q;  // Una dichiarazione per riga → più chiaro
```

---

### 2.4 Inizializzazione di Puntatori — 15 min

**Buone pratiche:**

```c
// 1. Inizializzazione a NULL (sicuro)
int* p = NULL;  // Puntatore nullo (non punta a nulla)

if (p == NULL) {
    printf("Puntatore non valido\n");
}

// 2. Inizializzazione con indirizzo
int x = 10;
int* p = &x;    // p punta a x

printf("%d\n", *p);  // 10

// 3. Assegnamento successivo
int y = 20;
int* q;
q = &y;         // OK
printf("%d\n", *q);  // 20
```

---

**⚠️ ERRORI COMUNI — Leggili ad alta voce!**

```c
// ERRORE 1: Puntatore non inizializzato
int* p;
*p = 42;  // ❌ CRASH! p contiene un indirizzo casuale (garbage)

// ERRORE 2: Dereferenziare NULL
int* p = NULL;
*p = 42;  // ❌ CRASH! Segmentation fault

// ERRORE 3: Confondere valore e indirizzo
int x = 10;
int* p = x;  // ❌ ERRORE! p deve contenere un indirizzo, non un valore
// Corretto: int* p = &x;

// ERRORE 4: Assegnare valore invece di indirizzo
int* p;
int x = 10;
p = x;  // ❌ ERRORE! Assegna valore a puntatore
// Corretto: p = &x;
```

**Regola d'oro:**
> "Un puntatore deve sempre contenere un **indirizzo**, mai un valore diretto."

---

### 2.5 Puntatori e Costanti — 10 min

**Tre casi da distinguere:**

**1. Puntatore a costante** (il valore non può essere modificato):
```c
int x = 10, y = 20;
const int* p1 = &x;

// *p1 = 15;  // ❌ ERRORE! Non si può modificare *p1
p1 = &y;      // ✅ OK, il puntatore può cambiare
```

**2. Puntatore costante** (il puntatore non può cambiare):
```c
int x = 10, y = 20;
int* const p2 = &x;

*p2 = 15;     // ✅ OK, si può modificare il valore
// p2 = &y;   // ❌ ERRORE! Il puntatore è fisso
```

**3. Puntatore costante a costante** (nulla può cambiare):
```c
int x = 10, y = 20;
const int* const p3 = &x;

// *p3 = 15;  // ❌ ERRORE!
// p3 = &y;   // ❌ ERRORE!
```

**Mnemonic:**
- `const` prima di `*` → il **valore** è costante
- `const` dopo `*` → il **puntatore** è costante

```
const int* p;       → valore costante
int* const p;       → puntatore costante
const int* const p; → entrambi costanti
```


---

## PARTE 3: PUNTATORI E ARRAY (60 minuti)

### 3.1 Array e Puntatori — Relazione Fondamentale (15 min)

**Fatto importante:**
> In C, il **nome di un array** è un **puntatore costante** al primo elemento.

```c
int arr[] = {10, 20, 30, 40, 50};

// arr è equivalente a &arr[0]
printf("%p\n", arr);        // Indirizzo del primo elemento
printf("%p\n", &arr[0]);    // Stesso indirizzo!
```

**Quindi:**
```c
int* p = arr;  // ✅ OK (senza &)

// È equivalente a:
int* p = &arr[0];
```

---

**Visualizzazione in memoria:**

```
Array: int arr[] = {10, 20, 30, 40, 50};

Indirizzo  Valore  Notazione
─────────────────────────────
0x1000     10      arr[0]  = *arr       = *(arr+0)
0x1004     20      arr[1]  = *(arr+1)
0x1008     30      arr[2]  = *(arr+2)
0x100C     40      arr[3]  = *(arr+3)
0x1010     50      arr[4]  = *(arr+4)
 ↑
arr (punta qui)
```

**Accesso equivalente:**

```c
arr[2]  ==  *(arr + 2)  ==  *(2 + arr)  ==  2[arr]

// Tutti accedono al terzo elemento (30)!
```

> "Il compilatore traduce `arr[i]` in `*(arr + i)` automaticamente."

---

### 3.2 Aritmetica dei Puntatori (20 min)

**Operazioni valide:**
- `p + n` : sposta il puntatore avanti di **n elementi**
- `p - n` : sposta il puntatore indietro di **n elementi**
- `p++` : sposta al **prossimo** elemento
- `p--` : sposta all'elemento **precedente**
- `p1 - p2` : **distanza** tra due puntatori (in elementi)

---

**IMPORTANTE — Il salto dipende dal tipo:**

```c
int arr[] = {10, 20, 30, 40, 50};
int* p = arr;

printf("Indirizzo p:     %p\n", p);
printf("Indirizzo p+1:   %p\n", p+1);
printf("Indirizzo p+2:   %p\n", p+2);
```

**Output:**
```
Indirizzo p:     0x1000
Indirizzo p+1:   0x1004  ← +4 byte (sizeof(int))
Indirizzo p+2:   0x1008  ← +8 byte totali
```

> "`p+1` NON è `indirizzo+1`, ma `indirizzo + sizeof(tipo)`"

---

**Esempio pratico:**

```c
int numeri[] = {10, 20, 30, 40, 50};
int* p = numeri;

printf("%d\n", *p);       // 10 (primo elemento)
printf("%d\n", *(p+1));   // 20 (secondo elemento)
printf("%d\n", *(p+2));   // 30 (terzo elemento)

p++;  // Sposta al prossimo elemento
printf("%d\n", *p);       // 20

p += 2;  // Sposta di 2 posizioni
printf("%d\n", *p);       // 40
```

---

**Differenza tra puntatori:**

```c
int arr[] = {10, 20, 30, 40, 50};
int* p1 = &arr[0];
int* p2 = &arr[4];

int distanza = p2 - p1;
printf("Distanza: %d elementi\n", distanza);  // 4
```

---

### 3.3 Iterazione con Puntatori (15 min)

**Tre modi per iterare su un array:**

**Metodo 1: Indice classico**
```c
int arr[] = {10, 20, 30, 40, 50};
for (int i = 0; i < 5; i++) {
    printf("%d ", arr[i]);
}
```

**Metodo 2: Aritmetica dei puntatori**
```c
int arr[] = {10, 20, 30, 40, 50};
for (int i = 0; i < 5; i++) {
    printf("%d ", *(arr + i));
}
```

**Metodo 3: Incremento del puntatore**
```c
int arr[] = {10, 20, 30, 40, 50};
int* p = arr;
int* fine = arr + 5;

while (p < fine) {
    printf("%d ", *p);
    p++;
}
```

**Metodo 4: Stile compatto**
```c
int arr[] = {10, 20, 30, 40, 50};
int* p = arr;

for (int i = 0; i < 5; i++) {
    printf("%d ", *p++);  // Stampa e poi incrementa
}
```

---

### 3.4 Array vs Puntatore — Differenze Importanti (10 min)

**Somiglianze:**
```c
int arr[5];
int* p = arr;

arr[2] == p[2] == *(arr+2) == *(p+2)  // ✅ Tutti uguali
```

**Differenze:**

| | Array | Puntatore |
|---|---|---|
| **Modifica** | ❌ `arr++` errore | ✅ `p++` ok |
| **sizeof** | Dimensione totale | Dimensione puntatore |
| **Tipo** | Puntatore costante | Variabile |

```c
int arr[5] = {1, 2, 3, 4, 5};
int* p = arr;

// arr è COSTANTE, p è VARIABILE
p++;       // ✅ OK: p ora punta al secondo elemento
// arr++;  // ❌ ERRORE! Non si può modificare arr

// sizeof comportamento diverso
printf("%lu\n", sizeof(arr));  // 20 (5 * 4 byte)
printf("%lu\n", sizeof(p));    // 8 (dimensione puntatore su 64-bit)
```

---

## PARTE 4: PASSAGGIO PER RIFERIMENTO (45 minuti)

### 4.1 Problema del Passaggio per Valore (10 min)

**Situazione:**

```c
void incrementa(int x) {
    x++;
    printf("Dentro funzione: x = %d\n", x);
}

int main() {
    int numero = 10;
    incrementa(numero);
    printf("Fuori funzione: numero = %d\n", numero);
    return 0;
}
```

**Output:**
```
Dentro funzione: x = 11
Fuori funzione: numero = 10  ← NON è cambiato!
```

**Perché?**
> La funzione riceve una **copia** del valore. Modificare `x` dentro la funzione non modifica `numero` nel `main()`.

**Visualizzazione:**

```
main():                  incrementa():
┌──────────┐            ┌──────────┐
│ numero   │            │ x        │
│ = 10     │ ─copia─→   │ = 10     │
└──────────┘            └──────────┘
                             ↓ x++
                        ┌──────────┐
                        │ x        │
                        │ = 11     │
                        └──────────┘
                        
numero rimane 10 (la copia è sparita)
```

---

### 4.2 Soluzione: Passaggio per Riferimento (15 min)

**Strategia:** Passa l'**indirizzo** invece del valore.

```c
void incrementa(int* x) {
    (*x)++;  // Modifica il valore puntato
    printf("Dentro funzione: *x = %d\n", *x);
}

int main() {
    int numero = 10;
    incrementa(&numero);  // Passa l'indirizzo
    printf("Fuori funzione: numero = %d\n", numero);
    return 0;
}
```

**Output:**
```
Dentro funzione: *x = 11
Fuori funzione: numero = 11  ← È cambiato! ✓
```

**Visualizzazione:**

```
main():                  incrementa():
┌──────────┐            ┌──────────┐
│ numero   │◄───────────│ x        │
│ = 10     │   punta    │ = &numero│
│ @0x1000  │            └──────────┘
└──────────┘                  ↓ (*x)++
┌──────────┐
│ numero   │ ← Modificato direttamente!
│ = 11     │
│ @0x1000  │
└──────────┘
```

**Sintassi:**
```c
// Dichiarazione
void funzione(int* parametro);

// Chiamata
funzione(&variabile);

// Uso interno
*parametro = nuovoValore;
```

---

### 4.3 Esempio: Swap di Due Variabili (10 min)

**Implementazione SBAGLIATA (per valore):**

```c
void swapSbagliato(int a, int b) {
    int temp = a;
    a = b;
    b = temp;
    // Scambia solo le copie locali!
}
```

**Implementazione CORRETTA (per riferimento):**

```c
void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main() {
    int x = 10, y = 20;
    printf("Prima: x=%d, y=%d\n", x, y);
    
    swap(&x, &y);  // Passa gli indirizzi
    
    printf("Dopo: x=%d, y=%d\n", x, y);
    return 0;
}
```

**Output:**
```
Prima: x=10, y=20
Dopo: x=20, y=10  ← Scambiati! ✓
```

---

### 4.4 Restituzione di Multipli Valori (10 min)

**Problema:** In C una funzione può tornare **UN SOLO** valore.

**Soluzione:** Usa puntatori per "tornare" più valori.

**Esempio: Divisione con quoziente e resto**

```c
void divisioneCompleta(int dividendo, int divisore,
                        int* quoziente, int* resto) {
    *quoziente = dividendo / divisore;
    *resto = dividendo % divisore;
}

int main() {
    int q, r;
    divisioneCompleta(17, 5, &q, &r);
    
    printf("17 / 5 = %d con resto %d\n", q, r);
    // Output: 17 / 5 = 3 con resto 2
    
    return 0;
}
```

**Come funziona:**

```
main():
┌────┐  ┌────┐
│ q  │  │ r  │
└────┘  └────┘
  ↑       ↑
  │       │
divisioneCompleta(..., &q, &r)
  │       │
  │       └─ scrive il resto in r
  └───────── scrive il quoziente in q
```


---

## PARTE 5: PUNTATORI E STRINGHE (45 minuti)

### 5.1 Stringhe come Puntatori (10 min)

**Fatto:**
> In C, le stringhe sono **array di char**, quindi **puntatori a char**.

**Due modi di dichiarare stringhe:**

```c
// Modo 1: Array di caratteri (modificabile)
char str1[] = "Ciao";
str1[0] = 'c';  // ✅ OK: posso modificare

// Modo 2: Puntatore a stringa letterale (NON modificabile)
char* str2 = "Ciao";
// str2[0] = 'c';  // ❌ ERRORE: stringa in memoria read-only
```

**Differenza:**

| | `char str[]` | `char* str` |
|---|---|---|
| **Memoria** | Stack | Read-only (costante) |
| **Modificabile** | ✅ Sì | ❌ No |
| **Uso** | Buffers, manipolazione | Stringhe costanti |

---

### 5.2 Iterare su Stringhe con Puntatori (15 min)

**Metodo 1: Indice**
```c
char stringa[] = "Hello";
for (int i = 0; i < strlen(stringa); i++) {
    printf("%c ", stringa[i]);
}
```

**Metodo 2: Puntatore**
```c
char stringa[] = "Hello";
char* p = stringa;

while (*p != '\0') {  // Finché non raggiungi il terminatore
    printf("%c ", *p);
    p++;
}
```

**Output entrambi:**
```
H e l l o
```

---

**Esempio: Calcola lunghezza stringa**

```c
int lunghezza(char* str) {
    int len = 0;
    while (*str != '\0') {
        len++;
        str++;
    }
    return len;
}

int main() {
    char testo[] = "Programmazione";
    printf("Lunghezza: %d\n", lunghezza(testo));  // 14
    return 0;
}
```

---

### 5.3 Funzioni con Stringhe (10 min)

**Copia stringa:**

```c
void copiaStringa(char* dest, char* src) {
    while (*src != '\0') {
        *dest = *src;
        dest++;
        src++;
    }
    *dest = '\0';  // Aggiungi terminatore
}

// Versione compatta
void copiaStringa2(char* dest, char* src) {
    while ((*dest++ = *src++) != '\0');
}
```

**Confronta stringhe:**

```c
int confrontaStringhe(char* str1, char* str2) {
    while (*str1 != '\0' && *str2 != '\0') {
        if (*str1 != *str2) {
            return *str1 - *str2;
        }
        str1++;
        str2++;
    }
    return *str1 - *str2;
}
```

---

### 5.4 Array di Stringhe (10 min)

**Un array di stringhe è un array di puntatori:**

```c
char* giorni[] = {
    "Lunedì",
    "Martedì",
    "Mercoledì",
    "Giovedì",
    "Venerdì",
    "Sabato",
    "Domenica"
};

for (int i = 0; i < 7; i++) {
    printf("%s\n", giorni[i]);
}
```

**Visualizzazione:**

```
giorni è un array di puntatori:

┌──────┐
│ ptr  │──→ "Lunedì"
├──────┤
│ ptr  │──→ "Martedì"
├──────┤
│ ptr  │──→ "Mercoledì"
├──────┤
...

giorni[0] punta a "Lunedì"
giorni[1] punta a "Martedì"
```

---

## RIEPILOGO E CHIUSURA (10 minuti)

### Concetti Chiave

**✓ Puntatori:**
- Contengono **indirizzi** di memoria
- `&` → ottiene l'indirizzo
- `*` → dereferenzia (accede al valore)

**✓ Array e Puntatori:**
- Il nome dell'array è un puntatore al primo elemento
- `arr[i]` è equivalente a `*(arr + i)`
- Aritmetica: `p+n` salta `n * sizeof(tipo)` byte

**✓ Passaggio per Riferimento:**
- Passa `&variabile` alla funzione
- Dentro la funzione: `*puntatore = valore`
- Permette di modificare variabili e tornare multipli valori

**✓ Stringhe:**
- Sono `char*` (puntatori a caratteri)
- Iterazione: `while (*p != '\0')`
- Array di stringhe: `char* arr[]`

---

### Errori Comuni da Evitare

```c
// ❌ Puntatore non inizializzato
int* p;
*p = 42;  // CRASH

// ❌ Dereferenziare NULL
int* p = NULL;
*p = 42;  // CRASH

// ❌ Confondere valore e indirizzo
int x = 10;
int* p = x;  // ERRORE
// Corretto: int* p = &x;

// ❌ Dimenticare le parentesi
int* p;
*p++;    // Incrementa p, poi dereferenzia (sbagliato)
(*p)++;  // Incrementa il valore puntato (corretto)
```

---

### Domande di Verifica

1. **"Cosa restituisce l'operatore `&`?"**
2. **"Cosa fa l'operatore `*`?"**
3. **"Perché `arr[2]` è equivalente a `*(arr+2)`?"**
4. **"Come si passa una variabile per riferimento?"**
5. **"Qual è la differenza tra `char str[]` e `char* str`?"**

---

<details>
<summary><b>📝 RISPOSTE PER IL DOCENTE</b></summary>

### 1. Operatore &

**Risposta:** Restituisce l'**indirizzo di memoria** di una variabile.

```c
int x = 42;
printf("%p\n", &x);  // Stampa l'indirizzo (es. 0x7fff...)
```

L'operatore `&` (address-of) è come chiedere: "Dove si trova questa variabile in memoria?"

---

### 2. Operatore *

**Risposta:** **Dereferenzia** un puntatore, cioè accede al valore nella posizione di memoria puntata.

```c
int x = 42;
int* p = &x;
printf("%d\n", *p);  // 42 (valore di x)
```

`*p` significa: "Vai all'indirizzo contenuto in `p` e leggimi il valore che c'è."

**Inoltre, `*` si usa anche per dichiarare puntatori:**
```c
int* p;  // Dichiarazione: p è un puntatore a int
```

---

### 3. Equivalenza arr[2] e *(arr+2)

**Risposta:** Il compilatore C traduce `arr[i]` in `*(arr + i)` automaticamente.

**Spiegazione:**

```c
int arr[] = {10, 20, 30, 40, 50};

arr[2]       // Notazione con indice
*(arr + 2)   // Notazione con puntatore

Entrambi accedono al terzo elemento (30).
```

**Perché?**
1. `arr` è un puntatore al primo elemento
2. `arr + 2` sposta il puntatore di 2 posizioni
3. `*(arr + 2)` dereferenzia → legge il valore

**In generale:**
```
arr[i]  ≡  *(arr + i)  ≡  *(i + arr)  ≡  i[arr]
```

Tutte queste notazioni sono **equivalenti** (anche se `i[arr]` è bizzarro!).

---

### 4. Passaggio per riferimento

**Risposta:** Si passa l'**indirizzo** della variabile usando `&`, e la funzione riceve un **puntatore**.

**Passaggi:**

1. **Dichiarazione:** funzione riceve puntatore
   ```c
   void modifica(int* p);
   ```

2. **Chiamata:** passa l'indirizzo con `&`
   ```c
   int x = 10;
   modifica(&x);
   ```

3. **Uso interno:** dereferenzia con `*`
   ```c
   void modifica(int* p) {
       *p = 100;  // Modifica x nel main
   }
   ```

**Perché funziona?**
La funzione riceve l'indirizzo di `x`, quindi può modificare direttamente il valore originale (non una copia).

---

### 5. Differenza char str[] vs char* str

**Risposta:**

**`char str[] = "Ciao"`** (array):
- Allocato nello **stack**
- **Modificabile**
- Copia la stringa in memoria locale
```c
char str1[] = "Ciao";
str1[0] = 'c';  // ✅ OK
```

**`char* str = "Ciao"`** (puntatore a letterale):
- Punta a memoria **read-only** (segmento costanti)
- **NON modificabile**
- Più efficiente (non fa copia)
```c
char* str2 = "Ciao";
str2[0] = 'c';  // ❌ CRASH: segmentation fault
```

**Quando usare quale:**
- `char str[]` → quando devi **modificare** la stringa
- `char* str` → stringhe **costanti** (es. menu, messaggi)

**Best practice per stringhe costanti:**
```c
const char* str = "Ciao";  // Rendi esplicito che è costante
```

</details>

---

## NOTE PER IL DOCENTE

### ⚠️ Punti critici da monitorare:

1. **Confusione tra `&` e `*`** — studenti invertono gli operatori
2. **Dereferenziare puntatori non inizializzati** — causa crash
3. **Dimenticare le parentesi in `(*p)++`** — precedenza operatori
4. **Modificare stringhe letterali** — comportamento indefinito
5. **Confondere array e puntatori** — `sizeof` comportamento diverso

### 💡 Suggerimenti didattici:

- Usa **diagrammi di memoria** alla lavagna per ogni esempio
- Fai **disegnare** agli studenti dove puntano i puntatori
- **Simula passo-passo** il passaggio per riferimento con frecce
- Usa **analogie concrete** (POST-IT, edificio con appartamenti)
- **Esegui codice live** mostrando gli indirizzi con `printf("%p")`

### 📊 Valutazione comprensione:

- ✅ Lo studente distingue `&` da `*`
- ✅ Lo studente inizializza correttamente i puntatori
- ✅ Lo studente itera su array con puntatori
- ✅ Lo studente passa variabili per riferimento
- ✅ Lo studente manipola stringhe con puntatori

### 🎯 Obiettivi minimi per questa lezione:

Lo studente è pronto se:
- Dichiara e inizializza puntatori senza errori
- Usa `&` per ottenere indirizzi e `*` per dereferenziare
- Passa variabili per riferimento a funzioni
- Itera su array usando puntatori
- Evita gli errori comuni (NULL, non inizializzato)

---

**Buona lezione! 🚀**
