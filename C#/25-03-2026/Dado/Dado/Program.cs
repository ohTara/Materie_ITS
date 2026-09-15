Console.WriteLine("Lancio di un dado");

int faccia = 0;

Random random = new Random();

faccia = random.Next(6)+1;
Console.WriteLine(faccia);
