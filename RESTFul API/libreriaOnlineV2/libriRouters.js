libriRouter.get('/:id', (req, res) => {
    console.log("GET /api/v2/libri - Recupero tutti i libri");
    db.get(SELECT_BY_ID, [req.params.id], function(err, rows) {
        if (err) {
            console.error('Errore durante il recupero dei libri:', err.message);
            res.status(500).json({ error: 'Errore durante il recupero dei libri' });
        } else {
            res.json(rows);
        }
    });
});

libriRouter.post('/libri', (req, res) => {
    const { titolo, autore, anno_pubblicazione } = req.body;
    const query = 'INSERT INTO libri (titolo, autore, anno_pubblicazione) VALUES (?, ?, ?)';
    db.run(query, [titolo, autore, anno_pubblicazione], function(err) {
        if (err) {
            console.error('Errore durante l\'inserimento del libro:', err.message);
            res.status(500).json({ error: 'Errore durante l\'inserimento del libro' });
        } else {
            res.json({ id: this.lastID, titolo, autore, anno_pubblicazione });
        }
    });
});

libriRouter.delete('/libri/:id', (req, res) => {
    const { id } = req.params;
    const query = 'DELETE FROM libri WHERE id = ?';
    db.run(query, [id], function(err) {
        if (err) {
            console.error('Errore durante la cancellazione del libro:', err.message);
            res.status(500).json({ error: 'Errore durante la cancellazione del libro' });
        }
        else if (this.changes === 0) {
            res.status(404).json({ error: 'Libro non trovato' });
        } else {
            res.json({ message: 'Libro cancellato con successo' });
        }
    });
});

libriRouter.put('/libri/:id', (req, res) => {
    const { id } = req.params;
    const { titolo, autore, anno_pubblicazione } = req.body;
    const query = 'UPDATE libri SET titolo = ?, autore = ?, anno_pubblicazione = ? WHERE id = ?';
    db.run(query, [titolo, autore, anno_pubblicazione, id], function(err) {
        if (err) {
            console.error('Errore durante l\'aggiornamento del libro:', err.message);
            res.status(500).json({ error: 'Errore durante l\'aggiornamento del libro' });
        }
        else if (this.changes === 0) {
            res.status(404).json({ error: 'Libro non trovato' });
        } else {
            res.json({ message: 'Libro aggiornato con successo' });
        }
    });
});

export default libriRouter;