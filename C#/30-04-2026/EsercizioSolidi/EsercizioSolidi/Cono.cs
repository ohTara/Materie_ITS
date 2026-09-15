using System;
using System.Collections.Generic;
using System.Text;

namespace EsercizioSolidi
{
    internal class Cono : Solidi
    {
        /*
         * Rappresenta un cono, un solido geometrico con una base circolare e una superficie laterale curva.
         * Formule:
         *  Generatrice = √(raggio^2 + altezza^2)
         *  Volume = (1/3) * π * raggio^2 * altezza
         *  Area Superficie = π * raggio * (raggio + generatrice)
         *  Perimetro Base = 2 * π * raggio
         *  Diagonale = generatrice (non ha senso per un cono, quindi non implementiamo CalcolaDiagonale())
         */

        // Proprietà specifiche del cono
        public double Raggio { get; private set; }
        public double Altezza { get; private set; }

        // Calcola la generatrice del cono

        public double CalcolaGeneratrice()
            => Math.Sqrt(Math.Pow(Raggio, 2) + Math.Pow(Altezza, 2));

        // Costruttore
        public Cono(double raggio, double altezza) : base("Cono")
        {
            if (altezza < 0)
                throw new ArgumentException("L'altezza deve essere maggiore di zero.", nameof(altezza));
            if (raggio < 0)
                throw new ArgumentException("Il raggio deve essere maggiore di zero.", nameof(raggio));
            Raggio = raggio;
            Altezza = altezza;
        }

        // Implementazione dei metodi astratti
        public override double CalcolaVolume()
            => (1.0 / 3.0) * Math.PI * Math.Pow(Raggio, 2) * Altezza;

        public override double CalcolaAreaSuperficie()
            => Math.PI * Raggio * (Raggio + CalcolaGeneratrice());
        
        public override double CalcolaPerimetroBase()
            => 2 * Math.PI * Raggio;

        public override double? CalcolaDiagonale()
            => CalcolaGeneratrice();

        protected override void MostraParametri()
        {
            Console.WriteLine($"  {"Raggio",-22} {Raggio,10:F2} {Unita}");
            Console.WriteLine($"  {"Altezza",-22} {Altezza,10:F2} {Unita}");
            Console.WriteLine($"  {"Generatrice",-22} {CalcolaGeneratrice(),10:F2} {Unita}");
        }
    }
}
