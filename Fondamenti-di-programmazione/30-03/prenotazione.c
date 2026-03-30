#include "camera.h"
#include "prenotazione.h"
#include "persistenza.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

float calcolaCostoSoggiorno(int tipoCamera, int numeroNotti, int colazione)
{
    float costoPerNotte;
    switch (tipoCamera)
    {
    case 1:
        costoPerNotte = 60.0f; // Singola
        break;
    case 2:
        costoPerNotte = 90.0f; // Doppia
        break;
    case 3:
        costoPerNotte = 150.0f; // Suite
        break;
    default:
        return -1;
    }
    if (colazione)
        costoPerNotte += 12.0f; // Supplemento colazione
    return costoPerNotte * numeroNotti;
}

void prenotazioneCamera(struct prenotazione prenotazioni[], int maxPrenotazioni,
                        struct camera camere[], int maxCamere)
{
    int i, idx = -1;
    for (i = 0; i < maxPrenotazioni; i++)
    {
        if (prenotazioni[i].numeroCamera == 0)
        {
            idx = i;
            break;
        }
    }
    if (idx == -1)
    {
        printf("Nessuno slot disponibile.\n");
        return;
    }

    struct prenotazione p = {0};

    printf("Nome ospite: ");
    scanf("%49s", p.nomeOspite);

    // Selezione tipo camera
    printf("Tipo camera:\n");
    printf("  1. Singola  (60.00 EUR/notte)\n");
    printf("  2. Doppia   (90.00 EUR/notte)\n");
    printf("  3. Suite   (150.00 EUR/notte)\n");
    printf("Scelta: ");
    int tipo;
    scanf("%d", &tipo);
    if (tipo < 1 || tipo > 3)
    {
        printf("Tipo non valido.\n");
        return;
    }

    // Trova prima camera libera del tipo scelto
    int camIdx = -1;
    for (i = 0; i < maxCamere; i++)
    {
        if (camere[i].tipoCamera == tipo && camere[i].occupata == 0)
        {
            camIdx = i;
            break;
        }
    }
    if (camIdx == -1)
    {
        printf("Nessuna camera di quel tipo disponibile.\n");
        return;
    }
    p.numeroCamera = camere[camIdx].numeroCamera;
    printf("Camera assegnata: %d\n", p.numeroCamera);

    int dateValide = 0;
    do
    {
        printf("Giorno arrivo  (1-31): ");
        scanf("%d", &p.giornoArrivo);
        printf("Mese arrivo    (1-12): ");
        scanf("%d", &p.meseArrivo);
        printf("Giorno partenza (1-31): ");
        scanf("%d", &p.giornoPartenza);
        printf("Mese partenza  (1-12): ");
        scanf("%d", &p.mesePartenza);

        // Controlla che le date siano valide (giorni 1-31, mesi 1-12)
        if (p.giornoArrivo < 1 || p.giornoArrivo > 31 ||
            p.meseArrivo < 1 || p.meseArrivo > 12 ||
            p.giornoPartenza < 1 || p.giornoPartenza > 31 ||
            p.mesePartenza < 1 || p.mesePartenza > 12)
        {
            printf("Date non valide. Giorni (1-31), mesi (1-12).\n");
            continue;
        }

        // Controlla che partenza sia dopo arrivo
        int assArrivo = p.meseArrivo * 100 + p.giornoArrivo;
        int assPartenza = p.mesePartenza * 100 + p.giornoPartenza;
        if (assPartenza <= assArrivo)
        {
            printf("La data di partenza deve essere successiva all'arrivo.\n");
            continue;
        }

        dateValide = 1; // tutto ok, esci dal loop

    } while (!dateValide);

    printf("Colazione (0=no, 1=si): ");
    scanf("%d", &p.colazione);

    prenotazioni[idx] = p;
    printf("Prenotazione effettuata.\n");
    salvaPrenotazioniSuFile(prenotazioni, maxPrenotazioni, "prenotazioni.txt");
}

