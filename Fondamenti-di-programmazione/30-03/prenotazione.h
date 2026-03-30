#ifndef PRENOTAZIONE_H
#define PRENOTAZIONE_H

#include "camera.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_PRENOTAZIONI 50

struct prenotazione {
    int numeroCamera;
    char nomeOspite[50];
    int giornoArrivo, meseArrivo;
    int giornoPartenza, mesePartenza;
    int colazione;
    int checkinEffettuato; // 0 = no, 1 = si
};

float calcolaCostoSoggiorno(int tipoCamera, int numeroNotti, int colazione);
void prenotazioneCamera(struct prenotazione prenotazioni[], int maxPrenotazioni, struct camera camere[], int maxCamere);
void checkIn(struct prenotazione prenotazioni[], int n, struct camera camere[]);
void checkOut(struct prenotazione prenotazioni[], int n, struct camera camere[]);
void visualizzaPrenotazioni(struct prenotazione prenotazioni[], int n);
void bubbleSortPrenotazioni(struct prenotazione prenotazioni[], int n);

#endif // PRENOTAZIONE_H