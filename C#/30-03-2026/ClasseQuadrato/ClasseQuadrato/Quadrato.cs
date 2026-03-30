using System;
using System.Collections.Generic;
using System.Text;

// "namespace" è un contenitore che permette di organizzare il codice in modo logico e di evitare conflitti di nomi tra classi, interfacce, ecc. In questo caso, "ClasseQuadrato" è il namespace che contiene la classe "Quadrato". La parola chiave "internal" indica che la classe "Quadrato" è accessibile solo all'interno dello stesso assembly (progetto) e non può essere utilizzata da altri assembly.

namespace ClasseQuadrato
{
    internal class Quadrato
    {
        // caratteristica 
        // attributi
        public double lato; // attributo che rappresenta la lunghezza del lato del quadrato
        // funzionalità
        
        // azioni

        // metodi
        public double Perimetro()
        {
            double p =  4 * lato; // calcola e restituisce il perimetro del quadrato
            return p;
        }

        public double Area()
        {
            double a = lato * lato; // calcola e restituisce l'area del quadrato
            return a;
        }

        public double Diagonale()
        {
            double d = lato * Math.Sqrt(2); // calcola e restituisce la lunghezza della diagonale del quadrato
            return d;
        }
    }
}