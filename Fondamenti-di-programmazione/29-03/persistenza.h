#ifndef PERSISTENZA_H
#define PERSISTENZA_H

#include "paziente.h"

void salvaAllPazienti(struct paziente *pazienti, int count, const char *filename);
void caricaPazienti(struct paziente **pazienti, int *count, const char *filename);

#endif /* PERSISTENZA_H */
