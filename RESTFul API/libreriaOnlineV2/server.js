import express from 'express';
import bodyParser from 'body-parser';
import sqlite3 from 'sqlite3';
import { CREATE_LIBRI_TABLE } from './database/script_libri.js';

const app = express();
app.use(bodyParser.json());

export const db = new sqlite3.Database('./database/libreria.db', (err) => {
    if (err) {
        console.error('Errore durante la connessione al database:', err.message);
    } else {
        console.log('Connesso al database SQLite');
    }
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Il server è arrivo sulla porta ${PORT}`);
    initializeDatabase();
});

function initializeDatabase() {
    console.log('Inizializzazione del database...');
    db.exec(CREATE_LIBRI_TABLE
    , (err) => {
        if (err) {
            console.error('Errore durante la creazione della tabella:', err.message);
        } else {
            console.log('Tabella "libri" creata o già esistente');
        }
    });
}