using System;
using System.Collections.Generic;
using System.Text;

namespace EsercizioSolidi
{
    internal class Piramide : Solidi
    {
        /*
         * Rappresenta una piramide quadrata, un solido geometrico con una base quadrata e quattro facce triangolari.
         * Formule:
         *  Volume = (Base^2 * Altezza) / 3
         *  Area Superficie = Base^2 + 2 * Base * Altezza
         *  Perimetro Base = 4 * Base
         *  Diagonale = √2 * Base (diagonale della base quadrata)
         *  Apotema (a) = √((Base/2)^2 + Altezza^2) (altezza della faccia triangolare)
         */

        // Proprietà specifiche della piramide
        public double Base { get; private set; }
        public double Altezza { get; private set; }
        public int NumeroLati { get; private set; }

        // Costruttore
        public Piramide(double baseLato, double altezza, int numeroLati, string unita = "cm") : base($"Piramide (base {numeroLati} lati)", unita)
        {
            if (numeroLati == 0)
                throw new ArgumentException("Il numero di lati deve essere maggiore di zero.", nameof(numeroLati));
            if (baseLato <= 0)
                throw new ArgumentException("La base deve essere maggiore di zero.", nameof(baseLato));
            if (altezza <= 0)
                throw new ArgumentException("L'altezza deve essere maggiore di zero.", nameof(altezza));
            Base = baseLato;
            Altezza = altezza;
            NumeroLati = numeroLati;
        }

        // Implementazione dei metodi astratti

        public double CalcolaAreaBase()
            => (CalcolaPerimetroBase() * CalcolaApotemaPiramide()) / 2;
        public double CalcolaApotemaBase()
            => Base / (2 * Math.Tan(Math.PI / NumeroLati));
        public double CalcolaApotemaPiramide()
            => Math.Sqrt(Math.Pow(Altezza, 2) + Math.Pow(CalcolaApotemaBase(), 2));
        public override double CalcolaVolume()
            => (CalcolaAreaBase() * Altezza) / 3;

        public override double CalcolaAreaSuperficie()
            => (CalcolaAreaBase() + (CalcolaPerimetroBase() * CalcolaApotemaPiramide()) / 2);

        public override double CalcolaPerimetroBase()
            => NumeroLati * Base;

        // Diagonale della base quadrata
        public override double? CalcolaDiagonale()
        {
            if (NumeroLati == 4)
                return Math.Sqrt(2) * Base;
            return null;
        }

        // Mostra i parametri specifici della piramide
        protected override void MostraParametri()
        {
            Console.WriteLine($"  {"Numero Lati",-22} {NumeroLati,10}");
            Console.WriteLine($"  {"Lato Base",-22} {Base,10:F2}");
            Console.WriteLine($"  {"Altezza",-22} {Altezza,10:F2}");
            Console.WriteLine($"  {"Apotema Piramide",-22} {CalcolaApotemaPiramide(),10:F2}");
        }
    }
}
