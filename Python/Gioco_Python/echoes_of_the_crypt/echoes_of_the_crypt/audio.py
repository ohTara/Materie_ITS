"""Effetti sonori e musica generati dal programma (nessun file audio esterno).

I suoni sono sintetizzati all'avvio a partire dai dizionari SUONI e MUSICA:
cosi' il gioco resta un insieme di soli file .py e non usa materiale di terzi.
Se la scheda audio non e' disponibile tutte le funzioni non fanno nulla.
"""
from __future__ import annotations

import math
import random
from array import array

import pygame

FREQUENZA = 22050          # campioni al secondo (mono, 16 bit)
AMPIEZZA = 32767           # valore massimo di un campione a 16 bit

# Ogni suono e' una lista di tratti: (onda, Hz iniziali, Hz finali, secondi, volume).
# La frequenza scivola da quella iniziale a quella finale; "pausa" e' silenzio.
SUONI: dict[str, list[tuple[str, float, float, float, float]]] = {
    "sparo":     [("quadra", 880, 440, 0.07, 0.25)],
    "colpo":     [("rumore", 0, 0, 0.05, 0.30)],
    "morte":     [("quadra", 300, 80, 0.18, 0.30)],
    "danno":     [("quadra", 200, 90, 0.25, 0.45)],
    "moneta":    [("sinusoide", 1320, 1320, 0.05, 0.35), ("sinusoide", 1760, 1760, 0.10, 0.35)],
    "cuore":     [("sinusoide", 660, 990, 0.16, 0.35)],
    "oggetto":   [("sinusoide", 523, 523, 0.08, 0.35), ("sinusoide", 659, 659, 0.08, 0.35),
                  ("sinusoide", 784, 784, 0.16, 0.35)],
    "acquisto":  [("sinusoide", 1320, 1320, 0.05, 0.35), ("sinusoide", 988, 988, 0.05, 0.35),
                  ("sinusoide", 1568, 1568, 0.14, 0.35)],
    "sinergia":  [("sinusoide", 523, 523, 0.07, 0.4), ("sinusoide", 659, 659, 0.07, 0.4),
                  ("sinusoide", 784, 784, 0.07, 0.4), ("sinusoide", 1047, 1047, 0.25, 0.4)],
    "abilita":   [("sinusoide", 300, 900, 0.14, 0.35)],
    "furia":     [("quadra", 140, 60, 0.45, 0.40), ("rumore", 0, 0, 0.15, 0.25)],
    "carica":    [("quadra", 180, 520, 0.16, 0.22)],
    "porte":     [("quadra", 220, 330, 0.12, 0.20)],
    "menu":      [("quadra", 660, 660, 0.03, 0.15)],
    "piano":     [("sinusoide", 392, 392, 0.12, 0.4), ("sinusoide", 523, 523, 0.12, 0.4),
                  ("sinusoide", 784, 784, 0.30, 0.4)],
    "vittoria":  [("sinusoide", 523, 523, 0.14, 0.4), ("sinusoide", 659, 659, 0.14, 0.4),
                  ("sinusoide", 784, 784, 0.14, 0.4), ("sinusoide", 1047, 1047, 0.45, 0.4)],
    "sconfitta": [("quadra", 330, 311, 0.22, 0.3), ("quadra", 262, 247, 0.22, 0.3),
                  ("quadra", 196, 98, 0.55, 0.3)],
}

# Musica di sottofondo: (Hz, secondi) per ogni nota; 0 Hz = pausa. Viene ripetuta.
MUSICA: list[tuple[float, float]] = [
    (110.0, 0.6), (164.8, 0.6), (220.0, 0.6), (261.6, 0.6), (220.0, 0.6), (164.8, 0.6),
    (98.0, 0.6), (146.8, 0.6), (196.0, 0.6), (246.9, 0.6), (196.0, 0.6), (146.8, 0.6),
    (87.3, 0.6), (130.8, 0.6), (174.6, 0.6), (220.0, 0.6), (174.6, 0.6), (130.8, 0.6),
    (82.4, 0.6), (123.5, 0.6), (164.8, 0.6), (207.7, 0.6), (164.8, 1.2),
]
VOLUME_MUSICA = 0.15     # volumi di partenza: bassi, si alza dal mixer del sistema
VOLUME_EFFETTI = 0.5

