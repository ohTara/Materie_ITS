/*
 * Calcolare la media aritmetica di n numeri interi strattamente positivi 
 * 
 * Visualizzare il risultato
 * 
 * NB: l'inserimento termina alla presenza di un numero nullo o negativo
 * 
 */

int somma = 0;
int conta = 0;
int numero;

Console.WriteLine("Inserire un numero (0 o negativo per terminare):");

for (numero = int.Parse(Console.ReadLine()); numero > 0; numero = int.Parse(Console.ReadLine()))
{
    somma += numero;
    conta++;
    Console.WriteLine("Inserire un numero (0 o negativo per terminare):");
}

if (conta > 0)
{
    double media = (double)somma / conta;
    Console.WriteLine($"Media aritmetica = {media}");
}
else
{
    Console.WriteLine("Nessun numero valido inserito.");
}