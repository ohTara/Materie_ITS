using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;

namespace ClasseProdotto
{
    internal class Prodotto
    {
        public int Codice { get; set; }
        public string Descrizione { get; set; }

        public string Denominazione { get; set; }

        public double Prezzo { get; set; }

        public int Giacenza { get; set; }
        
        // metodi 

        public bool IsInScorta()
        {
            return Giacenza > 0 && Giacenza < 10;
        }

        public bool IsEsaurito()
        {
            return Giacenza == 0;
        }
         public double CalcolaValoreScorta()
        {
            return Prezzo * Giacenza;
        }

        // metodi "usa e getta" per visualizzare le informazioni del prodotto
        // Method to check if product is in stock (quantity between 1 and 9)
        public bool GiacenzaBassa()
        {
            return Giacenza >= 1 && Giacenza <= 9;
        }

        // Method to check if product is in good stock
        public bool InScortaOvvero()
        {
            return Giacenza >= 10;
        }

        // Method to check if product is sold out
        public bool EsauritoOvvero()
        {
            return Giacenza == 0;
        }

        // Linear format printing
        public void StampaLineare()
        {
            Console.WriteLine($"[{Codice}] {Denominazione} - €{Prezzo:F2} - Qty: {Giacenza}");
        }

        // Detailed format printing
        public void StampaDettaglio()
        {
            Console.WriteLine($"Codice: {Codice}");
            Console.WriteLine($"Nome: {Denominazione}");
            Console.WriteLine($"Descrizione: {Descrizione}");
            Console.WriteLine($"Prezzo: €{Prezzo:F2}");
            Console.WriteLine($"Giacenza: {Giacenza} unità");
            Console.WriteLine($"Stato: {GetStockStatusDetail()}");
            Console.WriteLine();
        }

        // Helper method for detailed status
        private string GetStockStatusDetail()
        {
            if (EsauritoOvvero())
                return "ESAURITO";
            else if (GiacenzaBassa())
                return "BASSA GIACENZA";
            else
                return "DISPONIBILE";
        }

        // Override ToString method
        public override string ToString()
        {
            return $"Prodotto: {Denominazione} (cod. {Codice}) - Prezzo: €{Prezzo:F2} - Disponibilità: {Giacenza} pz";
        }
    }
}
