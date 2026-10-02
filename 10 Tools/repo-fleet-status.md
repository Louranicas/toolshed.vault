---
tags: [toolshed, tool, workspace-5, local-helper]
tool: repo-fleet-status
version: 1.0 (local, 2026-09-02)
workspace: W5 · pane w1:pV
agent_door: habitat q repo-fleet
---

# repo-fleet-status — the repo fleet at a glance

Local helper (`~/.local/bin/repo-fleet-status`), written in-habitat. Walks every git repo under `$REPOS_DIR` (default `/var/mnt/STORAGE-10TB/repos`) and prints **branch · working-tree state (`clean` / `±N`) · last-commit date**, with a clean/dirty rollup. **Read-only: never fetches, never mutates.**

```bash
repo-fleet-status                                   # default repos dir
REPOS_DIR=/some/other/tree repo-fleet-status
```

Current fleet: **31 git repos — 28 clean, 3 dirty** (`ORAC ±173`, `herdr ±1`, `zellij ±1`). The other 16 directories under `repos/` are vault/graph exports, not git repos.

## Why it exists

`repos/` holds 47 directories; `git status` per repo is 31 commands. This is the cheapest possible answer to *"is anything uncommitted anywhere"* — the question that precedes any backup, rebase, or machine migration.

## Chains

**Feeds into:** [[lazygit]] (open the dirty one), `fzf` (pick a repo), [[Workflow Recipes]] R4 (pre-flight check).

```bash
repo-fleet-status | awk '$3 ~ /±/ {print $1}'          # just the dirty repos
cd "$REPOS_DIR/$(repo-fleet-status | awk '$3 ~ /±/ {print $1}' | fzf)" && lazygit
```

Related: [[lazygit]] · [[Workflow Recipes]] · [[00 - Habitat Toolkit]] ·
[[00 - Toolshed Index]] · [[Command Matrix]]
