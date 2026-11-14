@echo off
rem Avvia Echoes of the Crypt dai sorgenti: crea l'ambiente virtuale, installa
rem le dipendenze (solo la prima volta) e lancia il gioco. Serve Python 3.12 o successivo.
cd /d "%~dp0"

set PY=python
where py >nul 2>nul && set PY=py -3

%PY% --version >nul 2>nul
if errorlevel 1 (
    echo Python non e' installato.
    echo Scaricalo da https://www.python.org/downloads/ e durante l'installazione
    echo spunta la casella "Add python.exe to PATH". Poi riavvia questo file.
    pause
    exit /b 1
)

if not exist .venv (
    echo Preparo il gioco: la prima volta serve circa un minuto...
    %PY% -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install -q --disable-pip-version-check -r requirements.txt
if errorlevel 1 (
    echo Installazione delle dipendenze non riuscita: controlla la connessione a Internet.
    pause
    exit /b 1
)

python main.py
if errorlevel 1 pause
