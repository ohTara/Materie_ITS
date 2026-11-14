"""Oggetti raccoglibili: passivi (anche con effetti multipli), sinergie, cuori e monete."""
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
    "clessidra": {"nome": "Clessidra incrinata", "effetti": {"cadenza": -0.06, "vel_proiettile": 80}},
    "pietra":    {"nome": "Pietra affilata",   "effetti": {"danno": 1, "gittata": -60}},
    "piuma":     {"nome": "Piuma di corvo",    "effetti": {"velocita": 50, "vel_proiettile": 60}},
    "elmo":      {"nome": "Elmo di ferro",     "effetti": {"vita_max": 1, "vita": 1, "gittata": 40}},
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
            g.monete += 1
        elif self.tipo == "cuore":
            g.vita = min(g.vita_max, g.vita + 1)
        else:
            dati = OGGETTI[self.id]
            applica_effetti(g, dati["effetti"])
            g.oggetti.append(dati["nome"])
            g.avvisi.append(f"Ottenuto: {dati['nome']}")
            for nome in attiva_sinergie(g):
                g.avvisi.append(f"Sinergia: {nome}!")

    def draw(self, schermo: pygame.Surface, g=None) -> None:
        """Disegna il raccoglibile; se e' in vendita aggiunge nome e prezzo.

        Args:
            schermo (pygame.Surface): superficie di destinazione.
            g: il giocatore; se non puo' comprare, il prezzo e' grigio.
        """
        pygame.draw.rect(schermo, COLORI[self.tipo], self.rect)
        if self.prezzo == 0:
            return
        ok = g is None or self.acquistabile(g)
        righe = [(self.nome, (235, 235, 235), self.rect.top - 22),
                 (f"{self.prezzo} monete", COLORI["moneta"] if ok else (120, 120, 130),
                  self.rect.bottom + 18)]
        for s, colore, y in righe:
            img = pygame.font.Font(None, 24).render(s, True, colore)
            schermo.blit(img, img.get_rect(center=(self.rect.centerx, y)))
