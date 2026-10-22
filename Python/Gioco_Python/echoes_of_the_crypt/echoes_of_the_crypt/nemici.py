"""Nemici: classe base e sottoclassi con IA diversa (polimorfismo)."""
from __future__ import annotations

import random

import pygame

from entita import Entita, Proiettile

# I dati sono separati dalla logica: per un nuovo nemico basta una voce.
DATI_NEMICI: dict[str, dict] = {
    "inseguitore": {"vita": 3, "velocita": 120, "dim": 30, "colore": (200, 60, 60)},
    "errante":     {"vita": 2, "velocita": 90,  "dim": 28, "colore": (190, 120, 40)},
    "tiratore":    {"vita": 2, "velocita": 80,  "dim": 28, "colore": (170, 60, 190)},
    # Un boss per piano, sempre piu' forte: vita, velocita', proiettili per raffica.
    "boss_1": {"vita": 25, "velocita": 70, "dim": 64, "colore": (120, 20, 20),
               "proiettili": 8, "intervallo": 2.0},
    "boss_2": {"vita": 45, "velocita": 85, "dim": 70, "colore": (80, 30, 140),
               "proiettili": 12, "intervallo": 1.8},
    "boss_3": {"vita": 70, "velocita": 100, "dim": 76, "colore": (30, 30, 30),
               "proiettili": 16, "intervallo": 1.5},
}
TIPI_COMUNI: list[str] = ["inseguitore", "errante", "tiratore"]


class Nemico(Entita):
    """Classe base dei nemici (danno da contatto)."""

    def __init__(self, x: float, y: float, tipo: str, piano: int = 1) -> None:
        """Crea il nemico da DATI_NEMICI; i comuni hanno +30% di vita per piano."""
        d = DATI_NEMICI[tipo]
        scala = 1 + 0.3 * (piano - 1) if tipo in TIPI_COMUNI else 1
        super().__init__(x, y, d["dim"], d["velocita"], round(d["vita"] * scala), d["colore"])
        self.tipo = tipo

    def update(self, dt: float, stanza) -> None:
        """Comportamento di default: fermo."""


class Inseguitore(Nemico):
    """Si muove direttamente verso il giocatore."""

    def update(self, dt: float, stanza) -> None:
        """Insegue il giocatore."""
        self.muovi(stanza.giocatore.pos - self.pos, dt, stanza.AREA)


class Errante(Nemico):
    """Cambia direzione a caso ogni tanto."""

    def __init__(self, x: float, y: float, tipo: str, piano: int = 1) -> None:
        """Crea l'errante con direzione e timer iniziali."""
        super().__init__(x, y, tipo, piano)
        self._dir = pygame.Vector2(1, 0)
        self._timer = 0.0

    def update(self, dt: float, stanza) -> None:
        """Cammina in una direzione casuale, cambiandola ogni 1-2 s."""
        self._timer -= dt
        if self._timer <= 0:
            self._dir = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            self._timer = random.uniform(1.0, 2.0)
        self.muovi(self._dir, dt, stanza.AREA)


class Tiratore(Nemico):
    """Mantiene le distanze e spara al giocatore."""

    def __init__(self, x: float, y: float, tipo: str, piano: int = 1) -> None:
        """Crea il tiratore con il timer di sparo."""
        super().__init__(x, y, tipo, piano)
        self._ricarica = random.uniform(0.5, 1.5)

    def update(self, dt: float, stanza) -> None:
        """Si avvicina/allontana per stare a ~300 px e spara ogni 1.5 s."""
        verso = stanza.giocatore.pos - self.pos
        if verso.length() < 250:
            self.muovi(-verso, dt, stanza.AREA)
        elif verso.length() > 350:
            self.muovi(verso, dt, stanza.AREA)
        self._ricarica -= dt
        if self._ricarica <= 0 and verso.length() > 0:
            stanza.proiettili.append(Proiettile(
                self.pos.x, self.pos.y, verso, 260, 1, 700, ostile=True))
            self._ricarica = 1.5


class Boss(Inseguitore):
    """Boss di fine piano: insegue e spara raffiche a stella (dati per piano)."""

    def __init__(self, x: float, y: float, tipo: str, piano: int = 1) -> None:
        """Crea il boss leggendo numero di proiettili e intervallo dai dati."""
        super().__init__(x, y, tipo, piano)
        d = DATI_NEMICI[tipo]
        self._n = d["proiettili"]
        self._intervallo = d["intervallo"]
        self._raffica = self._intervallo

    def update(self, dt: float, stanza) -> None:
        """Insegue (super) e a intervalli regolari spara una raffica a stella."""
        super().update(dt, stanza)
        self._raffica -= dt
        if self._raffica <= 0:
            for i in range(self._n):
                stanza.proiettili.append(Proiettile(
                    self.pos.x, self.pos.y, pygame.Vector2(1, 0).rotate(360 * i / self._n),
                    220, 1, 600, ostile=True))
            self._raffica = self._intervallo


def crea_nemico(tipo: str, x: float, y: float, piano: int = 1) -> Nemico:
    """Factory: istanzia la classe giusta in base al tipo.

    Args:
        tipo (str): chiave di DATI_NEMICI.
        x (float): coordinata x.
        y (float): coordinata y.
        piano (int): piano corrente (scala la vita dei nemici comuni).

    Returns:
        Nemico: l'istanza creata.
    """
    classi = {"inseguitore": Inseguitore, "errante": Errante,
              "tiratore": Tiratore, "boss_1": Boss, "boss_2": Boss, "boss_3": Boss}
    return classi[tipo](x, y, tipo, piano)
