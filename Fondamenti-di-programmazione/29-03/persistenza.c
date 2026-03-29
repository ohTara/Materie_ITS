#include <stdio.h>
#include <stdlib.h>
#include "paziente.h"
#include "persistenza.h"

void salvaAllPazienti(struct paziente *pazienti, int count, const char *filename)
{
    FILE *file = fopen(filename, "w");
    if (file == NULL)
    {
        perror("Errore apertura file");
        return;
    }
    for (int i = 0; i < count; i++)
    {
        fprintf(file, "%s %s %d %02d:%02d %d\n",
                pazienti[i].cognome, pazienti[i].nome, pazienti[i].codice,
                pazienti[i].oraArrivo, pazienti[i].minutoArrivo, pazienti[i].visitato);
    }
    fclose(file);
}

void caricaPazienti(struct paziente **pazienti, int *count, const char *filename)
{
    FILE *file = fopen(filename, "r");
    if (file == NULL)
        return;

    struct paziente temp;
    while (fscanf(file, "%49s %49s %d %d:%d %d",
                  temp.cognome, temp.nome, &temp.codice,
                  &temp.oraArrivo, &temp.minutoArrivo,
                  &temp.visitato) == 6)
    {
        *pazienti = realloc(*pazienti, (*count + 1) * sizeof(struct paziente));
        if (*pazienti == NULL)
        {
            printf("Errore di memoria!\n");
            fclose(file);
            return;
        }
        (*pazienti)[*count] = temp;
        (*count)++;
    }
    fclose(file);
}
