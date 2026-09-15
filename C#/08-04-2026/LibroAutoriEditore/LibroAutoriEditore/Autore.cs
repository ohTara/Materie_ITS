using System;
using System.Collections.Generic;
using System.Text;

namespace LibroAutoriEditore
{
    internal class Autore
    {
        // Parametri: Nome, Cognome, Email
        public string Nome { get; set; }
        public string Cognome { get; set; }
        public string Email { get; set; }

        // costruttore
        /*
         public Autore(string nome, string cognome, string email, string v, string v1)
        {
            Nome = nome;
            Cognome = cognome;
            Email = email;
        }
        */
        // Nominativo: iniziale del nome + cognome
        public string Nominativo()
        {
            return $"{Nome[0]}. {Cognome}";
        }

        // ToString: nome completo
        public override string ToString()
        {
            return $"{Nome} {Cognome}";
        }
    }
}
