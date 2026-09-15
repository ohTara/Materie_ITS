namespace ClasseCerchio
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Istanza di Cerchio!");

            Cerchio c = new Cerchio();

            c.SetRaggio(-0.5);
            
            Console.WriteLine($"Raggio: {c.GetRaggio()}");
            Console.WriteLine($"Raggio: {c.Diametro()}");
            Console.WriteLine($"Raggio: {c.Circonferenza()}");
            Console.WriteLine($"Raggio: {c.Area()}");
        }
    }
}