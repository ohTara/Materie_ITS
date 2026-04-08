using System;
using System.Collections.Generic;
using System.Text;

namespace Rubrica
{
    internal class Contatto
    {
        // Proprietà per rappresentare i dettagli del contatto
        public string Nome { get; set; }
        public string Cognome { get; set; }
        public string Telefono { get; set; }
        public string Email { get; set; }
        public Indirizzo Indirizzo { get; set; }

        // costruttore con parametri

        public Contatto(string nome, string cognome, string telefono, string email, Indirizzo indirizzo)
        {
            Nome = nome;
            Cognome = cognome;
            Telefono = telefono;
            Email = email;
            Indirizzo = indirizzo;
        }
        // costruttore per creare un contatto con solo nome e cognome
        public Contatto(string nome, string cognome)
        {
            Nome = nome;
            Cognome = cognome;
        }
        // Metodo per visualizzare la scheda completa del contatto
        public string SchedaCompleta ()
        {
            return $"Nome: {Nome}\nCognome: {Cognome}\nTelefono: {Telefono}\nEmail: {Email}\nIndirizzo: {Indirizzo}";
        }
    }
}
