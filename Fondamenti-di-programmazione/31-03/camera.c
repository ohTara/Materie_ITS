// definizione della struttura per rappresentare una camera,
// trova prima libera, cerca,
// stampa elenco camere occupate,
// stampa elenco camere libere

#include "camera.h"
#include <stdio.h>
int trovaPrimaCameraLibera(struct camera camere[], int n)
{
    for (int i = 0; i < n; i++)
    {
        if (camere[i].occupata == 0)
        {
            return i; // Restituisce l'indice della prima camera libera
        }
    }
    return -1; // Nessuna camera libera trovata
}

int cercaCamera(struct camera camere[], int n, int numeroCamera)
{
    for (int i = 0; i < n; i++)
    {
        if (camere[i].numeroCamera == numeroCamera)
        {
            return i; // Restituisce l'indice della camera trovata
        }
    }
    return -1; // Camera non trovata
}

void stampaElencoCamere(struct camera camere[], int n, int occupate)
{
    printf("Elenco delle camere %s:\n", occupate ? "occupate" : "libere");
    for (int i = 0; i < n; i++)
    {
        if (camere[i].occupata == occupate)
        {
            switch (camere[i].tipoCamera)
            {
            case 1:
                printf("Camera %d: Tipo Singola\n", camere[i].numeroCamera);
                break;
            case 2:
                printf("Camera %d: Tipo Doppia\n", camere[i].numeroCamera);
                break;
            case 3:
                printf("Camera %d: Tipo Suite\n", camere[i].numeroCamera);
                break;

            default:
                break;
            }
        }
    }
}