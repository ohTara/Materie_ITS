namespace ClasseRettangolo
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Istanza di Rettangolo!");

            Rettangolo r = new Rettangolo();

            r.Base = -1.5;
            r.Altezza = 2.5;
            
            string msg = $"" +
                $"\nBase: {r.Base}, " +
                $"\nAltezza: {r.Altezza}, " +
                $"\nArea: {r.Area()}, " +
                $"\nPerimetro: {r.Perimetro()}, " +
                $"\nDiagonale: {r.Diagonale()}";

            Console.WriteLine(msg);
        }
    }
}
