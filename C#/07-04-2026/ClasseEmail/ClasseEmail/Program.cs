using System;

namespace ClasseEmail
{
    internal class Program
    {
        static void Main()
        {
            // Email 1 - Priorità BASSA
            Email email1 = new Email(
                da: "mario.rossi@example.com",
                a: "luigi.bianchi@example.com",
                cc: "info@example.com",
                bcc: "",
                oggetto: "Riunione di lavoro",
                messaggio: "Ti allego il documento richiesto.",
                data: new DateTime(2024, 12, 15, 10, 30, 0),
                priorità: Priorità.BASSA
            );

            // Email 2 - Priorità NORMALE (default)
            Email email2 = new Email(
                da: "responsabile@example.com",
                a: "team@example.com",
                oggetto: "Aggiornamento progetto",
                messaggio: "Il progetto sta procedendo secondo i piani."
            );

            // Email 3 - Priorità ALTA
            Email email3 = new Email(
                da: "admin@example.com",
                a: "direttore@example.com",
                cc: "responsabile@example.com",
                oggetto: "URGENTE: Problema critico risolto",
                messaggio: "Il problema di sistema è stato risolto. Sistema ripristinato.",
                priorità: Priorità.ALTA
            );

            // Visualizza le tre email
            Console.WriteLine("========== EMAIL 1 ==========\n");
            Console.WriteLine(email1);
            Console.WriteLine("\n\n========== EMAIL 2 ==========\n");
            Console.WriteLine(email2);
            Console.WriteLine("\n\n========== EMAIL 3 ==========\n");
            Console.WriteLine(email3);

            // Test validazione
            Console.WriteLine("\n\n========== TEST VALIDAZIONE ==========\n");
            try
            {
                Email emailScorretta = new Email(
                    da: "test@example.com",
                    a: "user1@example.com, user2@example.com"  // Errore: due indirizzi
                );
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"❌ Il programma ha bloccato un errore correttamente: {ex.Message}");
            }

            Console.WriteLine("\n✅ Esecuzione completata con successo!");

            // =========================================================
            // LA RIGA MAGICA: ferma il programma finché non premi Invio
            // =========================================================
            Console.WriteLine("\nPremi INVIO sulla tastiera per chiudere questa finestra...");
            Console.ReadLine();
        }
    }
}