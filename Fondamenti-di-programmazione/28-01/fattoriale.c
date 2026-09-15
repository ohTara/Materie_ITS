#include <stdio.h>
int main(int argc, char const *argv[])
{
    int n;
    long long fattoriale = 1;
    printf("Calculating factorials\n");
    scanf("%d", &n);
    n = (n < 0 || n==1 || n==0) ? 0 : n; // if n<0 or n==1 or n==0 set n to 0 else keep n unchanged
    
    for (int i = 1; i <= n; i++)
    {
        fattoriale = fattoriale*i;  
        printf("Factorial of %d is %lld\n", n, fattoriale);
    }
    
    return 0;
}
