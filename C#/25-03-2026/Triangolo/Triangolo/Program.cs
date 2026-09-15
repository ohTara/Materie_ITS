using System.Drawing;
// Scrivere un programma che chiede all’utente di inserire
// tre lati di un triangolo,
// calcola il perimetro e l’area del triangolo
// determina se è equilatero, isoscele o scaleno.
double l1, l2, l3;

Console.WriteLine("lato 1");
l1=Convert.ToDouble(Console.ReadLine());
Console.WriteLine("lato 2");
l2 = Convert.ToDouble(Console.ReadLine());
Console.WriteLine("lato 3");
l3 = Convert.ToDouble(Console.ReadLine());

//perimetro del triangolo
double perimetro = l1 + l2 + l3;

// Area del triangolo con formula di Erone
double sp = perimetro / 2;
double area = Math.Sqrt(sp * (sp - l1) * (sp - l2) * (sp - l3));

// calcolo del tipo di triangolo
string tipoTriangolo = "Scaleno";

if (l1==l2 && l1==l3)
{
    tipoTriangolo = "Equilatero";
}
else if (l1==l2 || l1==l3 || l2==l3)
{
    tipoTriangolo = "Isoscele";
}

// Sanitizzazione dei dati e controllo se è possibile costruire un triangolo con i lati inseriti
bool isCostruibile = 
       (l1 + l2 > l3) 
    && (l1 + l3 > l2) 
    && (l2 + l3 > l1);
if (isCostruibile)
{
    // Output
    string msg = $"" +
        $"lato 1: {l1} \n" +
        $"lato 2: {l2} \n" +
        $"lato 3: {l3} \n" +
        $"Il triangolo è {tipoTriangolo} \n" +
        $"Il perimetro è {perimetro} \n" +
        $"L'area è {area}";
    Console.WriteLine(msg);
}
else
{
    Console.WriteLine("Con i lati inseriti non si puo' costruire un triangolo");
}

