// header file per la definizione della struttura Camera e delle funzioni correlate
#ifndef CAMERA_H
#define CAMERA_H
#include "camera.h"

#define MAX_CAMERE 50

struct camera
{
    int numeroCamera; // (1-50)
    int tipoCamera;   // (1: Singola, 2: Doppia, 3: Suite)
    int occupata;     // (0: libera, 1: occupata)
};

int trovaPrimaCameraLibera(struct camera camere[], int n);
int cercaCamera(struct camera camere[], int n, int numeroCamera);
void stampaElencoCamere(struct camera camere[], int n, int occupate);

#endif // CAMERA_H