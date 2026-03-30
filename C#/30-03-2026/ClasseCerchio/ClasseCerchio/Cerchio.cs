using System;
using System.Collections.Generic;
using System.Text;

namespace ClasseCerchio
{
    internal class Cerchio
    {
        // attributi
        private double _raggio;
        
        // metodi 

        // getter
        public double GetRaggio()
        {
            return _raggio;
        }

        // setter 

        public void SetRaggio(double raggio) {
            if (raggio <= 0)
            {
                throw new Exception("Errore! Il raggio non può essere negativo.");
            }
            _raggio = raggio;
        }

        public double Diametro()
        {
            return 2 * _raggio;
        }

        public double Circonferenza()
        {
            return 2 * Math.PI * _raggio;
        }

        public double Area()
        {
            return Math.PI * Math.Pow(_raggio, 2);
        }
    }
}