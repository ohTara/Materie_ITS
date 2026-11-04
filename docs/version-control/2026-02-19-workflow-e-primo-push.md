# Version Control — workflow e primo push

**Cartella:** `Fondamenti_Version_Control/` · **Commit correlati:** 19/02–06/03/2026 (primo commit, CI C/C++, merge, pull request #1 `aggiuntaesercizi`)

## Cosa c'è nella repo
- `Esercizio-WorkFlow_19-02/ReadMe.md`: un singolo file di prova (esercizio di workflow a due persone).
- `Lezione_3_Fondamenti-Version-Controll/ReadMe.md`: *"Primo push, Lezione 3"*.
- PDF: *Lezione 3 – Introduzione a Git Remoto e Repository Online*.

## Cosa si ricava dalla cronologia (fatti)
Primo commit del 27/02/2026; un errore con una `.git` annidata risolto con *"Fix: Rimossa .git Interna"*; aggiunta di un workflow GitHub Actions *C/C++ CI* (`.github/workflows/c-cpp.yml`); merge di `main` e una **pull request** (#1) il 06/03/2026.

## Concetti
`add → commit → push`, `pull`, **merge**, **pull request**. Una repo dentro un'altra repo (`.git` annidata) fa tracciare la cartella come *submodule vuoto*: va rimossa la `.git` interna.

> Il vecchio README citava rebase e stash: nei file della repo non ci sono prove di questi argomenti, quindi non sono riportati qui.
