// Leggi 5 interi inseriti dall'utente e sta,pali in ordine inverso usando una pila (stack). 
#include <stdio.h>
#include <stdbool.h>
#define MAX 5
int pila[MAX];
int top = -1; // -1 = pila vuota

int isEmpty() { return top == -1; }
int isFull() { return top == MAX - 1; }

void push(){
    do
    {
        if (isFull())
    {
        printf("Errore: pila piena!\n");
        return;
    } else
    {
    
        int valore;
        printf("Inserisci un numero intero: ");
        scanf("%d", &valore);
        top++;
        pila[top] = valore;     
    }
    } while (!isFull());
}

int pop() {
    if (isEmpty()) {
        printf("Errore: pila vuota!\n");
        return -1;
    }
    int valore = pila[top];
    top--;
    return valore;
}
void stampaPila() {
    if (top == -1)
    {
        printf("Pila vuota!\n");
        return;
    }else{
        printf("Pila in ordine inverso:\n");
        for (int i = top; i >= 0; i--)
        {
            printf("%d\n", pila[i]);
        }
    }
}
int main(int argc, char const *argv[])
{
    push();
    stampaPila();
    return 0;
}
