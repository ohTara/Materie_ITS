"""Il personaggio controllato dal giocatore: classi, abilita' e sblocchi."""
from __future__ import annotations

import pygame

import audio
from entita import Entita, Proiettile

# Abilita' attive (tasto Spazio): una per personaggio, con tempo di ricarica in secondi.
ABILITA: dict[str, dict] = {
    "scatto":     {"nome": "Scatto", "ricarica": 3.5,
                   "descrizione": "Balzo rapido che attraversa nemici e colpi"},
    "lame":       {"nome": "Ventaglio di lame", "ricarica": 5.0,
                   "descrizione": "Otto colpi in tutte le direzioni"},
    "scudo":      {"nome": "Scudo sacro", "ricarica": 8.0,
                   "descrizione": "Intoccabile per 1 s; spazza i colpi vicini"},
    "esplosione": {"nome": "Onda arcana", "ricarica": 7.0,
                   "descrizione": "Ferisce i nemici vicini e ne cancella i colpi"},
}

# Personaggi giocabili: stesse regole, statistiche di partenza diverse.
# "sblocco" e' la condizione per poterlo scegliere: ("sempre", 0), ("piano", n)
# = raggiungere il piano n, ("vittorie", n) = vincere n partite con qualunque personaggio.
# La "maestria" e' un bonus che si ottiene vincendo MAESTRIA_VITTORIE volte con lui.
PERSONAGGI: dict[str, dict] = {
    "viandante":  {"nome": "Viandante", "descrizione": "Equilibrato in tutto",
                   "tinta": (52, 66, 98), "vita": 6, "velocita": 260, "danno": 1,
                   "cadenza": 0.35, "gittata": 350.0, "vel_proiettile": 500.0,
                   "abilita": "scatto", "sblocco": ("sempre", 0),
                   "maestria": "Lo Scatto si ricarica in meta' tempo"},
    "predone":    {"nome": "Predone", "descrizione": "Veloce ma fragile",
                   "tinta": (58, 96, 62), "vita": 4, "velocita": 320, "danno": 1,
                   "cadenza": 0.28, "gittata": 300.0, "vel_proiettile": 520.0,
                   "abilita": "lame", "sblocco": ("piano", 2),
                   "maestria": "Ogni moneta raccolta vale doppio"},
    "templare":   {"nome": "Templare", "descrizione": "Lento, resistente, colpi pesanti",
                   "tinta": (120, 112, 96), "vita": 8, "velocita": 220, "danno": 2,
                   "cadenza": 0.50, "gittata": 320.0, "vel_proiettile": 460.0,
                   "abilita": "scudo", "sblocco": ("vittorie", 1),
                   "maestria": "Una volta per piano sopravvive a un colpo mortale"},
    "occultista": {"nome": "Occultista", "descrizione": "Colpisce da molto lontano",
                   "tinta": (98, 44, 60), "vita": 5, "velocita": 250, "danno": 1,
                   "cadenza": 0.32, "gittata": 500.0, "vel_proiettile": 620.0,
                   "abilita": "esplosione", "sblocco": ("vittorie", 3),
                   "maestria": "I colpi attraversano i nemici"},
}
PREDEFINITO = "viandante"
MAESTRIA_VITTORIE = 2          # vittorie con un personaggio per ottenerne la maestria
INVULNERABILE_DOPO_COLPO = 0.7 # secondi di tregua dopo aver subito un danno
VEL_SCATTO, DURATA_SCATTO = 950, 0.16
RAGGIO_SCUDO, RAGGIO_ESPLOSIONE = 130, 180
DURATA_SCUDO = 1.0
DANNO_ESPLOSIONE = 3           # fisso: non cresce con gli oggetti che aumentano il danno
# Frecce di sparo -> direzione. Se se ne tengono premute piu' d'una vale l'ultima premuta.
FRECCE = {pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1),
          pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0)}


def sbloccato(chiave: str, dati: dict) -> bool:
    """Dice se il personaggio si puo' scegliere, in base alle statistiche del profilo.

    Args:
        chiave (str): chiave di PERSONAGGI.
        dati (dict): statistiche del profilo ("vittorie", "piano_record", ...).

    Returns:
        bool: True se la condizione di sblocco e' soddisfatta.
    """
    tipo, soglia = PERSONAGGI[chiave]["sblocco"]
    if tipo == "piano":
        return dati.get("piano_record", 0) >= soglia
    if tipo == "vittorie":
        return dati.get("vittorie", 0) >= soglia
    return True


def testo_sblocco(chiave: str) -> str:
    """Frase che spiega come sbloccare il personaggio."""
    tipo, soglia = PERSONAGGI[chiave]["sblocco"]
    if tipo == "piano":
        return f"Raggiungi il piano {soglia}"
    if tipo == "vittorie":
        return "Vinci una partita" if soglia == 1 else f"Vinci {soglia} partite"
    return ""


