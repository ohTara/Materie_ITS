using System;
using System.Collections.Generic;
using System.Text;

namespace ClasseAuto
{
    internal class Auto
    {

        // proprietà
        public string Marca { get; set; }
        public string Modello { get; set; }
        public int Cilindrata { get; set; }
        public TipoCarburante Carburante { get; set; }
        public string Colore { get; set; }
        public int VelocitaAttuale { get; set; }

        // costruttore 
        public Auto(string marca, string modello, int cilindrata, TipoCarburante carburante, string colore)
        {
            Marca = marca;
            Modello = modello;
            Cilindrata = cilindrata;
            Carburante = carburante;
            Colore = colore;
        }

        // calcolo velocità massima (semplice formula: velocità massima = cilindrata / 10) + bonus tipo carburante
        public int VelocitaMax()
        {
            int velocita = Cilindrata / 10;
             
            switch(Carburante)
            {
                case TipoCarburante.benzina:
                    velocita += 30;
                    break;
                case TipoCarburante.diesel:
                    velocita += 20;
                    break;
                case TipoCarburante.gpl:
                    velocita -= 10;
                    break;
                case TipoCarburante.metano:
                    velocita -= 30;
                    break;
                default:
                    break;
            }
            return velocita;
        }

        public void Accelera()
        {
            VelocitaAttuale += 10;
        }

        public void Frena()
        {
            VelocitaAttuale -= 5;
        }

        // metodo per visualizzare le informazioni dell'auto
        public override string ToString()
        {
            return $"Marca: {Marca}, Modello: {Modello}, Cilindrata: {Cilindrata}cc, Carburante: {Carburante}, Colore: {Colore}, Velocità Massima: {VelocitaMax()} km/h";
        }

    }
}
