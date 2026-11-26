"""Aspetto grafico del gioco: una cripta buia illuminata dalle torce.

Tutta la grafica e' generata dal programma (nessuna immagine esterna):
- gli sprite sono pixel art descritti da griglie di caratteri (SPRITE + TAVOLOZZA);
- pavimento, muri e decorazioni di ogni stanza sono disegnati una volta sola
  e poi riusati (cache), con un generatore casuale legato alla stanza;
- il buio e' un velo nero in cui giocatore, torce e proiettili "scavano" la luce.
Qui si disegna soltanto: collisioni e regole restano negli altri moduli.
"""
from __future__ import annotations

import math
import random

import pygame

# ---------- Colori del tema ----------
NERO = (10, 9, 14)             # sfondo della finestra
OSSO = (214, 208, 190)         # testo normale
SPENTO = (110, 104, 120)       # testo secondario
SANGUE = (176, 34, 44)         # titoli
ORO = (204, 168, 84)           # evidenziazioni
BUIO = 190                     # opacita' del buio (0 = giorno, 255 = nero totale)
SPESSORE_MURO = 48

# Un carattere = un colore; "." e' trasparente, "x"/"X" sono la tinta variabile.
TAVOLOZZA: dict[str, tuple[int, int, int]] = {
    "k": (12, 10, 16), "d": (48, 44, 58), "w": (228, 222, 202), "g": (150, 145, 135),
    "r": (150, 26, 36), "R": (226, 58, 70), "e": (255, 70, 60),
    "p": (74, 44, 104), "P": (128, 86, 168), "b": (52, 66, 98), "B": (96, 120, 164),
    "s": (212, 188, 164), "n": (104, 72, 48), "y": (226, 186, 70), "Y": (255, 236, 150),
    "o": (236, 130, 40), "c": (150, 222, 216), "C": (86, 150, 160),
    "v": (72, 112, 66), "V": (124, 172, 102),
}

