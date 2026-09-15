#include <stdio.h>
#include <stdlib.h>

/*
    Es 3: Filtra numeri positivi
          1. Leggi n numeri in un array dinamico
          2. Conta quanti sono positivi
          3. Alloca un secondo array della dimensione necessaria
          4. Copia solo i numeri positivi nel secondo array
          5. Stampa entambi & free
*/ 

int main(int argc, char const *argv[])
{
    int n;
    printf("Quanti numeri vuoi inserire? ");
    scanf("%d", &n);
    int* numeri = (int*) malloc(n * sizeof(int));
    if (numeri == NULL)
    {
        printf("Errore nell'allocazione della memoria\n");
        return 1;
    }
    for (int i = 0; i < n; i++)
    {
        printf("Inserisci il numero %d: ", i + 1);
        scanf("%d", &numeri[i]);
    }
    
    int* nPositivi = (int*) calloc(n, sizeof(int));
    if (nPositivi == NULL)
    {
        printf("Errore nell'allocazione della memoria\n");
        free(nPositivi);    
        free(numeri);
        return 1;
    }
    for (int i = 0; i < n; i++)
    {
        if (numeri[i] >= 0)
        {
            nPositivi[i]=numeri[i];
        }
        printf("%d ", nPositivi[i]);
        printf("\n", numeri[i]);
    }
    
    
   
    return 0;
}
