"""Generazione del piano (random walk) e logica delle stanze."""
from __future__ import annotations

import random
from collections import deque

import pygame

from nemici import Nemico, TIPI_COMUNI, crea_nemico
from oggetti import OGGETTI, Raccoglibile

DIREZIONI: dict[str, tuple[int, int]] = {
    "su": (0, -1), "giu": (0, 1), "sinistra": (-1, 0), "destra": (1, 0)}
OPPOSTA: dict[str, str] = {"su": "giu", "giu": "su",
                           "sinistra": "destra", "destra": "sinistra"}


class Stanza:
    """Una stanza del dungeon: nemici, proiettili, oggetti e porte."""

    AREA = pygame.Rect(240, 100, 800, 520)   # zona calpestabile

    def __init__(self, coord: tuple[int, int], ruolo: str = "normale", piano: int = 1) -> None:
        """Crea la stanza.

        Args:
            coord (tuple[int, int]): posizione nella griglia del piano.
            ruolo (str): "iniziale", "normale", "tesoro" o "boss".
            piano (int): piano del dungeon (aumenta la difficolta').
        """
        self.coord = coord
        self.ruolo = ruolo
        self.piano = piano
        self.vicini: list[str] = []       # direzioni con una porta
        self.nemici: list[Nemico] = []
        self.proiettili: list = []
        self.raccoglibili: list[Raccoglibile] = []
        self.visitata = False
        self.popolata = False
        self.giocatore = None

    @property
    def pulita(self) -> bool:
        """True se la stanza e' stata popolata e non ci sono nemici."""
        return self.popolata and not self.nemici

    def rect_porta(self, direzione: str) -> pygame.Rect:
        """Rettangolo della porta nella direzione data."""
        a = self.AREA
        if direzione == "su":
            return pygame.Rect(a.centerx - 30, a.top - 10, 60, 20)
        if direzione == "giu":
            return pygame.Rect(a.centerx - 30, a.bottom - 10, 60, 20)
        if direzione == "sinistra":
            return pygame.Rect(a.left - 10, a.centery - 30, 20, 60)
        return pygame.Rect(a.right - 10, a.centery - 30, 20, 60)

    def entra(self, giocatore, rng: random.Random) -> None:
        """Segna la stanza visitata e la popola la prima volta."""
        self.giocatore = giocatore
        self.visitata = True
        self.proiettili.clear()
        if self.popolata:
            return
        self.popolata = True
        c = self.AREA.center
        if self.ruolo == "boss":
            self.nemici.append(crea_nemico(f"boss_{min(self.piano, 3)}", c[0], c[1], self.piano))
        elif self.ruolo == "tesoro":
            nuovi = [k for k, v in OGGETTI.items() if v["nome"] not in giocatore.oggetti]
            self.raccoglibili.append(
                Raccoglibile("passivo", c, rng.choice(nuovi or list(OGGETTI))))
        elif self.ruolo == "normale":
            for _ in range(min(6, rng.randint(2, 4) + self.piano - 1)):
                while True:
                    p = pygame.Vector2(rng.randint(self.AREA.left + 60, self.AREA.right - 60),
                                       rng.randint(self.AREA.top + 60, self.AREA.bottom - 60))
                    if p.distance_to(giocatore.pos) > 200:
                        break
                self.nemici.append(crea_nemico(rng.choice(TIPI_COMUNI), p.x, p.y, self.piano))

    def update(self, dt: float) -> None:
        """Aggiorna giocatore, nemici, proiettili, collisioni e raccolta."""
        g = self.giocatore
        g.update(dt, self)
        for n in self.nemici:
            n.update(dt, self)
            if n.rect.colliderect(g.rect):
                g.subisci_danno(1)
        for p in self.proiettili:
            p.update(dt, self)
            if p.ostile:
                if p.rect.colliderect(g.rect):
                    g.subisci_danno(p.danno)
                    p.vita = 0
            else:
                for n in self.nemici:
                    if p.rect.colliderect(n.rect):
                        n.subisci_danno(p.danno)
                        p.vita = 0
                        break
        for n in [n for n in self.nemici if not n.vivo]:
            g.uccisioni += 1
            if random.random() < 0.3:
                self.raccoglibili.append(Raccoglibile("moneta", n.pos))
            elif random.random() < 0.2:
                self.raccoglibili.append(Raccoglibile("cuore", n.pos))
        self.nemici = [n for n in self.nemici if n.vivo]
        self.proiettili = [p for p in self.proiettili if p.vivo]
        for r in [r for r in self.raccoglibili if r.rect.colliderect(g.rect)]:
            r.applica(g)
            self.raccoglibili.remove(r)

    def draw(self, schermo: pygame.Surface) -> None:
        """Disegna pavimento, porte, oggetti, nemici, proiettili, giocatore."""
        pygame.draw.rect(schermo, (40, 36, 48), self.AREA)
        pygame.draw.rect(schermo, (110, 100, 130), self.AREA, 6)
        for d in self.vicini:
            colore = (70, 200, 90) if self.pulita or self.ruolo in ("iniziale", "tesoro") \
                else (200, 60, 60)
            pygame.draw.rect(schermo, colore, self.rect_porta(d))
        for e in (*self.raccoglibili, *self.nemici, *self.proiettili, self.giocatore):
            e.draw(schermo)

    def a_dict(self) -> dict:
        """Stato salvabile della stanza (i nemici vivi non si salvano: la stanza ricomincia)."""
        return {"visitata": self.visitata, "popolata": self.pulita,
                "raccoglibili": [[r.tipo, r.rect.centerx, r.rect.centery, r.id]
                                 for r in self.raccoglibili] if self.pulita else []}

    def da_dict(self, dati: dict) -> None:
        """Ripristina visitata, popolata e oggetti a terra da un salvataggio."""
        self.visitata = dati.get("visitata", False)
        self.popolata = dati.get("popolata", False)
        self.raccoglibili = [Raccoglibile(t, (x, y), i)
                             for t, x, y, i in dati.get("raccoglibili", [])]

    def porte_aperte(self) -> bool:
        """True se i nemici sono stati sconfitti (o non ce ne sono)."""
        return not self.nemici


