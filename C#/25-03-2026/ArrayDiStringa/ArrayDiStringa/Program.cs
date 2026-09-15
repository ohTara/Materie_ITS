Console.WriteLine("Array di nomi di persone!");

// array di nomi di persone
Console.WriteLine("Array di nomi di persone!");

string[] nomiFemminili = {
    "Sofia", "Giulia", "Martina", "Sara", "Laura",
    "Valentina", "Federica", "Chiara", "Alessia", "Francesca",
    "Elena", "Silvia", "Roberta", "Paola", "Cristina",
    "Michela", "Daniela", "Elisa", "Simona", "Serena",
    "Beatrice", "Ilaria", "Giorgia", "Veronica", "Monica",
    "Claudia", "Stefania", "Angela", "Patrizia", "Lucia",
    "Maria", "Anna", "Rosa", "Carla", "Giovanna",
    "Teresa", "Carmela", "Nunzia", "Grazia", "Concetta",
    "Irene", "Eleonora", "Caterina", "Alessandra", "Mariana",
    "Viola", "Aurora", "Emma", "Alice", "Greta",
    "Noemi", "Camilla", "Ginevra", "Fiamma", "Rossella",
    "Ornella", "Miriam", "Letizia", "Sabrina", "Cinzia",
    "Lorena", "Antonella", "Gabriella", "Isabella", "Manuela",
    "Nadia", "Tiziana", "Viviana", "Wanda", "Zelinda",
    "Ada", "Bruna", "Diana", "Ester", "Fiorella",
    "Gemma", "Helga", "Ines", "Jolanda", "Katia",
    "Linda", "Marta", "Nora", "Olga", "Pia",
    "Rita", "Sonia", "Tamara", "Ursula", "Virginia",
    "Agata", "Bianca", "Cecilia", "Daria", "Enrica",
    "Fabiola", "Georgia", "Hanna", "Ivana", "Jessica"
};

string[] nomiMaschili = {
    "Marco", "Luca", "Matteo", "Davide", "Andrea",
    "Simone", "Stefano", "Alessandro", "Roberto", "Antonio",
    "Francesco", "Giovanni", "Paolo", "Luigi", "Riccardo",
    "Nicola", "Fabio", "Daniele", "Mauro", "Giorgio",
    "Alberto", "Enrico", "Claudio", "Massimo", "Bruno",
    "Carmelo", "Domenico", "Enzo", "Filippo", "Giacomo",
    "Lorenzo", "Mario", "Natale", "Oscar", "Pietro",
    "Quintino", "Renato", "Salvatore", "Tiziano", "Umberto",
    "Valerio", "Walter", "Xeno", "Yuri", "Zeno",
    "Adriano", "Benedetto", "Carlo", "Diego", "Emanuele",
    "Federico", "Gabriele", "Horatio", "Ivan", "Jacopo",
    "Kevin", "Leonardo", "Manuel", "Niccolò", "Ottavio",
    "Patrick", "Quirino", "Rodolfo", "Sergio", "Tommaso",
    "Ugo", "Vincenzo", "William", "Xavier", "Yassin",
    "Angelo", "Bernardo", "Cristian", "Dario", "Edoardo",
    "Franco", "Gianmarco", "Iacopo", "Jonathan", "Karim",
    "Leandro", "Mirko", "Nando", "Orlando", "Primo",
    "Renzo", "Silvio", "Tullio", "Ubaldo", "Virgilio",
    "Achille", "Biagio", "Cosimo", "Donato", "Ettore",
    "Fausto", "Gerardo", "Ilario", "Jonatan", "Kristian"
};

Console.WriteLine("\n--- Nomi Femminili ---");
foreach (string nome in nomiFemminili)
    Console.WriteLine(nome);

Console.WriteLine("\n--- Nomi Maschili ---");
foreach (string nome in nomiMaschili)
    Console.WriteLine(nome);
// Array pre confezionato

string[] nomi = { "Giulio", "Matilde" };
foreach (string nom in nomi)
    Console.WriteLine(nom);
