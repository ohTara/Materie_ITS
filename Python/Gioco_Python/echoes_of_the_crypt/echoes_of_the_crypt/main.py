"""Echoes of the Crypt - ciclo di gioco principale."""
from __future__ import annotations

import random

import pygame

import salvataggio
from dungeon import DIREZIONI, Dungeon, Stanza
from giocatore import Giocatore
from interfaccia import Hud, Menu, testo
from oggetti import OGGETTI, Raccoglibile

LARGHEZZA, ALTEZZA, FPS = 1280, 720, 60
NUM_PIANI = 3


class Gioco:
    """Gestisce stati (menu, gioco, pausa, ...) e ciclo input-update-draw."""

    def __init__(self) -> None:
        """Inizializza pygame, finestra, menu e statistiche."""
        pygame.init()
        pygame.display.set_caption("Echoes of the Crypt")
        self.schermo = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
        self.clock = pygame.time.Clock()
        self.dati = salvataggio.carica()
        self.menu_pausa = Menu("PAUSA", ["Riprendi", "Menu principale"])
        self.in_esecuzione = True
        self.vittoria = False
        self.piano = 1
        self.tempo = 0.0
        self.messaggio = ""
        self.t_messaggio = 0.0
        self.stanza_salvata = False
        self.vai_al_menu()

    def vai_al_menu(self) -> None:
        """Torna al menu; la voce 'Continua' compare solo se c'e' un checkpoint."""
        voci = (["Continua"] if salvataggio.esiste_partita() else []) \
            + ["Nuova partita", "Statistiche", "Esci"]
        self.menu = Menu("ECHOES OF THE CRYPT", voci)
        self.stato = "menu"

    def costruisci_piano(self, piano: int, seed: int | None = None) -> None:
        """Genera il dungeon del piano (piu' alto = piu' stanze e nemici piu' forti)."""
        self.piano = piano
        self.dungeon = Dungeon(num_stanze=7 + 2 * piano, seed=seed, piano=piano)

    def salva_checkpoint(self) -> None:
        """Salva piano, seed, statistiche, stanza corrente e stato di tutte le stanze."""
        salvataggio.salva_partita({
            "piano": self.piano, "seed": self.dungeon.seed, "tempo": self.tempo,
            "giocatore": self.giocatore.a_dict(), "stanza": list(self.stanza.coord),
            "stanze": {f"{x},{y}": s.a_dict() for (x, y), s in self.dungeon.stanze.items()}})

    def avvia_piano(self, piano: int, seed: int | None = None) -> None:
        """Genera il piano, mette il giocatore all'inizio e salva il checkpoint.

        Args:
            piano (int): numero del piano (piu' alto = piu' stanze e nemici piu' forti).
            seed (int | None): seme per rigenerare un piano salvato.
        """
        self.costruisci_piano(piano, seed)
        self.stanza = self.dungeon.stanze[(0, 0)]
        self.giocatore.pos.update(Stanza.AREA.center)
        self.stanza.entra(self.giocatore, self.dungeon.rng)
        self.salva_checkpoint()
        self.stanza_salvata = self.stanza.pulita

    def nuova_partita(self) -> None:
        """Inizia una partita dal piano 1."""
        self.giocatore = Giocatore(*Stanza.AREA.center)
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
        self.stato = "gioco"

    def piano_completato(self) -> None:
        """Boss sconfitto: premio (cura + oggetto) e passaggio al piano successivo."""
        if self.piano >= NUM_PIANI:
            self.fine_partita(True)
            return
        g = self.giocatore
        g.vita = min(g.vita_max, g.vita + 2)
        nuovi = [k for k, v in OGGETTI.items() if v["nome"] not in g.oggetti]
        premio = Raccoglibile("passivo", (0, 0), random.choice(nuovi or list(OGGETTI)))
        premio.applica(g)
        completato = self.piano
        self.avvia_piano(completato + 1)
        self.messaggio = f"Piano {completato} completato! Ottenuto: {OGGETTI[premio.id]['nome']}"
        self.t_messaggio = 4.0

    def cambia_stanza(self, direzione: str) -> None:
        """Passa alla stanza vicina e posiziona il giocatore alla porta opposta."""
        dx, dy = DIREZIONI[direzione]
        x, y = self.stanza.coord
        self.stanza = self.dungeon.stanze[(x + dx, y + dy)]
        a = Stanza.AREA
        arrivo = {"su": (a.centerx, a.bottom - 40), "giu": (a.centerx, a.top + 40),
                  "sinistra": (a.right - 40, a.centery), "destra": (a.left + 40, a.centery)}
        self.giocatore.pos.update(arrivo[direzione])
        self.stanza.entra(self.giocatore, self.dungeon.rng)
        self.salva_checkpoint()
        self.stanza_salvata = self.stanza.pulita

    def fine_partita(self, vittoria: bool) -> None:
        """Registra le statistiche, elimina il checkpoint (permadeath), mostra il riepilogo."""
        self.vittoria = vittoria
        self.dati = salvataggio.registra_partita(
            self.dati, self.giocatore.uccisioni, self.tempo, vittoria, self.piano)
        salvataggio.cancella_partita()
        self.stato = "fine"

    def gestisci_eventi(self) -> None:
        """Smista gli eventi in base allo stato corrente."""
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                if self.stato in ("gioco", "pausa"):
                    self.salva_checkpoint()
                self.in_esecuzione = False
            elif self.stato == "menu":
                scelta = self.menu.gestisci_evento(ev)
                if scelta == "Continua":
                    self.continua_partita()
                elif scelta == "Nuova partita":
                    self.nuova_partita()
                elif scelta == "Statistiche":
                    self.stato = "statistiche"
                elif scelta == "Esci":
                    self.in_esecuzione = False
            elif self.stato == "gioco":
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    self.stato = "pausa"
            elif self.stato == "pausa":
                scelta = self.menu_pausa.gestisci_evento(ev)
                if scelta == "Riprendi" or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
                    self.stato = "gioco"
                elif scelta == "Menu principale":
                    self.salva_checkpoint()
                    self.vai_al_menu()
            elif self.stato in ("fine", "statistiche"):
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
        self.stanza.update(dt)
        if self.giocatore.vita <= 0:
            self.fine_partita(False)
        elif self.stanza.ruolo == "boss" and self.stanza.pulita:
            self.piano_completato()
        elif self.stanza.porte_aperte():
            if not self.stanza_salvata:        # stanza appena completata: salva
                self.salva_checkpoint()
                self.stanza_salvata = True
            for d in self.stanza.vicini:
                if self.giocatore.rect.colliderect(self.stanza.rect_porta(d)):
                    self.cambia_stanza(d)
                    break

    def disegna(self) -> None:
        """Disegna la schermata in base allo stato."""
        self.schermo.fill((18, 16, 24))
        if self.stato == "menu":
            self.menu.draw(self.schermo)
        elif self.stato == "statistiche":
            testo(self.schermo, "STATISTICHE", (640, 150), 64, (240, 200, 90), True)
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
            Hud.draw(self.schermo, self.giocatore, self.dungeon, self.stanza,
                     self.tempo, self.piano, self.messaggio)
            if self.stato == "pausa":
                self.menu_pausa.draw(self.schermo)
            elif self.stato == "fine":
                g = self.giocatore
                titolo = "HAI VINTO!" if self.vittoria else "GAME OVER"
                testo(self.schermo, titolo, (640, 200), 80, (240, 200, 90), True)
                for i, r in enumerate([f"Piano raggiunto: {self.piano}",
                                       f"Nemici sconfitti: {g.uccisioni}",
                                       f"Oggetti raccolti: {len(g.oggetti)}",
                                       f"Tempo: {self.tempo:.0f} s",
                                       "Invio per tornare al menu"]):
                    testo(self.schermo, r, (640, 300 + i * 50), 40, centrato=True)
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
