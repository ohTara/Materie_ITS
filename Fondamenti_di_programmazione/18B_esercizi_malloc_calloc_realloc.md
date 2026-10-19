# ESERCIZI - MALLOC, CALLOC E REALLOC

### TEMPO STIMATO: 2 ore (15 esercizi)

---

**DISTRIBUZIONE CONSIGLIATA:**
- Esercizi 1-5: malloc base (40 min)
- Esercizi 6-10: calloc e array paralleli (50 min)
- Esercizi 11-15: realloc e ridimensionamento (30 min)

---

## PARTE 1: ESERCIZI MALLOC

## Esercizio 1: Array Dinamico di Interi (10 min)

Scrivi un programma che:
1. Chiede all'utente quanti numeri vuole inserire
2. Alloca un array dinamico con `malloc`
3. Legge i numeri da tastiera
4. Stampa l'array, la somma e la media
5. Libera la memoria

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;

    printf("Quanti numeri vuoi inserire? ");
    scanf("%d", &n);

    // Alloca array dinamicamente
    int* arr = (int*) malloc(n * sizeof(int));

    if (arr == NULL) {
        printf("ERRORE: Allocazione fallita!\n");
        return 1;
    }

    // Inserimento
    printf("Inserisci %d numeri:\n", n);
    for (int i = 0; i < n; i++) {
        printf("  arr[%d] = ", i);
        scanf("%d", &arr[i]);
    }

    // Stampa
    printf("\nArray: [ ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("]\n");

    // Somma e media
    int somma = 0;
    for (int i = 0; i < n; i++) {
        somma += arr[i];
    }
    float media = (float) somma / n;

    printf("Somma:  %d\n", somma);
    printf("Media:  %.2f\n", media);

    // Libera la memoria
    free(arr);
    arr = NULL;

    return 0;
}
```

**Esempio di esecuzione:**
```
Quanti numeri vuoi inserire? 5
Inserisci 5 numeri:
  arr[0] = 10
  arr[1] = 30
  arr[2] = 20
  arr[3] = 50
  arr[4] = 40

Array: [ 10 30 20 50 40 ]
Somma:  150
Media:  30.00
```

</details>

---

## Esercizio 2: Temperature della Settimana (10 min)

Alloca dinamicamente un array per 7 temperature (una per giorno), calcola:
- Media settimanale
- Giorno più caldo
- Giorno più freddo

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c

```

</details>

---

## Esercizio 3: Filtra Numeri Positivi (10 min)

1. Leggi n numeri in un array dinamico#include <stdio.h>
#include <stdlib.h>

