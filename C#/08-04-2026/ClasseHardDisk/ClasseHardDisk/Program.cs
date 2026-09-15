namespace ClasseHardDisk
{
    internal class Program
    {
        static void Main(string[] args)
        {
            // Istanziare 5 oggetti HardDisk con valori diversi
            HardDisk hardDisk1 = new HardDisk("Seagate", 7200, 5, 1000);
            HardDisk hardDisk2 = new HardDisk("Western Digital", 5400, 10, 2000);
            HardDisk hardDisk3 = new HardDisk("Samsung", 10000, 2, 500);
            HardDisk hardDisk4 = new HardDisk("Toshiba", 7200, 8, 1500);
            HardDisk hardDisk5 = new HardDisk("Hitachi", 5400, 12, 2500);

            // Stampare le informazioni di ogni HardDisk e il punteggio calcolato

            Console.WriteLine(hardDisk1.ToString());    // Il metodo ToString() dovrebbe essere implementato per restituire una stringa con le informazioni dell'HardDisk
            Console.WriteLine(hardDisk2.ToString());    // Viene usato implicitamente quando si passa l'oggetto a Console.WriteLine(), 
            Console.WriteLine(hardDisk3.ToString());    // quindi è importante che sia implementato correttamente per mostrare le informazioni desiderate, 
            Console.WriteLine(hardDisk4.ToString());    // non è necessario chiamarlo esplicitamente.
            Console.WriteLine(hardDisk5.ToString());
        }
    }
}