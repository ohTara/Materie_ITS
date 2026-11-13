#!/usr/bin/env python3
"""Test di verifica per l'integrazione SQLite in Echoes of the Crypt.

Esegue: python test_verifica.py
"""
from __future__ import annotations

import json
import os
import shutil
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

# Aggiunge la directory del progetto al path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from database import Database, cartella_dati
import salvataggio


class TestDatabase(unittest.TestCase):
    """Test suite per database.py e salvataggio.py."""

    def setUp(self) -> None:
        """Crea DB temporaneo isolato per ogni test."""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="echoes_test_"))
        self.db_path = self.temp_dir / "game.db"
        self.db = Database(self.db_path)

    def tearDown(self) -> None:
        """Pulizia."""
        self.db.close()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _count_rows(self, table: str) -> int:
        cur = self.db._get_conn().execute(f"SELECT COUNT(*) FROM {table}")
        return cur.fetchone()[0]

    # ========== SCHEMA ==========

    def test_01_schema_creato(self) -> None:
        """Schema creato con tutte le tabelle e indici."""
        conn = self.db._get_conn()
        tables = {row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
        expected = {"schema_version", "profiles", "game_stats",
                    "save_games", "run_history"}
        self.assertTrue(expected.issubset(tables))

        # Indici
        indexes = {row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='index'")}
        self.assertIn("idx_run_history_profile_data", indexes)
        self.assertIn("idx_run_history_vittoria_tempo", indexes)
        self.assertIn("idx_save_games_profile", indexes)

        # Trigger
        triggers = {row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='trigger'")}
        self.assertIn("trg_game_stats_updated", triggers)
        self.assertIn("trg_save_games_updated", triggers)
        self.assertIn("trg_profiles_last_played", triggers)

    # ========== PROFILI ==========

    def test_02_crea_e_recupera_profilo(self) -> None:
        """Crea profilo e lo recupera."""
        pid = self.db.crea_profilo("TestPlayer")
        self.assertIsNotNone(pid)
        self.assertIsInstance(pid, int)

        profilo = self.db.get_profilo(pid)
        self.assertIsNotNone(profilo)
        self.assertEqual(profilo["nome"], "TestPlayer")

    def test_03_duplicato_nome_fallisce(self) -> None:
        """Nome duplicato ritorna None."""
        self.db.crea_profilo("Duplicato")
        result = self.db.crea_profilo("Duplicato")
        self.assertIsNone(result)

    def test_04_lista_profili_con_stats(self) -> None:
        """get_profili ritorna stats aggregate."""
        self.db.crea_profilo("P1")
        self.db.crea_profilo("P2")
        profili = self.db.get_profili()
        self.assertEqual(len(profili), 2)
        for p in profili:
            self.assertIn("partite", p)
            self.assertIn("vittorie", p)
            self.assertIn("piano_record", p)

    def test_05_elimina_profilo_cascade(self) -> None:
        """Eliminazione profilo cascata su stats/save/history."""
        pid = self.db.crea_profilo("DaEliminare")
        self.db.save_stats(pid, {"partite": 5, "vittorie": 3})
        self.db.save_checkpoint(pid, {"piano": 2, "seed": 123, "tempo": 100.0,
                                       "giocatore": {}, "stanza": [0, 0], "stanze": {}})
        self.db.add_run(pid, {"piano": 2, "nemici": 10, "tempo": 100.0,
                               "vittoria": True, "oggetti": []})

        self.db.elimina_profilo(pid)

        self.assertEqual(self._count_rows("profiles"), 0)
        self.assertEqual(self._count_rows("game_stats"), 0)
        self.assertEqual(self._count_rows("save_games"), 0)
        self.assertEqual(self._count_rows("run_history"), 0)

    # ========== STATISTICHE ==========

    def test_06_save_load_stats(self) -> None:
        """Roundtrip statistiche."""
        pid = self.db.crea_profilo("StatsTest")
        stats_in = {"partite": 10, "vittorie": 7, "record_nemici": 50,
                    "miglior_tempo": 123.4, "piano_record": 3}
        self.db.save_stats(pid, stats_in)
        stats_out = self.db.load_stats(pid)
        self.assertEqual(stats_out["partite"], 10)
        self.assertEqual(stats_out["vittorie"], 7)
        self.assertEqual(stats_out["record_nemici"], 50)
        self.assertAlmostEqual(stats_out["miglior_tempo"], 123.4)
        self.assertEqual(stats_out["piano_record"], 3)

    def test_07_stats_default_se_assenti(self) -> None:
        """Stats default se profilo senza stats."""
        pid = self.db.crea_profilo("NoStats")
        stats = self.db.load_stats(pid)
        self.assertEqual(stats["partite"], 0)
        self.assertEqual(stats["vittorie"], 0)

    # ========== SAVE GAME (CHECKPOINT) ==========

    def test_08_save_load_checkpoint(self) -> None:
        """Roundtrip checkpoint completo."""
        pid = self.db.crea_profilo("CheckpointTest")
        checkpoint = {
            "piano": 2,
            "seed": 42,
            "tempo": 345.6,
            "giocatore": {"vita": 6, "vita_max": 6, "danno": 2, "monete": 15,
                          "uccisioni": 23, "oggetti": ["Stivali veloci"]},
            "stanza": [1, 0],
            "stanze": {"0,0": {"visitata": True, "popolata": True, "raccoglibili": []},
                       "1,0": {"visitata": True, "popolata": False, "raccoglibili": []}}
        }
        self.db.save_checkpoint(pid, checkpoint)
        loaded = self.db.load_checkpoint(pid)

        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["piano"], 2)
        self.assertEqual(loaded["seed"], 42)
        self.assertAlmostEqual(loaded["tempo"], 345.6)
        self.assertEqual(loaded["giocatore"]["vita"], 6)
        self.assertEqual(loaded["giocatore"]["oggetti"], ["Stivali veloci"])
        self.assertEqual(loaded["stanza"], [1, 0])
        self.assertIn("0,0", loaded["stanze"])

    def test_09_delete_checkpoint(self) -> None:
        """Eliminazione checkpoint."""
        pid = self.db.crea_profilo("DelCheckpoint")
        self.db.save_checkpoint(pid, {"piano": 1, "seed": 1, "tempo": 0.0,
                                       "giocatore": {}, "stanza": [0, 0], "stanze": {}})
        self.assertTrue(self.db.esiste_checkpoint(pid))
        self.db.delete_checkpoint(pid)
        self.assertFalse(self.db.esiste_checkpoint(pid))
        self.assertIsNone(self.db.load_checkpoint(pid))

    def test_10_upsert_checkpoint_sovrascrive(self) -> None:
        """Secondo save_checkpoint sovrascrive il primo."""
        pid = self.db.crea_profilo("UpsertTest")
        self.db.save_checkpoint(pid, {"piano": 1, "seed": 1, "tempo": 10.0,
                                       "giocatore": {}, "stanza": [0, 0], "stanze": {}})
        self.db.save_checkpoint(pid, {"piano": 3, "seed": 99, "tempo": 999.0,
                                       "giocatore": {}, "stanza": [2, 0], "stanze": {}})
        loaded = self.db.load_checkpoint(pid)
        self.assertEqual(loaded["piano"], 3)
        self.assertEqual(loaded["seed"], 99)

    # ========== RUN HISTORY / LEADERBOARD ==========

    def test_11_add_run_e_history(self) -> None:
        """Aggiunta run e recupero storico."""
        pid = self.db.crea_profilo("HistoryTest")
        self.db.add_run(pid, {"piano": 1, "nemici": 5, "tempo": 100.0,
                               "vittoria": False, "oggetti": []})
        self.db.add_run(pid, {"piano": 3, "nemici": 30, "tempo": 500.0,
                               "vittoria": True, "oggetti": ["Amuleto di forza"]})

        history = self.db.get_history(pid, limit=10)
        self.assertEqual(len(history), 2)
        # Verifica contenuto indipendentemente dall'ordine (timestamp possono essere uguali)
        piani = {h["piano_raggiunto"] for h in history}
        vittorie = {h["vittoria"] for h in history}
        self.assertEqual(piani, {1, 3})
        self.assertEqual(vittorie, {0, 1})

    def test_12_leaderboard_solo_vittorie_ordinate_tempo(self) -> None:
        """Leaderboard mostra solo vittorie ordinate per tempo."""
        pid1 = self.db.crea_profilo("Fast")
        pid2 = self.db.crea_profilo("Slow")
        self.db.add_run(pid1, {"piano": 3, "nemici": 20, "tempo": 200.0,
                                "vittoria": True, "oggetti": []})
        self.db.add_run(pid2, {"piano": 3, "nemici": 25, "tempo": 400.0,
                                "vittoria": True, "oggetti": []})
        self.db.add_run(pid1, {"piano": 2, "nemici": 10, "tempo": 150.0,
                                "vittoria": False, "oggetti": []})  # sconfitta, non in LB

        lb = self.db.get_leaderboard(limit=5)
        self.assertEqual(len(lb), 2)
        self.assertEqual(lb[0]["nome"], "Fast")
        self.assertEqual(lb[0]["tempo"], 200.0)
        self.assertEqual(lb[1]["nome"], "Slow")
        self.assertEqual(lb[1]["tempo"], 400.0)

    # ========== MIGRAZIONE JSON ==========

    def test_13_migrazione_da_json_stats(self) -> None:
        """Migrazione automatica statistiche da JSON legacy."""
        # Crea file JSON legacy
        data_dir = self.temp_dir
        (data_dir / "salvataggio.json").write_text(json.dumps({
            "partite": 25, "vittorie": 10, "record_nemici": 100,
            "miglior_tempo": 300.5, "piano_record": 3
        }))
        (data_dir / "partita.json").write_text(json.dumps({
            "piano": 2, "seed": 123, "tempo": 150.0,
            "giocatore": {"vita": 4, "danno": 2},
            "stanza": [1, 0], "stanze": {}
        }))

        # Monkey-patch cartella_dati per usare temp_dir
        import database
        original = database.cartella_dati
        database.cartella_dati = lambda: data_dir
        try:
            db2 = Database(self.temp_dir / "game2.db")
            stats = db2.load_stats(1)  # profilo default "Giocatore1"
            self.assertEqual(stats["partite"], 25)
            self.assertEqual(stats["vittorie"], 10)
            self.assertEqual(stats["record_nemici"], 100)

            checkpoint = db2.load_checkpoint(1)
            self.assertIsNotNone(checkpoint)
            self.assertEqual(checkpoint["piano"], 2)
            self.assertEqual(checkpoint["seed"], 123)
        finally:
            database.cartella_dati = original

    def test_14_migrazione_crea_backup_json(self) -> None:
        """Migrazione rinomina JSON in .bak."""
        data_dir = self.temp_dir
        (data_dir / "salvataggio.json").write_text(json.dumps({"partite": 1}))

        import database
        original = database.cartella_dati
        database.cartella_dati = lambda: data_dir
        try:
            Database(self.temp_dir / "game3.db")
            self.assertTrue((data_dir / "salvataggio.json.bak").exists())
        finally:
            database.cartella_dati = original

    # ========== MULTI-PROFILO ==========

    def test_15_stats_separate_per_profilo(self) -> None:
        """Statistiche isolate per profilo."""
        p1 = self.db.crea_profilo("Player1")
        p2 = self.db.crea_profilo("Player2")
        self.db.save_stats(p1, {"partite": 10, "vittorie": 5})
        self.db.save_stats(p2, {"partite": 3, "vittorie": 3})

        self.assertEqual(self.db.load_stats(p1)["partite"], 10)
        self.assertEqual(self.db.load_stats(p2)["partite"], 3)

    def test_16_checkpoint_separati_per_profilo(self) -> None:
        """Checkpoint isolati per profilo."""
        p1 = self.db.crea_profilo("CP1")
        p2 = self.db.crea_profilo("CP2")
        self.db.save_checkpoint(p1, {"piano": 1, "seed": 1, "tempo": 10.0,
                                      "giocatore": {}, "stanza": [0, 0], "stanze": {}})
        self.db.save_checkpoint(p2, {"piano": 3, "seed": 2, "tempo": 20.0,
                                      "giocatore": {}, "stanza": [2, 0], "stanze": {}})

        self.assertEqual(self.db.load_checkpoint(p1)["piano"], 1)
        self.assertEqual(self.db.load_checkpoint(p2)["piano"], 3)

    # ========== TRANSAZIONI ==========

    def test_17_transazioni_atomiche(self) -> None:
        """Rollback su errore in transazione multi-tabella."""
        pid = self.db.crea_profilo("TransTest")
        self.db.save_stats(pid, {"partite": 1})

        # Forza errore: insert duplicato PK in game_stats (stesso profile_id)
        # Non dovrebbe corrompere i dati esistenti
        try:
            with self.db._transaction() as tx:
                tx.execute("INSERT INTO game_stats (profile_id) VALUES (?)", (pid,))
                tx.execute("INSERT INTO game_stats (profile_id) VALUES (?)", (pid,))  # duplicate
        except sqlite3.IntegrityError:
            pass

        # Statistiche originali intatte
        stats = self.db.load_stats(pid)
        self.assertEqual(stats["partite"], 1)

    # ========== INTEGRAZIONE SALVATAGGIO.PY ==========

    def test_18_salvataggio_api_compatibile(self) -> None:
        """salvataggio.py mantiene stessa API della versione JSON."""
        import database
        import salvataggio as sv
        # Patch both modules
        orig_db_cartella = database.cartella_dati
        orig_sv_cartella = sv.cartella_dati
        database.cartella_dati = lambda: self.temp_dir
        sv.cartella_dati = lambda: self.temp_dir
        # Reset ALL singletons
        database._db_instance = None
        sv._default_profile_id = None
        sv._db = None
        try:
            # Test API
            stats = sv.carica()
            self.assertEqual(stats["partite"], 0)

            sv.registra_partita(stats, nemici=5, tempo=100.0, vittoria=True, piano=1)
            stats2 = sv.carica()
            self.assertEqual(stats2["partite"], 1)
            self.assertEqual(stats2["vittorie"], 1)

            # Checkpoint
            stato = {"piano": 2, "seed": 42, "tempo": 200.0,
                     "giocatore": {"vita": 6}, "stanza": [0, 0], "stanze": {}}
            sv.salva_partita(stato)
            self.assertTrue(sv.esiste_partita())
            loaded = sv.carica_partita()
            self.assertEqual(loaded["piano"], 2)

            sv.cancella_partita()
            self.assertFalse(sv.esiste_partita())
        finally:
            database.cartella_dati = orig_db_cartella
            sv.cartella_dati = orig_sv_cartella
            database._db_instance = None
            sv._db = None

    def test_19_nuove_funzioni_profili(self) -> None:
        """Nuove funzioni multi-profilo in salvataggio.py."""
        import database
        import salvataggio as sv
        # Patch both modules
        orig_db_cartella = database.cartella_dati
        orig_sv_cartella = sv.cartella_dati
        database.cartella_dati = lambda: self.temp_dir
        sv.cartella_dati = lambda: self.temp_dir
        # Reset ALL singletons
        database._db_instance = None
        sv._default_profile_id = None
        sv._db = None
        try:
            pid = sv.crea_profilo("NuovoProfilo")
            self.assertIsNotNone(pid)

            profili = sv.get_profili()
            self.assertEqual(len(profili), 1)
            self.assertEqual(profili[0]["nome"], "NuovoProfilo")

            sv.seleziona_profilo(pid)
            self.assertEqual(sv.get_profilo_corrente()["id"], pid)

            leaderboard = sv.get_leaderboard()
            self.assertIsInstance(leaderboard, list)

            storico = sv.get_storico(pid)
            self.assertIsInstance(storico, list)

            globali = sv.get_statistiche_globali()
            self.assertIn("total_profili", globali)
        finally:
            database.cartella_dati = orig_db_cartella
            sv.cartella_dati = orig_sv_cartella
            database._db_instance = None
            sv._db = None
            sv._default_profile_id = None

    # ========== INTEGRAZIONE GIOCO (SIMULAZIONE) ==========

    def test_20_simulazione_partita_completa(self) -> None:
        """Simula: nuova partita -> gioca piano -> salva -> esce -> ricarica -> stato identico."""
        import database
        import salvataggio as sv
        # Patch both modules
        orig_db_cartella = database.cartella_dati
        orig_sv_cartella = sv.cartella_dati
        database.cartella_dati = lambda: self.temp_dir
        sv.cartella_dati = lambda: self.temp_dir
        # Reset ALL singletons
        database._db_instance = None
        sv._default_profile_id = None
        sv._db = None
        try:
            # 1. Nuova partita
            stats = sv.carica()
            self.assertEqual(stats["partite"], 0)

            # 2. Gioca piano 1, sconfigge nemici, raccoglie oggetti
            stato_piano1 = {
                "piano": 1, "seed": 12345, "tempo": 120.5,
                "giocatore": {"vita": 6, "vita_max": 6, "danno": 2,
                              "gittata": 350, "cadenza": 0.35, "vel_proiettile": 500,
                              "velocita": 260, "monete": 10, "uccisioni": 8,
                              "oggetti": ["Stivali veloci", "Lente d'ingrandimento"]},
                "stanza": [0, 1],
                "stanze": {
                    "0,0": {"visitata": True, "popolata": True, "raccoglibili": []},
                    "0,1": {"visitata": True, "popolata": True, "raccoglibili": []}
                }
            }
            sv.salva_partita(stato_piano1)

            # 3. Esce e ricarica (simula riavvio gioco)
            database._db_instance = None  # forza nuovo DB con nuova cartella
            sv._default_profile_id = None
            sv._db = None
            stats2 = sv.carica()
            self.assertEqual(stats2["partite"], 0)  # partita non finita

            loaded = sv.carica_partita()
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded["piano"], 1)
            self.assertEqual(loaded["seed"], 12345)
            self.assertAlmostEqual(loaded["tempo"], 120.5)
            self.assertEqual(loaded["giocatore"]["danno"], 2)
            self.assertEqual(loaded["giocatore"]["oggetti"],
                             ["Stivali veloci", "Lente d'ingrandimento"])
            self.assertEqual(loaded["stanza"], [0, 1])

            # 4. Completa il gioco (vittoria)
            sv.registra_partita(stats2, nemici=25, tempo=350.0, vittoria=True, piano=3)
            stats3 = sv.carica()
            self.assertEqual(stats3["partite"], 1)
            self.assertEqual(stats3["vittorie"], 1)
            self.assertEqual(stats3["piano_record"], 3)
            self.assertAlmostEqual(stats3["miglior_tempo"], 350.0)

            # 5. Checkpoint cancellato dopo vittoria
            self.assertFalse(sv.esiste_partita())

            # 6. Leaderboard aggiornato
            lb = sv.get_leaderboard()
            self.assertEqual(len(lb), 1)
            self.assertEqual(lb[0]["tempo"], 350.0)
        finally:
            database.cartella_dati = orig_db_cartella
            sv.cartella_dati = orig_sv_cartella
            database._db_instance = None
            sv._db = None
            sv._default_profile_id = None

    # ========== CLASSIFICA E STORICO ==========

    def test_21_storico_piu_recente_per_primo(self) -> None:
        """Partite registrate nello stesso secondo: l'ultima inserita e' la prima."""
        pid = self.db.crea_profilo("Ordine")
        for piano in (1, 2, 3):
            self.db.add_run(pid, {"piano": piano, "nemici": piano, "tempo": 10.0 * piano})
        storico = self.db.get_history(pid)
        self.assertEqual([r["piano_raggiunto"] for r in storico], [3, 2, 1])
        self.assertIn("data_locale", storico[0])

    def test_22_classifica_solo_vittorie_in_ordine_di_tempo(self) -> None:
        """La classifica contiene solo le vittorie, dalla piu' veloce, con il nome del profilo."""
        a = self.db.crea_profilo("Anna")
        b = self.db.crea_profilo("Bruno")
        self.db.add_run(a, {"piano": 3, "nemici": 30, "tempo": 400.0, "vittoria": True})
        self.db.add_run(b, {"piano": 3, "nemici": 28, "tempo": 250.0, "vittoria": True})
        self.db.add_run(b, {"piano": 2, "nemici": 12, "tempo": 90.0, "vittoria": False})
        classifica = self.db.get_leaderboard()
        self.assertEqual([(r["nome"], r["tempo"]) for r in classifica],
                         [("Bruno", 250.0), ("Anna", 400.0)])
        self.assertEqual(len(self.db.get_leaderboard(limit=1)), 1)

    def test_23_oggetti_salvati_nello_storico(self) -> None:
        """registra_partita salva nello storico gli oggetti raccolti."""
        import database
        import salvataggio as sv
        orig_db_cartella = database.cartella_dati
        orig_sv_cartella = sv.cartella_dati
        database.cartella_dati = lambda: self.temp_dir
        sv.cartella_dati = lambda: self.temp_dir
        database._db_instance = None
        sv._default_profile_id = None
        sv._db = None
        try:
            stats = sv.carica()
            sv.registra_partita(stats, nemici=7, tempo=120.0, vittoria=False, piano=2,
                                oggetti=["Lama affilata", "Stivali alati"])
            storico = sv.get_storico()
            self.assertEqual(len(storico), 1)
            self.assertEqual(json.loads(storico[0]["oggetti_raccolti"]),
                             ["Lama affilata", "Stivali alati"])
            # Senza il parametro la lista resta vuota (compatibilita' con le chiamate esistenti)
            sv.registra_partita(sv.carica(), nemici=1, tempo=5.0, vittoria=False)
            self.assertEqual(json.loads(sv.get_storico()[0]["oggetti_raccolti"]), [])
        finally:
            database.cartella_dati = orig_db_cartella
            sv.cartella_dati = orig_sv_cartella
            database._db_instance = None
            sv._db = None
            sv._default_profile_id = None

    def test_24_formatta_tempo(self) -> None:
        """formatta_tempo converte i secondi in minuti:secondi."""
        try:
            from interfaccia import formatta_tempo
        except ImportError:
            self.skipTest("pygame non installato")
        self.assertEqual(formatta_tempo(0), "0:00")
        self.assertEqual(formatta_tempo(59.9), "0:59")
        self.assertEqual(formatta_tempo(125.4), "2:05")
        self.assertEqual(formatta_tempo(3600), "60:00")
        self.assertEqual(formatta_tempo(-3), "0:00")


def run_tests() -> None:
    """Esegue tutti i test e riporta risultato."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDatabase)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print(f"[OK] TUTTI I {result.testsRun} TEST SUPERATI")
    else:
        print(f"[FAIL] {len(result.failures)} FALLIMENTI, {len(result.errors)} ERRORI su {result.testsRun} test")
        for test, trace in result.failures + result.errors:
            print(f"  - {test}: {trace.split(chr(10))[-2]}")
    print("=" * 60)

    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    run_tests()
