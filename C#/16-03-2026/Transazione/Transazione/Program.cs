/*
   Dati in input il prezzo e la quantità di acquisto di un prodotto,
   calcolare il totale da pagare
   Visualizzare il risultato
*/

// variabili 

int quantita;
double totale;
double prezzoProdotto;

// input

Console.WriteLine("Inserisci la quantità:");
quantita = int.Parse(Console.ReadLine());

Console.WriteLine("Inserire il prezzo del prodotto: ");
prezzoProdotto = double.Parse(Console.ReadLine());

// calcolo transazione
totale = quantita * prezzoProdotto;

// output
string risultato = $"\nIl totale della transazione è: {totale:C2}";
Console.WriteLine(risultato);
