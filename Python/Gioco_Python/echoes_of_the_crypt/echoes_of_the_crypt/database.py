"""Database SQLite per Echoes of the Crypt: profili, statistiche, save game, storico."""
from __future__ import annotations

import json
import os
import sqlite3
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any


def cartella_dati() -> Path:
    """Cartella dati utente (stessa di salvataggio.py)."""
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home()))
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    cartella = base / "echoes_of_the_crypt"
    cartella.mkdir(parents=True, exist_ok=True)
    return cartella


SCHEMA_VERSION = 1


def _default_db_path() -> Path:
    """Percorso default del database (valutato al momento della chiamata)."""
    return cartella_dati() / "game.db"


SCHEMA_SQL = f"""
-- Schema v{SCHEMA_VERSION}
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    last_played TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS game_stats (
    profile_id INTEGER PRIMARY KEY,
    partite INTEGER NOT NULL DEFAULT 0,
    vittorie INTEGER NOT NULL DEFAULT 0,
    piano_record INTEGER NOT NULL DEFAULT 0,
    record_nemici INTEGER NOT NULL DEFAULT 0,
    miglior_tempo REAL NOT NULL DEFAULT 0.0,
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS save_games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL UNIQUE,
    piano INTEGER NOT NULL,
    seed INTEGER NOT NULL,
    tempo REAL NOT NULL,
    player_json TEXT NOT NULL,
    stanza_coord TEXT NOT NULL,
    stanze_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS run_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    piano_raggiunto INTEGER NOT NULL,
    nemici_uccisi INTEGER NOT NULL,
    tempo REAL NOT NULL,
    vittoria INTEGER NOT NULL,
    oggetti_raccolti TEXT NOT NULL,
    data TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);

-- Indici per query frequenti
CREATE INDEX IF NOT EXISTS idx_run_history_profile_data
    ON run_history(profile_id, data DESC);
CREATE INDEX IF NOT EXISTS idx_run_history_vittoria_tempo
    ON run_history(vittoria, tempo ASC);
CREATE INDEX IF NOT EXISTS idx_save_games_profile
    ON save_games(profile_id);

-- Trigger per updated_at automatico
CREATE TRIGGER IF NOT EXISTS trg_game_stats_updated
AFTER UPDATE ON game_stats
BEGIN
    UPDATE game_stats SET updated_at = datetime('now') WHERE profile_id = NEW.profile_id;
END;

CREATE TRIGGER IF NOT EXISTS trg_save_games_updated
AFTER UPDATE ON save_games
BEGIN
    UPDATE save_games SET updated_at = datetime('now') WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_profiles_last_played
AFTER UPDATE ON profiles
BEGIN
    UPDATE profiles SET last_played = datetime('now') WHERE id = NEW.id;
END;
"""


