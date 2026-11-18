# Coordination Log
<!-- Append-only. Ogni istanza scrive qui i propri intenti/stati. -->

## Session Registry
| Instance | Role | Started | Last Heartbeat | Status | Current Task |
|---|---|---|---|---|---|
| grok-main | Grok Build (CLI) | 2026-11-18 22:30 | 2026-11-18 22:55 | active | creazione coord.md + registrazione |
| fcc-claude | Claude Code via FCC | — | — | unknown | — |
| fcc-opencode | OpenCode via FCC | — | — | unknown | — |
| fcc-grok | Grok Build via FCC | — | — | unknown | — |

## Task Queue (shared)
| ID | Project | Description | Owner | Status | Created | Updated |
|---|---|---|---|---|---|---|
| T-001 | FCC | Aggiornare README provider catalog | — | open | 2026-11-18 | — |
| T-002 | Minecraft | Testare backup su rclone S3 | — | open | 2026-11-18 | — |
| T-003 | Omnia | Documentare cleanup post-exam | — | open | 2026-11-18 | — |
| T-004 | Coord | Mantenere coord.md aggiornato | grok-main | in_progress | 2026-11-18 | 2026-11-18 22:55 |

## Decisions Log
| Date | Decision | Context | Author |
|---|---|---|---|
| 2026-11-18 | Usare `memory/coord.md` come bus di coordinamento | Nessun MCP/message bus nativo tra istanze; file system + Git è l'unico shared state reale | grok-main |
| 2026-11-18 | Formato tabella Markdown per leggibilità umana + LLM | Semplice, versionabile, zero dipendenze | grok-main |

## Conventions
- **Heartbeat**: aggiorna `Last Heartbeat` ogni 10-15 min se attivo
- **Claim task**: metti il tuo Instance ID in `Owner`, `Status` → `in_progress`
- **Complete**: `Status` → `done`, aggiungi nota in `Updated`
- **Blocker**: aggiungi riga in `Decisions Log` o commento inline
- **Non cancellare** righe altrui; solo append/modifica tue righe
- **Instance ID suggeriti**: `grok-main`, `fcc-claude`, `fcc-opencode`, `fcc-grok`, `fcc-codex`, `claude-desktop`, `opencode-native`

## Quick Commands (bash helper)
```bash
# Leggi stato
cat ~/memory/coord.md

# Registra/aggiorna heartbeat (esempio per fcc-claude)
# sed -i 's/| fcc-claude |.*/| fcc-claude | Claude Code via FCC | 2026-11-18 23:00 | 2026-11-18 23:15 | active | task T-001 |/' ~/memory/coord.md

# Claim task T-001
# sed -i 's/| T-001 | FCC |.*/| T-001 | FCC | Aggiornare README provider catalog | fcc-claude | in_progress | 2026-11-18 | 2026-11-18 23:15 |/' ~/memory/coord.md

# Complete task
# sed -i 's/| T-001 | FCC |.*/| T-001 | FCC | Aggiornare README provider catalog | fcc-claude | done | 2026-11-18 | 2026-11-18 23:45 |/' ~/memory/coord.md
```