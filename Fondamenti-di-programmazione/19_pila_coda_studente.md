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

    printf("Dequeue: %d\n", dequeue());
    printf("Dequeue: %d\n", dequeue());
    enqueue(40);
    printf("Dequeue: %d\n", dequeue());
    printf("Dequeue: %d\n", dequeue());

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

**D2:** In una pila implementata con array, cosa significa `top == -1`?

**D3:** Qual è la differenza tra `pop()` e `peek()`?

**D4:** In una coda, dove entrano i nuovi elementi e da dove escono?

**D5:** Eseguo: `push(1)`, `push(2)`, `push(3)`, `pop()`, `pop()`. Qual è la cima?

**D6:** Eseguo su una coda: `enqueue(1)`, `enqueue(2)`, `enqueue(3)`, `dequeue()`. Qual è il prossimo da estrarre?

**D7:** Cosa succede se chiamo `pop()` su una pila vuota nel codice degli esempi?

**D8:** Qual è il limite della coda lineare che la coda circolare risolve?

**D9:** In una coda circolare con MAX=4, se `tail` vale 3 e faccio un `enqueue`, dove si trova il prossimo `tail`?

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
