---
tags: [toolshed, workflow, trigger, autonomous, event-driven]
created: 2026-09-02
updated: 2026-09-06
source: ~/.local/bin/habitat-trigger
---

# 🎯 Autonomous Triggers — the habitat acts without being asked

A cascade you have to *run* is still a command. This fires one when a **condition becomes true**,
so a single edit produces detection, a parallel cascade, and annotations in the live diff — with
no further input.

```bash
habitat-trigger <triggers.toml> [--dry-run] [--once]
HABITAT_TRIGGER_POLL=3 habitat-trigger ...       # poll interval, default 4s
```

## Proven end to end

```
21:02:03  armed 2 trigger(s): build-broke@probe, fleet-dirty@probe
21:02:13  ⚡ build-broke ← error: could not compile `arena-core` (lib) due to 6 previous errors
21:02:15     ✓ W4 when         32 ms  2026-09-02T21:02:13+10:00
21:02:15        wave 1: 90 ms wall vs 122 ms serial
21:02:15     ✓ W3 annotate   1280 ms
21:02:15     total 1372 ms  → rc=0
```

Armed while the build was green; one edit introduced a type error; ten seconds later the cascade
had run and annotated. **No command was issued between the edit and the result.**

## Existing spec — inspected 2026-09-06

```toml
[[trigger]]
name  = "build-broke"
probe = "cargo check --message-format short 2>&1 | tail -5"
cwd   = "/var/home/Louranicas/fedora-arena"
regex = "^error|could not compile"
run   = "habitat-cascade run .../on-break.toml"
debounce = 20
```

A trigger may watch a **`probe`** (a command) or a **`pane`**/`service`. Fires on the **rising
edge** only — the transition from not-matching to matching — never on a level that is merely
still true. `debounce` guards against a rebuild emitting many matching lines.

## Probe cost and lifecycle

Source inspection confirms that the default four-second poll executes each `probe` even when
no action fires. **Debounce limits actions, not probe execution.** `--dry-run` also executes
the probes; it only suppresses the triggered action. Do not treat it as a passive preview of
an unfamiliar command.

The checked Arena configuration still contains the `cargo check | tail -5` probe above. It is
an output-pattern detector, not a compiler-exit-status gate. Pairing it with an active Bacon
watcher can duplicate build work; the short tail can also omit relevant diagnostics. The
configuration was inspected, not changed or activated during this documentation review.

Before keeping a trigger resident, establish its owner, project, useful poll interval, scratch
location and normal shutdown path. Prefer a lightweight current result where its freshness
and error handling can be established. Otherwise choose an explicit probe interval for the
workload; changing `HABITAT_TRIGGER_POLL` is a trial to measure, not an automatic improvement.
Repeated scans, build probes and resulting cascades all belong in the resource budget.

See [[60 Workflows/00 - Workflows#Daily operating cycle — reviewed 2026-09-06|the daily cycle]]
and [[50 Field Notes/lukes workflows#Recommended working rhythm|Luke's working rhythm]].

## Why it watches state, not screens ⭐

The first three designs all failed, and the reasons are the interesting part:

1. **Subscribe to `pane.exited`** — never fires. It is about the *pane*, not its foreground
   process ([[00 - Field Findings|F17]]).
2. **Subscribe to `pane.output_matched` on the bacon pane** — never fires. bacon is an
   **alt-screen TUI**; `output_matched` cannot see alt-screen rendering.
3. **Give `bacon --headless` its own pane** (it writes plain text to the normal screen) — *still*
   never fires. The decisive finding: **`pane.output_matched` evaluates the pane snapshot at
   subscribe time, fires at most once, and is then consumed.** Arming on an already-broken pane
   fired instantly; arming on a clean pane and then breaking the build produced nothing. It is a
   *check now*, not a *watch* — the name misleads.

> A nice reversal: `bacon --headless` was earlier catalogued as a **defect** ("watches forever,
> hangs the caller, useless as a one-shot verdict"). Those exact properties — never exits, prints
> plain text — are what make it a good event *source*. A tool's worst property in one role can be
> its best in another.

**Resolution:** a `probe` asks the question directly (`cargo check`), so it is immune to how any
tool chooses to render. Edge detection by polling. Less elegant than an event, and *actually works*.

## Two triggers that ship

| name | probe | fires on |
|---|---|---|
| `build-broke` | `cargo check --message-format short` | `^error\|could not compile` → `on-break` cascade |
| `fleet-dirty` | `repo-fleet-status \| tail -1` | 5+ dirty repos across the fleet |

Related: [[Cascade Engine]] · [[Habitat Reactor]] · [[00 - Field Findings]] · [[bacon]] ·
[[00 - Habitat Toolkit]] · [[00 - Toolshed Index]] · [[00 - Workflows]]
