using System;
using System.Collections.Generic;
using System.Text;

namespace ClasseEmail
{
    internal enum Priorità
    {
        BASSA,
        NORMALE,
        ALTA
    }

    internal class Email
    {
        private string _da;
        private string _a;
        private string _cc;
        private string _bcc;

        public string DA
        {
            get { return _da; }
            set
            {
                // Validazione: un solo indirizzo email
                if (!string.IsNullOrEmpty(value) && value.Contains(","))
                    throw new ArgumentException("DA può contenere solo un indirizzo email");
                _da = value;
            }
        }

        public string A
        {
            get { return _a; }
            set
            {
                // Validazione: un solo indirizzo email
                if (!string.IsNullOrEmpty(value) && value.Contains(","))
                    throw new ArgumentException("A può contenere solo un indirizzo email");
                _a = value;
            }
        }

        public string CC
        {
            get { return _cc; }
            set
            {
                // Validazione: un solo indirizzo email (opzionale)
                if (!string.IsNullOrEmpty(value) && value.Contains(","))
                    throw new ArgumentException("CC può contenere solo un indirizzo email");
                _cc = value;
            }
        }

        public string BCC
        {
            get { return _bcc; }
            set
            {
                // Validazione: un solo indirizzo email (opzionale)
                if (!string.IsNullOrEmpty(value) && value.Contains(","))
                    throw new ArgumentException("BCC può contenere solo un indirizzo email");
                _bcc = value;
            }
        }

        public string Oggetto { get; set; }

        public string Messaggio { get; set; }

        public DateTime? Data { get; set; }

        public Priorità Priorità { get; set; }

        // Costruttore con valori di default
        public Email(string da, string a, string cc = "", string bcc = "", string oggetto = "",
                     string messaggio = "", DateTime? data = null, Priorità priorità = Priorità.NORMALE)
        {
            DA = da;
            A = a;
            CC = cc;
            BCC = bcc;
            Oggetto = oggetto;
            Messaggio = messaggio;
            Data = data ?? DateTime.Now;  // Se null, usa la data odierna
            Priorità = priorità;
        }

        // Metodo ToString
        public override string ToString()
        {
            return $"DA: {DA}\nA: {A}\nCC: {CC}\nBCC: {BCC}\nOggetto: {Oggetto}\n" +
                   $"Messaggio: {Messaggio}\nData: {Data:dd/MM/yyyy HH:mm}\nPriorità: {Priorità}";
        }
    }
}