int main() {
    int n = 7;
    char* giorni[] = {"Lunedì", "Martedì", "Mercoledì", "Giovedì", 
                      "Venerdì", "Sabato", "Domenica"};

    float* temp = (float*) malloc(n * sizeof(float));
    if (temp == NULL) {
        printf("Errore allocazione!\n");
        return 1;
    }

    printf("=== TEMPERATURE SETTIMANALI ===\n\n");
    for (int i = 0; i < n; i++) {
        printf("  %s: ", giorni[i]);
        scanf("%f", &temp[i]);
    }

    // Media
    float somma = 0;
    for (int i = 0; i < n; i++) somma += temp[i];
    float media = somma / n;

    // Max e min
    float max = temp[0], min = temp[0];
    int giornoMax = 0, giornoMin = 0;
    
    for (int i = 1; i < n; i++) {
        if (temp[i] > max) {
            max = temp[i];
            giornoMax = i;
        }
        if (temp[i] < min) {
            min = temp[i];
            giornoMin = i;
        }
    }

    printf("\n=== RISULTATI ===\n");
    printf("Media:         %.2f°C\n", media);
    printf("Giorno più caldo:  %s (%.2f°C)\n", giorni[giornoMax], max);
    printf("Giorno più freddo: %s (%.2f°C)\n", giorni[giornoMin], min);

    free(temp);
    temp = NULL;

    return 0;
}
2. Conta quanti sono positivi
3. Alloca un secondo array esattamente della dimensione necessaria
4. Copia solo i numeri positivi nel secondo array
5. Stampa entrambi e libera

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;

    printf("Quanti numeri? ");
    scanf("%d", &n);

    // Array originale
    int* arr = (int*) malloc(n * sizeof(int));
    if (arr == NULL) {
        printf("Errore allocazione!\n");
        return 1;
    }

    printf("Inserisci %d numeri:\n", n);
    for (int i = 0; i < n; i++) {
        printf("  arr[%d] = ", i);
        scanf("%d", &arr[i]);
    }

    // Conta i positivi
    int conta = 0;
    for (int i = 0; i < n; i++) {
        if (arr[i] > 0) conta++;
    }

    printf("\nNumeri positivi: %d\n\n", conta);

    // Alloca array per i positivi
    int* positivi = (int*) malloc(conta * sizeof(int));
    if (positivi == NULL) {
        free(arr);
        return 1;
    }

    // Copia solo i positivi
    int idx = 0;
    for (int i = 0; i < n; i++) {
        if (arr[i] > 0) {
            positivi[idx++] = arr[i];
        }
    }

    // Stampa
    printf("Array originale:  [ ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("]\n");

    printf("Array positivi:   [ ");
    for (int i = 0; i < conta; i++) printf("%d ", positivi[i]);
    printf("]\n");

    free(arr);
    arr = NULL;
    free(positivi);
    positivi = NULL;

    return 0;
}
```

**Esempio:**
```
Quanti numeri? 6
Inserisci 6 numeri:
  arr[0] = -5
  arr[1] = 12
  arr[2] = -3
  arr[3] = 8
  arr[4] = 0
  arr[5] = 15

Numeri positivi: 3

Array originale:  [ -5 12 -3 8 0 15 ]
Array positivi:   [ 12 8 15 ]
```

</details>

---

## Esercizio 4: Trova e Sostituisci (5 min)

Alloca un array, cerca un valore e sostituiscilo con un altro (conta quante sostituzioni fai).

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;

    printf("Dimensione array: ");
    scanf("%d", &n);

    int* arr = (int*) malloc(n * sizeof(int));
    if (arr == NULL) return 1;

    printf("Inserisci %d numeri:\n", n);
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    int vecchio, nuovo;
    printf("\nValore da cercare: ");
    scanf("%d", &vecchio);
    printf("Valore sostitutivo: ");
    scanf("%d", &nuovo);

    int sostituzioni = 0;
    for (int i = 0; i < n; i++) {
        if (arr[i] == vecchio) {
            arr[i] = nuovo;
            sostituzioni++;
        }
    }

    printf("\nSostituzioni effettuate: %d\n\n", sostituzioni);
    printf("Array modificato: [ ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("]\n");

    free(arr);
    arr = NULL;

    return 0;
}
```

</details>

---

## Esercizio 5: Copia e Inverti (5 min)

Alloca due array: uno originale e uno che è la copia invertita del primo.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;

    printf("Dimensione: ");
    scanf("%d", &n);

    int* arr = (int*) malloc(n * sizeof(int));
    int* invertito = (int*) malloc(n * sizeof(int));
    
    if (arr == NULL || invertito == NULL) {
        free(arr);
        free(invertito);
        return 1;
    }

    printf("Inserisci %d numeri:\n", n);
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    // Copia invertendo
    for (int i = 0; i < n; i++) {
        invertito[i] = arr[n - 1 - i];
    }

    printf("\nOriginale:  [ ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("]\n");

    printf("Invertito:  [ ");
    for (int i = 0; i < n; i++) printf("%d ", invertito[i]);
    printf("]\n");

    free(arr);
    free(invertito);

    return 0;
}
```

</details>

---

## PARTE 2: ESERCIZI CALLOC

## Esercizio 6: Inizializzazione con calloc (10 min)

Alloca un array con `calloc`, stampa i valori iniziali (tutti 0), poi inserisci solo nelle posizioni pari.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;

    printf("Quanti elementi? ");
    scanf("%d", &n);

    // calloc: alloca E inizializza tutto a zero
    float* arr = (float*) calloc(n, sizeof(float));

    if (arr == NULL) {
        printf("ERRORE: Allocazione fallita!\n");
        return 1;
    }

    // Stampa valori iniziali (tutti zero grazie a calloc)
    printf("\nValori iniziali:\n[ ");
    for (int i = 0; i < n; i++) {
        printf("%.1f ", arr[i]);
    }
    printf("]\n");

    // Inserisce solo nelle posizioni pari
    printf("\nInserisci i valori nelle posizioni pari:\n");
    for (int i = 0; i < n; i += 2) {
        printf("  arr[%d] = ", i);
        scanf("%f", &arr[i]);
    }

    // Stampa array finale
    printf("\nArray finale:\n[ ");
    for (int i = 0; i < n; i++) {
        printf("%.1f ", arr[i]);
    }
    printf("]\n");

    free(arr);
    arr = NULL;

    return 0;
}
```

