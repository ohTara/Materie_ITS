// See https://aka.ms/new-console-template for more information
/*
 *  Dato in input un numero intero,
 *  verificare se è pari o dispari.
 *  Visualizzare il risultato.
 * 
 * es. input: 5
 * 
 * output :
 *  5 è un numero dispari.
 */

Console.WriteLine("Pari o Dispari!");

Console.WriteLine("Inserisci un numero intero:");
int numero = int.Parse(Console.ReadLine());

int resto = numero % 2; 

if (resto == 0)
{
    Console.WriteLine($"{numero} è un numero pari.");
}
else
{
    Console.WriteLine($"{numero} è un numero dispari.");
}