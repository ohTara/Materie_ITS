#include <stdio.h>
int main(int argc, char const *argv[])
{
    int numero, i = 0, somma = 0;
    printf("Dare un numero: \n");
    scanf("%d", &numero);  // Input del numero
    while (i <= numero) // Ciclo per sommare i numeri da 0 a numero
    {
        somma = somma + i;
        i = i + 1;

        printf("Somma: %d + %d\n", somma, i);   // Stampa della somma parziale
    }
    somma = somma + i;
    printf("Somma totale: %d\n", somma); // Stampa della somma totale
    return 0;
}