# ESERCIZI - PUNTATORI IN C

### TEMPO STIMATO: 3 ore (15 esercizi + bonus)

---

**DISTRIBUZIONE CONSIGLIATA:**
- Esercizi 1-5: Basi puntatori (50 min)
- Esercizi 6-10: Aritmetica e array (60 min)
- Esercizi 11-15: Stringhe e avanzati (70 min)

---

## PARTE 1: BASI DEI PUNTATORI

## Esercizio 1: Primo Contatto con i Puntatori (15 min)

Scrivi un programma che:
1. Dichiara una variabile `int x = 42`
2. Dichiara un puntatore `int* p` che punta a `x`
3. Stampa:
   - Valore di `x`
   - Indirizzo di `x` (`&x`)
   - Valore di `p` (dovrebbe essere uguale a `&x`)
   - Valore puntato da `p` (`*p`)
   - Indirizzo di `p` (`&p`)
4. Modifica il valore di `x` attraverso il puntatore: `*p = 100`
5. Ristampa `x` e `*p`

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

int main() {
    int x = 42;
    int* p;
    
    p = &x;  // p ora punta a x
    
    printf("=== INFORMAZIONI INIZIALI ===\n");
    printf("Valore di x: %d\n", x);
    printf("Indirizzo di x (&x): %p\n", &x);
    printf("\n");
    printf("Valore di p: %p\n", p);
    printf("Valore puntato da p (*p): %d\n", *p);
    printf("Indirizzo di p (&p): %p\n", &p);
    printf("\n");
    
    // Verifica che p contenga l'indirizzo di x
    if (p == &x) {
        printf("✓ Il puntatore p punta correttamente a x\n\n");
    }
    
    // Modifica attraverso il puntatore
    printf("=== MODIFICA ATTRAVERSO PUNTATORE ===\n");
    printf("Eseguo: *p = 100\n\n");
    *p = 100;
    
    printf("Valore di x: %d\n", x);
    printf("Valore puntato da p (*p): %d\n", *p);
    
    return 0;
}
```

**Output:**
```
=== INFORMAZIONI INIZIALI ===
Valore di x: 42
Indirizzo di x (&x): 0x7fff5fbff73c

Valore di p: 0x7fff5fbff73c
Valore puntato da p (*p): 42
Indirizzo di p (&p): 0x7fff5fbff740

✓ Il puntatore p punta correttamente a x

=== MODIFICA ATTRAVERSO PUNTATORE ===
Eseguo: *p = 100

Valore di x: 100
Valore puntato da p (*p): 100
```

</details>

---

## Esercizio 2: Swap con Puntatori (15 min)

Implementa due versioni della funzione swap:
1. **swapSbagliato(int a, int b)** — passaggio per valore (non funziona)
2. **swap(int* a, int* b)** — passaggio per riferimento (funziona)

Testa entrambe e spiega perché solo la seconda funziona.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

// Versione SBAGLIATA: passaggio per valore
void swapSbagliato(int a, int b) {
    int temp = a;
    a = b;
    b = temp;
    printf("  Dentro swapSbagliato: a=%d, b=%d\n", a, b);
}

// Versione CORRETTA: passaggio per riferimento
void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
    printf("  Dentro swap: *a=%d, *b=%d\n", *a, *b);
}

int main() {
    int x = 10, y = 20;
    
    printf("=== TEST SWAP SBAGLIATO ===\n");
    printf("Prima: x=%d, y=%d\n", x, y);
    swapSbagliato(x, y);
    printf("Dopo:  x=%d, y=%d\n", x, y);
    printf("❌ Non funziona! x e y non sono cambiati\n\n");
    
    printf("=== TEST SWAP CORRETTO ===\n");
    printf("Prima: x=%d, y=%d\n", x, y);
    swap(&x, &y);
    printf("Dopo:  x=%d, y=%d\n", x, y);
    printf("✓ Funziona! x e y sono scambiati\n");
    
    return 0;
}
```

**Output:**
```
=== TEST SWAP SBAGLIATO ===
Prima: x=10, y=20
  Dentro swapSbagliato: a=20, b=10
Dopo:  x=10, y=20
❌ Non funziona! x e y non sono cambiati

=== TEST SWAP CORRETTO ===
Prima: x=10, y=20
  Dentro swap: *a=20, *b=10
Dopo:  x=20, y=10
✓ Funziona! x e y sono scambiati
```

**Spiegazione:**
- `swapSbagliato` riceve COPIE dei valori → scambia le copie, non gli originali
- `swap` riceve gli INDIRIZZI → può modificare direttamente gli originali

