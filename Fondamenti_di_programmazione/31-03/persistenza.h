// header file per la definizione della struttura Camera e delle funzioni correlate
#ifndef PERSISTENZA_H
#define PERSISTENZA_H
#include "prenotazione.h"

void salvaPrenotazioniSuFile(struct prenotazione prenotazioni[], int n, const char* nomeFile);
int caricaPrenotazioniDaFile(struct prenotazione prenotazioni[], int maxPrenotazioni, const char* nomeFile);
void salvaLogCheckout(struct prenotazione *p, int notti, float costo, const char *nomeFile);

#endif // PERSISTENZA_H