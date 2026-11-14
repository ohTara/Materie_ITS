# Python — progetto "Echoes of the Crypt" (22–23/10/2026)

**Cartella:** `Python/Gioco_Python/echoes_of_the_crypt/` · **Commit:** 22/10 (*Python_alpha_0.0.2*) e 23/10 (*ultima versione eseguibile*)

## Obiettivo
Mettere insieme classi, ereditarietà, moduli e file in un gioco a dungeon con salvataggio, e distribuirlo come eseguibile.

## Concetti chiave
- Architettura a moduli: entità, giocatore, nemici, oggetti, dungeon, interfaccia, salvataggio.
- Libreria grafica: `pygame-ce` (da `requirements.txt`); gli import dei singoli moduli sono nella tabella.
- Distribuzione: PyInstaller (`EchoesOfTheCrypt.spec`, `crea_eseguibile.bat`).

## Moduli
| Modulo | Contenuto (da codice) |
|---|---|
| `dungeon.py` | classi: `Stanza`, `Dungeon` · import: __future__, collections, nemici, oggetti, pygame, random |
| `entita.py` | classi: `Entita(ABC)`, `Proiettile(Entita)` · import: __future__, abc, pygame |
| `giocatore.py` | classi: `Giocatore(Entita)` · import: __future__, entita, pygame |
| `interfaccia.py` | classi: `Menu`, `Hud` · funzioni: `testo()` · import: __future__, dungeon, pygame |
| `main.py` | classi: `Gioco` · funzioni: `main()` · import: __future__, dungeon, giocatore, interfaccia, oggetti, pygame, random, salvataggio |
| `nemici.py` | classi: `Nemico(Entita)`, `Inseguitore(Nemico)`, `Errante(Nemico)`, `Tiratore(Nemico)`, `Boss(Inseguitore)` · funzioni: `crea_nemico()` · import: __future__, entita, pygame, random |
| `oggetti.py` | classi: `Raccoglibile` · import: __future__, pygame |
| `salvataggio.py` | funzioni: `cartella_dati()`, `_leggi()`, `_scrivi()`, `carica()`, `registra_partita()`, `salva_partita()`, `carica_partita()`, `esiste_partita()` · import: __future__, json, os, pathlib, sys |

## Nota sulla repo
La cartella include artefatti di build (`build/`, `dist/`, `.exe`, DLL, `.pyc`). Vanno rigenerati, non versionati: vedi `docs/README.md` → *Manutenzione della repo*.


## Aggiornamento 14/11/2026 — negozio
Le monete ora si spendono: ogni piano ha una stanza `negozio` (oltre a inizio, tesoro e boss).
- `oggetti.py`: dizionario `PREZZI` (cuore 3, passivo 5); `Raccoglibile` ha l'attributo `prezzo` e i metodi `acquistabile()` e `raccogli()`.
- `dungeon.py`: `Dungeon._genera()` assegna il ruolo `negozio`; `Stanza._rifornisci()` espone due passivi non posseduti e un cuore. Si compra toccando l'oggetto; il cuore non viene venduto a vita piena.
- Salvataggio: il prezzo è il quinto valore di ogni raccoglibile nel checkpoint; i salvataggi precedenti restano leggibili.
- `interfaccia.py`: sulla minimappa tesoro e negozio hanno un colore proprio.
- `test_verifica.py`: 5 test nuovi (`TestNegozio`), 29 in totale.

## Aggiornamento 14/11/2026 — oggetti e sinergie
- `oggetti.py`: gli oggetti passivi sono 15 (nuovi: Clessidra incrinata, Pietra affilata, Piuma di corvo, Elmo di ferro). Nuovo dizionario `SINERGIE` (6 voci): chi possiede entrambi gli oggetti richiesti riceve un bonus, una volta sola. Funzioni `applica_effetti()` e `attiva_sinergie()`.
- `giocatore.py`: liste `sinergie` (salvata nel checkpoint) e `avvisi` (messaggi che `main.py` mostra a schermo: oggetto ottenuto, sinergia attivata).
- `interfaccia.py`: l'HUD elenca le sinergie attive sotto gli oggetti.
- `test_verifica.py`: 4 test nuovi (`TestOggetti`), 33 in totale.