</details>

---

## Esercizio 3: Multipli Valori di Ritorno (20 min)

Implementa `void statistiche(int arr[], int dim, int* somma, float* media, int* max, int* min)` che calcola tutte le statistiche di un array usando puntatori per "tornare" i valori.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

void statistiche(int arr[], int dim, int* somma, float* media, int* max, int* min) {
    *somma = 0;
    *max = arr[0];
    *min = arr[0];
    
    for (int i = 0; i < dim; i++) {
        *somma += arr[i];
        if (arr[i] > *max) *max = arr[i];
        if (arr[i] < *min) *min = arr[i];
    }
    
    *media = (float)(*somma) / dim;
}

int main() {
    int array[] = {12, 45, 7, 23, 89, 34, 16};
    int dim = 7;
    
    int somma, max, min;
    float media;
    
    statistiche(array, dim, &somma, &media, &max, &min);
    
    printf("=== STATISTICHE ARRAY ===\n");
    printf("Array: ");
    for (int i = 0; i < dim; i++) {
        printf("%d ", array[i]);
    }
    printf("\n\n");
    
    printf("Somma:   %d\n", somma);
    printf("Media:   %.2f\n", media);
    printf("Massimo: %d\n", max);
    printf("Minimo:  %d\n", min);
    
    return 0;
}
```

**Output:**
```
=== STATISTICHE ARRAY ===
Array: 12 45 7 23 89 34 16 

Somma:   226
Media:   32.29
Massimo: 89
Minimo:  7
```

</details>

---

## Esercizio 4: Incrementa e Triplo (15 min)

Scrivi due funzioni:
- `void incrementa(int* x)` — incrementa il valore puntato
- `void triplo(int* x)` — moltiplica per 3 il valore puntato

Testa con una variabile che parte da 5.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

void incrementa(int* x) {
    (*x)++;
}

void triplo(int* x) {
    *x = *x * 3;
}

int main() {
    int num = 5;
    
    printf("Valore iniziale: %d\n", num);
    
    incrementa(&num);
    printf("Dopo incrementa: %d\n", num);
    
    incrementa(&num);
    printf("Dopo 2° incrementa: %d\n", num);
    
    triplo(&num);
    printf("Dopo triplo: %d\n", num);
    
    return 0;
}
```

**Output:**
```
Valore iniziale: 5
Dopo incrementa: 6
Dopo 2° incrementa: 7
Dopo triplo: 21
```

</details>

---

## Esercizio 5: Divisione Completa (15 min)

Implementa `void divisioneCompleta(int dividendo, int divisore, int* quoziente, int* resto)` che calcola sia quoziente che resto.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

void divisioneCompleta(int dividendo, int divisore, int* quoziente, int* resto) {
    if (divisore == 0) {
        *quoziente = 0;
        *resto = 0;
        printf("ERRORE: Divisione per zero!\n");
        return;
    }
    
    *quoziente = dividendo / divisore;
    *resto = dividendo % divisore;
}

int main() {
    int q, r;
    
    printf("=== DIVISIONI COMPLETE ===\n\n");
    
    divisioneCompleta(17, 5, &q, &r);
    printf("17 / 5 = %d con resto %d\n\n", q, r);
    
    divisioneCompleta(100, 7, &q, &r);
    printf("100 / 7 = %d con resto %d\n\n", q, r);
    
    divisioneCompleta(50, 10, &q, &r);
    printf("50 / 10 = %d con resto %d\n\n", q, r);
    
    return 0;
}
```

**Output:**
```
=== DIVISIONI COMPLETE ===

17 / 5 = 3 con resto 2

100 / 7 = 14 con resto 2

50 / 10 = 5 con resto 0
```

</details>

---

## PARTE 2: ARITMETICA DEI PUNTATORI E ARRAY

## Esercizio 6: Stampa Array con Puntatori (15 min)

Implementa `void stampaArrayConPuntatori(int* arr, int dim)` che itera l'array usando l'aritmetica dei puntatori (senza indici).

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

void stampaArrayConPuntatori(int* arr, int dim) {
    int* p = arr;
    int* fine = arr + dim;
    
    printf("[ ");
    while (p < fine) {
        printf("%d ", *p);
        p++;
    }
    printf("]\n");
}

int main() {
    int numeri[] = {10, 20, 30, 40, 50, 60, 70};
    int dim = 7;
    
    printf("=== STAMPA CON PUNTATORI ===\n");
    stampaArrayConPuntatori(numeri, dim);
    
    return 0;
}
```

