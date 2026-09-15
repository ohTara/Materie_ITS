# Lezione G14: Strutture (`struct`) — Definizione, accesso, array di struct

**Durata totale:** 4 ore
**Teoria:** 3 ore | **Esercizi:** 1 ora
**Data:** _______________
**Ambiente:** CLion (JetBrains)
**Giornata:** G14 di 19 — Ore corso: 52/76

---

## PARTE 1 — TEORIA (3 ore)

### 1.1 Introduzione e motivazione

Nella lezione precedente (G13) abbiamo gestito una rubrica con **due array paralleli**: uno per i nomi e uno per i telefoni. Questo approccio funziona, ma ha un difetto importante: i dati che appartengono allo stesso contatto sono **sparpagliati** in strutture separate. Basta un errore di indice e nome e telefono non corrispondono più.

```
APPROCCIO CON ARRAY PARALLELI (G13):

nomi[0]  = "Bianchi Mario"   tel[0] = "3337654321"
nomi[1]  = "Rossi Luca"      tel[1] = "3331234567"
nomi[2]  = "Verdi Anna"      tel[2] = "3339876543"

Problema: cosa succede se ordino solo nomi[] e dimentico tel[]?
→ I dati si disallineano e la rubrica è corrotta. ❌
```

Le **struct** risolvono questo problema raggruppando in un'unica variabile tutti i dati che descrivono la stessa entità del mondo reale. Un contatto ha nome E telefono — perché tenerli separati?

```
APPROCCIO CON STRUCT:

contatti[0] → { nome: "Bianchi Mario", tel: "3337654321" }
contatti[1] → { nome: "Rossi Luca",    tel: "3331234567" }
contatti[2] → { nome: "Verdi Anna",    tel: "3339876543" }

Nome e telefono viaggiano sempre insieme. ✅
```

Le struct sono il primo passo verso la **programmazione orientata agli oggetti**: raggruppare dati correlati in un tipo personalizzato è esattamente il concetto alla base delle classi in Java e C++.

---

### 1.2 Spiegazione dell'argomento

#### Definizione di una struct

Una `struct` è un tipo di dato **composto**, definito dal programmatore, che raggruppa variabili di tipo anche diverso chiamate **campi** (o *membri*).

**Sintassi:**
```c
struct NomeStruct {
    tipo1 campo1;
    tipo2 campo2;
    /* ... altri campi ... */
};
```

**Esempio concreto — un punto nel piano cartesiano:**
```c
struct Punto {
    float x;
    float y;
};
```

**Esempio — uno studente:**
```c
struct Studente {
    char nome[50];
    char cognome[50];
    int matricola;
    float media;
};
```

> **Importante:** la definizione di una struct NON alloca memoria — è solo la descrizione di come sarà fatto il tipo. La memoria viene allocata quando si dichiara una **variabile** di quel tipo.

---

#### Dichiarazione di variabili struct

Dopo aver definito la struct, si dichiarano le variabili:

```c
struct Studente s1;           // variabile singola
struct Studente s2, s3;       // più variabili

// Inizializzazione alla dichiarazione (in ordine dei campi)
struct Studente s4 = {"Mario", "Rossi", 12345, 27.5};
```

**Visualizzazione in memoria:**
```
struct Studente s1:
┌────────────────────────────────────────────────┐
│ nome[50]  │ cognome[50] │ matricola │  media   │
│ "Mario"   │ "Rossi"     │   12345   │  27.5    │
└────────────────────────────────────────────────┘
  50 byte      50 byte      4 byte     4 byte
                        Totale ≈ 108 byte
```

Tutti i campi della stessa variabile struct sono **contigui in memoria** e si spostano sempre insieme.

---

#### Accesso ai campi: operatore `.`

Per leggere o scrivere un campo di una struct si usa l'**operatore punto** `.`:

```c
struct Studente s;

/* Scrittura dei campi */
strcpy(s.nome, "Luigi");
strcpy(s.cognome, "Bianchi");
s.matricola = 54321;
s.media = 29.0;

/* Lettura dei campi */
printf("Nome: %s %s\n", s.nome, s.cognome);
printf("Matricola: %d\n", s.matricola);
printf("Media: %.1f\n", s.media);
```

