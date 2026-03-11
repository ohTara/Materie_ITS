/*
Funzionalità Richieste:
    Salvataggio/Caricamento dati da file (formato tabellare)
*/
#include <stdio.h>
#include <stdbool.h>

#define FILE_SALA 10
#define POSTI_PER_FILA 12
#define TITOLO_SALA "=== Manu Cinema ===\n"
#define PREZZO_BIGLIETTO_FILA_0_2 10
#define PREZZO_BIGLIETTO_FILA_3_9 7

typedef struct Cinema // Struttura per rappresentare il cinema, contiene la matrice della sala e l'incasso totale
{
    int sala[FILE_SALA][POSTI_PER_FILA];
    int incassoTotale;
} Cinema;

void mainMenu()     // Funzione per mostrare il menu principale
{
    printf(TITOLO_SALA);
    printf("1. Mostra Sala\n");
    printf("2. Prenota Posto e acquista biglietto\n");
    printf("3. Annulla Prenotazione e rimborso\n");
    printf("4. Mostra Statistiche\n");
    printf("5. Salva sala e biglietti\n");
    printf("6. Carica sala e biglietti\n");
    printf("7. Esci\n");
}

void mostraSala(Cinema *cinema)    // Funzione per mostrare lo stato attuale della sala
{
    printf(TITOLO_SALA);
    printf("Visualizzazione posti Sala:\n");
    printf("     "); // Indentazione per allineare con le righe
    for (int i = 0; i < POSTI_PER_FILA; i++)   // FIX: iterare fino a POSTI_PER_FILA (12), non 10
    {
        printf("%3d ", i);
    }
    printf("\n");
    for (int j = 0; j < FILE_SALA; j++)    // Stampa ogni fila con i posti
    {
        printf("%3d: ", j);
        for (int i = 0; i < POSTI_PER_FILA; i++)    // Stampa stato del posto (0 o 1)
        {
            printf("%3d ", cinema->sala[j][i]);  // FIX: usare cinema->sala invece di Cinema.sala
        }
        printf("\n");
    }
}

void inizializzaSala(Cinema *cinema)   // Funzione per inizializzare la sala con tutti i posti liberi (0)
{
    cinema->incassoTotale = 0;
    for (int i = 0; i < FILE_SALA; i++)
    {
        for (int j = 0; j < POSTI_PER_FILA; j++)
        {
            cinema->sala[i][j] = 0; // FIX: usare cinema->sala invece di Cinema.sala
        }
    }
}

// FIX: restituisce true solo se la prenotazione viene effettivamente confermata
bool prenotaPosto(Cinema *cinema, int *fila, int *posto)
{
    printf("Inserisci fila (0-9): ");
    scanf("%d", fila);
    printf("Inserisci posto (0-11): ");
    scanf("%d", posto);

    if (*fila >= 0 && *fila < FILE_SALA && *posto >= 0 && *posto < POSTI_PER_FILA)
    {
        if (cinema->sala[*fila][*posto] == 0)   // FIX: usare cinema->sala
        {
            printf("Confermare prenotazione: Y/N \n");
            char conferma;
            scanf(" %c", &conferma);
            if (conferma == 'Y' || conferma == 'y')
            {
                cinema->sala[*fila][*posto] = 1; // FIX: spostato qui, prenota solo se confermato
                printf("Posto prenotato con successo!\n");
                return true;  // FIX: true solo se confermato
            }
            else
            {
                printf("Prenotazione annullata.\n");
                return false; // FIX: false se l'utente non conferma
            }
        }
        else
        {
            printf("Posto già prenotato. Scegli un altro posto.\n");
            return false;
        }
    }
    else
    {
        printf("Fila o posto non validi. Riprova.\n");
        return false;
    }
}

void acquistareBiglietto(Cinema *cinema)
{
    int fila, posto;

    if (prenotaPosto(cinema, &fila, &posto))
    {
        int prezzo = (fila <= 2) ? PREZZO_BIGLIETTO_FILA_0_2 : PREZZO_BIGLIETTO_FILA_3_9;
        cinema->incassoTotale += prezzo; // FIX: aggiorna incassoTotale nello struct
        printf("Biglietto acquistato con successo! Prezzo: %d€\n", prezzo);
    }
}