**Output:**
```
=== STAMPA CON PUNTATORI ===
[ 10 20 30 40 50 60 70 ]
```

</details>

---

## Esercizio 7: Somma Array con Puntatori (15 min)

Implementa `int sommaConPuntatori(int* arr, int dim)` usando solo puntatori.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

int sommaConPuntatori(int* arr, int dim) {
    int somma = 0;
    int* p = arr;
    int* fine = arr + dim;
    
    while (p < fine) {
        somma += *p;
        p++;
    }
    
    return somma;
}

int main() {
    int numeri[] = {5, 10, 15, 20, 25};
    int dim = 5;
    
    printf("Array: ");
    for (int i = 0; i < dim; i++) {
        printf("%d ", numeri[i]);
    }
    printf("\n");
    
    int somma = sommaConPuntatori(numeri, dim);
    printf("Somma: %d\n", somma);
    
    return 0;
}
```

**Output:**
```
Array: 5 10 15 20 25 
Somma: 75
```

</details>

---

## Esercizio 8: Trova Massimo con Puntatori (20 min)

Implementa `int* trovaMax(int* arr, int dim)` che ritorna un **puntatore** all'elemento massimo.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

int* trovaMax(int* arr, int dim) {
    int* maxPtr = arr;
    int* p = arr + 1;
    int* fine = arr + dim;
    
    while (p < fine) {
        if (*p > *maxPtr) {
            maxPtr = p;
        }
        p++;
    }
    
    return maxPtr;
}

int main() {
    int numeri[] = {15, 42, 8, 23, 67, 34, 12};
    int dim = 7;
    
    printf("Array: ");
    for (int i = 0; i < dim; i++) {
        printf("%d ", numeri[i]);
    }
    printf("\n");
    
    int* maxPtr = trovaMax(numeri, dim);
    
    printf("Elemento massimo: %d\n", *maxPtr);
    printf("Posizione: %ld\n", maxPtr - numeri);
    
    // Modifico il massimo
    *maxPtr = 100;
    
    printf("\nDopo modifica del massimo a 100:\n");
    printf("Array: ");
    for (int i = 0; i < dim; i++) {
        printf("%d ", numeri[i]);
    }
    printf("\n");
    
    return 0;
}
```

**Output:**
```
Array: 15 42 8 23 67 34 12 
Elemento massimo: 67
Posizione: 4

Dopo modifica del massimo a 100:
Array: 15 42 8 23 100 34 12 
```

</details>

---

## Esercizio 9: Inversione Array con Puntatori (20 min)