**Schema dell'operatore `.`:**
```
  s  .  nome
  ↑  ↑    ↑
  │  │    └─ campo a cui accedere
  │  └─ operatore punto
  └─ variabile struct
```

---

#### `typedef` — semplificare il nome del tipo

Scrivere `struct Studente` ogni volta è verboso. Il costrutto `typedef` permette di creare un **alias** più breve:

```c
/* Senza typedef */
struct Studente s1;
struct Studente s2;

/* Con typedef */
typedef struct {
    char nome[50];
    char cognome[50];
    int matricola;
    float media;
} Studente;

/* Ora si può scrivere semplicemente: */
Studente s1;
Studente s2;
```

> **Convenzione:** i nomi dei tipi definiti con `typedef` si scrivono con la **prima lettera maiuscola** (es. `Studente`, `Punto`, `Prodotto`).

---

#### Assegnazione tra struct

A differenza degli array, due variabili struct dello stesso tipo si possono assegnare direttamente con `=`: il compilatore copia tutti i campi automaticamente.

```c
Studente a = {"Anna", "Verdi", 11111, 28.5};
Studente b;

b = a;   // copia TUTTI i campi di a in b ✅

/* Equivale a: */
strcpy(b.nome, a.nome);
strcpy(b.cognome, a.cognome);
b.matricola = a.matricola;
b.media = a.media;
```

Questo rende lo **scambio tra struct** molto più semplice:
```c
Studente temp = a;
a = b;
b = temp;
/* Nessuna strcpy necessaria! */
```

---

#### Array di struct

La combinazione più potente: un **array di struct** permette di gestire collezioni di entità complesse in modo pulito e ordinato.

```c
Studente classe[30];   /* array di 30 studenti */
```

**Visualizzazione in memoria:**
```
classe[0]: [ nome | cognome | matricola | media ]
classe[1]: [ nome | cognome | matricola | media ]
classe[2]: [ nome | cognome | matricola | media ]
...
classe[29]:[ nome | cognome | matricola | media ]
```

**Accesso ai campi dell'i-esimo elemento:**
```c
/* Sintassi: array[indice].campo */
strcpy(classe[0].nome, "Mario");
classe[0].media = 27.0;

printf("%s — media: %.1f\n", classe[i].nome, classe[i].media);
```

---

#### Lettura di un array di struct da tastiera

```c
Studente classe[30];
int n;

printf("Quanti studenti? ");
scanf("%d", &n);
getchar();   /* consuma il '\n' residuo */

for (int i = 0; i < n; i++) {
    printf("--- Studente %d ---\n", i + 1);

    printf("Nome: ");
    fgets(classe[i].nome, sizeof(classe[i].nome), stdin);
    if (classe[i].nome[strlen(classe[i].nome)-1] == '\n')
        classe[i].nome[strlen(classe[i].nome)-1] = '\0';

    printf("Cognome: ");
    fgets(classe[i].cognome, sizeof(classe[i].cognome), stdin);
    if (classe[i].cognome[strlen(classe[i].cognome)-1] == '\n')
        classe[i].cognome[strlen(classe[i].cognome)-1] = '\0';

    printf("Matricola: ");
    scanf("%d", &classe[i].matricola);

    printf("Media: ");
    scanf("%f", &classe[i].media);
    getchar();
}
```

---

#### Ordinamento di un array di struct

Per ordinare un array di struct si usa il Bubble Sort già noto. Poiché `=` copia tutti i campi automaticamente, lo **scambio è semplicissimo**:

```c
/* Ordinamento per media crescente */
for (int i = 0; i < n - 1; i++) {
    for (int j = 0; j < n - 1 - i; j++) {
        if (classe[j].media > classe[j+1].media) {
            Studente temp = classe[j];       /* copia intera struct */
            classe[j]     = classe[j+1];
            classe[j+1]   = temp;
        }
    }
}

/* Ordinamento per cognome (alfabetico) */
for (int i = 0; i < n - 1; i++) {
    for (int j = 0; j < n - 1 - i; j++) {
        if (strcmp(classe[j].cognome, classe[j+1].cognome) > 0) {
            Studente temp = classe[j];
            classe[j]     = classe[j+1];
            classe[j+1]   = temp;
        }
    }
}
```

