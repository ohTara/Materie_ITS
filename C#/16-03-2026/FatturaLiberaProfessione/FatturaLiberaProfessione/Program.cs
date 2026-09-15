// See https://aka.ms/new-console-template for more information
/*
    Dato in input l'imponibile di un costo,
    calcolare il totale da pagare, l'ivam, la ritenuta d'acconto e il netto da pagare.
    
    Condirerare l'aliquota iva al 22%
    Considerare la ritenuta d'accounto al 20% dell'imponibile
    
    Visaulizzare i risultati 

    es. 
    Imponibile: 1000

    Imponibile=1000,00 euro
    IVA (22% dell'imponibile)=220,00 euro
    Totale lordo=1220,00 euro
    Ritenuta d'acconto (20% dell'imponibile)=200,00 euro
    Netto da pagare=1020,00 euro
*/

// definizione costanti

const int ALIQUOTA_IVA = 22;
const int PERC_RITENUTA_ACCONTO = 20;

// input

Console.WriteLine("Inserisci l'imponibile:");
double imponibile = double.Parse(Console.ReadLine());

// calcoli

double iva = (imponibile * ALIQUOTA_IVA) / 100;

double totaleLordo = imponibile + iva;

double ritenutaDacconto = (imponibile * PERC_RITENUTA_ACCONTO) / 100;

double nettoDaPagare = totaleLordo - ritenutaDacconto;

// output

string msg = $"" +
    $"\nImponibile={imponibile:0.00} euro" +
    $"\nIVA ({ALIQUOTA_IVA}% dell'imponibile)={iva:0.00} euro" +
    $"\nTotale da pagare={totaleLordo:0.00} euro" +
    $"\nRitenuta d'acconto (20% dell'imponibile)={ritenutaDacconto:0.00} euro" +
    $"\nNetto da pagare={nettoDaPagare:0.00} euro";

Console.WriteLine(msg);