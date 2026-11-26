"""Oggetti raccoglibili: passivi (anche con effetti multipli), sinergie, cuori e monete."""
from __future__ import annotations

import math
import pygame

import grafica

# Ogni oggetto puo' modificare piu' statistiche insieme (bonus e malus).
OGGETTI: dict[str, dict] = {
    "stivali":   {"nome": "Stivali veloci",    "effetti": {"velocita": 40}, "sprite": "stivali"},
    "lente":     {"nome": "Lente d'ingrandimento", "effetti": {"gittata": 120}, "sprite": "lente"},
    "amuleto":   {"nome": "Amuleto di forza",  "effetti": {"danno": 1}, "sprite": "amuleto"},
    "caffe":     {"nome": "Caffe' forte",      "effetti": {"cadenza": -0.08}, "sprite": "caffe"},
    "cuore_ex":  {"nome": "Cuore extra",       "effetti": {"vita_max": 2, "vita": 2}, "sprite": "cuore_ex"},
    "sangue":    {"nome": "Sangue antico",     "effetti": {"danno": 1, "vita_max": 1, "vita": 1}, "sprite": "sangue"},
    "fiamme":    {"nome": "Scarpe di fiamma",  "effetti": {"velocita": 30, "cadenza": -0.05}, "sprite": "fiamme"},
    "falco":     {"nome": "Occhio di falco",   "effetti": {"gittata": 150, "vel_proiettile": 100}, "sprite": "falco"},
    "cannone":   {"nome": "Cannone pesante",   "effetti": {"danno": 2, "cadenza": 0.10}, "sprite": "cannone"},
    "armatura":  {"nome": "Armatura antica",   "effetti": {"vita_max": 2, "vita": 2, "velocita": -20}, "sprite": "armatura"},
    "reliquia":  {"nome": "Reliquia sacra",    "effetti": {"danno": 1, "velocita": 20, "vita_max": 1, "vita": 1, "gittata": 50}, "sprite": "reliquia"},
    "clessidra": {"nome": "Clessidra incrinata", "effetti": {"cadenza": -0.06, "vel_proiettile": 80}, "sprite": "clessidra"},
    "pietra":    {"nome": "Pietra affilata",   "effetti": {"danno": 1, "gittata": -60}, "sprite": "pietra"},
    "piuma":     {"nome": "Piuma di corvo",    "effetti": {"velocita": 50, "vel_proiettile": 60}, "sprite": "piuma"},
    "elmo":      {"nome": "Elmo di ferro",     "effetti": {"vita_max": 1, "vita": 1, "gittata": 40}, "sprite": "elmo"},
}
# Sinergie: quando il giocatore possiede tutti gli oggetti richiesti (chiavi di
# OGGETTI) ottiene, una volta sola, un bonus in piu'. Per aggiungerne una basta una voce.
SINERGIE: dict[str, dict] = {
    "passo_fuoco": {"nome": "Passo di fuoco", "richiede": ("stivali", "fiamme"),
                    "effetti": {"velocita": 30, "cadenza": -0.03}},
    "cecchino":    {"nome": "Cecchino", "richiede": ("lente", "falco"),
                    "effetti": {"danno": 1, "vel_proiettile": 100}},
    "colosso":     {"nome": "Colosso", "richiede": ("armatura", "elmo"),
                    "effetti": {"vita_max": 1, "vita": 1, "danno": 1}},
    "artiglieria": {"nome": "Artiglieria", "richiede": ("cannone", "caffe"),
                    "effetti": {"cadenza": -0.08}},
    "patto":       {"nome": "Patto di sangue", "richiede": ("sangue", "amuleto"),
                    "effetti": {"danno": 1, "vita": 2}},
    "tempesta":    {"nome": "Tempesta", "richiede": ("clessidra", "piuma"),
                    "effetti": {"cadenza": -0.04, "velocita": 20}},
}
COLORI = {"moneta": (240, 200, 40), "cuore": (230, 60, 100), "passivo": (80, 230, 160)}
# Colore di un oggetto passivo in base alla prima statistica che modifica.
COLORI_EFFETTO: dict[str, tuple[int, int, int]] = {
    "danno": (170, 40, 46), "velocita": (70, 150, 84), "gittata": (64, 104, 180),
    "vel_proiettile": (70, 160, 170), "cadenza": (200, 160, 60),
    "vita_max": (180, 70, 120), "vita": (180, 70, 120)}
# Sprite per le icone delle statistiche HUD
SPRITE_STAT: dict[str, str] = {
    "danno": "stat_danno",
    "velocita": "stat_velocita",
    "gittata": "stat_gittata",
    "cadenza": "stat_cadenza",
    "vel_proiettile": "stat_velcolpi",
}
# Prezzi in monete della merce del negozio (un negozio per piano).
PREZZI: dict[str, int] = {"cuore": 3, "passivo": 5}


def applica_effetti(g, effetti: dict[str, float]) -> None:
    """Somma gli effetti alle statistiche del giocatore g, rispettandone i limiti.

    Args:
        g: il giocatore.
        effetti (dict[str, float]): statistica -> variazione (bonus o malus).
    """
    for stat, valore in effetti.items():
        setattr(g, stat, getattr(g, stat) + valore)
    g.danno = max(1, g.danno)
    g.cadenza = max(0.1, g.cadenza)
    g.velocita = max(120, g.velocita)
    g.gittata = max(150, g.gittata)
    g.vita_max = min(12, g.vita_max)
    g.vita = min(g.vita, g.vita_max)