def ha_maestria(chiave: str, vittorie_per_personaggio: dict[str, int]) -> bool:
    """True se con quel personaggio si e' vinto abbastanza da averne la maestria."""
    return vittorie_per_personaggio.get(chiave, 0) >= MAESTRIA_VITTORIE


def traguardi(dati: dict, vittorie_per_personaggio: dict[str, int]) -> set[str]:
    """Elenco (come frasi) di tutto cio' che il profilo ha sbloccato finora.

    Confrontando l'elenco prima e dopo una partita si ricavano le novita' da annunciare.
    """
    fatti = set()
    for chiave, p in PERSONAGGI.items():
        if p["sblocco"][0] != "sempre" and sbloccato(chiave, dati):
            fatti.add(f"Nuovo personaggio: {p['nome']}")
        if ha_maestria(chiave, vittorie_per_personaggio):
            fatti.add(f"Maestria del {p['nome']}: {p['maestria']}")
    return fatti


class Giocatore(Entita):
    """Personaggio con statistiche modificabili dagli oggetti e un'abilita' attiva."""

    def __init__(self, x: float, y: float, personaggio: str = PREDEFINITO) -> None:
        """Crea il giocatore al centro indicato.

        Args:
            x (float): coordinata x del centro.
            y (float): coordinata y del centro.
            personaggio (str): chiave di PERSONAGGI (statistiche di partenza).
        """
        p = PERSONAGGI[personaggio]
        super().__init__(x, y, 32, p["velocita"], p["vita"], p["tinta"])
        self.personaggio = personaggio
        self.vita_max = p["vita"]
        self.sprite = "giocatore"
        self.tinta = p["tinta"]
        self.danno = p["danno"]
        self.gittata = p["gittata"]
        self.cadenza = p["cadenza"]          # secondi tra due colpi
        self.vel_proiettile = p["vel_proiettile"]
        self.monete = 0
        self.uccisioni = 0
        self.oggetti: list[str] = []
        self.sinergie: list[str] = []     # nomi delle sinergie gia' attive
        self.sconfitti: set[str] = set()  # tipi di nemici battuti (per il Compendio)
        self.avvisi: list[str] = []       # messaggi da mostrare (li consuma main.py)
        self.maestria = False             # bonus del personaggio (vedi PERSONAGGI)
        self.fede_usata = False           # maestria del Templare: una volta per piano
        self.ricarica_abilita = 0.0       # secondi che mancano per riusare l'abilita'
        self.scudo = 0.0                  # secondi di Scudo sacro rimasti
        self._ricarica = 0.0
        self._invulnerabile = 0.0         # tregua dopo un colpo (il personaggio lampeggia)
        self._intoccabile = 0.0           # protezione di scatto e scudo
        self._scatto = 0.0
        self._direzione = pygame.Vector2(0, 1)   # ultima direzione di movimento
        self._frecce: list[int] = []      # frecce tenute premute, dalla prima all'ultima

    @property
    def abilita(self) -> dict:
        """Dati dell'abilita' attiva del personaggio (voce di ABILITA)."""
        return ABILITA[PERSONAGGI[self.personaggio]["abilita"]]

    def ha(self, personaggio: str) -> bool:
        """True se il giocatore usa quel personaggio e ne ha la maestria."""
        return self.maestria and self.personaggio == personaggio

    @property
    def tempo_ricarica(self) -> float:
        """Ricarica completa dell'abilita' (dimezzata dalla maestria del Viandante)."""
        return self.abilita["ricarica"] * (0.5 if self.ha("viandante") else 1)

    def update(self, dt: float, stanza) -> None:
        """Legge la tastiera: WASD muove, frecce sparano, Spazio usa l'abilita'."""
        k = pygame.key.get_pressed()
        mov = pygame.Vector2(k[pygame.K_d] - k[pygame.K_a],
                             k[pygame.K_s] - k[pygame.K_w])
        if mov.length() > 0:
            self._direzione = mov.normalize()
        for timer in ("_ricarica", "_invulnerabile", "_intoccabile", "ricarica_abilita", "scudo"):
            setattr(self, timer, max(0.0, getattr(self, timer) - dt))
        ostacoli = getattr(stanza, "ostacoli", [])
        if self._scatto > 0:                     # durante lo scatto non si cambia direzione
            self._scatto -= dt
            normale, self.velocita = self.velocita, VEL_SCATTO
            self.muovi(self._direzione, dt, stanza.AREA, ostacoli)
            self.velocita = normale
        else:
            self.muovi(mov, dt, stanza.AREA, ostacoli)
        # Applica knockback residuo e decay flash
        self.applica_knockback(dt, stanza.AREA, ostacoli)
        self._flash_danno = max(0.0, self._flash_danno - dt)
        if k[pygame.K_SPACE] and self.ricarica_abilita == 0:
            self.usa_abilita(stanza)
        # Ordine di pressione delle frecce: si tolgono le rilasciate, in coda le nuove.
        self._frecce = [t for t in self._frecce if k[t]] + \
            [t for t in FRECCE if k[t] and t not in self._frecce]
        if self._frecce and self._ricarica == 0:
            tiro = pygame.Vector2(FRECCE[self._frecce[-1]])   # niente diagonali
            stanza.proiettili.append(Proiettile(
                self.pos.x, self.pos.y, tiro, self.vel_proiettile,
                self.danno, self.gittata, perforante=self.ha("occultista")))
            self._ricarica = self.cadenza
            audio.suona("sparo")

    def usa_abilita(self, stanza) -> None:
        """Esegue l'abilita' del personaggio e ne fa partire la ricarica."""
        nome = PERSONAGGI[self.personaggio]["abilita"]
        self.ricarica_abilita = self.tempo_ricarica
        audio.suona("abilita")
        if nome == "scatto":
            self._scatto = DURATA_SCATTO
            self._intoccabile = max(self._intoccabile, DURATA_SCATTO + 0.12)
        elif nome == "lame":
            for i in range(8):
                stanza.proiettili.append(Proiettile(
                    self.pos.x, self.pos.y, pygame.Vector2(1, 0).rotate(45 * i),
                    self.vel_proiettile, self.danno, 260))
        elif nome == "scudo":
            self.scudo = DURATA_SCUDO
            self._intoccabile = max(self._intoccabile, DURATA_SCUDO)
            self._spazza_colpi(stanza, RAGGIO_SCUDO)
            stanza.effetti.append({"pos": tuple(self.pos), "raggio": RAGGIO_SCUDO,
                                   "t": 0.0, "durata": 0.35, "colore": (226, 186, 70)})
        elif nome == "esplosione":
            for n in stanza.nemici:
                if n.pos.distance_to(self.pos) <= RAGGIO_ESPLOSIONE + n.dimensione / 2:
                    n.subisci_danno(DANNO_ESPLOSIONE)
            self._spazza_colpi(stanza, RAGGIO_ESPLOSIONE)
            stanza.effetti.append({"pos": tuple(self.pos), "raggio": RAGGIO_ESPLOSIONE,
                                   "t": 0.0, "durata": 0.4, "colore": (170, 90, 220)})

    def _spazza_colpi(self, stanza, raggio: float) -> None:
        """Distrugge i proiettili nemici entro il raggio indicato."""
        for p in stanza.proiettili:
            if p.ostile and p.pos.distance_to(self.pos) <= raggio:
                p.vita = 0

    def subisci_danno(self, danno: int, knockback: pygame.Vector2 | None = None) -> None:
        """Applica il danno, se il giocatore non e' protetto.

        La maestria del Templare annulla, una volta per piano, il colpo mortale.

        Args:
            danno (int): danno da subire.
            knockback (pygame.Vector2 | None): vettore di spinta (opzionale).
        """
        if self._invulnerabile > 0 or self._intoccabile > 0:
            return
        super().subisci_danno(danno, knockback)
        self._invulnerabile = INVULNERABILE_DOPO_COLPO
        audio.suona("danno")
        if self.vita <= 0 and self.ha("templare") and not self.fede_usata:
            self.vita = 1
            self.fede_usata = True
            self._invulnerabile = 1.5
            self.avvisi.append("Fede incrollabile: sei ancora in piedi!")

    def draw(self, schermo: pygame.Surface) -> None:
        """Lampeggia mentre e' invulnerabile; con lo scudo attivo mostra un alone dorato."""
        if self.scudo > 0:
            pygame.draw.circle(schermo, (226, 186, 70), self.rect.center, 30, 3)
        if self._invulnerabile > 0 and int(self._invulnerabile * 10) % 2:
            return
        super().draw(schermo)

    CAMPI = ("vita", "vita_max", "danno", "gittata", "cadenza",
             "vel_proiettile", "velocita", "monete", "uccisioni", "oggetti", "sinergie",
             "personaggio", "maestria", "fede_usata")

    def a_dict(self) -> dict:
        """Esporta le statistiche in un dizionario (per il salvataggio)."""
        return {c: list(v) if isinstance(v := getattr(self, c), list) else v
                for c in self.CAMPI}

    def da_dict(self, dati: dict) -> None:
        """Ripristina le statistiche da un dizionario salvato."""
        for c in self.CAMPI:
            if c in dati:
                v = dati[c]
                setattr(self, c, list(v) if isinstance(v, list) else v)
        if self.personaggio not in PERSONAGGI:     # salvataggio di una versione diversa
            self.personaggio = PREDEFINITO
        self.tinta = PERSONAGGI[self.personaggio]["tinta"]
