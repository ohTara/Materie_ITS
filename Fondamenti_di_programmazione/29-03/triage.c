#include <stdio.h>
#include "triage.h"

void visitaProssimoPaziente(struct paziente **pazienti, int *count) {
    int minCodice = 5, index = -1;
    for (int i = 0; i < *count; i++) {
        if ((*pazienti)[i].visitato == 0 && (*pazienti)[i].codice < minCodice) {
            minCodice = (*pazienti)[i].codice;
            index = i;
        }
    }
    if (index != -1) {
        printf("Visita in corso: %s %s, codice: %d, arrivo: %02d:%02d\n",
               (*pazienti)[index].cognome, (*pazienti)[index].nome,
               (*pazienti)[index].codice,
               (*pazienti)[index].oraArrivo, (*pazienti)[index].minutoArrivo);
        printf("Indice paziente: %d\n", index);
    } else {
        printf("Nessun paziente in attesa.\n");
    }
}

int tempoMassimoAttesa(struct paziente *pazienti, int count, int codice) {
    int maxAttesa = 0;

    time_t now = time(NULL);
    struct tm *t = localtime(&now);
    int minutiOra = t->tm_hour * 60 + t->tm_min;

    for (int i = 0; i < count; i++) {
        if (pazienti[i].codice == codice && pazienti[i].visitato == 0) {
            int attesa = minutiOra - (pazienti[i].oraArrivo * 60 + pazienti[i].minutoArrivo);
            if (attesa < 0) attesa += 24 * 60;
            if (attesa > maxAttesa) maxAttesa = attesa;
        }
    }
    return maxAttesa;
}
