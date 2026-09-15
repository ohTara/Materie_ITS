using System;
using System.Security.Cryptography.X509Certificates;

public class HardDisk
{

	// attributi

	private string marca;
	private int velocita;
	private int tempoAccesso;
	private int capacita;

    // costruttore
    public HardDisk(string marca, int velocità, int tempoAccesso, int capacita)
	{
		this.marca = marca;
		this.capacita = capacita;
		this.tempoAccesso = tempoAccesso;
		this.velocita = velocità;
    }

	public int CalcolaPunteggio()
	{
		return (velocita*1)+(tempoAccesso*-200)+(capacita*500);
	}

    // --- ToString per stampare le info ---
    public override string ToString()
    {
        return $"Marca: {marca} | Velocità: {velocita} RPM | " +
               $"Tempo accesso: {tempoAccesso} ms | Capacità: {capacita} GB | " +
               $"Punteggio: {CalcolaPunteggio()}";
    }
}
