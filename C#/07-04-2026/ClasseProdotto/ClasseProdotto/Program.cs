namespace ClasseProdotto
{
    internal class Program
    {
        static void Main()
        {
            // Istanzia due oggetti di tipo Prodotto
            Prodotto prodotto1 = new Prodotto
            {
                Codice = 101,
                Denominazione = "Laptop",
                Descrizione = "Laptop ad alte prestazioni per professionisti",
                Prezzo = 1299.99,
                Giacenza = 5
            };

            Prodotto prodotto2 = new Prodotto
            {
                Codice = 102,
                Denominazione = "Mouse",
                Descrizione = "Mouse wireless ergonomico",
                Prezzo = 29.99,
                Giacenza = 0
            };

            // Stampa lineare
            Console.WriteLine("=== STAMPA LINEARE ===\n");
            prodotto1.StampaLineare();
            prodotto2.StampaLineare();

            // Stampa dettaglio
            Console.WriteLine("\n=== STAMPA DETTAGLIO ===\n");
            prodotto1.StampaDettaglio();
            prodotto2.StampaDettaglio();

            // Test ToString()
            Console.WriteLine("=== TOSTRING ===\n");
            Console.WriteLine(prodotto1.ToString());
            Console.WriteLine(prodotto2.ToString());

            // Test metodi di stato giacenza
            Console.WriteLine("\n=== STATO GIACENZA ===\n");
            Console.WriteLine($"Prodotto 1 - In bassa giacenza: {prodotto1.GiacenzaBassa()}");
            Console.WriteLine($"Prodotto 1 - In scorta (>=10): {prodotto1.InScortaOvvero()}");
            Console.WriteLine($"Prodotto 1 - Esaurito: {prodotto1.EsauritoOvvero()}");

            Console.WriteLine();

            Console.WriteLine($"Prodotto 2 - In bassa giacenza: {prodotto2.GiacenzaBassa()}");
            Console.WriteLine($"Prodotto 2 - In scorta (>=10): {prodotto2.InScortaOvvero()}");
            Console.WriteLine($"Prodotto 2 - Esaurito: {prodotto2.EsauritoOvvero()}");

            // Test CalcolaValoreScorta
            Console.WriteLine($"\n=== VALORE SCORTA ===\n");
            Console.WriteLine($"Valore scorta Prodotto 1: €{prodotto1.CalcolaValoreScorta():F2}");
            Console.WriteLine($"Valore scorta Prodotto 2: €{prodotto2.CalcolaValoreScorta():F2}");
        }
    }

}