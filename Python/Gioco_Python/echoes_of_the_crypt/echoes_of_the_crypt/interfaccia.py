"""Menu, caselle di testo, tabelle, HUD e minimappa."""
from __future__ import annotations

import pygame

import audio
import grafica
from dungeon import DIREZIONI, Dungeon, Stanza
from giocatore import (ABILITA, MAESTRIA_VITTORIE, PERSONAGGI, ha_maestria, sbloccato,
                       testo_sblocco)


def testo(schermo: pygame.Surface, s: str, pos: tuple[int, int], dim: int = 32,
          colore: tuple[int, int, int] = grafica.OSSO, centrato: bool = False) -> None:
    """Scrive del testo a schermo.

    Args:
        schermo (pygame.Surface): superficie di destinazione.
        s (str): testo.
        pos (tuple[int, int]): posizione.
        dim (int): dimensione del carattere.
        colore (tuple[int, int, int]): colore RGB.
        centrato (bool): se True pos e' il centro del testo.
    """
    img = grafica.carattere(dim).render(s, True, colore)
    r = img.get_rect(center=pos) if centrato else img.get_rect(topleft=pos)
    schermo.blit(img, r)


def titolo(schermo: pygame.Surface, s: str, pos: tuple[int, int], dim: int = 72) -> None:
    """Scrive un titolo centrato, rosso sangue con l'ombra nera.

    Args:
        schermo (pygame.Surface): superficie di destinazione.
        s (str): testo.
        pos (tuple[int, int]): centro del titolo.
        dim (int): dimensione del carattere.
    """
    font = grafica.carattere(dim, titolo=True)
    for colore, scarto in (((0, 0, 0), 4), (grafica.SANGUE, 0)):
        img = font.render(s, True, colore)
        schermo.blit(img, img.get_rect(center=(pos[0] + scarto, pos[1] + scarto)))


def formatta_tempo(secondi: float) -> str:
    """Converte una durata in secondi nel formato minuti:secondi.

    Args:
        secondi (float): durata in secondi.

    Returns:
        str: durata nel formato "m:ss" (es. 125.4 -> "2:05").
    """
    totale = max(0, int(secondi))
    return f"{totale // 60}:{totale % 60:02d}"


class Tabella:
    """Schermata con titolo, intestazioni di colonna e righe di dati."""

    def __init__(self, titolo: str, colonne: list[tuple[str, int]],
                 righe: list[list[str]], vuota: str = "Nessun dato",
                 sottotitolo: str = "") -> None:
        """Crea la tabella.

        Args:
            titolo (str): titolo della schermata.
            colonne (list[tuple[str, int]]): intestazione e posizione x di ogni colonna.
            righe (list[list[str]]): una lista di celle (gia' testo) per ogni riga.
            vuota (str): messaggio mostrato quando non ci sono righe.
            sottotitolo (str): riga facoltativa sotto il titolo.
        """
        self.titolo = titolo
        self.colonne = colonne
        self.righe = righe
        self.vuota = vuota
        self.sottotitolo = sottotitolo

    def draw(self, schermo: pygame.Surface, y0: int = 190) -> None:
        """Disegna titolo, intestazioni, righe e l'istruzione per tornare al menu."""
        titolo(schermo, self.titolo, (640, 80), 64)
        if self.sottotitolo:
            testo(schermo, self.sottotitolo, (640, 130), 30, grafica.SPENTO, True)
        for nome, x in self.colonne:
            testo(schermo, nome, (x, y0), 30, grafica.ORO)
        pygame.draw.line(schermo, (90, 90, 105), (self.colonne[0][1], y0 + 30),
                         (1280 - self.colonne[0][1], y0 + 30), 2)
        if not self.righe:
            testo(schermo, self.vuota, (640, y0 + 110), 36, grafica.SPENTO, True)
        for i, riga in enumerate(self.righe):
            for cella, (_, x) in zip(riga, self.colonne):
                testo(schermo, cella, (x, y0 + 45 + i * 38), 32)
        testo(schermo, "Invio per tornare al menu", (640, 670), 30, grafica.SPENTO, True)


