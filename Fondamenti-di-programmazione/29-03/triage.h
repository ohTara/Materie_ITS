#ifndef TRIAGE_H
#define TRIAGE_H

#include <time.h>
#include "paziente.h"

void visitaProssimoPaziente(struct paziente **pazienti, int *count);
int  tempoMassimoAttesa(struct paziente *pazienti, int count, int codice);

#endif /* TRIAGE_H */
