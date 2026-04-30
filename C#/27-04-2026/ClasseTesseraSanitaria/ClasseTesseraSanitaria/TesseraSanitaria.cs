using System;
using System.Collections.Generic;
using System.Text;

namespace ClasseTesseraSanitaria
{
    internal class TesseraSanitaria
    {
        // proprietà
        public string CodiceFiscale { get; set; }
        public string NumeroIdentificativoTessera { get; set; }
        public string Nome { get; set; }
        public string Cognome { get; set; }
        public string LuogoNascita { get; set; }
        public string ProvinciaNascita { get; set; }
        public DateOnly DataNascita { get; set; }
        public DateTime DataScadenza { get; set; }
        public Sesso Sesso { get; set; }
        public required string NumeroIdentificativoIstituzione { get; set; }


        // costruttore

        public TesseraSanitaria(string codiceFiscale, string numeroIdentificativoTessera, string nome, string cognome, string luogoNascita, string provinciaNascita, DateOnly dataNascita, DateTime dataScadenza, Sesso sesso, string numeroIdentificativoIstituzione, string v)
        {
            CodiceFiscale = codiceFiscale;
            NumeroIdentificativoTessera = numeroIdentificativoTessera;
            Nome = nome;
            Cognome = cognome;
            LuogoNascita = luogoNascita;
            ProvinciaNascita = provinciaNascita;
            DataNascita = dataNascita;
            DataScadenza = dataScadenza;
            Sesso = sesso;
            NumeroIdentificativoIstituzione = numeroIdentificativoIstituzione;
        }

        
     


        // metodi
        public bool IsInScadenza()
        {
            DateTime oggi = DateTime.Now;
            DateTime verifica = DataScadenza.AddDays(-30);
            if (verifica < oggi)
                {
                return true;    // La tessera è in scadenza
            }
            else
                {
                return false;   // La tessera non è in scadenza
            }
            }

        public override string ToString()
        {
            return $"{{{nameof(CodiceFiscale)}={CodiceFiscale}" +
                $", {nameof(NumeroIdentificativoTessera)}={NumeroIdentificativoTessera}" +
                $", {nameof(Nome)}={Nome}" +
                $", {nameof(Cognome)}={Cognome}," +
                $", {nameof(LuogoNascita)}={LuogoNascita}" +
                $", {nameof(ProvinciaNascita)}={ProvinciaNascita}" +
                $", {nameof(DataNascita)}={DataNascita.ToString()}" +
                $", {nameof(DataScadenza)}={DataScadenza.ToString()}" +
                $", {nameof(Sesso)}={Sesso.ToString()}" +
                $", {nameof(NumeroIdentificativoIstituzione)}={NumeroIdentificativoIstituzione}}}";
        }
    }
}
