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

