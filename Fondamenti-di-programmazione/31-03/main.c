#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "camera.h"
#include "prenotazione.h"
#include "persistenza.h"

int main(int argc, char const *argv[])
{
    int selezione;

    // Inizializza array di camere e prenotazioni
    struct camera camera[MAX_CAMERE];
    struct prenotazione prenotazione[MAX_PRENOTAZIONI];
    memset(prenotazione, 0, sizeof(prenotazione)); // zeroes everything, not just numeroCamera

    // Initialize camere
    for (int i = 0; i < MAX_CAMERE; i++)
    {
        camera[i].numeroCamera = i + 1;
        camera[i].tipoCamera = (i % 3) + 1; // 1=Singola 2=Doppia 3=Suite
        camera[i].occupata = 0;
    }

    //  Initialize prenotazioni
    for (int i = 0; i < MAX_PRENOTAZIONI; i++)
        prenotazione[i].numeroCamera = 0;

    caricaPrenotazioniDaFile(prenotazione, MAX_PRENOTAZIONI, "prenotazioni.txt"); // Carica prenotazioni da file all'avvio

    do
    {
        printf("\nMenu:\n");
        printf("1. Prenota camera\n");
        printf("2. Check-in\n");
        printf("3. Check-out\n");
        printf("4. Visualizza elenco camere libere\n");
        printf("5. Visualizza elenco prenotazioni\n");
        printf("6. Cerca camera\n");
        printf("7 . Esci\n");
        printf("Seleziona un'opzione: ");
        scanf("%d", &selezione);

        switch (selezione)
        {
        case 1:
            prenotazioneCamera(prenotazione, MAX_PRENOTAZIONI, camera, MAX_CAMERE); 
            continue;
        case 2:
            checkIn(prenotazione, MAX_PRENOTAZIONI, camera); // Effettua il check-in per una prenotazione esistente
            continue;
        case 3:
            checkOut(prenotazione, MAX_PRENOTAZIONI, camera); // Effettua il check-out per una prenotazione esistente
            continue;
        case 4:
            stampaElencoCamere(camera, MAX_CAMERE, 0); // libere
            continue;
        case 5:
            visualizzaPrenotazioni(prenotazione, MAX_PRENOTAZIONI); 
            continue;
        case 6:     // Cerca camera per numero
        {
            int numCam;
            printf("Numero camera da cercare: ");
            scanf("%d", &numCam);
            int idx = cercaCamera(camera, MAX_CAMERE, numCam);
            if (idx >= 0)
                printf("Camera %d - Tipo: %d - %s\n",
                       camera[idx].numeroCamera,
                       camera[idx].tipoCamera,
                       camera[idx].occupata ? "Occupata" : "Libera");
            else
                printf("Camera non trovata.\n");
            continue;
        }

        case 7:
            printf("Uscita in corso...\n");
            break;
        default:
            printf("Opzione non valida. Riprova.\n");
            break;
        }
    } while (selezione != 7);

    return 0;
}