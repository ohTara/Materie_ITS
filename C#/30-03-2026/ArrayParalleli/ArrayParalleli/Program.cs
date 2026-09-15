using System;
using System.Dynamic;

internal partial class Program
{
    static void Main(string[] args)
    {
        string[] nominativi = { "Carlino Giulia", "Dargen Pietro", "Rossi Marco", "Bianchi Anna" };
        int[] eta = { 29, 35, 22, 27 };

        int n = nominativi.Length;

        for (int i = 0; i < n; i++)
        {
            Console.WriteLine($"{i + 1} - {nominativi[i]}, eta': {eta[i]}");
        }
    }
}

/* Prof: 
 *  var nomi = new string [] {"Carliano Giulia", "Dargen Pietro", "Pistacchio Pino"}
 *  var eta = new int [] {29, 35, 22}
 *  for (int i = 0; i < nomi.Length; i++)
 *      Console.WriteLine(nomi[i] + ", eta': " + eta[i]);
 */