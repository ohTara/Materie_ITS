// See https://aka.ms/new-console-template for more information
/*
    Dato in input il lato di un quadrato, 
    calcolare il pelimetro, l'area e la diagonale del quadrato.
    Visualizzare i risultati.
*/

// variabili & input

Console.WriteLine("Inserisci il lato del quadrato:");
double l1= double.Parse(Console.ReadLine());

// calcoli

double perimetro = 4 * l1;
double area = Math.Pow(l1,2);
double diagonale = l1 * Math.Sqrt(2);

// output
// fomattazione lineare

string msg = $"" +
     $"lato={l1}" +
     $", perimetro={perimetro}" +
     $", area={area}" +
     $", diagonale={diagonale}";

Console.WriteLine(msg);