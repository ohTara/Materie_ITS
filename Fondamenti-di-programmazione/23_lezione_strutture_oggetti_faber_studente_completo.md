# Lezione G15: Strutture, Oggetti e Progetto Faber

**Durata totale:** 4 ore
**Teoria:** 3 ore | **Esercizi:** 1 ora
**Data:** _______________
**Ambiente:** CLion (JetBrains)
**Giornata:** G15 di 19 — Ore corso: 56/76

---

## PARTE 1 — TEORIA (3 ore)

### 1.1 Introduzione e motivazione

Immagina di dover gestire un archivio di dipendenti di un'azienda. Per ogni dipendente ti servono: nome, cognome, età, stipendio, reparto. Con quello che sai finora, dovresti usare array separati:

```c
char nomi[100][50];
char cognomi[100][50];
int eta[100];
float stipendi[100];
char reparti[100][30];
```

Questo approccio è fragile: se vuoi spostare il dipendente numero 5 in un'altra posizione, devi aggiornare tutti e cinque gli array separatamente. Un errore è quasi garantito.

Le **strutture** (`struct`) risolvono questo problema: permettono di raggruppare dati di tipo diverso sotto un unico nome. Sono il mattone fondamentale della programmazione orientata ai dati — e, come vedremo, il precursore diretto degli **oggetti** della programmazione orientata agli oggetti (OOP).

Il **Progetto Faber** è un sistema gestionale per un negozio di strumenti musicali. Oggi costruiremo insieme le strutture dati che lo sostengono: un catalogo di strumenti, un registro di vendite, e le funzioni per gestirli.

---

### 1.2 Spiegazione dell'argomento

#### 1.2.1 Ripasso: cos'è una `struct`

Una `struct` è un tipo di dato composto, definito dal programmatore, che raccoglie variabili (chiamate **campi** o **membri**) anche di tipo diverso.

**Sintassi:**

```c
struct NomeTipo {
    tipo1 campo1;
    tipo2 campo2;
    // ...
};
```

**Dichiarazione di una variabile:**

```c
struct NomeTipo variabile;
```

**Accesso ai campi (operatore punto):**

```c
variabile.campo1 = valore;
```

**Memoria — come è organizzata una struct:**

```
struct Punto { int x; int y; };

Memoria RAM:
+--------+--------+
|   x    |   y    |
| 4 byte | 4 byte |
+--------+--------+
   ^
   indirizzo della struct
```

Ogni campo occupa spazio contiguo in memoria. La dimensione totale è (almeno) la somma dei campi — il compilatore può aggiungere padding per l'allineamento.

#### 1.2.2 `typedef` — dare un nome pulito alla struct

Scrivere `struct Strumento s;` ogni volta è verboso. Con `typedef` possiamo rinominare il tipo:

```c
typedef struct {
    char nome[50];
    char categoria[30];
    float prezzo;
    int quantita;
} Strumento;
```

Ora possiamo scrivere semplicemente:

```c
Strumento s;
```

Questa è la forma moderna e preferita in C.

#### 1.2.3 Inizializzazione di una struct

**Modo 1 — inizializzazione per posizione:**

```c
Strumento s = {"Chitarra Classica", "Cordofoni", 349.90f, 5};
```

**Modo 2 — inizializzazione per nome (C99, più leggibile):**

```c
Strumento s = {
    .nome = "Chitarra Classica",
    .categoria = "Cordofoni",
    .prezzo = 349.90f,
    .quantita = 5
};
```

**Modo 3 — assegnazione campo per campo:**

```c
Strumento s;
strcpy(s.nome, "Chitarra Classica");
strcpy(s.categoria, "Cordofoni");
s.prezzo = 349.90f;
s.quantita = 5;
```

⚠️ Per i campi stringa, non usare `=` ma sempre `strcpy()` — oppure `snprintf()` se vuoi più sicurezza.

#### 1.2.4 Array di struct

È la combinazione più utile: un catalogo, un archivio, un registro.

```
Strumento catalogo[100]:

catalogo[0]             catalogo[1]             catalogo[2]
+------------------+   +------------------+   +------------------+
| nome: "Chitarra" |   | nome: "Violino"  |   | nome: "Tromba"   |
| cat:  "Cordof."  |   | cat:  "Cordof."  |   | cat:  "Ottoni"   |
| prezzo: 349.90   |   | prezzo: 890.00   |   | prezzo: 520.00   |
| quantita: 5      |   | quantita: 2      |   | quantita: 8      |
+------------------+   +------------------+   +------------------+
```

