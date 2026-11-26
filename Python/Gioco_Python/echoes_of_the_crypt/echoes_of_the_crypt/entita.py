"""Classi base del gioco: Entita (astratta) e Proiettile."""
from __future__ import annotations

from abc import ABC, abstractmethod

import pygame

import grafica


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
        self.sprite: str | None = None    # chiave di grafica.SPRITE (None = rettangolo)
        self.tinta: tuple[int, int, int] | None = None   # colore variabile dello sprite
        self.fluttua = False              # True se galleggia a mezz'aria
        # Feedback visivo danno
        self._flash_danno = 0.0           # secondi rimanenti del flash bianco
        self._knockback = pygame.Vector2(0, 0)  # vettore knockback residuo

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
              limiti: pygame.Rect, ostacoli: list[pygame.Rect] | None = None) -> None:
        """Sposta l'entita' restando dentro i limiti ed evitando ostacoli.

        Args:
            direzione (pygame.Vector2): direzione (anche non normalizzata).
            dt (float): secondi trascorsi dall'ultimo frame.
            limiti (pygame.Rect): area in cui restare.
            ostacoli (list[pygame.Rect] | None): lista di rettangoli solidi da evitare.
        """
        if direzione.length() > 0:
            nuova_pos = self.pos + direzione.normalize() * self.velocita * dt
            metà = self.dimensione / 2
            # Clamp ai limiti della stanza
            nuova_pos.x = max(limiti.left + metà, min(limiti.right - metà, nuova_pos.x))
            nuova_pos.y = max(limiti.top + metà, min(limiti.bottom - metà, nuova_pos.y))
            # Controlla collisione con ostacoli (supporta sia vecchi rect che nuovi dict con "rect")
            if ostacoli:
                rect_test = pygame.Rect(0, 0, self.dimensione, self.dimensione)
                rect_test.center = (round(nuova_pos.x), round(nuova_pos.y))
                for ostacolo in ostacoli:
                    obs_rect = ostacolo["rect"] if isinstance(ostacolo, dict) else ostacolo
                    if rect_test.colliderect(obs_rect):
                        # Collisione: non si muove
                        return
            self.pos = nuova_pos

    def subisci_danno(self, danno: int, knockback: pygame.Vector2 | None = None) -> None:
        """Riduce la vita del valore indicato e applica knockback/flash.

        Args:
            danno (int): danno da subire.
            knockback (pygame.Vector2 | None): vettore di spinta (opzionale).
        """
        self.vita -= danno
        self._flash_danno = 0.15  # flash bianco per 150ms
        if knockback is not None and knockback.length() > 0:
            self._knockback = knockback.normalize() * 200  # 200 px/s di spinta

    def applica_knockback(self, dt: float, limiti: pygame.Rect,
                          ostacoli: list | None = None) -> None:
        """Applica il knockback residuo e lo smorza."""
        if self._knockback.length() > 0:
            nuova_pos = self.pos + self._knockback * dt
            metà = self.dimensione / 2
            nuova_pos.x = max(limiti.left + metà, min(limiti.right - metà, nuova_pos.x))
            nuova_pos.y = max(limiti.top + metà, min(limiti.bottom - metà, nuova_pos.y))
            # Controlla collisione con ostacoli durante knockback
            if ostacoli:
                rect_test = pygame.Rect(0, 0, self.dimensione, self.dimensione)
                rect_test.center = (round(nuova_pos.x), round(nuova_pos.y))
                for ostacolo in ostacoli:
                    obs_rect = ostacolo["rect"] if isinstance(ostacolo, dict) else ostacolo
                    if rect_test.colliderect(obs_rect):
                        # Collisione: ferma il knockback
                        self._knockback = pygame.Vector2(0, 0)
                        return
            self.pos = nuova_pos
            # Smorza il knockback esponenzialmente
            self._knockback *= 0.1 ** dt  # si azzera in ~0.5s

    @abstractmethod
    def update(self, dt: float, stanza) -> None:
        """Aggiorna lo stato (ogni sottoclasse lo implementa a modo suo)."""

    def draw(self, schermo: pygame.Surface) -> None:
        """Disegna l'entita' con il suo sprite (vedi grafica.py)."""
        # Se sta flashando, disegna una versione bianca dello sprite
        if self._flash_danno > 0:
            # Salva tinta originale, imposta bianca, disegna, ripristina
            tinta_originale = self.tinta
            self.tinta = (255, 255, 255)
            grafica.disegna_entita(schermo, self)
            self.tinta = tinta_originale
        else:
            grafica.disegna_entita(schermo, self)


class Proiettile(Entita):
    """Proiettile sparato dal giocatore o dai nemici."""

    def __init__(self, x: float, y: float, direzione: pygame.Vector2,
                 velocita: float, danno: int, gittata: float,
                 ostile: bool = False, perforante: bool = False) -> None:
        """Crea un proiettile.

        Args:
            x (float): x di partenza.
            y (float): y di partenza.
            direzione (pygame.Vector2): direzione di volo.
            velocita (float): pixel al secondo.
            danno (int): danno inflitto.
            gittata (float): distanza massima in pixel.
            ostile (bool): True se colpisce il giocatore.
            perforante (bool): True se attraversa i nemici (li colpisce una volta ciascuno).
        """
        colore = (255, 90, 90) if ostile else (255, 240, 120)
        super().__init__(x, y, 10, velocita, 1, colore)
        self.direzione = pygame.Vector2(direzione).normalize()
        self.danno = danno
        self.rimanente = gittata
        self.ostile = ostile
        self.perforante = perforante
        self.colpiti: set[int] = set()    # nemici gia' colpiti da un colpo perforante

    def update(self, dt: float, stanza) -> None:
        """Avanza; si distrugge a fine gittata o contro il muro."""
        passo = self.velocita * dt
        self.pos += self.direzione * passo
        self.rimanente -= passo
        if self.rimanente <= 0 or not stanza.AREA.contains(self.rect):
            self.vita = 0

    def draw(self, schermo: pygame.Surface) -> None:
        """Disegna il proiettile come globo luminoso."""
        grafica.disegna_proiettile(schermo, self)
