// See https://aka.ms/new-console-template for more information
/*
    Dato in input il raggio di un cerchio, 
    calcolare il diametro, l'area e la circonferenza.
    Visualizzare i risultati.
*/

// variabili & input

Console.WriteLine("Inserisci il raggio:");
double r1 = double.Parse(Console.ReadLine());

// calcoli

double diametro = r1 * 2;
double area = Math.PI*Math.Pow(r1, 2);
double circonferenza = diametro * Math.PI;

// output
// fomattazione lineare

string msg = $"Dati del Cerchio" +
     $"raggio={r1}" +
     $", diametro={diametro}" +
     $", area={area}" +
     $", circonferenza={circonferenza}";

Console.WriteLine(msg);