void annullarePrenotazione(Cinema *cinema)
{
    int fila, posto;
    printf("Inserisci fila (0-9) per annullare prenotazione: ");
    scanf("%d", &fila);
    printf("Inserisci posto (0-11) per annullare prenotazione: ");
    scanf("%d", &posto);

    if (fila >= 0 && fila < FILE_SALA && posto >= 0 && posto < POSTI_PER_FILA)
    {
        if (cinema->sala[fila][posto] == 1)  // FIX: usare cinema->sala
        {
            cinema->sala[fila][posto] = 0;
            int rimborso = (fila <= 2) ? PREZZO_BIGLIETTO_FILA_0_2 : PREZZO_BIGLIETTO_FILA_3_9;
            cinema->incassoTotale -= rimborso; // FIX: aggiorna incassoTotale in caso di rimborso
            printf("Prenotazione annullata con successo! Rimborso: %d€\n", rimborso);
        }
        else
        {
            printf("Posto non è prenotato. Non è possibile annullare.\n");
        }
    }
    else
    {
        printf("Fila o posto non validi. Riprova.\n");
    }
}

void statistiche(Cinema *cinema)
{
    int postiPrenotati = 0;
    int incassoTotale = 0;

    for (int i = 0; i < FILE_SALA; i++)
    {
        for (int j = 0; j < POSTI_PER_FILA; j++)
        {
            if (cinema->sala[i][j] == 1)  // FIX: usare cinema->sala
            {
                postiPrenotati++;
                incassoTotale += (i <= 2) ? PREZZO_BIGLIETTO_FILA_0_2 : PREZZO_BIGLIETTO_FILA_3_9;
            }
        }
    }

    int postiLiberi = (FILE_SALA * POSTI_PER_FILA) - postiPrenotati;
    printf("Posti prenotati: %d\n", postiPrenotati);
    printf("Posti liberi: %d\n", postiLiberi);
    printf("Incasso totale: %d€\n", incassoTotale);
}

void salvaSala(Cinema *cinema)
{
    FILE *file = fopen("sala.txt", "w");
    if (file == NULL)
    {
        printf("Errore nell'apertura del file per la scrittura.\n");
        return;
    }

    for (int i = 0; i < FILE_SALA; i++)
    {
        for (int j = 0; j < POSTI_PER_FILA; j++)
        {
            fprintf(file, "%d ", cinema->sala[i][j]);
        }
        fprintf(file, "\n");
    }

    fclose(file);
    printf("Sala salvata con successo in 'sala.txt'.\n");
}

void caricaSala(Cinema *cinema)
{
    FILE *file = fopen("sala.txt", "r");
    if (file == NULL)
    {
        printf("Errore nell'apertura del file. Assicurati che 'sala.txt' esista.\n");
        return;
    }

    for (int i = 0; i < FILE_SALA; i++)
    {
        for (int j = 0; j < POSTI_PER_FILA; j++)
        {
            fscanf(file, "%d", &cinema->sala[i][j]);
        }
    }

    fclose(file);
    printf("Sala caricata con successo da 'sala.txt'.\n");
}

int main(void)
{
    int selMenu;
    bool cont = true;
    Cinema cinema;  // FIX: dichiarare una variabile Cinema, non un array grezzo

    inizializzaSala(&cinema);

    while (cont)
    {
        printf("Seleziona un'opzione: \n");
        mainMenu();
        scanf("%d", &selMenu);

        switch (selMenu)
        {
        case 1:
            mostraSala(&cinema);    // FIX: passare &cinema a tutte le funzioni
            break;
        case 2:
            acquistareBiglietto(&cinema);
            break;
        case 3:
            annullarePrenotazione(&cinema);
            break;
        case 4:
            statistiche(&cinema);
            break;
        case 5:
            salvaSala(&cinema);
            break;
        case 6:
            caricaSala(&cinema);
            break;
        case 7:
            printf("Uscita in corso...\n");
            cont = false;
            break;
        default:
            printf("Opzione non valida. Riprova.\n");
            break;
        }
    }

    return 0;
}