# Echoes of the Crypt — Preparazione alle domande sul codice

**Progetto:** dungeon crawler in Python con `pygame-ce`
**Versione:** v1.5 (delivery)
**Cartella:** `echoes_of_the_crypt/`
**Linguaggio:** Python 3
**Eseguibile:** PyInstaller (da verificare)

> **Nota:** questo file è pensato per ripassare le domande che l'insegnante potrebbe farti sul codice. Tutti i dettagli sono ricavati dai file sorgenti del progetto. Dove un dato non si ricava dai file, è segnato come *da verificare*.

---

## 1. Cos'è il progetto (intuizione)

Echoes of the Crypt è un dungeon crawler 2D a turni/tempo reale con visuale dall'alto. Il giocatore esplora 3 piani di dungeon generati proceduralmente, combatte nemici, raccoglie oggetti, attiva sinergie, compra nel negozio e affronta un boss per piano. Alla fine dell'ultimo piano c'è la vittoria.

**Punti chiave da ricordare:**
- Generazione procedurale delle stanze basata su *random walk* + BFS per verificare che ogni stanza sia raggiungibile.
- Salvataggio persistente su **SQLite** (schema v4), con migrazione automatica dai vecchi file JSON.
- 4 personaggi giocabili con abilità e maestrie uniche.
- 15 oggetti passivi con 6 sinergie attivabili.
- Audio e grafica generati interamente da codice (nessun asset esterno).
- Macchina a stati per il gioco (`Gioco.stato`: menu, gioco, pausa, fine, …).

---

## 2. Struttura dei file (sorgenti principali)

| File | Responsabilità |
|------|----------------|
| `main.py` | Classe `Gioco`, stato macchina, loop principale a 60 FPS, cambio piano, botola, vittoria/sconfitta |
| `entita.py` | Classe base `Entita` (hitbox, movimento, collizioni) e `Proiettile` |
| `giocatore.py` | `Giocatore`, 4 personaggi (`PERSONAGGI`), abilità (`ABILITA`), sblocchi e maestrie |
| `nemici.py` | `Nemico` e sottoclassi, boss, `crea_nemico()`, scalatura per piano |
| `dungeon.py` | `Stanza` e `Dungeon`, generazione procedurale, porte, negozio, botola |
| `oggetti.py` | `OGGETTI` (15 oggetti), `SINERGIE` (6), `Raccoglibile`, negozio e prezzi |
| `salvataggio.py` | API di salvataggio/caricamento, multi-profilo, storico, leaderboard |
| `database.py` | Classe `Database`, schema SQLite v4, WAL, trigger, migrazioni |
| `grafica.py` | Sprite generati da codice, tavolozza colori, disegno stanze e menu |
| `interfaccia.py` | Menu, caselle di testo, scelta personaggio, Compendio |
| `audio.py` | Sintesi sonora e musica senza file esterni |
| `test_verifica.py` | 62 test automatici (unittest) che coprono tutto il progetto |

> I file `*.py` si trovano in `echoes_of_the_crypt/` insieme a `PREPARAZIONE_ESAME.md`. Il `.venv` è l'ambiente virtuale di sviluppo (non va versionato).

---

## 3. Architettura: macchina a stati (main.py)

La classe `Gioco` gestisce il flusso tramite uno stato (`self.stato`) che può essere:

- `menu` — schermata iniziale (nuova partita, continua, compendio, esci)
- `scelta_personaggio` — scelta tra i 4 personaggi
- `gioco` — partita in corso dentro una stanza
- `pausa` — menu di pausa
- `fine` — partita conclusa (vittoria o sconfitta)
- `compendio` — scheda delle scoperte fatte

**Loop principale (`run()`):**
1. Gestisce gli eventi pygame (tastiera, uscita).
2. Chiama `aggiorna(dt)` che aggiorna la stanza attiva (nemici, proiettili, giocatore).
3. Disegna tutto con `disegna()`.
4. Gira a **60 FPS** (`clock.tick(60)`).

**Transizioni importanti:**
- `nuova_partita(seed)` — crea un nuovo `Giocatore`, un nuovo `Dungeon`, imposta piano 1.
- `continua_partita()` — carica il checkpoint dal database (piano, seed, stanza, oggetti).
- `avvia_piano(piano)` — passa al piano successivo (genera un nuovo dungeon).
- `boss_sconfitto()` — apre la botola nella stanza del boss.
- `piano_completato()` — scende nella botola e passa al piano successivo.
- `fine_partita(vittoria)` — registra run nello storico, salva statistiche, cancella il checkpoint.

