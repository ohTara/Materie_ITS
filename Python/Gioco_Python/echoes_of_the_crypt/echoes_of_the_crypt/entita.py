"""Classi base del gioco: Entita (astratta) e Proiettile."""
from __future__ import annotations

from abc import ABC, abstractmethod

import pygame

import grafica


class Entita(ABC):
    """Oggetto di gioco con posizione, vita e velocita' (classe astratta)."""

    # Modalità debug hitbox (attivabile con F3/H)
    _debug_hitbox = False

    def __init__(self, x: float, y: float, dimensione: int, velocita: float,
                 vita: int, colore: tuple[int, int, int],
                 hitbox_moltiplicatore: float = 1.0, hitbox_offset_y: int = 0) -> None:
        """Inizializza l'entita'.

        Args:
            x (float): coordinata x del centro.
            y (float): coordinata y del centro.
            dimensione (int): lato del quadrato in pixel (sprite).
            velocita (float): pixel al secondo.
            vita (int): punti vita iniziali.
            colore (tuple[int, int, int]): colore RGB.
            hitbox_moltiplicatore (float): fattore per ridurre/ingrandire hitbox vs sprite (default 1.0).
                                           Es. 0.7 = hitbox 70% dello sprite.
            hitbox_offset_y (int): offset verticale hitbox in pixel (positivo = verso il basso).
                                   Utile per centrare hitbox sui piedi del personaggio.
        """
        self.pos = pygame.Vector2(x, y)
        self.dimensione = dimensione
        self.velocita = velocita
        self.vita = vita
        self.colore = colore
        self.sprite: str | None = None    # chiave di grafica.SPRITE (None = rettangolo)
        self.tinta: tuple[int, int, int] | None = None   # colore variabile dello sprite
        self.fluttua = False              # True se galleggia a mezz'aria
        # Hitbox personalizzabile (forgiving hitbox)
        self._hitbox_moltiplicatore = max(0.1, min(2.0, hitbox_moltiplicatore))
        self._hitbox_offset_y = hitbox_offset_y
        # Feedback visivo danno
        self._flash_danno = 0.0           # secondi rimanenti del flash bianco
        self._knockback = pygame.Vector2(0, 0)  # vettore knockback residuo

    @property
    def rect(self) -> pygame.Rect:
        """Rettangolo di collisione (hitbox) - può essere più piccolo dello sprite."""
        hit_w = int(self.dimensione * self._hitbox_moltiplicatore)
        hit_h = int(self.dimensione * self._hitbox_moltiplicatore)
        r = pygame.Rect(0, 0, hit_w, hit_h)
        # Centra orizzontalmente, sposta verticalmente per offset (es. piedi)
        r.centerx = round(self.pos.x)
        r.centery = round(self.pos.y) + self._hitbox_offset_y
        return r

    @property
    def rect_sprite(self) -> pygame.Rect:
        """Rettangolo dello sprite grafico (sempre dimensione piena, centrato)."""
        r = pygame.Rect(0, 0, self.dimensione, self.dimensione)
        r.center = (round(self.pos.x), round(self.pos.y))
        return r

    @classmethod
    def toggle_debug_hitbox(cls) -> bool:
        """Attiva/disattiva modalità debug hitbox. Returns nuovo stato."""
        cls._debug_hitbox = not cls._debug_hitbox
        return cls._debug_hitbox

    @classmethod
    def is_debug_hitbox(cls) -> bool:
        """True se modalità debug hitbox è attiva."""
        return cls._debug_hitbox

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
            # Usa hitbox per il clamp ai limiti (così l'hitbox non esce dall'area)
            hit_w = int(self.dimensione * self._hitbox_moltiplicatore)
            hit_h = int(self.dimensione * self._hitbox_moltiplicatore)
            metà_w = hit_w / 2
            metà_h = hit_h / 2
            # Clamp ai limiti della stanza - considera offset_y hitbox
            nuova_pos.x = max(limiti.left + metà_w, min(limiti.right - metà_w, nuova_pos.x))
            nuova_pos.y = max(limiti.top + metà_h - self._hitbox_offset_y,
                             min(limiti.bottom - metà_h - self._hitbox_offset_y, nuova_pos.y))
            # Controlla collisione con ostacoli (usa hitbox per collisioni)
            if ostacoli:
                rect_test = pygame.Rect(0, 0, hit_w, hit_h)
                rect_test.centerx = round(nuova_pos.x)
                rect_test.centery = round(nuova_pos.y) + self._hitbox_offset_y
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
            # Usa hitbox per il clamp ai limiti (così l'hitbox non esce dall'area)
            hit_w = int(self.dimensione * self._hitbox_moltiplicatore)
            hit_h = int(self.dimensione * self._hitbox_moltiplicatore)
            metà_w = hit_w / 2
            metà_h = hit_h / 2
            # Clamp ai limiti della stanza - considera offset_y hitbox
            nuova_pos.x = max(limiti.left + metà_w, min(limiti.right - metà_w, nuova_pos.x))
            nuova_pos.y = max(limiti.top + metà_h - self._hitbox_offset_y,
                             min(limiti.bottom - metà_h - self._hitbox_offset_y, nuova_pos.y))
            # Controlla collisione con ostacoli durante knockback (usa hitbox)
            if ostacoli:
                rect_test = pygame.Rect(0, 0, hit_w, hit_h)
                rect_test.centerx = round(nuova_pos.x)
                rect_test.centery = round(nuova_pos.y) + self._hitbox_offset_y
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