**Esempio:**
```
Quanti elementi? 6

Valori iniziali:
[ 0.0 0.0 0.0 0.0 0.0 0.0 ]

Inserisci i valori nelle posizioni pari:
  arr[0] = 1.5
  arr[2] = 3.0
  arr[4] = 7.5

Array finale:
[ 1.5 0.0 3.0 0.0 7.5 0.0 ]
```

</details>

---

## Esercizio 7: Contatore di Voti (10 min)

Usa `calloc` per creare un array di contatori (da 0 a 10), poi conta quante volte compare ogni voto.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;

    printf("Quanti voti? ");
    scanf("%d", &n);

    // Array dei voti
    int* voti = (int*) malloc(n * sizeof(int));
    if (voti == NULL) return 1;

    // Contatori per ogni voto da 0 a 10
    // calloc: partono tutti da 0, pronti per il conteggio
    int* contatori = (int*) calloc(11, sizeof(int));
    if (contatori == NULL) {
        free(voti);
        return 1;
    }

    printf("Inserisci i voti (0-10):\n");
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
            printf("  Voto %2d: ", v);
            for (int i = 0; i < contatori[v]; i++) printf("█");
            printf(" (%d)\n", contatori[v]);
        }
    }

    free(voti);
    free(contatori);

    return 0;
}
```

</details>

---

## Esercizio 8: Matrice con calloc (10 min)

Simula una matrice 3x3 usando un array monodimensionale allocato con `calloc`. Inizia tutto a 0, poi chiedi all'utente di riempire solo alcune celle.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int righe = 3, colonne = 3;
    int dimensione = righe * colonne;

    // calloc: parte tutta a zero
    int* matrice = (int*) calloc(dimensione, sizeof(int));
    if (matrice == NULL) return 1;

    printf("Matrice iniziale (calloc → tutto 0):\n");
    for (int i = 0; i < righe; i++) {
        for (int j = 0; j < colonne; j++) {
            int indice = i * colonne + j;
            printf("%3d ", matrice[indice]);
        }
        printf("\n");
    }

    printf("\nQuante celle vuoi modificare? ");
    int n;
    scanf("%d", &n);

    for (int k = 0; k < n; k++) {
        int i, j, valore;
        printf("  Cella [riga][colonna] valore: ");
        scanf("%d %d %d", &i, &j, &valore);
        
        if (i >= 0 && i < righe && j >= 0 && j < colonne) {
            matrice[i * colonne + j] = valore;
        }
    }

    printf("\nMatrice finale:\n");
    for (int i = 0; i < righe; i++) {
        for (int j = 0; j < colonne; j++) {
            int indice = i * colonne + j;
            printf("%3d ", matrice[indice]);
        }
        printf("\n");
    }

    free(matrice);

    return 0;
}
```

</details>

---

## Esercizio 9: Array Paralleli - Studenti (10 min)

