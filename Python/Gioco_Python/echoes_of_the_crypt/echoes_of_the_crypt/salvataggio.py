"""Salvataggio di statistiche e partita (SQLite) nella cartella dati dell'utente.
API identica alla versione JSON per backward compatibility."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from database import Database, cartella_dati

DEFAULT: dict[str, int | float] = {
    "partite": 0, "vittorie": 0, "record_nemici": 0,
    "miglior_tempo": 0.0, "piano_record": 0}
CAMPI_PARTITA = ("piano", "seed", "tempo", "giocatore")

# Profile ID default (inizializzato al primo uso)
_default_profile_id: int | None = None
_db: Database | None = None


def _get_db() -> Database:
    """Singleton Database inizializzato al primo uso."""
    global _db
    if _db is None:
        _db = Database()
    return _db


def _get_profile_id() -> int:
    """Ottiene il profile ID default: 'Giocatore1' o primo profilo esistente."""
    global _default_profile_id
    if _default_profile_id is None:
        db = _get_db()
        # Prova a ottenere il profilo più recente, altrimenti crea "Giocatore1"
        profili = db.get_profili()
        if profili:
            _default_profile_id = profili[0]["id"]
        else:
            _default_profile_id = db.crea_profilo("Giocatore1") or 1
    return _default_profile_id


def _set_profile_id(profile_id: int) -> None:
    """Imposta il profile ID manualmente (per cambio profilo)."""
    global _default_profile_id
    _default_profile_id = profile_id


def _migra_da_json_se_necessario() -> None:
    """Backward compatibility: se migrazione non fatta, leggi JSON e migra."""
    db = _get_db()
    # Il Database.__init__ chiama già _migra_da_json_se_vuoto()
    # Ma se l'utente ha file JSON e DB vuoto, forziamo la migrazione
    db._migra_da_json_se_vuoto()


def carica() -> dict:
    """Carica le statistiche del profilo corrente (default se assenti)."""
    _migra_da_json_se_necessario()
    db = _get_db()
    stats = db.load_stats(_get_profile_id())
    return {**DEFAULT, **stats}


def registra_partita(dati: dict, nemici: int, tempo: float,
                     vittoria: bool, piano: int = 1,
                     oggetti: list[str] | None = None,
                     personaggio: str | None = None,
                     seed_partita: int | None = None) -> dict:
    """Aggiorna le statistiche con l'esito di una partita e le salva.
    Aggiunge anche la run allo storico. Se vittoria, cancella il checkpoint (permadeath).

    Args:
        dati (dict): statistiche correnti del profilo.
        nemici (int): nemici sconfitti nella partita.
        tempo (float): durata della partita in secondi.
        vittoria (bool): True se la partita e' stata vinta.
        piano (int): piano raggiunto.
        oggetti (list[str] | None): nomi degli oggetti raccolti, salvati nello storico.
        personaggio (str | None): nome del personaggio usato, salvato nello storico.
        seed_partita (int | None): seed della partita, salvato nello storico.

    Returns:
        dict: statistiche aggiornate.
    """
    _migra_da_json_se_necessario()
    db = _get_db()
    profile_id = _get_profile_id()

    # Aggiorna stats globali
    dati["partite"] += 1
    dati["record_nemici"] = max(dati["record_nemici"], nemici)
    dati["piano_record"] = max(dati["piano_record"], piano)
    if vittoria:
        dati["vittorie"] += 1
        if dati["miglior_tempo"] == 0 or tempo < dati["miglior_tempo"]:
            dati["miglior_tempo"] = round(tempo, 1)

    db.save_stats(profile_id, dati)

    # Registra run nello storico
    db.add_run(profile_id, {
        "piano": piano,
        "nemici": nemici,
        "tempo": tempo,
        "vittoria": vittoria,
        "oggetti": list(oggetti or []),
        "personaggio": personaggio,
        "seed_partita": seed_partita,
    })

    # Permadeath: cancella checkpoint se partita finita (vittoria o sconfitta)
    if vittoria:
        db.delete_checkpoint(profile_id)

    return dati


def salva_partita(stato: dict) -> None:
    """Salva il checkpoint (inizio del piano corrente) per 'Continua'."""
    _migra_da_json_se_necessario()
    _get_db().save_checkpoint(_get_profile_id(), stato)


def carica_partita() -> dict | None:
    """Carica il checkpoint; None se manca o è incompleto."""
    _migra_da_json_se_necessario()
    d = _get_db().load_checkpoint(_get_profile_id())
    if d and all(c in d for c in CAMPI_PARTITA):
        return d
    return None


def esiste_partita() -> bool:
    """True se c'è una partita da continuare per il profilo corrente."""
    _migra_da_json_se_necessario()
    return _get_db().load_checkpoint(_get_profile_id()) is not None


