"""Classi base del gioco: Entita (astratta) e Proiettile."""
from __future__ import annotations

from abc import ABC, abstractmethod

import pygame


class Entita(ABC):
    """Oggetto di gioco con posizione, vita e velocita' (classe astratta)."""

    def __init__(self, x: float, y: float, dimensione: int, velocita: float,
                 vita: int, colore: tuple[int, int, int]) -> None:
        """Inizializza l'entita'.

        Args:
            x (float): coordinata x del centro.
            y (float): coordinata y del centro.
            dimensione (int): lato del quadrato in pixel.
            velocita (float): pixel al secondo.
            vita (int): punti vita iniziali.
            colore (tuple[int, int, int]): colore RGB.
        """
        self.pos = pygame.Vector2(x, y)
        self.dimensione = dimensione
        self.velocita = velocita
        self.vita = vita
        self.colore = colore

    @property
    def rect(self) -> pygame.Rect:
        """Rettangolo di collisione centrato sulla posizione."""
        r = pygame.Rect(0, 0, self.dimensione, self.dimensione)
        r.center = (round(self.pos.x), round(self.pos.y))
        return r

    @property
    def vivo(self) -> bool:
        """True se i punti vita sono maggiori di zero."""
        return self.vita > 0

    def muovi(self, direzione: pygame.Vector2, dt: float,
              limiti: pygame.Rect) -> None:
        """Sposta l'entita' restando dentro i limiti.

        Args:
            direzione (pygame.Vector2): direzione (anche non normalizzata).
            dt (float): secondi trascorsi dall'ultimo frame.
            limiti (pygame.Rect): area in cui restare.
        """
        if direzione.length() > 0:
            self.pos += direzione.normalize() * self.velocita * dt
        metà = self.dimensione / 2
        self.pos.x = max(limiti.left + metà, min(limiti.right - metà, self.pos.x))
        self.pos.y = max(limiti.top + metà, min(limiti.bottom - metà, self.pos.y))

    def subisci_danno(self, danno: int) -> None:
        """Riduce la vita del valore indicato."""
        self.vita -= danno

    @abstractmethod
    def update(self, dt: float, stanza) -> None:
        """Aggiorna lo stato (ogni sottoclasse lo implementa a modo suo)."""

    def draw(self, schermo: pygame.Surface) -> None:
        """Disegna l'entita' come rettangolo colorato."""
        pygame.draw.rect(schermo, self.colore, self.rect)


class Proiettile(Entita):
    """Proiettile sparato dal giocatore o dai nemici."""

    def __init__(self, x: float, y: float, direzione: pygame.Vector2,
                 velocita: float, danno: int, gittata: float,
                 ostile: bool = False) -> None:
        """Crea un proiettile.

        Args:
            x (float): x di partenza.
            y (float): y di partenza.
            direzione (pygame.Vector2): direzione di volo.
            velocita (float): pixel al secondo.
            danno (int): danno inflitto.
            gittata (float): distanza massima in pixel.
            ostile (bool): True se colpisce il giocatore.
        """
        colore = (255, 90, 90) if ostile else (255, 240, 120)
        super().__init__(x, y, 10, velocita, 1, colore)
        self.direzione = pygame.Vector2(direzione).normalize()
        self.danno = danno
        self.rimanente = gittata
        self.ostile = ostile

    def update(self, dt: float, stanza) -> None:
        """Avanza; si distrugge a fine gittata o contro il muro."""
        passo = self.velocita * dt
        self.pos += self.direzione * passo
        self.rimanente -= passo
        if self.rimanente <= 0 or not stanza.AREA.contains(self.rect):
            self.vita = 0