Usa `calloc` per creare array paralleli per nomi e voti. Stampa solo gli studenti che hanno passato (voto >= 6).

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    int n;

    printf("Quanti studenti? ");
    scanf("%d", &n);
    getchar();

    // Array di puntatori per i nomi
    char** nomi = (char**) malloc(n * sizeof(char*));
    if (nomi == NULL) return 1;

    // Array di voti con calloc (partono da 0)
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

        nomi[i] = (char*) malloc((strlen(buffer) + 1) * sizeof(char));
        if (nomi[i] == NULL) {
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

    // Stampa solo i promossi
    printf("\n=== STUDENTI PROMOSSI (voto >= 6) ===\n");
    int promossi = 0;
    for (int i = 0; i < n; i++) {
        if (voti[i] >= 6) {
            printf("  %-20s → %.2f\n", nomi[i], voti[i]);
            promossi++;
        }
    }
    printf("\nTotale promossi: %d su %d\n", promossi, n);

    // Libera tutto
    for (int i = 0; i < n; i++) {
        free(nomi[i]);
    }
    free(nomi);
    free(voti);

    return 0;
}
```

</details>

---

## Esercizio 10: Inventario Prodotti (10 min)

Array paralleli per nomi prodotti, quantità (con calloc = 0 iniziale), prezzi. Permetti di aggiungere/rimuovere quantità.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    int n = 5;
    char* prodotti[] = {"Laptop", "Mouse", "Tastiera", "Monitor", "Cuffie"};
    float prezzi[] = {899.99, 29.99, 79.99, 349.99, 149.99};

    // Quantità partono da 0 (magazzino vuoto)
    int* quantita = (int*) calloc(n, sizeof(int));
    if (quantita == NULL) return 1;

    printf("=== INVENTARIO INIZIALE ===\n");
    for (int i = 0; i < n; i++) {
        printf("%d. %-15s | €%.2f | Qnt: %d\n", 
               i + 1, prodotti[i], prezzi[i], quantita[i]);
    }

    // Operazioni
    while (1) {
        printf("\n1. Aggiungi stock\n2. Rimuovi stock\n3. Visualizza\n0. Esci\n> ");
        int scelta;
        scanf("%d", &scelta);

        if (scelta == 0) break;

        if (scelta == 1 || scelta == 2) {
            printf("Prodotto (1-%d): ", n);
            int prod;
            scanf("%d", &prod);
            prod--;

            if (prod >= 0 && prod < n) {
                printf("Quantità: ");
                int q;
                scanf("%d", &q);

                if (scelta == 1) {
                    quantita[prod] += q;
                    printf("✓ Aggiunti %d %s\n", q, prodotti[prod]);
                } else {
                    if (quantita[prod] >= q) {
                        quantita[prod] -= q;
                        printf("✓ Rimossi %d %s\n", q, prodotti[prod]);
                    } else {
                        printf("✗ Stock insufficiente!\n");
                    }
                }
            }
        } else if (scelta == 3) {
            printf("\n=== INVENTARIO ATTUALE ===\n");
            for (int i = 0; i < n; i++) {
                printf("%d. %-15s | €%.2f | Qnt: %d\n", 
                       i + 1, prodotti[i], prezzi[i], quantita[i]);
            }
        }
    }

    free(quantita);

    return 0;
}
```

</details>

---

## PARTE 3: ESERCIZI REALLOC

## Esercizio 11: Array che Cresce On-Demand (10 min)