def cancella_partita() -> None:
    """Elimina il checkpoint (permadeath: dopo sconfitta o vittoria)."""
    _migra_da_json_se_necessario()
    _get_db().delete_checkpoint(_get_profile_id())


# ========== NUOVE FUNZIONI PER PROFILI MULTIPLI ==========

def get_profili() -> list[dict[str, Any]]:
    """Lista tutti i profili con stats riepilogative."""
    _migra_da_json_se_necessario()
    return _get_db().get_profili()


def crea_profilo(nome: str) -> int | None:
    """Crea nuovo profilo. Ritorna id o None se nome duplicato."""
    _migra_da_json_se_necessario()
    return _get_db().crea_profilo(nome)


def elimina_profilo(profile_id: int) -> bool:
    """Elimina profilo e tutti i suoi dati."""
    _migra_da_json_se_necessario()
    return _get_db().elimina_profilo(profile_id)


def seleziona_profilo(profile_id: int) -> None:
    """Imposta il profilo attivo per le successive operazioni."""
    _set_profile_id(profile_id)


def get_profilo_corrente() -> dict | None:
    """Info profilo attualmente selezionato."""
    _migra_da_json_se_necessario()
    return _get_db().get_profilo(_get_profile_id())


def get_leaderboard(limit: int = 10) -> list[dict]:
    """Top tempi vittorie (globale)."""
    _migra_da_json_se_necessario()
    return _get_db().get_leaderboard(limit)


def get_vittorie_per_personaggio() -> dict[str, int]:
    """Vittorie del profilo corrente per personaggio (nome del personaggio -> vittorie)."""
    _migra_da_json_se_necessario()
    return _get_db().vittorie_per_personaggio(_get_profile_id())


def registra_scoperte(tipo: str, chiavi) -> None:
    """Segna nel profilo corrente oggetti, sinergie o nemici incontrati (per il Compendio)."""
    chiavi = list(chiavi)
    if chiavi:
        _get_db().aggiungi_scoperte(_get_profile_id(), tipo, chiavi)


def get_scoperte() -> dict[str, set[str]]:
    """Scoperte del profilo corrente (tipo -> chiavi).

    Gli oggetti raccolti nelle partite giocate prima che esistesse il Compendio
    si ricavano dallo storico, dove sono salvati per nome.
    """
    _migra_da_json_se_necessario()
    from oggetti import OGGETTI
    scoperte = _get_db().get_scoperte(_get_profile_id())
    per_nome = {v["nome"]: k for k, v in OGGETTI.items()}
    for partita in get_storico(limit=10**6):
        for nome in json.loads(partita["oggetti_raccolti"] or "[]"):
            if nome in per_nome:
                scoperte.setdefault("oggetto", set()).add(per_nome[nome])
    return scoperte


def get_storico(profile_id: int | None = None, limit: int = 50) -> list[dict]:
    """Storico partite per profilo (default: profilo corrente)."""
    _migra_da_json_se_necessario()
    pid = profile_id if profile_id is not None else _get_profile_id()
    return _get_db().get_history(pid, limit)


def get_statistiche_globali() -> dict:
    """Statistiche aggregate su tutti i profili."""
    _migra_da_json_se_necessario()
    return _get_db().get_global_stats()
