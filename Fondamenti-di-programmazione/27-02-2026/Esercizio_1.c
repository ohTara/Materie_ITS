/*
Scrivi un programma che legge una stringa dall'utente (max 100 caratteri) e stampa: 
1. Lunghezza della stringa; 
2. il primo e ultimo carattere; 
3. Se contiene la lettera 's' (maiuscola o minuscola) 
*/


#include <stdio.h>
#include <string.h>
#define MAX 100

void stampa_stringa(char* stringa){
    // strcat(stringa, "\0"); // Assicurarsi che la stringa sia terminata correttamente
    
    if (strlen(stringa)-1=='\n')
    {
        stringa[strlen(stringa)-1] = '\0'; // Rimuove il carattere di nuova linea
    }
    printf("Lunghezza della stringa: %ld\n", strlen(stringa));
    printf("Primo carattere: %c\n", stringa[0]);
    printf("Ultimo carattere: %c\n", stringa[strlen(stringa)-2]);
    if (strchr(stringa, 's') || strchr(stringa, 'S')) {
        printf("La stringa contiene la lettera 's'.\n");
    } else {
        printf("La stringa non contiene la lettera 's'.\n");
    }
}

int main(int argc, char const *argv[])
{
    char stringa[MAX];
    printf("Inserisci una stringa (max 100 caratteri): ");
    fgets(stringa, sizeof(stringa), stdin); // Legge la stringa dall'utente, inclusi gli spazi
    
    stampa_stringa(stringa);
    return 0;
}
