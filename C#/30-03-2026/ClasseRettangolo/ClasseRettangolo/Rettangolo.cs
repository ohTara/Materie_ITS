 using System;
using System.Collections.Generic;
using System.Text;

namespace ClasseRettangolo
{
    internal class Rettangolo
    {
        // attributi
        private double _base;

        // proprietà
        public double Base
        {
            get { return _base; }
            set { _base = value;
                if (value < 0)
                    throw new Exception("Errore! Dato non valido");
            }
        }

        private double _altezza;

        public double Altezza
        {
            get { return _altezza; }
            set {  if (value < 0)
                    throw new Exception("Errore! Dato non valido");
                   _altezza = value; }

        }

        // metodi

        public double Area()
        {
            return Base * Altezza;
        }
         public double Perimetro()
        {
            return 2 * (Base + Altezza);
        }
        public double Diagonale()
        {
            return Math.Sqrt(Math.Pow(Base,2)+Math.Pow(Altezza,2));
        }
    }
}
  