"""Echoes of the Crypt - ciclo di gioco principale."""
from __future__ import annotations

import json
import math
import random

import pygame

import audio
import grafica
import salvataggio
from database import get_database
from dungeon import DIREZIONI, Dungeon, Stanza
from giocatore import PERSONAGGI, PREDEFINITO, Giocatore, ha_maestria, traguardi
from interfaccia import (Aiuto, CampoTesto, Compendio, Hud, Menu, MenuImpostazioni, SceltaPersonaggio, Tabella,
                         formatta_tempo, testo, titolo)
from oggetti import OGGETTI, SINERGIE, Raccoglibile

LARGHEZZA, ALTEZZA, FPS = 1280, 720, 60
NUM_PIANI = 3
RIGHE_TABELLA = 10
SEED_MAX = 10**9          # i seed vanno da 0 a 999 999 999 (9 cifre)


def seed_del_piano(seed_partita: int, piano: int) -> int:
    """Ricava dal seed della partita il seed di un piano.

    Lo stesso seed di partita produce sempre gli stessi piani, cosi' il seed
    si puo' condividere per far giocare a un amico lo stesso dungeon.

    Args:
        seed_partita (int): seed scelto (o estratto a caso) a inizio partita.
        piano (int): numero del piano.

    Returns:
        int: seed con cui generare quel piano.
    """
    return random.Random(f"{seed_partita}-{piano}").randrange(SEED_MAX)


def testo_seed(seed: int | None) -> str:
    """Seed da mostrare in tabella ("-" per le partite registrate prima che esistesse)."""
    return "-" if seed is None else str(seed)


