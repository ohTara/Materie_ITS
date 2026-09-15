# Lezione: Pila e Coda (Stack e Queue)
**Durata totale:** 4 ore
**Teoria:** 1.5 ore | **Esercizi:** 2.5 ore
**Data:** _______________
**Ambiente:** CLion (JetBrains)

> ⚠️ NOTA DIDATTICA: Tutte le implementazioni usano **array e variabili separate** senza `struct`.

---

# PARTE 1 — TEORIA (1.5 ore)

## 1.1 Introduzione e Motivazione

Immagina di essere in fila alla cassa del supermercato: il primo ad arrivare è il primo a essere servito. Oppure pensa a una pila di piatti: li metti uno sopra l'altro e prendi sempre quello in cima.

Questi due scenari descrivono due strutture dati fondamentali in informatica:

- **Pila (Stack):** LIFO — *Last In, First Out* (l'ultimo inserito è il primo a uscire)
- **Coda (Queue):** FIFO — *First In, First Out* (il primo inserito è il primo a uscire)

**Dove si usano nella realtà e nei programmi?**

- **Stack:** la cronologia "Indietro" del browser, il meccanismo di chiamata delle funzioni, il controllo delle parentesi bilanciate in un compilatore, l'operazione "Annulla" (Ctrl+Z).
- **Queue:** la coda di stampa, i messaggi in attesa di elaborazione, le richieste a un server web, le animazioni in un videogioco.

---

## 1.2 Spiegazione dell'Argomento

### La Pila (Stack)

Una pila è una struttura in cui gli elementi vengono inseriti e rimossi sempre dalla stessa estremità, chiamata **cima** (*top*).

**Operazioni principali:**
- `push(x)` — inserisce x in cima
- `pop()` — rimuove e restituisce l'elemento in cima
- `peek()` — legge la cima senza rimuoverla
- `isEmpty()` — true se la pila è vuota
- `isFull()` — true se la pila è piena

**Visualizzazione passo-passo:**

```
Inizio        push(10)      push(20)      push(30)      pop()
              +------+      +------+      +------+      +------+
              |  10  |<top  |  20  |<top  |  30  |<top  |  20  |<top
              +------+      +------+      +------+      +------+
                            |  10  |      |  20  |      |  10  |
                            +------+      +------+      +------+
                                          |  10  |
                                          +------+
top = -1      top = 0       top = 1       top = 2       top = 1
```

**Implementazione con array:**

Usiamo un array per memorizzare gli elementi e una variabile intera `top` come indice dell'elemento in cima. Convenzione: `top = -1` significa pila vuota.

```
Array:   [ 10 | 20 | 30 | -- | -- ]
indici:     0    1    2    3    4
                      ^
                   top = 2
```

- `push(x)`: incrementa `top`, poi assegna `pila[top] = x`
- `pop()`: salva `pila[top]`, poi decrementa `top`

---

### La Coda (Queue)

Una coda è una struttura in cui i nuovi elementi entrano in **fondo** (*tail*) ed escono dalla **testa** (*head*).

**Operazioni principali:**
- `enqueue(x)` — inserisce x in fondo
- `dequeue()` — rimuove e restituisce l'elemento in testa
- `isEmpty()` — true se la coda è vuota
- `isFull()` — true se la coda è piena

**Visualizzazione passo-passo:**

```
Inizio       enqueue(10)   enqueue(20)   enqueue(30)   dequeue()
             +------+      +------+---+  +------+---+--+  +------+---+
             |  10  |      |  10  |20 |  |  10  |20 |30|  |  20  |30 |
             +------+      +------+---+  +------+---+--+  +------+---+
             ^      ^      ^         ^   ^            ^        ^      ^
            h=0   t=0+1   h=0      t=1  h=0         t=2      h=1    t=2
```

**Implementazione con array:**

Usiamo un array e tre variabili: `head` (indice da cui si estrae), `tail` (prossimo slot libero), `size` (numero elementi presenti).

```
Array:   [ 10 | 20 | 30 | -- | -- ]
indici:     0    1    2    3    4
            ^              ^
         head=0          tail=3    size=3
```

Dopo `dequeue()`:
```
Array:   [ -- | 20 | 30 | -- | -- ]
                ^         ^
             head=1     tail=3    size=2
```

---

### Il Problema della Coda Lineare

La coda lineare ha un limite importante: dopo molte operazioni di `enqueue`/`dequeue`, `tail` raggiunge la fine dell'array anche se ci sono slot liberi all'inizio (quelli già "consumati" dai `dequeue`). Lo spazio non viene mai recuperato.

```
Dopo 3 enqueue + 2 dequeue:

Array:   [ -- | -- | 30 | -- | -- ]   (MAX = 5)
                     ^         ^
                  head=2     tail=3    size=1

Posizioni 0 e 1 sono libere ma inaccessibili!
Se facessi altri 2 enqueue, tail arriverebbe a 5 → fuori dall'array.
```

---

### La Coda Circolare (Circular Buffer)

La soluzione è trattare l'array come se fosse **un cerchio**: quando `tail` raggiunge la fine, riparte dall'indice 0. Questo si ottiene con l'operatore **modulo** (`%`).

**Regola chiave:**
```
tail = (tail + 1) % MAX
head = (head + 1) % MAX
```

**Visualizzazione — array di 5 slot come cerchio:**

```
        indice 0
           |
    4 ---- 0
   /         \
  3           1
   \         /
    2 ---- 2
           |
        indice 2

Stato: head=3, tail=1, size=3  →  elementi in posizioni 3, 4, 0
Array:  [ 70 | -- | -- | 30 | 50 ]
              ^              ^
            tail=1         head=3
```

**Confronto passo-passo con MAX=5:**

```
Operazione     head  tail  size  Array (indici 0..4)
-----------    ----  ----  ----  -------------------
enqueue(10)      0     1     1   [10| - | - | - | - ]
enqueue(20)      0     2     2   [10|20 | - | - | - ]
enqueue(30)      0     3     3   [10|20 |30 | - | - ]
dequeue()→10     1     3     2   [ - |20 |30 | - | - ]
dequeue()→20     2     3     1   [ - | - |30 | - | - ]
enqueue(40)      2     4     2   [ - | - |30 |40 | - ]
enqueue(50)      2     0     3   [ - | - |30 |40 |50 ]
  (tail torna a 0 con % 5!)
enqueue(60)      2     1     4   [60 | - |30 |40 |50 ]
  (slot 0 riciclato!)
```

**Condizioni di pieno e vuoto:**
- Vuota: `size == 0`
- Piena: `size == MAX`

---

## 1.3 Esempi di Codice Commentati

### Esempio 1 — Pila (Stack) con array

```c
#include <stdio.h>

#define MAX 5

int pila[MAX];
int top = -1;  // -1 = pila vuota

int isEmpty() { return top == -1; }
int isFull()  { return top == MAX - 1; }

void push(int valore) {
    if (isFull()) {
        printf("Errore: pila piena!\n");
        return;
    }
    top++;
    pila[top] = valore;
}

int pop() {
    if (isEmpty()) {
        printf("Errore: pila vuota!\n");
        return -1;
    }
    int valore = pila[top];
    top--;
    return valore;
}

int peek() {
    if (isEmpty()) {
        printf("Errore: pila vuota!\n");
        return -1;
    }
    return pila[top];
}

int main() {
    push(10);
    push(20);
    push(30);

    printf("Cima: %d\n", peek());  // 30
    printf("Pop: %d\n", pop());    // 30
    printf("Pop: %d\n", pop());    // 20
    printf("Cima: %d\n", peek());  // 10

    return 0;
}
```

**Output atteso:**
```
Cima: 30
Pop: 30
Pop: 20
Cima: 10
```

---

### Esempio 2 — Coda (Queue) con array

```c
#include <stdio.h>

#define MAX 5

int coda[MAX];
int head = 0;
int tail = 0;
int size = 0;

int isEmpty() { return size == 0; }
int isFull()  { return size == MAX; }

void enqueue(int valore) {
    if (isFull()) {
        printf("Errore: coda piena!\n");
        return;
    }
    coda[tail] = valore;
    tail++;
    size++;
}

int dequeue() {
    if (isEmpty()) {
        printf("Errore: coda vuota!\n");
        return -1;
    }
    int valore = coda[head];
    head++;
    size--;
    return valore;
}

int main() {
    enqueue(10);
    enqueue(20);
    enqueue(30);

    printf("Dequeue: %d\n", dequeue());  // 10 — FIFO
    printf("Dequeue: %d\n", dequeue());  // 20
    enqueue(40);
    printf("Dequeue: %d\n", dequeue());  // 30
    printf("Dequeue: %d\n", dequeue());  // 40

    return 0;
}
```

**Output atteso:**
```
Dequeue: 10
Dequeue: 20
Dequeue: 30
Dequeue: 40
```

---

### Esempio 3 — Stampare il contenuto della pila

```c
#include <stdio.h>

#define MAX 5

int pila[MAX];
int top = -1;

void push(int v) {
    if (top < MAX - 1) pila[++top] = v;
}

void stampaPila() {
    if (top == -1) {
        printf("Pila vuota.\n");
        return;
    }
    printf("Pila (dalla cima alla base):\n");
    for (int i = top; i >= 0; i--) {
        printf("  [%d]\n", pila[i]);
    }
}

int main() {
    push(5);
    push(15);
    push(25);
    stampaPila();
    return 0;
}
```

**Output atteso:**
```
Pila (dalla cima alla base):
  [25]
  [15]
  [5]
```

---

### Esempio 4 — Coda Circolare con array

```c
#include <stdio.h>

#define MAX 5

int coda[MAX];
int head = 0;
int tail = 0;
int size = 0;

int isEmpty() { return size == 0; }
int isFull()  { return size == MAX; }

void enqueue(int valore) {
    if (isFull()) { printf("Errore: coda piena!\n"); return; }
    coda[tail] = valore;
    tail = (tail + 1) % MAX;  // avanza circolarmente
    size++;
}

int dequeue() {
    if (isEmpty()) { printf("Errore: coda vuota!\n"); return -1; }
    int valore = coda[head];
    head = (head + 1) % MAX;  // avanza circolarmente
    size--;
    return valore;
}

void stampaCoda() {
    printf("Coda (%d elementi): ", size);
    for (int i = 0; i < size; i++)
        printf("%d ", coda[(head + i) % MAX]);
    printf("\n");
}

int main() {
    enqueue(10); enqueue(20); enqueue(30);
    stampaCoda();
    dequeue(); dequeue();
    stampaCoda();
    enqueue(40); enqueue(50); enqueue(60);
    stampaCoda();
    printf("Dequeue: %d\n", dequeue());
    stampaCoda();
    return 0;
}
```

**Output atteso:**
```
Coda (3 elementi): 10 20 30
Coda (1 elementi): 30
Coda (4 elementi): 30 40 50 60
Dequeue: 30
Coda (3 elementi): 40 50 60
```

> 💡 **Il trucco del modulo:** `(head + i) % MAX` permette di visitare gli elementi nell'ordine corretto anche quando "scavalcano" la fine dell'array e ripartono da 0.

---

## 1.4 Riepilogo Visivo

```
╔══════════════════════════════════════════════════════╗
║              PILA (STACK) — LIFO                     ║
╠══════════════════╦═══════════════════════════════════╣
║ Operazione       ║ Descrizione                       ║
╠══════════════════╬═══════════════════════════════════╣
║ push(x)          ║ Inserisce x in CIMA               ║
║ pop()            ║ Rimuove e restituisce la CIMA      ║
║ peek()           ║ Legge la CIMA (senza rimuovere)   ║
║ isEmpty()        ║ top == -1                         ║
║ isFull()         ║ top == MAX-1                      ║
╚══════════════════╩═══════════════════════════════════╝
  Accesso consentito: solo dalla CIMA

╔════════════════════════╦════════════════════════════════╗
║   CODA LINEARE         ║   CODA CIRCOLARE               ║
╠════════════════════════╬════════════════════════════════╣
║ tail++                 ║ tail = (tail+1) % MAX          ║
║ head++                 ║ head = (head+1) % MAX          ║
║ Spazio non riciclato   ║ Spazio riciclato automaticam.  ║
║ Semplice da capire     ║ Più efficiente in memoria      ║
╚════════════════════════╩════════════════════════════════╝
  Entrambe: isEmpty → size==0 | isFull → size==MAX

╔═══════════════╦═══════════╦═══════════════════════════╗
║ Caratteristica║   STACK   ║    QUEUE (circolare)       ║
╠═══════════════╬═══════════╬═══════════════════════════╣
║ Ordine        ║   LIFO    ║         FIFO              ║
║ Inserimento   ║   cima    ║         fondo             ║
║ Rimozione     ║   cima    ║         testa             ║
║ Var. chiave   ║   top     ║   head, tail, size        ║
║ Avanzamento   ║   +1/-1   ║   (indice+1) % MAX        ║
╚═══════════════╩═══════════╩═══════════════════════════╝
```

---

## 1.5 Domande di Verifica Orale

**D1:** Cosa significa LIFO e FIFO? Fai un esempio concreto per ciascuno.

<details>
<summary><b>💡 RISPOSTA</b></summary>

LIFO = Last In First Out — l'ultimo elemento inserito è il primo ad uscire (es. pila di piatti, cronologia del browser). FIFO = First In First Out — il primo elemento inserito è il primo ad uscire (es. fila alla cassa, coda di stampa).

</details>

---

**D2:** In una pila implementata con array, cosa significa `top == -1`?

<details>
<summary><b>💡 RISPOSTA</b></summary>

La pila è vuota: non contiene alcun elemento.

</details>

---

**D3:** Qual è la differenza tra `pop()` e `peek()`?

<details>
<summary><b>💡 RISPOSTA</b></summary>

`pop()` rimuove e restituisce l'elemento in cima (la pila cambia). `peek()` restituisce l'elemento in cima senza rimuoverlo (la pila rimane invariata).

</details>

---

**D4:** In una coda, dove entrano i nuovi elementi e da dove escono?

<details>
<summary><b>💡 RISPOSTA</b></summary>

I nuovi elementi entrano in fondo (tail). Gli elementi escono dalla testa (head).

</details>

---

**D5:** Eseguo: `push(1)`, `push(2)`, `push(3)`, `pop()`, `pop()`. Qual è la cima?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Dopo i push la pila è [1, 2, 3] con 3 in cima. Dopo due `pop()` vengono rimossi 3 e poi 2. La cima è ora 1.

</details>

---

**D6:** Eseguo su una coda: `enqueue(1)`, `enqueue(2)`, `enqueue(3)`, `dequeue()`. Qual è il prossimo da estrarre?

<details>
<summary><b>💡 RISPOSTA</b></summary>

La coda è [1, 2, 3] con 1 in testa. Dopo `dequeue()` viene rimosso 1. Il prossimo da estrarre è 2.

</details>

---

**D7:** Cosa succede se chiamo `pop()` su una pila vuota nel codice degli esempi?

<details>
<summary><b>💡 RISPOSTA</b></summary>

La funzione `isEmpty()` restituisce vero, viene stampato "Errore: pila vuota!" e la funzione restituisce -1 come valore sentinella.

</details>

---

**D8:** Qual è il limite della coda lineare che la coda circolare risolve?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Nella coda lineare, le posizioni prima di `head` non vengono mai riutilizzate: dopo molti `enqueue`/`dequeue`, `tail` raggiunge la fine dell'array anche se ci sono slot liberi all'inizio. La coda circolare usa `(tail + 1) % MAX` per far "girare" l'indice e riciclare quegli spazi.

</details>

---

**D9:** In una coda circolare con MAX=4, se `tail` vale 3 e faccio un `enqueue`, dove si trova il prossimo `tail`?

<details>
<summary><b>💡 RISPOSTA</b></summary>

`tail = (3 + 1) % 4 = 0`. L'indice riparte da capo, sfruttando lo spazio liberato dai precedenti `dequeue`.

</details>

---

# PARTE 2 — ESERCIZI (2.5 ore)

---

## 🟢 Livello Base

### Esercizio 1 — Inverti una sequenza con la Pila (15–20 min)

**Testo:**
Leggi 5 interi inseriti dall'utente e stampali in ordine inverso usando una pila. Inserisci gli elementi nella pila uno per uno con `push`, poi estraili con `pop` e stampali.

**Esempio input/output:**
```
Inserisci 5 numeri: 1 2 3 4 5
Ordine inverso: 5 4 3 2 1
```

**💡 Hint:**
1. Dichiara `int pila[5]` e `int top = -1`.
2. Primo ciclo `for`: leggi 5 numeri con `scanf` e chiama `push` per ciascuno.
3. Secondo ciclo: chiama `pop` finché la pila non è vuota e stampa ogni valore.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

#define MAX 5

int pila[MAX];
int top = -1;

void push(int v) {
    if (top < MAX - 1) pila[++top] = v;
}

int pop() {
    if (top == -1) return -1;
    return pila[top--];
}

int isEmpty() { return top == -1; }

int main() {
    printf("Inserisci 5 numeri: ");
    for (int i = 0; i < MAX; i++) {
        int n;
        scanf("%d", &n);
        push(n);
    }

    printf("Ordine inverso:");
    while (!isEmpty()) {
        printf(" %d", pop());
    }
    printf("\n");

    return 0;
}
```

</details>

---

### Esercizio 2 — Gestione di una coda clienti (15–20 min)

**Testo:**
Simula una coda di 4 clienti al banco. Aggiungi i clienti numerati da 1 a 4 alla coda, poi servili uno alla volta stampando `"Cliente N servito."` a ogni estrazione.

**Esempio output:**
```
Cliente 1 servito.
Cliente 2 servito.
Cliente 3 servito.
Cliente 4 servito.
```

**💡 Hint:**
1. Dichiara `int coda[10]`, `head = 0`, `tail = 0`, `size = 0`.
2. Ciclo `for` da 1 a 4: chiama `enqueue(i)`.
3. Ciclo `while (!isEmpty())`: chiama `dequeue()` e stampa il risultato.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

#define MAX 10

int coda[MAX];
int head = 0, tail = 0, size = 0;

void enqueue(int v) {
    if (size < MAX) { coda[tail++] = v; size++; }
}

int dequeue() {
    if (size == 0) return -1;
    size--;
    return coda[head++];
}

int isEmpty() { return size == 0; }

int main() {
    for (int i = 1; i <= 4; i++) enqueue(i);

    while (!isEmpty()) {
        printf("Cliente %d servito.\n", dequeue());
    }
    return 0;
}
```

</details>

---

## 🟡 Livello Intermedio

### Esercizio 3 — Controlla parentesi bilanciate (20–30 min)

**Testo:**
Leggi una stringa (max 50 caratteri) e verifica se le parentesi tonde `(` e `)` sono bilanciate usando una pila di caratteri.

Esempi:
- `(a+(b*c))` → **Bilanciata: SI**
- `((x+y)` → **Bilanciata: NO**
- `)x+y(` → **Bilanciata: NO**

**Esempio input/output:**
```
Inserisci stringa: (a+(b*c))
Parentesi bilanciate: SI
```

**💡 Hint:**
1. Scorri la stringa con un ciclo `for` e `strlen`.
2. Se trovi `(`, fai `push('(')`.
3. Se trovi `)`: se la pila è vuota → NO; altrimenti `pop()`.
4. Alla fine: se la pila è vuota → SI; altrimenti → NO.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <string.h>

#define MAX 50

char pila[MAX];
int top = -1;

void push(char c) { if (top < MAX-1) pila[++top] = c; }
char pop()        { return (top == -1) ? '\0' : pila[top--]; }
int isEmpty()     { return top == -1; }

int main() {
    char s[MAX + 1];
    printf("Inserisci stringa: ");
    scanf("%s", s);

    int ok = 1;
    int len = strlen(s);

    for (int i = 0; i < len && ok; i++) {
        if (s[i] == '(') {
            push('(');
        } else if (s[i] == ')') {
            if (isEmpty()) ok = 0;
            else pop();
        }
    }

    if (!isEmpty()) ok = 0;

    printf("Parentesi bilanciate: %s\n", ok ? "SI" : "NO");
    return 0;
}
```

</details>

---

### Esercizio 4 — Due code con priorità (25–30 min)

**Testo:**
Simula uno sportello con due code: **urgenti** e **normali**. Il programma legge N persone (max 6), ciascuna con numero e priorità (1=urgente, 0=normale). Prima vengono servite tutte le urgenti (nell'ordine di arrivo), poi le normali.

**Esempio input:**
```
Quante persone? 4
Persona 1, priorita (1=urgente, 0=normale): 0
Persona 2, priorita (1=urgente, 0=normale): 1
Persona 3, priorita (1=urgente, 0=normale): 0
Persona 4, priorita (1=urgente, 0=normale): 1
```

**Esempio output:**
```
Ordine di servizio:
Persona 2 (urgente)
Persona 4 (urgente)
Persona 1 (normale)
Persona 3 (normale)
```

**💡 Hint:**
1. Usa due array separati `coda_urgenti[]` e `coda_normali[]` con indici `tu` e `tn`.
2. Leggi le N persone e smistale nell'array giusto.
3. Stampa prima `coda_urgenti`, poi `coda_normali`.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

#define MAX 6

int coda_urgenti[MAX], tu = 0;
int coda_normali[MAX], tn = 0;

int main() {
    int n;
    printf("Quante persone? ");
    scanf("%d", &n);
    if (n > MAX) n = MAX;

    for (int i = 1; i <= n; i++) {
        int p;
        printf("Persona %d, priorita (1=urgente, 0=normale): ", i);
        scanf("%d", &p);
        if (p == 1) coda_urgenti[tu++] = i;
        else        coda_normali[tn++] = i;
    }

    printf("Ordine di servizio:\n");
    for (int i = 0; i < tu; i++)
        printf("Persona %d (urgente)\n", coda_urgenti[i]);
    for (int i = 0; i < tn; i++)
        printf("Persona %d (normale)\n", coda_normali[i]);

    return 0;
}
```

</details>

---

### Esercizio 5 — Interprete di comandi per la pila (20–25 min)

**Testo:**
Leggi comandi da tastiera:
- `P N` → push del numero N
- `O` → pop (stampa il valore rimosso, o `"vuota"` se la pila è vuota)
- `F` → fine programma

**Esempio input:**
```
P 5
P 12
O
P 3
O
O
F
```

**Esempio output:**
```
Pop: 12
Pop: 3
Pop: 5
```

**💡 Hint:**
1. Usa `scanf(" %c", &cmd)` per leggere il carattere comando.
2. Se `cmd == 'P'`: leggi anche un intero e fai push.
3. Se `cmd == 'O'`: fai pop e stampa.
4. Se `cmd == 'F'`: `break`.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

#define MAX 10

int pila[MAX];
int top = -1;

void push(int v) { if (top < MAX-1) pila[++top] = v; }
int pop()        { return (top == -1) ? -999 : pila[top--]; }
int isEmpty()    { return top == -1; }

int main() {
    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'P') {
            int n; scanf("%d", &n);
            push(n);
        } else if (cmd == 'O') {
            if (isEmpty()) printf("Pop: vuota\n");
            else printf("Pop: %d\n", pop());
        } else if (cmd == 'F') {
            break;
        }
    }
    return 0;
}
```

</details>

---

### Esercizio 5b — Coda Circolare: riempi, svuota e riempi (20–25 min)

**Testo:**
Dimostra il vantaggio della coda circolare rispetto a quella lineare. Con un array di 4 slot:
1. Inserisci 3 elementi (10, 20, 30)
2. Estrai 2 elementi
3. Inserisci altri 3 elementi (40, 50, 60)
4. Stampa tutti gli elementi rimasti in coda

Con la coda **lineare** il passo 3 fallirebbe (tail raggiungerebbe il limite). Con la coda **circolare** funziona perché gli slot liberati vengono riutilizzati.

**Esempio output:**
```
Estratto: 10
Estratto: 20
Coda finale: 30 40 50 60
```

**💡 Hint:**
1. Implementa `enqueue` e `dequeue` usando `(indice + 1) % MAX` con `MAX = 4`.
2. Dopo i 2 `dequeue`, `head` è a 2. Inserendo altri elementi, `tail` passa per 3 poi torna a 0 e 1.
3. Per stampare: `for (i = 0; i < size; i++) printf("%d ", coda[(head + i) % MAX])`.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

#define MAX 4

int coda[MAX];
int head = 0, tail = 0, size = 0;

int isEmpty() { return size == 0; }
int isFull()  { return size == MAX; }

void enqueue(int v) {
    if (isFull()) { printf("Coda piena!\n"); return; }
    coda[tail] = v;
    tail = (tail + 1) % MAX;
    size++;
}

int dequeue() {
    if (isEmpty()) { printf("Coda vuota!\n"); return -1; }
    int v = coda[head];
    head = (head + 1) % MAX;
    size--;
    return v;
}

void stampa() {
    printf("Coda finale:");
    for (int i = 0; i < size; i++)
        printf(" %d", coda[(head + i) % MAX]);
    printf("\n");
}

int main() {
    enqueue(10); enqueue(20); enqueue(30);
    printf("Estratto: %d\n", dequeue());
    printf("Estratto: %d\n", dequeue());
    enqueue(40); enqueue(50); enqueue(60);
    stampa();
    return 0;
}
```

