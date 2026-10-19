# Lezione G16: Strutture e Gestione File — Lettura e Scrittura su File

**Durata totale:** 4 ore
**Teoria:** 3 ore | **Esercizi:** 1 ora
**Data:** _______________
**Ambiente:** CLion (JetBrains)
**Giornata:** G16 di 19 — Ore corso: 64/76

---

# PARTE 1 — TEORIA (3 ore)

## 1.1 Introduzione e Motivazione

Finora tutti i dati del nostro programma esistono soltanto mentre il programma è in esecuzione: appena termina, ogni array, ogni struct, ogni variabile scompare. Immagina un programma gestionale per una piccola biblioteca: se alla chiusura del programma l'elenco dei libri viene perso, il sistema è inutilizzabile.

La **gestione dei file** risolve questo problema: permette di salvare dati su disco e rileggerne ad ogni avvio, rendendo i programmi **persistenti**.

Combinando `struct` (già note da G14–G15) con la lettura/scrittura su file otteniamo uno degli strumenti più potenti del C standard: la capacità di costruire archivi dati rudimentali, simili a un database minimo.

---

## 1.2 Spiegazione dell'Argomento

### 1.2.1 Il tipo `FILE` e le funzioni principali

In C la gestione dei file avviene tramite un **puntatore a FILE**:

```c
FILE *fp;
```

`FILE` è un tipo definito in `<stdio.h>`. Il puntatore `fp` non punta direttamente al file su disco, ma a una struttura interna che gestisce il buffer e lo stato del file.

**Apertura e chiusura:**

```
fopen(nome_file, modalità)  →  restituisce FILE* oppure NULL se errore
fclose(fp)                  →  chiude il file e svuota il buffer
```

**Modalità di apertura:**

```
┌──────┬──────────────────────────────────────────────────────────┐
│ Modo │ Significato                                              │
├──────┼──────────────────────────────────────────────────────────┤
│ "r"  │ Lettura — il file deve esistere                          │
│ "w"  │ Scrittura — crea nuovo o svuota se esiste               │
│ "a"  │ Append — aggiunge in fondo, crea se non esiste           │
│ "rb" │ Lettura binaria                                          │
│ "wb" │ Scrittura binaria                                        │
│ "ab" │ Append binario                                           │
└──────┴──────────────────────────────────────────────────────────┘
```

### 1.2.2 File di testo vs file binari

**File di testo:** i dati vengono salvati come caratteri leggibili. Un intero `42` viene scritto come due byte: `'4'` e `'2'`. Utile per file leggibili con un editor.

**File binari:** i dati vengono scritti esattamente come sono in memoria. Un intero `42` occupa 4 byte (la sua rappresentazione binaria). Più compatti e veloci, ma non leggibili direttamente.

```
Valore int: 42

Testo:   [ '4' ][ '2' ][ '\n' ]   → 3 byte
Binario: [ 0x00 ][ 0x00 ][ 0x00 ][ 0x2A ]  → 4 byte (big-endian)
```

### 1.2.3 Operazioni su file di testo

**Scrittura con `fprintf`:**
```c
fprintf(fp, formato, argomenti);
// Esattamente come printf, ma scrive su file
```

**Lettura con `fscanf`:**
```c
fscanf(fp, formato, &variabile);
// Esattamente come scanf, ma legge da file
// Restituisce il numero di valori letti (utile per rilevare EOF)
```

**Lettura/scrittura di righe con `fgets` / `fputs`:**
```c
fgets(buffer, dimensione, fp);   // legge una riga (include '\n')
fputs(stringa, fp);              // scrive una stringa (senza '\n' automatico)
```

**Rilevamento fine file:**
```c
while (fscanf(fp, ...) == n_campi) { ... }  // preferibile
```

### 1.2.4 Operazioni su file binari: `fwrite` e `fread`

```c
fwrite(ptr, dim_elemento, n_elementi, fp);
fread(ptr, dim_elemento, n_elementi, fp);
```

Entrambe restituiscono il numero di elementi effettivamente scritti/letti.