> **Confronto con G13:** prima servivano due array paralleli (nomi + telefoni) e due serie di `strcpy` per lo scambio. Con le struct, lo scambio di **tutti i dati** di un contatto si fa con **tre semplici assegnazioni** `=`.

---

#### Struct come parametro di funzione

Le struct si possono passare alle funzioni **per valore** (viene passata una copia):

```c
void stampa_studente(Studente s) {
    printf("%-10s %-10s  matr: %d  media: %.1f\n",
           s.nome, s.cognome, s.matricola, s.media);
}

/* Chiamata */
stampa_studente(classe[i]);
```

---

### 1.3 Esempi di codice commentati

#### Esempio 1 — Prima struct: definizione, accesso e stampa

```c
#include <stdio.h>
#include <string.h>

typedef struct {
    char nome[30];
    int eta;
    float altezza;
} Persona;

int main() {
    Persona p1;
    Persona p2 = {"Maria", 25, 1.68};

    strcpy(p1.nome, "Luca");
    p1.eta     = 30;
    p1.altezza = 1.82;

    printf("Persona 1: %s, %d anni, %.2f m\n",
           p1.nome, p1.eta, p1.altezza);
    printf("Persona 2: %s, %d anni, %.2f m\n",
           p2.nome, p2.eta, p2.altezza);

    Persona p3 = p1;   /* copia completa */
    p3.eta = 31;       /* modifica solo p3 */

    printf("Persona 3 (copia di p1): %s, %d anni\n",
           p3.nome, p3.eta);
    printf("p1 invariata: %s, %d anni\n",
           p1.nome, p1.eta);

    return 0;
}
```

**Output atteso:**
```
Persona 1: Luca, 30 anni, 1.82 m
Persona 2: Maria, 25 anni, 1.68 m
Persona 3 (copia di p1): Luca, 31 anni
p1 invariata: Luca, 30 anni
```

---

#### Esempio 2 — Array di struct: rubrica migliorata

```c
#include <stdio.h>
#include <string.h>

#define MAX 5

typedef struct {
    char nome[30];
    char telefono[16];
} Contatto;

void stampa_rubrica(Contatto rubrica[], int n) {
    printf("\n%-25s %-15s\n", "NOME", "TELEFONO");
    printf("%-25s %-15s\n", "─────────────────────────", "───────────────");
    for (int i = 0; i < n; i++)
        printf("%-25s %-15s\n", rubrica[i].nome, rubrica[i].telefono);
}

int main() {
    Contatto rubrica[MAX] = {
        {"Bianchi Mario", "3337654321"},
        {"Rossi Luca",    "3331234567"},
        {"Verdi Anna",    "3339876543"},
        {"Conti Sara",    "3335551234"},
        {"Neri Paolo",    "3338889876"}
    };

    printf("Rubrica originale:");
    stampa_rubrica(rubrica, MAX);

    for (int i = 0; i < MAX - 1; i++) {
        for (int j = 0; j < MAX - 1 - i; j++) {
            if (strcmp(rubrica[j].nome, rubrica[j+1].nome) > 0) {
                Contatto temp = rubrica[j];
                rubrica[j]    = rubrica[j+1];
                rubrica[j+1]  = temp;
            }
        }
    }

    printf("\nRubrica ordinata:");
    stampa_rubrica(rubrica, MAX);

    return 0;
}
```

**Output atteso:**
```
Rubrica originale:
NOME                      TELEFONO
───────────────────────── ───────────────
Bianchi Mario             3337654321
Rossi Luca                3331234567
Verdi Anna                3339876543
Conti Sara                3335551234
Neri Paolo                3338889876

Rubrica ordinata:
NOME                      TELEFONO
───────────────────────── ───────────────
Bianchi Mario             3337654321
Conti Sara                3335551234
Neri Paolo                3338889876
Rossi Luca                3331234567
Verdi Anna                3339876543
```

---

#### Esempio 3 — Array di struct con input da tastiera e ricerca

