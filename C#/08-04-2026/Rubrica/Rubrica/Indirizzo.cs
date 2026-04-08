using System;
using System.Collections.Generic;
using System.Text;

namespace Rubrica
{
    internal class Indirizzo
    {
        // Proprietà per rappresentare i dettagli dell'indirizzo
        public string Via { get; set; }
        public string Cap { get; set; }
        public string Citta { get; set; }
        public string Provincia { get; set; }

        // Costruttore con parametri per creare un indirizzo completo
        public Indirizzo(string via, string cap, string citta, string provincia) 
        {
            Via = via;
            Cap = cap;
            Citta = citta;
            Provincia = provincia;
        }

        // Costruttore senza parametri per creare un indirizzo vuoto
        public Indirizzo() 
        { 
            Via = "";
            Cap = "";
            Citta = "";
            Provincia = "";
        }

        // Override del metodo ToString per visualizzare l'indirizzo in modo leggibile
        public override string ToString()
        {
            return $"{Via}, {Cap}, {Citta}, {Provincia}";
        }
    }
}
