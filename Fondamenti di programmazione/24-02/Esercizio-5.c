// Leggi i comandi da tastiera: 
// PN -> push del numero N
// O -> pop (stampa il valore rimosso, o "vuota" se la pila è vuota)
// F -> fine programma
#include <stdio.h>
#define MAX 5
int pila[MAX];
int top = -1; // -1 = pila vuota
int isEmpty() { return top == -1; }

int isFull() { return top == MAX - 1; }
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
        printf("Pila vuota!\n");
        return -1;
    }
    int valore = pila[top];
    top--;
    return valore;
}
int main() {
    char comando; 
    int numero;

    printf("Inserisci comando (P N = push N, O = pop, F = fine): ");
    scanf(" %c", &comando); // Legge il comando (P, O, F)
    do
    {
        switch (comando)
        {
        case 'P':
        printf("Inserisci numero da pushare: ");
        scanf("%d", &numero);
        push(numero);
        break;
        case 'O':
        int valore = pop();
        if (valore != -1) {
            printf("Pop: %d\n", valore);
        }
        break;
    
        case 'F':
        printf("Fine programma.\n");
        break;
        default:
        printf("Comando non valido!\n");
    }
    printf("Inserisci comando (P N = push N, O = pop, F = fine): ");
    scanf(" %c", &comando);
    } while (comando != 'F');
    
    
}
