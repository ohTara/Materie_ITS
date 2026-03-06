// Esercizio n. 1
/*
Scrivi un programma che definisce una struct Contatto con campi nome (stringa, max 30 car), cognome (stringa, max 30 car) e telefono (stringa, max 15 car).
Il programma deve:
1. Creare un array di 3 contatti inseriti direttamente nel codice (hardcoded)
2. Salvarli su un file di testo "rubrica.txt", uno per riga nel formato: nome, cognome, telefono
3. Rileggere i file e stampare a schermo i contatti letti.
*/

#include <stdio.h>
#include <string.h>

struct Contatto {
    char nome[30];
    char cognome[30];
    char telefono[15];
};

int main(int argc, char const *argv[])
{
    struct Contatto contatti[3] = {
        {"Mario", "Rossi", "1234567890"},
        {"Luigi", "Bianchi", "0987654321"},
        {"Anna", "Verdi", "5555555555"}
    };

    // Salva i contatti su un file di testo
    FILE *file = fopen("rubrica.txt", "w");
    if (file == NULL) {
        perror("Errore nell'apertura del file");
        return 1;
    }
    for (int i = 0; i < 3; i++) {
        fprintf(file, "%s, %s, %s\n", contatti[i].nome, contatti[i].cognome, contatti[i].telefono);
    }
    fclose(file);
    printf("Contatti salvati su rubrica.txt\n");

    // Rileggi i contatti dal file e stampali a schermo
    file = fopen("rubrica.txt", "r");
    if (file == NULL) {
        perror("Errore nell'apertura del file");
        return 1;
    }
    char buffer[100];

    while (fgets(buffer, sizeof(buffer), file) != NULL) {
        printf("%s", buffer);
    }
    fclose(file);
    printf("Contatti letti da rubrica.txt\n");

    
    return 0;
}
