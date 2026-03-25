#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_POSTI 100
#define LUNGHEZZA_TARGA 8
#define TARIFFA_A 1.70
#define TARIFFA_B 2.80

typedef struct
{
    char targa[LUNGHEZZA_TARGA];
    int oraIngresso;
    int minutoIngresso;
    int occupato;
} Veicolo;

typedef struct
{
    Veicolo posti[MAX_POSTI];
    int dimensione;
} Parcheggio;

// Dopo i #define e typedef, prima di qualsiasi funzione:
int salvaFile(Parcheggio *p, const char *filename);
int caricaFile(Parcheggio *p, const char *filename);
void leggiStringa(const char targa[], char buffer[], int dimensione);

// Genera targa casuale
const char *generaTarga(char *targa)
{
    int tipoTarga = 2;
    const char lettere[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    for (int i = 0; i < 7; i++)
    {
        if (i >= tipoTarga && i < 5)
            targa[i] = '0' + rand() % 10;
        else
            targa[i] = lettere[rand() % 26];
    }
    targa[7] = '\0';
}

// Inizializzazione
void inizializzaParcheggio(Parcheggio *p, int dimensione, char *targa)
{
    p->dimensione = dimensione;

    // Azzera TUTTI i posti prima di qualsiasi altra cosa
    for (int i = 0; i < dimensione; i++)
        p->posti[i].occupato = 0;

    if (caricaFile(p, "parcheggio.txt") == 0)
    {
        leggiStringa("Dati caricati da file. Vuoi sovrascrivere? (s/n): ", targa, LUNGHEZZA_TARGA);
        if (strcmp(targa, "s") == 0)
        {
            printf("Sovrascrivo i dati esistenti.\n");
            for (int i = 0; i < dimensione; i++)
                p->posti[i].occupato = 0;
        }
        else
        {
            printf("Dati caricati con successo.\n");
        }
    }
    else
    {
        printf("Nessun dato salvato, inizializzazione standard.\n");
    }
}

// Visualizza stato
void stampaStato(Parcheggio *p)
{
    for (int i = 0; i < p->dimensione; i++)
    {
        if (p->posti[i].occupato)
        {
            printf("Posto %d: %s (%02d:%02d)\n",
                   i + 1,
                   p->posti[i].targa,
                   p->posti[i].oraIngresso,
                   p->posti[i].minutoIngresso);
        }
        else
        {
            printf("Posto %d: Libero\n", i + 1);
        }
    }
}

// Ingresso veicolo
void occupaPosto(Parcheggio *p)
{
    char targa[LUNGHEZZA_TARGA];
    generaTarga(targa);

    time_t now = time(NULL);
    struct tm *t = localtime(&now);

    for (int i = 0; i < p->dimensione; i++)
    {
        if (!p->posti[i].occupato)
        {
            p->posti[i].occupato = 1;
            strcpy(p->posti[i].targa, targa);
            p->posti[i].oraIngresso = t->tm_hour;
            p->posti[i].minutoIngresso = t->tm_min;

            printf("Ingresso: %s al posto %d\n", targa, i + 1);
            return;
        }
    }
    printf("Parcheggio pieno!\n");
}

// Uscita + calcolo costo
void liberaPosto(Parcheggio *p, char *targa)
{
    for (int i = 0; i < p->dimensione; i++)
    {
        if (p->posti[i].occupato && strcmp(p->posti[i].targa, targa) == 0)
        {

            time_t now = time(NULL);
            struct tm *t = localtime(&now);

            int oraU = t->tm_hour;
            int minU = t->tm_min;

            int durataOre = oraU - p->posti[i].oraIngresso;
            int durataMin = minU - p->posti[i].minutoIngresso;

            if (durataMin < 0)
            {
                durataMin += 60;
                durataOre--;
            }

            float costo;
            if (durataOre < 2)
                costo = TARIFFA_A;
            else
                costo = TARIFFA_A + (durataOre - 2) * TARIFFA_B;

            printf("Uscita %s - Costo: %.2f euro\n", targa, costo);

            p->posti[i].occupato = 0;
            return;
        }
    }
    printf("Veicolo non trovato!\n");
}

const int salvaFile(Parcheggio *p, const char *filename)
{
    FILE *file = fopen(filename, "w");
    if (file == NULL)
    {
        printf("Errore nell'apertura del file!\n");
        return -1;
    }

    for (int i = 0; i < p->dimensione; i++)
    {
        if (p->posti[i].occupato)
        {
            fprintf(file, "%s %02d:%02d\n",
                    p->posti[i].targa,
                    p->posti[i].oraIngresso,
                    p->posti[i].minutoIngresso);
        }
    }
    fclose(file);
    return 0; // Salvataggio riuscito
}

const int caricaFile(Parcheggio *p, const char *filename)
{
    FILE *file = fopen(filename, "r");
    if (file == NULL)
    {
        return -1; // File non trovato
    }

    char targa[LUNGHEZZA_TARGA];
    int ora, minuto;
    int index = 0;

    while (fscanf(file, "%s %d:%d", targa, &ora, &minuto) == 3 && index < p->dimensione)
    {
        p->posti[index].occupato = 1;
        strcpy(p->posti[index].targa, targa);
        p->posti[index].oraIngresso = ora;
        p->posti[index].minutoIngresso = minuto;
        index++;
    }
    fclose(file);
    return 0; // Caricamento riuscito
}

void leggiStringa(const char targa[], char buffer[], int dimensione)
{
    printf("%s", targa);
    fgets(buffer, dimensione, stdin);
    buffer[strcspn(buffer, "\n")] = '\0';
}

void stampaMenu()
{
    printf("\n--- Parcheggio Intelligente ---\n");
    printf("1. Ingresso\n");
    printf("2. Uscita\n");
    printf("3. Stato\n");
    printf("4. Esci\n");
}

void uscitaProgramma(Parcheggio *p)
{
    if (salvaFile(p, "parcheggio.txt") == 0)
    {
        printf("Dati salvati con successo.\n");
    }
    else
    {
        printf("Errore nel salvataggio dei dati.\n");
    }
    printf("Uscita programma.\n");
}

// MAIN
int main()
{
    srand(time(NULL));

    Parcheggio p;
    char targa[LUNGHEZZA_TARGA];

    inizializzaParcheggio(&p, 10, targa);

    int scelta;

    do
    {
        stampaMenu();
        scanf("%d", &scelta);

        switch (scelta)
        {
        case 1:
            occupaPosto(&p);
            break;
        case 2:
            printf("Inserisci targa: ");
            scanf("%s", targa);
            liberaPosto(&p, targa);
            break;
        case 3:
            stampaStato(&p);
            break;
        case 4:
            uscitaProgramma(&p);
            break;
        default:
            printf("Scelta non valida!\n");
        }

    } while (scelta != 4);

    return 0;
}