**Esempio concettuale:**
```
struct Libro libro = {"Il nome della rosa", "Eco", 1980};

fwrite(&libro, sizeof(struct Libro), 1, fp);
         │          │                │
         │          │                └── quanti elementi
         │          └─────────────────── dimensione di ciascuno
         └────────────────────────────── indirizzo da cui leggere
```

### 1.2.5 Salvataggio e caricamento di array di struct

```
SALVATAGGIO                        CARICAMENTO
──────────                         ───────────
apri file in "wb"                  apri file in "rb"
fwrite(array, sizeof(T), n, fp)    n = fread(array, sizeof(T), MAX, fp)
chiudi file                        chiudi file
                                   usa n come dimensione effettiva
```

### 1.2.6 Schema generale del flusso

```
PROGRAMMA
   │
   ├─► fopen("dati.bin", "wb") ──────────────────────────────────────►  FILE SU DISCO
   │         │                                                              dati.bin
   │    fwrite(&struct, sizeof, n, fp)  ────────────────────────────►   [raw bytes...]
   │         │
   │    fclose(fp)
   │
   └─► fopen("dati.bin", "rb") ──────────────────────────────────────►  FILE SU DISCO
             │                                                              dati.bin
        fread(&struct, sizeof, MAX, fp) ◄──────────────────────────────  [raw bytes...]
             │
        fclose(fp)
             │
        usa i dati in memoria
```

### 1.2.7 Controllo errori — sempre obbligatorio

```c
FILE *fp = fopen("archivio.bin", "rb");
if (fp == NULL) {
    printf("Errore: impossibile aprire il file.\n");
    return 1;
}
```

---

## 1.3 Esempi di Codice Commentati

### Esempio 1 — Scrittura e lettura di testo con struct

```c
#include <stdio.h>
#include <string.h>

struct Studente {
    char nome[50];
    int  voto;
};

int main() {
    FILE *fp = fopen("studenti.txt", "w");
    if (fp == NULL) {
        printf("Errore apertura file in scrittura.\n");
        return 1;
    }

    struct Studente lista[3] = {
        {"Alice",  28},
        {"Bruno",  25},
        {"Carla",  30}
    };

    for (int i = 0; i < 3; i++) {
        fprintf(fp, "%s %d\n", lista[i].nome, lista[i].voto);
    }
    fclose(fp);
    printf("Scrittura completata.\n");

    fp = fopen("studenti.txt", "r");
    if (fp == NULL) {
        printf("Errore apertura file in lettura.\n");
        return 1;
    }

    struct Studente letto;
    printf("\nContenuto del file:\n");
    while (fscanf(fp, "%49s %d", letto.nome, &letto.voto) == 2) {
        printf("Nome: %-15s  Voto: %d\n", letto.nome, letto.voto);
    }
    fclose(fp);

    return 0;
}
```

**Output atteso:**
```
Scrittura completata.

Contenuto del file:
Nome: Alice            Voto: 28
Nome: Bruno            Voto: 25
Nome: Carla            Voto: 30
```

---

### Esempio 2 — Scrittura e lettura binaria di un array di struct

```c
#include <stdio.h>

#define MAX 100

struct Prodotto {
    char  nome[40];
    float prezzo;
    int   quantita;
};

void salva(struct Prodotto arr[], int n, const char *nome_file) {
    FILE *fp = fopen(nome_file, "wb");
    if (fp == NULL) { printf("Errore.\n"); return; }
    fwrite(&n, sizeof(int), 1, fp);
    fwrite(arr, sizeof(struct Prodotto), n, fp);
    fclose(fp);
    printf("Salvati %d prodotti.\n", n);
}

int carica(struct Prodotto arr[], const char *nome_file) {
    FILE *fp = fopen(nome_file, "rb");
    if (fp == NULL) { printf("File non trovato, archivio vuoto.\n"); return 0; }
    int n = 0;
    fread(&n, sizeof(int), 1, fp);
    fread(arr, sizeof(struct Prodotto), n, fp);
    fclose(fp);
    printf("Caricati %d prodotti.\n", n);
    return n;
}

int main() {
    struct Prodotto magazzino[MAX];
    int n = carica(magazzino, "magazzino.bin");

    struct Prodotto nuovo = {"Tastiera meccanica", 89.99f, 15};
    magazzino[n++] = nuovo;
    salva(magazzino, n, "magazzino.bin");

    printf("\n--- Inventario ---\n");
    for (int i = 0; i < n; i++) {
        printf("%-25s  €%.2f  qty:%d\n",
               magazzino[i].nome, magazzino[i].prezzo, magazzino[i].quantita);
    }
    return 0;
}
```

