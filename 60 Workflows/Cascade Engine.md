---
tags: [toolshed, workflow, cascade, parallel, dag, W1, W2, W3, W4, W5]
created: 2026-09-02
updated: 2026-09-06
source: ~/.local/bin/habitat-cascade
---

# ⚡ Cascade Engine — parallel DAGs across the workspaces

Everything before this ran **one thing at a time**. The [[Cross-Workspace Review Gate|gate]] asked
W2, then W3, then W4, then W5 — but those questions are independent. The cascade engine turns a
cross-workspace sweep into a **dependency graph**, runs every independent stage concurrently, and
fans the answers back into one document.

```bash
habitat-cascade graph <spec.toml>          # the DAG and its parallel waves
habitat-cascade run   <spec.toml> [-v K=V] [--dry-run] [--seq] [--json]
just dag doctor · just doctor · just sweep · just bench
atuin scripts run cascade -v name=doctor
```

## Measured in the original demonstration

Identical work, same 14 stages:

| mode | total |
|---|---|
| `--seq` (forced sequential) | **2259 ms** |
| default (parallel waves) | **1008 ms** |

**2.24× on the whole cascade**; wave 1 alone reports `605 ms wall vs 2324 ms serial — saved 1719 ms`.
The engine prints that saving per wave, so the parallelism is visible rather than claimed.

## Capacity and scheduling — source checked 2026-09-06

The installed `~/.local/bin/habitat-cascade` sizes its thread pool to the number of ready
stages (`max_workers=max(1, len(ready))`). Its CLI exposes `--seq` but **no configurable worker
cap**. A dependency graph expresses ordering; it does not establish a safe resource budget.

For heavy builds, begin with `--seq` or split the workload into deliberately bounded groups.
Limit compiler/test concurrency inside each worker as well. The older 14-/20-child discovery
demonstrations are not evidence that 14 or 20 simultaneous Rust builds will be efficient.
Measure a representative run before expanding width; a global scheduler limit remains a future
implementation task, not an available flag.

Give each independent worktree appropriate NVMe scratch and target ownership. Preserve the
mutation runner's explicit removal of inherited `CARGO_TARGET_DIR`; it owns isolated copies.
See [[50 Field Notes/lukes workflows#The largest actionable finding: temporary data|scratch placement]]
and [[60 Workflows/00 - Workflows#Daily operating cycle — reviewed 2026-09-06|the daily cycle]].

## Spec format

```toml
name = "doctor"
cwd  = "/var/home/Louranicas/fedora-arena"
receipts = "/var/home/Louranicas/fedora-arena/receipts"
verdict  = "services={{services.running}} palace={{palace.drawers}} broken={{vault_links}}"

[[stage]]
id      = "palace"
ws      = "W1"
capture = "json"          # json | int | text
run     = "mempalace status | ..."

[[stage]]
id    = "annotate"
ws    = "W3"
needs = ["lints"]          # waits only for what it actually needs
run   = "./scripts/clippy-to-hunk.sh . clippy"
```

Stage output is addressable by dependents and by the verdict as `{{stage.path.to.field}}` —
so `{{system.load}}`, `{{lints.0.lint}}`, `{{agents.blocked}}` all resolve into the rendered
command or verdict string. `-v KEY=VAL` supplies external variables.

Scheduling is **Kahn layering**: each wave is the set of stages whose dependencies are all
satisfied, run together in a thread pool; cycles are reported rather than deadlocking.

## The cascades that ship

| Spec | Shape | What it answers |
|---|---|---|
| `doctor.toml` | **9 parallel** + 1 join | whole-habitat health in ~580 ms |
| `full-sweep.toml` | **11 ∥** → 2 ∥ → 1 | every workspace probed, then acted on, then joined |
| `on-break.toml` | 2 ∥ → 1 | fired automatically when the build breaks |

`doctor` verdict, live:
```
services=12/0stopped reactor=active agents=5(0blocked) palace=1026
brokenlinks=0 backup=0h dirty=3 disk=26% podman=active
```
Nine subsystems — services, reactor, agents, palace, **vault link integrity**, backup age, repo
fleet, disk, podman socket — in one 576 ms answer.

## Runtime fan-out — tree and matrix ⭐

Stages may declare a width that is not known when the spec is written:

```toml
foreach = "discover"                                   # one child per element of that stage's list
matrix  = { repo = "repos", check = ["test","ci"] }    # cartesian product of two axes
```

This forced the scheduler to become **iterative** — waves cannot be layered up front once a
stage's width depends on an earlier stage's result. Each child gets its own binding
(`{{item}}`, or `{{repo}}`/`{{check}}`), an id like `probe[deep-diff-forge]`, and a `└` in the
run output so the tree is visible.

Measured: `tree-repos` turned 7 discovered repos into **14 parallel children** (90 ms wall vs
947 ms serial); `matrix-quality` produced **20 cells** from 5 repos × 4 checks (67 ms vs 1186 ms).
Full write-up: [[Clustering Shapes]].

## Receipts — the habitat remembers its own runs ⭐

With `receipts = "<dir>"`, every run writes a dated markdown receipt: per-stage ms/rc/value, the
wave structure, and the verdict. Because the arena is mined into the palace, that history becomes
**queryable**:

```bash
habitat recall "cascade receipt total ms waves stages"
# → on-break-20260902-210323.md  (cosine 0.616)
```

The habitat can now be asked *when did the build last break* and answer from its own record.

## Four traps this cost

- **[[00 - Field Findings|F29]] a top-level TOML key placed *after* `[[stage]]` is absorbed into
  that last table.** `verdict` sat at the end of the file and silently became a stage field —
  `"verdict" in spec` was False and no verdict ever rendered. Root keys go **before** the first
  array-of-tables.
- **[[00 - Field Findings|F30]] `sed -E 's/.*([0-9]+) running/\1/'` captures only the LAST digit**
  — greedy `.*` eats the `1` of `12`. The doctor cheerfully reported 2 running services out of 12.
  Use `grep -oE` per field.
- TOML forbids `id = "x"; ws = "W1"` on one line — each pair needs its own line.
- `cmd | jq ... || echo fallback` can hide producer failure because the pipeline normally
  reports jq's status. Use Bash `pipefail` when the producer's status matters. `(.field // [])`
  supplies a data default; it does not prove the producer succeeded.

Related: [[Habitat Reactor]] · [[Cross-Workspace Review Gate]] · [[00 - Workflows]] ·
[[00 - Field Findings]] · [[00 - Habitat Toolkit]] · [[00 - Toolshed Index]] ·
[[Assimilation - Rules That Fire]] · [[Autonomous Triggers]] ·
[[Cascade and Runbook Catalogue]] · [[Forge - Deployment Framework]] ·
[[Habitat Introspection]] · [[Runbooks]] · [[Sandbox Fanout and Fusion]]
