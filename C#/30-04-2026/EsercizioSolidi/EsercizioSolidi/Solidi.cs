using System;
using System.Collections.Generic;
using System.Text;

namespace EsercizioSolidi
{
    internal abstract class Solidi
    {
        /// Classe astratta base che rappresenta un solido geometrico.
        /// Ogni solido concreto deve implementare i metodi astratti.

        // proprietà 
        public string Nome { get; protected set; }
        public string Unita { get; protected set; }

        // Costruttore
        protected Solidi(string nome, string unita = "cm")
        {
            Nome = nome;
            Unita = unita;
        }

        // Metodi astratti obbligatori per ogni classe

        public abstract double CalcolaVolume();
        public abstract double CalcolaAreaSuperficie();
        public abstract double CalcolaPerimetroBase();

        // Metodi virtuali opzionali per i solidi che non hanno una base (come la sfera) o una diagonale (come il cubo)
        public virtual double? CalcolaDiagonale() 
            => null;

        // Metodi comuni a tutti i solidi
        public virtual void MostraInfo()
        {
            Console.WriteLine($"\n╔══════════════════════════════╗");
            Console.WriteLine($"  {Nome}");
            Console.WriteLine($"╚══════════════════════════════╝");
            MostraParametri();
            Console.WriteLine($"  {"Volume",-22} {CalcolaVolume(),10:F2} {Unita}");
            Console.WriteLine($"  {"Area Superficie",-22} {CalcolaAreaSuperficie(),10:F2} {Unita}");
            Console.WriteLine($"  {"Perimetro Base",-22} {CalcolaPerimetroBase(),10:F2} {Unita}");

            double? diag = CalcolaDiagonale();
            if (diag.HasValue)
                Console.WriteLine($"  {"Diagonale",-22} {diag.Value,10:F2} {Unita}");
        }

        protected virtual void MostraParametri() { }
        public override string ToString() => $"{Nome} [V={CalcolaVolume():F2}, A={CalcolaAreaSuperficie():F2}]";
    }
}
