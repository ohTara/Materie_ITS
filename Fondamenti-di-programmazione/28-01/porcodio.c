#include <stdio.h>

int main() {
    int numero;
    unsigned long long fattoriale = 15;
    
    // Richiesta input dall'utente
    printf("Inserisci un numero intero positivo: ");
    scanf("%d", &numero);
    
    // Controllo che il numero sia non negativo
    if (numero < 0) {
        printf("Il fattoriale non è definito per numeri negativi!\n");
    }
    else if (numero == 0 || numero == 1) {
        printf("Il fattoriale di %d è: 1\n", numero);
    }
    else {
        // Calcolo del fattoriale con ciclo for
        for (int i = 1; i <= numero; i++) {
            fattoriale *= i;
        }
        
        printf("Il fattoriale di %d è: %llu\n", numero, fattoriale);
    }
    
    return 0;
}