SPRITE: dict[str, list[str]] = {
    "giocatore": ["....kkkk....", "...kxxxxk...", "..kxxxxxxk..", "..kxssssxk..",
                  "..kxksskxk..", "...kxssxk...", "..kxxxxxxk..", ".kxxXxxXxxk.",
                  ".kxxxxxxxxk.", "..kxxkkxxk..", "..knk..knk..", "..kkk..kkk.."],
    "teschio":   ["...kkkkkk...", "..kwwwwwwk..", ".kwwwwwwwwk.", ".kwwwwwwwwk.",
                  ".kwkkwwkkwk.", ".kwkewwekwk.", ".kwwwkkwwwk.", ".kgwwwwwwgk.",
                  "..kwkwkwwk..", "..kgwgwgwk..", "...kkkkkk...", "............"],
    "spettro":   ["....kkkk....", "...kcccck...", "..kcccccck..", ".kcccccccck.",
                  ".kckkcckkck.", ".kckkcckkck.", ".kcccccccck.", ".kccckkccck.",
                  ".kcCccccCck.", ".kcccccccck.", ".kckcckkcck.", "..k.kk..kk.."],
    "cultista":  ["....kkkk....", "...kppppk...", "..kppppppk..", "..kpkkkkpk..",
                  "..kpekkepk..", "..kpkkkkpk..", "...kppppk...", ".kppPppPppk.",
                  ".kppppppppk.", ".kppppppppk.", ".kppppppppk.", ".kkkkkkkkkk."],
    "ghoul":     ["...kkkkkk...", "..kvvvvvvk..", ".kvVvvvvVvk.", ".kvekvvkevk.",
                  ".kvvvvvvvvk.", ".kvkwkwkwvk.", ".kvvkkkkvvk.", "..kvvvvvvk..",
                  ".kvvk..kvvk.", ".kvk....kvk.", ".kkk....kkk.", "............"],
    "boss":      ["..k..........k..", ".kXk........kXk.", ".kxxk.kkkk.kxxk.",
                  ".kxxxkxxxxkxxxk.", "..kxxXXXXXXxxk..", "..kxxxxxxxxxxk..",
                  ".kxxkkkxxkkkxxk.", ".kxxkeekxkeekxk.", ".kxxkkkxxkkkxxk.",
                  ".kxxxxxkkxxxxxk.", "..kxxxxxxxxxxk..", "..kxwxwxwxwxxk..",
                  "..kxwxwxwxwxxk..", "...kxxxxxxxxk...", "....kkkkkkkk....",
                  "................"],
    "moneta":    ["..kkkk..", ".kyyyyk.", "kyYyyyyk", "kyYyyyyk",
                  "kyyyyyyk", "kyyyyyyk", ".kyyyyk.", "..kkkk.."],
    "cuore":     [".kk..kk.", "kRRkkRRk", "kRwRRRRk", "kRRRRRRk",
                  "kRRRRRRk", ".kRRRRk.", "..kRRk..", "...kk..."],
    "cuore_vuoto": [".kk..kk.", "kddkkddk", "kddddddk", "kddddddk",
                    "kddddddk", ".kddddk.", "..kddk..", "...kk..."],
    "passivo":   ["kkkkkkkk", "kxXxxxxk", "kxXxxxxk", ".kxxxxk.",
                  "..kxxk..", "..kxxk..", ".kxxxxk.", ".kkkkkk."],
    "torcia":    ["..nn..", "..nn..", "..nn..", "..nn..", ".kkkk."],
    # --- Nuove icone uniche per ogni oggetto passivo (10 chars wide x 12 rows) ---
    "stivali":   ["..kkkk....", "..kxXxXk..", "..kxxxxk..", ".kxxxxxxk.",  # Stivali veloci
                  "kxxxxxxxxk", "kxXXXXXXxk", "kxkxxxxkxk", ".kxxkkxxk.",
                  "..kxxkk...", "..kk..kk..", "..........", ".........."],
    "lente":     ["..kkkk....", ".kxxXxxXk.", "kxxXxxXxxk", "kxxXxxXxxk",  # Lente d'ingrandimento
                  "kxxXxxXxxk", "kxXXXXXXXk", "kxkxxxxkxk", ".kxxkkxxk.",
                  "..kxxxx...", "...kkkk...", "..........", ".........."],
    "amuleto":   ["...kkk....", "..kxxxxk..", ".kxxXXxxk.", "kxxXxxxXxk",  # Amuleto di forza
                  "kxxXxxxXxk", "kxXXXXXXXk", ".kxxxxxxk.", "..kxxxxk..",
                  "...kkkk...", "..........", "..........", ".........."],
    "caffe":     ["...kkk....", "..kxxxxk..", ".kxxXXXXk.", "kxXxXXxXxk",  # Caffe' forte
                  "kxXxXXxXxk", "kxXXXXXXXk", ".kxxxxxxk.", "..kxxxxk..",
                  "...kkkk...", "..........", "..........", ".........."],
    "cuore_ex":  ["...kkk....", "..kRRRk...", ".kRRRRRk..", "kRRRRRRRRk",  # Cuore extra
                  "kRRRRRRRRk", "kRRRRRRRRk", ".kRRRRRk..", "..kRRRk...",
                  "...kkk....", "..........", "..........", ".........."],
    "sangue":    ["...kkk....", "..kRkkk...", ".kRRRRRk..", "kRRRRRRRRk",  # Sangue antico
                  "kRkRRRkRkk", "kRRRRRRRRk", ".kRRRRRk..", "..kRRRk...",
                  "...kkk....", "..........", "..........", ".........."],
    "fiamme":    ["..kkkk....", "..kxXxXk..", "..kxxxxk..", ".kxxxxxxk.",  # Scarpe di fiamma
                  "kxxxRRRxxk", "kxRRRRRRxk", "kxRRRRRRxk", ".kxRRRRxk.",
                  "..kxxxk...", "..kk.kk...", "..........", ".........."],
    "falco":     ["..kkkk....", ".kxxxxxxk.", "kxxXXXXxxk", "kxxXXXXXxk",  # Occhio di falco
                  "kxXXXXXXXk", "kxXXXXXxXk", ".kxxxxxxk.", "..kxxkkk..",
                  "...kxk....", "....k.....", "..........", ".........."],
    "cannone":   ["...kkk....", "..kxxxxk..", ".kxxxxxxk.", "kxxxxxxxxk",  # Cannone pesante
                  "kxXXXXXXxk", "kxXkXXkXxk", "kxXkXXkXxk", ".kxXXXXxk.",
                  "..kxxxxk..", "...kkkk...", "..........", ".........."],
    "armatura":  ["..kkkkkk..", ".kxxxxxxk.", "kxxXXXXXxk", "kxXXXXXXXk",  # Armatura antica
                  "kxXXXXXXxk", "kxXXXXXXxk", "kxxxxxxxxk", ".kxxxxxxk.",
                  "..kxxxxk..", "...kkkk...", "..........", ".........."],
    "reliquia":  ["..kkkk....", ".kxxPPxxk.", "kxPPPPPPxk", "kxPxxxxPxk",  # Reliquia sacra
                  "kxPxPxxPxk", "kxPPPPPPxk", ".kxxPPxxk.", "..kxxxxk..",
                  "...kxxk...", "....kk....", "..........", ".........."],
    "clessidra": ["..kkkk....", ".kxxxxxxk.", "kxXXXXXXxk", ".kxXXXXxk.",  # Clessidra incrinata
                  "..kxXXxk..", "..kxXXxk..", ".kxXXXXxk.", "kxXXXXXXxk",
                  ".kxxxxxxk.", "..kkkk....", "..........", ".........."],
    "pietra":    ["...kkk....", "..kxxxxk..", ".kxxXXxxk.", "kxXXXXXxXk",  # Pietra affilata
                  "kxXXXXXxXk", "kxXXXXXxXk", ".kxxXXxxk.", "..kxxxxk..",
                  "...kkk....", "..........", "..........", ".........."],
    "piuma":     ["....kk....", "...kxxk...", "..kxXXxk..", ".kxXXXXxk.",  # Piuma di corvo
                  "kxXXXXXXXk", "kxXXXXXXXk", ".kxXXXXxk.", "..kxXXxk..",
                  "...kxxk...", "....kk....", "..........", ".........."],
    "elmo":      ["..kkkkkk..", ".kxxxxxxk.", "kxXXXXXXXk", "kxXkXXXxXk",  # Elmo di ferro
                  "kxXkXXXxXk", "kxXXXXXXXk", "kxXXXXXXXk", ".kxxxxxxk.",
                  "..kkkkkk..", "..........", "..........", ".........."],
    # --- Icone statistiche HUD (10 chars wide x 12 rows) ---
    "stat_danno":     ["....rr....", "...rRRr...", "..rRRRRr..", ".rRRRRRRr.",  # Spada per Danno
                       ".rRRRRRRr.", "..rRRRRr..", "...rRRr...", "....rr....",
                       "....k.....", "....k.....", "....k.....", "....k....."],
    "stat_velocita":  ["....kk....", "...kxXk...", "..kxxxxk..", ".kxxXXxxk.",  # Stivale per Velocita'
                       "kxxxxxxxxk", "kxXXXXXXxk", "kxkXXXXkxk", ".kxxXXxxk.",
                       "..kxxxxk..", "...kxxk...", "....kk....", ".........."],
    "stat_gittata":   ["....kk....", "...kXXk...", "..kXXXXk..", ".kXXkkXXk.",  # Mirino per Gittata
                       "kXXkkkkXXk", "kXXkkkkXXk", ".kXXkkXXk.", "..kXXXXk..",
                       "...kXXk...", "....kk....", "..........", ".........."],
    "stat_cadenza":   ["....kk....", "...kXXk...", "..kXXXXk..", ".kXXXXXXk.",  # Clessidra per Cadenza
                       "kXXXXXkXXk", ".kXXXXXkX.", "..kXXXXXk.", "...kXXXk..",
                       "....kXk...", "....kk....", "..........", ".........."],
    "stat_velcolpi":  ["....kk....", "...kCCk...", "..kCCCCk..", ".kCCCCCCk.",  # Proiettile veloce per Vel. colpi
                       "kCCCCCCCCk", "kCCCCCCCCk", ".kCCCCCCk.", "..kCCCCk..",
                       "...kCCk...", "....kk....", "..........", ".........."],
    # --- Pulsante toggle inventario (10 chars wide x 12 rows) ---
    "btn_toggle":     ["kkkkkkkk..", "kXXXXXXXXk", "kXkkkkkkXk", "kXkXXXXkXk",  # Pulsante griglia/lista
                       "kXkXXkXkXk", "kXkXXkXkXk", "kXkXXXXkXk", "kXkkkkkkXk",
                       "kXXXXXXXXk", "kkkkkkkk..", "..........", ".........."],
}