class CampoTesto:
    """Schermata con una casella in cui scrivere da tastiera (nome profilo, seed)."""

    def __init__(self, titolo: str, richiesta: str, lunghezza_max: int = 12,
                 solo_cifre: bool = False, iniziale: str = "") -> None:
        """Crea la casella di testo.

        Args:
            titolo (str): titolo della schermata.
            richiesta (str): riga che spiega cosa scrivere.
            lunghezza_max (int): numero massimo di caratteri.
            solo_cifre (bool): se True accetta solo le cifre da 0 a 9.
            iniziale (str): testo gia' presente all'apertura.
        """
        self.titolo = titolo
        self.richiesta = richiesta
        self.lunghezza_max = lunghezza_max
        self.solo_cifre = solo_cifre
        self.valore = iniziale[:lunghezza_max]
        self.errore = ""

    def accetta(self, carattere: str) -> bool:
        """True se il carattere puo' essere aggiunto al testo."""
        if len(carattere) != 1 or len(self.valore) >= self.lunghezza_max:
            return False
        if self.solo_cifre:
            return carattere in "0123456789"
        return carattere.isalnum() or carattere in " _-"

    def gestisci_evento(self, evento: pygame.event.Event) -> str | None:
        """Gestisce un evento tastiera.

        Returns:
            str | None: il testo confermato con Invio (mai vuoto), altrimenti None.
        """
        if evento.type != pygame.KEYDOWN:
            return None
        if evento.key == pygame.K_RETURN:
            return self.valore.strip() or None
        self.errore = ""
        if evento.key == pygame.K_BACKSPACE:
            self.valore = self.valore[:-1]
        elif self.accetta(getattr(evento, "unicode", "")):
            self.valore += evento.unicode
        return None

    def draw(self, schermo: pygame.Surface) -> None:
        """Disegna titolo, richiesta, casella con il testo ed eventuale errore."""
        titolo(schermo, self.titolo, (640, 160))
        testo(schermo, self.richiesta, (640, 260), 34, grafica.SPENTO, True)
        casella = pygame.Rect(390, 310, 500, 70)
        pygame.draw.rect(schermo, (40, 36, 48), casella)
        pygame.draw.rect(schermo, (110, 100, 130), casella, 4)
        testo(schermo, self.valore + "_", casella.center, 48, centrato=True)
        if self.errore:
            testo(schermo, self.errore, (640, 420), 30, (230, 90, 90), True)
        testo(schermo, "Invio per confermare - Esc per annullare", (640, 670), 30,
              grafica.SPENTO, True)


def a_capo(s: str, larghezza: int) -> list[str]:
    """Divide una frase in righe di al massimo `larghezza` caratteri, senza spezzare le parole."""
    righe, riga = [], ""
    for parola in s.split():
        if riga and len(riga) + 1 + len(parola) > larghezza:
            righe.append(riga)
            riga = parola
        else:
            riga = f"{riga} {parola}".strip()
    return righe + [riga] if riga else righe


