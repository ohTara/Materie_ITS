// See https://aka.ms/new-console-template for more information
Console.WriteLine("Hello, World!");
// commenti in linea

/* 
 TESTO: DATO IN INPUT DUE NUMERI INTERI,
 calcolare la somma
 visualizzare il risultato 
*/

// Variabili
int n1, n2, somma;
string tmp; 
// Input 

Console.WriteLine("n1: ");
tmp= Console.ReadLine(); // 4   

n1= int.Parse(tmp); // "4" => 4

Console.WriteLine("n2: ");
tmp= Console.ReadLine(); 
n2= int.Parse(tmp); 

// calcolo

somma= n1 + n2;

// Output: 4 + ? => ?

Console.WriteLine(somma);
Console.WriteLine("La somma è: " + somma); // stile java
Console.WriteLine("Somma ={0}", somma); // segnaposto
Console.WriteLine(n1+"+"+n2+" = " + somma); // stile java
Console.WriteLine("{0} + {1} = {2}", n1, n2, somma);
Console.WriteLine($"{n1} + {n2} = {somma}"); // string interpolation