```c
#include <stdio.h>
#include <string.h>

#define MAX_PROD 20

typedef struct {
    char descrizione[50];
    float prezzo;
    int quantita;
} Prodotto;

void stampa_prodotto(Prodotto p) {
    printf("  %-30s  €%7.2f  qty: %d\n",
           p.descrizione, p.prezzo, p.quantita);
}

int main() {
    Prodotto magazzino[MAX_PROD];
    int n, i;

    printf("Quanti prodotti? ");
    scanf("%d", &n);
    getchar();
    if (n > MAX_PROD) n = MAX_PROD;

    for (i = 0; i < n; i++) {
        printf("\n--- Prodotto %d ---\n", i + 1);
        printf("Descrizione: ");
        fgets(magazzino[i].descrizione, sizeof(magazzino[i].descrizione), stdin);
        if (magazzino[i].descrizione[strlen(magazzino[i].descrizione)-1] == '\n')
            magazzino[i].descrizione[strlen(magazzino[i].descrizione)-1] = '\0';

        printf("Prezzo: ");
        scanf("%f", &magazzino[i].prezzo);
        printf("Quantita': ");
        scanf("%d", &magazzino[i].quantita);
        getchar();
    }

    /* Ordina per prezzo crescente */
    for (i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (magazzino[j].prezzo > magazzino[j+1].prezzo) {
                Prodotto temp  = magazzino[j];
                magazzino[j]   = magazzino[j+1];
                magazzino[j+1] = temp;
            }
        }
    }

    printf("\n=== Prodotti ordinati per prezzo ===\n");
    for (i = 0; i < n; i++)
        stampa_prodotto(magazzino[i]);

    int idx_min = 0;
    for (i = 1; i < n; i++)
        if (magazzino[i].quantita < magazzino[idx_min].quantita)
            idx_min = i;

    printf("\nProdotto con scorte minime:\n");
    stampa_prodotto(magazzino[idx_min]);

    return 0;
}
```

**Output atteso (esempio):**
```
=== Prodotti ordinati per prezzo ===
  Mouse wireless                   € 22.50  qty: 8
  Tastiera USB                     € 45.90  qty: 12
  Monitor 24"                      €189.00  qty: 3

Prodotto con scorte minime:
  Monitor 24"                      €189.00  qty: 3
```

---

#### Esempio 4 — Struct come parametro di funzione

```c
#include <stdio.h>
#include <string.h>

typedef struct {
    char nome[50];
    int voti[5];
    int num_voti;
} Studente;

float calcola_media(Studente s) {
    float somma = 0;
    for (int i = 0; i < s.num_voti; i++)
        somma += s.voti[i];
    return (s.num_voti > 0) ? somma / s.num_voti : 0;
}

void stampa_studente(Studente s) {
    printf("%-20s  voti: ", s.nome);
    for (int i = 0; i < s.num_voti; i++)
        printf("%d ", s.voti[i]);
    printf(" → media: %.1f\n", calcola_media(s));
}

int main() {
    Studente classe[3] = {
        {"Anna Rossi",   {28, 30, 27, 29, 30}, 5},
        {"Luca Bianchi", {22, 25, 24},          3},
        {"Sara Conti",   {30, 28, 29, 27},      4}
    };

    printf("=== Registro della classe ===\n");
    for (int i = 0; i < 3; i++)
        stampa_studente(classe[i]);

    int idx_max = 0;
    for (int i = 1; i < 3; i++)
        if (calcola_media(classe[i]) > calcola_media(classe[idx_max]))
            idx_max = i;

    printf("\nMiglior studente: %s (media %.1f)\n",
           classe[idx_max].nome, calcola_media(classe[idx_max]));

    return 0;
}
```

**Output atteso:**
```
=== Registro della classe ===
Anna Rossi            voti: 28 30 27 29 30  → media: 28.8
Luca Bianchi          voti: 22 25 24        → media: 23.7
Sara Conti            voti: 30 28 29 27     → media: 28.5

Miglior studente: Anna Rossi (media 28.8)
```

---

### 1.4 Riepilogo visivo