Accesso:

```c
catalogo[0].prezzo = 399.90f;
printf("%s: %.2f €\n", catalogo[1].nome, catalogo[1].prezzo);
```

#### 1.2.5 Struct come parametri di funzione

**Passaggio per valore (copia):** la funzione riceve una copia. Modifiche non si propagano.

```c
void stampa_strumento(Strumento s) {
    printf("[%s] %s — %.2f €, qty: %d\n",
           s.categoria, s.nome, s.prezzo, s.quantita);
}
```

**Passaggio per indirizzo (puntatore):** la funzione lavora sull'originale. Modifiche si propagano. Si usa l'operatore `->` per accedere ai campi.

```c
void applica_sconto(Strumento *s, float percentuale) {
    s->prezzo *= (1.0f - percentuale / 100.0f);
}
```

Regola pratica:
- Se la funzione **legge** la struct → passa per valore (o `const *`)
- Se la funzione **modifica** la struct → passa per puntatore

#### 1.2.6 Operatore `->` vs `.`

```
Strumento s;          →  s.prezzo         (variabile diretta)
Strumento *p = &s;   →  p->prezzo        (puntatore)
                         (*p).prezzo      (equivalente, ma più verboso)
```

```
Accesso diretto:              Accesso tramite puntatore:
   s                              p
+--------+                    +------+     +--------+
| prezzo |   <-- s.prezzo     | addr |---> | prezzo |  <-- p->prezzo
+--------+                    +------+     +--------+
```

#### 1.2.7 Struct annidate

Una struct può contenere un'altra struct come campo:

```c
typedef struct {
    int giorno;
    int mese;
    int anno;
} Data;

typedef struct {
    char cliente[50];
    Strumento articolo;
    int quantita_venduta;
    Data data_vendita;
    float totale;
} Vendita;
```

Accesso:

```c
Vendita v;
v.data_vendita.giorno = 15;
v.data_vendita.mese   = 3;
v.data_vendita.anno   = 2025;
```

#### 1.2.8 Dal C agli oggetti — il ponte concettuale

Le `struct` del C e gli **oggetti** dell'OOP (Java, C++, Python) condividono l'idea di fondo: raggruppare dati correlati. La differenza principale è che gli oggetti aggiungono **metodi** (funzioni) direttamente all'interno del tipo.

```
STRUCT in C:                    OGGETTO in Java/C++:
+------------------------+      +----------------------------+
| DATI                   |      | DATI (attributi)           |
|  nome, prezzo, qty     |      |  nome, prezzo, qty         |
+------------------------+      +----------------------------+
                                | COMPORTAMENTI (metodi)     |
Funzioni ESTERNE:               |  stampa(), applica_sconto()|
stampa_strumento(&s);           +----------------------------+
applica_sconto(&s, 10);         s.stampa(); s.sconto(10);
```

In C, il "collegamento" tra dati e funzioni è implicito (convezione: passiamo sempre la struct come primo parametro). Negli OOP è esplicito e garantito dal linguaggio.

Questa è la **radice storica e concettuale** dell'OOP: C → C with classes → C++ → Java.

---

### 1.3 Esempi di codice commentati

#### Esempio 1 — Struttura base e stampa

```c
#include <stdio.h>
#include <string.h>

typedef struct {
    char nome[50];
    char categoria[30];
    float prezzo;
    int quantita;
} Strumento;

void stampa_strumento(Strumento s) {
    printf("%-25s | %-15s | %8.2f € | qty: %d\n",
           s.nome, s.categoria, s.prezzo, s.quantita);
}

int main() {
    Strumento s1, s2, s3;

    strcpy(s1.nome, "Chitarra Classica");
    strcpy(s1.categoria, "Cordofoni");
    s1.prezzo    = 349.90f;
    s1.quantita  = 5;

    Strumento s2_init = {"Violino 4/4", "Cordofoni", 890.00f, 2};
    s2 = s2_init;

    Strumento s3_init = {
        .nome      = "Tromba in Sib",
        .categoria = "Ottoni",
        .prezzo    = 520.00f,
        .quantita  = 8
    };
    s3 = s3_init;

    printf("%-25s | %-15s | %8s   | %s\n",
           "NOME", "CATEGORIA", "PREZZO", "QTY");
    printf("%-25s-+-%-15s-+-%-8s---+------\n",
           "-------------------------", "---------------", "--------");

    stampa_strumento(s1);
    stampa_strumento(s2);
    stampa_strumento(s3);

    return 0;
}
```