> **Domanda probabile:** *"Come gestisci il passaggio da un piano all'altro?"*  
> **Risposta:** quando il boss dell'ultimo piano muore → `fine_partita(vittoria=True)`; altrimenti si apre la botola, il giocatore ci sale sopra e `piano_completato()` genera il dungeon del piano successivo con un nuovo seed derivato dal seed di partita.

---

## 4. Generazione del dungeon (dungeon.py)

### Classe `Stanza`
Ogni stanza ha:
- Coordinate `(x, y)` nella griglia del dungeon.
- Un `ruolo`: `iniziale`, `normale`, `tesoro`, `negozio`, `boss`.
- Liste di nemici, proiettili, raccoglibili, effetti visivi, rinforzi.
- Porte sui 4 lati (`su`, `giu`, `sinistra`, `destra`).
- Stati `visitata` e `popolata` (per sapere se va rigenerata al rientro).

### Classe `Dungeon`
- Genera le stanze con **random walk** (camminata casuale) partendo dalla stanza iniziale.
- Usa **BFS** (`distanze()`) per verificare che tutte le stanze generate siano raggiungibili da quella iniziale (nessuna stanza isolata).
- Assegna i ruoli: una stanza iniziale, un tesoro, un negozio e un boss per piano; le restanti sono normali.
- `num_stanze` varia per piano: 9 (piano 1), 11 (piano 2), 13 (piano 3) — *da verificare se hardcoded o calcolato*.
- Ogni piano ha esattamente **un negozio**, con due oggetti passivi diversi e un cuore in vendita.

> **Domanda probabile:** *"Come fai a garantire che il dungeon sia connesso?"*  
> **Risposta:** il random walk crea le stanze, poi la BFS da `distanze()` calcola le distanze dalla stanza iniziale; se una stanza risulta non raggiungibile, viene scartata o rigenerata.

---

## 5. Entità e combattimento (entita.py, giocatore.py, nemici.py)

### `Entita` (base)
- Posizione `pygame.Vector2`, hitbox `rect` per le collizioni.
- Metodi `update()`, `disegna()`, `subisci_danno()`.
- `Proiettile(Entita)` — si muove in linea retta, può essere perforante (attraversa più nemici) o no.

### `Giocatore`
- Estende `Entita`.
- Statistiche: `vita`, `vita_max`, `danno`, `velocita`, `cadenza`, `gittata`, `vel_proiettile`, `monete`, `uccisioni`, `oggetti` (lista), `sinergie` (lista attive).
- `usa_abilita(stanza)` — attiva l'abilità del personaggio scelto (vedi sezione 7).
- `a_dict()` / `da_dict()` — serializzazione per il salvataggio su SQLite.

### Nemici
`DATI_NEMICI` definisce le statistiche base di ogni tipo: `inseguitore`, `errante`, `tiratore`, `caricatore`, `boss_1`, `boss_2`, `boss_3`.
- `crea_nemico(tipo, x, y, piano)` — factory che scala vita e velocità in base al piano.
- `Boss(Inseguitore)` — quando scende sotto metà vita entra in **furia**: velocità aumentata, spawn di rinforzi, teschi in aiuto (una volta sola).

> **Domanda probabile:** *"Come scalano i nemici nei piani successivi?"*  
> **Risposta:** `crea_nemico()` riceve il numero di piano e moltiplica vita e velocità (test: `crea_nemico(tipo, 0, 0, 3)` ha vita e velocità maggiori di `crea_nemico(tipo, 0, 0, 1)`).

---

## 6. Oggetti e sinergie (oggetti.py)

### `OGGETTI`
15 oggetti passivi, ognuno con:
- `nome`, `descrizione`, `effetti` (dizionario stat → valore), `tipo` = `"passivo"`.

Esempi di effetti: `vita_max`, `danno`, `velocita`, `cadenza`, `gittata`, `vel_proiettile`.

### `SINERGIE`
6 sinergie, ognuna richiede 2 o più oggetti specifici. Esempio: `"Cecchino"` richiede `falco` + `lente`.

