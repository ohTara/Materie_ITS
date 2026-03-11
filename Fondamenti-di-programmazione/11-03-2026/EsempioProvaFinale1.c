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

void mostraSala(int sala[FILE_SALA][POSTI_PER_FILA])    // Funzione per mostrare lo stato attuale della sala
{
    printf(TITOLO_SALA);
    printf("Visualizzazione posti Sala:\n");    
    for (int i = 0; i < 10; i++)        // Stampa intestazione colonne
    {
        printf("%3d: ", i);
    }
    printf("\n");
    for (int j = 0; j < 10; j++)    // Stampa ogni fila con i posti
    {
        printf("%3d: ", j);
        for (int i = 0; i < 12; i++)    // Stampa stato del posto (0 o 1)
        {
            printf("%3d ", sala[j][i]);
        }
        printf("\n");
    }
}

void inizializzaSala(int sala[FILE_SALA][POSTI_PER_FILA])   // Funzione per inizializzare la sala con tutti i posti liberi (0)
{
    for (int i = 0; i < FILE_SALA; i++) // Ciclo per ogni fila
    {
        for (int j = 0; j < POSTI_PER_FILA; j++) // Ciclo per ogni posto nella fila
        {
            sala[i][j] = 0; // 0 = libero, 1 = prenotato
        }
    }
}

bool prenotaPosto(int sala[FILE_SALA][POSTI_PER_FILA], int *fila, int *posto)   // Funzione per prenotare un posto, restituisce true se la prenotazione è avvenuta con successo, altrimenti false
{
    printf("Inserisci fila (0-9): ");
    scanf("%d", fila);
    printf("Inserisci posto (0-11): ");
    scanf("%d", posto);

    if (*fila >= 0 && *fila < FILE_SALA && *posto >= 0 && *posto < POSTI_PER_FILA)  // Controlla se la fila e il posto sono validi
    {
        if (sala[*fila][*posto] == 0)
        {
            sala[*fila][*posto] = 1;
            printf("Confermare prenotazione: Y/N \n");  // Prenota il posto
            char conferma;
            scanf(" %c", &conferma);
            if (conferma == 'Y' || conferma == 'y')     // Chiede conferma all'utente
            {
                printf("Posto prenotato con successo!\n");
            } else
            {
                sala[*fila][*posto] = 0; // Se l'utente non conferma, libera il posto
                printf("Prenotazione annullata.\n");
            }
            
            return true;
        }
        else
        {
            printf("Posto già prenotato. Scegli un altro posto.\n");    // Se il posto è già prenotato, informa l'utente e restituisce false
            return false;
        }
    }
    else
    {
        printf("Fila o posto non validi. Riprova.\n");      // Se la fila o il posto non sono validi, informa l'utente e restituisce false
        return false;
    }
}
void acquistareBiglietto(int sala[FILE_SALA][POSTI_PER_FILA])     // Funzione per acquistare un biglietto, calcola il prezzo in base alla fila e mostra il prezzo all'utente
{
    int fila, posto;

    if (prenotaPosto(sala, &fila, &posto))  // Se la prenotazione è avvenuta con successo, calcola il prezzo del biglietto
    {
        int prezzo = (fila <= 2) ? PREZZO_BIGLIETTO_FILA_0_2 : PREZZO_BIGLIETTO_FILA_3_9;   // Calcola il prezzo in base alla fila
        printf("Biglietto acquistato con successo! Prezzo: %d\n", prezzo);
    }
}
void annullarePrenotazione(int sala[FILE_SALA][POSTI_PER_FILA])     // Funzione per annullare una prenotazione, chiede all'utente la fila e il posto da annullare, verifica se è prenotato e annulla la prenotazione
{
    int fila, posto;
    printf("Inserisci fila (0-9) per annullare prenotazione: ");
    scanf("%d", &fila);
    printf("Inserisci posto (0-11) per annullare prenotazione: ");
    scanf("%d", &posto);

    if (fila >= 0 && fila < FILE_SALA && posto >= 0 && posto < POSTI_PER_FILA)  // Controlla se la fila e il posto sono validi
    {
        if (sala[fila][posto] == 1)
        {
            sala[fila][posto] = 0; // Annulla la prenotazione
            printf("Prenotazione annullata con successo!\n");
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

void statistiche(int sala[FILE_SALA][POSTI_PER_FILA])   // Funzione per mostrare le statistiche della sala, conta i posti prenotati, i posti liberi e calcola l'incasso totale in base ai posti prenotati
{
    int postiPrenotati = 0;
    int incassoTotale = 0;

    for (int i = 0; i < FILE_SALA; i++)
    {
        for (int j = 0; j < POSTI_PER_FILA; j++)
        {
            if (sala[i][j] == 1)
            {
                postiPrenotati++;
                incassoTotale += (i <= 2) ? PREZZO_BIGLIETTO_FILA_0_2 : PREZZO_BIGLIETTO_FILA_3_9;
            }
        }
    }

    int postiLiberi = (FILE_SALA * POSTI_PER_FILA) - postiPrenotati;
    printf("Posti prenotati: %d\n", postiPrenotati);
    printf("Posti liberi: %d\n", postiLiberi);
    printf("Incasso totale: %d\n", incassoTotale);
}
void salvaSala(int sala[FILE_SALA][POSTI_PER_FILA]) // Funzione per salvare lo stato della sala su un file di testo, scrive la matrice della sala in un formato tabellare nel file "sala.txt"
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
            fprintf(file, "%d ", sala[i][j]);
        }
        fprintf(file, "\n");
    }

    fclose(file);
    printf("Sala salvata con successo in 'sala.txt'.\n");
}

void caricaSala(int sala[FILE_SALA][POSTI_PER_FILA])    // Funzione per caricare lo stato della sala da un file di testo, legge la matrice della sala dal file "sala.txt" e aggiorna lo stato della sala
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
            fscanf(file, "%d", &sala[i][j]);
        }
    }

    fclose(file);
    printf("Sala caricata con successo da 'sala.txt'.\n");
}

typedef struct  // Struttura per rappresentare il cinema, contiene la matrice della sala e l'incasso totale
{
    int sala[FILE_SALA][POSTI_PER_FILA];
    int incassoTotale;
} Cinema;

int main(void)
{
    int selMenu;
    bool cont = true;
    int sala[FILE_SALA][POSTI_PER_FILA];

    inizializzaSala(sala);

    while (cont)
    {
        printf("Seleziona un'opzione: \n");
        mainMenu();
        scanf("%d", &selMenu);

        switch (selMenu)
        {
        case 1:
            mostraSala(sala);
            break;

        case 2:
            acquistareBiglietto(sala);
            break;
        case 3:
            annullarePrenotazione(sala);
            break;
        case 4:
            statistiche(sala);
            break;
        case 5:
            salvaSala(sala);
            break;
        case 6:
            caricaSala(sala);
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