**Output atteso:**
```
NOME                      | CATEGORIA       |   PREZZO   | QTY
--------------------------+-----------------+------------+------
Chitarra Classica         | Cordofoni       |   349.90 € | qty: 5
Violino 4/4               | Cordofoni       |   890.00 € | qty: 2
Tromba in Sib             | Ottoni          |   520.00 € | qty: 8
```

---

#### Esempio 2 — Array di struct e funzione con puntatore

```c
#include <stdio.h>
#include <string.h>

#define MAX_CATALOGO 100

typedef struct {
    char nome[50];
    char categoria[30];
    float prezzo;
    int quantita;
} Strumento;

int aggiungi_strumento(Strumento catalogo[], int *n,
                       const char *nome, const char *cat,
                       float prezzo, int qty) {
    if (*n >= MAX_CATALOGO) return 0;
    strcpy(catalogo[*n].nome, nome);
    strcpy(catalogo[*n].categoria, cat);
    catalogo[*n].prezzo   = prezzo;
    catalogo[*n].quantita = qty;
    (*n)++;
    return 1;
}

void sconto_categoria(Strumento catalogo[], int n,
                      const char *categoria, float perc) {
    for (int i = 0; i < n; i++) {
        if (strcmp(catalogo[i].categoria, categoria) == 0) {
            catalogo[i].prezzo *= (1.0f - perc / 100.0f);
        }
    }
}

void stampa_catalogo(const Strumento catalogo[], int n) {
    printf("\n--- CATALOGO (%d articoli) ---\n", n);
    for (int i = 0; i < n; i++) {
        printf("%2d. %-25s [%-12s] %8.2f €  qty:%d\n",
               i + 1,
               catalogo[i].nome,
               catalogo[i].categoria,
               catalogo[i].prezzo,
               catalogo[i].quantita);
    }
}

int main() {
    Strumento catalogo[MAX_CATALOGO];
    int n = 0;

    aggiungi_strumento(catalogo, &n, "Chitarra Classica",  "Cordofoni", 349.90f, 5);
    aggiungi_strumento(catalogo, &n, "Chitarra Elettrica", "Cordofoni", 720.00f, 3);
    aggiungi_strumento(catalogo, &n, "Violino 4/4",        "Cordofoni", 890.00f, 2);
    aggiungi_strumento(catalogo, &n, "Tromba in Sib",      "Ottoni",    520.00f, 8);
    aggiungi_strumento(catalogo, &n, "Basso Elettrico",    "Cordofoni", 480.00f, 4);

    stampa_catalogo(catalogo, n);

    printf("\nApplico sconto 10%% ai Cordofoni...\n");
    sconto_categoria(catalogo, n, "Cordofoni", 10.0f);

    stampa_catalogo(catalogo, n);

    return 0;
}
```

**Output atteso:**
```
--- CATALOGO (5 articoli) ---
 1. Chitarra Classica      [Cordofoni   ]   349.90 €  qty:5
 2. Chitarra Elettrica     [Cordofoni   ]   720.00 €  qty:3
 3. Violino 4/4            [Cordofoni   ]   890.00 €  qty:2
 4. Tromba in Sib          [Ottoni      ]   520.00 €  qty:8
 5. Basso Elettrico        [Cordofoni   ]   480.00 €  qty:4

Applico sconto 10% ai Cordofoni...

--- CATALOGO (5 articoli) ---
 1. Chitarra Classica      [Cordofoni   ]   314.91 €  qty:5
 2. Chitarra Elettrica     [Cordofoni   ]   648.00 €  qty:3
 3. Violino 4/4            [Cordofoni   ]   801.00 €  qty:2
 4. Tromba in Sib          [Ottoni      ]   520.00 €  qty:8
 5. Basso Elettrico        [Cordofoni   ]   432.00 €  qty:4
```

