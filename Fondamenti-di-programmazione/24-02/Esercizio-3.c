// Leggi una stringa (MAX 50 caratteri) e verifica se le parentesi tonde ( e ) sono bilanciate usando una pila di caratteri.
#include <stdio.h>

#define MAX 6

int coda_urgenti[MAX], tu = 0;
int coda_normali[MAX], tn = 0;

int main(){
    int n;
    printf("Quante persone? ");
    scanf("%d", &n);
    if (n > MAX) n= MAX; // Limitiamo il numero di persone a MAX
    for (int i = 0; i < n; i++)
    {
        int p;
        printf("Persona %d, priorita (1=urgente, 0=normale): ", i);
        scanf("%d", &p);
        if (p==1) coda_urgenti[i] = i;
        else coda_normali[i] = i;
    }

    printf("Ordine di servizio:\n");
    for (int i = 0; i < tu; i++){
        printf("Persona %d (urgente) \n", coda_urgenti[i]);
    }
    for (int i = 0; i < tn; i++){
        printf("Persona %d (normale) \n", coda_normali[i]);
    }
return 0;
}