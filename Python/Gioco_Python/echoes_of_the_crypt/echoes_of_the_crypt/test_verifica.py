#!/usr/bin/env python3
"""Test di verifica di Echoes of the Crypt: integrazione SQLite, negozio, oggetti, sinergie, audio, seed, grafica, personaggi, abilita' e sblocchi.

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


class TestNegozio(unittest.TestCase):
    """Test del negozio: generazione, acquisti e salvataggio della merce."""

    def _negozio(self, seed: int = 1):
        """Restituisce (giocatore, stanza negozio gia' rifornita) di un piano di prova."""
        from dungeon import Dungeon, Stanza
        from giocatore import Giocatore
        d = Dungeon(num_stanze=9, seed=seed)
        g = Giocatore(*Stanza.AREA.center)
        stanza = next(s for s in d.stanze.values() if s.ruolo == "negozio")
        stanza.entra(g, d.rng)
        return g, stanza

    def test_25_un_negozio_per_piano(self) -> None:
        """Ogni piano ha un solo negozio, oltre a inizio, tesoro e boss."""
        from dungeon import Dungeon
        for seed in range(200):
            for piano in (1, 2, 3):
                ruoli = [s.ruolo for s in Dungeon(7 + 2 * piano, seed, piano).stanze.values()]
                for ruolo in ("iniziale", "tesoro", "negozio", "boss"):
                    self.assertEqual(ruoli.count(ruolo), 1, f"seed {seed} piano {piano}: {ruolo}")

    def test_26_merce_del_negozio(self) -> None:
        """Il negozio espone due passivi diversi e un cuore, tutti a pagamento e senza nemici."""
        from oggetti import PREZZI
        g, stanza = self._negozio()
        self.assertEqual(sorted(r.tipo for r in stanza.raccoglibili),
                         ["cuore", "passivo", "passivo"])
        self.assertEqual(len({r.id for r in stanza.raccoglibili if r.tipo == "passivo"}), 2)
        self.assertTrue(all(r.prezzo == PREZZI[r.tipo] for r in stanza.raccoglibili))
        self.assertTrue(stanza.porte_aperte())
        # Chi riprende la partita riparte dal centro: non deve toccare la merce.
        self.assertFalse(any(r.rect.colliderect(g.rect) for r in stanza.raccoglibili))

    def test_27_acquisto_con_e_senza_monete(self) -> None:
        """Senza monete non si compra; con le monete si paga e si ottiene l'oggetto."""
        from oggetti import PREZZI
        g, stanza = self._negozio()
        passivo = next(r for r in stanza.raccoglibili if r.tipo == "passivo")
        g.monete = PREZZI["passivo"] - 1
        self.assertFalse(passivo.raccogli(g))
        self.assertEqual((g.monete, g.oggetti), (PREZZI["passivo"] - 1, []))
        g.monete = PREZZI["passivo"] + 2
        self.assertTrue(passivo.raccogli(g))
        self.assertEqual((g.monete, g.oggetti), (2, [passivo.nome]))

    def test_28_cuore_non_venduto_a_vita_piena(self) -> None:
        """Il cuore in vendita si compra solo se serve; quello gratis si raccoglie sempre."""
        from oggetti import Raccoglibile
        g, stanza = self._negozio()
        cuore = next(r for r in stanza.raccoglibili if r.tipo == "cuore")
        g.monete = 10
        self.assertFalse(cuore.raccogli(g))
        self.assertEqual(g.monete, 10)
        g.vita -= 2
        self.assertTrue(cuore.raccogli(g))
        self.assertEqual((g.vita, g.monete), (g.vita_max - 1, 10 - cuore.prezzo))
        self.assertTrue(Raccoglibile("cuore", (0, 0)).raccogli(g))

    def test_29_prezzi_nel_salvataggio(self) -> None:
        """La merce rimasta conserva il prezzo dopo salva/carica; i vecchi salvataggi restano validi."""
        from dungeon import Stanza
        _, stanza = self._negozio()
        stanza.raccoglibili.pop(0)                       # un oggetto gia' comprato
        dati = json.loads(json.dumps(stanza.a_dict()))   # passa dal JSON come il checkpoint
        copia = Stanza(stanza.coord, "negozio")
        copia.da_dict(dati)
        self.assertEqual([(r.tipo, r.id, r.prezzo, r.rect.center) for r in copia.raccoglibili],
                         [(r.tipo, r.id, r.prezzo, r.rect.center) for r in stanza.raccoglibili])
        self.assertTrue(copia.popolata)                  # rientrando non si rifornisce
        vecchia = Stanza((0, 0), "tesoro")
        vecchia.da_dict({"visitata": True, "popolata": True,
                         "raccoglibili": [["passivo", 640, 360, "stivali"]]})
        self.assertEqual(vecchia.raccoglibili[0].prezzo, 0)


class TestOggetti(unittest.TestCase):
    """Test dei dizionari OGGETTI e SINERGIE e dell'attivazione delle sinergie."""

    def _giocatore(self):
        """Restituisce un giocatore nuovo."""
        from giocatore import Giocatore
        return Giocatore(0, 0)

    def _prendi(self, g, *ids: str) -> None:
        """Fa raccogliere al giocatore g gli oggetti passivi indicati."""
        from oggetti import Raccoglibile
        for k in ids:
            Raccoglibile("passivo", (0, 0), k).raccogli(g)

    def test_30_dati_coerenti(self) -> None:
        """15 oggetti con nomi unici; effetti e sinergie usano solo chiavi esistenti."""
        from oggetti import OGGETTI, SINERGIE
        g = self._giocatore()
        self.assertEqual(len(OGGETTI), 15)
        self.assertEqual(len({v["nome"] for v in OGGETTI.values()}), len(OGGETTI))
        for dati in (*OGGETTI.values(), *SINERGIE.values()):
            for stat in dati["effetti"]:
                self.assertTrue(hasattr(g, stat), f"{dati['nome']}: statistica {stat}")
        for dati in SINERGIE.values():
            self.assertGreaterEqual(len(set(dati["richiede"])), 2, dati["nome"])
            for k in dati["richiede"]:
                self.assertIn(k, OGGETTI, dati["nome"])

    def test_31_sinergia_una_volta_sola(self) -> None:
        """La sinergia scatta col secondo oggetto, in qualunque ordine, e non si ripete."""
        g = self._giocatore()
        self._prendi(g, "falco")
        self.assertEqual(g.sinergie, [])
        self._prendi(g, "lente")
        self.assertEqual(g.sinergie, ["Cecchino"])
        self.assertEqual(g.danno, 2)                      # 1 di base + 1 della sinergia
        self.assertEqual(g.avvisi[-1], "Sinergia: Cecchino!")
        self._prendi(g, "stivali")                        # un altro oggetto non la riattiva
        self.assertEqual((g.sinergie, g.danno), (["Cecchino"], 2))

    def test_32_tutte_le_sinergie_e_limiti(self) -> None:
        """Con tutti gli oggetti sono attive tutte le sinergie e le statistiche restano nei limiti."""
        from oggetti import OGGETTI, SINERGIE
        g = self._giocatore()
        self._prendi(g, *OGGETTI)
        self.assertEqual(sorted(g.sinergie), sorted(v["nome"] for v in SINERGIE.values()))
        self.assertGreaterEqual(g.cadenza, 0.1)
        self.assertLessEqual(g.vita_max, 12)
        self.assertLessEqual(g.vita, g.vita_max)
        self.assertGreaterEqual(g.gittata, 150)

    def test_33_sinergie_nel_salvataggio(self) -> None:
        """Le sinergie attive sopravvivono a salva/carica e non danno il bonus due volte."""
        g = self._giocatore()
        self._prendi(g, "cannone", "caffe")
        dati = json.loads(json.dumps(g.a_dict()))
        copia = self._giocatore()
        copia.da_dict(dati)
        self.assertEqual(copia.sinergie, ["Artiglieria"])
        cadenza = copia.cadenza
        self._prendi(copia, "elmo")
        self.assertEqual((copia.sinergie, copia.cadenza), (["Artiglieria"], cadenza))
        vecchio = self._giocatore()                       # salvataggio senza il campo
        vecchio.da_dict({"oggetti": ["Stivali veloci"]})
        self.assertEqual(vecchio.sinergie, [])


class TestAudio(unittest.TestCase):
    """Test della sintesi dei suoni (senza scheda audio)."""

    def test_34_sintesi_dei_suoni(self) -> None:
        """Ogni suono ha la durata dichiarata, non satura e finisce in silenzio."""
        import audio
        for nome, tratti in audio.SUONI.items():
            campioni = audio.sintetizza(tratti)
            attesi = sum(int(audio.FREQUENZA * t[3]) for t in tratti)
            self.assertEqual(len(campioni), attesi, nome)
            self.assertGreater(max(abs(c) for c in campioni), 1000, nome)
            self.assertLess(abs(campioni[-1]), 500, nome)

    def test_35_musica_e_suoni_usati(self) -> None:
        """La musica dura quanto le sue note; i suoni usati nel codice esistono tutti."""
        import audio
        import re
        musica = audio.sintetizza_musica(audio.MUSICA)
        self.assertEqual(len(musica), sum(int(audio.FREQUENZA * d) for _, d in audio.MUSICA))
        self.assertLessEqual(max(abs(c) for c in musica), audio.AMPIEZZA)
        usati = set()
        for f in PROJECT_ROOT.glob("*.py"):
            if f.name != "test_verifica.py":
                usati.update(re.findall(r'"(\w+)"', " ".join(
                    re.findall(r"audio\.suona\((.*?)\)$", f.read_text(encoding="utf-8"),
                               re.M | re.S))))
        usati -= {"passivo"}                      # e' un tipo di raccoglibile, non un suono
        self.assertTrue(usati)
        self.assertLessEqual(usati, set(audio.SUONI), usati - set(audio.SUONI))

    def test_36_senza_audio_non_si_blocca(self) -> None:
        """Senza mixer inizializzato suona() e avvia_musica() non fanno nulla."""
        import audio
        audio._suoni.clear()
        audio._musica = None
        audio.suona("sparo")
        audio.suona("inesistente")
        audio.avvia_musica()
        self.assertTrue(audio.cambia_muto())
        self.assertFalse(audio.cambia_muto())


class TestSeedEInput(unittest.TestCase):
    """Test del seed condivisibile e della casella di testo."""

    def _scrivi(self, campo, testo: str):
        """Simula la digitazione di testo nella casella; restituisce l'ultimo risultato."""
        import pygame
        esito = None
        for c in testo:
            tasto = {"\n": pygame.K_RETURN, "\b": pygame.K_BACKSPACE}.get(c, ord(c))
            esito = campo.gestisci_evento(
                pygame.event.Event(pygame.KEYDOWN, key=tasto, unicode=c))
        return esito

    def test_37_stesso_seed_stessi_piani(self) -> None:
        """Lo stesso seed di partita genera gli stessi piani; i piani sono diversi tra loro."""
        from dungeon import Dungeon
        from main import seed_del_piano

        def mappa(seed_partita: int, piano: int) -> dict:
            d = Dungeon(7 + 2 * piano, seed_del_piano(seed_partita, piano), piano)
            return {c: s.ruolo for c, s in d.stanze.items()}

        for piano in (1, 2, 3):
            self.assertEqual(mappa(12345, piano), mappa(12345, piano))
        self.assertEqual(len({seed_del_piano(12345, p) for p in (1, 2, 3)}), 3)
        self.assertNotEqual(seed_del_piano(12345, 1), seed_del_piano(12346, 1))
        self.assertTrue(all(0 <= seed_del_piano(s, 1) < 10**9 for s in range(50)))

    def test_38_casella_nome(self) -> None:
        """La casella accetta lettere, cifre e spazi, rispetta la lunghezza e conferma con Invio."""
        from interfaccia import CampoTesto
        campo = CampoTesto("T", "R", lunghezza_max=8)
        self.assertIsNone(self._scrivi(campo, "Lu;ca!\b\bca 2026abc"))
        self.assertEqual(campo.valore, "Luca 202")
        self.assertEqual(self._scrivi(campo, "\n"), "Luca 202")
        vuoto = CampoTesto("T", "R")
        self.assertIsNone(self._scrivi(vuoto, "  \n"))        # un nome vuoto non si conferma

    def test_39_casella_seed(self) -> None:
        """La casella del seed accetta solo cifre, al massimo 9."""
        from interfaccia import CampoTesto
        campo = CampoTesto("T", "R", lunghezza_max=9, solo_cifre=True)
        self.assertEqual(self._scrivi(campo, "12a-3 4567890123\n"), "123456789")

    def test_40_seed_partita_nel_checkpoint(self) -> None:
        """Il seed della partita si salva nel checkpoint, anche in un database creato prima (v1)."""
        cartella = Path(tempfile.mkdtemp(prefix="echoes_seed_"))
        try:
            db = Database(cartella / "nuovo.db")
            pid = db.crea_profilo("Seed")
            stato = {"piano": 2, "seed": 777, "seed_partita": 42, "tempo": 1.5,
                     "giocatore": {}, "stanza": [0, 0], "stanze": {}}
            db.save_checkpoint(pid, stato)
            self.assertEqual(db.load_checkpoint(pid)["seed_partita"], 42)
            db.save_checkpoint(pid, {**stato, "seed_partita": 0})      # 0 e' un seed valido
            self.assertEqual(db.load_checkpoint(pid)["seed_partita"], 0)
            db.close()

            # Database "vecchio": stessa struttura ma senza la colonna nuova.
            vecchio = cartella / "vecchio.db"
            db = Database(vecchio)
            pid = db.crea_profilo("Vecchio")
            db.save_checkpoint(pid, stato)
            db.close()
            conn = sqlite3.connect(vecchio)
            conn.execute("ALTER TABLE save_games DROP COLUMN seed_partita")
            conn.execute("UPDATE schema_version SET version = 1")
            conn.commit()
            conn.close()
            db = Database(vecchio)                         # riaprendolo viene migrato
            caricato = db.load_checkpoint(pid)
            self.assertIsNone(caricato["seed_partita"])
            self.assertEqual(caricato["seed"], 777)
            db.save_checkpoint(pid, stato)
            self.assertEqual(db.load_checkpoint(pid)["seed_partita"], 42)
            db.close()
        finally:
            shutil.rmtree(cartella, ignore_errors=True)

    def test_47_personaggio_e_seed_nello_storico(self) -> None:
        """Storico e classifica riportano personaggio e seed; le partite vecchie restano leggibili."""
        cartella = Path(tempfile.mkdtemp(prefix="echoes_storico_"))
        try:
            vecchio = cartella / "vecchio.db"
            db = Database(vecchio)
            pid = db.crea_profilo("Storico")
            db.add_run(pid, {"piano": 3, "nemici": 9, "tempo": 80.0, "vittoria": True})
            db.close()
            conn = sqlite3.connect(vecchio)                # torna alla struttura precedente
            conn.execute("ALTER TABLE run_history DROP COLUMN personaggio")
            conn.execute("ALTER TABLE run_history DROP COLUMN seed_partita")
            conn.execute("UPDATE schema_version SET version = 2")
            conn.commit()
            conn.close()
            db = Database(vecchio)
            db.add_run(pid, {"piano": 3, "nemici": 20, "tempo": 60.0, "vittoria": True,
                             "personaggio": "Templare", "seed_partita": 0})
            prima, seconda = db.get_leaderboard()
            self.assertEqual((prima["personaggio"], prima["seed_partita"]), ("Templare", 0))
            self.assertEqual((seconda["personaggio"], seconda["seed_partita"]), (None, None))
            self.assertEqual(db.get_history(pid)[0]["personaggio"], "Templare")
            db.close()
        finally:
            shutil.rmtree(cartella, ignore_errors=True)
        from main import testo_seed
        self.assertEqual((testo_seed(None), testo_seed(0), testo_seed(42)), ("-", "0", "42"))


class TestGrafica(unittest.TestCase):
    """Test della grafica generata dal programma (senza finestra)."""

    def test_41_sprite_ben_formati(self) -> None:
        """Ogni sprite e' una griglia rettangolare che usa solo i caratteri della tavolozza."""
        import grafica
        ammessi = set(grafica.TAVOLOZZA) | set(".xX")
        for nome, griglia in grafica.SPRITE.items():
            self.assertEqual(len({len(riga) for riga in griglia}), 1, nome)
            self.assertLessEqual(set("".join(griglia)), ammessi, nome)
            img = grafica.sprite(nome, 3, (100, 40, 40))
            self.assertEqual(img.get_size(), (len(griglia[0]) * 3, len(griglia) * 3), nome)

    def test_42_ogni_nemico_ha_lo_sprite(self) -> None:
        """Tutti i nemici (boss compresi) e tutti gli oggetti hanno uno sprite e un colore."""
        import grafica
        from nemici import DATI_NEMICI, crea_nemico
        from oggetti import COLORI_EFFETTO, OGGETTI
        for tipo in DATI_NEMICI:
            self.assertIn(crea_nemico(tipo, 0, 0).sprite, grafica.SPRITE, tipo)
        for dati in OGGETTI.values():
            self.assertIn(next(iter(dati["effetti"])), COLORI_EFFETTO, dati["nome"])

    def test_43_disegno_di_tutte_le_stanze(self) -> None:
        """Ogni tipo di stanza si disegna senza errori, con nemici, proiettili, merce e macchie."""
        import pygame
        import grafica
        from dungeon import Dungeon, Stanza
        from entita import Proiettile
        from giocatore import Giocatore
        schermo = pygame.Surface((1280, 720))
        d = Dungeon(num_stanze=11, seed=3, piano=2)
        g = Giocatore(*Stanza.AREA.center)
        ruoli = set()
        for stanza in d.stanze.values():
            stanza.entra(g, d.rng)
            stanza.proiettili.append(Proiettile(500, 300, pygame.Vector2(1, 0), 100, 1, 300))
            stanza.proiettili.append(Proiettile(600, 300, pygame.Vector2(0, 1), 100, 1, 300, True))
            schermo.fill(grafica.NERO)
            stanza.draw(schermo)
            grafica.aggiungi_macchia(stanza, (640, 360), 30, (74, 14, 20))
            stanza.draw(schermo)
            self.assertNotEqual(schermo.get_at(Stanza.AREA.center)[:3], grafica.NERO)
            ruoli.add(stanza.ruolo)
        self.assertEqual(ruoli, {"iniziale", "normale", "tesoro", "negozio", "boss"})
        grafica.disegna_sfondo_menu(schermo)
        grafica.velo(schermo)


class TestPersonaggi(unittest.TestCase):
    """Test dei personaggi giocabili."""

    def test_44_statistiche_di_partenza(self) -> None:
        """Ogni personaggio parte con le statistiche del dizionario e nomi unici."""
        from giocatore import PERSONAGGI, PREDEFINITO, Giocatore
        self.assertIn(PREDEFINITO, PERSONAGGI)
        self.assertEqual(len({p["nome"] for p in PERSONAGGI.values()}), len(PERSONAGGI))
        for chiave, p in PERSONAGGI.items():
            g = Giocatore(0, 0, chiave)
            self.assertEqual((g.vita, g.vita_max), (p["vita"], p["vita"]), chiave)
            for stat in ("velocita", "danno", "cadenza", "gittata", "vel_proiettile"):
                self.assertEqual(getattr(g, stat), p[stat], f"{chiave}: {stat}")
            self.assertEqual(g.tinta, p["tinta"])
            self.assertLessEqual(p["vita"], 12)
        self.assertEqual(Giocatore(0, 0).personaggio, PREDEFINITO)

    def test_45_personaggio_nel_salvataggio(self) -> None:
        """Il personaggio sopravvive a salva/carica; i salvataggi vecchi usano quello predefinito."""
        from giocatore import PERSONAGGI, PREDEFINITO, Giocatore
        g = Giocatore(0, 0, "templare")
        copia = Giocatore(0, 0)
        copia.da_dict(json.loads(json.dumps(g.a_dict())))
        self.assertEqual((copia.personaggio, copia.vita_max, copia.danno, copia.tinta),
                         ("templare", 8, 2, PERSONAGGI["templare"]["tinta"]))
        vecchio = Giocatore(0, 0)
        vecchio.da_dict({"vita": 3, "oggetti": []})
        self.assertEqual(vecchio.personaggio, PREDEFINITO)
        strano = Giocatore(0, 0)
        strano.da_dict({"personaggio": "inesistente"})
        self.assertEqual(strano.personaggio, PREDEFINITO)

    def test_46_schermata_di_scelta(self) -> None:
        """Le frecce scorrono i personaggi in cerchio, Invio conferma; la schermata si disegna."""
        import pygame
        from giocatore import PERSONAGGI
        from interfaccia import SceltaPersonaggio
        scelta = SceltaPersonaggio()
        chiavi = list(PERSONAGGI)

        def premi(tasto: int):
            return scelta.gestisci_evento(pygame.event.Event(pygame.KEYDOWN, key=tasto))

        self.assertEqual(premi(pygame.K_RETURN), chiavi[0])
        self.assertIsNone(premi(pygame.K_LEFT))
        self.assertEqual(premi(pygame.K_RETURN), chiavi[-1])
        premi(pygame.K_RIGHT)
        premi(pygame.K_RIGHT)
        self.assertEqual(premi(pygame.K_RETURN), chiavi[1])
        scelta.draw(pygame.Surface((1280, 720)))


class TestSfida(unittest.TestCase):
    """Test di sblocchi, maestrie, abilita' e dei nemici piu' difficili."""

    @classmethod
    def setUpClass(cls) -> None:
        """Apre un video finto: Stanza.update legge lo stato della tastiera."""
        import pygame
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
        pygame.display.init()

    def _stanza(self, personaggio: str = "viandante", maestria: bool = False):
        """Restituisce (giocatore, stanza vuota) pronti per una prova."""
        from dungeon import Stanza
        from giocatore import Giocatore
        g = Giocatore(*Stanza.AREA.center, personaggio)
        g.maestria = maestria
        stanza = Stanza((5, 5), "normale")
        stanza.giocatore = g
        stanza.popolata = True
        return g, stanza

    def test_48_sblocco_dei_personaggi(self) -> None:
        """All'inizio c'e' solo il Viandante; gli altri si aprono con piani e vittorie."""
        import pygame
        from giocatore import PERSONAGGI, sbloccato, testo_sblocco
        from interfaccia import SceltaPersonaggio

        def aperti(vittorie: int, piano: int) -> list[str]:
            dati = {"vittorie": vittorie, "piano_record": piano}
            return [k for k in PERSONAGGI if sbloccato(k, dati)]

        self.assertEqual(aperti(0, 1), ["viandante"])
        self.assertEqual(aperti(0, 2), ["viandante", "predone"])
        self.assertEqual(aperti(1, 3), ["viandante", "predone", "templare"])
        self.assertEqual(aperti(3, 3), list(PERSONAGGI))
        self.assertTrue(all(testo_sblocco(k) for k in PERSONAGGI if k != "viandante"))
        scelta = SceltaPersonaggio({"vittorie": 0, "piano_record": 1}, {})
        invio = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
        self.assertEqual(scelta.gestisci_evento(invio), "viandante")
        scelta.gestisci_evento(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))
        self.assertIsNone(scelta.gestisci_evento(invio))          # il Predone e' bloccato
        scelta.draw(pygame.Surface((1280, 720)))

    def test_49_maestria_e_traguardi(self) -> None:
        """La maestria arriva dopo le vittorie con quel personaggio; i traguardi nuovi si ricavano per differenza."""
        from giocatore import MAESTRIA_VITTORIE, ha_maestria, traguardi
        self.assertFalse(ha_maestria("viandante", {"viandante": MAESTRIA_VITTORIE - 1}))
        self.assertTrue(ha_maestria("viandante", {"viandante": MAESTRIA_VITTORIE}))
        self.assertFalse(ha_maestria("predone", {"viandante": 9}))
        prima = traguardi({"vittorie": 0, "piano_record": 3}, {})
        dopo = traguardi({"vittorie": 1, "piano_record": 3}, {"viandante": 1})
        self.assertEqual(dopo - prima, {"Nuovo personaggio: Templare"})
        cartella = Path(tempfile.mkdtemp(prefix="echoes_maestria_"))
        try:
            db = Database(cartella / "m.db")
            pid = db.crea_profilo("Maestro")
            for nome, vinta in (("Viandante", True), ("Viandante", True), ("Predone", False),
                                ("Predone", True), (None, True)):
                db.add_run(pid, {"vittoria": vinta, "personaggio": nome})
            self.assertEqual(db.vittorie_per_personaggio(pid), {"Viandante": 2, "Predone": 1})
            db.close()
        finally:
            shutil.rmtree(cartella, ignore_errors=True)

    def test_50_abilita_dei_personaggi(self) -> None:
        """Ogni abilita' fa il suo effetto e parte la ricarica (dimezzata dalla maestria del Viandante)."""
        import pygame
        from entita import Proiettile
        from giocatore import ABILITA, PERSONAGGI
        from nemici import crea_nemico
        self.assertTrue(all(p["abilita"] in ABILITA for p in PERSONAGGI.values()))

        g, stanza = self._stanza("viandante")
        vita = g.vita
        g.usa_abilita(stanza)
        g.subisci_danno(1)                                # durante lo scatto non si viene colpiti
        self.assertEqual((g.vita, g.ricarica_abilita), (vita, ABILITA["scatto"]["ricarica"]))
        x = g.pos.y
        stanza.update(0.05)
        self.assertGreater(g.pos.y - x, 40)               # lo scatto sposta molto in un attimo
        g2, s2 = self._stanza("viandante", maestria=True)
        g2.usa_abilita(s2)
        self.assertEqual(g2.ricarica_abilita, ABILITA["scatto"]["ricarica"] / 2)

        g, stanza = self._stanza("predone")
        g.usa_abilita(stanza)
        self.assertEqual(len(stanza.proiettili), 8)
        self.assertEqual(len({(round(p.direzione.x, 2), round(p.direzione.y, 2))
                              for p in stanza.proiettili}), 8)

        g, stanza = self._stanza("templare")
        vicino = Proiettile(g.pos.x + 60, g.pos.y, pygame.Vector2(-1, 0), 100, 1, 500, True)
        lontano = Proiettile(g.pos.x + 300, g.pos.y, pygame.Vector2(-1, 0), 100, 1, 500, True)
        stanza.proiettili += [vicino, lontano]
        g.usa_abilita(stanza)
        g.subisci_danno(1)
        self.assertEqual((vicino.vivo, lontano.vivo, g.vita), (False, True, g.vita_max))
        self.assertEqual(len(stanza.effetti), 1)

        g, stanza = self._stanza("occultista")
        a = crea_nemico("inseguitore", g.pos.x + 100, g.pos.y)
        b = crea_nemico("inseguitore", g.pos.x + 350, g.pos.y)
        stanza.nemici += [a, b]
        vita_a, vita_b = a.vita, b.vita
        g.usa_abilita(stanza)
        self.assertEqual((a.vita, b.vita), (vita_a - (g.danno * 2 + 1), vita_b))

    def test_51_maestrie(self) -> None:
        """Predone: monete doppie. Templare: un colpo mortale annullato per piano. Occultista: colpi perforanti."""
        import pygame
        from entita import Proiettile
        from nemici import crea_nemico
        from oggetti import Raccoglibile
        for maestria, attese in ((False, 1), (True, 2)):
            g, _ = self._stanza("predone", maestria)
            Raccoglibile("moneta", (0, 0)).raccogli(g)
            self.assertEqual(g.monete, attese)

        g, _ = self._stanza("templare", maestria=True)
        g.vita = 1
        g.subisci_danno(1)
        self.assertEqual((g.vita, g.fede_usata), (1, True))
        g._invulnerabile = 0
        g.subisci_danno(1)
        self.assertLessEqual(g.vita, 0)                   # la seconda volta non salva
        senza, _ = self._stanza("templare")
        senza.vita = 1
        senza.subisci_danno(1)
        self.assertLessEqual(senza.vita, 0)

        for perforante, colpiti in ((False, 1), (True, 2)):
            g, stanza = self._stanza("occultista")
            g.pos.update(300, 150)
            nemici = [crea_nemico("caricatore", 700, 400), crea_nemico("caricatore", 704, 400)]
            for n in nemici:
                n.velocita = 0
                n._timer = 99
            stanza.nemici += nemici
            stanza.proiettili.append(Proiettile(702, 400, pygame.Vector2(1, 0), 0, 1, 500,
                                                perforante=perforante))
            stanza.update(0.001)
            stanza.update(0.001)                          # un colpo perforante non ferisce due volte
            self.assertEqual(sum(n.vita < 4 for n in nemici), colpiti)
            self.assertEqual(sum(4 - n.vita for n in nemici), colpiti)

    def test_52_nemici_piu_difficili(self) -> None:
        """Scalatura per piano, ventaglio del tiratore, carica del ghoul e furia del boss."""
        from nemici import DATI_NEMICI, TIPI_COMUNI, crea_nemico
        for tipo in TIPI_COMUNI:
            base, avanti = crea_nemico(tipo, 0, 0, 1), crea_nemico(tipo, 0, 0, 3)
            self.assertGreater(avanti.vita, base.vita, tipo)
            self.assertGreater(avanti.velocita, base.velocita, tipo)

        for piano, colpi in ((1, 1), (2, 3)):
            g, stanza = self._stanza()
            t = crea_nemico("tiratore", g.pos.x + 300, g.pos.y, piano)
            t._ricarica = 0
            t.update(0.01, stanza)
            self.assertEqual(len(stanza.proiettili), colpi)

        g, stanza = self._stanza()
        c = crea_nemico("caricatore", g.pos.x + 250, g.pos.y)
        c._timer = 0
        c.update(0.01, stanza)
        self.assertTrue(c.avviso)                          # si ferma e avvisa
        x = c.pos.x
        c.update(c.ATTESA, stanza)
        self.assertFalse(c.avviso)
        c.update(0.1, stanza)
        self.assertGreater(x - c.pos.x, 40)                # poi carica verso il giocatore
        c.update(c.DURATA_CARICA, stanza)
        self.assertEqual(c._fase, "avvicina")

        for tipo in ("boss_1", "boss_2", "boss_3"):
            g, stanza = self._stanza()
            g.pos.update(300, 150)
            boss = crea_nemico(tipo, 800, 500, int(tipo[-1]))
            boss.update(0.01, stanza)
            self.assertFalse(boss.furia)
            velocita = boss.velocita
            boss.vita = boss.vita // 2
            boss.update(0.01, stanza)
            self.assertTrue(boss.furia)
            self.assertEqual((len(stanza.rinforzi), len(stanza.effetti)), (2, 1))
            self.assertGreater(boss.velocita, velocita)
            boss.update(0.01, stanza)
            self.assertEqual(len(stanza.rinforzi), 2)      # la furia scatta una volta sola
            boss.update(DATI_NEMICI[tipo]["intervallo"], stanza)
            self.assertGreaterEqual(len(stanza.proiettili), DATI_NEMICI[tipo]["proiettili"])

    def test_53_partita_simulata_senza_errori(self) -> None:
        """Dieci secondi di gioco in ogni stanza dei tre piani, con ogni personaggio, senza errori."""
        from dungeon import NEMICI_MAX, Dungeon, Stanza
        from giocatore import PERSONAGGI, Giocatore
        for piano, chiave in zip((1, 2, 3, 3), PERSONAGGI):
            d = Dungeon(7 + 2 * piano, seed=piano * 11, piano=piano)
            g = Giocatore(*Stanza.AREA.center, chiave)
            g.maestria = True
            for stanza in d.stanze.values():
                stanza.entra(g, d.rng)
                self.assertLessEqual(len(stanza.nemici), NEMICI_MAX)
                for passo in range(600):
                    g.vita = g.vita_max
                    if passo % 120 == 0:
                        g.ricarica_abilita = 0
                        g.usa_abilita(stanza)
                    if passo == 300:
                        for n in stanza.nemici:            # porta il boss in furia
                            n.vita = max(1, n.vita // 2)
                    stanza.update(1 / 60)
                    self.assertTrue(Stanza.AREA.contains(g.rect))


class TestFeedbackAmici(unittest.TestCase):
    """Correzioni dopo le prove degli amici: porte, stanza del boss, sparo e volume."""

    @classmethod
    def setUpClass(cls) -> None:
        """Apre un video finto: Giocatore.update legge lo stato della tastiera."""
        import pygame
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
        pygame.display.init()

    def test_54_soglia_delle_porte(self) -> None:
        """Si cambia stanza andando contro la porta, non sfiorandola lungo il muro."""
        from dungeon import Stanza
        stanza, a = Stanza((0, 0)), Stanza.AREA
        contro_il_muro = a.top + 16                     # centro del giocatore schiacciato in alto
        self.assertTrue(stanza.rect_porta("su").collidepoint(a.centerx, contro_il_muro))
        self.assertTrue(stanza.rect_porta("su").collidepoint(a.centerx + 15, contro_il_muro))
        self.assertFalse(stanza.rect_porta("su").collidepoint(a.centerx + 40, contro_il_muro))
        self.assertFalse(stanza.rect_porta("su").collidepoint(a.centerx, a.top + 40))
        self.assertTrue(stanza.rect_porta("giu").collidepoint(a.centerx, a.bottom - 16))
        self.assertTrue(stanza.rect_porta("sinistra").collidepoint(a.left + 16, a.centery))
        self.assertTrue(stanza.rect_porta("destra").collidepoint(a.right - 16, a.centery))
        self.assertFalse(stanza.rect_porta("destra").collidepoint(a.right - 16, a.centery - 35))

    def test_55_porte_verso_il_boss(self) -> None:
        """Le stanze accanto al boss sanno quale porta porta da lui, e sono disegnate."""
        import pygame
        from dungeon import DIREZIONI, Dungeon
        for seed in range(30):
            d = Dungeon(num_stanze=11, seed=seed, piano=2)
            boss = next(c for c, s in d.stanze.items() if s.ruolo == "boss")
            segnate = [(c, n) for c, s in d.stanze.items() for n in s.verso_boss]
            self.assertTrue(segnate)
            for (x, y), nome in segnate:
                dx, dy = DIREZIONI[nome]
                self.assertEqual((x + dx, y + dy), boss)
                self.assertIn(nome, d.stanze[(x, y)].vicini)
        stanza = d.stanze[segnate[0][0]]
        from grafica import disegna_stanza
        disegna_stanza(pygame.Surface((1280, 720)), stanza, True)

    def test_56_sparo_verso_l_ultima_freccia(self) -> None:
        """Con due frecce premute si spara verso l'ultima premuta (prima vinceva l'orizzontale)."""
        from unittest import mock
        import pygame
        from dungeon import Stanza
        from giocatore import Giocatore

        def tasti(*premuti):
            return mock.patch("pygame.key.get_pressed",
                              return_value=type("T", (), {"__getitem__": lambda s, k: k in premuti})())

        g = Giocatore(*Stanza.AREA.center)
        stanza = Stanza((0, 0))
        with tasti(pygame.K_LEFT):
            g.update(0.01, stanza)
        g._ricarica = 0
        with tasti(pygame.K_LEFT, pygame.K_DOWN):
            g.update(0.01, stanza)
        self.assertEqual(tuple(stanza.proiettili[-1].direzione), (0, 1))
        g._ricarica = 0
        with tasti(pygame.K_LEFT):                      # rilasciata la giu', torna a sinistra
            g.update(0.01, stanza)
        self.assertEqual(tuple(stanza.proiettili[-1].direzione), (-1, 0))

    def test_57_volume_iniziale_basso(self) -> None:
        """All'avvio musica ed effetti partono a volume ridotto."""
        import audio
        self.assertLessEqual(audio.VOLUME_MUSICA, 0.2)
        self.assertLessEqual(audio.VOLUME_EFFETTI, 0.6)


class TestBotolaBilanciamentoCompendio(unittest.TestCase):
    """Botola dopo il boss, bilanciamento di boss e abilita', Compendio delle scoperte."""

    def setUp(self) -> None:
        """Gioco con video e audio finti e una cartella dati temporanea tutta sua."""
        import database
        import salvataggio as sv
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
        os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
        self.temp_dir = Path(tempfile.mkdtemp(prefix="echoes_botola_"))
        self.xdg = os.environ.get("XDG_DATA_HOME")
        os.environ["XDG_DATA_HOME"] = str(self.temp_dir)
        database._db_instance = None
        sv._db = None
        sv._default_profile_id = None

    def tearDown(self) -> None:
        """Chiude il database e rimette la cartella dati di prima."""
        import database
        import salvataggio as sv
        if sv._db is not None:
            sv._db.close()
        if database._db_instance is not None:
            database._db_instance.close()
        database._db_instance = None
        sv._db = None
        sv._default_profile_id = None
        if self.xdg is None:
            os.environ.pop("XDG_DATA_HOME", None)
        else:
            os.environ["XDG_DATA_HOME"] = self.xdg
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _gioco_nella_stanza_del_boss(self, piano: int = 1):
        """Partita al piano indicato, giocatore nella stanza del boss vicino al muro sinistro."""
        from main import Gioco
        gioco = Gioco()
        gioco.nuova_partita(seed=1234)
        if piano > 1:
            gioco.avvia_piano(piano)
        boss = next(s for s in gioco.dungeon.stanze.values() if s.ruolo == "boss")
        gioco.stanza = boss
        gioco.giocatore.pos.update(boss.AREA.left + 40, boss.AREA.centery)
        boss.entra(gioco.giocatore, gioco.dungeon.rng)
        gioco.stanza_salvata = False
        gioco.botola_pronta = False
        return gioco, boss

    def test_58_botola_dopo_il_boss(self) -> None:
        """Battuto il boss si resta nella stanza con il premio a terra; si scende dalla botola."""
        import salvataggio as sv
        gioco, boss = self._gioco_nella_stanza_del_boss()
        boss.nemici[0].furia = True                        # gia' in furia: niente teschi in aiuto
        boss.nemici[0].vita = 0
        gioco.aggiorna(1 / 60)
        self.assertEqual((gioco.piano, gioco.stato), (1, "gioco"))
        self.assertTrue(boss.botola and boss.porte_aperte())
        premio = lambda: sorted(r.tipo for r in boss.raccoglibili if r.tipo != "moneta")
        self.assertEqual(premio(), ["cuore", "passivo"])   # (una moneta puo' cadere a caso)
        self.assertIn("boss_1", sv.get_scoperte().get("nemico", set()))
        gioco.aggiorna(1 / 60)                             # il premio si da' una volta sola
        self.assertEqual(premio(), ["cuore", "passivo"])
        gioco.giocatore.pos.update(boss.rect_botola().center)
        gioco.aggiorna(1 / 60)
        self.assertEqual(gioco.piano, 2)

    def test_59_botola_non_scatta_subito(self) -> None:
        """Se il boss muore mentre si e' sopra la botola, bisogna prima scenderne."""
        gioco, boss = self._gioco_nella_stanza_del_boss()
        gioco.giocatore.pos.update(boss.rect_botola().center)
        boss.nemici.clear()
        for _ in range(3):
            gioco.aggiorna(1 / 60)
        self.assertEqual(gioco.piano, 1)
        gioco.giocatore.pos.update(boss.AREA.left + 40, boss.AREA.centery)
        gioco.aggiorna(1 / 60)
        gioco.giocatore.pos.update(boss.rect_botola().center)
        gioco.aggiorna(1 / 60)
        self.assertEqual(gioco.piano, 2)

    def test_60_ultimo_boss_vince(self) -> None:
        """All'ultimo piano il boss sconfitto chiude la partita con la vittoria."""
        from main import NUM_PIANI
        gioco, boss = self._gioco_nella_stanza_del_boss(NUM_PIANI)
        boss.nemici.clear()
        gioco.aggiorna(1 / 60)
        self.assertEqual((gioco.stato, gioco.vittoria), ("fine", True))

    def test_61_bilanciamento(self) -> None:
        """Boss piu' resistenti, Scatto piu' lento, Scudo piu' breve, Onda arcana a danno fisso."""
        import pygame
        from dungeon import Stanza
        from giocatore import ABILITA, DANNO_ESPLOSIONE, DURATA_SCUDO, Giocatore
        from nemici import DATI_NEMICI, crea_nemico
        pygame.display.init()
        self.assertEqual([DATI_NEMICI[f"boss_{i}"]["vita"] for i in (1, 2, 3)], [50, 85, 125])
        self.assertEqual((ABILITA["scatto"]["ricarica"], DURATA_SCUDO), (3.5, 1.0))
        g = Giocatore(*Stanza.AREA.center, "occultista")
        g.danno = 6                                         # tanti oggetti di danno
        stanza = Stanza((0, 0))
        stanza.giocatore = g
        n = crea_nemico("caricatore", g.pos.x + 80, g.pos.y)
        n.vita = 20
        stanza.nemici.append(n)
        g.usa_abilita(stanza)
        self.assertEqual(n.vita, 20 - DANNO_ESPLOSIONE)

    def test_62_compendio(self) -> None:
        """Scoperte salvate per profilo; il Compendio nasconde cio' che non si conosce."""
        import pygame
        import salvataggio as sv
        from interfaccia import Compendio, descrivi_effetti
        pygame.display.init()
        sv.registra_scoperte("oggetto", ["stivali", "stivali", "caffe"])
        sv.registra_scoperte("nemico", ["teschio_finto"])
        sv.registra_partita(sv.carica(), 1, 10.0, False, 1, ["Armatura antica"], "Viandante", 1)
        scoperte = sv.get_scoperte()
        self.assertEqual(scoperte["oggetto"], {"stivali", "caffe", "armatura"})  # anche dallo storico
        self.assertEqual(descrivi_effetti({"vita_max": 2, "vita": 2, "velocita": -20}),
                         ["Cuori massimi +2", "Velocita' -20"])
        self.assertEqual(descrivi_effetti({"cadenza": -0.08}),
                         ["Tempo tra i colpi -0.08 s (spari piu' spesso)"])
        c = Compendio(scoperte)
        self.assertEqual(c.nome("stivali"), "Stivali veloci")
        self.assertEqual(c.nome("lente"), "???")
        schermo = pygame.Surface((1280, 720))
        destra = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
        giu = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
        for _ in range(3):                                  # tutte le voci di tutte le schede
            for _ in range(len(c._chiavi())):
                c.draw(schermo)
                c.gestisci_evento(giu)
            c.gestisci_evento(destra)
        self.assertEqual(c.scheda, 0)
        c.gestisci_evento(destra)                           # sinergia ignota: indizio con ???
        righe = [r for r, _ in c.dettagli("passo_fuoco")]
        self.assertIn("Richiede: Stivali veloci + ???", righe)


def run_tests() -> None:
    """Esegue tutti i test e riporta risultato."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDatabase)
    suite.addTests(loader.loadTestsFromTestCase(TestNegozio))
    suite.addTests(loader.loadTestsFromTestCase(TestOggetti))
    suite.addTests(loader.loadTestsFromTestCase(TestAudio))
    suite.addTests(loader.loadTestsFromTestCase(TestSeedEInput))
    suite.addTests(loader.loadTestsFromTestCase(TestGrafica))
    suite.addTests(loader.loadTestsFromTestCase(TestPersonaggi))
    suite.addTests(loader.loadTestsFromTestCase(TestSfida))
    suite.addTests(loader.loadTestsFromTestCase(TestFeedbackAmici))
    suite.addTests(loader.loadTestsFromTestCase(TestBotolaBilanciamentoCompendio))
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
