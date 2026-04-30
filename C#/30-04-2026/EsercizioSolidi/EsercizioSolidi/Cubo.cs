using System;
using System.Collections.Generic;
using System.Text;

namespace EsercizioSolidi
{
    internal class Cubo : Solidi
    {
        /*
         * Rappresenta un cubo, un solido geometrico con sei facce quadrate uguali.
         * Formule:
         *  Volume = lato^3
         *  Area Superficie = 6 * lato^2
         *  Perimetro Base = 4 * lato
         *  Diagonale = lato * √2
         *  Diagonale Spaziale = lato * √3
         */

        // Proprietà specifiche del cubo
        public double Lato { get; private set; }

        // Costruttore
        public Cubo(double lato) : base("Cubo")
        {
            if (lato <= 0)
                throw new ArgumentException("Il lato deve essere maggiore di zero.", nameof(lato));
            Lato = lato;
        }

        // Implementazione dei metodi astratti
        public override double CalcolaVolume() 
            => Math.Pow(Lato, 3);
        public override double CalcolaAreaSuperficie() 
            => 6 * Math.Pow(Lato, 2);
        public override double CalcolaPerimetroBase() 
            => 4 * Lato;
        public override double? CalcolaDiagonale() 
            => Lato * Math.Sqrt(2);

        // Diagonale spaziale del cubo (non richiesta ma utile): av3
        public double? CalcolaDiagonaleSpaziale() 
            => Lato * Math.Sqrt(3);

        protected override void MostraParametri()
        {
            Console.WriteLine($"  {"Lato",-22} {Lato,10:F2}");
        }
    }
}