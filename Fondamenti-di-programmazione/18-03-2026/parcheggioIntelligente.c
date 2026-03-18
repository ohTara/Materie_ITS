/* Realizzare un'applicazione in C che gestisca un parcheggio di dimensione configurabile.
 L'applicazione deve consentire:
 1. L'ingesso e uscita dei veicoli,
 2. La registrazione della targa e l'orario di ingesso,
 3. Calcolare il costo in base alla durata,
 4. Cercare veicoli e produrre un log giornaliero su file.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_POSTI 100
#define LUNGHEZZA_TARGA 16
#define TARIFFA_A 1.70
#define TARIFFA_B 2.80

typedef struct
{
    char targa[LUNGHEZZA_TARGA];
    int oraIngresso;
    int minutoIngresso;
    int occupato; // 0 se il posto è libero, 1 se è occupato
} Veicolo;

typedef struct
{
    Veicolo posti[MAX_POSTI];
    int dimensione;
} Parcheggio;

void generaTarga(char *targa, Parcheggio *p, int *dimensione)
{
    do
    {
        const char lettere[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        const char n_lettere = sizeof(lettere) - 1; // Esclude il carattere di terminazione
        targa[0] = lettere[rand() % n_lettere];
        targa[1] = lettere[rand() % n_lettere];
        targa[2] = '0' + rand() % 10;
        targa[3] = '0' + rand() % 10;
        targa[4] = '0' + rand() % 10;
        targa[5] = lettere[rand() % n_lettere];
        targa[6] = lettere[rand() % n_lettere];
        targa[7] = '\0';
    } while (p->dimensione < *dimensione);
}

void stampaTarga(char *targa, Parcheggio *p, int *dimensione)
{
    srand((unsigned int)time(NULL));   // Inizializza il generatore di numeri casuali
    generaTarga(targa, p, dimensione); // Genera una targa casuale
    printf("Targa: %s\n", targa);
}

void inizializzaParcheggio(Parcheggio *p, int *dimensione)
{
    printf("Inserisci la dimensione del parcheggio (max %d): ", MAX_POSTI);
    scanf("%d", dimensione);
    if (*dimensione < 1 || *dimensione > MAX_POSTI)
    {
        printf("Dimensione non valida! Impostazione a %d posti.\n", MAX_POSTI);
        *dimensione = MAX_POSTI;
    }
    p->dimensione = *dimensione;
    for (int i = 0; i < p->dimensione; i++)
    {
        p->posti[i].occupato = 0;    // Inizializza tutti i posti come liberi
        p->posti[i].targa[0] = '\0'; // Inizializza la targa come stringa vuota
        p->posti[i].oraIngresso = 0;
        p->posti[i].minutoIngresso = 0;
    }
}

void visualizzaParcheggio(Parcheggio *p, int postiOccupati, char *targa)
{
    generaTarga(targa, p, &p->dimensione); // Genera una targa casuale per la simulazione

    printf("Parcheggio (dimensione: %d posti): \n", p->dimensione);
    for (int i = 0; i < p->dimensione; i++)
    {
        if (p->posti[i].occupato)
        {
            printf("Posto %d: Occupato - Targa: %s, Ingresso: %02d:%02d\n",
                   i + 1, p->posti[i].targa, p->posti[i].oraIngresso, p->posti[i].minutoIngresso);
            postiOccupati++;
        }
        else
        {
            printf("Posto %d: Libero\n", i + 1);
        }
    }
    printf("Numero posti occupati: %d\n", postiOccupati);
}

void stampaStato(Parcheggio *p)
{
    printf("Parcheggio (dimensione: %d posti):\n", p->dimensione);
    for (int i = 0; i < p->dimensione; i++)
    {
        if (p->posti[i].occupato)
        {
            printf("Posto %d: Occupato - Targa: %s, Ingresso: %02d:%02d\n",
                   i + 1, p->posti[i].targa, p->posti[i].oraIngresso, p->posti[i].minutoIngresso);
        }
        else
        {
            printf("Posto %d: Libero\n", i + 1);
        }
    }
}

void calcoloCosto(int *oraIngresso, int *minutoIngresso)
{ // Tariffa A (Prime 2 ore), poi tariffa B

    *oraIngresso = 10;    // Simulazione orario di ingresso
    *minutoIngresso = 30; // Simulazione minuto di ingresso
    int oraUscita, minutoUscita;

    printf("Inserisci l'orario di uscita (HH MM): ");
    scanf("%d%*c%d", &oraUscita, &minutoUscita);

    int durataOre = oraUscita - *oraIngresso;
    int durataMinuti = minutoUscita - *minutoIngresso;

    if (durataMinuti < 0)
    {
        durataMinuti += 60;
        durataOre--;
    }
    else if (durataMinuti >= 60)
    {
        durataMinuti -= 60;
        durataOre++;
    }

    float costo = 0;
    if (durataOre < 2)
    {
        costo = TARIFFA_A; // Tariffa A
    }
    else
    {
        costo = TARIFFA_A + ((durataOre - 2) * TARIFFA_B); // Tariffa B
    }
    printf("Entrata: %d ore e %d minuti\n", *oraIngresso, *minutoIngresso);
    printf("Uscita: %d ore e %d minuti\n", oraUscita, minutoUscita);
    printf("Durata: %d ore e %d minuti\n", durataOre, durataMinuti);
    printf("Costo totale: %.2f euro\n", (float)costo);
}

void occupaPosto(Parcheggio *p, char *targa, int oraIngresso, int minutoIngresso)
{
    generaTarga(targa, p, &p->dimensione); // Genera una targa casuale per la simulazione
    for (int i = 0; i < p->dimensione; i++)
    {
        if (!p->posti[i].occupato)
        {
            p->posti[i].occupato = 1;
            strncpy(p->posti[i].targa, targa, LUNGHEZZA_TARGA);
            p->posti[i].oraIngresso = oraIngresso;
            p->posti[i].minutoIngresso = minutoIngresso;
            printf("Veicolo con targa %s parcheggiato al posto %d\n", targa, i + 1);
            return;
        }
    }
    printf("Parcheggio pieno! Impossibile parcheggiare il veicolo con targa %s\n", targa);
}

void liberaPosto(Parcheggio *p, char *targa)
{
    generaTarga(targa, p, &p->dimensione); // Genera una targa casuale per la simulazione
    for (int i = 0; i < p->dimensione; i++)
    {
        if (p->posti[i].occupato && strcmp(p->posti[i].targa, targa) == 0)
        {
            p->posti[i].occupato = 0;
            printf("Veicolo con targa %s ha lasciato il posto %d\n", targa, i + 1);
            return;
        }
    }
    printf("Veicolo con targa %s non trovato nel parcheggio!\n", targa);
}

int main(int argc, char const *argv[])
{
    int selezione;
    Parcheggio p;
    char targa[LUNGHEZZA_TARGA];
    inizializzaParcheggio(&p, &p.dimensione);
    do
    {
        printf("Seleziona un'opzione:\n1. Ingresso veicolo\n2. Uscita veicolo\n3. Visualizza parcheggio\n4. Calcola costo\n5. Esci\n");
        scanf("%d", &selezione);
        switch (selezione)
        {
        case 1:                             // Ingresso veicolo
            occupaPosto(&p, targa, 10, 30); // Parcheggia un veicolo con targa generata
            break;

        case 2:                     // Uscita veicolo
            liberaPosto(&p, targa); // Libera il posto del veicolo con targa generata
            break;
        case 3:                          // Visualizza parcheggio
            visualizzaParcheggio(&p, 0, targa); // Visualizza lo stato del parcheggio
            break;
        case 4: // Calcola costo
            calcoloCosto(&p.posti[0].oraIngresso, &p.posti[0].minutoIngresso);
            break;
        case 5: // Esci
            printf("Uscita dal programma.\n");
            break;

        default:
            printf("Opzione non valida!\n");
            break;
        }
    } while (selezione != 5);

    return 0;
}
