#include <stdio.h>
int main(int argc, char const *argv[])
{
    int a;
    printf("Selezionare operazione:\n"); // Menu di selezione
    printf("1. Somma di numeri\n");
    printf("2. Media di numeri\n");
    printf("3. Sottrazione\n");
    printf("4. Divisione\n");
    printf("5. Moltiplicazione\n");
    printf("0. Uscita\n");
    scanf("%d", &a);
    switch (a) // Struttura di selezione
    {
    case 1: // Somma di n numeri
        int i, b;
        printf("Quanti numeri vuoi sommare?\n");
        scanf("%d", &b);
        int sum = 0;
        i = 1;
        do
        {
            int num;
            printf("Inserisci il numero %d: ", i);
            scanf("%d", &num);
            sum += num;
            i++;
        } while (i <= b);
        printf("La somma dei numeri inseriti e': %d\n", sum);
        break;
    case 2: // Media di n numeri
        printf("Quanti numeri vuoi mediare?\n");
        scanf("%d", &b);
        int med = 0;
        i = 1;
        do
        {
            int num;
            printf("Inserisci il numero %d: ", i);
            scanf("%d", &num);
            med += num;
            i++;
        } while (i <= b);
        double average = (double)med / b;
        printf("La media dei numeri inseriti e': %.2f\n", average);
        break;
    case 3: // Sottrazione
    {
        int num1, num2;
        printf("Inserisci il primo numero: ");
        scanf("%d", &num1);
        printf("Inserisci il sottraendo: ");
        scanf("%d", &num2);
        int difference = num1 - num2;
        printf("La differenza e': %d\n", difference);
    }
    break;
    case 4: // Divisione
    {
        double num1, num2;
        printf("Inserisci il dividendo: ");
        scanf("%lf", &num1);
        printf("Inserisci il divisore: ");
        scanf("%lf", &num2);
        if (num2 != 0)
        {
            double quotient = num1 / num2;
            printf("Il quoziente e': %.2f\n", quotient);
        }
        else
        {
            printf("Errore: Divisione per zero non permessa.\n");
        }
    }
    break;
    case 5: // Moltiplicazione di n numeri
    {
        int num1, num2, i, b;
        printf("Quanti numeri vuoi moltiplicare?\n");
        scanf("%d", &b);
        i = 1;
        printf("Inserisci il primo numero da moltiplicare:\n");
        scanf("%d", &num1);
        while (i <= b) // Ciclo di moltiplicazione
        {
            int num;
            printf("Inserisci il numero %d: ", i);
            scanf("%d", &num);
            if (i <= b && num != 0) // Controllo del numero di iterazioni
            {
                num2 = num;
                int product = num1 * num2;
                printf("Il prodotto parziale e': %d\n", product);
                num1 = product; // Aggiorna num1 con il prodotto corrente
            }
            else // Gestione errore
            {
                printf("Exception\n");
                num1 = 0;
                break;
            }
            i++;
        }
        printf("Il prodotto totale e': %d\n", num1);
    }
    break;
    case 0: // Uscita
        printf("Uscita.\n");
        break;
    default: // Scelta non valida
        printf("Scelta non valida\n");
        break;
    }
}