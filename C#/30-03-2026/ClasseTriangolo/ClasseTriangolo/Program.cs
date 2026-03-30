namespace ClasseTriangolo
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello, World!");

            var t = new Triangolo(3,4,5);

            string msg = $", Lato1={t.Lato1}" + 
                         $", Lato2={t.Lato2}" +
                         $", Lato3={t.Lato3}" +
                         $", Perimetro={t.Perimetro}" +
                         $", Area={t.Area}" +
                         $", Tipo={t.TipoTriangolo()}";
            Console.WriteLine(msg);

            var t2 = new Triangolo(4,4,5);

            //format lineare
            msg =  $", Lato1={t2.Lato1}" +
                   $", Lato2={t2.Lato2}" +
                   $", Lato3={t2.Lato3}" +
                   $", Perimetro={t2.Perimetro}" +
                   $", Area={t2.Area}" +
                   $", Tipo={t2.TipoTriangolo()}";

            Console.WriteLine(t2.FormatoLineare());

            var t3 = new Triangolo(4,4,4);
             Console.WriteLine(t3.FormatoDettaglio());
        }
    }
}
