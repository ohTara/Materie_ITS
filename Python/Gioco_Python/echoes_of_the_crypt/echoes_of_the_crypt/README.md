# Echoes of the Crypt

Videogioco 2D roguelike a visuale dall'alto, progetto d'esame di Programmazione Python (ITS ICT Piemonte, Cloud Specialist). Si attraversano tre piani di una cripta generata a caso, si sconfiggono nemici e boss e si raccolgono oggetti che potenziano il personaggio. Se si muore si ricomincia da capo.

Tutto è scritto in Python con `pygame-ce`: grafica e audio sono generati dal programma, senza immagini o file sonori esterni.

## Avvio

**Linux**

```bash
./run.sh
```

Lo script crea l'ambiente virtuale, installa le dipendenze e avvia il gioco.

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

Serve Python 3.12 o successivo.

## Comandi

| Tasto | Azione |
|---|---|
| W A S D | Movimento |
| Frecce | Sparo nelle quattro direzioni |
| Esc | Pausa; nei menu torna indietro |
| Invio | Conferma |
| M | Audio acceso / spento |

## Come si gioca

- Le porte di una stanza restano chiuse dalla grata finché ci sono nemici.
- Ogni piano ha una stanza del **tesoro** (un oggetto gratis), un **negozio** (due oggetti a 5 monete e un cuore a 3) e la stanza del **boss**. Sconfitto il boss si passa al piano successivo con un oggetto in premio.
- La partita si salva da sola a ogni stanza: **Continua** riprende dall'ultima.
- **Partita con seed**: lo stesso seed (mostrato in pausa e a fine partita) genera gli stessi piani, negozi e premi. Restano casuali monete e cuori lasciati dai nemici.
- **Profili**: ogni profilo ha statistiche, storico e salvataggio propri. La classifica raccoglie le vittorie più veloci di tutti i profili.

## Personaggi

| Personaggio | Vita | Velocità | Danno | Cadenza | Gittata |
|---|---|---|---|---|---|
| Viandante | 6 | 260 | 1 | 0,35 s | 350 |
| Predone | 4 | 320 | 1 | 0,28 s | 300 |
| Templare | 8 | 220 | 2 | 0,50 s | 320 |
| Occultista | 5 | 250 | 1 | 0,32 s | 500 |

## Nemici

| Nemico | Comportamento |
|---|---|
| Teschio | Insegue il giocatore |
| Spettro | Vaga cambiando direzione |
| Cultista | Tiene le distanze e spara |
| Boss | Insegue e spara raffiche a stella; uno per piano, sempre più forte |

## Oggetti e sinergie

Gli oggetti passivi sono 15 e modificano danno, velocità, gittata, cadenza e vita. Chi possiede entrambi gli oggetti di una coppia ottiene un bonus in più:

| Sinergia | Oggetti |
|---|---|
| Passo di fuoco | Stivali veloci + Scarpe di fiamma |
| Cecchino | Lente d'ingrandimento + Occhio di falco |
| Colosso | Armatura antica + Elmo di ferro |
| Artiglieria | Cannone pesante + Caffe' forte |
| Patto di sangue | Sangue antico + Amuleto di forza |
| Tempesta | Clessidra incrinata + Piuma di corvo |

## Struttura del codice

| Modulo | Contenuto |
|---|---|
| `main.py` | Ciclo di gioco e stati (menu, partita, pausa, tabelle) |
| `dungeon.py` | Generazione del piano (random walk) e logica delle stanze |
| `entita.py` | Classe astratta `Entita` e `Proiettile` |
| `giocatore.py` | Giocatore e dizionario `PERSONAGGI` |
| `nemici.py` | Nemici e boss (dizionario `DATI_NEMICI`) |
| `oggetti.py` | Oggetti, sinergie e prezzi (`OGGETTI`, `SINERGIE`, `PREZZI`) |
| `interfaccia.py` | Menu, caselle di testo, tabelle, HUD e minimappa |
| `grafica.py` | Sprite in pixel art, stanze, luci e buio |
| `audio.py` | Effetti e musica sintetizzati (`SUONI`, `MUSICA`) |
| `salvataggio.py`, `database.py` | Profili, statistiche, storico e checkpoint su SQLite |

I contenuti del gioco stanno in dizionari separati dalla logica: per aggiungere un nemico, un oggetto, una sinergia, un personaggio o un suono basta una voce in più.

## Test

```bash
python test_verifica.py
```

Sono 47 test su database, negozio, oggetti, audio, seed, grafica e personaggi; non serve una finestra.

## Eseguibile per Windows

```bat
crea_eseguibile.bat
```

Usa PyInstaller con `EchoesOfTheCrypt.spec` e produce `EchoesOfTheCrypt.zip`. Lo zip presente nella repo è precedente a negozio, sinergie, audio, grafica e personaggi: va rigenerato.
