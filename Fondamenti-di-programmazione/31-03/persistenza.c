// funzioni per la persistenza dei dati su file,
// come il salvataggio e il caricamento delle prenotazioni
#include <stdio.h>
#include "prenotazione.h"
#include "persistenza.h"
#include <string.h>
#include <stdlib.h>
void salvaPrenotazioniSuFile(struct prenotazione prenotazioni[], int n, const char *nomeFile)   // Salva le prenotazioni su un file di log
{
    FILE *file = fopen(nomeFile, "w");
    if (file == NULL)
    {
        perror("Errore apertura file");
        return;
    }
    for (int i = 0; i < n; i++)
    {
        if (prenotazioni[i].numeroCamera > 0 && strlen(prenotazioni[i].nomeOspite) > 0)
        {
            fprintf(file, "%d,%s,%d,%d,%d,%d,%d,%d\n",
                    prenotazioni[i].numeroCamera,
                    prenotazioni[i].nomeOspite,
                    prenotazioni[i].giornoArrivo,
                    prenotazioni[i].meseArrivo,
                    prenotazioni[i].giornoPartenza,
                    prenotazioni[i].mesePartenza,
                    prenotazioni[i].colazione,
                    prenotazioni[i].checkinEffettuato);
        }
    }
    fclose(file);
}

void salvaLogCheckout(struct prenotazione *p, int notti, float costo, const char *nomeFile) // Salva i dettagli del check-out in un file di log
{
    FILE *file = fopen(nomeFile, "a"); // "a" = append, non sovrascrive
    if (file == NULL)
    {
        perror("Errore apertura log_checkout.txt");
        return;
    }
    fprintf(file, "Ospite: %s | Camera: %d | Arrivo: %02d/%02d | Partenza: %02d/%02d | Notti: %d | Costo: %.2f EUR | Colazione: %s\n",
            p->nomeOspite,
            p->numeroCamera,
            p->giornoArrivo, p->meseArrivo,
            p->giornoPartenza, p->mesePartenza,
            notti,
            costo,
            p->colazione ? "Si" : "No");
    fclose(file);
}

int caricaPrenotazioniDaFile(struct prenotazione prenotazioni[], int maxPrenotazioni, const char *nomeFile)
{
    FILE *file = fopen(nomeFile, "r");
    if (file == NULL)
    {
        perror("Errore apertura file");
        return -1;
    }
    int count = 0;
    while (count < maxPrenotazioni && fscanf(file, "%d,%49[^,],%d,%d,%d,%d,%d,%d\n", &prenotazioni[count].numeroCamera, prenotazioni[count].nomeOspite, // Validazione dei dati caricati
                                             &prenotazioni[count].giornoArrivo, &prenotazioni[count].meseArrivo, &prenotazioni[count].giornoPartenza,
                                             &prenotazioni[count].mesePartenza, &prenotazioni[count].colazione, &prenotazioni[count].checkinEffettuato) == 8)   
    {
        if (prenotazioni[count].numeroCamera < 1 ||
            prenotazioni[count].meseArrivo < 1 || prenotazioni[count].meseArrivo > 12 ||
            prenotazioni[count].mesePartenza < 1 || prenotazioni[count].mesePartenza > 12)
            continue;
        count++;
    }
    fclose(file);
    return count;
}