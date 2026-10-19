#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include "paziente.h"

void bubleSortPazienti(struct paziente *pazienti, int count, int ordine) {
    for (int i = 0; i < count - 1; i++)
        for (int j = 0; j < count - i - 1; j++)
            if (pazienti[j].codice > pazienti[j+1].codice) {
                struct paziente temp = pazienti[j];
                pazienti[j] = pazienti[j+1];
                pazienti[j+1] = temp;
            }
    (void)ordine; /* parametro riservato per usi futuri */
}

void registraPaziente(struct paziente *p) {
    printf("Inserisci cognome: ");
    scanf(" %49s", p->cognome);
    printf("Inserisci nome: ");
    scanf(" %49s", p->nome);

    printf("Inserisci codice (1=rosso; 2=arancione; 3=giallo; 4=verde): ");
    while (scanf(" %d", &p->codice) != 1 || p->codice < 1 || p->codice > 4) {
        printf("Codice non valido. Inserisci un valore tra 1 e 4: ");
        while (getchar() != '\n');
    }

    /* Ora di arrivo automatica */
    time_t now = time(NULL);
    struct tm *t = localtime(&now);
    p->oraArrivo    = t->tm_hour;
    p->minutoArrivo = t->tm_min;
    p->visitato = 0;

    printf("Paziente %s %s registrato (codice %d) alle %02d:%02d.\n",
           p->cognome, p->nome, p->codice, p->oraArrivo, p->minutoArrivo);
}

void rimuoviPazienteVisitato(struct paziente **pazienti, int *count, int indice) {
    if (indice < 0 || indice >= *count) {
        printf("Indice non valido.\n");
        return;
    }
    for (int i = indice; i < *count - 1; i++)
        (*pazienti)[i] = (*pazienti)[i+1];
    (*count)--;
    if (*count == 0) {
        free(*pazienti);
        *pazienti = NULL;
    } else {
        *pazienti = realloc(*pazienti, (*count) * sizeof(struct paziente));
    }
}

void cercaPaziente(struct paziente *pazienti, int count, const char *cognome) {
    int trovati = 0;
    for (int i = 0; i < count; i++)
        if (strcmp(pazienti[i].cognome, cognome) == 0) {
            printf("Paziente trovato: %s %s, codice: %d, arrivo: %02d:%02d\n",
                   pazienti[i].cognome, pazienti[i].nome, pazienti[i].codice,
                   pazienti[i].oraArrivo, pazienti[i].minutoArrivo);
            trovati++;
        }
    if (trovati == 0)
        printf("Paziente con cognome '%s' non trovato.\n", cognome);
}

void durataAttesa(struct paziente *pazienti, int count) {
    int tempoMax[] = {0, 0, 15, 30, 120};

    time_t now = time(NULL);
    struct tm *t = localtime(&now);
    int minutiOra = t->tm_hour * 60 + t->tm_min;

    for (int i = 0; i < count; i++) {
        if (pazienti[i].visitato == 0) {
            int attesa = minutiOra - (pazienti[i].oraArrivo * 60 + pazienti[i].minutoArrivo);
            if (attesa < 0) attesa += 24 * 60;

            printf("  %s %s - attesa: %d min", pazienti[i].cognome, pazienti[i].nome, attesa);

            int codice = pazienti[i].codice;
            if (codice >= 1 && codice <= 4 && tempoMax[codice] > 0 && attesa > tempoMax[codice])
                printf(" [ATTENZIONE: superato limite di %d min!]", tempoMax[codice]);
            printf("\n");
        }
    }
}

void stampaSalaAttesa(struct paziente *pazienti, int count) {
    if (count == 0) {
        printf("Nessun paziente in attesa.\n");
        return;
    }
    printf("\nPazienti in attesa (ordinati per priorita'):\n");
    bubleSortPazienti(pazienti, count, 1);
    durataAttesa(pazienti, count);
}

void statistichePazienti(struct paziente *pazienti, int count) {
    int codici[4] = {0, 0, 0, 0};
    for (int i = 0; i < count; i++)
        if (pazienti[i].codice >= 1 && pazienti[i].codice <= 4)
            codici[pazienti[i].codice - 1]++;
    printf("\nStatistiche pazienti:\n");
    printf("Rosso:     %d\n", codici[0]);
    printf("Arancione: %d\n", codici[1]);
    printf("Giallo:    %d\n", codici[2]);
    printf("Verde:     %d\n", codici[3]);
}
