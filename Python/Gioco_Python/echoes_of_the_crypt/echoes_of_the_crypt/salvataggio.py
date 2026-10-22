"""Salvataggio di statistiche e partita (JSON) nella cartella dati dell'utente."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

DEFAULT: dict[str, int | float] = {
    "partite": 0, "vittorie": 0, "record_nemici": 0,
    "miglior_tempo": 0.0, "piano_record": 0}
CAMPI_PARTITA = ("piano", "seed", "tempo", "giocatore")


def cartella_dati() -> Path:
    """Cartella dove salvare i dati, fuori dal codice (sopravvive agli aggiornamenti).

    Returns:
        Path: %APPDATA%/echoes_of_the_crypt su Windows,
        ~/.local/share/echoes_of_the_crypt su Linux.
    """
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home()))
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    cartella = base / "echoes_of_the_crypt"
    cartella.mkdir(parents=True, exist_ok=True)
    return cartella


def _leggi(nome: str) -> dict | None:
    """Legge un file JSON; None se manca o e' corrotto."""
    try:
        with open(cartella_dati() / nome, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _scrivi(nome: str, dati: dict) -> None:
    """Scrive un file JSON (gli errori di scrittura non fermano il gioco)."""
    try:
        with open(cartella_dati() / nome, "w", encoding="utf-8") as f:
            json.dump(dati, f, indent=2)
    except OSError as errore:
        print(f"Impossibile salvare {nome}: {errore}")


def carica() -> dict:
    """Carica le statistiche (default se assenti).

    Returns:
        dict: statistiche salvate.
    """
    return {**DEFAULT, **(_leggi("salvataggio.json") or {})}


def registra_partita(dati: dict, nemici: int, tempo: float,
                     vittoria: bool, piano: int = 1) -> dict:
    """Aggiorna le statistiche con l'esito di una partita e le salva.

    Args:
        dati (dict): statistiche correnti.
        nemici (int): nemici sconfitti.
        tempo (float): durata in secondi.
        vittoria (bool): True se l'ultimo boss e' stato sconfitto.
        piano (int): piano raggiunto.

    Returns:
        dict: statistiche aggiornate.
    """
    dati["partite"] += 1
    dati["record_nemici"] = max(dati["record_nemici"], nemici)
    dati["piano_record"] = max(dati["piano_record"], piano)
    if vittoria:
        dati["vittorie"] += 1
        if dati["miglior_tempo"] == 0 or tempo < dati["miglior_tempo"]:
            dati["miglior_tempo"] = round(tempo, 1)
    _scrivi("salvataggio.json", dati)
    return dati


def salva_partita(stato: dict) -> None:
    """Salva il checkpoint (inizio del piano corrente) per 'Continua'."""
    _scrivi("partita.json", stato)


def carica_partita() -> dict | None:
    """Carica il checkpoint; None se manca o e' incompleto."""
    d = _leggi("partita.json")
    return d if d and all(c in d for c in CAMPI_PARTITA) else None


def esiste_partita() -> bool:
    """True se c'e' una partita da continuare."""
    return carica_partita() is not None


def cancella_partita() -> None:
    """Elimina il checkpoint (permadeath: dopo sconfitta o vittoria)."""
    try:
        (cartella_dati() / "partita.json").unlink(missing_ok=True)
    except OSError:
        pass
