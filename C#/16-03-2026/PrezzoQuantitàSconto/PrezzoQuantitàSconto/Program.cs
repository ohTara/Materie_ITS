// See https://aka.ms/new-console-template for more information
/*
    Dati in input il prezzo, la quantità e la percentuale di scnto di acquisto di un prodotto,
    calcolare il totale da pagare.
    Visualizzare il risultato

.   es.
    prezzo = 10
    quantità = 3
    percentuale di sconto = 30

    totale = 30,00 euro
    sconto = 9,00 euro
    totale scontato = 21,00 euro
 
 */

Console.WriteLine("Prezzo");
double prezzo = double.Parse(Console.ReadLine());

Console.WriteLine("Quantità");
int quantità = int.Parse(Console.ReadLine());

Console.WriteLine("Percentuale di sconto");
double percentualeSconto = double.Parse(Console.ReadLine());

double totale = prezzo * quantità;

Console.WriteLine($"Totale={totale}");
double sconto = totale * percentualeSconto / 100;

double totaleScontato = totale - sconto;

String scontrino = $"Prezzo={prezzo} euro" +
    $"\nQuantità={quantità} unità" +
    $"\nPercentuale di sconto={percentualeSconto} euro" +
    $"\nTotale={totale} euro" +
    $"\nSconto={sconto} euro" +
    $"\nTotale Scontato={totaleScontato} euro";

Console.WriteLine(scontrino);