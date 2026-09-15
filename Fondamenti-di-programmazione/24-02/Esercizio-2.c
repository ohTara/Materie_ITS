// Simula una coda di 4 clienti al banco. Aggiungi i clienti numerati da 1 a 4 alla cosa, poi servili una alla volta stampando "cliente N servito" a ogni estrazione. Usa un array per rappresentare la coda e due indici per tenere traccia dell'inizio e della fine della coda.
#include <stdio.h>
#define MAX 4

int coda[MAX];
int head,tail,size;
int isEmpty() { return size == 0; }
int isFull() { return size == MAX; }

void enqueue(int cliente) {     // Aggiunge un cliente alla coda
    if (isFull()) {
        printf("Errore: coda piena!\n");
        return;
    }
    coda[tail] = cliente;
    tail++; //= (tail + 1) % MAX; // Avanza il tail in modo circolare
    size++;
}

int dequeue(){      // Rimuove un cliente dalla coda
    if (isEmpty()) {
        printf("Errore: coda vuota!\n");
        return -1;
    }
    int cliente = coda[head];
    head++; //= (head + 1) % MAX; // Avanza l'head in modo circolare
    size--; 
    return cliente;
}

int main() {
    head = 0;
    tail = 0;
    size = 0;

    // Aggiungi clienti alla coda
    for (int i = 1; i <= MAX; i++) {
        enqueue(i); // Aggiunge il cliente i alla coda
        printf("Cliente %d aggiunto alla coda.\n", i);
    }

    // Servi i clienti
    while (!isEmpty()){
        int clienteServito = dequeue(); // Rimuove un cliente dalla coda
        printf("Cliente %d servito.\n", clienteServito);
    }

    return 0;
}