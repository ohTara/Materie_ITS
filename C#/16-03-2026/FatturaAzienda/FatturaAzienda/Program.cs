// See https://aka.ms/new-console-template for more information
/*
    Dato in input l'imponibile di un costo,
    calcolare il totale da pagare.
    
    Condirerare l'aliquota iva al 22%
    
    Visaulizzare i risultati 

    es. 
    Imponibile: 1000

    Imponibile=1000,00 euro
    IVA (22% dell'imponibile)=220,00 euro
    Totale da pagare=1220,00 euro
*/

// definizione costanti

const int ALIQUOTA_IVA = 22;

// input

Console.WriteLine("Inserisci l'imponibile:");
double imponibile = double.Parse(Console.ReadLine());

// calcoli

double iva = (imponibile * ALIQUOTA_IVA) / 100;

double totaleDaPagare = imponibile + iva;

// output

string msg = $"" +
    $"\nImponibile={imponibile:0.00} euro\n" +
    $"\nIVA ({ALIQUOTA_IVA}% dell'imponibile)={iva:0.00} euro\n" +
    $"\nTotale da pagare={totaleDaPagare:0.00} euro";

Console.WriteLine(msg);