Inizia con capacità 2, raddoppia ogni volta che l'array si riempie.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int capacita = 2;
    int dimensione = 0;

    int* arr = (int*) malloc(capacita * sizeof(int));
    if (arr == NULL) return 1;

    printf("Inserisci numeri (0 per terminare):\n");

    while (1) {
        int num;
        printf("  Numero: ");
        scanf("%d", &num);

        if (num == 0) break;

        // Se pieno, raddoppia
        if (dimensione == capacita) {
            capacita *= 2;
            printf("    → Raddoppio capacità a %d...\n", capacita);

            int* temp = (int*) realloc(arr, capacita * sizeof(int));
            if (temp == NULL) {
                free(arr);
                return 1;
            }
            arr = temp;
        }

        arr[dimensione++] = num;
    }

    printf("\nArray finale (%d elementi, capacità %d):\n[ ",
           dimensione, capacita);
    for (int i = 0; i < dimensione; i++) {
        printf("%d ", arr[i]);
    }
    printf("]\n");

    free(arr);

    return 0;
}
```

</details>

---

## Esercizio 12: Ridimensiona Array (5 min)

Alloca un array, riempilo, poi chiedi all'utente una nuova dimensione e usa `realloc`.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;

    printf("Dimensione iniziale: ");
    scanf("%d", &n);

    int* arr = (int*) malloc(n * sizeof(int));
    if (arr == NULL) return 1;

    printf("Inserisci %d numeri:\n", n);
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    printf("\nArray originale: [ ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("]\n");

    printf("\nNuova dimensione: ");
    int nuova;
    scanf("%d", &nuova);

    int* temp = (int*) realloc(arr, nuova * sizeof(int));
    if (temp == NULL) {
        free(arr);
        return 1;
    }
    arr = temp;

    if (nuova > n) {
        printf("Inserisci i %d nuovi elementi:\n", nuova - n);
        for (int i = n; i < nuova; i++) {
            printf("  arr[%d] = ", i);
            scanf("%d", &arr[i]);
        }
    }

    printf("\nArray ridimensionato: [ ");
    for (int i = 0; i < nuova; i++) printf("%d ", arr[i]);
    printf("]\n");

    free(arr);

    return 0;
}
```

</details>

---

## Esercizio 13: Lista Dinamica di Stringhe (10 min)

Permetti all'utente di inserire stringhe una alla volta, usando `realloc` per far crescere l'array.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    int dimensione = 0;
    int capacita = 2;

    char** lista = (char**) malloc(capacita * sizeof(char*));
    if (lista == NULL) return 1;

    printf("Inserisci stringhe (invio vuoto per terminare):\n\n");

    while (1) {
        char buffer[100];
        printf("  Stringa %d: ", dimensione + 1);
        fgets(buffer, sizeof(buffer), stdin);
        buffer[strcspn(buffer, "\n")] = '\0';

        if (strlen(buffer) == 0) break;

        // Se pieno, raddoppia
        if (dimensione == capacita) {
            capacita *= 2;
            printf("    → Espando a capacità %d\n", capacita);

            char** temp = (char**) realloc(lista, capacita * sizeof(char*));
            if (temp == NULL) {
                for (int i = 0; i < dimensione; i++) free(lista[i]);
                free(lista);
                return 1;
            }
            lista = temp;
        }

        lista[dimensione] = (char*) malloc((strlen(buffer) + 1) * sizeof(char));
        if (lista[dimensione] == NULL) {
            for (int i = 0; i < dimensione; i++) free(lista[i]);
            free(lista);
            return 1;
        }
        strcpy(lista[dimensione], buffer);
        dimensione++;
    }

    printf("\n=== LISTA FINALE (%d stringhe) ===\n", dimensione);
    for (int i = 0; i < dimensione; i++) {
        printf("%d. %s\n", i + 1, lista[i]);
    }

    for (int i = 0; i < dimensione; i++) free(lista[i]);
    free(lista);

    return 0;
}
```

</details>

---

## Esercizio 14: Compatta Array (5 min)

Alloca un array, rimuovi tutti gli elementi negativi usando `realloc` per ridurre la dimensione.

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n;

    printf("Dimensione: ");
    scanf("%d", &n);

    int* arr = (int*) malloc(n * sizeof(int));
    if (arr == NULL) return 1;

    printf("Inserisci %d numeri:\n", n);
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    printf("\nArray originale: [ ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("]\n");

    // Compatta rimuovendo negativi
    int nuovaDim = 0;
    for (int i = 0; i < n; i++) {
        if (arr[i] >= 0) {
            arr[nuovaDim++] = arr[i];
        }
    }

    printf("Negativi rimossi: %d\n", n - nuovaDim);

    // Riduci dimensione
    int* temp = (int*) realloc(arr, nuovaDim * sizeof(int));
    if (temp == NULL && nuovaDim > 0) {
        free(arr);
        return 1;
    }
    arr = temp;

    printf("\nArray compattato: [ ");
    for (int i = 0; i < nuovaDim; i++) printf("%d ", arr[i]);
    printf("]\n");

    free(arr);

    return 0;
}
```

