using ClasseAuto;

public class Program
{
    public static void Main(string[] args)
    {
        Auto auto = new Auto("Ferrari", "F40", 3000, TipoCarburante.benzina, "Rosso");

        int scelta;

        do
        {
            // Stampa velocità attuale
            Console.WriteLine($"\nVelocità attuale: {auto.VelocitaAttuale} km/h");

            // Avviso se supera 130 km/h
            if (auto.VelocitaAttuale > 130)
                Console.WriteLine("Rallenta! Stai andando troppo forte");

            // Menu
            Console.WriteLine("1 - Accelera");
            Console.WriteLine("2 - Frena");
            Console.WriteLine("0 - Esci");
            Console.Write("Scelta: ");

            if (!int.TryParse(Console.ReadLine(), out scelta))
            {
                scelta = -1; // Valore non valido
            }

            switch (scelta)
            {
                case 1: auto.Accelera(); break;
                case 2: auto.Frena(); break;
                case 0: Console.WriteLine("Uscita dal programma."); break;
                default: Console.WriteLine("Scelta non valida!"); break;
            }

        } while (scelta != 0);
    }
}