```
┌──────────────────────────────────────────────────────────────────┐
│                   SINTASSI DELLE STRUCT                          │
├──────────────────────────────────────────────────────────────────┤
│  DEFINIZIONE (con typedef):                                      │
│  typedef struct {                                                │
│      tipo1 campo1;                                               │
│      tipo2 campo2;                                               │
│  } NomeTipo;                                                     │
│                                                                  │
│  DICHIARAZIONE:                                                  │
│  NomeTipo var;                                                   │
│  NomeTipo var = {val1, val2};   /* inizializzazione */          │
│  NomeTipo arr[N];               /* array di struct */            │
│                                                                  │
│  ACCESSO:                                                        │
│  var.campo        /* variabile singola */                        │
│  arr[i].campo     /* elemento di array */                        │
│                                                                  │
│  ASSEGNAZIONE:                                                   │
│  var2 = var1;     /* copia tutti i campi ✅ */                   │
│                                                                  │
│  SCAMBIO (Bubble Sort):                                          │
│  NomeTipo temp = arr[j];                                         │
│  arr[j]        = arr[j+1];                                       │
│  arr[j+1]      = temp;                                           │
└──────────────────────────────────────────────────────────────────┘

CONFRONTO: ARRAY PARALLELI vs STRUCT
──────────────────────────────────────────────────────────────────
  PRIMA (G13 — array paralleli):     ORA (G14 — struct):
  char nomi[10][30];                 typedef struct {
  char tel[10][16];                      char nome[30];
                                         char tel[16];
  Scambio: 6 strcpy!                 } Contatto;
  strcpy(tempN, nomi[j]);            Contatto rubrica[10];
  strcpy(nomi[j], nomi[j+1]);
  strcpy(nomi[j+1], tempN);          Scambio: 3 righe!
  strcpy(tempT, tel[j]);             Contatto t = rubrica[j];
  strcpy(tel[j], tel[j+1]);          rubrica[j] = rubrica[j+1];
  strcpy(tel[j+1], tempT);           rubrica[j+1] = t;

ERRORI FREQUENTI
──────────────────────────────────────────────────────────────────
  ❌  s.nome = "Mario"       ✅  strcpy(s.nome, "Mario")
  ❌  s1 == s2               ✅  confronta campo per campo
  ❌  printf("%s", s)        ✅  printf("%s", s.nome)
  ✅  s2 = s1  (copia intera struct — funziona!)
```

---

### 1.5 Domande di verifica orale

**D1:** Cos'è una `struct` in C? Cosa si intende per "campo"?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Una `struct` è un tipo di dato composto definito dal programmatore che raggruppa variabili di tipo anche diverso in un'unica entità. Le singole variabili che la compongono si chiamano **campi** (o membri). Esempio: una struct `Studente` può avere i campi `nome` (stringa), `matricola` (intero) e `media` (float).

</details>

---

**D2:** Qual è la differenza tra la *definizione* di una struct e la *dichiarazione* di una variabile struct?

<details>
<summary><b>💡 RISPOSTA</b></summary>

La **definizione** (`typedef struct { ... } Nome;`) descrive al compilatore come è fatto il tipo — non alloca memoria. La **dichiarazione** (`Nome var;`) crea una variabile di quel tipo e alloca la memoria necessaria. È la stessa distinzione che esiste tra il progetto di una casa (definizione) e la costruzione effettiva (dichiarazione).

</details>

---

**D3:** Come si accede al campo `prezzo` della terza struct in un array `Prodotto magazzino[10]`?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Con `magazzino[2].prezzo`. Si usa la notazione `array[indice].campo`: prima l'indice per selezionare l'elemento dell'array, poi il punto per accedere al campo desiderato.

</details>

---

**D4:** Perché l'assegnazione `s2 = s1` funziona per le struct ma NON per gli array?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Per le struct, il compilatore sa esattamente quanta memoria occupa il tipo e genera automaticamente il codice per copiare campo per campo. Per gli array, il nome è un puntatore al primo elemento e `=` copierebbe solo l'indirizzo, non il contenuto. Questa è una delle differenze fondamentali tra struct e array in C.

</details>

---