</details>

---

## Esercizio 15: Buffer Circolare con realloc (10 min)

Simula un buffer in cui aggiungi elementi, rimuovi elementi, visualizza elementi che può espandersi: quando si riempie, raddoppia con `realloc`.

Comandi: 1=Aggiungi 2=Rimuovi 3=Visualizza 0=Esci

<details>
<summary><b>💡 SOLUZIONE</b></summary>

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int capacita = 3;
    int dimensione = 0;

    int* buffer = (int*) malloc(capacita * sizeof(int));
    if (buffer == NULL) return 1;

    printf("=== BUFFER DINAMICO ===\n");
    printf("Comandi: 1=Aggiungi 2=Rimuovi 3=Visualizza 0=Esci\n\n");

    while (1) {
        printf("> ");
        int cmd;
        scanf("%d", &cmd);

        if (cmd == 0) break;

        if (cmd == 1) {
            // Aggiungi
            if (dimensione == capacita) {
                capacita *= 2;
                printf("  Buffer pieno → espando a capacità %d\n", capacita);

                int* temp = (int*) realloc(buffer, capacita * sizeof(int));
                if (temp == NULL) {
                    free(buffer);
                    return 1;
                }
                buffer = temp;
            }

            printf("  Valore: ");
            int val;
            scanf("%d", &val);
            buffer[dimensione++] = val;
            printf("  ✓ Aggiunto (size=%d/%d)\n", dimensione, capacita);

        } else if (cmd == 2) {
            // Rimuovi
            if (dimensione > 0) {
                dimensione--;
                printf("  ✓ Rimosso (size=%d/%d)\n", dimensione, capacita);
            } else {
                printf("  ✗ Buffer vuoto!\n");
            }

        } else if (cmd == 3) {
            // Visualizza
            printf("  Buffer (%d/%d): [ ", dimensione, capacita);
            for (int i = 0; i < dimensione; i++) {
                printf("%d ", buffer[i]);
            }
            printf("]\n");
        }
    }

    free(buffer);

    return 0;
}
```

</details>

---

## Riepilogo: Cosa Hai Praticato

| Esercizio | malloc | calloc | realloc | Tecnica |
|-----------|--------|--------|---------|---------|
| 1 | ✅ | | | Input dinamico |
| 2 | ✅ | | | Trova max/min |
| 3 | ✅ | | | Filtraggio con secondo array |
| 4 | ✅ | | | Ricerca e sostituzione |
| 5 | ✅ | | | Copia invertita |
| 6 | | ✅ | | Posizioni pari/dispari |
| 7 | | ✅ | | Contatori |
| 8 | | ✅ | | Matrice monodimensionale |
| 9 | ✅ | ✅ | | Array paralleli |
| 10 | | ✅ | | Inventario con operazioni |
| 11 | ✅ | | ✅ | Crescita automatica |
| 12 | ✅ | | ✅ | Ridimensionamento manuale |
| 13 | ✅ | | ✅ | Lista stringhe dinamica |
| 14 | ✅ | | ✅ | Compattazione |
| 15 | ✅ | | ✅ | Buffer espandibile |

---

## Checklist Finale

**Prima di ogni esercizio, ricorda:**
```
✓ Includi <stdlib.h>
✓ Controlla sempre se malloc/calloc/realloc ritornano NULL
✓ Usa sizeof(tipo) per calcolare i byte
✓ Per realloc, usa una variabile temporanea
✓ Fai free() prima di uscire dal programma
✓ Imposta il puntatore a NULL dopo free
```

**Complimenti! Ora padroneggi l'allocazione dinamica in C! 🎉**