Implementa `void invertiConPuntatori(int* arr, int dim)` usando due puntatori (uno all'inizio, uno alla fine).

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

void invertiConPuntatori(int* arr, int dim) {
    int* inizio = arr;
    int* fine = arr + dim - 1;
    
    while (inizio < fine) {
        // Swap
        int temp = *inizio;
        *inizio = *fine;
        *fine = temp;
        
        inizio++;
        fine--;
    }
}

void stampaArray(int* arr, int dim) {
    printf("[ ");
    for (int i = 0; i < dim; i++) {
        printf("%d ", arr[i]);
    }
    printf("]\n");
}

int main() {
    int numeri[] = {10, 20, 30, 40, 50, 60, 70};
    int dim = 7;
    
    printf("Array originale:\n");
    stampaArray(numeri, dim);
    
    invertiConPuntatori(numeri, dim);
    
    printf("Array invertito:\n");
    stampaArray(numeri, dim);
    
    return 0;
}
```

**Output:**
```
Array originale:
[ 10 20 30 40 50 60 70 ]
Array invertito:
[ 70 60 50 40 30 20 10 ]
```

</details>

---

## Esercizio 10: Conta Elementi Maggiori di X (20 min)

Implementa `int contaMaggiori(int* arr, int dim, int soglia)` che conta quanti elementi sono > soglia, usando puntatori.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

int contaMaggiori(int* arr, int dim, int soglia) {
    int conta = 0;
    int* p = arr;
    int* fine = arr + dim;
    
    while (p < fine) {
        if (*p > soglia) {
            conta++;
        }
        p++;
    }
    
    return conta;
}

int main() {
    int numeri[] = {5, 12, 8, 20, 15, 3, 25, 7};
    int dim = 8;
    
    printf("Array: ");
    for (int i = 0; i < dim; i++) {
        printf("%d ", numeri[i]);
    }
    printf("\n\n");
    
    int soglie[] = {10, 15, 20};
    
    for (int i = 0; i < 3; i++) {
        int conta = contaMaggiori(numeri, dim, soglie[i]);
        printf("Elementi > %d: %d\n", soglie[i], conta);
    }
    
    return 0;
}
```

**Output:**
```
Array: 5 12 8 20 15 3 25 7 

Elementi > 10: 4
Elementi > 15: 2
Elementi > 20: 1
```

</details>

---

## PARTE 3: PUNTATORI E STRINGHE

## Esercizio 11: Lunghezza Stringa con Puntatori (15 min)

Implementa `int lunghezza(char* str)` che calcola la lunghezza senza usare `strlen()`.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

int lunghezza(char* str) {
    int len = 0;
    while (*str != '\0') {
        len++;
        str++;
    }
    return len;
}

int main() {
    char* stringhe[] = {
        "Ciao",
        "Programmazione",
        "C",
        "Hello World!"
    };
    
    printf("=== CALCOLO LUNGHEZZE ===\n\n");
    
    for (int i = 0; i < 4; i++) {
        printf("'%s' → lunghezza: %d\n", stringhe[i], lunghezza(stringhe[i]));
    }
    
    return 0;
}
```

**Output:**
```
=== CALCOLO LUNGHEZZE ===

'Ciao' → lunghezza: 4
'Programmazione' → lunghezza: 14
'C' → lunghezza: 1
'Hello World!' → lunghezza: 12
```

</details>

---

## Esercizio 12: Copia Stringa con Puntatori (20 min)

Implementa `void copiaStringa(char* dest, char* src)` senza usare `strcpy()`.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

void copiaStringa(char* dest, char* src) {
    while (*src != '\0') {
        *dest = *src;
        dest++;
        src++;
    }
    *dest = '\0';  // Terminatore
}

// Versione compatta
void copiaStringaCompatta(char* dest, char* src) {
    while ((*dest++ = *src++) != '\0');
}

int main() {
    char originale[] = "Programmazione in C";
    char copia1[100];
    char copia2[100];
    
    copiaStringa(copia1, originale);
    copiaStringaCompatta(copia2, originale);
    
    printf("Originale: '%s'\n", originale);
    printf("Copia 1:   '%s'\n", copia1);
    printf("Copia 2:   '%s'\n", copia2);
    
    return 0;
}
```

**Output:**
```
Originale: 'Programmazione in C'
Copia 1:   'Programmazione in C'
Copia 2:   'Programmazione in C'
```

</details>

---

## Esercizio 13: Confronta Stringhe con Puntatori (20 min)

Implementa `int confrontaStringhe(char* str1, char* str2)` che ritorna:
- 0 se uguali
- valore < 0 se str1 < str2
- valore > 0 se str1 > str2

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

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

int main() {
    char* coppie[][2] = {
        {"Ciao", "Ciao"},
        {"Anna", "Antonio"},
        {"Zebra", "Alpaca"},
        {"ABC", "ABCD"}
    };
    
    printf("=== CONFRONTO STRINGHE ===\n\n");
    
    for (int i = 0; i < 4; i++) {
        int risultato = confrontaStringhe(coppie[i][0], coppie[i][1]);
        
        printf("'%s' vs '%s' → ", coppie[i][0], coppie[i][1]);
        
        if (risultato == 0) {
            printf("UGUALI\n");
        } else if (risultato < 0) {
            printf("'%s' viene PRIMA\n", coppie[i][0]);
        } else {
            printf("'%s' viene DOPO\n", coppie[i][0]);
        }
    }
    
    return 0;
}
```

**Output:**
```
=== CONFRONTO STRINGHE ===

'Ciao' vs 'Ciao' → UGUALI
'Anna' vs 'Antonio' → 'Anna' viene PRIMA
'Zebra' vs 'Alpaca' → 'Zebra' viene DOPO
'ABC' vs 'ABCD' → 'ABC' viene PRIMA
```

</details>

---

## Esercizio 14: Conta Vocali con Puntatori (20 min)

Implementa `int contaVocali(char* str)` che conta le vocali (a, e, i, o, u, maiuscole e minuscole).

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

int contaVocali(char* str) {
    int contatore = 0;
    
    while (*str != '\0') {
        char c = *str;
        
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' ||
            c == 'A' || c == 'E' || c == 'I' || c == 'O' || c == 'U') {
            contatore++;
        }
        
        str++;
    }
    
    return contatore;
}

int main() {
    char* frasi[] = {
        "Ciao mondo",
        "Programmazione in C",
        "AEIOU",
        "xyz"
    };
    
    printf("=== CONTA VOCALI ===\n\n");
    
    for (int i = 0; i < 4; i++) {
        int vocali = contaVocali(frasi[i]);
        printf("'%s' → %d vocali\n", frasi[i], vocali);
    }
    
    return 0;
}
```

**Output:**
```
=== CONTA VOCALI ===

'Ciao mondo' → 4 vocali
'Programmazione in C' → 8 vocali
'AEIOU' → 5 vocali
'xyz' → 0 vocali
```

</details>

---

## Esercizio 15: Maiuscolo/Minuscolo con Puntatori (25 min)

Implementa due funzioni:
- `void maiuscolo(char* str)` — converte in maiuscolo
- `void minuscolo(char* str)` — converte in minuscolo

**Hint:** Le lettere minuscole hanno valori ASCII maggiori di 32 rispetto alle maiuscole.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>

void maiuscolo(char* str) {
    while (*str != '\0') {
        if (*str >= 'a' && *str <= 'z') {
            *str = *str - 32;  // Converti in maiuscolo
        }
        str++;
    }
}

void minuscolo(char* str) {
    while (*str != '\0') {
        if (*str >= 'A' && *str <= 'Z') {
            *str = *str + 32;  // Converti in minuscolo
        }
        str++;
    }
}

int main() {
    char str1[] = "Ciao Mondo!";
    char str2[] = "Programmazione IN C";
    char str3[] = "HeLLo WoRLd 123";
    
    printf("=== CONVERSIONI ===\n\n");
    
    // Test maiuscolo
    printf("Originale: '%s'\n", str1);
    maiuscolo(str1);
    printf("Maiuscolo: '%s'\n\n", str1);
    
    // Test minuscolo
    printf("Originale: '%s'\n", str2);
    minuscolo(str2);
    printf("Minuscolo: '%s'\n\n", str2);
    
    // Test combinato
    printf("Originale: '%s'\n", str3);
    maiuscolo(str3);
    printf("Maiuscolo: '%s'\n", str3);
    minuscolo(str3);
    printf("Minuscolo: '%s'\n", str3);
    
    return 0;
}
```

**Output:**
```
=== CONVERSIONI ===

Originale: 'Ciao Mondo!'
Maiuscolo: 'CIAO MONDO!'

Originale: 'Programmazione IN C'
Minuscolo: 'programmazione in c'

Originale: 'HeLLo WoRLd 123'
Maiuscolo: 'HELLO WORLD 123'
Minuscolo: 'hello world 123'
```

</details>

---

## ESERCIZI BONUS

### Bonus 1: Concatena Stringhe (20 min)
Implementa `void concatena(char* dest, char* src)` che aggiunge `src` alla fine di `dest`.

### Bonus 2: Cerca Carattere (15 min)
Implementa `char* cercaCarattere(char* str, char c)` che ritorna un puntatore alla prima occorrenza di `c` in `str`, o `NULL` se non trovato.

### Bonus 3: Inverti Stringa (20 min)
Implementa `void invertiStringa(char* str)` che inverte la stringa in place usando due puntatori.

### Bonus 4: Sostituisci Carattere (20 min)
Implementa `int sostituisci(char* str, char vecchio, char nuovo)` che sostituisce tutte le occorrenze e ritorna il numero di sostituzioni.

### Bonus 5: Filtra Array (25 min)
Implementa `int filtraPari(int* src, int* dest, int dim)` che copia solo gli elementi pari da `src` a `dest` e ritorna quanti ne ha copiati.

---

## Domande di Verifica

1. **Cosa restituisce l'operatore `&`?**
2. **Cosa fa l'operatore `*`?**
3. **Perché `arr[2]` è equivalente a `*(arr+2)`?**
4. **Come si passa una variabile per riferimento?**
5. **Qual è la differenza tra `char str[]` e `char* str`?**

<details>
<summary><b>📝 RISPOSTE</b></summary>

1. L'**indirizzo di memoria** di una variabile
2. **Dereferenzia** un puntatore (accede al valore puntato)
3. Il compilatore traduce `arr[i]` in `*(arr + i)` automaticamente
4. Si passa l'**indirizzo** con `&` e la funzione riceve un **puntatore**
5. `char str[]` è modificabile (stack), `char* str` punta a memoria read-only

</details>

---

**Complimenti! Hai completato tutti gli esercizi sui puntatori! 🎉**
