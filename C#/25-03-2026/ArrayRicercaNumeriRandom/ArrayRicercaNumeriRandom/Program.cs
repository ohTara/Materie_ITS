Console.WriteLine("Array di numeri casuali - Ricerca sequenziale!");

/*
 * Generare un array di n numeri casuali
 * appartenenti all'intervallo [inf, sup]
 * con n, inf e sup dati in input 
   
   Effettuare la ricerca di un numero dato in input e
   visualizzare la prima occorrenza utile in una certa posizione
 
   oppure visualizzare numero non trovato
 */

Console.WriteLine("Array di numeri casuali - Ricerca sequenziale!");

Random random = new Random();

// ❌ usavi inf e sup per cose sbagliate, servono 3 variabili separate
Console.WriteLine("Inserire la grandezza dell'array:");
int n = int.Parse(Console.ReadLine());

Console.WriteLine("Inserire il limite inferiore dell'intervallo:");
int inf = int.Parse(Console.ReadLine());

Console.WriteLine("Inserire il limite superiore dell'intervallo:");
int sup = int.Parse(Console.ReadLine());

// ❌ int[] n = [inf] crea un array da 1 elemento, non da inf elementi
int[] numeri = new int[n];

for (int i = 0; i < n; i++)
{
    // ❌ random.Next(8)+1 ignorava inf e sup
    numeri[i] = random.Next(inf, sup + 1); // Next(inf, sup+1) genera numeri in [inf, sup]
    // ❌ Console.WriteLine(n) stampava il riferimento all'array, non il valore
    Console.WriteLine($"numeri[{i}] = {numeri[i]}");
}

Console.WriteLine("Inserire il numero da cercare:");
int cerca = int.Parse(Console.ReadLine());

bool trovato = false; // ❌ mancava un flag: stampavi "non trovato" ad ogni elemento != cerca

for (int i = 0; i < n; i++)
{
    if (cerca == numeri[i])
    {
        Console.WriteLine($"Numero {cerca} trovato in posizione {i}");
        trovato = true;
        break; // ci fermiamo alla prima occorrenza
    }
}

if (!trovato)
    Console.WriteLine($"Numero {cerca} non trovato"); 