**D5:** Nel Bubble Sort applicato a un array di struct, come si esegue lo scambio?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Grazie all'assegnazione diretta tra struct, lo scambio si riduce a tre righe con una variabile temporanea dello stesso tipo:
```c
NomeTipo temp = arr[j];
arr[j]        = arr[j+1];
arr[j+1]      = temp;
```
Questo copia automaticamente **tutti i campi** in una sola operazione — molto più semplice dei 6 `strcpy` necessari con gli array paralleli.

</details>

---

**D6:** Ho una struct `Studente` con un campo `char nome[50]`. Perché devo usare `strcpy(s.nome, "Mario")` e non `s.nome = "Mario"`?

<details>
<summary><b>💡 RISPOSTA</b></summary>

Il campo `nome` è un array di `char`. Come per tutti gli array in C, non si può assegnare direttamente con `=` (copierebbe solo il puntatore). Si deve usare `strcpy` per copiare i caratteri uno ad uno. Questa regola vale per tutti i campi di tipo array all'interno di una struct, mentre per campi di tipo semplice (`int`, `float`, `char`) si usa normalmente `=`.

</details>

---

**D7:** Cosa significa `typedef` applicato a una struct? Quale vantaggio offre?

<details>
<summary><b>💡 RISPOSTA</b></summary>

`typedef` crea un **alias** — un nome alternativo per un tipo già esistente. Applicato a una struct, permette di evitare di scrivere la parola chiave `struct` ogni volta: invece di `struct Studente s1;` si scrive semplicemente `Studente s1;`. Il codice diventa più leggibile e manutenibile, e il nome del tipo si comporta esattamente come i tipi primitivi (`int`, `float`, ecc.).

</details>

---

## PARTE 2 — ESERCIZI (1 ora)

---

### 🟢 Esercizio 1 — Struct Libro (Base)

**Testo:** Definisci una struct `Libro` con i campi: `titolo` (stringa, max 60 caratteri), `autore` (stringa, max 40 caratteri), `anno` (intero), `prezzo` (float). Scrivi un programma che:
1. Dichiara e inizializza manualmente nel codice 3 libri
2. Li stampa in formato tabellare

**Esempio input/output:**
```
=== Catalogo Libri ===
TITOLO                          AUTORE                   ANNO   PREZZO
Il nome della rosa              Umberto Eco              1980   €12.50
1984                            George Orwell            1949    €9.90
Il Signore degli Anelli         J.R.R. Tolkien           1954   €24.00
```

**💡 Hint:**
1. Usa `typedef struct { ... } Libro;`
2. Inizializza con `Libro libri[3] = { {"titolo", "autore", anno, prezzo}, ... };`
3. Per la stampa allineata usa `%-30s` per le stringhe e `%6.2f` per i float

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

typedef struct {
    char titolo[61];
    char autore[41];
    int  anno;
    float prezzo;
} Libro;

void stampa_libro(Libro l) {
    printf("%-32s %-25s %4d  €%6.2f\n",
           l.titolo, l.autore, l.anno, l.prezzo);
}

int main() {
    Libro libri[3] = {
        {"Il nome della rosa",        "Umberto Eco",      1980, 12.50},
        {"1984",                      "George Orwell",    1949,  9.90},
        {"Il Signore degli Anelli",   "J.R.R. Tolkien",  1954, 24.00}
    };

    printf("=== Catalogo Libri ===\n");
    printf("%-32s %-25s %4s  %6s\n",
           "TITOLO", "AUTORE", "ANNO", "PREZZO");

    for (int i = 0; i < 3; i++)
        stampa_libro(libri[i]);

    return 0;
}
```

</details>

---

### 🟡 Esercizio 2 — Registro studenti con ordinamento (Intermedio)

**Testo:** Scrivi un programma che:
1. Legge da tastiera N studenti (max 20), ciascuno con: cognome (max 30 char), nome (max 30 char), voto (intero 18–30)
2. Ordina gli studenti per voto **decrescente** usando il Bubble Sort
3. Stampa il registro ordinato con posizione, cognome, nome e voto
4. Stampa il voto più alto, il più basso e la media della classe

**Esempio input/output:**
```
Quanti studenti? 4
...

