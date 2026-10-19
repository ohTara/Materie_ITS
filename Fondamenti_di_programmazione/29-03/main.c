#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "paziente.h"
#include "triage.h"
#include "persistenza.h"

int main()
{
    struct paziente *pazienti = NULL;
    int count = 0;
    int scelta;

    caricaPazienti(&pazienti, &count, "pazienti.txt");

    do
    {
        printf("\nBenvenuto al sistema di gestione pronto soccorso!\n");
        printf("Seleziona un'opzione:\n");
        printf("1. Registra nuovo paziente\n");
        printf("2. Visita prossimo paziente\n");
        printf("3. Visualizza pazienti in attesa\n");
        printf("4. Cerca paziente\n");
        printf("5. Statistiche pazienti\n");
        printf("6. Esci\n");
        scanf(" %d", &scelta);

        switch (scelta)
        {
        case 1:
            pazienti = realloc(pazienti, (count + 1) * sizeof(struct paziente));
            if (pazienti == NULL)
            {
                printf("Errore di memoria!\n");
                return 1;
            }
            registraPaziente(&pazienti[count]);
            count++;
            salvaAllPazienti(pazienti, count, "pazienti.txt");
            break;
        case 2:
            visitaProssimoPaziente(&pazienti, &count);
            if (count > 0)
            {
                int indice;
                printf("Inserisci l'indice del paziente visitato: ");
                scanf("%d", &indice);
                rimuoviPazienteVisitato(&pazienti, &count, indice);
                printf("Paziente visitato e rimosso.\n");
            }
            salvaAllPazienti(pazienti, count, "pazienti.txt");
            break;
        case 3:
            stampaSalaAttesa(pazienti, count);
            salvaAllPazienti(pazienti, count, "pazienti.txt");
            break;
        case 4:
        {
            char cognome[50];
            printf("Inserisci cognome da cercare: ");
            scanf("%49s", cognome);
            cercaPaziente(pazienti, count, cognome);
            salvaAllPazienti(pazienti, count, "pazienti.txt");
            break;
        }
        case 5:
            statistichePazienti(pazienti, count);
            salvaAllPazienti(pazienti, count, "pazienti.txt");
            break;
        case 6:
            printf("Arrivederci!\n");
            salvaAllPazienti(pazienti, count, "pazienti.txt");
            break;
        default:
            printf("Opzione non valida.\n");
        }
    } while (scelta != 6);

    free(pazienti);
    return 0;
}
