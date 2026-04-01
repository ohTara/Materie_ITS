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
    const nuovoLibro = req.body;
    if(!nuovoLibro){
        return res.status(400).json({ message: 'Dati del libro mancanti' });
    }
    // Genera un nuovo ID incrementale per il libro
    const maxId = catalogo.map(item => item.id).reduce((max, id) => Math.max(max, id), 0);
    nuovoLibro.id = maxId + 1; // Assegna un nuovo ID incrementale

    catalogo.push(nuovoLibro); // Aggiungi il nuovo libro al catalogo
    res.status(201).json(nuovoLibro);
});
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

app.post(`${BASE_PATH}/clienti`, (req, res) => {
    const nuovoCliente = {
        id: clientiFile.length + 1,
        nome: req.body.nome,
        email: req.body.email
    };
    clientiFile.push(nuovoCliente);
    res.status(201).json(nuovoCliente);
});

app.get(`${BASE_PATH}/clienti/:id`, (req, res) => {
    const id = parseInt(req.params.id);
    const cliente = clientiFile.find(c => c.id === id);
    if (cliente) {
        res.json(cliente);
    } else {
        res.status(404).json({ message: 'Cliente non trovato' });
    }
}); 

function validaLibro(libro) {
    if (!libro.titolo || !libro.genere || !libro.autore || !libro.editore || !libro.numeroPagine) {
        return res.status(400).json({ message: 'Dati del libro mancanti' });
    }
}