class SceltaPersonaggio:
    """Schermata con una scheda per ogni personaggio (frecce sinistra/destra e Invio).

    I personaggi non ancora sbloccati si vedono ma non si possono scegliere.
    """

    def __init__(self, dati: dict | None = None,
                 vittorie: dict[str, int] | None = None) -> None:
        """Crea la schermata.

        Args:
            dati (dict | None): statistiche del profilo (decidono chi e' sbloccato).
            vittorie (dict[str, int] | None): vittorie per personaggio (chiave -> numero).
        """
        self.chiavi = list(PERSONAGGI)
        self.indice = 0
        self.dati = dati if dati is not None else {"vittorie": 10**6, "piano_record": 10**6}
        self.vittorie = vittorie or {}

    def gestisci_evento(self, evento: pygame.event.Event) -> str | None:
        """Gestisce un evento tastiera.

        Returns:
            str | None: la chiave del personaggio confermato con Invio (solo se
            sbloccato), altrimenti None.
        """
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_LEFT, pygame.K_a):
                self.indice = (self.indice - 1) % len(self.chiavi)
                audio.suona("menu")
            elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                self.indice = (self.indice + 1) % len(self.chiavi)
                audio.suona("menu")
            elif evento.key == pygame.K_RETURN:
                chiave = self.chiavi[self.indice]
                if sbloccato(chiave, self.dati):
                    return chiave
                audio.suona("colpo")
        return None

    def draw(self, schermo: pygame.Surface) -> None:
        """Disegna le schede: sprite, statistiche, abilita' e maestria (o come sbloccarlo)."""
        titolo(schermo, "SCEGLI IL PERSONAGGIO", (640, 70), 60)
        passo = 1280 // len(self.chiavi)
        for i, chiave in enumerate(self.chiavi):
            p = PERSONAGGI[chiave]
            sel = i == self.indice
            aperto = sbloccato(chiave, self.dati)
            chiaro = grafica.OSSO if sel and aperto else grafica.SPENTO
            scheda = pygame.Rect(0, 0, passo - 30, 510)
            scheda.midtop = (passo // 2 + i * passo, 125)
            pygame.draw.rect(schermo, (34, 30, 42) if sel else (20, 18, 26), scheda)
            pygame.draw.rect(schermo, grafica.ORO if sel else (60, 56, 70), scheda, 4 if sel else 2)
            img = grafica.sprite("giocatore", 7, p["tinta"] if aperto else (26, 24, 32))
            schermo.blit(img, img.get_rect(midtop=(scheda.centerx, scheda.top + 16)))
            cx, y = scheda.centerx, scheda.top + 122
            testo(schermo, p["nome"], (cx, y), 38, chiaro, True)
            if not aperto:
                testo(schermo, "BLOCCATO", (cx, y + 70), 34, grafica.SANGUE, True)
                testo(schermo, testo_sblocco(chiave), (cx, y + 110), 26, grafica.OSSO, True)
                continue
            testo(schermo, p["descrizione"], (cx, y + 32), 21, grafica.SPENTO, True)
            for j, riga in enumerate([f"Vita {p['vita']}   Danno {p['danno']}",
                                      f"Velocita' {p['velocita']}   Gittata {p['gittata']:.0f}",
                                      f"Un colpo ogni {p['cadenza']:.2f} s"]):
                testo(schermo, riga, (cx, y + 68 + j * 26), 24, chiaro, True)
            abilita = ABILITA[p["abilita"]]
            testo(schermo, f"SPAZIO: {abilita['nome']}", (cx, y + 164), 26, grafica.ORO, True)
            righe = a_capo(f"{abilita['descrizione']} (ricarica {abilita['ricarica']:g} s)", 30)
            for j, riga in enumerate(righe):
                testo(schermo, riga, (cx, y + 190 + j * 22), 21, grafica.SPENTO, True)
            vinte = self.vittorie.get(chiave, 0)
            if ha_maestria(chiave, self.vittorie):
                testo(schermo, "MAESTRIA ATTIVA", (cx, y + 274), 24, grafica.ORO, True)
            else:
                testo(schermo, f"Maestria: {vinte}/{MAESTRIA_VITTORIE} vittorie", (cx, y + 274),
                      24, grafica.SPENTO, True)
            for j, riga in enumerate(a_capo(p["maestria"], 30)):
                testo(schermo, riga, (cx, y + 300 + j * 22), 21, grafica.SPENTO, True)
        testo(schermo, "Frecce per scegliere - Invio per iniziare - Esc per tornare",
              (640, 680), 28, grafica.SPENTO, True)


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
                audio.suona("menu")
            elif evento.key == pygame.K_DOWN:
                self.indice = (self.indice + 1) % len(self.voci)
                audio.suona("menu")
            elif evento.key == pygame.K_RETURN:
                return self.voci[self.indice]
        return None

    def draw(self, schermo: pygame.Surface, y0: int = 250) -> None:
        """Disegna titolo e voci (quella scelta evidenziata)."""
        titolo(schermo, self.titolo, (640, y0 - 90))
        for i, v in enumerate(self.voci):
            sel = i == self.indice
            testo(schermo, ("> " if sel else "") + v, (640, y0 + i * 55), 44,
                  grafica.OSSO if sel else grafica.SPENTO, True)


class Hud:
    """Indicatori a schermo e minimappa."""

    # Colore sulla minimappa delle stanze speciali gia' visitate.
    COLORI_MAPPA = {"boss": (230, 200, 60), "tesoro": (80, 230, 160), "negozio": (90, 170, 240)}

    @staticmethod
    def draw(schermo: pygame.Surface, g, dungeon: Dungeon,
             corrente: Stanza, tempo: float, piano: int = 1, messaggio: str = "") -> None:
        """Disegna cuori, monete, statistiche, tempo e minimappa."""
        for i in range(g.vita_max):
            schermo.blit(grafica.sprite("cuore" if i < g.vita else "cuore_vuoto", 3),
                         (16 + i * 28, 16))
        schermo.blit(grafica.sprite("moneta", 2), (20, 54))
        testo(schermo, f"x {g.monete}", (44, 53), 28)
        testo(schermo, f"Danno {g.danno}  Vel {g.velocita:.0f}", (20, 80), 24)
        testo(schermo, f"Gittata {g.gittata:.0f}  Cad {g.cadenza:.2f}", (20, 102), 24)
        testo(schermo, f"Tempo {tempo:.0f}s", (20, 130), 24)
        testo(schermo, f"Piano {piano}", (20, 150), 24, grafica.ORO)
        if messaggio:
            testo(schermo, messaggio, (640, 60), 36, grafica.ORO, True)
        for i, nome in enumerate(g.oggetti[-5:]):
            testo(schermo, nome, (20, 180 + i * 22), 22, (120, 230, 170))
        for i, nome in enumerate(g.sinergie[-4:]):
            testo(schermo, f"+ {nome}", (20, 300 + i * 22), 22, grafica.ORO)
        # Abilita' del personaggio: barra che si riempie durante la ricarica.
        pronta = g.ricarica_abilita == 0
        testo(schermo, f"SPAZIO  {g.abilita['nome']}", (20, 636), 24,
              grafica.ORO if pronta else grafica.SPENTO)
        pygame.draw.rect(schermo, (44, 42, 54), (20, 660, 170, 8))
        pieno = 1 - g.ricarica_abilita / g.tempo_ricarica
        pygame.draw.rect(schermo, grafica.ORO if pronta else grafica.SPENTO,
                         (20, 660, round(170 * pieno), 8))
        if g.maestria:
            testo(schermo, "Maestria attiva", (20, 676), 22, grafica.ORO)
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
                col = Hud.COLORI_MAPPA.get(st.ruolo, (140, 140, 160))
            else:
                col = (44, 42, 54)
            pygame.draw.rect(schermo, col, (ox + x * s, oy + y * s, s - 3, s - 3))