---

#### Esempio 3 — Struct annidate: Vendita con Data

```c
#include <stdio.h>
#include <string.h>

typedef struct {
    char nome[50];
    char categoria[30];
    float prezzo;
    int quantita;
} Strumento;

typedef struct {
    int giorno;
    int mese;
    int anno;
} Data;

typedef struct {
    char cliente[50];
    Strumento articolo;
    int quantita_venduta;
    Data data_vendita;
    float totale;
} Vendita;

void stampa_vendita(const Vendita *v) {
    printf("Cliente:  %s\n", v->cliente);
    printf("Articolo: %s (%.2f € x %d)\n",
           v->articolo.nome,
           v->articolo.prezzo,
           v->quantita_venduta);
    printf("Totale:   %.2f €\n", v->totale);
    printf("Data:     %02d/%02d/%04d\n",
           v->data_vendita.giorno,
           v->data_vendita.mese,
           v->data_vendita.anno);
}

int main() {
    Strumento ch;
    strcpy(ch.nome, "Chitarra Classica");
    strcpy(ch.categoria, "Cordofoni");
    ch.prezzo   = 349.90f;
    ch.quantita = 5;

    Vendita v;
    strcpy(v.cliente, "Marco Rossi");
    v.articolo         = ch;
    v.quantita_venduta = 2;
    v.data_vendita.giorno = 15;
    v.data_vendita.mese   = 3;
    v.data_vendita.anno   = 2025;
    v.totale = v.articolo.prezzo * v.quantita_venduta;

    printf("=== SCONTRINO ===\n");
    stampa_vendita(&v);

    return 0;
}
```

**Output atteso:**
```
=== SCONTRINO ===
Cliente:  Marco Rossi
Articolo: Chitarra Classica (349.90 € x 2)
Totale:   699.80 €
Data:     15/03/2025
```

---

### 1.4 Riepilogo visivo

```
CONCETTI CHIAVE — STRUCT IN C
═══════════════════════════════════════════════════════════════

 DEFINIZIONE                    ACCESSO
 ──────────                     ───────
 typedef struct {               Diretta:    s.campo
     tipo1 campo1;              Puntatore:  p->campo
     tipo2 campo2;              Annidato:   s.inner.campo
 } NomeTipo;

 INIZIALIZZAZIONE               FUNZIONI
 ──────────────                 ────────
 Per posizione: {"a", 1, 2.0}  Lettura → passa per valore
 Per nome: {.campo = val}       Modifica → passa per puntatore
 Campo per campo: s.x = 5;

 ARRAY DI STRUCT                STRUCT ANNIDATE
 ──────────────                 ───────────────
 NomeTipo arr[N];               typedef struct {
 arr[i].campo = val;                Data d;     ← struct dentro struct
 for (i = 0..n) arr[i]...          float tot;
                                } Vendita;

 DAL C AGLI OGGETTI
 ──────────────────
 C struct    →  dati raggruppati
 C funzioni  →  comportamenti separati
 OOP objects →  dati + metodi insieme (incapsulamento)
```

---

### 1.5 Domande di verifica orale

**D1:** Qual è la differenza tra `s.campo` e `p->campo`?

<details>
<summary><b>💡 RISPOSTA</b></summary>

`s.campo` si usa quando `s` è una variabile struct (accesso diretto). `p->campo` si usa quando `p` è un puntatore a struct; equivale a `(*p).campo`.

</details>

---

**D2:** Perché per copiare una stringa in un campo struct si usa `strcpy` e non l'operatore `=`?

<details>
<summary><b>💡 RISPOSTA</b></summary>

