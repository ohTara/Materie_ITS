"""Menu, caselle di testo, tabelle, HUD e minimappa."""
from __future__ import annotations

import math
import pygame

import audio
import grafica
from dungeon import DIREZIONI, Dungeon, Stanza
from giocatore import (ABILITA, MAESTRIA_VITTORIE, PERSONAGGI, ha_maestria, sbloccato,
                       testo_sblocco)
from nemici import DATI_NEMICI, TIPI_COMUNI
from oggetti import (COLORI_EFFETTO, OGGETTI, SINERGIE, PREZZI, SPRITE_STAT)


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
        passo = min(55, (650 - y0) // max(1, len(self.voci) - 1))   # sempre sopra il fondo
        for i, v in enumerate(self.voci):
            sel = i == self.indice
            testo(schermo, ("> " if sel else "") + v, (640, y0 + i * passo), 44,
                  grafica.OSSO if sel else grafica.SPENTO, True)


class MenuImpostazioni:
    """Menu impostazioni con slider, toggle e rimappatura tasti."""

    CATEGORIE = ["Audio", "Video", "Controlli", "Accessibilità", "Lingua"]

    def __init__(self) -> None:
        self.categoria = 0
        self.indice = 0
        # Impostazioni default (sovrascritte da carica_impostazioni)
        self.audio_musica = 50
        self.audio_effetti = 70
        self.schermo_intero = False
        self.riduzione_effetti = False
        self.daltonici = False
        self.testo_grande = False
        self.lingua = "it"
        # Mappatura tasti default
        self.tasti = {
            "su": pygame.K_w, "giu": pygame.K_s, "sinistra": pygame.K_a, "destra": pygame.K_d,
            "sparo_su": pygame.K_UP, "sparo_giu": pygame.K_DOWN,
            "sparo_sinistra": pygame.K_LEFT, "sparo_destra": pygame.K_RIGHT,
            "abilita": pygame.K_SPACE, "muto": pygame.K_m, "pausa": pygame.K_ESCAPE,
        }
        self._in_attesa_tasto = None  # quale tasto sta rimappando
        self.carica_impostazioni()

    def carica_impostazioni(self) -> None:
        """Carica impostazioni da file JSON (o default)."""
        import json, os
        path = os.path.join(os.path.dirname(__file__), "impostazioni.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    d = json.load(f)
                self.audio_musica = d.get("audio_musica", 50)
                self.audio_effetti = d.get("audio_effetti", 70)
                self.schermo_intero = d.get("schermo_intero", False)
                self.riduzione_effetti = d.get("riduzione_effetti", False)
                self.daltonici = d.get("daltonici", False)
                self.testo_grande = d.get("testo_grande", False)
                self.lingua = d.get("lingua", "it")
                tasti_salvati = d.get("tasti", {})
                for k, v in tasti_salvati.items():
                    if k in self.tasti:
                        self.tasti[k] = v
            except Exception:
                pass
        # Applica volumi ad audio
        audio.imposta_volume_musica(self.audio_musica / 100)
        audio.imposta_volume_effetti(self.audio_effetti / 100)

    def salva_impostazioni(self) -> None:
        """Salva impostazioni su file JSON."""
        import json, os
        path = os.path.join(os.path.dirname(__file__), "impostazioni.json")
        d = {
            "audio_musica": self.audio_musica,
            "audio_effetti": self.audio_effetti,
            "schermo_intero": self.schermo_intero,
            "riduzione_effetti": self.riduzione_effetti,
            "daltonici": self.daltonici,
            "testo_grande": self.testo_grande,
            "lingua": self.lingua,
            "tasti": self.tasti,
        }
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(d, f, indent=2)
        except Exception:
            pass

    def get_impostazioni(self) -> dict:
        """Restituisce un dizionario con tutte le impostazioni correnti."""
        return {
            "audio_musica": self.audio_musica,
            "audio_effetti": self.audio_effetti,
            "schermo_intero": self.schermo_intero,
            "riduzione_effetti": self.riduzione_effetti,
            "daltonici": self.daltonici,
            "testo_grande": self.testo_grande,
            "lingua": self.lingua,
        }

    def _voci_categoria(self) -> list[tuple[str, any]]:
        """Restituisce le voci (label, chiave_attributo, tipo, extra) per la categoria corrente."""
        if self.categoria == 0:  # Audio
            return [
                ("Volume musica", "audio_musica", "slider", (0, 100)),
                ("Volume effetti", "audio_effetti", "slider", (0, 100)),
            ]
        elif self.categoria == 1:  # Video
            return [
                ("Schermo intero", "schermo_intero", "toggle", None),
                ("Riduzione effetti visivi", "riduzione_effetti", "toggle", None),
            ]
        elif self.categoria == 2:  # Controlli
            return [
                (f"Su: {pygame.key.name(self.tasti['su'])}", "su", "key", None),
                (f"Giù: {pygame.key.name(self.tasti['giu'])}", "giu", "key", None),
                (f"Sinistra: {pygame.key.name(self.tasti['sinistra'])}", "sinistra", "key", None),
                (f"Destra: {pygame.key.name(self.tasti['destra'])}", "destra", "key", None),
                (f"Sparo su: {pygame.key.name(self.tasti['sparo_su'])}", "sparo_su", "key", None),
                (f"Sparo giù: {pygame.key.name(self.tasti['sparo_giu'])}", "sparo_giu", "key", None),
                (f"Sparo sx: {pygame.key.name(self.tasti['sparo_sinistra'])}", "sparo_sinistra", "key", None),
                (f"Sparo dx: {pygame.key.name(self.tasti['sparo_destra'])}", "sparo_destra", "key", None),
                (f"Abilità: {pygame.key.name(self.tasti['abilita'])}", "abilita", "key", None),
                (f"Muto: {pygame.key.name(self.tasti['muto'])}", "muto", "key", None),
                (f"Pausa: {pygame.key.name(self.tasti['pausa'])}", "pausa", "key", None),
            ]
        elif self.categoria == 3:  # Accessibilità
            return [
                ("Modalità daltonici", "daltonici", "toggle", None),
                ("Testo grande", "testo_grande", "toggle", None),
            ]
        else:  # Lingua
            return [
                ("Italiano", "it", "radio", None),
                ("English (coming soon)", "en", "radio", None),
            ]

    def gestisci_evento(self, evento: pygame.event.Event) -> bool:
        """Gestisce input. Returns True se si deve chiudere (ESC)."""
        if self._in_attesa_tasto:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self._in_attesa_tasto = None
                    return False
                for k, v in self.tasti.items():
                    if v == evento.key and k != self._in_attesa_tasto:
                        return False
                self.tasti[self._in_attesa_tasto] = evento.key
                self._in_attesa_tasto = None
                self.salva_impostazioni()
            return False

        if evento.type != pygame.KEYDOWN:
            return False

        if evento.key == pygame.K_ESCAPE:
            self.salva_impostazioni()
            return True

        voci = self._voci_categoria()
        voce_corrente = voci[self.indice] if self.indice < len(voci) else None
        tipo_voce = voce_corrente[2] if voce_corrente else None

        # SU/GIÙ: sempre naviga tra le voci
        if evento.key == pygame.K_UP:
            self.indice = (self.indice - 1) % len(voci)
            audio.suona("menu")
            return False
        if evento.key == pygame.K_DOWN:
            self.indice = (self.indice + 1) % len(voci)
            audio.suona("menu")
            return False

        # TAB / SHIFT+TAB: cambia categoria
        if evento.key == pygame.K_TAB:
            mods = pygame.key.get_mods()
            if mods & pygame.KMOD_SHIFT:
                self.categoria = (self.categoria - 1) % len(self.CATEGORIE)
            else:
                self.categoria = (self.categoria + 1) % len(self.CATEGORIE)
            self.indice = 0
            audio.suona("menu")
            return False

        # SX/DX: SEMPRE modifica la voce corrente (slider: -/+, toggle: toggle)
        if evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
            if tipo_voce == "slider" and voce_corrente:
                label, key, tipo, extra = voce_corrente
                min_v, max_v = extra
                step = 5
                if evento.key == pygame.K_RIGHT:
                    if key == "audio_musica":
                        self.audio_musica = min(max_v, self.audio_musica + step)
                        audio.imposta_volume_musica(self.audio_musica / 100)
                    elif key == "audio_effetti":
                        self.audio_effetti = min(max_v, self.audio_effetti + step)
                        audio.imposta_volume_effetti(self.audio_effetti / 100)
                else:  # LEFT
                    if key == "audio_musica":
                        self.audio_musica = max(min_v, self.audio_musica - step)
                        audio.imposta_volume_musica(self.audio_musica / 100)
                    elif key == "audio_effetti":
                        self.audio_effetti = max(min_v, self.audio_effetti - step)
                        audio.imposta_volume_effetti(self.audio_effetti / 100)
                self.salva_impostazioni()
                audio.suona("menu")
                return False

            if tipo_voce == "toggle" and voce_corrente:
                # LEFT/RIGHT entrambi toggle
                label, key, tipo, extra = voce_corrente
                if key == "schermo_intero":
                    self.schermo_intero = not self.schermo_intero
                elif key == "riduzione_effetti":
                    self.riduzione_effetti = not self.riduzione_effetti
                elif key == "daltonici":
                    self.daltonici = not self.daltonici
                elif key == "testo_grande":
                    self.testo_grande = not self.testo_grande
                self.salva_impostazioni()
                audio.suona("menu")
                return False

            # Per key e radio: SX/DX non fa nulla (usano INVIO)
            return False

        # INVIO: toggle o remap
        if evento.key == pygame.K_RETURN and voce_corrente:
            label, key, tipo, extra = voce_corrente
            if tipo == "key":
                self._in_attesa_tasto = key
            elif tipo == "toggle":
                if key == "schermo_intero":
                    self.schermo_intero = not self.schermo_intero
                elif key == "riduzione_effetti":
                    self.riduzione_effetti = not self.riduzione_effetti
                elif key == "daltonici":
                    self.daltonici = not self.daltonici
                elif key == "testo_grande":
                    self.testo_grande = not self.testo_grande
                self.salva_impostazioni()
            elif tipo == "radio" and self.categoria == 4:
                self.lingua = key
                self.salva_impostazioni()
            audio.suona("menu")
        return False

    def draw(self, schermo: pygame.Surface) -> None:
        """Disegna il menu impostazioni."""
        titolo(schermo, "IMPOSTAZIONI", (640, 50), 56)
        # Categorie in alto
        for i, cat in enumerate(self.CATEGORIE):
            col = grafica.ORO if i == self.categoria else grafica.SPENTO
            testo(schermo, cat, (150 + i * 220, 110), 26, col, True)
        pygame.draw.line(schermo, (60, 56, 70), (100, 140), (1180, 140), 2)
        # Voci categoria
        voci = self._voci_categoria()
        for i, (label, key, tipo, extra) in enumerate(voci):
            sel = i == self.indice
            x_base = 150 if sel else 170
            y = 180 + i * 40
            prefisso = "> " if sel else "  "
            colore = grafica.OSSO if sel else grafica.SPENTO
            if tipo == "slider":
                min_v, max_v = extra
                val = self.audio_musica if key == "audio_musica" else self.audio_effetti
                pct = (val - min_v) / (max_v - min_v)
                barra_w = 300
                pygame.draw.rect(schermo, (44, 42, 54), (x_base + 250, y, barra_w, 16), border_radius=4)
                pygame.draw.rect(schermo, grafica.ORO, (x_base + 250, y, round(barra_w * pct), 16), border_radius=4)
                pygame.draw.rect(schermo, (90, 90, 105), (x_base + 250, y, barra_w, 16), 2, border_radius=4)
                testo(schermo, f"{prefisso}{label}: {val}%", (x_base, y), 28, colore)
            elif tipo == "toggle":
                val = (key == "schermo_intero" and self.schermo_intero) or \
                      (key == "riduzione_effetti" and self.riduzione_effetti) or \
                      (key == "daltonici" and self.daltonici) or \
                      (key == "testo_grande" and self.testo_grande)
                check = "[X]" if val else "[ ]"
                testo(schermo, f"{prefisso}{label} {check}", (x_base, y), 28, colore)
            elif tipo == "key":
                in_attesa = self._in_attesa_tasto == key
                tasto_nome = "..." if in_attesa else pygame.key.name(self.tasti[key])
                testo(schermo, f"{prefisso}{label.replace(pygame.key.name(self.tasti[key]), tasto_nome)}", (x_base, y), 28,
                      grafica.ORO if in_attesa else colore)
            elif tipo == "radio":
                attivo = (self.categoria == 4 and self.lingua == key)
                radio = "(*)" if attivo else "( )"
                testo(schermo, f"{prefisso}{label} {radio}", (x_base, y), 28, colore)
        # Istruzioni
        if self._in_attesa_tasto:
            testo(schermo, "Premi il nuovo tasto (ESC per annullare)", (640, 620), 26, grafica.SANGUE, True)
        else:
            testo(schermo, "TAB / MAIUSC+TAB: Cambia categoria  |  FRECCE SU/GIÙ: Sceglie voce  |  FRECCE SX/DX: Slider -/+ / Toggle  |  INVIO: Toggle/Remap tasto  |  ESC: Torna",
                  (640, 680), 24, grafica.SPENTO, True)


class Hud:
    """Indicatori a schermo, minimappa e inventario."""

    # Colore sulla minimappa delle stanze speciali gia' visitate.
    COLORI_MAPPA = {"boss": (230, 200, 60), "tesoro": (80, 230, 160), "negozio": (90, 170, 240)}

    @staticmethod
    def draw(schermo: pygame.Surface, g, dungeon: Dungeon,
             corrente: Stanza, tempo: float, piano: int = 1, messaggio: str = "",
             impostazioni_accessibilita: dict | None = None) -> None:
        """Disegna HUD completo: statistiche sx centrato, minimappa dx, inventario dx centrato, feedback pickup.

        Args:
            impostazioni_accessibilita: dict con chiavi 'riduzione_effetti', 'daltonici', 'testo_grande', 'lingua'
        """
        if impostazioni_accessibilita is None:
            impostazioni_accessibilita = {"riduzione_effetti": False, "daltonici": False, "testo_grande": False, "lingua": "it"}

        testo_grande = impostazioni_accessibilita.get("testo_grande", False)
        daltonici = impostazioni_accessibilita.get("daltonici", False)

        # Inizializza attributi per feedback pickup se non esistono
        if not hasattr(g, "_pickup_feedback"):
            g._pickup_feedback = []  # lista di (stat_key, vecchio, nuovo, timer, colore)

        # ============================================================
        # LATO SINISTRO: Cuori/Monete in alto, Statistiche CENTRATE, Abilità in basso
        # ============================================================
        left_x = 16

        # Cuori (in alto a sinistra)
        for i in range(g.vita_max):
            schermo.blit(grafica.sprite("cuore" if i < g.vita else "cuore_vuoto", 3),
                         (left_x + i * 28, 16))

        # Monete (sotto i cuori)
        monete_y = 16 + ((g.vita_max + 1) // 2) * 28 + 8
        schermo.blit(grafica.sprite("moneta", 2), (left_x, monete_y))
        fs = 28 if testo_grande else 24
        testo(schermo, f"x {g.monete}", (left_x + 24, monete_y - 1), fs)

        # Statistiche centrato verticalmente a sinistra
        stats_list = [
            ("danno", g.danno, grafica.SANGUE, True),           # intero
            ("velocita", g.velocita, (70, 150, 84), False),     # decimale
            ("gittata", g.gittata, (64, 104, 180), False),      # decimale
            ("cadenza", g.cadenza, (200, 160, 60), False),      # decimale (2 decimali)
            ("vel_proiettile", g.vel_proiettile, (70, 160, 170), False),  # decimale
        ]
        stat_names = {"danno": "Danno", "velocita": "Velocità", "gittata": "Gittata",
                      "cadenza": "Cadenza", "vel_proiettile": "Vel. colpi"}

        def fmt_val(stat_key: str, valore: float) -> str:
            """Formatta il valore per la visualizzazione: intero o 2 decimali."""
            if stat_key in ("danno", "vita_max", "vita"):
                return str(int(round(valore)))
            return f"{valore:.2f}".rstrip('0').rstrip('.') if valore != int(valore) else str(int(valore))

        # Calcola area statistiche
        stat_h = 34 if testo_grande else 28
        num_stats = len(stats_list)
        stats_total_h = num_stats * stat_h
        stats_start_y = (720 - stats_total_h) // 2

        for i, (stat_key, val, colore, is_int) in enumerate(stats_list):
            y = stats_start_y + i * stat_h
            # Icona statistica unica
            sprite_name = SPRITE_STAT.get(stat_key, "stat_danno")
            img = grafica.sprite(sprite_name, 2, colore)
            schermo.blit(img, (left_x, y - 2))
            # Valore numerico formattato
            nome = stat_names.get(stat_key, stat_key)
            # Feedback pickup: mostra "vecchio -> nuovo" se c'è animazione per questa stat
            display_val = fmt_val(stat_key, val)
            feedback_color = colore
            for fb_stat, fb_vecchio, fb_nuovo, fb_timer, fb_col in g._pickup_feedback:
                if fb_stat == stat_key and fb_timer > 0:
                    v_old = fmt_val(stat_key, fb_vecchio)
                    v_new = fmt_val(stat_key, fb_nuovo)
                    display_val = f"{v_old} -> {v_new}"
                    feedback_color = fb_col
                    break
            fs = 22 if testo_grande else 18
            testo(schermo, f"{nome}: {display_val}", (left_x + 28, y), fs, feedback_color)

        # Sinergie attive (sotto le statistiche)
        sinergie_y = stats_start_y + stats_total_h + 16
        for i, nome in enumerate(g.sinergie[-4:]):
            fs = 24 if testo_grande else 20
            testo(schermo, f"+ {nome}", (left_x, sinergie_y + i * 26), fs, grafica.ORO)

        # Abilità personaggio: in basso a sinistra
        pronta = g.ricarica_abilita == 0
        ability_y = 636
        testo(schermo, f"SPAZIO  {g.abilita['nome']}", (left_x, ability_y), 22,
              grafica.ORO if pronta else grafica.SPENTO)
        pygame.draw.rect(schermo, (44, 42, 54), (left_x, ability_y + 24, 180, 8))
        pieno = 1 - g.ricarica_abilita / g.tempo_ricarica if g.tempo_ricarica > 0 else 1
        pygame.draw.rect(schermo, grafica.ORO if pronta else grafica.SPENTO,
                         (left_x, ability_y + 24, round(180 * pieno), 8))
        if g.maestria:
            testo(schermo, "Maestria attiva", (left_x, ability_y + 44), 20, grafica.ORO)

        # Tempo e piano (in alto a sinistra, accanto ai cuori)
        tempo_y = 16 + g.vita_max * 28 + 8
        testo(schermo, f"Tempo {int(tempo)}s", (left_x, tempo_y), 22)
        testo(schermo, f"Piano {piano}", (left_x, tempo_y + 24), 22, grafica.ORO)

        # Messaggio centrale (es. boss, pickup)
        if messaggio:
            testo(schermo, messaggio, (640, 60), 36, grafica.ORO, True)

        # ============================================================
        # FEEDBACK PICKUP: aggiorna timer (animazione per ogni stat)
        # ============================================================
        g._pickup_feedback = [(s, v, n, t - 1/60, c) for s, v, n, t, c in g._pickup_feedback if t > 0]

        # ============================================================
        # MINIMAPPA (destra, in alto)
        # ============================================================
        Hud._minimappa(schermo, dungeon, corrente)

        # ============================================================
        # INVENTARIO (destra, centrato verticalmente sotto minimappa)
        # ============================================================
        Hud._disegna_inventario(schermo, g)

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
            elif st.ruolo == "boss":
                col = (180, 60, 70)
            elif st.ruolo == "tesoro":
                col = (60, 180, 120)
            elif st.ruolo == "negozio":
                col = (70, 140, 200)
            else:
                col = (44, 42, 54)
            pygame.draw.rect(schermo, col, (ox + x * s, oy + y * s, s - 3, s - 3))
            if st.visitata and st.ruolo != "normale":
                cx = ox + x * s + (s - 3) // 2
                cy = oy + y * s + (s - 3) // 2
                if st.ruolo == "boss":
                    pygame.draw.circle(schermo, (255, 220, 80), (cx, cy), 3)
                elif st.ruolo == "tesoro":
                    pygame.draw.rect(schermo, (255, 220, 80), (cx - 2, cy - 2, 4, 4))
                elif st.ruolo == "negozio":
                    pygame.draw.line(schermo, (255, 220, 80), (cx - 3, cy), (cx + 3, cy), 2)
                    pygame.draw.line(schermo, (255, 220, 80), (cx, cy - 3), (cx, cy + 3), 2)

    @staticmethod
    def _disegna_inventario(schermo: pygame.Surface, g) -> None:
        """Disegna l'inventario compatto a destra, centrato verticalmente sotto la minimappa."""
        # Posizione: sotto la minimappa, centrato verticalmente nello spazio rimanente
        minimap_bottom = 80 + 20 * 22  # minimappa finisce circa qui
        larghezza = 180
        icon_size = 36
        padding = 8
        cols = 4
        rows = 4
        grid_w = cols * (icon_size + padding) - padding + 16
        grid_h = rows * (icon_size + padding) - padding + 50  # +50 per titolo e toggle

        ox = 1280 - grid_w - 10
        oy = (720 - grid_h) // 2 + 30  # Sotto minimappa, centrato

        # Inizializza modalità inventario se non esiste
        if not hasattr(g, "_inv_compact_mode"):
            g._inv_compact_mode = False  # False = Estesa, True = Compatta

        # Reverse map: display name -> internal key
        nome_a_chiave = {v["nome"]: k for k, v in OGGETTI.items()}

        # Sfondo semi-trasparente
        surf_bg = pygame.Surface((grid_w, grid_h), pygame.SRCALPHA)
        surf_bg.fill((20, 18, 26, 220))
        schermo.blit(surf_bg, (ox, oy))
        pygame.draw.rect(schermo, (80, 76, 90), (ox, oy, grid_w, grid_h), 2)

        # Titolo + toggle
        titolo_x = ox + grid_w // 2
        testo(schermo, "INVENTARIO", (titolo_x, oy + 16), 20, grafica.ORO, True)
        # Pulsante toggle modalità
        btn_rect = pygame.Rect(ox + grid_w - 36, oy + 4, 32, 32)
        btn_col = grafica.ORO if g._inv_compact_mode else grafica.SPENTO
        img = grafica.sprite("btn_toggle", 2, btn_col)
        schermo.blit(img, img.get_rect(center=btn_rect.center))
        # Tooltip toggle
        mouse_pos = pygame.mouse.get_pos()
        if btn_rect.collidepoint(mouse_pos):
            tooltip = "Modalità Compatta (icone)" if not g._inv_compact_mode else "Modalità Estesa (lista)"
            tip_surf = grafica.carattere(16).render(tooltip, True, grafica.OSSO)
            schermo.blit(tip_surf, (btn_rect.left - tip_surf.get_width() - 4, btn_rect.centery - 8))

        if not g.oggetti:
            modo = "Compatta" if g._inv_compact_mode else "Estesa"
            testo(schermo, f"Vuoto ({modo})", (titolo_x, oy + grid_h // 2), 18, grafica.SPENTO, True)
            return

        # Area griglia/lista
        grid_start_y = oy + 44
        item_h = 24 if not g._inv_compact_mode else (icon_size + padding)

        if g._inv_compact_mode:
            # --- MODALITÀ COMPATTA: Griglia 4x4 di sole icone ---
            max_items = cols * rows
            inizio = max(0, len(g.oggetti) - max_items)
            for idx, nome in enumerate(g.oggetti[inizio:]):
                chiave = nome_a_chiave.get(nome)
                if not chiave:
                    continue
                dati = OGGETTI[chiave]
                col_idx = idx % cols
                row_idx = idx // cols
                ix = ox + 8 + col_idx * (icon_size + padding)
                iy = grid_start_y + row_idx * (icon_size + padding)
                # Icona oggetto unica
                sprite_name = dati.get("sprite", "passivo")
                effetto = next(iter(dati["effetti"]))
                col = COLORI_EFFETTO.get(effetto, grafica.OSSO)
                img = grafica.sprite(sprite_name, 3, col)
                r = img.get_rect(center=(ix + icon_size // 2, iy + icon_size // 2))
                schermo.blit(img, r)
                # Tooltip al passaggio mouse
                mouse_pos = pygame.mouse.get_pos()
                if r.collidepoint(mouse_pos):
                    tooltip_text = f"{dati['nome']}\n{descrivi_effetti(dati['effetti'])[0]}"
                    # Draw tooltip
                    lines = tooltip_text.split('\n')
                    tip_w = max(grafica.carattere(16).size(l)[0] for l in lines) + 16
                    tip_h = len(lines) * 20 + 10
                    tip_x = min(r.right + 8, 1280 - tip_w - 8)
                    tip_y = r.centery - tip_h // 2
                    tip_surf = pygame.Surface((tip_w, tip_h), pygame.SRCALPHA)
                    tip_surf.fill((20, 18, 26, 240))
                    pygame.draw.rect(tip_surf, (80, 76, 90), (0, 0, tip_w, tip_h), 2)
                    for li, line in enumerate(lines):
                        t = grafica.carattere(16).render(line, True, grafica.OSSO)
                        tip_surf.blit(t, (8, 5 + li * 20))
                    schermo.blit(tip_surf, (tip_x, tip_y))
        else:
            # --- MODALITÀ ESTESA: Lista verticale icona + nome ---
            riga_h = 28
            max_righe = (grid_h - 50) // riga_h
            inizio = max(0, len(g.oggetti) - max_righe)
            for i, nome in enumerate(g.oggetti[inizio:]):
                chiave = nome_a_chiave.get(nome)
                if not chiave:
                    continue
                dati = OGGETTI[chiave]
                y = grid_start_y + i * riga_h
                # Icona oggetto unica
                sprite_name = dati.get("sprite", "passivo")
                effetto = next(iter(dati["effetti"]))
                col = COLORI_EFFETTO.get(effetto, grafica.OSSO)
                img = grafica.sprite(sprite_name, 2, col)
                r = img.get_rect(center=(ox + 24, y + riga_h // 2))
                schermo.blit(img, r)
                # Nome
                testo(schermo, dati["nome"], (ox + 48, y + 4), 18, grafica.OSSO)

    @staticmethod
    def aggiungi_feedback_pickup(giocatore, stat_key: str, vecchio: float, nuovo: float,
                                  colore: tuple[int, int, int] = grafica.ORO) -> None:
        """Aggiunge un feedback di pickup per una specifica statistica.

        Args:
            giocatore: istanza Giocatore
            stat_key (str): chiave della statistica (es. "danno", "velocita")
            vecchio (float): valore precedente
            nuovo (float): valore nuovo
            colore (tuple): colore RGB del feedback (verde per bonus, rosso per malus)
        """
        if not hasattr(giocatore, "_pickup_feedback"):
            giocatore._pickup_feedback = []
        # Durata 3.5 secondi con dissolvenza
        giocatore._pickup_feedback.append((stat_key, vecchio, nuovo, 3.5, colore))


# Nome da mostrare per ogni statistica che un oggetto o una sinergia modifica.
NOMI_STATISTICHE = {"danno": "Danno", "velocita": "Velocita'", "gittata": "Gittata",
                    "cadenza": "Tempo tra i colpi", "vel_proiettile": "Velocita' dei colpi",
                    "vita_max": "Cuori massimi", "vita": "Cura"}


def descrivi_effetti(effetti: dict[str, float]) -> list[str]:
    """Trasforma gli effetti di un oggetto in frasi (es. {"danno": 1} -> ["Danno +1"]).

    La cura che accompagna i cuori massimi non si ripete: "Cuori massimi +2" basta.
    """
    righe = []
    for stat, valore in effetti.items():
        if stat == "vita" and "vita_max" in effetti:
            continue
        frase = f"{NOMI_STATISTICHE.get(stat, stat)} {valore:+g}"
        if stat == "cadenza":
            frase += " s (" + ("spari piu' spesso" if valore < 0 else "spari meno spesso") + ")"
        righe.append(frase)
    return righe


class Compendio:
    """Schede su oggetti, sinergie e nemici; cio' che non e' ancora stato scoperto resta "???".

    Frecce sinistra/destra cambiano scheda, su/giu' scelgono la voce.
    """

    SCHEDE = ("OGGETTI", "SINERGIE", "BESTIARIO")
    RIGHE_VISIBILI = 11

    def __init__(self, scoperte: dict[str, set[str]]) -> None:
        """Crea il compendio.

        Args:
            scoperte (dict[str, set[str]]): chiavi scoperte per tipo ("oggetto",
                "sinergia", "nemico"), come le restituisce salvataggio.get_scoperte.
        """
        self.scoperte = scoperte
        self.scheda = 0
        self.indice = 0
        self.voci = {"OGGETTI": list(OGGETTI), "SINERGIE": list(SINERGIE),
                     "BESTIARIO": TIPI_COMUNI + [k for k in DATI_NEMICI if k.startswith("boss")]}

    def _tipo(self) -> str:
        """Tipo di scoperta della scheda aperta."""
        return ("oggetto", "sinergia", "nemico")[self.scheda]

    def _chiavi(self) -> list[str]:
        """Voci della scheda aperta."""
        return self.voci[self.SCHEDE[self.scheda]]

    def scoperta(self, chiave: str) -> bool:
        """True se la voce della scheda aperta e' gia' stata scoperta."""
        return chiave in self.scoperte.get(self._tipo(), set())

    def gestisci_evento(self, evento: pygame.event.Event) -> None:
        """Cambia scheda (sinistra/destra) o voce (su/giu')."""
        if evento.type != pygame.KEYDOWN:
            return
        if evento.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d):
            passo = -1 if evento.key in (pygame.K_LEFT, pygame.K_a) else 1
            self.scheda = (self.scheda + passo) % len(self.SCHEDE)
            self.indice = 0
            audio.suona("menu")
        elif evento.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_s):
            passo = -1 if evento.key in (pygame.K_UP, pygame.K_w) else 1
            self.indice = (self.indice + passo) % len(self._chiavi())
            audio.suona("menu")

    def nome(self, chiave: str) -> str:
        """Nome della voce, oppure "???" se non e' ancora stata scoperta."""
        if not self.scoperta(chiave):
            return "???"
        dati = (OGGETTI, SINERGIE, DATI_NEMICI)[self.scheda][chiave]
        return dati["nome"]

    def dettagli(self, chiave: str) -> list[tuple[str, tuple[int, int, int]]]:
        """Righe (testo, colore) della scheda di dettaglio della voce scelta."""
        tipo = self._tipo()
        if not self.scoperta(chiave):
            come = {"oggetto": "Raccoglilo in una partita per scoprirlo.",
                    "sinergia": "Possiedi insieme gli oggetti giusti per scoprirla.",
                    "nemico": "Sconfiggilo almeno una volta per scoprirlo."}[tipo]
            righe = [(come, grafica.SPENTO)]
            if tipo == "sinergia":                 # indizio: gli oggetti gia' noti
                nomi = [OGGETTI[k]["nome"] if k in self.scoperte.get("oggetto", set()) else "???"
                        for k in SINERGIE[chiave]["richiede"]]
                righe.append(("Richiede: " + " + ".join(nomi), grafica.OSSO))
            return righe
        if tipo == "oggetto":
            return [(r, grafica.OSSO) for r in descrivi_effetti(OGGETTI[chiave]["effetti"])]
        if tipo == "sinergia":
            dati = SINERGIE[chiave]
            nomi = " + ".join(OGGETTI[k]["nome"] for k in dati["richiede"])
            return ([("Richiede: " + nomi, grafica.SPENTO), ("Bonus in piu':", grafica.ORO)]
                    + [(r, grafica.OSSO) for r in descrivi_effetti(dati["effetti"])])
        d = DATI_NEMICI[chiave]
        righe = [(r, grafica.OSSO) for r in a_capo(d["descrizione"], 44)]
        vita = f"Vita {d['vita']}" + ("" if "proiettili" in d else " al piano 1, poi cresce")
        righe.append((f"{vita}   Velocita' {d['velocita']}", grafica.SPENTO))
        if "proiettili" in d:
            righe.append((f"Raffiche da {d['proiettili']} colpi ogni {d['intervallo']:g} s",
                          grafica.SPENTO))
        return righe

    def draw(self, schermo: pygame.Surface) -> None:
        """Disegna schede, elenco delle voci e dettaglio di quella scelta."""
        titolo(schermo, "COMPENDIO", (640, 64), 60)
        for i, nome in enumerate(self.SCHEDE):
            testo(schermo, nome, (390 + i * 250, 130), 34,
                  grafica.ORO if i == self.scheda else grafica.SPENTO, True)
        chiavi = self._chiavi()
        noti = sum(self.scoperta(k) for k in chiavi)
        testo(schermo, f"Scoperti {noti}/{len(chiavi)}", (640, 168), 26, grafica.SPENTO, True)
        inizio = min(max(0, self.indice - self.RIGHE_VISIBILI // 2),
                     max(0, len(chiavi) - self.RIGHE_VISIBILI))
        for riga, chiave in enumerate(chiavi[inizio:inizio + self.RIGHE_VISIBILI]):
            sel = inizio + riga == self.indice
            colore = grafica.OSSO if sel else grafica.SPENTO
            testo(schermo, ("> " if sel else "  ") + self.nome(chiave), (110, 210 + riga * 38), 30,
                  colore)
        riquadro = pygame.Rect(560, 205, 620, 420)
        pygame.draw.rect(schermo, (28, 25, 34), riquadro)
        pygame.draw.rect(schermo, (60, 56, 70), riquadro, 2)
        chiave = chiavi[self.indice]
        nota = self.scoperta(chiave)
        self._disegna_icona(schermo, chiave, nota, (riquadro.left + 70, riquadro.top + 70))
        testo(schermo, self.nome(chiave), (riquadro.left + 140, riquadro.top + 50), 40,
              grafica.ORO if nota else grafica.SPENTO)
        for i, (riga, colore) in enumerate(self.dettagli(chiave)):
            testo(schermo, riga, (riquadro.left + 30, riquadro.top + 150 + i * 34), 28, colore)
        testo(schermo, "Frecce per scegliere - Esc per tornare", (640, 680), 28,
              grafica.SPENTO, True)

    def _disegna_icona(self, schermo: pygame.Surface, chiave: str, nota: bool,
                       centro: tuple[int, int]) -> None:
        """Icona della voce: lo sprite del nemico o un oggetto del colore del suo effetto."""
        buio = (26, 24, 32)
        if self.SCHEDE[self.scheda] == "BESTIARIO":
            d = DATI_NEMICI[chiave]
            nome_sprite = d.get("sprite", "boss")
            tinta = (d["colore"] if nome_sprite == "boss" else None) if nota else buio
            img = grafica.sprite(nome_sprite, 4 if nome_sprite == "boss" else 6, tinta)
            schermo.blit(img, img.get_rect(center=centro))
            return
        if self.SCHEDE[self.scheda] == "OGGETTI":
            effetto = next(iter(OGGETTI[chiave]["effetti"]))
            tinta = COLORI_EFFETTO[effetto] if nota else buio
        else:
            tinta = grafica.ORO if nota else buio
        r = pygame.Rect(0, 0, 44, 44)
        r.center = centro
        grafica.disegna_raccoglibile(schermo, "passivo", r, tinta)


class Aiuto:
    """Schermata di aiuto/tutorial con controlli e meccaniche di gioco."""

    PAGINE = [
        ("CONTROLLI", [
            "WASD / Frecce direzionali: Muovi il personaggio",
            "Frecce (SU/GIU/SX/DX): Sparo nella direzione",
            "SPAZIO: Abilità del personaggio (vedi sotto)",
            "M: Attiva/disattiva audio",
            "ESC: Pausa / Torna al menu",
            "INVIO: Conferma nei menu",
        ]),
        ("PERSONAGGI E ABILITÀ", [
            "Viandante (sempre): Scatto - Balzo rapido che attraversa nemici e colpi",
            "Predone (piano 2): Ventaglio di lame - 8 colpi in tutte le direzioni",
            "Templare (1 vittoria): Scudo sacro - Intoccabile 1s, spazza colpi vicini",
            "Occultista (3 vittorie): Onda arcana - Ferisce nemici vicini e cancella colpi",
            "",
            "Maestria: Vinci 2 volte con un personaggio per sbloccare un bonus permanente",
        ]),
        ("MECCANICHE", [
            "Sconfiggi tutti i nemici per aprire le porte",
            "Raccogli oggetti (passivi) per potenziarti",
            "Combina certi oggetti per attivare SINERGIE bonus",
            "Monete: comprano cuori e oggetti nei negozi (1 per piano)",
            "Cuori: curano 1 vita (max = cuori massimi)",
            "Boss: ha barra vita in alto; sotto 50% vita entra in FURIA",
            "Botola: appare nel boss sconfitto; ci scendi per il piano successivo",
            "3 piani totali: vinci sconfiggendo il boss del 3° piano",
        ]),
        ("OGGETTI PRINCIPALI", [
            "Stivali veloci: +Velocità",
            "Lente d'ingrandimento: +Gittata",
            "Amuleto di forza: +Danno",
            "Caffè forte: -Tempo tra colpi (spara più veloce)",
            "Cuore extra: +2 Cuori massimi + cura",
            "Sangue antico: +Danno +1 Cuore max + cura",
            "Scarpe di fiamma: +Velocità -Tempo tra colpi",
            "Occhio di falco: +Gittata +Velocità proiettili",
            "Cannone pesante: +2 Danno +Tempo tra colpi",
            "Armatura antica: +2 Cuori max + cura -Velocità",
            "Reliquia sacra: +Tutto (piccolo)",
            "Clessidra incrinata: -Tempo tra colpi +Vel. proiettili",
            "Pietra affilata: +Danno -Gittata",
            "Piuma di corvo: +Velocità +Vel. proiettili",
            "Elmo di ferro: +1 Cuore max + cura +Gittata",
        ]),
    ]

    def __init__(self) -> None:
        """Crea la schermata di aiuto."""
        self.pagina = 0

    def gestisci_evento(self, evento: pygame.event.Event) -> bool:
        """Gestisce input: frecce SX/DX per cambiare pagina, ESC/INVIO per chiudere.

        Returns:
            bool: True se l'aiuto deve chiudersi.
        """
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_LEFT, pygame.K_a):
                self.pagina = (self.pagina - 1) % len(self.PAGINE)
                audio.suona("menu")
            elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                self.pagina = (self.pagina + 1) % len(self.PAGINE)
                audio.suona("menu")
            elif evento.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                return True
        return False

    def draw(self, schermo: pygame.Surface) -> None:
        """Disegna la pagina corrente dell'aiuto."""
        titolo(schermo, "AIUTO / TUTORIAL", (640, 50), 56)
        # Indicatori pagina
        for i, (tit, _) in enumerate(self.PAGINE):
            col = grafica.ORO if i == self.pagina else grafica.SPENTO
            testo(schermo, tit, (150 + i * 220, 110), 24, col, True)
        pygame.draw.line(schermo, (60, 56, 70), (100, 140), (1180, 140), 2)
        # Contenuto
        _, righe = self.PAGINE[self.pagina]
        for i, riga in enumerate(righe):
            if riga == "":
                continue
            colore = grafica.OSSO
            if riga.startswith("Viandante") or riga.startswith("Predone") or \
               riga.startswith("Templare") or riga.startswith("Occultista") or \
               riga.startswith("Maestria"):
                colore = grafica.ORO
            testo(schermo, riga, (120, 170 + i * 32), 26, colore)
        testo(schermo, f"Pagina {self.pagina + 1}/{len(self.PAGINE)}", (640, 620), 24, grafica.SPENTO, True)
        testo(schermo, "<- / -> per cambiare pagina  |  ESC/INVIO per chiudere", (640, 660), 24, grafica.SPENTO, True)
