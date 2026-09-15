using System;
using System.Collections.Generic;
using System.Text;

namespace ClasseTriangolo
{
    internal class Triangolo
    {
        //attributi
        private double lato1;

        public double Lato1
        {
            get { return lato1; }
            set { lato1 = value; }
        }

        private double lato2;

        public double Lato2
        {
            get { return lato2; }
            set { lato2 = value; }
        }

        private double lato3;

        public double Lato3
        {
            get { return lato3; }
            set { lato3 = value; }
        }

        // costruttore
        // metodo speciale - serve per costruire oggetti
        // specifica come vanno costruiti gli oggetti della classe

        //costruttore di default è spvrascrottp - sostituoto
        /*public Triangolo()
        {
            // codice 
        }
        */
        
        // costruttore con passaggio di parametri
        public Triangolo(double lato1, double lato2, double lato3)
        {
            this.lato1 = lato1;
            this.lato2 = lato2;
            this.lato3 = lato3;
            if (!isCostruibile())
            {
                throw new Exception("Impossibile costruire il triangolo");
            }
        }




        //metodi

        private bool isCostruibile()
        {
            return (lato1 + lato2 > lato3) && (lato1 + lato3 > lato2) && (lato2 + lato3 > lato1);
        }
        public double Perimetro()
        {
            return Lato1 + Lato2 + Lato3;
        }

        public double Area()
        {
            
            //formula di Erone
            double semiperimetro = Perimetro() / 2;
            return Math.Sqrt(semiperimetro * (semiperimetro - lato1) * (semiperimetro - lato2) * (semiperimetro - lato3));
        }
        public string TipoTriangolo()
        {
            if (lato1 == lato2 && lato2 == lato3)
            {
                return "Equilatero";
            }
            else if (lato1 == lato2 || lato2 == lato3 || lato1 == lato3)
            {
                return "Isoscele";
            }
            else
            {
                return "Scaleno";
            }
        }

        // metodi "Usa e getta"
        public string FormatoLineare()
        {
            return $", Lato1={Lato1}" +
                   $", Lato2={Lato2}" +
                   $", Lato3={Lato3}" +
                   $", Perimetro={Perimetro}" +
                   $", Area={Area}" +
                   $", Tipo={TipoTriangolo()}";
        }

        public string FormatoDettaglio()
        {
            return $"\n Lato1={Lato1}" +
                   $"\n Lato2={Lato2}" +
                   $"\n Lato3={Lato3}" +
                   $"\n Perimetro={Perimetro}" +
                   $"\n Area={Area}" +
                   $"\n Tipo={TipoTriangolo()}";
        }

    }
}
