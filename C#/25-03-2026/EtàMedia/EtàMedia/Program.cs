/*
  Trovale l'età media tra un gruppo di persone
*/

int somma = 0;
int conta = 0;
int etaPersona;
Console.WriteLine("Inserire il numero di persone del gruppo");
int numeroPersone = int.Parse(Console.ReadLine());

for (int i=0; i < numeroPersone; i++)
{
    Console.WriteLine("Inserire l'età della persona");
    etaPersona = int.Parse(Console.ReadLine());
    somma += etaPersona;
    conta++;
}

if  (conta > 0)
{
    float media = somma / conta;
    Console.WriteLine($"L'età media è: {media}");
} else
{
    Console.WriteLine("Nessun numero valido inserito");
}