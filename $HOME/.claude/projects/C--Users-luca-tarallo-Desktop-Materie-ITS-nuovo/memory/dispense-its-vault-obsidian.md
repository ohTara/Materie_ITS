---
name: dispense-its-vault-obsidian
description: Dispense ITS in un vault Obsidian (_Dispensa_Completa = repo privata ohTara/Dispense_ITS): convenzioni concordate, metodo di lavoro e dove leggere lo stato di avanzamento
metadata:
  type: project
---

Dal 16/11/2026 Luca fa generare una dispensa di studio completa per ogni materia di `Materie_ITS_nuovo`, in formato Obsidian, da leggere anche sul telefono senza pagare Obsidian Sync.

- **Vault:** `Materie_ITS_nuovo/_Dispensa_Completa/` è il clone di `https://github.com/ohTara/Dispense_ITS.git` (privata, branch `main`), ignorato dalla repo principale con il `.gitignore`. Sul telefono: Obsidian + plugin Git (HTTPS + token fine-grained limitato alla repo).
- **Struttura:** `00 - Indice Generale ITS (MOC).md` nella radice, con la tabella delle materie e il loro stato (fa da registro di avanzamento). Una cartella per materia (es. `AWS/`) con `00 - Indice <Materia> (MOC)`, i moduli `NN - <nome>` e `99 - Glossario, Comandi e Cheat Sheet <Materia>`.
- **Convenzioni:** frontmatter `tags`/`modulo`/`stato`; barra di navigazione in alto e in fondo; callout abstract, important, example, warning, `[!success]-` pieghevole per le risposte alle domande di richiamo, `[!question]` solo negli indici; fonti come percorsi tra backtick (non wikilink: gli originali non sono nel vault); MOC e 99 portano il nome della materia per restare unici nel vault; niente `# : ? | [ ]` nei nomi (C# diventa CSharp); dati sensibili mascherati (ID account AWS, MAC, IP pubblici).
- **Metodo:** per ogni materia un workflow (autori in parallelo + revisore di completezza sulle fonti), poi MOC e 99 scritti dalla sessione principale; controllo automatico di link e ancore; commit Conventional Commits e push a fine materia, aggiungendo solo file del vault (mai la cartella `$HOME/`).
- **Ordine:** prima materia AWS (impostazioni consigliate, poi revisione di Luca su stile e profondità); le altre seguono il piano elencato nell'indice generale.

**Perché:** il lavoro (circa 160 file) richiede molte sessioni e queste scelte sono già state concordate: non vanno ridiscusse a ogni ripresa.
**Come applicare:** prima di riprendere, `git pull` nel vault (Luca può aver modificato note dal telefono), leggere l'indice generale per lo stato e seguire le stesse convenzioni. Collegato a [[progetti-its]].