**Output atteso (prima esecuzione):**
```
File non trovato, archivio vuoto.
Salvati 1 prodotti.

--- Inventario ---
Tastiera meccanica         €89.99  qty:15
```

---

### Esempio 3 — Append su file di testo (log eventi)

```c
#include <stdio.h>
#include <time.h>

void registra_evento(const char *messaggio) {
    FILE *fp = fopen("log.txt", "a");
    if (fp == NULL) return;
    time_t ora = time(NULL);
    char timestamp[30];
    strftime(timestamp, sizeof(timestamp), "%Y-%m-%d %H:%M:%S", localtime(&ora));
    fprintf(fp, "[%s] %s\n", timestamp, messaggio);
    fclose(fp);
}

int main() {
    registra_evento("Programma avviato");
    registra_evento("Utente connesso: admin");
    registra_evento("Operazione completata");
    registra_evento("Programma terminato");

    printf("Log aggiornato. Contenuto:\n\n");
    FILE *fp = fopen("log.txt", "r");
    if (fp == NULL) return 1;
    char riga[200];
    while (fgets(riga, sizeof(riga), fp)) printf("%s", riga);
    fclose(fp);
    return 0;
}
```

**Output atteso (esempio):**
```
Log aggiornato. Contenuto:

[2025-03-15 10:23:41] Programma avviato
[2025-03-15 10:23:41] Utente connesso: admin
[2025-03-15 10:23:41] Operazione completata
[2025-03-15 10:23:41] Programma terminato
```

---

## 1.4 Riepilogo Visivo

```
┌─────────────────────────────────────────────────────────────────┐
│                  GESTIONE FILE IN C — RIEPILOGO                 │
├──────────────┬──────────────────────┬───────────────────────────┤
│ OPERAZIONE   │ TESTO                │ BINARIO                   │
├──────────────┼──────────────────────┼───────────────────────────┤
│ Apertura     │ fopen("f","r"/"w")   │ fopen("f","rb"/"wb")      │
│ Scrittura    │ fprintf(fp,fmt,...)  │ fwrite(&var,sz,n,fp)      │
│ Lettura      │ fscanf(fp,fmt,...)   │ fread(&var,sz,n,fp)       │
│ Riga intera  │ fgets / fputs        │ —                         │
│ Chiusura     │ fclose(fp)           │ fclose(fp)                │
├──────────────┼──────────────────────┼───────────────────────────┤
│ PRO          │ Leggibile con editor │ Compatto, veloce, preciso │
│ CONTRO       │ Parsing complesso    │ Non leggibile a occhio    │
└──────────────┴──────────────────────┴───────────────────────────┘

MODALITÀ fopen:
  "r"  solo lettura (file deve esistere)
  "w"  scrittura (sovrascrive o crea)
  "a"  append (aggiunge in fondo o crea)
  +b   versione binaria di ognuna

SEMPRE: controllare che fopen non restituisca NULL!
```

---

## 1.5 Domande di Verifica Orale

**D1:** Cosa succede se chiami `fopen("dati.txt", "w")` su un file che esiste già?

**D2:** Qual è la differenza tra `fprintf` e `fwrite`?

**D3:** Perché è importante chiamare `fclose` dopo aver finito di usare un file?

**D4:** Come si riconosce la fine di un file durante la lettura con `fscanf`?

**D5:** Qual è il vantaggio di salvare un array di struct con un singolo `fwrite` invece di un ciclo con `fprintf`?

**D6:** Cosa stampa `fopen` se il file non esiste e si apre in modalità `"r"`?

**D7:** Se salvo una struct con `fwrite` su un computer e provo a leggerla con `fread` su un altro, è garantito che funzioni?

---

# PARTE 2 — ESERCIZI (1 ora)