def attiva_sinergie(g) -> list[str]:
    """Attiva le sinergie di cui il giocatore g ha appena completato gli oggetti.

    Returns:
        list[str]: nomi delle sinergie attivate adesso (vuota se nessuna).
    """
    nuove = []
    for dati in SINERGIE.values():
        if dati["nome"] in g.sinergie:
            continue
        if all(OGGETTI[k]["nome"] in g.oggetti for k in dati["richiede"]):
            applica_effetti(g, dati["effetti"])
            g.sinergie.append(dati["nome"])
            nuove.append(dati["nome"])
    return nuove


class Raccoglibile:
    """Oggetto a terra che il giocatore raccoglie toccandolo."""

    def __init__(self, tipo: str, pos: tuple[float, float],
                 id_oggetto: str | None = None, prezzo: int = 0) -> None:
        """Crea il raccoglibile.

        Args:
            tipo (str): "moneta", "cuore" o "passivo".
            pos (tuple[float, float]): posizione del centro.
            id_oggetto (str | None): chiave di OGGETTI (solo per i passivi).
            prezzo (int): monete necessarie per prenderlo (0 = gratis).
        """
        self.tipo = tipo
        self.id = id_oggetto
        self.prezzo = prezzo
        self.rect = pygame.Rect(0, 0, 22, 22)
        self.rect.center = (round(pos[0]), round(pos[1]))

    @property
    def nome(self) -> str:
        """Nome da mostrare sul cartellino del negozio."""
        return OGGETTI[self.id]["nome"] if self.tipo == "passivo" else self.tipo.capitalize()

    def acquistabile(self, g) -> bool:
        """True se il giocatore g puo' prenderlo: monete sufficienti e, per un
        cuore in vendita, vita non gia' al massimo (per non sprecare monete)."""
        if self.prezzo == 0:
            return True
        if self.tipo == "cuore" and g.vita >= g.vita_max:
            return False
        return g.monete >= self.prezzo

    def raccogli(self, g) -> bool:
        """Fa raccogliere (o comprare) l'oggetto al giocatore g.

        Returns:
            bool: True se l'oggetto e' stato preso e va tolto dalla stanza.
        """
        if not self.acquistabile(g):
            return False
        g.monete -= self.prezzo
        self.applica(g)
        return True

    def applica(self, g) -> None:
        """Applica l'effetto al giocatore g, rispettando i limiti delle statistiche."""
        if self.tipo == "moneta":
            g.monete += 2 if g.ha("predone") else 1     # maestria del Predone
        elif self.tipo == "cuore":
            g.vita = min(g.vita_max, g.vita + 1)
        else:
            dati = OGGETTI[self.id]
            # Cattura valori vecchi per feedback
            vecchi = {stat: getattr(g, stat) for stat in dati["effetti"]}
            applica_effetti(g, dati["effetti"])
            g.oggetti.append(dati["nome"])
            # Feedback per ogni statistica modificata
            from interfaccia import Hud
            for stat, delta in dati["effetti"].items():
                nuovo = getattr(g, stat)
                vecchio = vecchi[stat]
                # Colore: verde per bonus, rosso per malus (cadenza: minore è meglio)
                if stat == "cadenza":
                    colore = (70, 200, 70) if delta < 0 else (220, 60, 60)
                else:
                    colore = (70, 200, 70) if delta > 0 else (220, 60, 60)
                Hud.aggiungi_feedback_pickup(g, stat, vecchio, nuovo, colore)
            for nome in attiva_sinergie(g):
                g.avvisi.append(f"Sinergia: {nome}!")

    def draw(self, schermo: pygame.Surface) -> None:
        """Disegna il raccoglibile (il cartellino del negozio si disegna a parte)."""
        tinta = None
        if self.tipo == "passivo":
            # Usa lo sprite unico dell'oggetto
            sprite_name = OGGETTI[self.id].get("sprite", "passivo")
            tinta = COLORI_EFFETTO[next(iter(OGGETTI[self.id]["effetti"]))]
            img = grafica.sprite(sprite_name, 3, tinta)
            dy = round(2 * math.sin(pygame.time.get_ticks() / 300 + self.rect.x * 0.1))
            schermo.blit(img, img.get_rect(center=(self.rect.centerx, self.rect.centery + dy)))
        else:
            grafica.disegna_raccoglibile(schermo, self.tipo, self.rect, tinta)

    def draw_cartellino(self, schermo: pygame.Surface, g=None) -> None:
        """Scrive nome e prezzo della merce in vendita (dopo le luci, cosi' si legge al buio).

        Args:
            schermo (pygame.Surface): superficie di destinazione.
            g: il giocatore; se non puo' comprare, il prezzo e' grigio.
        """
        if self.prezzo == 0:
            return
        ok = g is None or self.acquistabile(g)
        righe = [(self.nome, grafica.OSSO, self.rect.top - 22),
                 (f"{self.prezzo} monete", grafica.ORO if ok else grafica.SPENTO,
                  self.rect.bottom + 18)]
        for s, colore, y in righe:
            img = grafica.carattere(24).render(s, True, colore)
            schermo.blit(img, img.get_rect(center=(self.rect.centerx, y)))
