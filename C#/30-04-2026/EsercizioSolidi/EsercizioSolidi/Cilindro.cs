using System;
using System.Collections.Generic;
using System.Text;

namespace EsercizioSolidi
{
    internal class Cilindro : Solidi
    {
        /*
         * Rappresenta un cilindro, un solido geometrico con due basi circolari e una superficie laterale curva.
         * Formule:
         *  Volume = π * raggio^2 * altezza
         *  Area Superficie = 2 * π * raggio * (raggio + altezza)
         *  Perimetro Base = 2 * π * raggio
         *  Diagonale = altezza (non ha senso per un cilindro, quindi non implementiamo CalcolaDiagonale())
         */

        // Proprietà specifiche del cilindro
        public double Raggio { get; private set; }
        public double Altezza { get; private set; }

        // Costruttore
        public Cilindro(double raggio, double altezza) : base("Cilindro")
        {
            if (altezza <= 0)
                throw new ArgumentException("L'altezza deve essere maggiore di zero.", nameof(altezza));
            if (raggio <= 0)
                throw new ArgumentException("Il raggio deve essere maggiore di zero.", nameof(raggio));
            Raggio = raggio;
            Altezza = altezza;
        }

        // Implementazione dei metodi astratti
        public override double CalcolaVolume()
            => Math.PI * Math.Pow(Raggio, 2) * Altezza;

        public override double CalcolaAreaSuperficie()
            => 2 * Math.PI * Raggio * (Raggio + Altezza);

        public override double CalcolaPerimetroBase()
            => 2 * Math.PI * Raggio;

        // Diagonale del parallelepipedo circoscritto 
        public override double? CalcolaDiagonale()
            => Math.Sqrt(4 * Math.Pow(Raggio, 2) + Math.Pow(Altezza, 2));

        // Mostra i parametri specifici del cilindro
        protected override void MostraParametri()
        {
            Console.WriteLine($"  {"Raggio",-22} {Raggio,10:F2}");
            Console.WriteLine($"  {"Altezza",-22} {Altezza,10:F2}");
        }

    }
}
