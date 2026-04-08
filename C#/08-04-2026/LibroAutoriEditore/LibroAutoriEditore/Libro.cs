using System;
using System.Collections.Generic;
using System.Text;

namespace LibroAutoriEditore
{
    internal class Libro
    {
        // Parametri: ISBN, Titolo, Autori (lista), Editore, Numero Pagine, Anno Pubblicazione
        public string Isbn { get; set; }
        public string Titolo { get; set; }
        public List<Autore> Autori { get; set; }
        public Editore Editore { get; set; }
        public int NumeroPagine { get; set; }
        public int AnnoPubblicazione { get; set; }

        // costruttore
        /*
        public Libro(string isbn, string titolo, List<Autore> autori, Editore editore, int numeroPagine, int annoPubblicazione)
        {
            Isbn = isbn;
            Titolo = titolo;
            Autori = autori;
            Editore = editore;
            NumeroPagine = numeroPagine;
            AnnoPubblicazione = annoPubblicazione;
        }
        */

        // CalcolaPrezzo: prezzo base 5.05 € + 0.05 € per pagina
        public double CalcolaPrezzo()
        {
            return 5.05 + (NumeroPagine * 0.05);
        }

        // StampaDettaglio: stampa tutte le informazioni del libro, incluso il prezzo calcolato
        public void StampaDettaglio()
        {
            string autoriStr = string.Join(", ", Autori.ConvertAll(a => a.Nominativo()));

            Console.WriteLine($"ISBN: {Isbn}");
            Console.WriteLine($"Titolo: {Titolo}");
            Console.WriteLine($"Autori: {autoriStr}");
            Console.WriteLine($"Editore: {Editore}");
            Console.WriteLine($"Numero Pagine: {NumeroPagine}");
            Console.WriteLine($"Anno Pubblicazione: {AnnoPubblicazione}");
            Console.WriteLine($"Prezzo: {CalcolaPrezzo():0.00} €");
        }
    }
}
