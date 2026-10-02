---
tags: [toolshed, workflow, arena, practice]
created: 2026-09-02
updated: 2026-09-06
path: /var/home/Louranicas/fedora-arena
---

# 🏟️ Arena — the practice ground

A writable sandbox built to exercise the whole toolchain against **real material** rather than
toy input. Every finding in [[00 - Field Findings]] and every workflow in [[00 - Workflows]] was
produced here.

## What is in it

| Thing | Why it exists |
|---|---|
| `crates/arena-core` — a Rust workspace, 5 passing tests | gives [[bacon]], `cargo`, [[just]] something real to chew |
| `data/readings.json` + `readings.csv` — 120 synthetic telemetry rows | [[jqp\|jq]] and [[nushell]] need both a JSON and a CSV subject |
| `justfile` — 4 groups mirroring W2–W5 | the verb layer |
| `notes/` — prose | [[fzf\|rg]], [[television]], [[mempalace]] |
| git history + a `feature/stats` branch | [[lazygit]], [[hunk]], [[tuicr]] need a diff |
| `scripts/` — the bridges | the workflows themselves |

Mined into the palace as its own wing (`fedora_arena`), so everything here is retrievable via
`habitat recall`.

## Deliberately imperfect code

`crates/arena-core/src/stats.rs` was written with real, idiomatic-Rust flaws so the bridges had
genuine findings to carry:

- `n % 2 == 0` → `clippy::manual_is_multiple_of`
- `count = count + 1` → `clippy::assign_op_pattern`
- `return count;` → `clippy::needless_return`
- `spread()` unwraps → panics on empty input (the *human's* note — clippy does not catch it)

That last one is the point: **the agent found three mechanical issues, the human found the
semantic one.** The gate's "no human note yet" rung exists because of exactly this asymmetry.

## `arena-pulse` — the five-cluster health check

`scripts/arena-pulse.sh` (also `just pulse`, `atuin scripts run arena-pulse`) crosses
C4 build → C5 data → C6 system → C7 spine in one command:

```json
{
  "C4_build":  {"errors": 0, "tests_passed": 5, "recipes": 6},
  "C5_data":   {"rows": 120, "failures": 16, "slowest": {"tool":"herdr","duration_ms":4171},
                "by_cluster": {"C1":15,"C2":24,"C3":29,"C4":18,"C5":12,"C6":12,"C7":10}},
  "C6_system": {"loadavg": "0.41 0.48 1.25", "containers": 1},
  "C7_spine":  {"arena_panes": 5, "services_running": 12},
  "verdict":   "green"
}
```

## Cross-workspace drill

Five panes across **three tabs** (W2 `t5`, W3 `t6`, W5 `tC`) were driven onto the arena
simultaneously and verified by content — bacon on `fedora-arena check`, just showing the arena's
`[data]` group, hunk showing the arena's own test code — then restored to registry state with
`habitat respawn`.

That drill is what exposed [[00 - Field Findings|F6]]: `herdr pane run` executes in the pane's
*current* directory, so respawn was relaunching tools wherever they had been driven. `habitat`
now prefixes `cd <registry cwd> &&`.

## The watch chain, demonstrated

The cheapest pattern in the habitat, proven live:

1. Injected `readings.iter().sum::<i64>() + "oops"`
2. `bacon` caught `E0277: cannot add &str to i64` — **without me running a build**
3. Read the full diagnostic with `habitat pane bacon`
4. Reverted → green

A pane read can avoid another build. The watcher itself consumes resources, and its result must
match the current project, revision and completed run before it is treated as evidence. Keep one
useful feedback loop per worktree; do not duplicate it with frequent build probes by default.
See [[60 Workflows/Autonomous Triggers#Probe cost and lifecycle]] and
[[60 Workflows/00 - Workflows#Daily operating cycle — reviewed 2026-09-06|the operating cycle]].

## Reproducing the arena

```bash
cd /var/home/Louranicas/fedora-arena
just --list        # every verb
just survey        # all four workspaces at a glance
just review        # build ▶ annotate ▶ coverage ▶ gate
```

Related: [[00 - Workflows]] · [[00 - Field Findings]] · [[Cross-Workspace Review Gate]]
