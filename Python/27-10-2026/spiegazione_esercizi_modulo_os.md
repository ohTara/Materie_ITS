# Esercizi sul modulo `os` — Guida di studio

Corso: Cloud Specialist (ITS) · Unità: Programmazione Python · Docente: Massimo Papa
Autore: Luca Tarallo · Data: 27/10/2026

---

## 1. Idea di fondo

Il modulo `os` è il ponte tra Python e il **sistema operativo**. Con `os` il programma può chiedere al SO cose che da terminale faresti a mano: elencare cartelle (`ls`/`dir`), cancellare file (`rm`/`del`), lanciare comandi.

Questo collega direttamente Python agli **script di automazione** che userai in Linux, Docker, CI/CD e cloud: spesso uno script fa proprio questo (cerca file, pulisce cartelle, lancia comandi).

```python
import os   # va sempre importato prima dell'uso
```

---

## 2. Le funzioni che servono (cheat sheet)

| Funzione | Cosa fa | Restituisce |
|---|---|---|
| `os.listdir(p)` | Elenca i **nomi** contenuti in `p` (file e cartelle mischiati) | `list[str]` |
| `os.path.join(a, b)` | Unisce due parti di percorso col separatore giusto del SO (`/` o `\`) | `str` |
| `os.path.isdir(p)` | `True` se `p` esiste ed è una directory | `bool` |
| `os.path.isfile(p)` | `True` se `p` esiste ed è un file | `bool` |
| `os.remove(p)` | Elimina il file `p` (**irreversibile**, niente cestino) | `None` |
| `os.system(cmd)` | Esegue `cmd` nella shell del SO | `int` (esito) |

### Il punto che sbagliano quasi tutti

`os.listdir()` restituisce **solo i nomi**, non i percorsi completi. Se fai `os.path.isfile("x.txt")` Python cerca `x.txt` nella cartella **da cui lanci il programma**, non in quella che stai esaminando. Per questo il codice fa sempre:

```python
completo = os.path.join(percorso, nome)   # percorso completo
os.path.isfile(completo)                  # ora il controllo è sul file giusto
```

> Senza `join`, il programma funziona solo per caso quando lo lanci dalla cartella esaminata, e dà risultati sbagliati (o `False` silenziosi) altrimenti.

---

## 3. Come ragionare su ogni esercizio (metodo del docente)

Per ogni problema: **input → output → sottoproblemi → una funzione per sottoproblema → programma principale che le richiama.**

Struttura di ogni file:

1. Intestazione (autore, data, titolo)
2. Funzioni, ognuna con commento: parametri formali e valore di ritorno
3. Programma principale: input → inizializzazioni → elaborazione → output

Vantaggio: ogni funzione fa **una cosa sola** e si può testare da sola.

---

## 4. Esercizio 1 — Elencare le directory di un percorso

**Traccia:** dato un percorso, elencare tutte le directory presenti.

- **Input:** un percorso (`str`)
- **Output:** i nomi delle sottodirectory
- **Sottoproblema:** "dato un percorso, dammi solo le directory" → funzione `elenca_directory`

**Ragionamento:** `os.listdir` mischia file e cartelle, quindi per ogni nome devo chiedere "sei una directory?" con `os.path.isdir` (sul percorso completo).

```python
def elenca_directory(percorso: str) -> list:
    directories = []
    for nome in os.listdir(percorso):
        if os.path.isdir(os.path.join(percorso, nome)):
            directories.append(nome)
    return directories
```

**Pattern:** *filtro* = scorro una lista, tengo solo gli elementi che soddisfano una condizione. Lo ritroverai ovunque.

**Casi limite gestiti:** percorso inesistente o che non è una cartella (controllato con `isdir`), nessuna sottodirectory, permessi insufficienti (`PermissionError`).

Equivalente da terminale Linux: `ls -d */`

---

## 5. Esercizio 2 — Contare i file con una data estensione

**Traccia:** esaminare le directory sotto un percorso e contare i file con una certa estensione (per ora solo primo livello).

- **Input:** percorso, estensione
- **Output:** conteggio per ogni sottodirectory + totale
- **Sottoproblemi:**
  1. `normalizza_estensione` → rende uguali `txt`, `.TXT`, `.txt`
  2. `conta_file_in_directory` → conta in **una** cartella
  3. `conta_in_sottodirectory` → ripete (2) per ogni sottocartella

**Ragionamento sulla normalizzazione:** l'utente può scrivere l'estensione in mille modi. Meglio ridurla a una forma unica (minuscola, col punto) prima di confrontare. Principio generale: **normalizza l'input all'ingresso**, così il resto del codice è semplice.

**Struttura a due livelli:**

```
percorso/
├── a/        ← conta i .txt qui dentro
│   ├── x.txt
│   └── y.TXT
├── b/        ← e qui dentro
│   └── z.txt
└── keep.txt  ← NON contato (è nel percorso base, non in una sottodirectory)
```

> **Scelta interpretativa:** la traccia dice "directories sotto un dato percorso", quindi ho contato solo i file *dentro le sottodirectory* di primo livello. Se il docente volesse contare anche i file del percorso base, basta chiamare `conta_file_in_directory(percorso, ext)` una volta in più.

**Dettagli di codice da capire:**
- `nome.lower().endswith(estensione)` → confronto senza distinzione maiuscole/minuscole
- Il risultato è un **dizionario** `{nome_sottodirectory: conteggio}`, e `sum(dict.values())` dà il totale
- `try/except PermissionError` → una cartella non leggibile non fa crashare tutto

**Possibile evoluzione (senza limite di profondità):** `os.walk(percorso)`, che visita ricorsivamente tutte le sottocartelle. Da studiare come passo successivo.

---

## 6. Esercizio 3 — Eseguire un comando del SO

**Traccia:** eseguire un comando del sistema operativo con il modulo `os`.

- **Input:** il comando (`str`)
- **Output:** l'output del comando (a video) e il codice di ritorno

```python
def esegui_comando(comando: str) -> int:
    codice = os.system(comando)
    return codice
```

**Come funziona:** `os.system` avvia una shell (`cmd.exe` su Windows, `sh`/`bash` su Linux), le passa la stringa e aspetta che finisca. L'output del comando va **direttamente nel terminale**: Python non lo cattura.

**Codice di ritorno:**
- `0` = successo, diverso da `0` = errore (convenzione universale dei SO, la stessa di `$?` in Bash)
- Su Linux/macOS `os.system` restituisce lo *status codificato*: il vero codice di uscita è `status >> 8`

**Comandi dipendenti dal SO:** `dir` funziona su Windows, `ls -l` su Linux. Provare un comando che non esiste mostra un codice ≠ 0.

### ⚠️ Sicurezza (importante per il cloud)

`os.system` passa la stringa **intera** alla shell. Se la stringa contiene input di un utente esterno, questi può aggiungere comandi (`; rm -rf ...`). Questo si chiama **command injection** ed è una vulnerabilità classica.

- Va bene qui: l'input è tuo e lo digiti tu.
- Nel codice "vero": usare `subprocess.run([...lista di argomenti...])`, che non passa dalla shell. È il modulo consigliato oggi e lo incontrerai negli script DevOps.

---

## 7. Esercizio 4 — Eliminare file per sequenza nel nome

**Traccia:** eliminare tutti i file che contengono nel nome una sequenza di caratteri data.

- **Input:** percorso, sequenza
- **Output:** numero di file eliminati
- **Sottoproblemi:**
  1. `trova_file` → *quali* file corrispondono (non cancella nulla)
  2. `elimina_file` → cancella la lista ricevuta

**Perché separare "trova" da "elimina"?** Così posso **mostrare l'elenco all'utente prima** di cancellare. Cancellare è irreversibile: prima si guarda, poi si conferma. È un principio di sicurezza che userai anche con `terraform plan` → `apply` o `kubectl --dry-run`.

**Le tre protezioni nel codice:**

1. **Sequenza vuota rifiutata.** In Python `"" in "qualsiasi"` è `True`: una sequenza vuota combacia con *ogni* nome e cancellerebbe tutta la cartella. Caso limite pericoloso.
2. **Conferma esplicita** (`s`) prima di eliminare. Qualsiasi altra risposta annulla.
3. **`try/except OSError`** su ogni file: se uno non si può cancellare (aperto, permessi), il programma lo segnala e continua con gli altri.

```python
if os.path.isfile(completo) and sequenza in nome:
```

- `isfile` evita di tentare di cancellare cartelle (`os.remove` funziona solo sui file)
- `sequenza in nome` distingue maiuscole/minuscole: `"TMP"` non combacia con `"tmp"`

Equivalente da terminale Linux: `rm *tmp*` (in `find` + `-delete` per più livelli).

---

## 8. Errori tipici da evitare

| Errore | Conseguenza | Come evitarlo |
|---|---|---|
| Usare `nome` invece di `join(percorso, nome)` | Risultati sbagliati se lanci da altra cartella | Costruire sempre il percorso completo |
| Non controllare che il percorso esista | `FileNotFoundError` | `os.path.isdir()` prima |
| Confrontare estensioni senza normalizzare | `.TXT` non trovato | `.lower()` e punto iniziale |
| Cancellare senza anteprima | Perdita dati irreversibile | Trovare → mostrare → confermare |
| `os.system` con input non fidato | Command injection | Usare `subprocess.run` con lista |

---

## 9. Come testare (richiesto dalla traccia: "anche i casi limite")

Crea una cartella di prova **fuori** dai tuoi appunti:

```
prova/
├── a/ (x.txt, y.TXT)
├── b/ (z.txt, w.log)
├── rootfile_tmp.txt
└── keep.txt
```

Casi da provare:

- Percorso inesistente → messaggio di errore, nessun crash
- Cartella senza sottodirectory → "Nessuna directory presente"
- Estensione in più formati (`txt`, `.txt`, `TXT`) → stesso risultato
- Estensione che non esiste → conteggio 0
- Sequenza vuota nell'es. 4 → rifiutata
- Sequenza che non combacia → "Nessun file corrispondente"
- Risposta `n` alla conferma → nessun file eliminato

> **Non testare mai l'esercizio 4 su cartelle con dati importanti.** Usa solo la cartella di prova.

---

## 10. Domande di richiamo (rispondi prima di guardare le soluzioni)

1. Cosa restituisce `os.listdir()`: nomi o percorsi completi? Cosa succede se passi solo il nome a `os.path.isfile` da una cartella diversa?
2. Perché `"" in "file.txt"` è un caso pericoloso nell'esercizio 4?
3. Che differenza c'è tra `os.path.isfile` e `os.path.isdir`? Perché servono entrambe?
4. Perché separare `trova_file` da `elimina_file`?
5. Cos'è la command injection e come la eviteresti al posto di `os.system`?
6. Come modificheresti l'esercizio 2 per contare anche nelle sottocartelle di secondo livello? (Suggerimento: cerca `os.walk`.)

<details>
<summary>Risposte brevi</summary>

1. Solo nomi. Python cerca quel nome nella directory di lavoro corrente, quindi può dare `False` anche se il file esiste altrove.
2. La stringa vuota è contenuta in ogni stringa: combacerebbe con tutti i file.
3. `isfile` è vero solo per i file, `isdir` solo per le cartelle; `listdir` le mescola, quindi serve distinguerle.
4. Per poter mostrare l'anteprima e chiedere conferma prima di un'azione irreversibile.
5. Iniezione di comandi extra tramite input non fidato; si evita con `subprocess.run([...])` senza passare dalla shell.
6. Con `os.walk(percorso)`, che attraversa ricorsivamente tutte le sottodirectory.

</details>

---

## 11. Collegamenti con il resto del corso

- **Linux/Bash:** `listdir` ≈ `ls`, `remove` ≈ `rm`, `system` ≈ lanciare un comando; `0`/non-`0` ≈ `$?`
- **Docker/CI-CD:** gli stessi pattern (cerca file, pulisci artefatti, lancia comandi) compaiono negli script di build e deploy
- **Sicurezza:** command injection, conferma prima di azioni distruttive, principio del minimo privilegio
- **Terraform:** `plan` prima di `apply` è lo stesso principio di "trova prima, elimina dopo"
