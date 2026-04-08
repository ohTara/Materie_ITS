using System;
using System.Collections.Generic;
using System.Text;

namespace LibroAutoriEditore
{
    internal class Indirizzo
    {
        // Parametri: Via, CAP, Città, Provincia
        public string Via { get; set; }
        public string Cap { get; set; }
        public string Citta { get; set; }
        public string Provincia { get; set; }

        // Costruttore
        /*
         public Indirizzo(string via, string cap, string citta, string provincia)
        {
            Via = via;
            Cap = cap;
            Citta = citta;
            Provincia = provincia;
        }
        */

        // stampo dell'indirizzo
        public override string ToString()
        {
            return $"{Via}, {Cap} {Citta} ({Provincia})";
        }
    }
}
