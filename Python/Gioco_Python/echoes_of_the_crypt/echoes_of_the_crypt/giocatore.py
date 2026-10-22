"""Il personaggio controllato dal giocatore."""
from __future__ import annotations

import pygame

from entita import Entita, Proiettile


class Giocatore(Entita):
    """Personaggio con statistiche modificabili dagli oggetti."""

    def __init__(self, x: float, y: float) -> None:
        """Crea il giocatore al centro indicato."""
        super().__init__(x, y, 32, 260, 6, (80, 160, 255))
        self.vita_max = 6
        self.danno = 1
        self.gittata = 350.0
        self.cadenza = 0.35          # secondi tra due colpi
        self.vel_proiettile = 500.0
        self.monete = 0
        self.uccisioni = 0
        self.oggetti: list[str] = []
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

    def subisci_danno(self, danno: int) -> None:
        """Applica il danno solo se non invulnerabile (1 s dopo un colpo)."""
        if self._invulnerabile > 0:
            return
        super().subisci_danno(danno)
        self._invulnerabile = 1.0

    def draw(self, schermo: pygame.Surface) -> None:
        """Lampeggia mentre e' invulnerabile."""
        if self._invulnerabile > 0 and int(self._invulnerabile * 10) % 2:
            return
        super().draw(schermo)

    CAMPI = ("vita", "vita_max", "danno", "gittata", "cadenza",
             "vel_proiettile", "velocita", "monete", "uccisioni", "oggetti")

    def a_dict(self) -> dict:
        """Esporta le statistiche in un dizionario (per il salvataggio)."""
        return {c: list(v) if isinstance(v := getattr(self, c), list) else v
                for c in self.CAMPI}

    def da_dict(self, dati: dict) -> None:
        """Ripristina le statistiche da un dizionario salvato."""
        for c in self.CAMPI:
            if c in dati:
                setattr(self, c, dati[c])
