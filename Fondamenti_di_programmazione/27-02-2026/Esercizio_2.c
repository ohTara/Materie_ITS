// Il programma legge N nomi dall'utente (max 20, max 50 caratteri ciascuno), li ordina in ordine alfabetico con il Bubble Sort e li stampa ordinati 
#include <stdio.h>
#include <string.h>

void Bubble_Sort(char nomi[20][50], int N) {
    for (int i = 0; i < N-1; i++) {
        for (int j = 0; j < N-i-1; j++) {
            if (strcmp(nomi[j], nomi[j+1]) > 0) {
                // Scambia i nomi
                char temp[50];
                strcpy(temp, nomi[j]);
                strcpy(nomi[j], nomi[j+1]);
                strcpy(nomi[j+1], temp);
            }
        }
    }

}

void stampa_nomi(char nomi[20][50], int N) {
    printf("Nomi ordinati:\n");
    for (int i = 0; i < N; i++) {
        printf("%s\n", nomi[i]);
    }
}

int main(int argc, char const *argv[])
{
    char nomi[20][50]; // Array di stringhe, 20 nomi, max 50 caratteri ciascuno
    int N;
    printf("Quanti nomi vuoi inserire? (max 20): ");
    scanf("%d", &N);
    if (N > 20) {
        printf("Numero di nomi troppo grande. Max 20.\n");
        return 1;
    }
    for (int i = 0; i < N; i++) {
        printf("Inserisci il nome %d: ", i+1);
        scanf("%s", nomi[i]); // Legge un nome alla volta
    }

    Bubble_Sort(nomi, N);
    stampa_nomi(nomi, N);

    return 0;
}
