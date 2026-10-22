"""Oggetti raccoglibili: passivi (anche con effetti multipli), cuori e monete."""
from __future__ import annotations

import pygame

# Ogni oggetto puo' modificare piu' statistiche insieme (bonus e malus).
OGGETTI: dict[str, dict] = {
    "stivali":   {"nome": "Stivali veloci",    "effetti": {"velocita": 40}},
    "lente":     {"nome": "Lente d'ingrandimento", "effetti": {"gittata": 120}},
    "amuleto":   {"nome": "Amuleto di forza",  "effetti": {"danno": 1}},
    "caffe":     {"nome": "Caffe' forte",      "effetti": {"cadenza": -0.08}},
    "cuore_ex":  {"nome": "Cuore extra",       "effetti": {"vita_max": 2, "vita": 2}},
    "sangue":    {"nome": "Sangue antico",     "effetti": {"danno": 1, "vita_max": 1, "vita": 1}},
    "fiamme":    {"nome": "Scarpe di fiamma",  "effetti": {"velocita": 30, "cadenza": -0.05}},
    "falco":     {"nome": "Occhio di falco",   "effetti": {"gittata": 150, "vel_proiettile": 100}},
    "cannone":   {"nome": "Cannone pesante",   "effetti": {"danno": 2, "cadenza": 0.10}},
    "armatura":  {"nome": "Armatura antica",   "effetti": {"vita_max": 2, "vita": 2, "velocita": -20}},
    "reliquia":  {"nome": "Reliquia sacra",    "effetti": {"danno": 1, "velocita": 20, "vita_max": 1, "vita": 1, "gittata": 50}},
}
COLORI = {"moneta": (240, 200, 40), "cuore": (230, 60, 100), "passivo": (80, 230, 160)}


class Raccoglibile:
    """Oggetto a terra che il giocatore raccoglie toccandolo."""

    def __init__(self, tipo: str, pos: tuple[float, float],
                 id_oggetto: str | None = None) -> None:
        """Crea il raccoglibile.

        Args:
            tipo (str): "moneta", "cuore" o "passivo".
            pos (tuple[float, float]): posizione del centro.
            id_oggetto (str | None): chiave di OGGETTI (solo per i passivi).
        """
        self.tipo = tipo
        self.id = id_oggetto
        self.rect = pygame.Rect(0, 0, 22, 22)
        self.rect.center = (round(pos[0]), round(pos[1]))

    def applica(self, g) -> None:
        """Applica l'effetto al giocatore g, rispettando i limiti delle statistiche."""
        if self.tipo == "moneta":
            g.monete += 1
        elif self.tipo == "cuore":
            g.vita = min(g.vita_max, g.vita + 1)
        else:
            dati = OGGETTI[self.id]
            for stat, valore in dati["effetti"].items():
                setattr(g, stat, getattr(g, stat) + valore)
            g.cadenza = max(0.1, g.cadenza)
            g.velocita = max(120, g.velocita)
            g.vita_max = min(12, g.vita_max)
            g.vita = min(g.vita, g.vita_max)
            g.oggetti.append(dati["nome"])

    def draw(self, schermo: pygame.Surface) -> None:
        """Disegna il raccoglibile."""
        pygame.draw.rect(schermo, COLORI[self.tipo], self.rect)