## 🟢 Esercizio 1 — Livello Base: Rubrica Telefonica su File di Testo

**Testo:**
Scrivi un programma che definisce una struct `Contatto` con campi `nome` (stringa, max 30 car.), `cognome` (stringa, max 30 car.) e `telefono` (stringa, max 15 car.). Il programma deve:
1. Creare un array di 3 contatti inseriti direttamente nel codice (hardcoded)
2. Salvarli su un file di testo `rubrica.txt`, uno per riga nel formato: `nome cognome telefono`
3. Rileggere il file e stampare a schermo i contatti letti

**Esempio input/output:**
```
Scrittura completata: 3 contatti salvati.

Lettura da file:
Mario Rossi 3331234567
Anna Bianchi 3479876543
Luca Verdi 3201112233
```

---

## 🟡 Esercizio 2 — Livello Intermedio: Archivio Libri Binario

**Testo:**
Crea un programma per gestire un piccolo archivio di libri. La struct `Libro` ha: `titolo` (60 car.), `autore` (40 car.), `anno` (int), `prezzo` (float). Il programma deve:
1. Definire un array di 4 libri con valori a piacere
2. Salvarlo in un file binario `libri.bin` (scrivi prima il numero di libri, poi l'array)
3. Ricaricare il file in un nuovo array e stampare tutti i libri con formattazione tabellare
4. Calcolare e stampare il prezzo medio

**Esempio input/output:**
```
Salvati 4 libri in libri.bin.

--- ARCHIVIO LIBRI ---
Titolo                        Autore              Anno    Prezzo
Il nome della rosa            Umberto Eco         1980    €12.50
1984                          George Orwell       1949    €8.90
Il Signore degli Anelli       J.R.R. Tolkien      1954    €18.00
Fondazione                    Isaac Asimov        1951    €10.00

Prezzo medio: €12.35
```

---

## 🔴 Esercizio 3 — Livello Avanzato: Gestionale Studenti con Menu

**Testo:**
Realizza un programma completo con menu interattivo per gestire un archivio studenti persistente. La struct `Studente` ha: `matricola` (int), `nome` (40 car.), `cognome` (40 car.), `voto_medio` (float). Il file si chiama `studenti.bin`. Il menu deve offrire:
1. Visualizza tutti gli studenti
2. Aggiungi uno studente
3. Salva archivio su file
4. Cerca studente per matricola
0. Esci (con salvataggio automatico)

Il programma deve caricare automaticamente l'archivio all'avvio.

**Esempio input/output:**
```
=== GESTIONALE STUDENTI ===
Caricati 2 studenti da file.

1. Visualizza studenti
2. Aggiungi studente
3. Salva su file
4. Cerca per matricola
0. Esci
Scelta: 2

Matricola: 1003
Nome: Carlo
Cognome: Neri
Voto medio: 27.5
Studente aggiunto.

Scelta: 0
Salvati 3 studenti. Arrivederci!
```

---

# PARTE 3 — RECAP FINALE (5 min)

## 🎯 Recap finale (5 min)

- **File e persistenza:** i file permettono di conservare i dati tra un'esecuzione e l'altra del programma, salvandoli su disco tramite `fopen`, `fwrite`/`fprintf` e `fclose`.
- **Testo vs binario:** i file di testo usano `fprintf`/`fscanf` e sono leggibili con un editor; i file binari usano `fwrite`/`fread` e salvano i byte grezzi della memoria — più veloci e compatti.
- **Array di struct su file:** il pattern `fwrite(&n, ...) + fwrite(array, ...)` / `fread(&n, ...) + fread(array, ...)` è il modo standard per salvare e ricaricare interi archivi in C.
- **Controllo errori:** `fopen` restituisce `NULL` in caso di errore — controllare sempre prima di usare il puntatore al file.
- ⚠️ **Errore comune da evitare:** dimenticare `fclose()`. Dati scritti con `fprintf`/`fwrite` possono restare nel buffer interno e non essere scritti su disco se il file non viene chiuso correttamente.
- ➡️ **Prossima lezione (G17):** Esercitazione riepilogativa parte 1 — ripasseremo struct, array, funzioni e file combinando tutto in un mini-progetto guidato.
