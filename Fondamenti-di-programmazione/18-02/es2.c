#include <stdio.h>
#include <stdlib.h>

// Es Chiedere n temperature, calcolare media, trovare la più alta e la più bassa.

int main(int argc, char const *argv[])
{
    int n=7;
    /*printf("Quante temperature? : ");
    scanf("%d", &n);*/    
    float* temp = (float*)malloc(n * sizeof(float));
    if (temp == NULL)
    {
        printf("Errore nell'allocazione della memoria\n");  
        return 1;
    }
    for (int i = 0; i < n; i++)
    {
        printf("Inserisci la temperatura %d: ", i + 1);
        scanf("%f", &temp[i]);
    }
    float sum = 0;
    for (int i = 0; i < n; i++)
    {
        sum += temp[i];
    }
     float avg = sum / n;
    
    
    float min = temp[0];
    float max = temp[0];
    for (int i = 0; i < n; i++)
    {
        if (temp[i]<min)
        {
            min = temp[i];     
        } else
        {
            if (temp[i] > max)
            {
                max = temp[i];
            }
        }    
    }
    printf("La media delle temperature è: %.2f\n", avg);
    printf("La temperatura minima è: %.2f\n", min);
    printf("La temperatura massima è: %.2f\n", max);
    free(temp);
    temp= NULL;
    return 0;
}