=== Registro (ordinato per voto) ===
 1. Bianchi Anna           30
 2. Conti Sara             28
 3. Rossi Luca             27
 4. Verdi Marco            24

Voto massimo: 30 | Voto minimo: 24 | Media: 27.25
```

**💡 Hint:**
1. Definisci `typedef struct { char cognome[31]; char nome[31]; int voto; } Studente;`
2. Per ordinamento decrescente: `if (classe[j].voto < classe[j+1].voto)` → scambia
3. Lo scambio è `Studente temp = classe[j]; classe[j] = classe[j+1]; classe[j+1] = temp;`
4. Per la media, somma tutti i voti e dividi per n (usa `float`)

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <string.h>

#define MAX 20

typedef struct {
    char cognome[31];
    char nome[31];
    int  voto;
} Studente;

int main() {
    Studente classe[MAX];
    int n, i, j;

    printf("Quanti studenti? ");
    scanf("%d", &n);
    getchar();
    if (n > MAX) n = MAX;

    for (i = 0; i < n; i++) {
        printf("Cognome: ");
        fgets(classe[i].cognome, sizeof(classe[i].cognome), stdin);
        if (classe[i].cognome[strlen(classe[i].cognome)-1] == '\n')
            classe[i].cognome[strlen(classe[i].cognome)-1] = '\0';

        printf("Nome: ");
        fgets(classe[i].nome, sizeof(classe[i].nome), stdin);
        if (classe[i].nome[strlen(classe[i].nome)-1] == '\n')
            classe[i].nome[strlen(classe[i].nome)-1] = '\0';

        printf("Voto: ");
        scanf("%d", &classe[i].voto);
        getchar();
    }

    for (i = 0; i < n - 1; i++) {
        for (j = 0; j < n - 1 - i; j++) {
            if (classe[j].voto < classe[j+1].voto) {
                Studente temp = classe[j];
                classe[j]     = classe[j+1];
                classe[j+1]   = temp;
            }
        }
    }

    printf("\n=== Registro (ordinato per voto) ===\n");
    for (i = 0; i < n; i++)
        printf("%2d. %-15s %-15s  %d\n",
               i+1, classe[i].cognome, classe[i].nome, classe[i].voto);

    int max = classe[0].voto, min = classe[n-1].voto;
    float somma = 0;
    for (i = 0; i < n; i++) somma += classe[i].voto;

    printf("\nVoto massimo: %d | Voto minimo: %d | Media: %.2f\n",
           max, min, somma / n);

    return 0;
}
```

</details>

---

### 🔴 Esercizio 3 — Gestione magazzino (Avanzato)

**Testo:** Scrivi un programma per la gestione di un magazzino con al massimo 15 prodotti. Ogni prodotto ha: `codice` (stringa max 10 char), `descrizione` (stringa max 40 char), `prezzo` (float), `quantita` (intero). Il programma deve:
1. Leggere N prodotti da tastiera
2. Calcolare e stampare il **valore totale** di ogni prodotto (prezzo × quantità)
3. Trovare e stampare il prodotto con il **valore totale più alto**
4. Ordinare i prodotti per **valore totale decrescente** e stampare il magazzino
5. Segnalare tutti i prodotti con quantità ≤ 2 (scorte critiche)

**Esempio input/output:**
```
=== Magazzino ordinato per valore ===
COD    DESCRIZIONE                    PREZZO   QTY   VALORE TOT
P001   Monitor 24"                   €189.00     5   €  945.00
P002   Mouse wireless                € 22.50    15   €  337.50
P003   Tastiera USB                  € 45.90     2   €   91.80

Prodotto di maggior valore: Monitor 24" (€945.00)

⚠ Scorte critiche (qty <= 2):
  [P003] Tastiera USB — qty: 2
```

**💡 Hint:**
1. Definisci la struct con i 4 campi; calcola il valore come `p.prezzo * p.quantita` al momento della stampa
2. Per trovare il massimo, usa `idx_max = 0` e aggiorna confrontando il valore dei prodotti
3. Per l'ordinamento, confronta `magazzino[j].prezzo * magazzino[j].quantita`
4. Per le scorte critiche, un ciclo `for` con `if (magazzino[i].quantita <= 2)`

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <string.h>

