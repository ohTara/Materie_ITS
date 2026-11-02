import html
import json
import os
import sqlite3
from contextlib import closing
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

VERSION = "2.0"
TITLE = os.environ.get("APP_TITLE", "Officina Ticket - CSP")
DATA = Path(os.environ.get("DATA_DIR", "/data"))
DB = DATA / "tickets.db"
NOT_READY = Path("/tmp/officina-not-ready")


def query(sql, values=()):
    with closing(sqlite3.connect(DB, timeout=5)) as db:
        with db:
            return db.execute(sql, values).fetchall()


class App(BaseHTTPRequestHandler):
    def reply(self, status, body, content_type="text/html; charset=utf-8"):
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/healthz":
            if NOT_READY.exists():
                return self.reply(503, "Temporaneamente non pronto", "text/plain")
            try:
                query("SELECT COUNT(*) FROM tickets")
            except sqlite3.Error:
                return self.reply(503, "Database non disponibile", "text/plain")
            return self.reply(200, "ok", "text/plain")

        if path not in ("/", "/api/tickets"):
            return self.reply(404, "Risorsa non trovata", "text/plain")

        rows = query("SELECT id, title, done FROM tickets ORDER BY id DESC")
        if path == "/api/tickets":
            data = [{"id": i, "title": t, "done": bool(d)} for i, t, d in rows]
            return self.reply(200, json.dumps(data), "application/json")

        items = []
        for ticket_id, title, done in rows:
            action = "<strong>Risolto</strong>" if done else (
                '<form method="post" action="/done">'
                f'<input type="hidden" name="id" value="{ticket_id}">'
                '<button>Segna risolto</button></form>'
            )
            items.append(
                f"<li><span>#{ticket_id} {html.escape(title)}</span>{action}</li>"
            )
        listing = "".join(items) or "<li>Nessun ticket: aprine uno.</li>"
        page = f"""<!doctype html>
<html lang="it"><meta charset="utf-8"><title>{html.escape(TITLE)}</title>
<style>
body {{ font: 18px system-ui; max-width: 850px; margin: 40px auto; padding: 20px; }}
h1 {{ color: #7b2cbf; }} input {{ padding: 12px; width: 60%; }}
button {{ padding: 12px; cursor: pointer; }} li {{ padding: 16px; background: #edf6fa;
margin: 10px 0; display: flex; justify-content: space-between; gap: 16px; }}
ul {{ padding: 0; }} small {{ color: #555; }}
</style>
<h1>{html.escape(TITLE)}</h1><small>Versione {VERSION}</small>
<form method="post" action="/tickets">
<input name="title" maxlength="120" required placeholder="Nuova richiesta sintetica">
<button>Apri ticket</button></form><ul>{listing}</ul>
<p><a href="/api/tickets">Dati JSON</a> | <a href="/healthz">Controllo disponibilità</a></p>
</html>"""
        self.reply(200, page)

    def do_POST(self):
        path = urlsplit(self.path).path
        if path not in ("/tickets", "/done"):
            return self.reply(404, "Risorsa non trovata", "text/plain")
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return self.reply(400, "Lunghezza non valida", "text/plain")
        if not 0 <= length <= 4096:
            return self.reply(413, "Richiesta troppo grande", "text/plain")
        fields = parse_qs(self.rfile.read(length).decode("utf-8", errors="replace"))
        if path == "/tickets":
            title = fields.get("title", [""])[0].strip()
            if not 1 <= len(title) <= 120:
                return self.reply(400, "Titolo richiesto, massimo 120 caratteri", "text/plain")
            query("INSERT INTO tickets(title, done) VALUES (?, 0)", (title,))
        else:
            try:
                ticket_id = int(fields.get("id", [""])[0])
            except ValueError:
                return self.reply(400, "ID non valido", "text/plain")
            query("UPDATE tickets SET done=1 WHERE id=?", (ticket_id,))
        self.send_response(303)
        self.send_header("Location", "/")
        self.send_header("Content-Length", "0")
        self.end_headers()


if __name__ == "__main__":
    DATA.mkdir(parents=True, exist_ok=True)
    query("CREATE TABLE IF NOT EXISTS tickets "
          "(id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER NOT NULL)")
    print(f"Officina {VERSION} - database {DB}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8000"))), App).serve_forever()