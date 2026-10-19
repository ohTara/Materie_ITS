#include <stdio.h>

#define MAX 5

int pila[MAX];
int top = -1;  // -1 = pila vuota

int isEmpty() { return top == -1; }
int isFull()  { return top == MAX - 1; }

void push(int valore) {
    if (isFull()) {
        printf("Errore: pila piena!\n");
        return;
    }
    top++;
    pila[top] = valore;
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

int peek() {
    if (isEmpty()) {
        printf("Errore: pila vuota!\n");
        return -1;
    }
    return pila[top];
}

int main() {
    push(10);
    push(20);
    push(30);

    printf("Cima: %d\n", peek());  // 30
    printf("Pop: %d\n", pop());    // 30
    printf("Pop: %d\n", pop());    // 20
    printf("Cima: %d\n", peek());  // 10

    return 0;
}