_cache: dict = {}


def _pronta(sup: pygame.Surface) -> pygame.Surface:
    """Converte la superficie nel formato dello schermo (piu' veloce), se c'e' una finestra."""
    return sup.convert_alpha() if pygame.display.get_surface() else sup


def _schiarisci(colore: tuple[int, int, int], quanto: int) -> tuple[int, int, int]:
    """Restituisce il colore reso piu' chiaro (o piu' scuro se quanto < 0)."""
    return tuple(max(0, min(255, c + quanto)) for c in colore)


def carattere(dim: int, titolo: bool = False) -> pygame.font.Font:
    """Restituisce il carattere della dimensione chiesta (creato una volta sola).

    Args:
        dim (int): dimensione in pixel.
        titolo (bool): se True usa, quando c'e', un carattere con le grazie in grassetto.
    """
    chiave = ("font", dim, titolo)
    if chiave not in _cache:
        if not pygame.font.get_init():
            pygame.font.init()
        percorso = None
        if titolo:
            percorso = pygame.font.match_font(
                "georgia,timesnewroman,dejavuserif,liberationserif,freeserif", bold=True)
        _cache[chiave] = pygame.font.Font(percorso, dim if percorso is None else int(dim * 0.8))
    return _cache[chiave]


def sprite(nome: str, scala: int, tinta: tuple[int, int, int] | None = None) -> pygame.Surface:
    """Costruisce (una volta sola) lo sprite indicato.

    Args:
        nome (str): chiave di SPRITE.
        scala (int): lato in pixel di ogni quadretto della griglia.
        tinta (tuple | None): colore dei caratteri "x" ("X" e' la versione chiara).

    Returns:
        pygame.Surface: immagine con sfondo trasparente.
    """
    chiave = ("sprite", nome, scala, tinta)
    if chiave not in _cache:
        griglia = SPRITE[nome]
        colori = dict(TAVOLOZZA)
        if tinta is not None:
            colori["x"], colori["X"] = tinta, _schiarisci(tinta, 60)
        img = pygame.Surface((len(griglia[0]) * scala, len(griglia) * scala), pygame.SRCALPHA)
        for riga, testo in enumerate(griglia):
            for colonna, c in enumerate(testo):
                if c != ".":
                    img.fill(colori[c], (colonna * scala, riga * scala, scala, scala))
        _cache[chiave] = _pronta(img)
    return _cache[chiave]


