using System;
using System.Collections.Generic;

namespace EsercizioSolidi
{
    internal class Program
    {
        static void Main(string[] args)
        {
            // Per supportare i caratteri speciali
            Console.OutputEncoding = System.Text.Encoding.UTF8;

            while (true)
            {
                Console.WriteLine("\n==================================");
                Console.WriteLine("    CALCOLATORE DI SOLIDI 3D");
                Console.WriteLine("==================================");
                Console.WriteLine("1. Cubo");
                Console.WriteLine("2. Sfera");
                Console.WriteLine("3. Piramide (base poligonale)");
                Console.WriteLine("4. Cono");
                Console.WriteLine("5. Cilindro");
                Console.WriteLine("0. Esci");
                Console.Write("\nScegli un'opzione: ");

                string scelta = Console.ReadLine();

                if (scelta == "0")
                {
                    Console.WriteLine("Uscita in corso...");
                    break;
                }

                try
                {
                    Solidi solido = null;

                    switch (scelta)
                    {
                        case "1":
                            Console.Write("Inserisci il lato del cubo (cm): ");
                            double latoCubo = Convert.ToDouble(Console.ReadLine());
                            solido = new Cubo(latoCubo);
                            break;

                        case "2":
                            Console.Write("Inserisci il raggio della sfera (cm): ");
                            double raggioSfera = Convert.ToDouble(Console.ReadLine());
                            solido = new Sfera(raggioSfera);
                            break;

                        case "3":
                            Console.Write("Quanti lati ha la base? (es. 4 per quadrata): ");
                            int lati = Convert.ToInt32(Console.ReadLine());
                            Console.Write("Inserisci la lunghezza del lato (cm): ");
                            double latoBase = Convert.ToDouble(Console.ReadLine());
                            Console.Write("Inserisci l'altezza della piramide (cm): ");
                            double altezzaPir = Convert.ToDouble(Console.ReadLine());
                            solido = new Piramide(latoBase, altezzaPir, lati);
                            break;

                        case "4":
                            Console.Write("Inserisci il raggio della base (cm): ");
                            double raggioCono = Convert.ToDouble(Console.ReadLine());
                            Console.Write("Inserisci l'altezza del cono (cm): ");
                            double altezzaCono = Convert.ToDouble(Console.ReadLine());
                            solido = new Cono(raggioCono, altezzaCono);
                            break;

                        case "5":
                            Console.Write("Inserisci il raggio della base (cm): ");
                            double raggioCilindro = Convert.ToDouble(Console.ReadLine());
                            Console.Write("Inserisci l'altezza del cilindro (cm): ");
                            double altezzaCilindro = Convert.ToDouble(Console.ReadLine());
                            solido = new Cilindro(raggioCilindro, altezzaCilindro);
                            break;

                        default:
                            Console.WriteLine("Scelta non valida. Riprova.");
                            continue;
                    }

                    // Se tutto è andato bene, mostriamo le info
                    solido?.MostraInfo();
                }
                catch (FormatException)
                {
                    Console.WriteLine("\n[ERRORE] Devi inserire un numero valido! Usa la virgola per i decimali.");
                }
                catch (ArgumentException ex)
                {
                    Console.WriteLine($"\n[ERRORE] {ex.Message}");
                }

                Console.WriteLine("\nPremi Invio per continuare...");
                Console.ReadLine();
                Console.Clear(); // Pulisce lo schermo per il prossimo calcolo
            }
        }
    }
}