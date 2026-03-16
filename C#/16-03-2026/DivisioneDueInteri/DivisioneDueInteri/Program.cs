// See https://aka.ms/new-console-template for more information
/*
    Dati in input dividendo e divisone numeri interi,
calcolare il quoziente intero, il resto e il quoziente reale.
Visualizzare i risultati.
 */

// var

int dividendo, divisore, quozienteIntero, resto;
double quozienteReale;

// input

Console.WriteLine("Inserisci il dividendo:");
dividendo = int.Parse(Console.ReadLine()); 

Console.WriteLine("Inserisci il divisore:");
divisore = int.Parse(Console.ReadLine());

// calcoli

quozienteIntero = dividendo / divisore;
resto = dividendo % divisore;
quozienteReale = (double)dividendo / divisore;  // casting 

// output
// format dettaglio

string msg = $""+
    $"\nquoziente intero={quozienteIntero}"+
    $"\nresto={resto}"+
    $"\nquoziente Reale={quozienteReale}";

Console.WriteLine(msg);