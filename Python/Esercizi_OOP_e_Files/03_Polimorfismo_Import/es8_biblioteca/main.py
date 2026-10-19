"""
Autore: Luca Tarallo
Data: 18/10/2026

Titolo: Sistema modulare per gestione biblioteca - File 3: main.py
        Programma principale che importa le classi dai moduli media e biblioteca, crea una
        biblioteca, aggiunge libri e DVD, prova tutti i metodi e stampa catalogo e statistiche.
"""
from media import Libro, DVD
from biblioteca import Biblioteca

"""
Programma principale
Crea la biblioteca con valori hard-coded (nessun input da tastiera) e testa tutti i metodi.
"""
# Sezione di input Dati
# (nessun input da tastiera: le classi sono istanziate in modalità hard-coded)

# Inizializzazioni variabili
biblioteca = Biblioteca()   # catalogo su cui lavorare
autore_cercato = "Orwell"   # autore usato per la ricerca

# Elaborazione
biblioteca.aggiungi_media(Libro("1984", "George Orwell", 1949, 328))
biblioteca.aggiungi_media(DVD("Inception", "Christopher Nolan", 2010, 148))
biblioteca.aggiungi_media(Libro("Il Nome della Rosa", "Umberto Eco", 1980, 512))

# Sezione di output
biblioteca.stampa_catalogo()

numero_libri, numero_dvd = biblioteca.get_statistiche()
print("=== STATISTICHE ===")
print("Libri:", numero_libri)
print("DVD:", numero_dvd)
print("Totale media:", numero_libri + numero_dvd)

print(f'=== RICERCA PER AUTORE "{autore_cercato}" ===')
for media in biblioteca.cerca_per_autore(autore_cercato):
    print(media)

# Eventuali sotto processi di Elaborazione: test dei metodi rimanenti e dei casi limite
print('=== RICERCA PER AUTORE "Tolkien" (nessun risultato) ===')
risultati = biblioteca.cerca_per_autore("Tolkien")
if len(risultati) == 0:
    print("Nessun media trovato")

print('=== RIMOZIONE DI "Inception" ===')
print("Rimosso:", biblioteca.rimuovi_media("Inception"))               # atteso True
print("Rimozione di un titolo inesistente:", biblioteca.rimuovi_media("Dune"))  # atteso False
biblioteca.stampa_catalogo()
numero_libri, numero_dvd = biblioteca.get_statistiche()
print(f"Statistiche aggiornate -> Libri: {numero_libri}, DVD: {numero_dvd}")

print("=== BIBLIOTECA VUOTA ===")
Biblioteca().stampa_catalogo()
