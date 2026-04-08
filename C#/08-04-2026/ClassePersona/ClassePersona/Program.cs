namespace ClassePersona
{
    internal class Program
    {
        static void Main(string[] args)
        {
            // Istanza 1 - costruttore senza parametri
            Persona p1 = new Persona();
            Console.WriteLine("-- P1 (senza parametri) --");
            Console.WriteLine(p1);

            // Istanza 2 - solo Nome e Cognome
            Persona p2 = new Persona("Mario", "Rossi");
            Console.WriteLine("\n-- P2 (Nome e Cognome) --");
            p2.StampaLineare();

            // Istanza 3 - Nome, Cognome, DataNascita, LuogoNascita
            Persona p3 = new Persona("Luigi", "Verdi", new DateTime(1990, 5, 15), "Milano");
            Console.WriteLine("\n-- P3 (senza Sesso) --");
            p3.StampaLineare();

            // Istanza 4 - tutti i dati
            Persona p4 = new Persona("Anna", "Bianchi", new DateTime(1985, 3, 22), "Roma", TipoSesso.Femmina);
            Console.WriteLine("\n-- P4 (completo) --");
            p4.StampaDettagliata();
        }
    }
}
