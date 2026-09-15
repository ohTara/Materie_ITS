using LibroAutoriEditore;

public class Program
{
    public static void Main(string[] args)
    {
        // Creo gli autori
        Autore a1 = new Autore
        {
            Nome = "Mario",
            Cognome = "Rossi",
            Email = "mario@email.it"
        };
        Autore a2 = new Autore
        {
            Nome = "Luigi",
            Cognome = "Verdi",
            Email = "luigi@email.it"
        };

        // Creo l'editore
        Indirizzo indEd = new Indirizzo
        {
            Via = "Via Roma 1",
            Cap = "20100",
            Citta = "Milano",
            Provincia = "MI"
        };

        Indirizzo indEd2 = new Indirizzo
        {
            Via = "Via Napoli 10",
            Cap = "80100",
            Citta = "Napoli",
            Provincia = "NA"
        };
        Editore ed = new Editore
        {
            RagioneSociale = "Mondadori",
            Indirizzo = indEd,
            Telefono = "02-1234567",
            Email = "info@mondadori.it",
        };

        Editore ed2 = new Editore
        {
            RagioneSociale = "Feltrinelli",
            Indirizzo = indEd2,
            Telefono = "081-7654321",
            Email = "info@feltrinelli.it"
        };

        // Creo il libro con entrambi gli autori
        Libro libro = new()
        {
            Isbn = "978-88-04-12345-6",
            Titolo = "Introduzione al C#",
            Autori = new() { a1, a2 },
            Editore = ed,
            NumeroPagine = 320,
            AnnoPubblicazione = 2024
        };
        Libro libro2 = new()
        {
            Isbn = "978-88-04-54321-0",
            Titolo = "Avanzato C#",
            Autori = new() { a1 },
            Editore = ed2,
            NumeroPagine = 450,
            AnnoPubblicazione = 2025
        };


        libro.StampaDettaglio();
        Console.WriteLine("\n-----------------------------\n");
        libro2.StampaDettaglio();

    }
}