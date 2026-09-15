using System;
using System.Collections.Generic;
using System.Text;

namespace LibroAutoriEditore
{
    internal class Editore
    {
        // Parametri: Ragione Sociale, Indirizzo, Telefono, Email, Sito Web
        public string RagioneSociale { get; set; }
        public Indirizzo Indirizzo { get; set; }
        public string Telefono { get; set; }
        public string Email { get; set; }

        // costruttore
        /*
        public Editore(string ragioneSociale, Indirizzo indirizzo, string telefono, string email, string sitoWeb)
        {
            RagioneSociale = ragioneSociale;
            Indirizzo = indirizzo;
            Telefono = telefono;
            Email = email;
            SitoWeb = sitoWeb;
        }
        */

        // ToString: ragione sociale
        public override string ToString()
        {
            return RagioneSociale;
        }
    }
}