class Gioco:
    """Gestisce stati (menu, gioco, pausa, ...) e ciclo input-update-draw."""

    def __init__(self) -> None:
        """Inizializza pygame, finestra, menu e statistiche."""
        pygame.init()
        pygame.display.set_caption("Echoes of the Crypt")
        self._fullscreen = False
        self.schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA), pygame.SCALED)
        self.clock = pygame.time.Clock()
        audio.inizializza()
        audio.avvia_musica()
        self.db = get_database()
        self.dati = salvataggio.carica()
        self.menu_pausa = Menu("PAUSA", ["Riprendi", "Menu principale"])
        self.in_esecuzione = True
        self.vittoria = False
        self.piano = 1
        self.seed_partita = 0
        self.tempo = 0.0
        self.messaggio = ""
        self.novita: list[str] = []
        self.t_messaggio = 0.0
        self.stanza_salvata = False
        self.botola_pronta = False   # la botola funziona solo dopo esserne scesi una volta
        self._transizione_cooldown = 0.0  # evita cambi stanza immediati
        # Carica e applica impostazioni video salvate
        self._carica_e_applica_impostazioni()
        self.vai_al_menu()

    def _carica_e_applica_impostazioni(self) -> None:
        """Carica impostazioni da file e applica quelle video (fullscreen) e accessibilità."""
        import json, os
        from interfaccia import MenuImpostazioni
        path = os.path.join(os.path.dirname(__file__), "impostazioni.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    d = json.load(f)
                if d.get("schermo_intero", False):
                    self._toggle_fullscreen(True)
                # Memorizza impostazioni accessibilità
                self._impostazioni_accessibilita = {
                    "riduzione_effetti": d.get("riduzione_effetti", False),
                    "daltonici": d.get("daltonici", False),
                    "testo_grande": d.get("testo_grande", False),
                    "lingua": d.get("lingua", "it"),
                }
            except Exception:
                pass
        # Default se non caricato
        if not hasattr(self, '_impostazioni_accessibilita'):
            self._impostazioni_accessibilita = {
                "riduzione_effetti": False,
                "daltonici": False,
                "testo_grande": False,
                "lingua": "it",
            }

    def vai_al_menu(self) -> None:
        """Torna al menu; la voce 'Continua' compare solo se c'e' un checkpoint."""
        voci = (["Continua"] if salvataggio.esiste_partita() else []) \
            + ["Nuova partita", "Partita con seed", "Compendio", "Aiuto", "Impostazioni",
               "Statistiche", "Classifica", "Storico", "Profili", "Esci"]
        self.menu = Menu("ECHOES OF THE CRYPT", voci)
        self.stato = "menu"
        # Applica impostazioni video dal menu impostazioni se esiste
        if hasattr(self, 'menu_impostazioni'):
            self._applica_impostazioni_video(self.menu_impostazioni)

    def _applica_impostazioni_video(self, menu_imp: 'MenuImpostazioni') -> None:
        """Applica le impostazioni video (fullscreen, vsync) e accessibilità."""
        desired = menu_imp.schermo_intero
        if desired != self._fullscreen:
            self._toggle_fullscreen(desired)
            # Sincronizza lo stato nel menu
            menu_imp.schermo_intero = self._fullscreen
            menu_imp.salva_impostazioni()
        # Applica impostazioni accessibilità
        self._impostazioni_accessibilita = menu_imp.get_impostazioni()

    def _applica_impostazioni_accessibilita(self, impostazioni: dict) -> None:
        """Applica impostazioni di accessibilità (riduzione effetti, daltonici, testo grande)."""
        self._impostazioni_accessibilita = impostazioni

    def _toggle_fullscreen(self, attiva: bool | None = None) -> None:
        """Attiva/disattiva fullscreen mantenendo aspect ratio e pixel-perfect."""
        if attiva is None:
            attiva = not self._fullscreen
        if attiva == self._fullscreen:
            return
        try:
            if attiva:
                # Fullscreen "borderless" / exclusive - usa la risoluzione nativa dello schermo
                info = pygame.display.Info()
                self.schermo = pygame.display.set_mode(
                    (info.current_w, info.current_h),
                    pygame.FULLSCREEN | pygame.SCALED
                )
            else:
                # Ritorna a finestra 1280x720
                self.schermo = pygame.display.set_mode(
                    (LARGHEZZA, ALTEZZA),
                    pygame.SCALED  # mantiene aspect ratio e pixel-perfect
                )
            self._fullscreen = attiva
        except pygame.error:
            # Fallback se SCALED non supportato
            if attiva:
                self.schermo = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:
                self.schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
            self._fullscreen = attiva

    def _gestisci_fullscreen_eventi(self, evento: pygame.event.Event) -> None:
        """Gestisce eventi legati al fullscreen (ESC per uscire, ridimensionamento)."""
        # In pygame, ESC non esce automaticamente dal fullscreen.
        # Se siamo in fullscreen e l'utente preme ESC fuori dal gioco (es. menu pausa),
        # usciamo dal fullscreen.
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            if self._fullscreen and self.stato not in ("gioco", "pausa"):
                # Se siamo in un menu, ESC esce dal fullscreen
                self._toggle_fullscreen(False)
                if hasattr(self, 'menu_impostazioni'):
                    self.menu_impostazioni.schermo_intero = False
                    self.menu_impostazioni.salva_impostazioni()

    def apri_classifica(self) -> None:
        """Mostra le vittorie piu' veloci di tutti i profili (dati letti una volta sola)."""
        righe = [[f"{i}.", r["nome"], r.get("personaggio") or "-", formatta_tempo(r["tempo"]),
                  str(r["nemici_uccisi"]), testo_seed(r.get("seed_partita")),
                  r["data_locale"][:10]]
                 for i, r in enumerate(salvataggio.get_leaderboard(RIGHE_TABELLA), 1)]
        colonne = [("#", 90), ("Profilo", 150), ("Personaggio", 390), ("Tempo", 600),
                   ("Nemici", 720), ("Seed", 850), ("Data", 1030)]
        self.tabella = Tabella("CLASSIFICA", colonne, righe,
                               "Nessuna vittoria registrata: completa i 3 piani!",
                               "Le vittorie piu' veloci")
        self.stato = "tabella"

    def apri_storico(self) -> None:
        """Mostra le ultime partite del profilo corrente (dati letti una volta sola)."""
        profilo = salvataggio.get_profilo_corrente() or {"nome": "?"}
        righe = [[r["data_locale"][:16], "Vittoria" if r["vittoria"] else "Sconfitta",
                  r.get("personaggio") or "-", str(r["piano_raggiunto"]),
                  str(r["nemici_uccisi"]), formatta_tempo(r["tempo"]),
                  str(len(json.loads(r["oggetti_raccolti"]))), testo_seed(r.get("seed_partita"))]
                 for r in salvataggio.get_storico(limit=RIGHE_TABELLA)]
        colonne = [("Data", 60), ("Esito", 290), ("Personaggio", 430), ("Piano", 630),
                   ("Nemici", 730), ("Tempo", 850), ("Oggetti", 960), ("Seed", 1080)]
        self.tabella = Tabella("STORICO", colonne, righe,
                               "Nessuna partita giocata con questo profilo",
                               f"Ultime partite di {profilo['nome']}")
        self.stato = "tabella"

    def apri_menu_profili(self) -> None:
        """Apre il menu di selezione/creazione profili."""
        profili = salvataggio.get_profili()
        voci = []
        for p in profili:
            label = f"{p['nome']}  (P:{p['partite']} V:{p['vittorie']} PR:{p['piano_record']})"
            voci.append(label)
        voci.append("+ Nuovo profilo")
        voci.append("Indietro")
        self.menu_profili = Menu("SELEZIONA PROFILO", voci)
        self.stato = "profili"

    def gestisci_scelta_profilo(self, scelta: str) -> None:
        """Gestisce la selezione nel menu profili."""
        if scelta == "Indietro":
            self.vai_al_menu()
            return
        if scelta == "+ Nuovo profilo":
            self.crea_nuovo_profilo()
            return
        # Selezione profilo esistente: estrae ID dalla lista
        profili = salvataggio.get_profili()
        for i, p in enumerate(profili):
            label = f"{p['nome']}  (P:{p['partite']} V:{p['vittorie']} PR:{p['piano_record']})"
            if label == scelta:
                salvataggio.seleziona_profilo(p["id"])
                self.dati = salvataggio.carica()
                self.vai_al_menu()
                return

    def apri_input(self, campo: CampoTesto, conferma, annulla) -> None:
        """Apre una casella di testo.

        Args:
            campo (CampoTesto): la casella da mostrare.
            conferma: funzione chiamata con il testo scritto; restituisce un
                messaggio di errore oppure None se il testo e' stato accettato.
            annulla: funzione chiamata se il giocatore preme Esc.
        """
        self.campo = campo
        self.conferma_input = conferma
        self.annulla_input = annulla
        self.stato = "input"

    def crea_nuovo_profilo(self) -> None:
        """Chiede il nome del nuovo profilo, proponendone uno libero."""
        nomi_esistenti = {p["nome"] for p in salvataggio.get_profili()}
        i = 1
        while f"Giocatore{i}" in nomi_esistenti:
            i += 1
        self.apri_input(CampoTesto("NUOVO PROFILO", "Scrivi il nome del profilo",
                                   iniziale=f"Giocatore{i}"),
                        self.conferma_profilo, self.apri_menu_profili)

    def conferma_profilo(self, nome: str) -> str | None:
        """Crea e seleziona il profilo; restituisce un errore se il nome esiste gia'."""
        pid = salvataggio.crea_profilo(nome)
        if not pid:
            return "Esiste gia' un profilo con questo nome"
        salvataggio.seleziona_profilo(pid)
        self.dati = salvataggio.carica()
        self.vai_al_menu()
        return None

    def chiedi_seed(self) -> None:
        """Chiede il seed con cui iniziare una partita uguale a quella di un amico."""
        self.apri_input(CampoTesto("PARTITA CON SEED", "Scrivi il seed (solo cifre, massimo 9)",
                                   lunghezza_max=9, solo_cifre=True),
                        self.conferma_seed, self.vai_al_menu)

    def conferma_seed(self, valore: str) -> None:
        """Passa alla scelta del personaggio con il seed scritto dal giocatore."""
        self.apri_scelta_personaggio(int(valore))

    def vittorie_per_chiave(self) -> dict[str, int]:
        """Vittorie del profilo corrente per personaggio (chiave di PERSONAGGI -> numero)."""
        per_nome = salvataggio.get_vittorie_per_personaggio()
        return {k: per_nome.get(p["nome"], 0) for k, p in PERSONAGGI.items()}

    def apri_scelta_personaggio(self, seed: int | None = None) -> None:
        """Mostra la scelta del personaggio prima di una nuova partita.

        Args:
            seed (int | None): seed della partita che sta per iniziare (None = casuale).
        """
        self.seed_scelto = seed
        self.scelta_personaggio = SceltaPersonaggio(self.dati, self.vittorie_per_chiave())
        self.stato = "personaggio"

    def costruisci_piano(self, piano: int, seed: int | None = None) -> None:
        """Genera il dungeon del piano (piu' alto = piu' stanze e nemici piu' forti)."""
        self.piano = piano
        self.dungeon = Dungeon(num_stanze=7 + 2 * piano, seed=seed, piano=piano)

    def registra_scoperte(self) -> None:
        """Segna nel profilo oggetti, sinergie e nemici incontrati (per il Compendio)."""
        g = self.giocatore
        per_nome = {v["nome"]: k for k, v in OGGETTI.items()}
        salvataggio.registra_scoperte("oggetto", [per_nome[n] for n in g.oggetti if n in per_nome])
        per_nome = {v["nome"]: k for k, v in SINERGIE.items()}
        salvataggio.registra_scoperte("sinergia", [per_nome[n] for n in g.sinergie if n in per_nome])
        salvataggio.registra_scoperte("nemico", g.sconfitti)

    def salva_checkpoint(self) -> None:
        """Salva piano, seed, statistiche, stanza corrente e stato di tutte le stanze."""
        self.registra_scoperte()
        salvataggio.salva_partita({
            "piano": self.piano, "seed": self.dungeon.seed, "tempo": self.tempo,
            "seed_partita": self.seed_partita,
            "giocatore": self.giocatore.a_dict(), "stanza": list(self.stanza.coord),
            "stanze": {f"{x},{y}": s.a_dict() for (x, y), s in self.dungeon.stanze.items()}})

    def avvia_piano(self, piano: int, seed: int | None = None) -> None:
        """Genera il piano, mette il giocatore all'inizio e salva il checkpoint.

        Args:
            piano (int): numero del piano (piu' alto = piu' stanze e nemici piu' forti).
            seed (int | None): seme del piano; se manca si ricava dal seed della partita.
        """
        if seed is None:
            seed = seed_del_piano(self.seed_partita, piano)
        self.costruisci_piano(piano, seed)
        self.stanza = self.dungeon.stanze[(0, 0)]
        self.giocatore.pos.update(Stanza.AREA.center)
        self.giocatore.fede_usata = False          # la maestria del Templare vale una volta per piano
        self.stanza.entra(self.giocatore, self.dungeon.rng)
        self.salva_checkpoint()
        self.stanza_salvata = self.stanza.pulita
        self.botola_pronta = False

    def nuova_partita(self, seed: int | None = None, personaggio: str = PREDEFINITO) -> None:
        """Inizia una partita dal piano 1.

        Args:
            seed (int | None): seed della partita; se manca viene estratto a caso.
            personaggio (str): chiave di PERSONAGGI.
        """
        self.seed_partita = random.randrange(SEED_MAX) if seed is None else seed
        self.giocatore = Giocatore(*Stanza.AREA.center, personaggio)
        self.giocatore.maestria = ha_maestria(personaggio, self.vittorie_per_chiave())
        self.tempo = 0.0
        self.vittoria = False
        self.messaggio = ""
        self.avvia_piano(1)
        self.stato = "gioco"

    def continua_partita(self) -> None:
        """Riparte dall'inizio del piano salvato, con le statistiche di allora."""
        d = salvataggio.carica_partita()
        if d is None:
            self.nuova_partita()
            return
        self.giocatore = Giocatore(*Stanza.AREA.center)
        self.giocatore.da_dict(d["giocatore"])
        self.tempo = float(d["tempo"])
        # Nei salvataggi precedenti il seed della partita non c'era.
        seed_partita = d.get("seed_partita")
        self.seed_partita = int(d["seed"] if seed_partita is None else seed_partita)
        self.vittoria = False
        self.messaggio = ""
        self.costruisci_piano(int(d["piano"]), d["seed"])
        for chiave, stato in d.get("stanze", {}).items():
            x, y = map(int, chiave.split(","))
            if (x, y) in self.dungeon.stanze:
                self.dungeon.stanze[(x, y)].da_dict(stato)
        coord = tuple(d.get("stanza", [0, 0]))
        self.stanza = self.dungeon.stanze.get(coord, self.dungeon.stanze[(0, 0)])
        self.giocatore.pos.update(Stanza.AREA.center)
        self.stanza.entra(self.giocatore, self.dungeon.rng)
        self.stanza_salvata = self.stanza.pulita
        self.botola_pronta = False             # si riparte dal centro: magari sopra la botola
        self.stato = "gioco"

    def boss_sconfitto(self) -> None:
        """Lascia a terra il premio (un oggetto e un cuore) accanto alla botola.

        Le porte si riaprono: si puo' tornare indietro sul piano e si scende
        solo camminando sulla botola. All'ultimo piano la partita e' vinta.
        """
        if self.piano >= NUM_PIANI:
            self.fine_partita(True)
            return
        nuovi = [k for k, v in OGGETTI.items() if v["nome"] not in self.giocatore.oggetti]
        # Scelto con il generatore del piano: a parita' di seed il premio non cambia.
        chiave = self.dungeon.rng.choice(nuovi or list(OGGETTI))
        cx, cy = Stanza.AREA.center
        self.stanza.raccoglibili += [Raccoglibile("passivo", (cx - 110, cy), chiave),
                                     Raccoglibile("cuore", (cx + 110, cy))]
        # Effetto drammatico: anello espansivo dorato + particelle
        self.stanza.effetti.append({"pos": (cx, cy), "raggio": 300, "t": 0.0,
                                    "durata": 1.0, "colore": (255, 215, 60)})
        # Particelle dorate esplosive
        import random
        for _ in range(30):
            angolo = random.uniform(0, 2 * math.pi)
            velocita = random.uniform(100, 300)
            self.stanza.particelle.append({
                "pos": pygame.Vector2(cx, cy),
                "vel": pygame.Vector2(velocita * math.cos(angolo), velocita * math.sin(angolo)),
                "colore": random.choice([(255, 215, 60), (255, 255, 150), (255, 180, 40)]),
                "raggio": random.randint(4, 8),
                "vita": random.uniform(0.8, 1.5),
                "t": 0.0,
            })
        self.messaggio = "Boss sconfitto! Prendi il premio e scendi nella botola"
        self.t_messaggio = 5.0
        audio.suona("vittoria")

    def piano_completato(self) -> None:
        """Il giocatore e' sceso nella botola: si passa al piano successivo."""
        completato = self.piano
        self.avvia_piano(completato + 1)
        audio.suona("piano")
        self.messaggio = f"Piano {completato} completato!"
        self.t_messaggio = 3.0

    def _trova_posizione_sicura(self, stanza, posizione_iniziale: pygame.Vector2) -> pygame.Vector2:
        """Trova una posizione vicina a quella iniziale che non sovrapponga nemici.

        Args:
            stanza: la stanza in cui posizionarsi.
            posizione_iniziale (pygame.Vector2): posizione desiderata (vicino alla porta).

        Returns:
            pygame.Vector2: posizione sicura.
        """
        pos = pygame.Vector2(posizione_iniziale)
        # Se la stanza non è popolata o non ha nemici, va bene la posizione iniziale
        if not stanza.popolata or not stanza.nemici:
            return pos
        # Controlla collisioni con i nemici e allontana se necessario
        max_tentativi = 20
        for _ in range(max_tentativi):
            collisione = False
            for n in stanza.nemici:
                if pos.distance_to(n.pos) < (n.dimensione + self.giocatore.dimensione) / 2 + 10:
                    collisione = True
                    # Allontana dal nemico
                    verso = pos - n.pos
                    if verso.length() > 0:
                        pos += verso.normalize() * 30
                    else:
                        pos += pygame.Vector2(30, 0)
                    break
            if not collisione:
                break
        # Clamp ai limiti della stanza
        metà = self.giocatore.dimensione / 2
        pos.x = max(stanza.AREA.left + metà, min(stanza.AREA.right - metà, pos.x))
        pos.y = max(stanza.AREA.top + metà, min(stanza.AREA.bottom - metà, pos.y))
        return pos

    def cambia_stanza(self, direzione: str) -> None:
        """Passa alla stanza vicina e posiziona il giocatore alla porta opposta."""
        dx, dy = DIREZIONI[direzione]
        x, y = self.stanza.coord
        self.stanza = self.dungeon.stanze[(x + dx, y + dy)]
        a = Stanza.AREA
        arrivo = {"su": (a.centerx, a.bottom - 40), "giu": (a.centerx, a.top + 40),
                  "sinistra": (a.right - 40, a.centery), "destra": (a.left + 40, a.centery)}
        posizione_iniziale = pygame.Vector2(arrivo[direzione])
        # Trova una posizione sicura che non sovrapponga nemici
        posizione_sicura = self._trova_posizione_sicura(self.stanza, posizione_iniziale)
        self.giocatore.pos.update(posizione_sicura)
        self.stanza.entra(self.giocatore, self.dungeon.rng)
        self.botola_pronta = False
        if self.stanza.ruolo == "negozio" and self.stanza.raccoglibili:
            self.messaggio = "Negozio: tocca un oggetto per comprarlo"
            self.t_messaggio = 3.0
        self.salva_checkpoint()
        self.stanza_salvata = self.stanza.pulita

    def fine_partita(self, vittoria: bool) -> None:
        """Registra le statistiche, elimina il checkpoint (permadeath), mostra il riepilogo."""
        self.vittoria = vittoria
        audio.suona("vittoria" if vittoria else "sconfitta")
        self.registra_scoperte()
        prima = traguardi(self.dati, self.vittorie_per_chiave())
        self.dati = salvataggio.registra_partita(
            self.dati, self.giocatore.uccisioni, self.tempo, vittoria, self.piano,
            self.giocatore.oggetti, PERSONAGGI[self.giocatore.personaggio]["nome"],
            self.seed_partita)
        # Novita' sbloccate da questa partita, annunciate nel riepilogo.
        self.novita = sorted(traguardi(self.dati, self.vittorie_per_chiave()) - prima)
        salvataggio.cancella_partita()
        self.stato = "fine"

    def gestisci_eventi(self) -> None:
        """Smista gli eventi in base allo stato corrente."""
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                if self.stato in ("gioco", "pausa"):
                    self.salva_checkpoint()
                self.in_esecuzione = False
                continue
            # Gestisci fullscreen (ESC per uscire dal fullscreen nei menu)
            self._gestisci_fullscreen_eventi(ev)
            if self.stato == "input":            # qui la M e' una lettera come le altre
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    self.annulla_input()
                else:
                    valore = self.campo.gestisci_evento(ev)
                    if valore is not None:
                        self.campo.errore = self.conferma_input(valore) or ""
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_m:
                audio.cambia_muto()
            elif self.stato == "menu":
                scelta = self.menu.gestisci_evento(ev)
                if scelta == "Continua":
                    self.continua_partita()
                elif scelta == "Nuova partita":
                    self.apri_scelta_personaggio()
                elif scelta == "Partita con seed":
                    self.chiedi_seed()
                elif scelta == "Compendio":
                    self.compendio = Compendio(salvataggio.get_scoperte())
                    self.stato = "compendio"
                elif scelta == "Aiuto":
                    self.aiuto = Aiuto()
                    self.stato = "aiuto"
                elif scelta == "Impostazioni":
                    self.menu_impostazioni = MenuImpostazioni()
                    self.stato = "impostazioni"
                elif scelta == "Statistiche":
                    self.stato = "statistiche"
                elif scelta == "Classifica":
                    self.apri_classifica()
                elif scelta == "Storico":
                    self.apri_storico()
                elif scelta == "Profili":
                    self.apri_menu_profili()
                elif scelta == "Esci":
                    self.in_esecuzione = False
            elif self.stato == "personaggio":
                scelta = self.scelta_personaggio.gestisci_evento(ev)
                if scelta:
                    self.nuova_partita(self.seed_scelto, scelta)
                elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    self.vai_al_menu()
            elif self.stato == "profili":
                scelta = self.menu_profili.gestisci_evento(ev)
                if scelta:
                    self.gestisci_scelta_profilo(scelta)
                elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    self.vai_al_menu()
            elif self.stato == "gioco":
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        self.stato = "pausa"
                    elif ev.key in (pygame.K_F1, pygame.K_h):
                        self.aiuto = Aiuto()
                        self.stato = "aiuto"
            elif self.stato == "pausa":
                scelta = self.menu_pausa.gestisci_evento(ev)
                if scelta == "Riprendi" or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
                    self.stato = "gioco"
                elif scelta == "Menu principale":
                    self.salva_checkpoint()
                    self.vai_al_menu()
            elif self.stato == "compendio":
                if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    self.vai_al_menu()
                else:
                    self.compendio.gestisci_evento(ev)
            elif self.stato == "aiuto":
                if self.aiuto.gestisci_evento(ev):
                    self.vai_al_menu()
            elif self.stato == "impostazioni":
                if self.menu_impostazioni.gestisci_evento(ev):
                    self.vai_al_menu()
                # Applica impostazioni video immediatamente se cambiate
                self._applica_impostazioni_video(self.menu_impostazioni)
            elif self.stato in ("fine", "statistiche", "tabella"):
                if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    self.vai_al_menu()

    def aggiorna(self, dt: float) -> None:
        """Aggiorna la partita: stanza, porte, boss e sconfitta."""
        if self.stato != "gioco":
            return
        self.tempo += dt
        self.t_messaggio = max(0.0, self.t_messaggio - dt)
        if self.t_messaggio == 0:
            self.messaggio = ""
        # Cooldown per evitare cambi stanza immediati
        self._transizione_cooldown = max(0.0, self._transizione_cooldown - dt)
        self.stanza.update(dt)
        if self.giocatore.avvisi:              # oggetti e sinergie appena ottenuti
            self.messaggio = "  ".join(self.giocatore.avvisi)
            if any(a.startswith("Sinergia") for a in self.giocatore.avvisi):
                audio.suona("sinergia")
            self.giocatore.avvisi.clear()
            self.t_messaggio = 3.0
        if self.giocatore.vita <= 0:
            self.fine_partita(False)
        elif self.stanza.porte_aperte():
            if not self.stanza_salvata:        # stanza appena completata: salva
                if self.stanza.ruolo == "boss":
                    self.boss_sconfitto()
                    if self.stato != "gioco":  # ultimo piano: partita vinta
                        return
                audio.suona("porte")
                self.salva_checkpoint()
                self.stanza_salvata = True
            if self.stanza.botola:
                sopra = self.stanza.rect_botola().collidepoint(self.giocatore.pos)
                if sopra and self.botola_pronta:
                    self.piano_completato()
                    return
                self.botola_pronta = self.botola_pronta or not sopra
            # Cambio stanza solo se il cooldown è finito
            if self._transizione_cooldown <= 0:
                for d in self.stanza.vicini:
                    if self.stanza.rect_porta(d).collidepoint(self.giocatore.pos):
                        self.cambia_stanza(d)
                        self._transizione_cooldown = 0.5  # 500ms di cooldown
                        break

    def disegna(self) -> None:
        """Disegna la schermata in base allo stato."""
        self.schermo.fill(grafica.NERO)
        if self.stato in ("menu", "profili", "input", "tabella", "statistiche", "personaggio",
                          "compendio"):
            grafica.disegna_sfondo_menu(self.schermo)
        if self.stato == "menu":
            self.menu.draw(self.schermo)
            testo(self.schermo, f"M: audio {'spento' if audio.e_muto() else 'acceso'}",
                  (640, 695), 26, grafica.SPENTO, True)
        elif self.stato == "profili":
            self.menu_profili.draw(self.schermo)
        elif self.stato == "input":
            self.campo.draw(self.schermo)
        elif self.stato == "personaggio":
            self.scelta_personaggio.draw(self.schermo)
        elif self.stato == "tabella":
            self.tabella.draw(self.schermo)
        elif self.stato == "compendio":
            self.compendio.draw(self.schermo)
        elif self.stato == "aiuto":
            grafica.disegna_sfondo_menu(self.schermo)
            self.aiuto.draw(self.schermo)
        elif self.stato == "impostazioni":
            grafica.disegna_sfondo_menu(self.schermo)
            self.menu_impostazioni.draw(self.schermo)
        elif self.stato == "statistiche":
            titolo(self.schermo, "STATISTICHE", (640, 150), 64)
            righe = [f"Partite giocate: {self.dati['partite']}",
                     f"Vittorie: {self.dati['vittorie']}",
                     f"Piano piu' alto raggiunto: {self.dati['piano_record']}",
                     f"Record nemici sconfitti: {self.dati['record_nemici']}",
                     f"Miglior tempo: {self.dati['miglior_tempo']} s",
                     "Invio per tornare al menu"]
            for i, r in enumerate(righe):
                testo(self.schermo, r, (640, 270 + i * 50), 40, centrato=True)
        else:
            self.stanza.draw(self.schermo)
            # Barra vita boss se siamo nella stanza del boss e il boss è vivo
            if self.stanza.ruolo == "boss" and self.stanza.nemici:
                boss = self.stanza.nemici[0]  # Il boss è sempre il primo nemico
                grafica.disegna_barra_boss(self.schermo, boss, self.piano)
            Hud.draw(self.schermo, self.giocatore, self.dungeon, self.stanza,
                     self.tempo, self.piano, self.messaggio,
                     self._impostazioni_accessibilita)
            if self.stato in ("pausa", "fine"):
                grafica.velo(self.schermo)
            if self.stato == "pausa":
                self.menu_pausa.draw(self.schermo)
                testo(self.schermo, f"Seed della partita: {self.seed_partita}",
                      (640, 470), 30, grafica.SPENTO, True)
            elif self.stato == "fine":
                g = self.giocatore
                esito = "HAI VINTO!" if self.vittoria else "GAME OVER"
                titolo(self.schermo, esito, (640, 200), 80)
                for i, r in enumerate([f"{PERSONAGGI[g.personaggio]['nome']} - "
                                       f"piano raggiunto: {self.piano}",
                                       f"Nemici sconfitti: {g.uccisioni}",
                                       f"Oggetti raccolti: {len(g.oggetti)}",
                                       f"Tempo: {self.tempo:.0f} s",
                                       f"Seed della partita: {self.seed_partita}",
                                       "Invio per tornare al menu"]):
                    testo(self.schermo, r, (640, 280 + i * 44), 36, centrato=True)
                for i, r in enumerate(self.novita):
                    testo(self.schermo, r, (640, 570 + i * 30), 28, grafica.ORO, True)
        pygame.display.flip()

    def run(self) -> None:
        """Ciclo principale: eventi -> aggiornamento -> disegno a 60 FPS."""
        while self.in_esecuzione:
            dt = min(self.clock.tick(FPS) / 1000, 0.05)
            self.gestisci_eventi()
            self.aggiorna(dt)
            self.disegna()
        pygame.quit()


def main() -> None:
    """Punto di ingresso del programma."""
    Gioco().run()


if __name__ == "__main__":
    main()