class Database:
    """Data Access Layer per SQLite."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or _default_db_path()
        self._conn: sqlite3.Connection | None = None
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(self.path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA foreign_keys = ON")
            self._conn.execute("PRAGMA journal_mode = WAL")
        return self._conn

    @contextmanager
    def _transaction(self):
        conn = self._get_conn()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    def _init_db(self) -> None:
        """Crea schema e migra da JSON se necessario."""
        with self._transaction() as conn:
            conn.executescript(SCHEMA_SQL)
            # Verifica versione schema
            cur = conn.execute("SELECT version FROM schema_version")
            row = cur.fetchone()
            if row is None:
                conn.execute("INSERT INTO schema_version (version) VALUES (?)", (SCHEMA_VERSION,))
            elif row[0] < SCHEMA_VERSION:
                # Future migrations would go here
                conn.execute("UPDATE schema_version SET version = ?", (SCHEMA_VERSION,))

        # Migrazione automatica da JSON se DB vuoto
        self._migra_da_json_se_vuoto()

    def _migra_da_json_se_vuoto(self) -> None:
        """Se non ci sono profili ma esiste salvataggio.json, migra i dati."""
        with self._transaction() as conn:
            cur = conn.execute("SELECT COUNT(*) FROM profiles")
            if cur.fetchone()[0] > 0:
                return  # DB già popolato

        # Cerca file JSON legacy
        json_stats = cartella_dati() / "salvataggio.json"
        json_save = cartella_dati() / "partita.json"
        if not json_stats.exists() and not json_save.exists():
            return  # Niente da migrare

        # Crea profilo default
        profile_id = self.crea_profilo("Giocatore1")
        if profile_id is None:
            return

        # Migra statistiche
        if json_stats.exists():
            try:
                with open(json_stats, "r", encoding="utf-8") as f:
                    stats = json.load(f)
                self.save_stats(profile_id, stats)
            except (json.JSONDecodeError, OSError):
                pass

        # Migra checkpoint
        if json_save.exists():
            try:
                with open(json_save, "r", encoding="utf-8") as f:
                    save_data = json.load(f)
                self.save_checkpoint(profile_id, save_data)
            except (json.JSONDecodeError, OSError):
                pass

        # Rinomina file JSON come backup (non cancella per sicurezza)
        try:
            if json_stats.exists():
                json_stats.rename(cartella_dati() / "salvataggio.json.bak")
            if json_save.exists():
                json_save.rename(cartella_dati() / "partita.json.bak")
        except OSError:
            pass

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    # ========== PROFILI ==========

    def get_profili(self) -> list[dict[str, Any]]:
        """Lista tutti i profili con stats riepilogative."""
        conn = self._get_conn()
        cur = conn.execute("""
            SELECT p.id, p.nome, p.created_at, p.last_played,
                   COALESCE(gs.partite, 0) as partite,
                   COALESCE(gs.vittorie, 0) as vittorie,
                   COALESCE(gs.piano_record, 0) as piano_record
            FROM profiles p
            LEFT JOIN game_stats gs ON p.id = gs.profile_id
            ORDER BY p.last_played DESC
        """)
        return [dict(row) for row in cur.fetchall()]

    def get_profilo(self, profile_id: int) -> dict[str, Any] | None:
        conn = self._get_conn()
        cur = conn.execute("SELECT * FROM profiles WHERE id = ?", (profile_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def get_profilo_by_nome(self, nome: str) -> dict[str, Any] | None:
        conn = self._get_conn()
        cur = conn.execute("SELECT * FROM profiles WHERE nome = ?", (nome,))
        row = cur.fetchone()
        return dict(row) if row else None

    def crea_profilo(self, nome: str) -> int | None:
        """Crea nuovo profilo con stats vuote. Ritorna id o None se nome duplicato."""
        try:
            with self._transaction() as conn:
                cur = conn.execute(
                    "INSERT INTO profiles (nome) VALUES (?)",
                    (nome,)
                )
                profile_id = cur.lastrowid
                conn.execute(
                    "INSERT INTO game_stats (profile_id) VALUES (?)",
                    (profile_id,)
                )
                return profile_id
        except sqlite3.IntegrityError:
            return None

    def elimina_profilo(self, profile_id: int) -> bool:
        with self._transaction() as conn:
            cur = conn.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
            return cur.rowcount > 0

    def get_or_create_default_profile(self) -> int:
        """Ottiene il profilo più recente o ne crea uno default."""
        profili = self.get_profili()
        if profili:
            return profili[0]["id"]
        return self.crea_profilo("Giocatore1") or 1

    # ========== STATISTICHE ==========

    def save_stats(self, profile_id: int, stats: dict) -> None:
        """Aggiorna statistiche globali (upsert)."""
        with self._transaction() as conn:
            conn.execute("""
                INSERT INTO game_stats (profile_id, partite, vittorie, piano_record, record_nemici, miglior_tempo)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(profile_id) DO UPDATE SET
                    partite = excluded.partite,
                    vittorie = excluded.vittorie,
                    piano_record = excluded.piano_record,
                    record_nemici = excluded.record_nemici,
                    miglior_tempo = excluded.miglior_tempo,
                    updated_at = datetime('now')
            """, (
                profile_id,
                stats.get("partite", 0),
                stats.get("vittorie", 0),
                stats.get("piano_record", 0),
                stats.get("record_nemici", 0),
                stats.get("miglior_tempo", 0.0),
            ))

    def load_stats(self, profile_id: int) -> dict:
        """Carica statistiche; default se assenti."""
        conn = self._get_conn()
        cur = conn.execute("SELECT * FROM game_stats WHERE profile_id = ?", (profile_id,))
        row = cur.fetchone()
        if row:
            return dict(row)
        return {
            "partite": 0, "vittorie": 0, "record_nemici": 0,
            "miglior_tempo": 0.0, "piano_record": 0
        }

    # ========== SAVE GAME (CHECKPOINT) ==========

    def save_checkpoint(self, profile_id: int, data: dict) -> None:
        """Salva/aggiorna checkpoint partita in corso."""
        with self._transaction() as conn:
            conn.execute("""
                INSERT INTO save_games (profile_id, piano, seed, tempo, player_json, stanza_coord, stanze_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(profile_id) DO UPDATE SET
                    piano = excluded.piano,
                    seed = excluded.seed,
                    tempo = excluded.tempo,
                    player_json = excluded.player_json,
                    stanza_coord = excluded.stanza_coord,
                    stanze_json = excluded.stanze_json,
                    updated_at = datetime('now')
            """, (
                profile_id,
                data.get("piano", 1),
                data.get("seed", 0),
                data.get("tempo", 0.0),
                json.dumps(data.get("giocatore", {})),
                json.dumps(data.get("stanza", [0, 0])),
                json.dumps(data.get("stanze", {})),
            ))

    def load_checkpoint(self, profile_id: int) -> dict | None:
        """Carica checkpoint; None se non esiste."""
        conn = self._get_conn()
        cur = conn.execute("SELECT * FROM save_games WHERE profile_id = ?", (profile_id,))
        row = cur.fetchone()
        if not row:
            return None
        d = dict(row)
        try:
            d["giocatore"] = json.loads(d["player_json"])
            d["stanza"] = json.loads(d["stanza_coord"])
            d["stanze"] = json.loads(d["stanze_json"])
        except json.JSONDecodeError:
            return None
        return d

    def delete_checkpoint(self, profile_id: int) -> None:
        with self._transaction() as conn:
            conn.execute("DELETE FROM save_games WHERE profile_id = ?", (profile_id,))

    def esiste_checkpoint(self, profile_id: int) -> bool:
        conn = self._get_conn()
        cur = conn.execute("SELECT 1 FROM save_games WHERE profile_id = ?", (profile_id,))
        return cur.fetchone() is not None

    # ========== RUN HISTORY / LEADERBOARD ==========

    def add_run(self, profile_id: int, run_data: dict) -> None:
        """Registra una partita completata nello storico."""
        with self._transaction() as conn:
            conn.execute("""
                INSERT INTO run_history (profile_id, piano_raggiunto, nemici_uccisi, tempo, vittoria, oggetti_raccolti)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                profile_id,
                run_data.get("piano", 1),
                run_data.get("nemici", 0),
                run_data.get("tempo", 0.0),
                1 if run_data.get("vittoria", False) else 0,
                json.dumps(run_data.get("oggetti", [])),
            ))

    def get_history(self, profile_id: int, limit: int = 50) -> list[dict]:
        """Storico partite per profilo (più recenti prima)."""
        conn = self._get_conn()
        cur = conn.execute("""
            SELECT * FROM run_history
            WHERE profile_id = ?
            ORDER BY data DESC
            LIMIT ?
        """, (profile_id, limit))
        return [dict(row) for row in cur.fetchall()]

    def get_leaderboard(self, limit: int = 10) -> list[dict]:
        """Top tempi vittorie (globale, tutti i profili)."""
        conn = self._get_conn()
        cur = conn.execute("""
            SELECT rh.*, p.nome
            FROM run_history rh
            JOIN profiles p ON rh.profile_id = p.id
            WHERE rh.vittoria = 1
            ORDER BY rh.tempo ASC
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cur.fetchall()]

    def get_global_stats(self) -> dict:
        """Statistiche aggregate globali."""
        conn = self._get_conn()
        cur = conn.execute("""
            SELECT
                COUNT(DISTINCT p.id) as total_profili,
                SUM(gs.partite) as total_partite,
                SUM(gs.vittorie) as total_vittorie,
                MAX(gs.piano_record) as max_piano,
                MAX(gs.record_nemici) as max_nemici,
                MIN(CASE WHEN gs.miglior_tempo > 0 THEN gs.miglior_tempo END) as best_time
            FROM profiles p
            LEFT JOIN game_stats gs ON p.id = gs.profile_id
        """)
        row = cur.fetchone()
        return dict(row) if row else {}


# Singleton per uso semplice
_db_instance: Database | None = None


def get_database() -> Database:
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance