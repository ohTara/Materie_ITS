"""Nemici: classe base e sottoclassi con IA diversa (polimorfismo)."""
from __future__ import annotations

import random

import pygame

import audio
from entita import Entita, Proiettile

# I dati sono separati dalla logica: per un nuovo nemico basta una voce.
DATI_NEMICI: dict[str, dict] = {
    "inseguitore": {"vita": 3, "velocita": 120, "dim": 30, "colore": (200, 60, 60),
                    "sprite": "teschio", "fluttua": True,
                    "nome": "Teschio", "descrizione": "Insegue il giocatore senza sosta."},
    "errante":     {"vita": 2, "velocita": 90,  "dim": 28, "colore": (190, 120, 40),
                    "sprite": "spettro", "fluttua": True, "macchia": (40, 84, 88),
                    "nome": "Spettro", "descrizione": "Vaga per la stanza cambiando direzione."},
    "tiratore":    {"vita": 2, "velocita": 80,  "dim": 28, "colore": (170, 60, 190),
                    "sprite": "cultista", "nome": "Cultista",
                    "descrizione": "Tiene le distanze e spara; dal piano 2 a ventaglio."},
    "caricatore":  {"vita": 4, "velocita": 75,  "dim": 30, "colore": (72, 112, 66),
                    "sprite": "ghoul", "macchia": (44, 70, 40), "nome": "Ghoul",
                    "descrizione": "Si ferma un attimo (punto esclamativo), poi carica in linea retta."},
    # Un boss per piano, sempre piu' forte: vita, velocita', proiettili per raffica.
    # Il colore del boss e' la tinta del suo sprite.
    "boss_1": {"vita": 50, "velocita": 70, "dim": 64, "colore": (140, 26, 32),
               "proiettili": 8, "intervallo": 2.0, "nome": "Guardiano del 1° piano",
               "descrizione": "Insegue e spara raffiche a stella; sotto meta' vita va in furia e chiama due teschi."},
    "boss_2": {"vita": 85, "velocita": 85, "dim": 70, "colore": (88, 44, 146),
               "proiettili": 12, "intervallo": 1.8, "nome": "Guardiano del 2° piano",
               "descrizione": "Insegue e spara raffiche a stella; sotto meta' vita va in furia e chiama due teschi."},
    "boss_3": {"vita": 125, "velocita": 100, "dim": 76, "colore": (44, 46, 60),
               "proiettili": 16, "intervallo": 1.5, "nome": "Guardiano del 3° piano",
               "descrizione": "Insegue e spara raffiche a stella; sotto meta' vita va in furia e chiama due teschi."},
}
TIPI_COMUNI: list[str] = ["inseguitore", "errante", "tiratore", "caricatore"]
# Difficolta': quanto crescono i nemici comuni a ogni piano oltre il primo.
SCALA_VITA, SCALA_VELOCITA = 0.4, 0.10
VEL_COLPI, VEL_COLPI_PIANO = 260, 30      # velocita' dei colpi nemici (px/s) e aumento per piano


def vel_colpi(piano: int) -> float:
    """Velocita' dei proiettili nemici al piano indicato."""
    return VEL_COLPI + VEL_COLPI_PIANO * (piano - 1)


class Nemico(Entita):
    """Classe base dei nemici (danno da contatto)."""

    def __init__(self, x: float, y: float, tipo: str, piano: int = 1) -> None:
        """Crea il nemico da DATI_NEMICI; i comuni diventano piu' forti e veloci a ogni piano."""
        d = DATI_NEMICI[tipo]
        comune = tipo in TIPI_COMUNI
        vita = d["vita"] * (1 + SCALA_VITA * (piano - 1) if comune else 1)
        velocita = d["velocita"] * (1 + SCALA_VELOCITA * (piano - 1) if comune else 1)
        super().__init__(x, y, d["dim"], velocita, round(vita), d["colore"])
        self.tipo = tipo
        self.piano = piano
        self.sprite = d.get("sprite", "boss")
        self.tinta = d["colore"] if self.sprite == "boss" else None
        self.fluttua = d.get("fluttua", False)
        self.macchia = d.get("macchia", (74, 14, 20))   # colore lasciato a terra

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
    """Mantiene le distanze e spara al giocatore (dal piano 2 a ventaglio)."""

    def __init__(self, x: float, y: float, tipo: str, piano: int = 1) -> None:
        """Crea il tiratore con il timer di sparo."""
        super().__init__(x, y, tipo, piano)
        self._ricarica = random.uniform(0.5, 1.5)

    def update(self, dt: float, stanza) -> None:
        """Si avvicina/allontana per stare a ~300 px e spara a intervalli regolari."""
        verso = stanza.giocatore.pos - self.pos
        if verso.length() < 250:
            self.muovi(-verso, dt, stanza.AREA)
        elif verso.length() > 350:
            self.muovi(verso, dt, stanza.AREA)
        self._ricarica -= dt
        if self._ricarica <= 0 and verso.length() > 0:
            angoli = (0,) if self.piano == 1 else (-18, 0, 18)
            for a in angoli:
                stanza.proiettili.append(Proiettile(
                    self.pos.x, self.pos.y, verso.rotate(a), vel_colpi(self.piano), 1, 700,
                    ostile=True))
            self._ricarica = max(0.9, 1.5 - 0.2 * (self.piano - 1))


class Caricatore(Nemico):
    """Si avvicina piano, si ferma un attimo (punto esclamativo) e poi carica in linea retta."""

    ATTESA, DURATA_CARICA, VEL_CARICA, PAUSA = 0.5, 0.45, 520, 1.4

    def __init__(self, x: float, y: float, tipo: str, piano: int = 1) -> None:
        """Crea il caricatore: parte nella fase di avvicinamento."""
        super().__init__(x, y, tipo, piano)
        self._fase = "avvicina"
        self._timer = random.uniform(0.6, 1.4)
        self._dir = pygame.Vector2(1, 0)
        self.avviso = False               # True mentre prepara la carica

    def update(self, dt: float, stanza) -> None:
        """Macchina a stati: avvicina -> prepara -> carica -> avvicina."""
        verso = stanza.giocatore.pos - self.pos
        self._timer -= dt
        if self._fase == "avvicina":
            self.muovi(verso, dt, stanza.AREA)
            if self._timer <= 0 and 0 < verso.length() < 380:
                self._fase, self._timer, self.avviso = "prepara", self.ATTESA, True
                self._dir = verso.normalize()         # la direzione si decide adesso
                audio.suona("carica")
        elif self._fase == "prepara":
            if self._timer <= 0:
                self._fase, self._timer, self.avviso = "carica", self.DURATA_CARICA, False
        else:
            normale, self.velocita = self.velocita, self.VEL_CARICA
            self.muovi(self._dir, dt, stanza.AREA)
            self.velocita = normale
            if self._timer <= 0:
                self._fase, self._timer = "avvicina", self.PAUSA


class Boss(Inseguitore):
    """Boss di fine piano: raffiche a stella; sotto meta' vita va in furia."""

    def __init__(self, x: float, y: float, tipo: str, piano: int = 1) -> None:
        """Crea il boss leggendo numero di proiettili e intervallo dai dati."""
        super().__init__(x, y, tipo, piano)
        d = DATI_NEMICI[tipo]
        self._n = d["proiettili"]
        self._intervallo = d["intervallo"]
        self._raffica = self._intervallo
        self._vita_iniziale = self.vita
        self._rotazione = 0.0
        self._mirati = self._intervallo / 2
        self.furia = False

    def update(self, dt: float, stanza) -> None:
        """Insegue e spara raffiche a stella, ruotate ogni volta.

        Sotto meta' vita entra in furia: piu' veloce, raffiche piu' fitte,
        colpi mirati tra una raffica e l'altra e due teschi in aiuto.
        """
        super().update(dt, stanza)
        if not self.furia and self.vita <= self._vita_iniziale / 2:
            self.furia = True
            self.velocita *= 1.25
            self._intervallo *= 0.65
            self.tinta = tuple(min(255, c + 50) for c in self.tinta)
            for dx in (-90, 90):
                stanza.rinforzi.append(crea_nemico("inseguitore", self.pos.x + dx, self.pos.y,
                                                   self.piano))
            stanza.effetti.append({"pos": tuple(self.pos), "raggio": 220, "t": 0.0,
                                   "durata": 0.5, "colore": (255, 70, 60)})
            audio.suona("furia")
        self._raffica -= dt
        if self._raffica <= 0:
            for i in range(self._n):
                stanza.proiettili.append(Proiettile(
                    self.pos.x, self.pos.y,
                    pygame.Vector2(1, 0).rotate(self._rotazione + 360 * i / self._n),
                    vel_colpi(self.piano) - 40, 1, 600, ostile=True))
            self._rotazione += 180 / self._n          # la prossima raffica copre i varchi
            self._raffica = self._intervallo
        if self.furia:
            self._mirati -= dt
            verso = stanza.giocatore.pos - self.pos
            if self._mirati <= 0 and verso.length() > 0:
                for a in (-12, 0, 12):
                    stanza.proiettili.append(Proiettile(
                        self.pos.x, self.pos.y, verso.rotate(a), vel_colpi(self.piano) + 40,
                        1, 700, ostile=True))
                self._mirati = self._intervallo


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
              "tiratore": Tiratore, "caricatore": Caricatore, "boss_1": Boss, "boss_2": Boss, "boss_3": Boss}
    return classi[tipo](x, y, tipo, piano)