void checkIn(struct prenotazione prenotazioni[], int n, struct camera camere[]) // Effettua il check-in per una prenotazione esistente
{
    char nome[50];
    printf("Nome ospite: ");
    scanf("%49s", nome);
    for (int i = 0; i < n; i++)
    {
        if (strcmp(prenotazioni[i].nomeOspite, nome) == 0)
        {
            if (prenotazioni[i].checkinEffettuato)
            {
                printf("Check-in già effettuato per %s.\n", nome);
                return;
            }
            int numCam = prenotazioni[i].numeroCamera;
            camere[numCam - 1].occupata = 1;
            prenotazioni[i].checkinEffettuato = 1;
            printf("Check-in effettuato per %s, camera %d.\n", nome, numCam);
            salvaPrenotazioniSuFile(prenotazioni, n, "prenotazioni.txt");
            return;
        }
    }
    printf("Prenotazione non trovata.\n");
}

void checkOut(struct prenotazione prenotazioni[], int n, struct camera camere[])    // Effettua il check-out per una prenotazione esistente
{
    char nome[50];
    printf("Nome ospite: ");
    scanf("%49s", nome);
    for (int i = 0; i < n; i++)
    {
        if (strcmp(prenotazioni[i].nomeOspite, nome) == 0)
        {
            if (!prenotazioni[i].checkinEffettuato)
            {
                printf("Impossibile effettuare il check-out: check-in non ancora eseguito.\n");
                return;
            }
            int numCam = prenotazioni[i].numeroCamera;
            int giorniMese[] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
            int assArrivo = prenotazioni[i].giornoArrivo;
            int assPartenza = prenotazioni[i].giornoPartenza;
            for (int m = 1; m < prenotazioni[i].meseArrivo; m++)
                assArrivo += giorniMese[m];
            for (int m = 1; m < prenotazioni[i].mesePartenza; m++)
                assPartenza += giorniMese[m];
            int notti = assPartenza - assArrivo;
            float costo = calcolaCostoSoggiorno(
                camere[numCam - 1].tipoCamera, notti, prenotazioni[i].colazione);

            // Salva nel log prima di azzerare i dati
            salvaLogCheckout(&prenotazioni[i], notti, costo, "log_checkout.txt");

            camere[numCam - 1].occupata = 0;
            prenotazioni[i].numeroCamera = 0;
            printf("Check-out effettuato. Notti: %d - Costo totale: %.2f EUR\n",
                   notti, costo);
            salvaPrenotazioniSuFile(prenotazioni, n, "prenotazioni.txt");
            return;
        }
    }
    printf("Prenotazione non trovata.\n");
}
void visualizzaPrenotazioni(struct prenotazione prenotazioni[], int n)  // Visualizza tutte le prenotazioni in modo ordinato per numero di camera
{
    printf("%-20s %-8s %-12s %-12s %-10s\n",
           "Ospite", "Camera", "Arrivo", "Partenza", "Colazione");
    for (int i = 0; i < n; i++)
    {
        if (prenotazioni[i].numeroCamera == 0)
            continue;
        printf("%-20s %-8d %02d/%02d       %02d/%02d       %-10s\n",
               prenotazioni[i].nomeOspite,
               prenotazioni[i].numeroCamera,
               prenotazioni[i].giornoArrivo, prenotazioni[i].meseArrivo,
               prenotazioni[i].giornoPartenza, prenotazioni[i].mesePartenza,
               prenotazioni[i].colazione ? "Sì" : "No");
    }
    bubbleSortPrenotazioni(prenotazioni, n);
}

void bubbleSortPrenotazioni(struct prenotazione prenotazioni[], int n)  // Ordina le prenotazioni per numero di camera (usato per visualizzazione ordinata)
{
    for (int i = 0; i < n - 1; i++)
        for (int j = 0; j < n - i - 1; j++)
            if (prenotazioni[j].numeroCamera > prenotazioni[j + 1].numeroCamera)
            {
                struct prenotazione tmp = prenotazioni[j];
                prenotazioni[j] = prenotazioni[j + 1];
                prenotazioni[j + 1] = tmp;
            }
}