def _alone(raggio: int, forza: int, colore: tuple[int, int, int] | None = None) -> pygame.Surface:
    """Cerchio sfumato dal centro al bordo, fatto di anelli concentrici.

    Senza colore serve a togliere buio (canale alfa); con il colore e' un
    bagliore da sommare allo schermo.
    """
    chiave = ("alone", raggio, forza, colore)
    if chiave not in _cache:
        sup = pygame.Surface((raggio * 2, raggio * 2), pygame.SRCALPHA)
        for r in range(raggio, 0, -2):
            f = (1 - r / raggio) ** 1.2
            if colore is None:
                valore = (0, 0, 0, int(forza * f))
            else:
                valore = (*(int(c * f * forza / 255) for c in colore), 255)
            pygame.draw.circle(sup, valore, (raggio, raggio), r)
        _cache[chiave] = sup
    return _cache[chiave]


def _mattoni(sup: pygame.Surface, rng: random.Random, base: tuple[int, int, int]) -> None:
    """Riempie la superficie con un muro di mattoni di colore leggermente variabile."""
    sup.fill(_schiarisci(base, -18))
    for riga, y in enumerate(range(0, sup.get_height(), 16)):
        for x in range(-16 if riga % 2 else 0, sup.get_width(), 32):
            sup.fill(_schiarisci(base, rng.randint(-5, 5)), (x + 1, y + 1, 30, 14))


# ---------- Stanza ----------

def zona(stanza) -> pygame.Rect:
    """Rettangolo occupato dalla stanza compresi i muri."""
    return stanza.AREA.inflate(SPESSORE_MURO * 2, SPESSORE_MURO * 2)


def torce(stanza) -> list[tuple[int, int]]:
    """Posizioni delle quattro torce appese ai muri (in alto e in basso)."""
    a = stanza.AREA
    return [(x, y) for y in (a.top - 24, a.bottom + 24) for x in (a.left + 140, a.right - 140)]


