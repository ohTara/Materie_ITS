import express from 'express';
import bodyParser from 'body-parser';
import catalogoLibri from './model/catalogo.js';
import clientiFile from './model/clientiFile.js';

const app = express();
app.use(bodyParser.json());
const PORT = 3000;
const BASE_PATH = '/api/v1';

var catalogo = [...catalogoLibri];
var clienti = [...clientiFile];

// Avvio del server
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

// endpoint per restituire un testo di prova
app.get('/', (req, res) => {
    res.send('Benvenuto nella tua libreria online!');
});
// endpoint per restituire il catalogo dei libri
app.get(`${BASE_PATH}/libri`, (req, res) => {
    res.json(catalogo);
});
// endpoint per aggiungere un nuovo libro al catalogo
app.post(`${BASE_PATH}/libri`, (req, res) => {
    // Estrai i dati del nuovo libro dalla richiesta
    const nuovoLibro = req.body;
    
    if (!validaLibro(nuovoLibro)) {
        return res.status(400).json({ message: 'Dati del libro mancanti o non validi' });
    }

    // Genera un nuovo ID incrementale per il libro
    const maxId = catalogo.map(item => item.id).reduce((max, id) => Math.max(max, id), 0);
    nuovoLibro.id = maxId + 1; // Assegna un nuovo ID incrementale

    catalogo.push(nuovoLibro); // Aggiungi il nuovo libro al catalogo
    res.status(201).json(nuovoLibro);
});

// endpoint per aggiornare un libro esistente
app.put(`${BASE_PATH}/libri/:id`, (req, res) => {
    // Estrai l'ID del libro da aggiornare dalla richiesta
    const id = parseInt(req.params.id);

    // Trova l'indice del libro nel catalogo
    const libroIndex = catalogo.findIndex(l => l.id === id);

    // Se il libro non esiste, restituisci un errore 404
    if (libroIndex === -1) {
        return res.status(404).json({ message: 'Libro non trovato' });
    }

    // Crea un nuovo oggetto libro aggiornato combinando i dati esistenti con quelli della richiesta
    const libroAggiornato = { ...catalogo[libroIndex], ...req.body };

    // Valida i dati del libro aggiornato
    if (!validaLibro(libroAggiornato)) {
        return res.status(400).json({ message: 'Dati del libro mancanti o non validi' });
    }

    let libroDaAggiornare = catalogo[libroIndex];
    console.log("Libro da aggiornare:", libroDaAggiornare);
    console.log("Dati aggiornati:", libroAggiornato);

    // Aggiorna il libro nel catalogo
    catalogo[libroIndex] = libroAggiornato;
    res.status(200).json({message: 'Libro aggiornato con successo', libro: libroAggiornato});
});

// endpoint per eliminare un libro esistente
app.delete(`${BASE_PATH}/libri/:id`, (req, res) => {
    // Estrai l'ID del libro da eliminare dalla richiesta
    const id = parseInt(req.params.id);

    // Trova l'indice del libro nel catalogo
    const libroIndex = catalogo.findIndex(l => l.id === id);

    // Se il libro non esiste, restituisci un errore 404
    if (libroIndex === -1) {
        return res.status(404).json({ message: 'Libro non trovato' });
    }

    // Rimuovi il libro dal catalogo
    catalogo.splice(libroIndex, 1);
    res.status(200).json({ message: 'Libro eliminato con successo' });
});

// endpoint per cercare libri in base a titolo, autore o genere
app.get(`${BASE_PATH}/libri/ricerca`, (req, res) => {

    const id = parseInt(req.params.id);
    
    // Trova l'indice del libro nel catalogo
    const libroIndex = catalogo.findIndex(l => l.id === id);

    // Se il libro non esiste, restituisci un errore 404
    if (libroIndex === -1) {
        return res.status(404).json({ message: 'Libro non trovato' });
    }

    const { titolo, autore, genere } = req.query;
    let risultati = catalogo;
    if (titolo) {
        risultati = risultati.filter(l => l.titolo.toLowerCase().includes(titolo.toLowerCase()));
    }
    if (autore) {
        risultati = risultati.filter(l => l.autore.toLowerCase().includes(autore.toLowerCase()));
    }
    if (genere) {
        risultati = risultati.filter(l => l.genere.toLowerCase().includes(genere.toLowerCase()));
    }
    res.status(200).json(libroTrovato);
});


// Utility function

function validaLibro(libro) {
    if (libro.titolo && libro.autore && libro.editore) {
        return true;
    } else {
        return false;
    }
}
/**
 * array=[{id:25, titolo:"titolo"}, {id:26, titolo:"titolo2"}, ...]
 *                  0                   1                      ...
 * 
 * 
 */


// endpoint per restituire un libro specifico in base all'id
app.get(`${BASE_PATH}/libri/:id`, (req, res) => {
    const id = parseInt(req.params.id);
    const libro = catalogo.find(l => l.id === id);
    if (libro) {
        res.json(libro);
    } else {
        res.status(404).json({ message: 'Libro non trovato' });
    }
});
// endpoint per restituire la lista dei clienti
app.get(`${BASE_PATH}/clienti`, (req, res) => {
    res.json(clienti);
});

// clienti 

app.get(`${BASE_PATH}/clienti/:id`, (req, res) => {
    
    // Estrai l'ID del cliente dalla richiesta
    const idCliente = parseInt(req.params.id);

    // Trova il cliente con l'ID specificato
    let clienteTrovato = clienti.find(c => c.id === idCliente);

    // Se il cliente esiste, restituiscilo; altrimenti, restituisci un errore 404
    if (clienteTrovato) {
        res.status(200).json(clienteTrovato);
    } else {
        res.status(404).json({ message: 'Cliente non trovato' });
    }
}); 


app.post(`${BASE_PATH}/clienti`, (req, res) => {
    const nuovoCliente = {
        id: clienti.length + 1,
        nome: req.body.nome,
        email: req.body.email
    };
    clienti.push(nuovoCliente);
    res.status(201).json(nuovoCliente);
});
// endpoint per restituire un cliente specifico in base all'id
app.get(`${BASE_PATH}/clienti/:id`, (req, res) => {
    const id = parseInt(req.params.id);
    const cliente = clienti.find(c => c.id === id);
    if (cliente) {
        res.json(cliente);
    } else {
        res.status(404).json({ message: 'Cliente non trovato' });
    }
}); 