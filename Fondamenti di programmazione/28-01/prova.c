#include <stdio.h>
int main(int argc, char const *argv[])
{
    int a,b;
    printf("Inserire primo numero\n");
    scanf("%d", &a);
    
    printf("Inserire secondo numero\n");
    scanf("%d", &b);
    /* int max = (a<b) ? b : a; // operatore ternario, equivalente a un if-else
    printf("Max value is %d\n", max);
    */
    int c = a << 1; // operatore di shift a sinistra, equivalente a moltiplicare a per 2^n
    int d = a >> 4; // equivalente a dividere a per 2^n
    printf("Result of %d >> 4 is %d\n", b, d);
    printf("Result of %d << 1 is %d\n", a, c);
}