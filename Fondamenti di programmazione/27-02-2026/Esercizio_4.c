/*
Scrivi un Programma per la gestione di un magazzino con al massimo 15 prodotti. 
Ogni prodotto ha: 
codice (stringa max 10 char); 
descrizione (stringa max 40 char); 
prezzo (float; quantita (int). 
Il programma deve: 
1. Leggere N prodotti da tastiera; 
2. Calcolare e stampare il valore totale di ogni prodotto (prezzo x quantita); 
3. Trovare e stampare il prodotto con il valore più alto; 
4. Ordinare i prodotti per valore totale decrescente e stampare il magazzino; 
5. Segnalare tutti i prodotti con quantità <=2 (scorte critiche)
*/
#include <stdio.h>
#include <string.h>
#define MAX_PRODOTTI 15
void leggiProdotti(char codice[]){
    printf("Inserisci il numero di prodotti (max %d): ", MAX_PRODOTTI);
    fgets(codice, sizeof(codice), stdin); // Legge la stringa dall'utente, inclusi gli spazi
}

void calcolaValoreTotale(float prezzo[], int quantita[], float valoreTotale[], int n){
    for(int i = 0; i < n; i++){
        valoreTotale[i] = prezzo[i] * quantita[i];
    }
}

void BubbleSort(float valoreTotale[], char codice[][11], int n){
    float temp;
    char tempCodice[10];
    for(int i = 0; i < n - 1; i++){
        for(int j = 0; j < n - i - 1; j++){
            if(valoreTotale[j] < valoreTotale[j + 1]){
                temp = valoreTotale[j];
                valoreTotale[j] = valoreTotale[j + 1];
                valoreTotale[j + 1] = temp;
                strcpy(tempCodice, codice[j]);
                strcpy(codice[j], codice[j + 1]);
                strcpy(codice[j + 1], tempCodice);
            }
        }
    }
}
void stampaMagazzino(char codice[][11], char descrizione[][41], float prezzo[], int quantita[], float valoreTotale[], int n){
    printf("\nMagazzino:\n");
    for(int i = 0; i < n; i++){
        printf("Codice: %s, Descrizione: %s, Prezzo: %.2f, Quantità: %d, Valore Totale: %.2f\n", codice[i], descrizione[i], prezzo[i], quantita[i], valoreTotale[i]);
    }
}
int main(int argc, char const *argv[])
{
    char codice[MAX_PRODOTTI][11];
    char descrizione[MAX_PRODOTTI][41];
    float prezzo[MAX_PRODOTTI];
    int quantita[MAX_PRODOTTI];
    return 0;
}
