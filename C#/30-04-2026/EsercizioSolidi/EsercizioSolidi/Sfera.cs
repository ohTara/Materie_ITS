using System;
using System.Collections.Generic;
using System.Text;

namespace EsercizioSolidi
{
    /*
     * Rappresenta una sfera, un solido geometrico tridimensionale perfettamente simmetrico.
     * Formule: 
     *  Volume = (4/3) * π * raggio^3
     *  Area Superficie = 4 * π * raggio^2
     *  Perimetro Base = 2 * π * raggio (per il cerchio massimo della sfera)
     *  Diagonale = 2 * raggio (diametro della sfera)
     */
    internal class Sfera : Solidi
    {
        // Proprietà specifiche della sfera
        public double Raggio { get; private set; }

        // Costruttore
        public Sfera(double raggio) : base("Sfera")
        {
            if (raggio <= 0)
                throw new ArgumentException("Il raggio deve essere maggiore di zero.", nameof(raggio));
            Raggio = raggio;
        }

        // Implementazione dei metodi astratti

        public override double CalcolaAreaSuperficie()
            =>  4 * Math.PI * Math.Pow(Raggio, 2);

        // Cerchio massimo della sfera, quindi il perimetro della base è il perimetro del cerchio massimo
        public override double CalcolaPerimetroBase()
            => 2 * Math.PI * Raggio;

        public override double CalcolaVolume()
            => (4.0 / 3.0) * Math.PI * Math.Pow(Raggio, 3);

        // Diagonale della sfera non ha senso, quindi non implementiamo CalcolaDiagonale()
        public override double? CalcolaDiagonale() 
            => 2 * Raggio;

        protected override void MostraParametri()
        {
            Console.WriteLine($"  {"Raggio",-22} {Raggio,10:F2}");
        }
    }
}
