"""Il personaggio controllato dal giocatore."""
from __future__ import annotations

import pygame

import audio
from entita import Entita, Proiettile

# Personaggi giocabili: stesse regole, statistiche di partenza diverse.
# Per aggiungerne uno basta una voce; "tinta" e' il colore del mantello.
PERSONAGGI: dict[str, dict] = {
    "viandante":  {"nome": "Viandante", "descrizione": "Equilibrato in tutto",
                   "tinta": (52, 66, 98), "vita": 6, "velocita": 260, "danno": 1,
                   "cadenza": 0.35, "gittata": 350.0, "vel_proiettile": 500.0},
    "predone":    {"nome": "Predone", "descrizione": "Veloce ma fragile",
                   "tinta": (58, 96, 62), "vita": 4, "velocita": 320, "danno": 1,
                   "cadenza": 0.28, "gittata": 300.0, "vel_proiettile": 520.0},
    "templare":   {"nome": "Templare", "descrizione": "Lento, resistente, colpi pesanti",
                   "tinta": (120, 112, 96), "vita": 8, "velocita": 220, "danno": 2,
                   "cadenza": 0.50, "gittata": 320.0, "vel_proiettile": 460.0},
    "occultista": {"nome": "Occultista", "descrizione": "Colpisce da molto lontano",
                   "tinta": (98, 44, 60), "vita": 5, "velocita": 250, "danno": 1,
                   "cadenza": 0.32, "gittata": 500.0, "vel_proiettile": 620.0},
}
PREDEFINITO = "viandante"


class Giocatore(Entita):
    """Personaggio con statistiche modificabili dagli oggetti."""

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
        self.avvisi: list[str] = []       # messaggi da mostrare (li consuma main.py)
        self._ricarica = 0.0
        self._invulnerabile = 0.0

    def update(self, dt: float, stanza) -> None:
        """Legge la tastiera: WASD muove, frecce sparano."""
        k = pygame.key.get_pressed()
        mov = pygame.Vector2(k[pygame.K_d] - k[pygame.K_a],
                             k[pygame.K_s] - k[pygame.K_w])
        self.muovi(mov, dt, stanza.AREA)
        self._ricarica = max(0.0, self._ricarica - dt)
        self._invulnerabile = max(0.0, self._invulnerabile - dt)
        tiro = pygame.Vector2(k[pygame.K_RIGHT] - k[pygame.K_LEFT],
                              k[pygame.K_DOWN] - k[pygame.K_UP])
        if tiro.length() > 0 and self._ricarica == 0:
            if tiro.x and tiro.y:        # niente diagonali: priorita' orizzontale
                tiro.y = 0
            stanza.proiettili.append(Proiettile(
                self.pos.x, self.pos.y, tiro, self.vel_proiettile,
                self.danno, self.gittata))
            self._ricarica = self.cadenza
            audio.suona("sparo")

    def subisci_danno(self, danno: int) -> None:
        """Applica il danno solo se non invulnerabile (1 s dopo un colpo)."""
        if self._invulnerabile > 0:
            return
        super().subisci_danno(danno)
        self._invulnerabile = 1.0
        audio.suona("danno")

    def draw(self, schermo: pygame.Surface) -> None:
        """Lampeggia mentre e' invulnerabile."""
        if self._invulnerabile > 0 and int(self._invulnerabile * 10) % 2:
            return
        super().draw(schermo)

    CAMPI = ("vita", "vita_max", "danno", "gittata", "cadenza",
             "vel_proiettile", "velocita", "monete", "uccisioni", "oggetti", "sinergie", "personaggio")

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
