---
tags: [toolshed, tool, workspace-2, rust, watcher]
tool: bacon
version: 3.25.0
upstream: https://github.com/Canop/bacon
workspace: W2 · pane w1:pJ (on repos/deep-diff-forge)
agent_door: habitat pane bacon  (preferred) · habitat q bacon → cargo check
updated: 2026-09-06
---

# bacon — background Rust checker

Watches a Rust project and re-runs a **job** on every save, rendering errors in a minimal persistent TUI. The canonical *"left pane codes, right pane judges"* tool.

## Jobs (verified `bacon --list-jobs` in deep-diff-forge)

`check` (default) · `check-all` · `clippy` · `clippy-all` · `pedantic` (`-W clippy::pedantic`) · `test` · `nextest` · `doc` · `doc-open` · `run` · `run-long` · `ex`

```bash
bacon                      # default job
bacon clippy · bacon test · bacon nextest
bacon -j clippy-all
bacon clippy -- -W clippy::pedantic     # extra args after --
bacon --list-jobs          # -l
bacon --init               # write a customisable bacon.toml
bacon --summary  (-s) · --no-summary (-S) · --wrap (-w) · --reverse · --help-line
bacon --offline · --prefs · --export-locations
```

## ⚠️ `--headless` is NOT a one-shot

Help text: *"Run without user interface: just run the default job **on change**"*. It **watches forever and never exits** — it will hang a caller. Corrected here 2026-09-02 after it hung a verification run; the herdr vault's Tool note said "one-shot verdict", which was wrong.

**The two real doors:**
1. **Read the resident pane** — `habitat pane bacon`. The watcher already computed the answer; reading costs nothing and re-runs nothing. *Preferred.*
2. **One-shot** — `cargo check --message-format short` (what `habitat q bacon` runs). ~0.05s warm.

## Remote control ⭐ (unexplored here)

```bash
bacon --listen              # bacon listens on a unix socket for commands
bacon --send <command>      # drive a RUNNING bacon from outside
```

This is the principled way to steer the resident watcher — switch it to `clippy`, or re-run — without touching the pane. Not yet wired into [[herdr]]; the obvious next integration.

## TUI keys

`c` clippy · `t` test · `d` doc · `r` run · `s` summary · `w` wrap · `p` pause · `/` search · `Esc` back · `q` quit · `?` help

## Config

`bacon.toml` per project (custom jobs — a job can shell out to `just`), `~/.config/bacon/prefs.toml` *(created on demand by `bacon --prefs`)* global. `--export-locations` writes `.bacon-locations` for editor jump integration.

## Chains

**Feeds from:** file saves (its own watcher) — including *my* edits.
**Feeds into:** `habitat pane bacon` → me. The [[herdr]] watcher pattern: I edit, bacon judges, I read the verdict without polling anything.

## Rust performance practice

Use [[40 Reference/Perfecting Rust - Performance Engineering#Practice until the reasoning is reproducible|the Rust mastery practice sessions]] to connect the watcher feedback loop to explicit correctness and performance evidence. [[40 Reference/Perfecting Rust - Performance Engineering#Benchmark the question you actually care about|Benchmark boundaries]] explain what a separate timing experiment measures; [[40 Reference/rust-mastery/2026-09-06/README|the runnable allocation lab]] supplies a small practice project.

Related: [[just]] · [[herdr]] · [[hunk]] · [[Tool Chaining Patterns]] · [[00 - Toolshed Index]] ·
[[Arena Practice Ground]] · [[Autonomous Triggers]] · [[Bridge - Diagnostics to Review]] ·
[[Command Matrix]] · [[Documented Surface and Source]] · [[Tool Clusters]]
