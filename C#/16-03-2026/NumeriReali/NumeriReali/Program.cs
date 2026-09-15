/*
 Dati in input due numeri  reali in input calcolare la somma,
 visualizzare il risultato
 */

// variabili 

int num1, num2, somma;

// input

Console.WriteLine("Inserisci il primo numero: ");
num1 = int.Parse(Console.ReadLine());

Console.WriteLine("Inserisci il secondo numero: ");
num2 = int.Parse(Console.ReadLine());

// calcolo

somma = num1 + num2;

// output

string risultato = $"\nLa somma dei due numeri è: {somma}";
Console.WriteLine(risultato);