def _crea_sfondo(stanza) -> pygame.Surface:
    """Disegna muri, pavimento e decorazioni della stanza (sempre uguali per quella stanza)."""
    z, a = zona(stanza), stanza.AREA
    rng = random.Random(f"{stanza.coord}-{stanza.piano}-{stanza.ruolo}")
    sup = pygame.Surface(z.size)
    _mattoni(sup, rng, (62, 56, 74))
    pav = a.move(-z.left, -z.top)
    base = {"boss": (78, 44, 50), "tesoro": (70, 64, 56), "negozio": (68, 56, 64)}.get(
        stanza.ruolo, (60, 56, 72))
    sup.fill(_schiarisci(base, -12), pav)
    for y in range(pav.top, pav.bottom, 40):               # lastre di pietra
        for x in range(pav.left, pav.right, 40):
            sup.fill(_schiarisci(base, rng.randint(-4, 4)), (x + 1, y + 1, 38, 38))
            if rng.random() < 0.10:                        # crepa
                p = (x + rng.randint(6, 34), y + rng.randint(6, 34))
                for _ in range(3):
                    q = (p[0] + rng.randint(-12, 12), p[1] + rng.randint(-12, 12))
                    pygame.draw.line(sup, _schiarisci(base, -24), p, q, 2)
                    p = q
    velo = pygame.Surface(z.size, pygame.SRCALPHA)
    for _ in range(6):                                     # macchie di muschio
        c = (rng.randint(pav.left + 30, pav.right - 30), rng.randint(pav.top + 30, pav.bottom - 30))
        pygame.draw.circle(velo, (60, 110, 62, 40), c, rng.randint(14, 34))
    for i in range(14):                                    # ombra lungo i muri
        pygame.draw.rect(velo, (0, 0, 0, 112 - i * 8), pav.inflate(-i * 4, -i * 4), 2)
    sup.blit(velo, (0, 0))
    for _ in range(rng.randint(2, 5)):                     # ossa sparse
        x, y = rng.randint(pav.left + 40, pav.right - 40), rng.randint(pav.top + 40, pav.bottom - 40)
        dx, dy = rng.choice([(9, 3), (8, -5), (3, 9)])
        pygame.draw.line(sup, (150, 145, 135), (x - dx, y - dy), (x + dx, y + dy), 3)
        pygame.draw.line(sup, (120, 116, 108), (x - dy, y + dx), (x + dy, y - dx), 2)
    cx, cy = pav.center
    # Disegna ostacoli pre-generati (da stanza.ostacoli, popolati in Stanza.entra)
    for rect_mondo in getattr(stanza, "ostacoli", []):
        # Converti coordinate mondo -> superficie
        rect = rect_mondo.move(-z.left, -z.top)
        w, h = rect.width, rect.height
        if w == 48 and h == 48:
            tipo = "pilastro"
        elif w == h and 40 <= w <= 70:
            tipo = "roccia"
        elif w == 64 and h == 36:
            tipo = "sarcofago"
        elif w == 40 and h == 60:
            tipo = "statua"
        elif w == 56 and h == 56:
            tipo = "pozzo"
        else:
            tipo = "pilastro"
        if tipo == "pilastro":
            pygame.draw.rect(sup, _schiarisci(base, -30), rect)
            pygame.draw.rect(sup, _schiarisci(base, -10), rect.inflate(-8, -8))
            pygame.draw.rect(sup, (80, 76, 92), rect, 2)
        elif tipo == "roccia":
            punti = []
            for i in range(8):
                ang = i * 2 * math.pi / 8
                r = rng.randint(min(w, h)//3, min(w, h)//2)
                punti.append((rect.centerx + r * math.cos(ang), rect.centery + r * math.sin(ang)))
            pygame.draw.polygon(sup, _schiarisci(base, -20), punti)
            pygame.draw.polygon(sup, (90, 86, 102), punti, 2)
        elif tipo == "statua":
            pygame.draw.rect(sup, (36, 32, 46), rect)
            pygame.draw.rect(sup, (66, 62, 78), rect.inflate(-6, -6))
            pygame.draw.rect(sup, (100, 96, 112), rect, 2)
            # Testa
            pygame.draw.circle(sup, (70, 66, 82), (rect.centerx, rect.top + 14), 12)
        elif tipo == "pozzo":
            pygame.draw.rect(sup, (8, 6, 10), rect)
            pygame.draw.rect(sup, (24, 22, 28), rect.inflate(-4, -4))
            pygame.draw.circle(sup, (4, 3, 6), rect.center, min(w, h)//2 - 4)
        else:  # sarcofago
            pygame.draw.rect(sup, (40, 36, 50), rect)
            pygame.draw.rect(sup, (70, 66, 82), rect.inflate(-4, -4))
            pygame.draw.rect(sup, ORO, rect, 2)
            pygame.draw.line(sup, ORO, (rect.left + 4, rect.centery), (rect.right - 4, rect.centery), 2)
    # Trappole (disegno visivo) - solo stanze normali
    if stanza.ruolo == "normale":
        for trappola in getattr(stanza, "trappole", []):
            rect = trappola["rect"].move(-z.left, -z.top)
            if trappola["tipo"] == "spike":
                pygame.draw.rect(sup, (80, 20, 20), rect)
                pygame.draw.rect(sup, (180, 40, 40), rect.inflate(-4, -4))
                # Punte
                for i in range(3):
                    x = rect.left + 8 + i * 14
                    pygame.draw.polygon(sup, (200, 60, 60),
                        [(x, rect.bottom), (x + 7, rect.top + 4), (x + 14, rect.bottom)])
            elif trappola["tipo"] == "fuoco":
                pygame.draw.rect(sup, (40, 10, 5), rect)
                for i in range(5):
                    fx = rect.left + 4 + i * 10
                    fy = rect.bottom - rng.randint(4, 16)
                    pygame.draw.polygon(sup, (255, 140, 30),
                        [(fx, rect.bottom), (fx + 5, fy), (fx + 10, rect.bottom)])
            else:  # veleno
                pygame.draw.rect(sup, (10, 40, 10), rect)
                pygame.draw.rect(sup, (60, 180, 60), rect.inflate(-4, -4))
                # Bolle
                for i in range(3):
                    bx = rect.left + 10 + i * 12
                    by = rect.centery + rng.randint(-8, 8)
                    pygame.draw.circle(sup, (100, 255, 100), (bx, by), 4)
    elif stanza.ruolo == "boss":                             # cerchio rituale
        rosso = (128, 24, 34)
        for r, w in ((150, 4), (138, 2), (60, 2)):
            pygame.draw.circle(sup, rosso, (cx, cy), r, w)
        punte = [(cx + 138 * math.cos(math.radians(60 * i - 90)),
                  cy + 138 * math.sin(math.radians(60 * i - 90))) for i in range(6)]
        for i in range(6):                                 # due triangoli intrecciati
            pygame.draw.line(sup, rosso, punte[i], punte[(i + 2) % 6], 2)
    elif stanza.ruolo == "tesoro":                         # piedistallo
        pygame.draw.rect(sup, (20, 18, 24), (cx - 34, cy - 26, 68, 68))
        pygame.draw.rect(sup, (86, 80, 96), (cx - 30, cy - 30, 60, 60))
        pygame.draw.rect(sup, ORO, (cx - 30, cy - 30, 60, 60), 3)
    elif stanza.ruolo == "negozio":                        # tappeto sotto la merce
        tappeto = pygame.Rect(0, 0, 560, 130)
        tappeto.center = (cx, cy - 90)
        pygame.draw.rect(sup, (74, 20, 28), tappeto)
        pygame.draw.rect(sup, ORO, tappeto.inflate(-12, -12), 2)
    pygame.draw.rect(sup, (78, 72, 92), pav.inflate(6, 6), 3)   # bordo chiaro del muro
    return sup


def aggiungi_macchia(stanza, pos, dimensione: int, colore: tuple[int, int, int]) -> None:
    """Lascia sul pavimento la macchia di un nemico sconfitto (resta finche' dura il piano)."""
    sfondo = getattr(stanza, "_sfondo", None)
    if sfondo is None:
        return
    z = zona(stanza)
    rng = random.Random(int(pos[0]) * 31 + int(pos[1]))
    for _ in range(7):
        c = (pos[0] - z.left + rng.randint(-dimensione, dimensione) * 0.6,
             pos[1] - z.top + rng.randint(-dimensione, dimensione) * 0.6)
        if stanza.AREA.move(-z.left, -z.top).inflate(-16, -16).collidepoint(c):
            pygame.draw.circle(sfondo, _schiarisci(colore, rng.randint(-8, 8)), c,
                               rng.randint(3, max(4, dimensione // 4)))


def _disegna_porta(schermo: pygame.Surface, stanza, direzione: str, aperta: bool) -> None:
    """Disegna un arco di pietra: passaggio buio se aperto, grata di ferro se chiuso."""
    a = stanza.AREA
    cornice, vano = {
        "su": ((a.centerx - 42, a.top - 48, 84, 48), (a.centerx - 30, a.top - 40, 60, 40)),
        "giu": ((a.centerx - 42, a.bottom, 84, 48), (a.centerx - 30, a.bottom, 60, 40)),
        "sinistra": ((a.left - 48, a.centery - 42, 48, 84), (a.left - 40, a.centery - 30, 40, 60)),
        "destra": ((a.right, a.centery - 42, 48, 84), (a.right, a.centery - 30, 40, 60)),
    }[direzione]
    vano = pygame.Rect(vano)
    verso_boss = direzione in getattr(stanza, "verso_boss", ())
    pygame.draw.rect(schermo, (120, 26, 34) if verso_boss else (84, 78, 98), cornice)
    pygame.draw.rect(schermo, (30, 27, 38), cornice, 3)
    if verso_boss:                       # cornice rossa con due teschi ai lati del vano
        c = pygame.Rect(cornice)
        lati = ([(c.left + 6, c.centery), (c.right - 6, c.centery)] if direzione in ("su", "giu")
                else [(c.centerx, c.top + 6), (c.centerx, c.bottom - 6)])
        for x, y in lati:
            pygame.draw.circle(schermo, (226, 220, 206), (x, y), 5)
            pygame.draw.circle(schermo, (20, 10, 12), (x - 2, y - 1), 1)
            pygame.draw.circle(schermo, (20, 10, 12), (x + 2, y - 1), 1)
        pygame.draw.rect(schermo, ORO, cornice, 1)
    pygame.draw.rect(schermo, (4, 3, 6) if aperta else (58, 12, 18), vano)
    if aperta:
        return
    ferro = (136, 130, 124)
    if direzione in ("su", "giu"):
        for x in range(vano.left + 6, vano.right, 12):
            pygame.draw.line(schermo, ferro, (x, vano.top), (x, vano.bottom - 1), 3)
        pygame.draw.line(schermo, ferro, (vano.left, vano.centery), (vano.right - 1, vano.centery), 3)
    else:
        for y in range(vano.top + 6, vano.bottom, 12):
            pygame.draw.line(schermo, ferro, (vano.left, y), (vano.right - 1, y), 3)
        pygame.draw.line(schermo, ferro, (vano.centerx, vano.top), (vano.centerx, vano.bottom - 1), 3)


def _tremolio(indice: int) -> float:
    """Valore tra circa 0.85 e 1.15 che cambia nel tempo: la fiamma che trema."""
    t = pygame.time.get_ticks() / 1000
    return 1 + 0.09 * math.sin(t * 9 + indice * 2.1) + 0.06 * math.sin(t * 23 + indice)


def disegna_stanza(schermo: pygame.Surface, stanza, porte_aperte: bool) -> None:
    """Disegna lo sfondo della stanza (dalla cache), le porte e le torce."""
    if getattr(stanza, "_sfondo", None) is None:
        stanza._sfondo = _crea_sfondo(stanza)
    schermo.blit(stanza._sfondo, zona(stanza).topleft)
    for d in stanza.vicini:
        _disegna_porta(schermo, stanza, d, porte_aperte)
    supporto = sprite("torcia", 3)
    for i, (x, y) in enumerate(torce(stanza)):
        schermo.blit(supporto, supporto.get_rect(midtop=(x, y - 2)))
        f = _tremolio(i)
        pygame.draw.circle(schermo, (236, 130, 40), (x, y - 5), round(7 * f))
        pygame.draw.circle(schermo, (255, 236, 150), (x, y - 4), round(3 * f))


def disegna_luci(schermo: pygame.Surface, stanza) -> None:
    """Copre la stanza di buio e lo toglie attorno a giocatore, torce, proiettili e oggetti."""
    z = zona(stanza)
    chiave = ("buio", z.size)
    if chiave not in _cache:
        _cache[chiave] = pygame.Surface(z.size, pygame.SRCALPHA)
    buio = _cache[chiave]
    buio.fill((0, 0, 0, BUIO))
    # Raggio della luce del giocatore ridotto da 250 a 180 per rendere l'illuminazione meno invadente
    luci = [(stanza.giocatore.rect.center, 180)]
    luci += [(pos, 10 * round(17 * _tremolio(i))) for i, pos in enumerate(torce(stanza))]
    luci += [(p.rect.center, 50) for p in stanza.proiettili]
    luci += [(r.rect.center, 70) for r in stanza.raccoglibili]
    porte_boss = [_centro_porta(stanza, d) for d in getattr(stanza, "verso_boss", ())]
    luci += [(pos, 110) for pos in porte_boss]
    if getattr(stanza, "botola", False):
        luci.append((stanza.AREA.center, 90))
    for (x, y), raggio in luci:
        alone = _alone(raggio, BUIO)
        buio.blit(alone, (x - z.left - raggio, y - z.top - raggio),
                  special_flags=pygame.BLEND_RGBA_SUB)
    schermo.blit(buio, z.topleft)
    # Luce fredda della lanterna: raggio ridotto da 150 a 100, intensità ridotta
    gx, gy = stanza.giocatore.rect.center
    schermo.blit(_alone(100, 18, (150, 190, 230)), (gx - 100, gy - 100),
                 special_flags=pygame.BLEND_RGB_ADD)
    for i, (x, y) in enumerate(torce(stanza)):             # bagliore caldo delle torce
        raggio = 10 * round(11 * _tremolio(i))
        schermo.blit(_alone(raggio, 70, (255, 150, 60)), (x - raggio, y - raggio),
                     special_flags=pygame.BLEND_RGB_ADD)
    for i, (x, y) in enumerate(porte_boss):                # bagliore rosso: di qui c'e' il boss
        raggio = 10 * round(9 * _tremolio(i + 7))
        schermo.blit(_alone(raggio, 90, (230, 30, 40)), (x - raggio, y - raggio),
                     special_flags=pygame.BLEND_RGB_ADD)


def disegna_botola(schermo: pygame.Surface, r: pygame.Rect) -> None:
    """Botola aperta verso il piano successivo: cornice di legno, buco nero e pioli di una scala."""
    pygame.draw.rect(schermo, (20, 18, 24), r.inflate(10, 10))
    pygame.draw.rect(schermo, (96, 66, 40), r.inflate(6, 6))
    pygame.draw.rect(schermo, (4, 3, 6), r)
    legno = (120, 86, 52)
    pygame.draw.line(schermo, legno, (r.left + 14, r.top + 4), (r.left + 14, r.bottom - 4), 3)
    pygame.draw.line(schermo, legno, (r.right - 15, r.top + 4), (r.right - 15, r.bottom - 4), 3)
    for y in range(r.top + 10, r.bottom - 4, 12):
        pygame.draw.line(schermo, legno, (r.left + 14, y), (r.right - 15, y), 3)
    pygame.draw.rect(schermo, ORO, r.inflate(6, 6), 2)


def _centro_porta(stanza, direzione: str) -> tuple[int, int]:
    """Centro del vano della porta nella direzione data (sul muro, fuori dal pavimento)."""
    a = stanza.AREA
    return {"su": (a.centerx, a.top - 20), "giu": (a.centerx, a.bottom + 20),
            "sinistra": (a.left - 20, a.centery), "destra": (a.right + 20, a.centery)}[direzione]


# ---------- Entita' e oggetti ----------

def disegna_entita(schermo: pygame.Surface, e) -> None:
    """Disegna un'entita' con il suo sprite e l'ombra (o un rettangolo, se non ha sprite)."""
    if e.sprite is None:
        pygame.draw.rect(schermo, e.colore, e.rect)
        return
    scala = max(1, round(e.dimensione * 1.25 / len(SPRITE[e.sprite])))
    img = sprite(e.sprite, scala, e.tinta)
    r = e.rect
    chiave = ("ombra", r.width)
    if chiave not in _cache:
        ombra = pygame.Surface((r.width, r.width // 3), pygame.SRCALPHA)
        pygame.draw.ellipse(ombra, (0, 0, 0, 110), ombra.get_rect())
        _cache[chiave] = ombra
    schermo.blit(_cache[chiave], _cache[chiave].get_rect(center=(r.centerx, r.bottom)))
    alzata = 0
    if e.fluttua:                                          # spettri e teschi galleggiano
        alzata = 5 + round(3 * math.sin(pygame.time.get_ticks() / 260 + e.pos.x * 0.05))
    schermo.blit(img, img.get_rect(midbottom=(r.centerx, r.bottom + scala - alzata)))
    if getattr(e, "avviso", False):                        # sta per caricare: punto esclamativo
        segno = carattere(40).render("!", True, (255, 70, 60))
        schermo.blit(segno, segno.get_rect(midbottom=(r.centerx, r.top - 8)))


def disegna_effetti(schermo: pygame.Surface, stanza) -> None:
    """Disegna gli anelli che si allargano (scudo, onda arcana, furia del boss)."""
    for e in stanza.effetti:
        f = min(1.0, e["t"] / e["durata"])
        colore = tuple(int(c * (1 - f * 0.7)) for c in e["colore"])
        pygame.draw.circle(schermo, colore, e["pos"], max(4, int(e["raggio"] * f)), 5)


def disegna_barra_boss(schermo: pygame.Surface, boss, piano: int) -> None:
    """Disegna la barra della vita del boss in alto al centro dello schermo.

    Args:
        schermo (pygame.Surface): superficie di destinazione.
        boss: istanza del boss (deve avere attributi vita, _vita_iniziale).
        piano (int): piano corrente (per il nome del boss).
    """
    if boss is None or not hasattr(boss, '_vita_iniziale'):
        return
    # Dimensioni e posizione
    larghezza = 600
    altezza = 28
    x = (schermo.get_width() - larghezza) // 2
    y = 30
    # Sfondo
    pygame.draw.rect(schermo, (40, 20, 24), (x, y, larghezza, altezza), border_radius=6)
    pygame.draw.rect(schermo, (120, 30, 36), (x, y, larghezza, altezza), 3, border_radius=6)
    # Vita attuale
    percentuale = max(0.0, boss.vita / boss._vita_iniziale)
    vita_larghezza = int((larghezza - 6) * percentuale)
    if vita_larghezza > 0:
        colore_vita = (230, 60, 70) if percentuale > 0.5 else (255, 180, 40)
        pygame.draw.rect(schermo, colore_vita, (x + 3, y + 3, vita_larghezza, altezza - 6), border_radius=4)
    # Nome del boss
    nomi_boss = {1: "Guardiano del 1° piano", 2: "Guardiano del 2° piano", 3: "Guardiano del 3° piano"}
    nome = nomi_boss.get(piano, "Boss")
    font = carattere(28, titolo=True)
    img = font.render(nome, True, (255, 240, 220))
    schermo.blit(img, img.get_rect(midbottom=(schermo.get_width() // 2, y - 6)))


def disegna_proiettile(schermo: pygame.Surface, p) -> None:
    """Disegna un proiettile come globo luminoso con scia che indica l'origine.

    La scia mostra da dove proviene il proiettile, rendendo chiari gli attacchi nemici.
    """
    colore = (255, 70, 60) if p.ostile else (150, 222, 216)
    c = p.rect.center
    # Disegna scia (linea che indica la direzione di provenienza)
    if hasattr(p, 'direzione') and p.direzione.length() > 0:
        # La scia va nella direzione opposta al movimento (verso l'origine)
        fine_scia = (c[0] - p.direzione.x * 30, c[1] - p.direzione.y * 30)
        pygame.draw.line(schermo, (*colore, 180), c, fine_scia, 4)
        pygame.draw.line(schermo, (*colore, 100), c,
                        (c[0] - p.direzione.x * 50, c[1] - p.direzione.y * 50), 2)
    # Globo luminoso
    schermo.blit(_alone(16, 150, colore), (c[0] - 16, c[1] - 16), special_flags=pygame.BLEND_RGB_ADD)
    pygame.draw.circle(schermo, colore, c, 5)
    pygame.draw.circle(schermo, (255, 250, 235), c, 2)


def disegna_raccoglibile(schermo: pygame.Surface, tipo: str, rect: pygame.Rect,
                         tinta: tuple[int, int, int] | None = None) -> None:
    """Disegna moneta, cuore o oggetto passivo (con un leggero dondolio)."""
    img = sprite(tipo, 3, tinta if tipo == "passivo" else None)
    dy = round(2 * math.sin(pygame.time.get_ticks() / 300 + rect.x * 0.1))
    schermo.blit(img, img.get_rect(center=(rect.centerx, rect.centery + dy)))


# ---------- Schermate ----------

def disegna_sfondo_menu(schermo: pygame.Surface) -> None:
    """Sfondo dei menu: un muro della cripta in penombra con due torce."""
    chiave = ("menu", schermo.get_size())
    if chiave not in _cache:
        sup = pygame.Surface(schermo.get_size())
        _mattoni(sup, random.Random(7), (40, 36, 50))
        velo = pygame.Surface(schermo.get_size(), pygame.SRCALPHA)
        velo.fill((0, 0, 0, 215))
        for x in (200, schermo.get_width() - 200):
            velo.blit(_alone(330, 150), (x - 330, 170 - 330), special_flags=pygame.BLEND_RGBA_SUB)
        sup.blit(velo, (0, 0))
        _cache[chiave] = sup
    schermo.blit(_cache[chiave], (0, 0))
    supporto = sprite("torcia", 5)
    for i, x in enumerate((200, schermo.get_width() - 200)):
        f = _tremolio(i)
        raggio = 10 * round(16 * f)
        schermo.blit(_alone(raggio, 60, (255, 150, 60)), (x - raggio, 170 - raggio),
                     special_flags=pygame.BLEND_RGB_ADD)
        schermo.blit(supporto, supporto.get_rect(midtop=(x, 172)))
        pygame.draw.circle(schermo, (236, 130, 40), (x, 164), round(12 * f))
        pygame.draw.circle(schermo, (255, 236, 150), (x, 166), round(5 * f))


def velo(schermo: pygame.Surface, opacita: int = 170) -> None:
    """Scurisce tutto lo schermo (dietro a pausa e riepilogo di fine partita)."""
    chiave = ("velo", schermo.get_size(), opacita)
    if chiave not in _cache:
        sup = pygame.Surface(schermo.get_size(), pygame.SRCALPHA)
        sup.fill((0, 0, 0, opacita))
        _cache[chiave] = sup
    schermo.blit(_cache[chiave], (0, 0))
