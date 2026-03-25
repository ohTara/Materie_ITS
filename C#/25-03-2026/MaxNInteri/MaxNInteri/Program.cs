/*
 * Dati in input n numeri interi, determinare il max inserito
 * 
 * Visualizzare il risultato
 */


Console.WriteLine("Determinare il max su n numeri interi!");
int maxNumeri = int.Parse(Console.ReadLine());

int max = int.MinValue;

for  (int i = 0; i < maxNumeri; i++)
{
    
    if (numero > max)
        max = numero;
}

Console.WriteLine($"Max: {max}");