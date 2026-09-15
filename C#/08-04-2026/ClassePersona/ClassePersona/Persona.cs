using System;
using System.Collections.Generic;
using System.Data;
using System.Text;

namespace ClassePersona
{
    internal class Persona
    {
        public string nome { get; set; }
        public string cognome { get; set; }
        public int eta { get; set; }
        public string luogoNascita { get; set; }

        public DateTime dataNascita { get; set; }

        public TipoSesso Sesso { get; set; }

        // costruttore completo

        public Persona(string nome, string cognome, int eta, string luogoNascita, DateTime dataNascita, TipoSesso sesso)
        {
            this.nome = nome;
            this.cognome = cognome;
            this.eta = eta;
            this.luogoNascita = luogoNascita;
            this.dataNascita = dataNascita;
            this.Sesso = sesso;
        }

        // costruttore vuoto

        public Persona()
        {
            this.cognome = "";
            this.nome = "";
            this.dataNascita = DateTime.Now;
            this.luogoNascita = "";
            this.Sesso = TipoSesso.Maschio;
        }

        // --- Costruttore con solo Nome e Cognome ---
        public Persona(string nome, string cognome)
        {
            this.nome = nome;
            this.cognome = cognome;
            this.dataNascita = DateTime.Now;
            this.luogoNascita = "";
            this.Sesso = TipoSesso.Maschio;
        }

        // --- Costruttore con Nome, Cognome, DataNascita, LuogoNascita ---
        public Persona(string nome, string cognome, DateTime dataNascita, string luogoNascita)
        {
            this.nome = nome;
            this.cognome = cognome;
            this.dataNascita = dataNascita;
            this.luogoNascita = luogoNascita;
            this.Sesso = TipoSesso.Maschio;
        }

        // --- Costruttore completo ---
        public Persona(string nome, string cognome, DateTime dataNascita, string luogoNascita, TipoSesso sesso)
        {
            this.nome = nome;
            this.cognome = cognome;
            this.dataNascita = dataNascita;
            this.luogoNascita = luogoNascita;
            this.Sesso = sesso;
        }
        public int Eta()
        {
            int eta = DateTime.Now.Year - dataNascita.Year;
            // Se il compleanno non è ancora passato quest'anno, sottrai 1
            if (DateTime.Now < dataNascita.AddYears(eta))
                eta--;
            return eta;
        }

        public void StampaLineare()
        {
            string luogo = luogoNascita != "" ? $"a {luogoNascita} " : "";
            Console.WriteLine($"{cognome} {nome}, {Eta()} anni, nato {luogo}il {dataNascita:dd/MM/yyyy}, sesso: {Sesso}");
        }

        public void StampaDettagliata()
        {
            Console.WriteLine($"Nome: {this.nome}");
            Console.WriteLine($"Cognome: {this.cognome}");
            Console.WriteLine($"Età: {Eta()} anni");          // <-- Eta() non this.eta
            Console.WriteLine($"Luogo di nascita: {this.luogoNascita}");
            Console.WriteLine($"Data di nascita: {this.dataNascita.ToShortDateString()}");
            Console.WriteLine($"Sesso: {this.Sesso}");
        }

        public override string ToString()
        {
            string luogo = luogoNascita != "" ? $"a {luogoNascita} " : "";
            return $"{this.cognome} {this.nome}, {Eta()} anni, nato {luogo}il {this.dataNascita:dd/MM/yyyy}, sesso: {this.Sesso}";
        }

    }
}