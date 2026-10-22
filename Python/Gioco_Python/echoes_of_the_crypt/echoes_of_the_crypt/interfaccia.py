"""Menu, HUD e minimappa."""
from __future__ import annotations

import pygame

from dungeon import DIREZIONI, Dungeon, Stanza


def testo(schermo: pygame.Surface, s: str, pos: tuple[int, int], dim: int = 32,
          colore: tuple[int, int, int] = (235, 235, 235), centrato: bool = False) -> None:
    """Scrive del testo a schermo.

    Args:
        schermo (pygame.Surface): superficie di destinazione.
        s (str): testo.
        pos (tuple[int, int]): posizione.
        dim (int): dimensione del carattere.
        colore (tuple[int, int, int]): colore RGB.
        centrato (bool): se True pos e' il centro del testo.
    """
    img = pygame.font.Font(None, dim).render(s, True, colore)
    r = img.get_rect(center=pos) if centrato else img.get_rect(topleft=pos)
    schermo.blit(img, r)


class Menu:
    """Menu verticale navigabile con frecce e Invio."""

    def __init__(self, titolo: str, voci: list[str]) -> None:
        """Crea il menu con titolo e voci."""
        self.titolo = titolo
        self.voci = voci
        self.indice = 0

    def gestisci_evento(self, evento: pygame.event.Event) -> str | None:
        """Gestisce un evento tastiera.

        Returns:
            str | None: la voce confermata con Invio, altrimenti None.
        """
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self.indice = (self.indice - 1) % len(self.voci)
            elif evento.key == pygame.K_DOWN:
                self.indice = (self.indice + 1) % len(self.voci)
            elif evento.key == pygame.K_RETURN:
                return self.voci[self.indice]
        return None

    def draw(self, schermo: pygame.Surface, y0: int = 250) -> None:
        """Disegna titolo e voci (quella scelta evidenziata)."""
        testo(schermo, self.titolo, (640, y0 - 90), 72, (240, 200, 90), True)
        for i, v in enumerate(self.voci):
            sel = i == self.indice
            testo(schermo, ("> " if sel else "") + v, (640, y0 + i * 55), 44,
                  (255, 255, 255) if sel else (150, 150, 160), True)


class Hud:
    """Indicatori a schermo e minimappa."""

    @staticmethod
    def draw(schermo: pygame.Surface, g, dungeon: Dungeon,
             corrente: Stanza, tempo: float, piano: int = 1, messaggio: str = "") -> None:
        """Disegna cuori, monete, statistiche, tempo e minimappa."""
        for i in range(g.vita_max):
            col = (230, 60, 100) if i < g.vita else (70, 40, 50)
            pygame.draw.rect(schermo, col, (20 + i * 30, 20, 24, 24))
        testo(schermo, f"Monete: {g.monete}", (20, 55), 28)
        testo(schermo, f"Danno {g.danno}  Vel {g.velocita:.0f}", (20, 80), 24)
        testo(schermo, f"Gittata {g.gittata:.0f}  Cad {g.cadenza:.2f}", (20, 102), 24)
        testo(schermo, f"Tempo {tempo:.0f}s", (20, 130), 24)
        testo(schermo, f"Piano {piano}", (20, 150), 24, (240, 200, 90))
        if messaggio:
            testo(schermo, messaggio, (640, 60), 36, (240, 200, 90), True)
        for i, nome in enumerate(g.oggetti[-5:]):
            testo(schermo, nome, (20, 180 + i * 22), 22, (120, 230, 170))
        Hud._minimappa(schermo, dungeon, corrente)

    @staticmethod
    def _minimappa(schermo: pygame.Surface, dungeon: Dungeon, corrente: Stanza) -> None:
        """Mostra le stanze visitate e le loro vicine; la corrente e' bianca."""
        ox, oy, s = 1160, 80, 22
        for (x, y), st in dungeon.stanze.items():
            vicina = any(dungeon.stanze[(x + dx, y + dy)].visitata
                         for dx, dy in DIREZIONI.values() if (x + dx, y + dy) in dungeon.stanze)
            if not (st.visitata or vicina):
                continue
            if st is corrente:
                col = (255, 255, 255)
            elif st.visitata:
                col = (230, 200, 60) if st.ruolo == "boss" else (140, 140, 160)
            else:
                col = (60, 60, 75)
            pygame.draw.rect(schermo, col, (ox + x * s, oy + y * s, s - 3, s - 3))
