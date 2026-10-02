---
tags: [toolshed, toolkit, reference, local-tools]
created: 2026-09-02
updated: 2026-09-06
---

# 🧰 Habitat Toolkit — the six locally-built tools

**Navigation:** [[40 Reference/Command Matrix#Composition and verification routes|Command Matrix ⇄ composition routes]] · [[00 - Toolshed Index|Toolshed master index]]. Find the locally authored bridge, cascade, sandbox and related tools.


> **⚓ Code anchor** — `~/.local/bin/habitat-sandbox:60` · expects `extra += ["-v", f"{hp}:{cp}:ro,z"]`
> The `:ro,z` mount option is the whole isolation guarantee. `:Z` cannot relabel a read-only mount; that one character is why fanout is safe.
> *Verified 2026-09-03 · re-check `just doc-anchors`; this note updates when the code does.*

Everything here was written **in this habitat**, lives in `~/.local/bin` (the durable `$HOME`
layer), and is captured by `habitat-settings-backup` — **verified 2026-09-03, and it was not true
when written**: the snapshot held 12 of 16 and omitted `habitat-cascade`, `-trigger`, `-sandbox`
and `-fleet`, while `backup-integrity` read `26/26 PASS` because it reconciles the *declared*
list. Both backup and restore now name all 16 ([[00 - Field Findings|F65]]). All six read the same registry
(`~/.config/habitat/services.json`), so none of them hardcodes a pane ID.

| Tool | One line | Note |
|---|---|---|
| **`habitat`** | the bridge — reach any Workspace service two ways | [Habitat Service Bridge](obsidian://open?vault=herdr-fedora-habitat.vault&file=70%20Toolchain%2FHabitat%20Service%20Bridge) |
| **`habitat-reactor`** | self-healing; systemd unit on herdr's event bus + liveness poll | [[Habitat Reactor]] |
| **`habitat-cascade`** | parallel DAG runner across W1–W5, with receipts | [[Cascade Engine]] |
| **`habitat-trigger`** | edge-detected state → fires a cascade, unattended | [[Autonomous Triggers]] |
| **`habitat-sandbox`** | disposable podman workers; fanout and fusion | [[Sandbox Fanout and Fusion]] |
| **`habitat-fleet`** | agent supervision, with herdr's detection rule exposed | below |
| **`habitat-runbook`** | named procedures spanning just/cascade/MCP; generates the other layers | [[Runbooks]] |
| **`habitat-introspect`** | profiles the habitat from its own cascade receipts | [[Habitat Introspection]] |
| **`mcpc`** | MCP client — drive any stdio server from the shell; `surface` costs a server by tier | [[MCP Servers]] |
| *(helper)* `repo-fleet-status` | branch/dirty/last-commit across every repo | [[repo-fleet-status]] |

---

## `habitat` — the service bridge

```bash
habitat status                 # 16 services: pane, running/stopped/shell, agent door
habitat map · habitat ls
habitat q <svc> [args...]      # the documented non-interactive door
habitat pane <svc> [lines]     # read the live TUI's screen (works for ALL services)
habitat doc <svc>              # print that service's Obsidian note
habitat respawn [-n] [svc..]   # relaunch only what is stopped (cd's to the registry cwd)
habitat recall <q> · habitat wake · habitat history <t> · habitat vault <p>
```

Services resolve by **tab label + geometry slot**, never a stored pane ID — which is what makes
it survive restarts, re-splits and rebuilt sessions.

## `habitat-reactor` — self-healing

```bash
systemctl --user status habitat-reactor      # via flatpak-spawn --host
habitat-reactor --dry-run · --once
tail -f ~/.local/state/habitat/reactor.log
```

Subscribes to herdr's bus for **topology** (`pane_created/closed`, `tab_*` → re-resolve the map)
and **polls every 20 s for liveness**, because the bus has no service-death signal at all
([[00 - Field Findings|F17]], [[00 - Field Findings|F22]]). Proven: `poll: tuicr down in w1:pR --
respawning` → back within 20 s.

## `habitat-cascade` — parallel DAGs

```bash
habitat-cascade graph <spec.toml>
habitat-cascade run   <spec.toml> [-v K=V] [--dry-run] [--seq] [--json]
just doctor · just sweep · just dag <name> · just bench
```

Kahn layering: each wave is the set of stages whose `needs` are satisfied, run in a thread pool.
**2259 ms → 1008 ms (2.24×)** on identical work. `receipts = "<dir>"` writes a mineable markdown
record per run, so the palace can answer *"when did the build last break"*.

## `habitat-trigger` — autonomous cascades

```bash
habitat-trigger <triggers.toml> [--dry-run] [--once]
HABITAT_TRIGGER_POLL=3 habitat-trigger ...
```

Watches a **`probe`** (a command) or a pane, fires on the **rising edge** only, with `debounce`.
Probes exist because screens lie: `output_matched` cannot see alt-screen TUIs and fires only on
the snapshot present at subscribe time.

## `habitat-sandbox` — isolated parallel workers

```bash
habitat-sandbox create --n 4 --src <dir> [--memory 512m --cpus 1.0]
habitat-sandbox list · exec <name> <cmd...>
habitat-sandbox fanout --tasks tasks.json     # one task per sandbox, in parallel
habitat-sandbox fuse --out fused.json         # keyed merge, not a flat add
habitat-sandbox destroy
```

Source mounted **read-only** (`:ro,z` — never `:Z`, see [[00 - Field Findings|F33]]), each worker
gets its own writable `/out`. podman is host-side, so every call escapes via `flatpak-spawn --host`.

## `habitat-fleet` — agent supervision

```bash
habitat-fleet            # one line per agent: kind, state, pane, tab, title
habitat-fleet --why      # + the WINNING detection rule and the region it inspected
habitat-fleet --json
```

`herdr agent list` says *what* state an agent is in; `herdr agent explain` returns the entire
rule-engine trace — every rule with its priority, terminal region and evidence. `--why` surfaces
the rule that actually won, which is what you need when a status looks wrong:

```
● claude   working  w1:p1   Orchistrator   Workspace repos setup and documentation
    rule osc_title_working  region=osc_title  (17 rules evaluated)
● codex    idle     w1:p3   Orchistrator   Louranicas
    rule osc_title_idle     region=osc_title  (8 rules evaluated)
```

Different agent kinds carry different rule sets — 17 for claude, 8 for codex.

## Durability

All six live in `$HOME`, so a toolbox rebuild does not touch them. They depend on `python3`
(toolbox layer, reinstalled by `toolbox-bootstrap`) and `herdr`/`jq`. The two systemd user units
(`habitat-reactor`, `habitat-trigger`) and the registry are captured by
`habitat-settings-backup`; `habitat-settings-restore` re-enables them.

Related: [[00 - Workflows]] · [[00 - Field Findings]] · [[00 - Toolshed Index]]
