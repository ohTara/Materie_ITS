"""Generazione del piano (random walk) e logica delle stanze."""
from __future__ import annotations

import math
import random
from collections import deque

import pygame

import audio
import grafica
from nemici import Nemico, TIPI_COMUNI, crea_nemico
from oggetti import OGGETTI, PREZZI, Raccoglibile


def _centro_porta(stanza, direzione: str) -> tuple[int, int]:
    """Centro del vano della porta nella direzione data (sul muro, fuori dal pavimento)."""
    a = stanza.AREA
    return {"su": (a.centerx, a.top - 20), "giu": (a.centerx, a.bottom + 20),
            "sinistra": (a.left - 20, a.centery), "destra": (a.right + 20, a.centery)}[direzione]

DIREZIONI: dict[str, tuple[int, int]] = {
    "su": (0, -1), "giu": (0, 1), "sinistra": (-1, 0), "destra": (1, 0)}
NEMICI_MAX = 8                 # tetto di nemici in una stanza
PROB_MONETA, PROB_CUORE = 0.30, 0.10   # cosa lascia un nemico sconfitto
OPPOSTA: dict[str, str] = {"su": "giu", "giu": "su",
                           "sinistra": "destra", "destra": "sinistra"}


class Stanza:
    """Una stanza del dungeon: nemici, proiettili, oggetti e porte."""

    AREA = pygame.Rect(240, 100, 800, 520)   # zona calpestabile

    def __init__(self, coord: tuple[int, int], ruolo: str = "normale", piano: int = 1) -> None:
        """Crea la stanza.

        Args:
            coord (tuple[int, int]): posizione nella griglia del piano.
            ruolo (str): "iniziale", "normale", "tesoro", "negozio" o "boss".
            piano (int): piano del dungeon (aumenta la difficolta').
        """
        self.coord = coord
        self.ruolo = ruolo
        self.piano = piano
        self.vicini: list[str] = []       # direzioni con una porta
        self.verso_boss: set[str] = set() # porte che portano alla stanza del boss
        self.nemici: list[Nemico] = []
        self.proiettili: list = []
        self.raccoglibili: list[Raccoglibile] = []
        self.rinforzi: list[Nemico] = []  # nemici evocati, aggiunti a fine aggiornamento
        self.effetti: list[dict] = []     # anelli luminosi (vedi grafica.disegna_effetti)
        self.particelle: list[dict] = []  # particelle per feedback visivo (raccolta oggetti, ecc.)
        self.ostacoli: list[pygame.Rect] = []  # ostacoli solidi (pilastri, rocce, ecc.)
        self.visitata = False
        self.popolata = False
        self.giocatore = None
        self._sfondo = None               # immagine della stanza, creata da grafica.py

    @property
    def pulita(self) -> bool:
        """True se la stanza e' stata popolata e non ci sono nemici."""
        return self.popolata and not self.nemici

    @property
    def botola(self) -> bool:
        """True se c'e' la botola per il piano successivo (stanza del boss ripulita)."""
        return self.ruolo == "boss" and self.pulita

    def rect_botola(self) -> pygame.Rect:
        """Botola al centro della stanza: ci si scende quando il centro del giocatore ci entra."""
        r = pygame.Rect(0, 0, 56, 56)
        r.center = self.AREA.center
        return r

    def rect_porta(self, direzione: str) -> pygame.Rect:
        """Soglia della porta: si cambia stanza quando il CENTRO del giocatore ci entra.

        E' stretta (40 px, il vano e' 60) e profonda 20 px dal muro: il centro
        del giocatore arriva a 16 px dal muro, quindi bisogna andare contro la
        porta, non basta sfiorarla camminando lungo la parete.
        """
        a = self.AREA
        if direzione == "su":
            return pygame.Rect(a.centerx - 20, a.top, 40, 20)
        if direzione == "giu":
            return pygame.Rect(a.centerx - 20, a.bottom - 20, 40, 20)
        if direzione == "sinistra":
            return pygame.Rect(a.left, a.centery - 20, 20, 40)
        return pygame.Rect(a.right - 20, a.centery - 20, 20, 40)

    def entra(self, giocatore, rng: random.Random) -> None:
        """Segna la stanza visitata e la popola la prima volta."""
        self.giocatore = giocatore
        self.visitata = True
        self.proiettili.clear()
        if self.popolata:
            return
        self.popolata = True
        # Genera ostacoli/trappole PRIMA di piazzare nemici (così le collisioni funzionano subito)
        self._genera_ostacoli(rng)
        c = self.AREA.center
        if self.ruolo == "boss":
            self.nemici.append(crea_nemico(f"boss_{min(self.piano, 3)}", c[0], c[1], self.piano))
        elif self.ruolo == "tesoro":
            nuovi = [k for k, v in OGGETTI.items() if v["nome"] not in giocatore.oggetti]
            self.raccoglibili.append(
                Raccoglibile("passivo", c, rng.choice(nuovi or list(OGGETTI))))
        elif self.ruolo == "negozio":
            self._rifornisci(giocatore, rng)
        elif self.ruolo == "normale":
            self._popola_normale(giocatore, rng)

    def _genera_ostacoli(self, rng: random.Random) -> None:
        """Genera ostacoli e trappole per la stanza (chiamato da entra, non dal disegno)."""
        self.ostacoli = []
        self.trappole = []  # trappole: (rect, tipo, cooldown, danno, ultimo_attivazione)
        if self.ruolo != "normale":
            return
        a = self.AREA
        cx, cy = a.center
        # Numero ostacoli scala col piano
        num_ostacoli = rng.randint(2, 4) + (self.piano - 1) // 2
        tipi_ostacolo = ["pilastro", "roccia", "sarcofago", "statua", "pozzo"]
        for _ in range(num_ostacoli):
            tentativi = 0
            while tentativi < 30:
                ox = rng.randint(a.left + 80, a.right - 80)
                oy = rng.randint(a.top + 80, a.bottom - 80)
                if math.hypot(ox - cx, oy - cy) < 100:
                    tentativi += 1
                    continue
                troppo_vicino = False
                for d in self.vicini:
                    porta_x, porta_y = _centro_porta(self, d)
                    if math.hypot(ox - porta_x, oy - porta_y) < 120:
                        troppo_vicino = True
                        break
                if troppo_vicino:
                    tentativi += 1
                    continue
                break
            tipo = rng.choice(tipi_ostacolo)
            if tipo == "pilastro":
                w, h = 48, 48
            elif tipo == "roccia":
                w = h = rng.randint(40, 70)
            elif tipo == "statua":
                w, h = 40, 60
            elif tipo == "pozzo":
                w, h = 56, 56
            else:  # sarcofago
                w, h = 64, 36
            rect = pygame.Rect(ox - w//2, oy - h//2, w, h)
            self.ostacoli.append(rect)
        # Trappole (solo piano 2+)
        if self.piano >= 2:
            num_trappole = rng.randint(0, 2)
            tipi_trappola = ["spike", "fuoco", "veleno"]
            for _ in range(num_trappole):
                tentativi = 0
                tx = ty = 0
                while tentativi < 20:
                    tx = rng.randint(a.left + 100, a.right - 100)
                    ty = rng.randint(a.top + 100, a.bottom - 100)
                    if math.hypot(tx - cx, ty - cy) < 80:
                        tentativi += 1
                        continue
                    # Evita ostacoli
                    rect_test = pygame.Rect(tx - 24, ty - 24, 48, 48)
                    if any(rect_test.colliderect(o) for o in self.ostacoli):
                        tentativi += 1
                        continue
                    break
                tipo_t = rng.choice(tipi_trappola)
                if tipo_t == "spike":
                    dmg, cd = 1, 2.0
                elif tipo_t == "fuoco":
                    dmg, cd = 1, 1.5
                else:  # veleno
                    dmg, cd = 1, 3.0
                self.trappole.append({
                    "rect": pygame.Rect(tx - 24, ty - 24, 48, 48),
                    "tipo": tipo_t,
                    "cooldown": cd,
                    "danno": dmg,
                    "timer": 0.0,
                    "attiva": False,
                })

    def _popola_normale(self, giocatore, rng: random.Random) -> None:
        """Popola stanza normale con nemici evitando ostacoli/trappole."""
        num_nemici = min(NEMICI_MAX, rng.randint(3, 5) + self.piano - 1)
        num_cerchio = min(num_nemici, 4)
        num_casuali = num_nemici - num_cerchio
        raggio_cerchio = 180
        c = self.AREA.center
        for i in range(num_cerchio):
            angolo = (2 * math.pi * i / num_cerchio) + rng.uniform(-0.3, 0.3)
            px = c[0] + raggio_cerchio * math.cos(angolo)
            py = c[1] + raggio_cerchio * math.sin(angolo)
            px = max(self.AREA.left + 60, min(self.AREA.right - 60, px))
            py = max(self.AREA.top + 60, min(self.AREA.bottom - 60, py))
            if math.hypot(px - giocatore.pos.x, py - giocatore.pos.y) < 200:
                verso = pygame.Vector2(px, py) - giocatore.pos
                if verso.length() > 0:
                    px = giocatore.pos.x + verso.normalize().x * 200
                    py = giocatore.pos.y + verso.normalize().y * 200
            # Evita ostacoli
            rect_test = pygame.Rect(0, 0, 32, 32)
            rect_test.center = (round(px), round(py))
            if any(rect_test.colliderect(o) for o in self.ostacoli):
                px, py = c[0] + rng.uniform(-200, 200), c[1] + rng.uniform(-150, 150)
            self.nemici.append(crea_nemico(rng.choice(TIPI_COMUNI), px, py, self.piano))
        for _ in range(num_casuali):
            tentativi = 0
            while tentativi < 30:
                p = pygame.Vector2(rng.randint(self.AREA.left + 60, self.AREA.right - 60),
                                   rng.randint(self.AREA.top + 60, self.AREA.bottom - 60))
                if p.distance_to(giocatore.pos) > 200:
                    troppo_vicino = False
                    for n in self.nemici:
                        if p.distance_to(n.pos) < 100:
                            troppo_vicino = True
                            break
                    rect_test = pygame.Rect(0, 0, 32, 32)
                    rect_test.center = (round(p.x), round(p.y))
                    if any(rect_test.colliderect(o) for o in self.ostacoli):
                        troppo_vicino = True
                    if not troppo_vicino:
                        break
                tentativi += 1
            self.nemici.append(crea_nemico(rng.choice(TIPI_COMUNI), p.x, p.y, self.piano))

    def _rifornisci(self, giocatore, rng: random.Random) -> None:
        """Espone la merce del negozio: due passivi non ancora posseduti e un cuore.

        La fila sta sopra il centro, cosi' chi riprende la partita (e riparte
        dal centro della stanza) non compra nulla per sbaglio.
        """
        nuovi = [k for k, v in OGGETTI.items() if v["nome"] not in giocatore.oggetti]
        scelti = rng.sample(nuovi, min(2, len(nuovi)))
        merce = [("passivo", k) for k in scelti] + [("cuore", None)]
        y = self.AREA.centery - 90
        for i, (tipo, id_oggetto) in enumerate(merce):
            x = self.AREA.centerx + (i - (len(merce) - 1) / 2) * 200
            self.raccoglibili.append(Raccoglibile(tipo, (x, y), id_oggetto, PREZZI[tipo]))

    def update(self, dt: float) -> None:
        """Aggiorna giocatore, nemici, proiettili, collisioni, trappole e raccolta."""
        g = self.giocatore
        g.update(dt, self)
        # Aggiorna trappole
        for trappola in getattr(self, "trappole", []):
            trappola["timer"] += dt
            if trappola["attiva"]:
                if trappola["timer"] >= 0.3:  # durata attivazione visiva
                    trappola["attiva"] = False
                    trappola["timer"] = 0.0
            else:
                if trappola["timer"] >= trappola["cooldown"]:
                    # Controlla se il giocatore è sopra la trappola
                    if trappola["rect"].colliderect(g.rect):
                        trappola["attiva"] = True
                        trappola["timer"] = 0.0
                        g.subisci_danno(trappola["danno"])
                        audio.suona("danno")
                        # Particelle feedback
                        self._crea_particelle_trappola(trappola["rect"].center, trappola["tipo"])
        for n in self.nemici:
            n.update(dt, self)
            if n.rect.colliderect(g.rect):
                # Knockback: spinge il giocatore nella direzione opposta al nemico
                verso = g.pos - n.pos
                if verso.length() > 0:
                    g.subisci_danno(1, verso)
                else:
                    g.subisci_danno(1)
        for p in self.proiettili:
            p.update(dt, self)
            if p.ostile:
                if p.rect.colliderect(g.rect):
                    # Knockback nella direzione del proiettile
                    g.subisci_danno(p.danno, p.direzione)
                    p.vita = 0
            else:
                for n in self.nemici:
                    if n.vivo and id(n) not in p.colpiti and p.rect.colliderect(n.rect):
                        # Knockback: spinge il nemico nella direzione del proiettile
                        n.subisci_danno(p.danno, p.direzione)
                        audio.suona("colpo" if n.vivo else "morte")
                        if not p.perforante:
                            p.vita = 0
                            break
                        p.colpiti.add(id(n))
        for n in [n for n in self.nemici if not n.vivo]:
            g.uccisioni += 1
            g.sconfitti.add(n.tipo)            # per il bestiario del Compendio
            grafica.aggiungi_macchia(self, n.pos, n.dimensione, n.macchia)
            if random.random() < PROB_MONETA:
                self.raccoglibili.append(Raccoglibile("moneta", n.pos))
            elif random.random() < PROB_CUORE:
                self.raccoglibili.append(Raccoglibile("cuore", n.pos))
        self.nemici = [n for n in self.nemici if n.vivo] + self.rinforzi
        self.rinforzi = []
        for e in self.effetti:
            e["t"] += dt
        self.effetti = [e for e in self.effetti if e["t"] < e["durata"]]
        # Aggiorna particelle
        for part in self.particelle:
            part["t"] += dt
            part["vita"] -= dt
            # Applica velocità
            part["pos"] += part["vel"] * dt
            # Attrito
            part["vel"] *= 0.95
        self.particelle = [p for p in self.particelle if p["vita"] > 0]
        self.proiettili = [p for p in self.proiettili if p.vivo]
        for r in [r for r in self.raccoglibili if r.rect.colliderect(g.rect)]:
            if r.raccogli(g):          # False = merce che non ci si puo' permettere
                # Crea particelle di raccolta
                self._crea_particelle_raccolta(r.rect.center, r.tipo)
                # Feedback visivo statistiche per oggetti passivi
                if r.tipo == "passivo":
                    from interfaccia import Hud
                    Hud.aggiungi_feedback_pickup(g, r.id)
                self.raccoglibili.remove(r)
                audio.suona("acquisto" if r.prezzo else
                            "oggetto" if r.tipo == "passivo" else r.tipo)

    def _crea_particelle_raccolta(self, pos: tuple[float, float], tipo: str) -> None:
        """Crea particelle visive quando si raccoglie un oggetto.

        Args:
            pos (tuple[float, float]): posizione di raccolta.
            tipo (str): tipo di oggetto ("moneta", "cuore", "passivo").
        """
        colori = {
            "moneta": [(255, 220, 50), (255, 255, 150), (255, 200, 30)],
            "cuore": [(255, 80, 100), (255, 150, 180), (255, 200, 200)],
            "passivo": [(100, 255, 150), (150, 255, 200), (80, 230, 160)],
        }
        palette = colori.get(tipo, [(200, 200, 200)])
        for _ in range(12):
            angolo = random.uniform(0, 2 * math.pi)
            velocita = random.uniform(40, 120)
            self.particelle.append({
                "pos": pygame.Vector2(pos),
                "vel": pygame.Vector2(velocita * math.cos(angolo), velocita * math.sin(angolo)),
                "colore": random.choice(palette),
                "raggio": random.randint(3, 6),
                "vita": random.uniform(0.4, 0.8),
                "t": 0.0,
            })

    def _crea_particelle_trappola(self, pos: tuple[float, float], tipo: str) -> None:
        """Crea particelle visive quando una trappola si attiva."""
        colori = {
            "spike": [(220, 50, 50), (255, 100, 100), (180, 30, 30)],
            "fuoco": [(255, 140, 30), (255, 200, 50), (255, 80, 0)],
            "veleno": [(60, 200, 60), (100, 255, 100), (40, 180, 40)],
        }
        palette = colori.get(tipo, [(255, 255, 255)])
        for _ in range(16):
            angolo = random.uniform(0, 2 * math.pi)
            velocita = random.uniform(60, 150)
            self.particelle.append({
                "pos": pygame.Vector2(pos),
                "vel": pygame.Vector2(velocita * math.cos(angolo), velocita * math.sin(angolo)),
                "colore": random.choice(palette),
                "raggio": random.randint(4, 8),
                "vita": random.uniform(0.3, 0.6),
                "t": 0.0,
            })

    def draw(self, schermo: pygame.Surface) -> None:
        """Disegna stanza e porte, poi oggetti, nemici, proiettili, giocatore e infine le luci."""
        aperte = self.pulita or self.ruolo in ("iniziale", "tesoro", "negozio")
        grafica.disegna_stanza(schermo, self, aperte)
        if self.botola:
            grafica.disegna_botola(schermo, self.rect_botola())
        for e in (*self.raccoglibili, *self.nemici, self.giocatore, *self.proiettili):
            e.draw(schermo)
        grafica.disegna_luci(schermo, self)
        grafica.disegna_effetti(schermo, self)
        # Disegna particelle
        self._disegna_particelle(schermo)
        for r in self.raccoglibili:
            r.draw_cartellino(schermo, self.giocatore)

    def _disegna_particelle(self, schermo: pygame.Surface) -> None:
        """Disegna le particelle di feedback visivo."""
        for part in self.particelle:
            f = part["t"] / part["vita"]
            alfa = int(255 * (1 - f))
            raggio = int(part["raggio"] * (1 - f * 0.5))
            if raggio > 0:
                col = part["colore"]
                # Gestisce sia RGB (3) che RGBA (4) - usa solo primi 3 + nuovo alpha
                if isinstance(col, (list, tuple)) and len(col) >= 3:
                    colore = (int(col[0]), int(col[1]), int(col[2]), alfa)
                else:
                    colore = (255, 255, 255, alfa)
                pygame.draw.circle(schermo, colore, (int(part["pos"].x), int(part["pos"].y)), raggio)

    def a_dict(self) -> dict:
        """Stato salvabile della stanza (i nemici vivi non si salvano: la stanza ricomincia)."""
        return {"visitata": self.visitata, "popolata": self.pulita,
                "raccoglibili": [[r.tipo, r.rect.centerx, r.rect.centery, r.id, r.prezzo]
                                 for r in self.raccoglibili] if self.pulita else []}

    def da_dict(self, dati: dict) -> None:
        """Ripristina visitata, popolata e oggetti a terra da un salvataggio."""
        self.visitata = dati.get("visitata", False)
        self.popolata = dati.get("popolata", False)
        # Il prezzo e' il quinto valore: nei salvataggi vecchi manca (= gratis).
        self.raccoglibili = [Raccoglibile(t, (x, y), i, *resto)
                             for t, x, y, i, *resto in dati.get("raccoglibili", [])]

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
        """Random walk, poi collegamento delle celle adiacenti e ruoli
        (iniziale, boss, tesoro e negozio)."""
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
        for nome, (dx, dy) in DIREZIONI.items():      # porte segnate di rosso verso il boss
            vicina = self.stanze.get((boss[0] - dx, boss[1] - dy))
            if vicina is not None:
                vicina.verso_boss.add(nome)
        foglie = [c for c, s in self.stanze.items()
                  if len(s.vicini) == 1 and s.ruolo == "normale"]
        candidati = foglie or [c for c, s in self.stanze.items() if s.ruolo == "normale"]
        if candidati:
            self.stanze[self.rng.choice(candidati)].ruolo = "tesoro"
        # Il negozio prende un'altra stanza normale (meglio se un vicolo cieco).
        foglie = [c for c in foglie if self.stanze[c].ruolo == "normale"]
        candidati = foglie or [c for c, s in self.stanze.items() if s.ruolo == "normale"]
        if candidati:
            self.stanze[self.rng.choice(candidati)].ruolo = "negozio"

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