I campi stringa sono array di char. In C non si possono assegnare array con `=` (assegnerebbe l'indirizzo, non il contenuto). `strcpy` copia byte per byte il contenuto. L'eccezione è l'inizializzazione con letterale stringa alla dichiarazione.

</details>

---

**D3:** Quando conviene passare una struct per puntatore invece che per valore?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Sempre quando la funzione deve **modificare** la struct originale. Anche quando la struct è grande, per evitare la copia in memoria (efficienza). Per sola lettura si può usare `const Strumento *s`.

</details>

---

**D4:** Cosa sono le struct annidate? Fai un esempio.

<details>
<summary><b>💡 RISPOSTA</b></summary>

Una struct che contiene un campo di tipo struct. Esempio: una struct `Vendita` che ha un campo `Data data_vendita` di tipo struct `Data`. Si accede con doppio punto: `v.data_vendita.giorno`.

</details>

---

**D5:** Qual è la differenza concettuale tra una struct in C e un oggetto in Java/C++?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Entrambi raggruppano dati correlati. La differenza è che gli oggetti includono anche i metodi (funzioni) all'interno del tipo, realizzando l'incapsulamento. In C, le funzioni che lavorano su una struct sono esterne e ricevono la struct come parametro.

</details>

---

**D6:** Come si scorre un array di struct con un ciclo `for`? Scrivi la sintassi.

<details>
<summary><b>💡 RISPOSTA</b></summary>

```c
for (int i = 0; i < n; i++) {
    // accesso: arr[i].campo
    printf("%s\n", arr[i].nome);
}
```

</details>

---

**D7:** `sizeof(Strumento)` sarà sempre uguale alla somma dei `sizeof` dei singoli campi?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Non necessariamente. Il compilatore può inserire **padding** (byte di allineamento) tra i campi per ottimizzare l'accesso in memoria. Quindi `sizeof(struct)` può essere ≥ alla somma dei campi.

</details>

---

## PARTE 2 — ESERCIZI (1 ora)

---

### 🟢 Livello Base

#### Esercizio 1 — Schedario Strumenti (20 min)

**Testo:**
Crea una struttura `Strumento` con i campi: `nome` (stringa, max 50 char), `categoria` (stringa, max 30 char), `prezzo` (float), `quantita` (int). Scrivi un programma che:
1. Chiede all'utente di inserire 3 strumenti da tastiera
2. Stampa un riepilogo tabellare di tutti gli strumenti inseriti

**Esempio Input:**
```
Strumento 1:
  Nome: Chitarra Classica
  Categoria: Cordofoni
  Prezzo: 349.90
  Quantita: 5
...
```

**Esempio Output:**
```
--- CATALOGO ---
1. Chitarra Classica     [Cordofoni]  349.90 € qty:5
2. Tromba in Sib         [Ottoni   ]  520.00 € qty:8
3. Flauto Traverso       [Legni    ]  280.00 € qty:3
```

**💡 Hint:**
1. Definisci `typedef struct { ... } Strumento;` prima del `main`
2. Usa un array `Strumento catalogo[3];` e un ciclo `for` per l'inserimento
3. Per leggere stringhe con spazi usa `fgets` e rimuovi il `\n` finale con `strcspn`
4. Per leggere float usa `scanf("%f", &catalogo[i].prezzo)`

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <string.h>

typedef struct {
    char nome[50];
    char categoria[30];
    float prezzo;
    int quantita;
} Strumento;

int main() {
    Strumento catalogo[3];
    int n = 3;

    for (int i = 0; i < n; i++) {
        printf("\nStrumento %d:\n", i + 1);

        printf("  Nome: ");
        fgets(catalogo[i].nome, sizeof(catalogo[i].nome), stdin);
        catalogo[i].nome[strcspn(catalogo[i].nome, "\n")] = '\0';

        printf("  Categoria: ");
        fgets(catalogo[i].categoria, sizeof(catalogo[i].categoria), stdin);
        catalogo[i].categoria[strcspn(catalogo[i].categoria, "\n")] = '\0';

        printf("  Prezzo: ");
        scanf("%f", &catalogo[i].prezzo);

        printf("  Quantita: ");
        scanf("%d", &catalogo[i].quantita);

        while (getchar() != '\n');
    }

    printf("\n--- CATALOGO ---\n");
    for (int i = 0; i < n; i++) {
        printf("%d. %-20s [%-10s] %8.2f € qty:%d\n",
               i + 1,
               catalogo[i].nome,
               catalogo[i].categoria,
               catalogo[i].prezzo,
               catalogo[i].quantita);
    }

    return 0;
}
```

</details>

---

### 🟡 Livello Intermedio

#### Esercizio 2 — Valore del Magazzino (25 min)

**Testo:**
Partendo da un catalogo di 5 strumenti hardcoded, scrivi una funzione `float valore_magazzino(Strumento catalogo[], int n)` che restituisce il valore totale del magazzino (prezzo × quantità per ogni strumento). Aggiungi anche una funzione `Strumento strumento_piu_costoso(Strumento catalogo[], int n)` che restituisce lo strumento con il prezzo più alto.

**Esempio Output:**
```
Valore totale magazzino: 13029.50 EUR
Strumento piu costoso: Violino 4/4 (890.00 EUR)
```

**💡 Hint:**
1. `valore_magazzino` scorre l'array con un `for` e accumula `catalogo[i].prezzo * catalogo[i].quantita`
2. `strumento_piu_costoso` tiene traccia dell'indice del massimo, come l'algoritmo di ricerca del massimo su array
3. Le funzioni ricevono l'array per indirizzo (automatico per gli array) e la dimensione `n`
4. Una funzione può restituire una struct per valore: `return catalogo[idx_max];`

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <string.h>

typedef struct {
    char nome[50];
    char categoria[30];
    float prezzo;
    int quantita;
} Strumento;

float valore_magazzino(Strumento catalogo[], int n) {
    float totale = 0.0f;
    for (int i = 0; i < n; i++) {
        totale += catalogo[i].prezzo * catalogo[i].quantita;
    }
    return totale;
}

Strumento strumento_piu_costoso(Strumento catalogo[], int n) {
    int idx_max = 0;
    for (int i = 1; i < n; i++) {
        if (catalogo[i].prezzo > catalogo[idx_max].prezzo) {
            idx_max = i;
        }
    }
    return catalogo[idx_max];
}

int main() {
    Strumento catalogo[] = {
        {"Chitarra Classica",  "Cordofoni", 349.90f, 5},
        {"Chitarra Elettrica", "Cordofoni", 720.00f, 3},
        {"Violino 4/4",        "Cordofoni", 890.00f, 2},
        {"Tromba in Sib",      "Ottoni",    520.00f, 8},
        {"Basso Elettrico",    "Cordofoni", 480.00f, 4}
    };
    int n = 5;

    float valore = valore_magazzino(catalogo, n);
    printf("Valore totale magazzino: %.2f EUR\n", valore);

    Strumento piu_costoso = strumento_piu_costoso(catalogo, n);
    printf("Strumento piu costoso: %s (%.2f EUR)\n",
           piu_costoso.nome, piu_costoso.prezzo);

    return 0;
}
```

</details>

---

#### Esercizio 3 — Mini Progetto Faber: Registro Vendite (30 min)

**Testo:**
Crea una struct `Vendita` con i campi: `cliente` (stringa), `nome_strumento` (stringa), `prezzo_unitario` (float), `quantita` (int), `totale` (float). Scrivi un programma che:
1. Permette di registrare fino a 10 vendite (inserimento da tastiera)
2. Al termine, stampa tutte le vendite e il totale incassato

**Esempio Output:**
```
=== REGISTRO VENDITE ===
1. Marco Rossi       | Chitarra Classica   | 2 x 349.90 = 699.80 EUR
2. Laura Bianchi     | Tromba in Sib       | 1 x 520.00 = 520.00 EUR
---------------------------------
Totale incassato: 1219.80 EUR
```

**💡 Hint:**
1. La struct `Vendita` non ha bisogno di contenere la struct `Strumento` — basta `nome_strumento` come stringa e `prezzo_unitario` come float
2. Calcola `totale = prezzo_unitario * quantita` al momento dell'inserimento
3. Usa un ciclo `do-while` con una condizione di uscita ("s/n")
4. Tieni un contatore `n_vendite` da passare alla funzione di stampa

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <string.h>

#define MAX_VENDITE 10

typedef struct {
    char cliente[50];
    char nome_strumento[50];
    float prezzo_unitario;
    int quantita;
    float totale;
} Vendita;

void stampa_registro(const Vendita registro[], int n) {
    float totale_incassato = 0.0f;
    printf("\n=== REGISTRO VENDITE ===\n");
    for (int i = 0; i < n; i++) {
        printf("%2d. %-20s | %-20s | %d x %.2f = %.2f EUR\n",
               i + 1,
               registro[i].cliente,
               registro[i].nome_strumento,
               registro[i].quantita,
               registro[i].prezzo_unitario,
               registro[i].totale);
        totale_incassato += registro[i].totale;
    }
    printf("---------------------------------\n");
    printf("Totale incassato: %.2f EUR\n", totale_incassato);
}

int main() {
    Vendita registro[MAX_VENDITE];
    int n = 0;
    char continua;

    do {
        if (n >= MAX_VENDITE) { printf("Registro pieno!\n"); break; }

        printf("\n--- Nuova vendita (#%d) ---\n", n + 1);

        printf("Cliente: ");
        fgets(registro[n].cliente, sizeof(registro[n].cliente), stdin);
        registro[n].cliente[strcspn(registro[n].cliente, "\n")] = '\0';

        printf("Strumento: ");
        fgets(registro[n].nome_strumento, sizeof(registro[n].nome_strumento), stdin);
        registro[n].nome_strumento[strcspn(registro[n].nome_strumento, "\n")] = '\0';

        printf("Prezzo unitario: ");
        scanf("%f", &registro[n].prezzo_unitario);

        printf("Quantita: ");
        scanf("%d", &registro[n].quantita);

        registro[n].totale = registro[n].prezzo_unitario * registro[n].quantita;
        n++;

        printf("Altra vendita? (s/n): ");
        scanf(" %c", &continua);
        while (getchar() != '\n');

    } while (continua == 's' || continua == 'S');

    stampa_registro(registro, n);

    return 0;
}
```

</details>

---

### 🔴 Livello Avanzato

#### Esercizio 4 — Progetto Faber Completo (45 min)

**Testo:**
Integra tutto in un mini-gestionale con menu interattivo:
```
1. Aggiungi strumento al catalogo
2. Visualizza catalogo
3. Registra una vendita (scegliendo da catalogo, aggiorna la quantità)
4. Visualizza registro vendite e totale incassato
5. Esci
```

Regole:
- Non è possibile vendere più pezzi di quanti ce ne siano in magazzino
- Ogni vendita aggiorna il campo `quantita` dello strumento venduto nel catalogo
- Il programma termina solo scegliendo l'opzione 5

**💡 Hint:**
1. Definisci due array: `Strumento catalogo[MAX]` e `Vendita registro[MAX]` con relativi contatori
2. Scrivi una funzione per ogni voce di menu — mantieni il `main` pulito (solo il ciclo del menu)
3. Per la vendita: mostra prima il catalogo, chiedi l'indice, controlla `qty_richiesta <= catalogo[idx].quantita`
4. Aggiorna `catalogo[idx].quantita -= qty_venduta` dopo la vendita

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <string.h>

#define MAX_CAT 50
#define MAX_VEN 100

typedef struct {
    char nome[50];
    char categoria[30];
    float prezzo;
    int quantita;
} Strumento;

typedef struct {
    char cliente[50];
    char nome_strumento[50];
    float prezzo_unitario;
    int quantita;
    float totale;
} Vendita;

Strumento catalogo[MAX_CAT];
int n_cat = 0;

Vendita registro[MAX_VEN];
int n_ven = 0;

void leggi_stringa(const char *prompt, char *dest, int size) {
    printf("%s", prompt);
    fgets(dest, size, stdin);
    dest[strcspn(dest, "\n")] = '\0';
}

void aggiungi_strumento(void) {
    if (n_cat >= MAX_CAT) { printf("Catalogo pieno.\n"); return; }
    Strumento *s = &catalogo[n_cat];
    leggi_stringa("Nome: ", s->nome, sizeof(s->nome));
    leggi_stringa("Categoria: ", s->categoria, sizeof(s->categoria));
    printf("Prezzo: "); scanf("%f", &s->prezzo);
    printf("Quantita: "); scanf("%d", &s->quantita);
    while (getchar() != '\n');
    n_cat++;
    printf("Strumento aggiunto.\n");
}

void visualizza_catalogo(void) {
    if (n_cat == 0) { printf("Catalogo vuoto.\n"); return; }
    printf("\n%-3s %-25s %-15s %8s %5s\n", "#", "NOME", "CATEGORIA", "PREZZO", "QTY");
    for (int i = 0; i < n_cat; i++) {
        printf("%-3d %-25s %-15s %8.2f %5d\n",
               i + 1,
               catalogo[i].nome, catalogo[i].categoria,
               catalogo[i].prezzo, catalogo[i].quantita);
    }
}

void registra_vendita(void) {
    if (n_cat == 0) { printf("Catalogo vuoto.\n"); return; }
    if (n_ven >= MAX_VEN) { printf("Registro pieno.\n"); return; }

    visualizza_catalogo();

    int idx;
    printf("Scegli strumento (1-%d): ", n_cat);
    scanf("%d", &idx);
    while (getchar() != '\n');
    idx--;

    if (idx < 0 || idx >= n_cat) { printf("Indice non valido.\n"); return; }
    if (catalogo[idx].quantita == 0) { printf("Esaurito.\n"); return; }

    int qty;
    printf("Quantita (disponibili: %d): ", catalogo[idx].quantita);
    scanf("%d", &qty);
    while (getchar() != '\n');

    if (qty <= 0 || qty > catalogo[idx].quantita) {
        printf("Quantita non valida.\n"); return;
    }

    Vendita *v = &registro[n_ven];
    leggi_stringa("Cliente: ", v->cliente, sizeof(v->cliente));
    strcpy(v->nome_strumento, catalogo[idx].nome);
    v->prezzo_unitario = catalogo[idx].prezzo;
    v->quantita        = qty;
    v->totale          = v->prezzo_unitario * v->quantita;

    catalogo[idx].quantita -= qty;
    n_ven++;

    printf("Vendita registrata: %.2f EUR\n", v->totale);
}

void visualizza_vendite(void) {
    if (n_ven == 0) { printf("Nessuna vendita.\n"); return; }
    float totale = 0.0f;
    printf("\n=== REGISTRO VENDITE ===\n");
    for (int i = 0; i < n_ven; i++) {
        printf("%2d. %-18s | %-20s | %dx%.2f = %.2f EUR\n",
               i + 1,
               registro[i].cliente,
               registro[i].nome_strumento,
               registro[i].quantita,
               registro[i].prezzo_unitario,
               registro[i].totale);
        totale += registro[i].totale;
    }
    printf("Totale incassato: %.2f EUR\n", totale);
}

int main() {
    int scelta;

    Strumento init[] = {
        {"Chitarra Classica",  "Cordofoni", 349.90f, 5},
        {"Tromba in Sib",      "Ottoni",    520.00f, 8},
        {"Violino 4/4",        "Cordofoni", 890.00f, 2}
    };
    for (int i = 0; i < 3; i++) catalogo[n_cat++] = init[i];

    do {
        printf("\n=== FABER MUSIC MANAGER ===\n");
        printf("1. Aggiungi strumento\n");
        printf("2. Visualizza catalogo\n");
        printf("3. Registra vendita\n");
        printf("4. Visualizza vendite\n");
        printf("5. Esci\n");
        printf("Scelta: ");
        scanf("%d", &scelta);
        while (getchar() != '\n');

        switch (scelta) {
            case 1: aggiungi_strumento(); break;
            case 2: visualizza_catalogo(); break;
            case 3: registra_vendita();    break;
            case 4: visualizza_vendite();  break;
            case 5: printf("Arrivederci!\n"); break;
            default: printf("Scelta non valida.\n");
        }
    } while (scelta != 5);

    return 0;
}
```

</details>

---

## 🎯 Recap finale (5 min)

- **`typedef struct`** permette di creare tipi composti personalizzati che raggruppano dati eterogenei sotto un unico nome — il mattone base della modellazione dati in C.
- **Operatore `.` vs `->`**: si usa `.` per accedere ai campi di una variabile struct, `->` per accedere ai campi tramite un puntatore a struct.
- **Passaggio per valore vs puntatore**: le funzioni che devono modificare una struct ricevono un puntatore (`Strumento *s`); quelle che la leggono soltanto possono riceverla per valore o come `const Strumento *s`.
- **Struct annidate e array di struct**: strumenti potenti per modellare entità reali complesse — un archivio, un registro vendite, un catalogo.
- ⚠️ **Errore comune da evitare**: assegnare una stringa a un campo con `s.nome = "valore"` — questo non compila (o produce un warning grave) perché `nome` è un array. Usa sempre `strcpy(s.nome, "valore")`.
- 📌 **Prossima lezione (G16):** Le struct incontrano i file — impareremo a salvare e leggere strutture su disco usando `fwrite`/`fread` e `fprintf`/`fscanf`, rendendo i dati persistenti tra un'esecuzione e l'altra.