</details>

---

## 🔴 Livello Avanzato

### Esercizio 6 — Coda di messaggi interattiva (30–40 min)

**Testo:**
Simula una coda di messaggi di testo. Comandi:
- `A TESTO` → aggiunge il messaggio TESTO (max 20 car.)
- `L` → legge ed elimina il primo messaggio
- `S` → mostra tutti i messaggi in coda
- `Q` → termina

Capacità massima: 5 messaggi.

**Esempio sessione:**
```
> A Ciao
> A Buongiorno
> A HaiVisto
> S
  [0] Ciao
  [1] Buongiorno
  [2] HaiVisto
> L
Messaggio letto: Ciao
> S
  [0] Buongiorno
  [1] HaiVisto
> Q
```

**💡 Hint:**
1. Usa `char coda[5][21]` per i messaggi.
2. `enqueue`: `strcpy(coda[tail], testo)` poi incrementa `tail` e `size`.
3. `dequeue`: stampa `coda[head]`, incrementa `head`, decrementa `size`.
4. `mostra`: ciclo `for (i = 0; i < size; i++)` — accede a `coda[(head + i) % MAX_MSG]`.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <string.h>

#define MAX_MSG 5
#define MAX_LEN 21

char coda[MAX_MSG][MAX_LEN];
int head = 0, tail = 0, size = 0;