**Come si attivano:**
1. Il giocatore raccoglie un oggetto → `applica_effetti()` aggiorna le statistiche.
2. `attiva_sinergie()` controlla se il set di oggetti raccolti soddisfa i requisiti di qualche sinergia non ancora attiva.
3. Se sì, la sinergia viene aggiunta a `g.sinergie` e i suoi effetti si applicano.
4. Una sinergia si attiva **una sola volta** (anche se si raccolgono altri oggetti dopo).

### Negozio
- Ogni piano ha un negozio con 2 passivi diversi + 1 cuore.
- I prezzi sono in `PREZZI` (dizionario tipo → prezzo).
- Il cuore si compra solo se il giocatore non ha vita piena; si paga con le monete.
- Senza monete sufficienti l'acquisto fallisce.

> **Domanda probabile:** *"Cosa succede se raccolgo tutti gli oggetti?"*  
> **Risposta:** si attivano tutte le 6 sinergie e le statistiche restano nei limiti definiti (es. `cadenza >= 0.1`, `vita_max <= 12`, `gittata >= 150`).

---

## 7. Personaggi, abilità e maestrie (giocatore.py)

### `PERSONAGGI` (4 personaggi)
| Chiave | Nome | Abilità | Sblocco |
|--------|------|---------|---------|
| `viandante` | Viandante | Scatto | Già disponibile |
| `predone` | Predone | Colpi multipli (8 direzioni) | Piano 2 |
| `templare` | Templare | Scudo che annulla un colpo mortale | 1 vittoria |
| `occultista` | Occultista | Onda arcana (danno fisso a tutti i nemici vicini) | 3 vittorie, piano 3 |

> I valori esatti di vita, danno, velocità di ogni personaggio sono in `PERSONAGGI` nel file `giocatore.py` — leggi il file per i numeri esatti.

### Abilità (`ABILITA`)
Ogni personaggio ha un'abilità con un tempo di **ricarica**:
- `viandante`: scatto (spostamento rapido, invulnerabile durante lo scatto).
- `predone`: spara 8 proiettili in tutte le direzioni.
- `templare`: scudo temporaneo che assorbe un colpo mortale una volta per piano.
- `occultista`: onda arcana che infligge danno fisso a tutti i nemici in stanza.

Con la **maestria** del personaggio, la ricarica dell'abilità è dimezzata (es. Viandante).

### Maestrie e sblocchi
- `sbloccato(chiave, dati)` — restituisce True se il personaggio è sbloccato in base a vittorie e piano record.
- `ha_maestria(nome, vittorie_per_personaggio)` — True se il personaggio ha abbastanza vittorie.
- Maestrie specifiche: Predone = monete doppie; Templare = colpo mortale annullato; Occultista = colpi perforanti.

> **Domanda probabile:** *"Come si sbloccano i personaggi?"*  
> **Risposta:** all'inizio c'è solo il Viandante. Il Predone si sblocca al piano 2, il Templare con 1 vittoria, l'Occultista con 3 vittorie e piano 3.

---

## 8. Salvataggio e database (salvataggio.py, database.py)

### Schema SQLite v4
Tabelle: `schema_version`, `profiles`, `game_stats`, `save_games`, `run_history`.  
Indici e trigger per `updated_at` e cascata di eliminazione.

### Flusso di salvataggio
1. **Nuova partita:** `sv.carica()` legge le statistiche del profilo corrente.
2. **Durante la partita:** `sv.salva_partita(stato)` scrive il checkpoint (piano, seed, tempo, stato giocatore, stanza, stanze visitate).
3. **Uscita / vittoria:** `sv.registra_partita()` salva la run nello storico e aggiorna le statistiche; il checkpoint viene cancellato dopo una vittoria.
4. **Ricarica:** `sv.carica_partita()` ripristina l'ultimo checkpoint.

### Multi-profilo
- `crea_profilo(nome)`, `get_profili()`, `seleziona_profilo(id)`, `get_profilo_corrente()`.
- Ogni profilo ha statistiche, checkpoint e storico separati.
- Eliminare un profilo cancella in cascata stats, save e history.

### Migrazione JSON
Se esistono i vecchi file `salvataggio.json` e `partita.json`, all'avvio vengono importati in SQLite e rinominati in `.bak`.

