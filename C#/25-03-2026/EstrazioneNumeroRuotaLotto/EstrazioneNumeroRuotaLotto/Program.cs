Console.WriteLine("Estrazione numeri ruota lotto!");

int e1, e2, e3, e4, e5;

Random random = new Random();

/*
 * e1= random.Next(90)+1;

do
{
    e2 = random.Next(90) + 1;
}while(e2==e1);

do
{
    e3 = random.Next(90)+1;
}
while (e1==e3 || e2==e3);

do
{
    e4 = random.Next(90) + 1;
}
while (e1 == e4 || e2 == e4 || e3==4);


do
{
    e5 = random.Next(90) + 1;
}
while (e5 == e1 || e5==e2 || e5 == e3 || e5==e4);

*/

do
{
    e1 = random.Next(90) + 1;
    e2 = random.Next(90) + 1;
    e3 = random.Next(90) + 1;
    e4 = random.Next(90) + 1;
    e5 = random.Next(90) + 1;
}
while (e5 == e1 || e5 == e2 || e5 == e3 || e5 == e4);

Console.WriteLine($"{e1} {e2} {e3} {e4} {e5}");