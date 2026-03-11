/*
Sistema di Prenotazione e Biglietteria Cinema.
Realizzare un sistema che gestisca:
    La prenotazione dei posti;
    La vendita dei biglietti;
    La visualizzazione della sala;
    Le statistiche;
    Il salvataggio/caricamento dei dati
Specifiche della Sala:
    10 file (0-9)
    12 posti per fila (0-11)
    ogni posto può essere prenotato o libero (1 o 0)
Funzionalità Richieste:
    Mostrare la sala
    Prenotare 1 Posto + conferma acquisto
    Annullare prenotazione + Rimborso
    Mostrare statistiche (posti prenotati, posti liberi, incasso totale)
    Salvataggio/Caricamento dati da file (formato tabellare)
Menu richiesto:
    1. Mostra Sala
    2. Prenota Posto e acquista biglietto
    3. Annulla Prenotazione e rimborso
    4. Mostra Statistiche
    5. Salva sala e biglietti
    6. Carica sala e biglietti
    7. Esci
*/
#include <stdio.h>
#include <stdbool.h>

#define FILE_SALA 10
#define POSTI_PER_FILA 12
#define TITOLO_SALA "=== Manu Cinema ===\n"
#define PREZZO_BIGLIETTO_FILA_0_2 10
#define PREZZO_BIGLIETTO_FILA_3_9 7

void mainMenu()
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

void mostraSala(int sala[FILE_SALA][POSTI_PER_FILA])
{
    printf(TITOLO_SALA);
    printf("Visualizzazione posti Sala:\n");
    for (int i = 0; i < 10; i++)
    {
        printf("%3d: ", i);
    }
    printf("\n");
    for (int j = 0; j < 10; j++)
    {
        printf("%3d: ", j);
        for (int i = 0; i < 12; i++)
        {
            printf("%3d ", sala[j][i]);
        }
        printf("\n");
    }
}

void inizializzaSala(int sala[FILE_SALA][POSTI_PER_FILA])
{
    for (int i = 0; i < FILE_SALA; i++)
    {
        for (int j = 0; j < POSTI_PER_FILA; j++)
        {
            sala[i][j] = 0; // 0 = libero, 1 = prenotato
        }
    }
}

bool prenotaPosto(int sala[FILE_SALA][POSTI_PER_FILA], int *fila, int *posto)
{
    printf("Inserisci fila (0-9): ");
    scanf("%d", fila);
    printf("Inserisci posto (0-11): ");
    scanf("%d", posto);

    if (*fila >= 0 && *fila < FILE_SALA && *posto >= 0 && *posto < POSTI_PER_FILA)
    {
        if (sala[*fila][*posto] == 0)
        {
            sala[*fila][*posto] = 1; // Prenota il posto
            printf("Posto prenotato con successo!\n");
            return true;
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
void acquistareBiglietto(int sala[FILE_SALA][POSTI_PER_FILA])
{
    int fila, posto;

    if (prenotaPosto(sala, &fila, &posto))
    {
        int prezzo = (fila <= 2) ? PREZZO_BIGLIETTO_FILA_0_2 : PREZZO_BIGLIETTO_FILA_3_9;
        printf("Biglietto acquistato con successo! Prezzo: %d\n", prezzo);
    }
}
void annullarePrenotazione(int sala[FILE_SALA][POSTI_PER_FILA])
{
    int fila, posto;
    printf("Inserisci fila (0-9) per annullare prenotazione: ");
    scanf("%d", &fila);
    printf("Inserisci posto (0-11) per annullare prenotazione: ");
    scanf("%d", &posto);

    if (fila >= 0 && fila < FILE_SALA && posto >= 0 && posto < POSTI_PER_FILA)
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

void statistiche(int sala[FILE_SALA][POSTI_PER_FILA])
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
void salvaSala(int sala[FILE_SALA][POSTI_PER_FILA])
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

void caricaSala(int sala[FILE_SALA][POSTI_PER_FILA])
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

typedef struct
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
