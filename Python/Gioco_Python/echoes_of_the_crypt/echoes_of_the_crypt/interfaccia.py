"""Menu, caselle di testo, tabelle, HUD e minimappa."""
from __future__ import annotations

import pygame

import audio
import grafica
from dungeon import DIREZIONI, Dungeon, Stanza
from giocatore import (ABILITA, MAESTRIA_VITTORIE, PERSONAGGI, ha_maestria, sbloccato,
                       testo_sblocco)
from nemici import DATI_NEMICI, TIPI_COMUNI
from oggetti import COLORI_EFFETTO, OGGETTI, SINERGIE, PREZZI


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

    def _voci_categoria(self) -> list[tuple[str, any]]:
        """Restituisce le voci (label, valore) per la categoria corrente."""
        if self.categoria == 0:  # Audio
            return [
                ("Volume musica", self.audio_musica, "slider", (0, 100)),
                ("Volume effetti", self.audio_effetti, "slider", (0, 100)),
            ]
        elif self.categoria == 1:  # Video
            return [
                ("Schermo intero", self.schermo_intero, "toggle", None),
                ("Riduzione effetti visivi", self.riduzione_effetti, "toggle", None),
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
                ("Modalità daltonici", self.daltonici, "toggle", None),
                ("Testo grande", self.testo_grande, "toggle", None),
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
                # Non permettere ESC per rimappare (serve per uscire)
                if evento.key == pygame.K_ESCAPE:
                    self._in_attesa_tasto = None
                    return False
                # Evita conflitti
                for k, v in self.tasti.items():
                    if v == evento.key and k != self._in_attesa_tasto:
                        return False
                self.tasti[self._in_attesa_tasto] = evento.key
                self._in_attesa_tasto = None
                self.salva_impostazioni()
            return False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.salva_impostazioni()
                return True  # chiudi
            # Categorie: solo FRECCE SX/DX
            if evento.key == pygame.K_LEFT:
                self.categoria = (self.categoria - 1) % len(self.CATEGORIE)
                self.indice = 0
                audio.suona("menu")
            elif evento.key == pygame.K_RIGHT:
                self.categoria = (self.categoria + 1) % len(self.CATEGORIE)
                self.indice = 0
                audio.suona("menu")
            # Voci: solo FRECCE SU/GIÙ
            elif evento.key == pygame.K_UP:
                self.indice = (self.indice - 1) % len(self._voci_categoria())
                audio.suona("menu")
            elif evento.key == pygame.K_DOWN:
                self.indice = (self.indice + 1) % len(self._voci_categoria())
                audio.suona("menu")
            # Slider e toggle: FRECCE SX/DX (quando su una voce slider/toggle)
            elif evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
                voci = self._voci_categoria()
                if self.indice < len(voci):
                    label, key, tipo, extra = voci[self.indice]
                    if tipo == "slider":
                        min_v, max_v = extra
                        step = 5
                        if evento.key == pygame.K_RIGHT:
                            if key == "audio_musica":
                                self.audio_musica = min(max_v, self.audio_musica + step)
                                audio.imposta_volume_musica(self.audio_musica / 100)
                            elif key == "audio_effetti":
                                self.audio_effetti = min(max_v, self.audio_effetti + step)
                                audio.imposta_volume_effetti(self.audio_effetti / 100)
                        else:  # K_LEFT
                            if key == "audio_musica":
                                self.audio_musica = max(min_v, self.audio_musica - step)
                                audio.imposta_volume_musica(self.audio_musica / 100)
                            elif key == "audio_effetti":
                                self.audio_effetti = max(min_v, self.audio_effetti - step)
                                audio.imposta_volume_effetti(self.audio_effetti / 100)
                        self.salva_impostazioni()
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
            elif evento.key == pygame.K_RETURN:
                voci = self._voci_categoria()
                if self.indice < len(voci):
                    label, key, tipo, extra = voci[self.indice]
                    if tipo == "key":
                        self._in_attesa_tasto = key
                    elif tipo == "toggle":  # INVIO anche per toggle
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
                pct = (key == "audio_musica" and self.audio_musica or self.audio_effetti - min_v) / (max_v - min_v)
                barra_w = 300
                pygame.draw.rect(schermo, (44, 42, 54), (x_base + 250, y, barra_w, 16), border_radius=4)
                pygame.draw.rect(schermo, grafica.ORO, (x_base + 250, y, round(barra_w * pct), 16), border_radius=4)
                pygame.draw.rect(schermo, (90, 90, 105), (x_base + 250, y, barra_w, 16), 2, border_radius=4)
                testo(schermo, f"{prefisso}{label}: {key == 'audio_musica' and self.audio_musica or self.audio_effetti}%", (x_base, y), 28, colore)
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
            testo(schermo, "FRECCE SX/DX: Cambia categoria  |  FRECCE SU/GIÙ: Sceglie voce  |  FRECCE SX/DX: Slider/Toggle  |  INVIO: Toggle/Remap  |  ESC: Torna",
                  (640, 680), 24, grafica.SPENTO, True)


class Hud:
    """Indicatori a schermo, minimappa e inventario."""

    # Colore sulla minimappa delle stanze speciali gia' visitate.
    COLORI_MAPPA = {"boss": (230, 200, 60), "tesoro": (80, 230, 160), "negozio": (90, 170, 240)}

    @staticmethod
    def draw(schermo: pygame.Surface, g, dungeon: Dungeon,
             corrente: Stanza, tempo: float, piano: int = 1, messaggio: str = "") -> None:
        """Disegna HUD completo: icone statistiche sx, minimappa dx, inventario sotto minimappa, feedback pickup."""
        # Inizializza attributi per feedback pickup se non esistono
        if not hasattr(g, "_pickup_feedback"):
            g._pickup_feedback = []  # lista di (testo, timer, colore)

        # --- PANNELLO SINISTRO: Statistiche come ICONA + VALORE ---
        pannello_x = 16
        pannello_y = 16
        spacing = 28
        riga = 0

        # Cuori
        for i in range(g.vita_max):
            schermo.blit(grafica.sprite("cuore" if i < g.vita else "cuore_vuoto", 3),
                         (pannello_x + i * 28, pannello_y))
        riga += 2

        # Monete
        schermo.blit(grafica.sprite("moneta", 2), (pannello_x, pannello_y + riga * spacing))
        testo(schermo, f"x {g.monete}", (pannello_x + 24, pannello_y + riga * spacing - 1), 24)
        riga += 1

        # Statistiche: icona "passivo" colorata + valore numerico (niente barre)
        stats = [
            ("Danno", g.danno, grafica.SANGUE),
            ("Velocità", round(g.velocita), (100, 230, 170)),
            ("Gittata", round(g.gittata), (90, 170, 240)),
            ("Cadenza", round(g.cadenza * 100) / 100, (230, 180, 90)),
            ("Vel. colpi", round(g.vel_proiettile), (200, 150, 255)),
        ]
        for nome, val, colore in stats:
            # Icona passivo colorata
            r = pygame.Rect(0, 0, 20, 20)
            r.topleft = (pannello_x, pannello_y + riga * spacing)
            grafica.disegna_raccoglibile(schermo, "passivo", r, colore)
            # Valore numerico a destra
            testo(schermo, f"{nome}: {val}", (pannello_x + 28, pannello_y + riga * spacing - 1), 18, colore)
            riga += 1

        # Tempo e piano
        testo(schermo, f"Tempo {int(tempo)}s", (pannello_x, pannello_y + riga * spacing), 22)
        riga += 1
        testo(schermo, f"Piano {piano}", (pannello_x, pannello_y + riga * spacing), 22, grafica.ORO)
        riga += 1.5

        # Messaggio centrale (es. boss, pickup)
        if messaggio:
            testo(schermo, messaggio, (640, 60), 36, grafica.ORO, True)

        # Sinergie attive
        for i, nome in enumerate(g.sinergie[-4:]):
            testo(schermo, f"+ {nome}", (pannello_x, pannello_y + riga * spacing + i * 22), 20, grafica.ORO)

        # Abilità personaggio: barra ricarica
        pronta = g.ricarica_abilita == 0
        testo(schermo, f"SPAZIO  {g.abilita['nome']}", (pannello_x, 636), 22,
              grafica.ORO if pronta else grafica.SPENTO)
        pygame.draw.rect(schermo, (44, 42, 54), (pannello_x, 660, 180, 8))
        pieno = 1 - g.ricarica_abilita / g.tempo_ricarica
        pygame.draw.rect(schermo, grafica.ORO if pronta else grafica.SPENTO,
                         (pannello_x, 660, round(180 * pieno), 8))
        if g.maestria:
            testo(schermo, "Maestria attiva", (pannello_x, 676), 20, grafica.ORO)

        # --- FEEDBACK PICKUP OGGETTI (animato, svanisce) ---
        # Aggiorna timer e rimuovi scaduti
        g._pickup_feedback = [(t, timer - 1/60, c) for t, timer, c in g._pickup_feedback if timer > 0]
        for i, (txt, timer, col) in enumerate(g._pickup_feedback):
            alpha = int(255 * min(1.0, timer / 2.0))  # fade out negli ultimi 2s
            y_pos = 180 + i * 26
            # Sfondo semitrasparente
            surf = pygame.Surface((260, 24), pygame.SRCALPHA)
            surf.fill((20, 18, 26, alpha))
            schermo.blit(surf, (pannello_x - 6, y_pos - 2))
            # Testo con fade
            font = grafica.carattere(22)
            img = font.render(txt, True, col)
            img.set_alpha(alpha)
            schermo.blit(img, (pannello_x, y_pos))

        # --- MINIMAPPA (destra) ---
        Hud._minimappa(schermo, dungeon, corrente)

        # --- INVENTARIO SOTTO MINIMAPPA ---
        Hud._disegna_inventario(schermo, g)

    @staticmethod
    def _disegna_barra_stat(schermo: pygame.Surface, x: int, y: int, w: int, h: int,
                            nome: str, valore: float, massimo: float, colore: tuple,
                            inverso: bool = False) -> None:
        """Disegna una statistica come label + barra + valore numerico."""
        # Label
        testo(schermo, nome, (x, y - 2), 18, grafica.OSSO)
        # Barra sfondo
        pygame.draw.rect(schermo, (44, 42, 54), (x, y + 16, w, h), border_radius=3)
        # Calcola riempimento
        if inverso:
            # Per cadenza: minore è meglio, barra piena quando valore è basso
            pct = max(0.0, min(1.0, 1.0 - valore / massimo))
        else:
            pct = max(0.0, min(1.0, valore / massimo))
        fill_w = round(w * pct)
        if fill_w > 0:
            pygame.draw.rect(schermo, colore, (x, y + 16, fill_w, h), border_radius=3)
        # Valore numerico a destra
        testo(schermo, str(valore), (x + w + 6, y - 2), 18, colore)

    @staticmethod
    def _minimappa(schermo: pygame.Surface, dungeon: Dungeon, corrente: Stanza) -> None:
        """Mostra le stanze visitate e le loro vicine; la corrente e' bianca.
        Le stanze speciali (boss, tesoro, negozio) sono riconoscibili anche se non visitate.
        """
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
        """Disegna l'inventario completo (tutti gli oggetti passivi) sotto la minimappa."""
        ox, oy = 1080, 380
        larghezza = 190
        riga_h = 24
        max_righe = 12

        # Reverse map: display name -> internal key
        nome_a_chiave = {v["nome"]: k for k, v in OGGETTI.items()}

        # Titolo
        testo(schermo, "INVENTARIO", (ox + larghezza // 2, oy - 24), 22, grafica.ORO, True)
        pygame.draw.rect(schermo, (28, 25, 34), (ox - 8, oy - 8, larghezza + 16, max_righe * riga_h + 16))
        pygame.draw.rect(schermo, (60, 56, 70), (ox - 8, oy - 8, larghezza + 16, max_righe * riga_h + 16), 2)

        if not g.oggetti:
            testo(schermo, "Vuoto", (ox + larghezza // 2, oy + 40), 20, grafica.SPENTO, True)
            return

        # Mostra tutti gli oggetti (scroll se troppi)
        inizio = max(0, len(g.oggetti) - max_righe)
        for i, nome in enumerate(g.oggetti[inizio:]):
            chiave = nome_a_chiave.get(nome)
            if not chiave:
                continue
            dati = OGGETTI[chiave]
            y = oy + i * riga_h
            # Colore per effetto principale
            effetto = next(iter(dati["effetti"]))
            col = COLORI_EFFETTO.get(effetto, grafica.OSSO)
            # Icona
            r = pygame.Rect(0, 0, 20, 20)
            r.center = (ox + 14, y + 10)
            grafica.disegna_raccoglibile(schermo, "passivo", r, col)
            # Nome
            testo(schermo, dati["nome"], (ox + 30, y), 18, grafica.OSSO)

    @staticmethod
    def aggiungi_feedback_pickup(giocatore, chiave_oggetto: str) -> None:
        """Aggiunge un messaggio di feedback quando si raccoglie un oggetto passivo.

        Args:
            giocatore: istanza Giocatore
            chiave_oggetto (str): chiave dell'oggetto in OGGETTI
        """
        if not hasattr(giocatore, "_pickup_feedback"):
            giocatore._pickup_feedback = []
        dati = OGGETTI[chiave_oggetto]
        righe = descrivi_effetti(dati["effetti"])
        for r in righe:
            giocatore._pickup_feedback.append((f"{dati['nome']}: {r}", 3.0, COLORI_EFFETTO.get(next(iter(dati["effetti"])), grafica.ORO)))


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