#define MAX 15

typedef struct {
    char codice[11];
    char descrizione[41];
    float prezzo;
    int   quantita;
} Prodotto;

float valore(Prodotto p) {
    return p.prezzo * p.quantita;
}

void stampa_prodotto(Prodotto p) {
    printf("%-6s %-30s €%7.2f  %4d  €%8.2f\n",
           p.codice, p.descrizione,
           p.prezzo, p.quantita, valore(p));
}

int main() {
    Prodotto magazzino[MAX];
    int n, i, j;

    printf("Quanti prodotti? ");
    scanf("%d", &n);
    getchar();
    if (n > MAX) n = MAX;

    for (i = 0; i < n; i++) {
        printf("\nCodice: ");
        fgets(magazzino[i].codice, sizeof(magazzino[i].codice), stdin);
        if (magazzino[i].codice[strlen(magazzino[i].codice)-1] == '\n')
            magazzino[i].codice[strlen(magazzino[i].codice)-1] = '\0';

        printf("Descrizione: ");
        fgets(magazzino[i].descrizione, sizeof(magazzino[i].descrizione), stdin);
        if (magazzino[i].descrizione[strlen(magazzino[i].descrizione)-1] == '\n')
            magazzino[i].descrizione[strlen(magazzino[i].descrizione)-1] = '\0';

        printf("Prezzo: ");
        scanf("%f", &magazzino[i].prezzo);
        printf("Quantita': ");
        scanf("%d", &magazzino[i].quantita);
        getchar();
    }

    for (i = 0; i < n - 1; i++) {
        for (j = 0; j < n - 1 - i; j++) {
            if (valore(magazzino[j]) < valore(magazzino[j+1])) {
                Prodotto temp  = magazzino[j];
                magazzino[j]   = magazzino[j+1];
                magazzino[j+1] = temp;
            }
        }
    }

    printf("\n=== Magazzino ordinato per valore ===\n");
    printf("%-6s %-30s %7s  %4s  %9s\n",
           "COD", "DESCRIZIONE", "PREZZO", "QTY", "VALORE TOT");
    for (i = 0; i < n; i++)
        stampa_prodotto(magazzino[i]);

    printf("\nProdotto di maggior valore: %s (€%.2f)\n",
           magazzino[0].descrizione, valore(magazzino[0]));

    int critici = 0;
    for (i = 0; i < n; i++) {
        if (magazzino[i].quantita <= 2) {
            if (!critici) printf("\n⚠ Scorte critiche (qty <= 2):\n");
            printf("  [%s] %s — qty: %d\n",
                   magazzino[i].codice,
                   magazzino[i].descrizione,
                   magazzino[i].quantita);
            critici++;
        }
    }
    if (!critici)
        printf("\nNessuna scorta critica.\n");

    return 0;
}
```

</details>

---

## 🎯 Recap finale (5 min)

- **Una `struct` raggruppa dati di tipo diverso** in un'unica variabile composita — nome, telefono, prezzo e quantità viaggiano sempre insieme, eliminando il rischio di disallineamento degli array paralleli.
- **L'operatore `.` accede ai campi**: `variabile.campo` per variabili singole, `array[i].campo` per array di struct.
- **L'assegnazione `=` funziona tra struct**: copia automaticamente tutti i campi — questo rende lo scambio nel Bubble Sort semplicissimo (3 righe con una variabile temporanea dello stesso tipo).
- **`typedef struct { ... } Nome;`** crea un alias che elimina la parola chiave `struct` dalla dichiarazione delle variabili, rendendo il codice più leggibile.
- ⚠️ **Errore comune da evitare:** usare `s.nome = "testo"` per i campi di tipo stringa — i campi array all'interno di una struct seguono le stesse regole degli array normali: si deve usare `strcpy(s.nome, "testo")`.
- 📌 **Prossima lezione (G15):** approfondimento delle struct in un contesto progettuale più ampio — introduzione al progetto Faber, dove i concetti di oggi verranno applicati a un problema reale.