class Dungeon:
    """Piano generato con random walk su griglia."""

    def __init__(self, num_stanze: int = 9, seed: int | None = None, piano: int = 1) -> None:
        """Genera il piano.

        Args:
            num_stanze (int): numero di stanze.
            seed (int | None): seme per rendere il piano riproducibile.
            piano (int): numero del piano (1, 2, 3...).
        """
        self.seed = seed if seed is not None else random.randrange(10**9)
        self.piano = piano
        self.rng = random.Random(self.seed)
        self.stanze: dict[tuple[int, int], Stanza] = {}
        self._genera(num_stanze)

    def _genera(self, n: int) -> None:
        """Random walk, poi collegamento delle celle adiacenti e ruoli."""
        corrente = (0, 0)
        celle = {corrente}
        while len(celle) < n:
            dx, dy = self.rng.choice(list(DIREZIONI.values()))
            corrente = (corrente[0] + dx, corrente[1] + dy)
            celle.add(corrente)
        self.stanze = {c: Stanza(c, "normale", self.piano) for c in celle}
        for (x, y), stanza in self.stanze.items():
            for nome, (dx, dy) in DIREZIONI.items():
                if (x + dx, y + dy) in self.stanze:
                    stanza.vicini.append(nome)
        dist = self.distanze((0, 0))
        assert len(dist) == len(self.stanze), "piano non connesso"
        self.stanze[(0, 0)].ruolo = "iniziale"
        boss = max(dist, key=dist.get)
        self.stanze[boss].ruolo = "boss"
        foglie = [c for c, s in self.stanze.items()
                  if len(s.vicini) == 1 and s.ruolo == "normale"]
        candidati = foglie or [c for c, s in self.stanze.items() if s.ruolo == "normale"]
        if candidati:
            self.stanze[self.rng.choice(candidati)].ruolo = "tesoro"

    def distanze(self, partenza: tuple[int, int]) -> dict[tuple[int, int], int]:
        """Visita in ampiezza (BFS): distanza di ogni stanza dalla partenza.

        Args:
            partenza (tuple[int, int]): coordinate di partenza.

        Returns:
            dict[tuple[int, int], int]: coordinate -> numero di porte da attraversare.
        """
        dist = {partenza: 0}
        coda = deque([partenza])
        while coda:
            x, y = coda.popleft()
            for d in self.stanze[(x, y)].vicini:
                dx, dy = DIREZIONI[d]
                v = (x + dx, y + dy)
                if v not in dist:
                    dist[v] = dist[(x, y)] + 1
                    coda.append(v)
        return dist
