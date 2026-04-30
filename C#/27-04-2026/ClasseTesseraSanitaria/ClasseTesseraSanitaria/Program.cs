using ClasseTesseraSanitaria;

Console.WriteLine("Istanze di oggetti di tipo TesseraSanitaria");

TesseraSanitaria tessera1 = new TesseraSanitaria("Mario", "Rossi", "RSSMRA80A01H501U", "1234567890", "Roma", "RM", new DateOnly(1980, 1, 1), new DateTime(2026, 05, 25), Sesso.M, "IST12345", "SSN-INDSA-MIN 22003");
TesseraSanitaria tessera2 = new TesseraSanitaria("Luigi", "Bianchi", "BNCLGU85B02F205X", "0987654321", "Milano", "MI", new DateOnly(1995, 2, 2), new DateTime(2026, 6, 30), Sesso.M, "IST54321", "SSN-INDSA-MIN 22004");


Console.WriteLine(tessera1);
Console.WriteLine(tessera2);    