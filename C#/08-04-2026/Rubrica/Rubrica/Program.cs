namespace Rubrica
{
    internal class Program
    {
        static void Main(string[] args)
        {
            // contatto 1 
            Indirizzo indirizzo = new Indirizzo("Via Roma", "00100", "Roma", "RM");
            Contatto contatto1 = new Contatto("Mario", "Rossi", "1234567890", "mario.rossi@example.com", indirizzo);
            
            // contatto 2 - solo nome e cognome
            Contatto contatto2 = new Contatto("Luigi", "Bianchi");

            Console.WriteLine(contatto1.SchedaCompleta());
            Console.WriteLine(contatto2.SchedaCompleta());
        }
    }
}
