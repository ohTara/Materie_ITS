# RESTful API con Node.js

**Cartella:** `RESTFul_API/` · commit 18/03, 01/04, 02/04 e 15/04/2026 (*get, put di clienti e libri*). Slide: *1 – Introduzione a REST*, *2 – JSON, request e response*.

## `libreriaOnline` (V1)
Express 5 + `body-parser` + `nodemon`; modelli in `model/catalogo.js` e `model/clientiFile.js` (dati su file). Specifica in `doc/Descrizione API.txt`:
| Metodo | Risorsa | Azione |
|---|---|---|
| GET | `/api/v1/libri` · `/:id` · `/search/?titolo=` | elenco, dettaglio, filtro |
| POST · PUT · DELETE | `/api/v1/libri[/:id]` | crea, modifica, elimina |
| GET/POST/PUT/DELETE | `/api/v1/clienti…` | stesse operazioni (filtro `?nome=`) |
| *(ToDo)* GET | `/api/v1/clienti/:id/ordini` | ordini di un cliente |

## `libreriaOnlineV2`
Aggiunge **SQLite** (`sqlite3`, `database/libreria.db`), router separato `libriRouters.js`, script `database/script_libri.js` che crea la tabella all'avvio; server su porta 3000.

## Concetti
URL = risorsa, metodo = azione; codici di stato; JSON; separazione server / router / dati.
**Nota:** `node_modules/` va escluso da Git (`package-lock.json` sì, resta).