void enqueue(char *testo) {
    if (size == MAX_MSG) { printf("Coda piena!\n"); return; }
    strcpy(coda[tail], testo);
    tail = (tail + 1) % MAX_MSG;
    size++;
}

void dequeue() {
    if (size == 0) { printf("Nessun messaggio.\n"); return; }
    printf("Messaggio letto: %s\n", coda[head]);
    head = (head + 1) % MAX_MSG;
    size--;
}

void mostra() {
    if (size == 0) { printf("Coda vuota.\n"); return; }
    for (int i = 0; i < size; i++)
        printf("  [%d] %s\n", i, coda[(head + i) % MAX_MSG]);
}

int main() {
    char cmd;
    char testo[MAX_LEN];
    while (1) {
        printf("> ");
        scanf(" %c", &cmd);
        if      (cmd == 'A') { scanf("%20s", testo); enqueue(testo); }
        else if (cmd == 'L') dequeue();
        else if (cmd == 'S') mostra();
        else if (cmd == 'Q') break;
    }
    return 0;
}
```

</details>

---

### Esercizio 7 — Valuta un'espressione aritmetica (35–45 min)

**Testo:**
Leggi un'espressione con **interi a una cifra** e operatori `+` e `-` senza spazi (es. `3+5-2+1`) e calcolane il valore.

> ⚠️ NOTA: Per semplicità gli operatori non hanno precedenza — l'espressione viene elaborata da sinistra a destra.

**Esempio input/output:**
```
Espressione: 3+5-2+1
Risultato: 7
```

**💡 Hint:**
1. Leggi la stringa con `scanf`.
2. Il valore di un carattere cifra si ottiene con `c - '0'`.
3. Inizializza `risultato` con il primo carattere convertito in intero.
4. Scorri la stringa a passi di 2 (`i += 2`): leggi operatore e operando, aggiorna `risultato`.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <string.h>

int main() {
    char expr[50];
    printf("Espressione: ");
    scanf("%s", expr);

    int risultato = expr[0] - '0';
    int len = strlen(expr);

    for (int i = 1; i < len - 1; i += 2) {
        char op = expr[i];
        int operando = expr[i + 1] - '0';
        if (op == '+') risultato += operando;
        else if (op == '-') risultato -= operando;
    }

    printf("Risultato: %d\n", risultato);
    return 0;
}
```

</details>
