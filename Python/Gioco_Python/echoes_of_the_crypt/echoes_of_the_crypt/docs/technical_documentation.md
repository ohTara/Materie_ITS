# Documentazione Tecnica - Echoes of the Crypt

**Progetto d'esame ITS Cloud Specialist**  
**Studente:** Luca Tarallo  
**Data:** 27/11/2026  
**Repository:** ohTara/Materie_ITS (submodule modulo-omnia-system)

---

## Indice

- [a) Architettura e Struttura del Progetto](#a-architettura-e-struttura-del-progetto)
- [b) Generazione Procedurale Dungeon](#b-generazione-procedurale-dungeon)
- [c) Sistema Entità e Hitbox Forgiving](#c-sistema-entità-e-hitbox-forgiving)
- [d) Trappole Animate e State Machine](#d-trappole-animate-e-state-machine)
- [e) Sistema Salvataggio (SQLite)](#e-sistema-salvataggio-sqlite)
- [f) Build Cross-Platform e CI/CD](#f-build-cross-platform-e-cicd)

---

## a) Architettura e Struttura del Progetto

### Panoramica Generale

**Echoes of the Crypt** è un dungeon crawler roguelike sviluppato in **Python 3.11+** con **pygame-ce 2.5.8** (SDL 2.32.10). Il gioco implementa un ciclo di gioco completo con generazione procedurale, sistema di progressione a personaggi sbloccabili, inventario con sinergie, e persistenza dati su SQLite.

### Struttura Modulare

```
echoes_of_the_crypt/
├── main.py              # Game loop, state machine, input handling
├── entita.py            # Classe base Entita + Proiettile (ABC)
├── giocatore.py         # Giocatore, personaggi, abilità, maestrie
├── nemici.py            # Nemici comuni, boss, AI comportamentale
├── dungeon.py           # Generazione piano (random walk), stanze, ostacoli, trappole
├── grafica.py           # Rendering: sprite pixel-art, luci, buio, trappole animate, debug hitbox
├── interfaccia.py       # Menu, HUD, compendio, impostazioni, campi testo
├── oggetti.py           # Oggetti passivi/attivi, sinergie, raccoglibili, negozio
├── audio.py             # Sintesi suoni (nessun asset esterno), musica procedurale
├── salvataggio.py       # API compatibilità JSON → SQLite
├── database.py          # Schema SQLite, migrazioni, profili, checkpoint, leaderboard
├── test_verifica.py     # 62 test automatizzati (pytest)
├── impostazioni.json    # Persistenza video/accessibilità
├── build.spec           # Config PyInstaller
└── .github/workflows/   # CI/CD matrix build Windows/Linux
```

### Design Patterns Utilizzati

| Pattern | Applicazione |
|---------|--------------|
| **State Machine** | `Gioco.stato`: menu, gioco, pausa, personaggio, input, tabella, profili |
| **Template Method** | `Entita.update()` astratto → `Giocatore.update()`, `Nemico.update()`, `Proiettile.update()` |
| **Component-like** | Hitbox configurabile (`hitbox_moltiplicatore`, `hitbox_offset_y`) separata da sprite |
| **Factory** | `crea_nemico(tipo, x, y, piano)` in `nemici.py` |
| **Observer (leggero)** | `avvisi` lista nel giocatore per messaggi UI one-shot |
| **Deterministic RNG** | `random.Random(seed)` per generazione riproducibile (condivisibile via seed) |

### Ciclo di Gioco Principale (`main.py:Gioco.run`)

```python
while self.in_esecuzione:
    dt = self.clock.tick(FPS) / 1000.0
    self._gestisci_eventi()      # Input → transizioni stato
    if self.stato == "gioco":
        self._aggiorna_gioco(dt) # Update entità, collisioni, transizioni stanza
    self._disegna()              # Render stato corrente
    pygame.display.flip()
```

**Stati principali:** `menu`, `gioco`, `pausa`, `personaggio`, `input`, `tabella`, `profili`, `impostazioni`, `aiuto`, `compendio`, `negozio`, `vittoria`, `gameover`.

---

## b) Generazione Procedurale Dungeon

### Algoritmo: Random Walk su Griglia

**File:** `dungeon.py:Dungeon.__init__` (righe ~320-400)

```python
def __init__(self, num_stanze: int, seed: int | None, piano: int):
    rng = random.Random(seed)
    self.griglia = {}                    # (x, y) -> Stanza
    self.stanze_ordinate = []            # lista per ordine visita
    # 1. Stanza iniziale a (0, 0)
    # 2. Random walk: da ogni stanza, tenta direzioni casuali
    # 3. Se cella libera → nuova stanza, collega porte bidirezionali
    # 4. Ripeti finché num_stanze raggiunto
    # 5. Scegli stanza boss: la più lontana (Manhattan) da (0,0)
    # 6. Marca percorso verso boss (verso_boss set su porte)
    # 7. Assegna ruoli: iniziale, boss, tesoro, negozio (2 per piano), normali
```

**Caratteristiche:**
- **Seed deterministico:** stesso seed = stesso dungeon (condivisibile tra giocatori)
- **Connettività garantita:** ogni stanza raggiungibile, grafo connesso
- **Scalabilità:** `num_stanze = 7 + 2 * piano` (piano 1: 9, piano 2: 11, piano 3: 13)
- **Boss placement:** stanza più distante → progressione naturale

### Tilemap Occupancy Grid (Anti-Sovrapposizione)

**File:** `dungeon.py:Stanza._genera_ostacoli` (righe ~114-288)

Sistema a **griglia 32×32 pixel** per posizionamento collision-free:

```python
TILE = 32
grid_w = a.width // TILE + 2
grid_h = a.height // TILE + 2
occupato = [[False] * grid_h for _ in range(grid_w)]

def marca_occupato(rect, margine=0):
    r = rect.inflate(margine * 2, margine * 2)
    gx1, gy1 = world_to_grid(r.left, r.top)
    gx2, gy2 = world_to_grid(r.right, r.bottom)
    for gx in range(max(0, gx1), min(grid_w, gx2 + 1)):
        for gy in range(max(0, gy1), min(grid_h, gy2 + 1)):
            occupato[gx][gy] = True

def e_libero(rect, margine=0) -> bool:
    # controlla tutte le tile coperte dal rect
```

**Safe Zones (raggio 120px):**
- Centro stanza (spawn giocatore) → mai ostacoli/trappole
- Porte (area 160×160 attorno a ogni porta) → passaggi sempre liberi

### Varietà Contenuti per Piano

| Elemento | Piano 1 | Piano 2 | Piano 3+ |
|----------|---------|---------|----------|
| **Ostacoli** | 3-5 base | +1 ogni 2 piani | 7 tipi: pilastro, roccia, sarcofago, statua, pozzo, **barile**, **pilastro_rotto** |
| **Trappole** | Nessuna | 1-3 + scaling | 7 tipi: **spike** (3 fasi), fuoco, veleno, buco, **acido**, **esplosivo**, **elettrica** |
| **Nemici** | 3-5 + piano-1 | Fino a 8 max | Scaling vita/danno + nuovi tipi boss |

---

## c) Sistema Entità e Hitbox Forgiving

### Classe Base `Entita` (`entita.py:11-172`)

```python
class Entita(ABC):
    def __init__(self, x, y, dimensione, velocita, vita, colore,
                 hitbox_moltiplicatore=1.0, hitbox_offset_y=0):
        self.pos = pygame.Vector2(x, y)      # Centro logico
        self.dimensione = dimensione         # Dimensione SPRITE (quadrato)
        self._hitbox_moltiplicatore = clamp(hitbox_moltiplicatore, 0.1, 2.0)
        self._hitbox_offset_y = hitbox_offset_y  # Offset verticale (px, + = giù)

    @property
    def rect(self) -> pygame.Rect:           # HITBOX per collisioni
        hit_w = int(self.dimensione * self._hitbox_moltiplicatore)
        hit_h = int(self.dimensione * self._hitbox_moltiplicatore)
        r = pygame.Rect(0, 0, hit_w, hit_h)
        r.centerx = round(self.pos.x)
        r.centery = round(self.pos.y) + self._hitbox_offset_y
        return r

    @property
    def rect_sprite(self) -> pygame.Rect:    # SPRITE per rendering
        r = pygame.Rect(0, 0, self.dimensione, self.dimensione)
        r.center = (round(self.pos.x), round(self.pos.y))
        return r
```

### Hitbox Forgiving - Giocatore (`giocatore.py:119-120`)

```python
super().__init__(x, y, 32, p["velocita"], p["vita"], p["tinta"],
                 hitbox_moltiplicatore=0.70, hitbox_offset_y=6)
```

| Parametro | Valore | Effetto |
|-----------|--------|---------|
| `dimensione` | 32px | Sprite 32×32 |
| `hitbox_moltiplicatore` | 0.70 | Hitbox 22×22 (70%) |
| `hitbox_offset_y` | +6px | Hitbox centrata sui **piedi** |

**Risultato:** Il giocatore può "sfiorare" nemici/proiettili con la parte alta dello sprite (testa/spalle) senza subire danno → percezione equità, riduzione frustrazione.

### Clamp Movimento con Offset (`entita.py:93-114`)

```python
def muovi(self, direzione, dt, limiti, ostacoli=None):
    hit_w = int(self.dimensione * self._hitbox_moltiplicatore)
    hit_h = int(self.dimensione * self._hitbox_moltiplicatore)
    metà_w, metà_h = hit_w / 2, hit_h / 2
    
    # Clamp considera offset_y: hitbox non esce dall'AREA
    nuova_pos.x = max(limiti.left + metà_w, min(limiti.right - metà_w, nuova_pos.x))
    nuova_pos.y = max(limiti.top + metà_h - self._hitbox_offset_y,
                      min(limiti.bottom - metà_h - self._hitbox_offset_y, nuova_pos.y))
```

**Fix critico (test_53):** Il clamp Y usa `- offset_y` per top e `- offset_y` per bottom (non `+`), perché offset positivo sposta hitbox **verso il basso** → il bordo superiore dell'hitbox sale, quello inferiore scende.

### Debug Hitbox (F3/H) - `entita.py:14-16, 67-76` + `grafica.py:677-739`

```python
# Toggle class-level
@classmethod
def toggle_debug_hitbox(cls) -> bool:
    cls._debug_hitbox = not cls._debug_hitbox
    return cls._debug_hitbox
```

**Colori debug:**
- 🟢 Verde: Player hitbox
- 🟢 Chiaro: Player sprite rect
- 🔴 Rosso: Nemici hitbox
- 🟡 Giallo: Proiettili ostili
- 🟦 Ciano: Proiettili player
- 🟠 Arancione: Ostacoli
- 🟣 Magenta: Trappole hitbox + rect_visivo
- 🔵 Blu: Porte
- ⚪ Bianco: Raccolgibili

---

## d) Trappole Animate e State Machine

### Architettura Trappole (`dungeon.py:233-288` + `grafica.py:452-606`)

**Struttura dati trappola:**
```python
trappola = {
    "rect": pygame.Rect,           # Hitbox collisione (con margine -4px)
    "rect_visivo": pygame.Rect,    # Area rendering (dimensione piena)
    "tipo": "spike"|"fuoco"|"veleno"|"buco"|"acido"|"esplosivo"|"elettrica",
    "cooldown": float,             # Ciclo completo (secondi)
    "danno": int,
    "timer": 0.0,                  # Timer interno
    "attiva": bool,                # Fase attiva corrente
    "raggio": int,                 # Raggio visivo
    "hitbox_raggio": int,          # Raggio hitbox (raggio - 4)
    # Spike-specific:
    "fase": 0|1|2,                 # 0=inattiva, 1=telegraph, 2=attiva
    "telegraph_durata": 0.6,
    "attiva_durata": 0.5,
    # Pozze (veleno/acido):
    "tick_timer": 0.0,
    "tick_cooldown": 0.5,
}
```

### State Machine: Spike (3 Fasi) - `dungeon.py:276-280` + `Stanza.update`

```python
def update_trappole(self, dt):
    for t in self.trappole:
        t["timer"] += dt
        if t["tipo"] == "spike":
            fase = t["fase"]
            if fase == 0:                          # INATTIVA
                if t["timer"] >= t["cooldown"]:
                    t["fase"] = 1
                    t["timer"] = 0
            elif fase == 1:                        # TELEGRAPH (preavviso)
                if t["timer"] >= t["telegraph_durata"]:
                    t["fase"] = 2
                    t["timer"] = 0
                    # INFLIGGE DANNO QUI se player in hitbox
            elif fase == 2:                        # ATTIVA (punte fuori)
                if t["timer"] >= t["attiva_durata"]:
                    t["fase"] = 0
                    t["timer"] = 0
```

**Timing spike (cooldown 2.0s):**
- **0.0–1.4s:** Inattiva (piastra visibile, fori)
- **1.4–2.0s:** Telegraph (punte semi-estratte, lampeggio arancione, **0.6s**)
- **2.0–2.5s:** Attiva (punte rosse estratte, danno, **0.5s**)
- **2.5–4.0s:** Ciclo ripetuto

### Rendering Animato (`grafica.py:disegna_trappole`)

**Deterministic PRNG per animazioni coerenti:**
```python
def _rng_trappola(trappola, tempo: float, seed_offset: int) -> int:
    x, y = trappola.get("rect_visivo", trappola["rect"]).center
    seed = int((int(x) * 73856093 + int(y) * 19349663 + 
                int(tempo * 1000) + seed_offset * 83492791) & 0x7fffffff)
    return (seed * 1103515245 + 12345) & 0x7fffffff  # LCG
```

**Effetti per tipo:**

| Tipo | Animazione | Danno |
|------|------------|-------|
| **Spike** | 3 fasi visive distinte (piastra → telegraph arancione → punte rosse) | 1 (istante fase 2) |
| **Fuoco** | Fiamme tremolanti + scintille casuali | 1 (contatto) |
| **Veleno** | Pozza verde, bolle sinusoidali, danno periodico 0.5s | 1/tick |
| **Buco** | Profondità a strati (4 livelli scuri), centro nero, riflesso bordo | 1 + knockback |
| **Acido** | Bolle rapide, schiuma, bordi sfrangiati giallo-verdi | 1/tick (0.5s) |
| **Esplosivo** | Base grigia, simbolo !, linee irradianti arancioni | 2 (esplosione) |
| **Elettrica** | Archi blu rotanti + rami casuali | 1 (contatto) |

### Integrazione Collisioni (`main.py:_aggiorna_gioco`)

```python
# Trappole spike: danno istantaneo in fase 2
for t in stanza.trappole:
    if t["tipo"] == "spike" and t["fase"] == 2:
        if giocatore.rect.colliderect(t["rect"]):
            giocatore.subisci_danno(t["danno"], knockback_dir)

# Pozze (veleno/acido): danno periodico
elif t["tipo"] in ("veleno", "acido"):
    if giocatore.rect.colliderect(t["rect"]):
        t["tick_timer"] += dt
        if t["tick_timer"] >= t["tick_cooldown"]:
            giocatore.subisci_danno(t["danno"])
            t["tick_timer"] = 0
```

---

## e) Sistema Salvataggio (SQLite)

### Schema Database (`database.py:1-150`)

```sql
-- Profili giocatore
CREATE TABLE profili (
    id INTEGER PRIMARY KEY,
    nome TEXT UNIQUE NOT NULL,
    creato_il TEXT DEFAULT (datetime('now')),
    ultima_partita TEXT,
    partite INTEGER DEFAULT 0,
    vittorie INTEGER DEFAULT 0,
    piano_record INTEGER DEFAULT 0,
    tempo_record REAL,
    seed_record TEXT
);

-- Statistiche per profilo (chiave-valore flessibile)
CREATE TABLE statistiche (
    profilo_id INTEGER REFERENCES profili(id) ON DELETE CASCADE,
    chiave TEXT NOT NULL,
    valore TEXT NOT NULL,
    PRIMARY KEY (profilo_id, chiave)
);

-- Checkpoint per ripresa partita
CREATE TABLE checkpoint (
    profilo_id INTEGER PRIMARY KEY REFERENCES profili(id) ON DELETE CASCADE,
    dati BLOB NOT NULL,           -- JSON serializzato
    aggiornato_il TEXT DEFAULT (datetime('now'))
);

-- Storico partite (leaderboard)
CREATE TABLE storico (
    id INTEGER PRIMARY KEY,
    profilo_id INTEGER REFERENCES profili(id) ON DELETE CASCADE,
    data_utc TEXT NOT NULL,
    data_locale TEXT NOT NULL,
    vittoria INTEGER NOT NULL,
    piano_raggiunto INTEGER NOT NULL,
    tempo REAL NOT NULL,
    nemici_uccisi INTEGER NOT NULL,
    oggetti_raccolti TEXT NOT NULL,  -- JSON array
    personaggio TEXT,
    seed_partita INTEGER,
    UNIQUE(profilo_id, data_utc)
);
```

### Migrazione Automatica JSON → SQLite (`database.py:180-280`)

```python
def _migra_da_json(self, conn):
    """Esegue una sola volta al primo avvio su DB vuoto."""
    # 1. Legge vecchi file: profilo.json, stats_<nome>.json, checkpoint_<nome>.json
    # 2. Inserisce in profili, statistiche, checkpoint
    # 3. Crea backup .bak dei file JSON originali
    # 4. Imposta flag migrazione_eseguita = 1
```

### API Compatibilità (`salvataggio.py`)

Mantiene **retrocompatibilità** con codice esistente:

```python
def carica() -> dict:                    # → statistiche profilo corrente
def salva(dati: dict) -> None:           # → statistiche profilo corrente
def esiste_partita() -> bool:            # → checkpoint exists
def carica_partita() -> dict | None:     # → checkpoint data
def salva_partita(dati: dict) -> None:   # → checkpoint upsert
def elimina_partita() -> None:           # → delete checkpoint
def get_leaderboard(limit=10) -> list:   # → storico vittorie ordinate tempo
def get_storico(limit=10) -> list:       # → ultime partite profilo
def registra_scoperte(tipo, chiavi) -> None:  # → statistiche (compendio)
```

### Checkpoint Struttura (`main.py:registra_checkpoint`)

```python
checkpoint = {
    "piano": self.piano,
    "seed_partita": self.seed_partita,
    "tempo": self.tempo,
    "giocatore": self.giocatore.a_dict(),
    "dungeon_seed": self.dungeon.seed if hasattr(self.dungeon, 'seed') else None,
    "stanza_corrente": self.dungeon.stanze_ordinate.index(stanza_corrente) if stanza_corrente in self.dungeon.stanze_ordinate else 0,
    "stanze_visitate": [s.coord for s in self.dungeon.stanze_ordinate if s.visitata],
}
salvataggio.salva_partita(checkpoint)
```

**Ripristino esatto:** Stesso seed → stesso dungeon → stessa stanza → stesse statistiche.

---

## f) Build Cross-Platform e CI/CD

### PyInstaller Configuration (`build.spec`)

```python
# build.spec
block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('impostazioni.json', '.'),
        ('database.py', '.'),
    ],
    hiddenimports=[
        'pygame', 'pygame._sdl2', 'sqlite3', 'json', 'random', 'math',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'test', 'unittest'],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz, a.scripts, a.binaries, a.zipfiles, a.datas,
    [],
    name='EchoesOfTheCrypt',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,        # Finestra GUI, no console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)
```

**Build commands:**
```bash
# Linux
pyinstaller --clean build.spec

# Windows (cross-compile non supportato → build nativo su Windows)
pyinstaller --clean build.spec
```

### GitHub Actions Matrix Build (`.github/workflows/build.yml`)

```yaml
name: Build Releases

on:
  push:
    tags:
      - 'echoes-v*'

jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ['3.11', '3.12']
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies (Linux)
        if: runner.os == 'Linux'
        run: |
          sudo apt-get update && sudo apt-get install -y \
            libsdl2-dev libsdl2-mixer-dev libfreetype6-dev \
            libpng-dev libjpeg-dev portaudio19-dev
          pip install pygame-ce
      
      - name: Install dependencies (Windows)
        if: runner.os == 'Windows'
        run: pip install pygame-ce
      
      - name: Install PyInstaller
        run: pip install pyinstaller
      
      - name: Build
        run: pyinstaller --clean build.spec
        working-directory: ./Python/Gioco_Python/echoes_of_the_crypt/echoes_of_the_crypt
      
      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: EchoesOfTheCrypt-${{ matrix.os }}-py${{ matrix.python-version }}
          path: |
            ./Python/Gioco_Python/echoes_of_the_crypt/echoes_of_the_crypt/dist/EchoesOfTheCrypt*
            ./Python/Gioco_Python/echoes_of_the_crypt/echoes_of_the_crypt/dist/EchoesOfTheCrypt.exe
      
      - name: Create Release
        if: startsWith(github.ref, 'refs/tags/')
        uses: softprops/action-gh-release@v1
        with:
          files: |
            ./Python/Gioco_Python/echoes_of_the_crypt/echoes_of_the_crypt/dist/EchoesOfTheCrypt*
            ./Python/Gioco_Python/echoes_of_the_crypt/echoes_of_the_crypt/dist/EchoesOfTheCrypt.exe
          generate_release_notes: true
```

### Output Atteso

| Piattaforma | Artifact | Note |
|-------------|----------|------|
| **Linux** | `EchoesOfTheCrypt` (ELF 64-bit) | `./EchoesOfTheCrypt` |
| **Windows** | `EchoesOfTheCrypt.exe` (PE32+) | Double-click to run |

**Dipendenze incluse:** Python interpreter, pygame-ce, SDL2, stdlib (sqlite3, json, etc.) → **Zero dipendenze esterne** per l'utente finale.

### Verifica Build Locale

```bash
# Test rapido build
cd echoes_of_the_crypt
pyinstaller --clean build.spec
./dist/EchoesOfTheCrypt  # Linux
# oppure
dist/EchoesOfTheCrypt.exe  # Windows
```

---

## Conclusione

**Echoes of the Crypt** dimostra competenze trasversali:

| Area | Tecnologie/Concetti |
|------|---------------------|
| **Programmazione** | Python OOP, ABC, type hints, design patterns |
| **Game Dev** | Game loop, state machine, procedural generation, collision detection, particle systems |
| **Graphics** | Pixel-art procedurale, lighting system (darkness mask), animation state machines |
| **Data** | SQLite, migrazioni, serializzazione JSON, checkpoint system |
| **DevOps** | PyInstaller, GitHub Actions matrix, cross-platform builds, semantic versioning |
| **Testing** | 62 test pytest (database, gameplay, graphics, audio, balance) |
| **Accessibilità** | Riduzione effetti, daltonici, testo grande, impostazioni persistenti |

Il progetto è **pronto per la consegna d'esame** (scadenza 27/11/2026) con:
- ✅ Tutti i 62 test passano
- ✅ Build cross-platform configurata
- ✅ Documentazione tecnica completa
- ✅ Tag `echoes-v1.5` pronto per push