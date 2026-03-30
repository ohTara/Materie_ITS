namespace ClasseQuadrato
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Istanza di oggetti Quadrato!");
            
            Quadrato q = new Quadrato(); // Creazione di un'istanza della classe Quadrato

            Console.Write("Inserisci il lato del quadrato (metri) : ");
            
            q.lato = double.Parse(Console.ReadLine()); // Impostazione del lato del quadrato, accessibilità in scrittura

            Console.WriteLine();
            Console.WriteLine($"Lato={q.lato} m");
            Console.WriteLine($"Diagonale={q.Diagonale()} m");
            Console.WriteLine($"Perimetro={q.Perimetro()} m");
            Console.WriteLine($"Area={q.Area()}  m");
        }
    }
}