_suoni: dict[str, pygame.mixer.Sound] = {}
_musica: pygame.mixer.Sound | None = None
_muto = False


def tratto(onda: str, f_inizio: float, f_fine: float, durata: float,
           volume: float) -> array:
    """Sintetizza un tratto di suono che si spegne gradualmente.

    Args:
        onda (str): "sinusoide", "quadra", "rumore" o "pausa".
        f_inizio (float): frequenza iniziale in Hz.
        f_fine (float): frequenza finale in Hz (uguale a quella iniziale = nota fissa).
        durata (float): durata in secondi.
        volume (float): da 0 a 1.

    Returns:
        array: campioni interi a 16 bit.
    """
    n = int(FREQUENZA * durata)
    campioni = array("h", bytes(2 * n))
    if onda == "pausa" or n == 0:
        return campioni
    rng = random.Random(n)                 # rumore sempre uguale a parita' di durata
    attacco = min(n, int(FREQUENZA * 0.005)) or 1
    fase = 0.0
    for i in range(n):
        freq = f_inizio + (f_fine - f_inizio) * i / n
        fase += 2 * math.pi * freq / FREQUENZA
        if onda == "sinusoide":
            valore = math.sin(fase)
        elif onda == "quadra":
            valore = 1.0 if math.sin(fase) >= 0 else -1.0
        else:
            valore = rng.uniform(-1, 1)
        inviluppo = min(1.0, i / attacco) * (1 - i / n)     # niente "click" a inizio e fine
        campioni[i] = int(AMPIEZZA * volume * inviluppo * valore)
    return campioni


def sintetizza(tratti: list[tuple[str, float, float, float, float]]) -> array:
    """Unisce in sequenza i tratti che descrivono un suono (vedi SUONI)."""
    campioni = array("h")
    for t in tratti:
        campioni.extend(tratto(*t))
    return campioni


def sintetizza_musica(note: list[tuple[float, float]]) -> array:
    """Trasforma le note di MUSICA in campioni: ogni nota e' una sinusoide con la sua ottava."""
    campioni = array("h")
    for freq, durata in note:
        if freq == 0:
            campioni.extend(tratto("pausa", 0, 0, durata, 0))
            continue
        base = tratto("sinusoide", freq, freq, durata, 0.5)
        alta = tratto("sinusoide", freq * 2, freq * 2, durata, 0.2)
        campioni.extend(array("h", (a + b for a, b in zip(base, alta))))
    return campioni


def _crea_suono(campioni: array) -> pygame.mixer.Sound:
    """Crea un Sound adattando i campioni mono ai canali del mixer."""
    canali = pygame.mixer.get_init()[2]
    if canali > 1:
        campioni = array("h", (c for c in campioni for _ in range(canali)))
    return pygame.mixer.Sound(buffer=campioni.tobytes())


def inizializza() -> bool:
    """Apre il mixer e prepara effetti e musica.

    Returns:
        bool: False se l'audio non e' disponibile (il gioco prosegue in silenzio).
    """
    global _musica
    try:
        pygame.mixer.quit()
        pygame.mixer.init(FREQUENZA, -16, 1, 512, allowedchanges=0)
        _suoni.update({nome: _crea_suono(sintetizza(t)) for nome, t in SUONI.items()})
        for suono in _suoni.values():
            suono.set_volume(VOLUME_EFFETTI)
        _musica = _crea_suono(sintetizza_musica(MUSICA))
        _musica.set_volume(VOLUME_MUSICA)
    except pygame.error:
        _suoni.clear()
        _musica = None
        return False
    return True


def suona(nome: str) -> None:
    """Riproduce l'effetto indicato (chiave di SUONI); non fa nulla se muto o senza audio."""
    if not _muto and nome in _suoni:
        _suoni[nome].play()


def avvia_musica() -> None:
    """Fa partire la musica di sottofondo in ciclo continuo."""
    if _musica is not None and not _muto and _musica.get_num_channels() == 0:
        _musica.play(loops=-1)


def cambia_muto() -> bool:
    """Attiva o disattiva tutto l'audio.

    Returns:
        bool: True se ora l'audio e' disattivato.
    """
    global _muto
    _muto = not _muto
    if _muto:
        if pygame.mixer.get_init():
            pygame.mixer.stop()
    else:
        avvia_musica()
    return _muto


def e_muto() -> bool:
    """True se l'audio e' stato disattivato dal giocatore."""
    return _muto
