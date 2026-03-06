// dimostra il vantaggio della coda circolare rispetto a quella linaere. Con un arrai di 4 slot:
// 1. Inserisci 3 elementi (10,20,30)
// 2. Estrai 2 elementi
// 3. Inserisci 3 elementi (40,50,60)
// 4. Stampa tutti gli elementi rimasti in coda
#include <stdio.h>
#define MAX 4

int coda[MAX];
int head = 0, tail = 0, size = 0;
int isEmpty() { return size == 0; }
int isFull() { return size == MAX; }
void enqueue(int numero) {
    if (isFull()) {
        printf("Errore: coda piena!\n");
        return;
    }
    coda[tail] = numero;
    tail = (tail + 1) % MAX; // Avanza il tail in modo circolare
    size++;
}
void dequeue() {
    if (isEmpty()) {
        printf("Errore: coda vuota!\n");
        return;
    }
    int numero = coda[head];
    head = (head + 1) % MAX; // Avanza il head in modo circolare
    size--;
}
void printCoda() {   // Stampa gli elementi rimasti in coda
    printf("Coda finale: %d elementi\n", size); 
    for (int i = 0; i < size; i++) {       
        printf("%d ", coda[(head + i) % MAX]); // Stampa in modo circolare
    printf("\n");
    }
}
int main(int argc, char const *argv[])
{
    enqueue(10);
    enqueue(20);
    enqueue(30);
    printf("Rimosso %d\n"), dequeue();
    printf("Rimosso %d\n"), dequeue();
    enqueue(40);
    enqueue(50);
    enqueue(60);
    printCoda();
    return 0;
}