### `test_verifica.py`
Contiene **62 test** organizzati in classi:
- `TestDatabase` — schema, profili, statistiche, checkpoint, transazioni atomiche, migrazione JSON.
- `TestNegozio` — generazione negozio, acquisti, prezzi.
- `TestOggetti` — sinergie, salvataggio sinergie.
- `TestAudio` — sintesi suoni, gestione senza audio.
- `TestSeedEInput` — determinismo del seed, caselle di testo.
- `TestGrafica` — sprite, disegno stanze.
- `TestPersonaggi` — statistiche, sblocchi, maestrie.
- `TestSfida` — abilità, nemici difficili, bilanciamento.
- `TestFeedbackAmici` — porte, sparo, volume.
- `TestBotolaBilanciamentoCompendio` — botola, vittoria, compendio.

> **Domanda probabile:** *"Perché usi SQLite invece di JSON?"*  
> **Risposta:** SQLite permette transazioni atomiche, query sullo storico e leaderboard, multi-profilo isolato e migrazione strutturata tramite `schema_version`.

---

## 9. Audio e grafica (audio.py, grafica.py)

### Audio
- Tutti i suoni sono **sintetizzati in codice** (nessun file `.wav` o `.mp3` esterno).
- `SUONI` definisce ~20 effetti (sparo, colpo, morte, moneta, cuore, oggetto, acquisto, sinergia, abilità, furia, carica, porte, menu, piano, vittoria, sconfitta).
- `MUSICA` definisce la traccia di sottofondo come sequenza di note `(Hz, secondi)`.
- Se il mixer audio non è disponibile, `inizializza()` restituisce `False` e il gioco prosegue in silenzio.
- Volumi di partenza bassi: musica 0.15, effetti 0.5 (*da verificare se sono i valori finali*).

### Grafica
- Sprite generati da codice come griglie di caratteri (tavolozza `TAVOLOZZA`).
- Ogni nemico e oggetto ha il suo sprite e colore.
- `disegna_stanza()` disegna pavimento, muri, porte, nemici, proiettili, raccoglibili e macchie.

---

## 10. Domande probabili e risposte (riassunto rapido)

| Domanda | Risposta chiave |
|---------|----------------|
| Come è strutturato il gioco? | Macchina a stati in `main.py`, loop a 60 FPS, classe `Gioco`. |
| Come generi i dungeon? | Random walk + BFS per la connettività, ruoli assegnati per piano. |
| Come salvi le partite? | SQLite schema v4, checkpoint + storico, multi-profilo, migrazione JSON. |
| Come funzionano le sinergie? | 6 sinergie che richiedono combinazioni di oggetti, si attivano una volta. |
| Quanti personaggi ci sono? | 4 (Viandante, Predone, Templare, Occultista), ciascuno con abilità e maestria. |
| Come si sbloccano i personaggi? | Piano 2, 1 vittoria, 3 vittorie + piano 3. |
| I nemici scalano per piano? | Sì, `crea_nemico(tipo, x, y, piano)` scala vita e velocità. |
| Cosa succede alla fine dell'ultimo piano? | Vittoria, partita registrata nello storico, checkpoint cancellato. |
| Ci sono test? | Sì, 62 test in `test_verifica.py` coprono database, negozio, oggetti, audio, grafica, personaggi, combattimento. |
| Audio e grafica usano file esterni? | No, tutto generato da codice (`audio.py`, `grafica.py`). |

---

## 11. Da verificare

I seguenti dati non sono stati ricavati con certezza dai file letti e andrebbero controllati direttamente nel codice o chiesti all'insegnante:

- Valori esatti di `vita`, `danno`, `velocita` per ciascun personaggio in `PERSONAGGI` (`giocatore.py`).
- Numero esatto di stanze per piano (`num_stanze` in `dungeon.py`).
- Prezzi esatti in `PREZZI` (`oggetti.py`).
- Modalità di build con PyInstaller (comando, file `.spec`, cartella `dist`).
- Se il `.venv` è incluso nella consegna o va escluso.

---

**Come usare questo file:** leggilo sezione per sezione, apri il file sorgente corrispondente per verificare i dettagli numerici, e prova a rispondere a voce alta alle domande della tabella. Se trovi discrepanze tra questo file e il codice, segnala la sezione da correggere.

*File generato per la preparazione all'esame/interrogazione su Echoes of the Crypt (v1.5).*