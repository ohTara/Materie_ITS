#!/usr/bin/env bash
# Crea (se serve) il venv, installa le dipendenze e avvia il gioco.
cd "$(dirname "$0")"
[ -d .venv ] || python3 -m venv .venv
. .venv/bin/activate
pip install -q -r requirements.txt
python main.py
