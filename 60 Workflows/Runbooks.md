---
tags: [toolshed, workflow, runbook, synthesis, atuin, just, cascade, mcp]
created: 2026-09-02
updated: 2026-09-09
source: ~/.local/bin/habitat-runbook · fedora-arena/runbooks/
---

# 📓 Runbooks — one definition, every layer

## The problem this solves

The habitat grew **three ways to name a procedure**, and they duplicated each other:

| Layer | Gives you | Cannot |
|---|---|---|
| **atuin script** | inspectable with `atuin scripts get NAME -s`, templated, syncable | by itself provide structured preconditions and verification |
| **just recipe** | discoverable per repo, parameterised | by itself synchronise a procedure across every entry point |
| **cascade spec** | dependencies, parallel stages and receipts | by itself provide the ordered procedure's full precondition/recovery contract |

An `atuin script` wrapping a `just` recipe running a `cascade` is a *chain*, not a system —
three places to edit, three places to drift.

A **runbook** is the missing layer above them: a named procedure with a **purpose**, checked
**preconditions**, ordered **steps** (each of which may be a just recipe, a cascade, an MCP call,
or a plain command), and a **verification** that says whether it actually worked.

`export` derives entry-point material from the definition. The inspected implementation prints
the Just recipe, writes an Atuin body file and prints a registration command. It does **not**
automatically install both surfaces or prove they match the current definition. Review and
regenerate through the existing deployment workflow when the source procedure changes.

```bash
habitat-runbook list
habitat-runbook show ship
# run and export are separate actions; review their effects before invoking them.
```

## A runbook spanning four layers

```toml
name    = "ship"
purpose = "Verify a change, annotate it for review, and gate it"

[[precondition]]
check      = "git rev-parse --abbrev-ref HEAD"
expect_not = "master"
expect_rc  = 0
message    = "ship runs on a feature branch — you are on master"

[[step]]
name = "build"
just = "check"                # ← a just recipe

[[step]]
name    = "review"
cascade = "web-review"        # ← a parallel DAG

[[step]]
name = "topology"
mcp  = "cockpit call ws_overview"   # ← an MCP tool

[verify]
run      = "just gate"
contains = "READY"
expect_rc = 0
```

This example adds explicit exit-status checks to the original demonstration. Use the project's
actual protected-branch policy; excluding `master` alone does not exclude `main`. The sample
transcripts below are historical, not reruns of this revised example.

Run:

```
▶ ship — Verify a change, annotate it for review, and gate it
  ✓ pre   git rev-parse --abbrev-ref HEAD          feature/stats
  ✓ pre   habitat status | tail -1                 12 running · 4 shell · 0 stopped
  ✓ 1. build       [just]      69 ms   Finished `dev` profile
  ✓ 2. test        [just]      64 ms   Doc-tests arena_core
  ✓ 3. review      [cascade]  933 ms   agent=0 human=1 — human-only review
  ✓ 4. topology    [mcp]      127 ms   12 running · 4 shell · 0 stopped
  VERIFIED  expected 'READY'
  ship complete in 1889 ms
```

## Preconditions must actually block

Same principle as the [[Cross-Workspace Review Gate|gate]]: a procedure that only ever succeeds is
decoration. Checked out `master` and re-ran:

```
  ✗ pre   git rev-parse --abbrev-ref HEAD          master
  BLOCKED — ship runs on a feature branch — you are on master
```

Preconditions are the part a human would otherwise hold in their head — *"don't run this on
master"*, *"the cockpit must be healthy first"*. Writing them down is most of the value; checking
them is the rest.

## Historical assimilation demonstration — 2026-09-02

One definition, **four entry points**, same procedure:

```bash
habitat-runbook run audit          # direct
just rb-audit                      # GENERATED recipe
atuin scripts run rb-audit         # GENERATED script (synced, portable)
mcpc cockpit call ws_runbook action=run name=audit    # via MCP
```

`just rb-audit` → `audit complete in 652 ms`; `atuin scripts run rb-audit` → `654 ms`. The same
work, reached four ways, defined once.

The generated recipes live under a `[runbook]` group marked **"GENERATED — do not edit by hand"**,
which is the honest way to say where the source of truth is.

## The verify loop

### Inspection and execution boundaries — source checked 2026-09-06

`run --dry-run` **executes preconditions** before skipping steps and final verification.
Inspect the TOML and `show` output first; a dry-run can still run an expensive or mutating
precondition. `export` writes an Atuin body file, so it is not a read-only inspection command.

For preconditions and `[verify]`, specify `expect_rc = 0` when success is required. A content
check alone does not imply a zero exit status in the installed executor. The retrying-step
path has a related limitation: a configured `expect` is passed as a content check without an
exit-status requirement. `expect_rc` is not accepted as a step key. Use a reviewed project
script that enforces the complete condition and a step gated by its exit status, or change
and test the executor separately. Adding an unsupported field is not enforcement.

### Resource ownership

Record the procedure's project/worktree, worker count, build/test concurrency, NVMe scratch,
outputs to retain and normal shutdown path. Put operational settings in the owning project
recipe or worker launcher; the current runbook schema has no general resource-policy block.
Do not hand-edit generated entry points to add a second competing policy.

The HEE mutation runner already owns `TMPDIR` and removes inherited `CARGO_TARGET_DIR` for
isolated copies. Preserve that contract. A lightweight audit recipe and a mutation campaign
need different budgets even if both are reachable through the same runbook interface.
See [[60 Workflows/00 - Workflows#Daily operating cycle — reviewed 2026-09-06|the daily cycle]].

`[verify]` and any step may declare `retries`, `remediate` and `backoff`, turning a one-shot check
into a loop — see [[Tool Chaining Patterns|P9]]. `audit`'s first step demonstrates it:

```
✗ 1. machine     11 running · 4 shell · 1 stopped
  ↻ remediate habitat respawn
✓ 1. machine     12 running · 4 shell · 0 stopped  (attempt 2/3)
```

`ship`'s verify remediates an unannotated diff — but **not** the gate's "no human note yet" rung,
which is deliberately outside what an agent may fix.

## The two original demonstrated runbooks — historical counts

| Runbook | Purpose |
|---|---|
| `ship` | verify a change, annotate it for review, gate it — 2 preconditions, 4 steps, verified |
| `audit` | health of the machine **and** integrity of its documentation — 1 precondition, 3 steps |

`audit` composes [[Habitat Introspection]] with the knowledge-audit cascade, so one command asks
both *"is the machine well?"* and *"is what we believe about it still true?"*.

## Pi Genesis planning seam — 2026-09-06
[Genesis Justfiles and Runbooks](obsidian://open?vault=pi.vault&file=95%20Genesis%2FGenesis%20Justfiles%20and%20Runbooks) links back here and separates inert inspection, staged generation and admitted execution. The Rust-engine plan reuses the one-procedure/thin-entry-point idea while explicitly refusing automatic compatibility with this installed shell runner. GR16/IF11/S8 cover typed inputs, generated-wrapper freshness, current grants and effect-aware recovery. Planning only: no Genesis runner, recipe installation or monthly schedule activation is implied.

## Fabric command-plane seam

Fabric should emit a typed, non-executable plan; the runbook layer should validate its service,
recipe, step and approval class before rendering Bash or generated entry points. The earlier
review recorded three runbook specs but only two generated Just/Atuin surfaces. That count is dated;
freshness must be checked before claiming convergence. The contract and promotion path live in
[[Fabric Bash Command Plane]].

Related: [[Factory Roster Expansion - DevOps Toolbox]] · [[Fabric Bash Command Plane]] · [[Fabric Habitat 90-Point Promotion and Practice]] · [[Cascade Engine]] · [[Clustering Shapes]] · [[MCP Servers]] · [[00 - Habitat Toolkit]] · [[atuin]] · [[just]]

## Current definition and entry-point review — 2026-09-06

All six installed definitions are listed in [[40 Reference/Cascade and Runbook Catalogue|the regenerated catalogue]] and the [runbook source map](file:///var/home/Louranicas/fedora-arena/runbooks/README.md). The current `audit` has six steps; `ship` has four; `corpus-backup` has two; each `factory-*` procedure has one. Only `audit` and `ship` currently have generated Arena Just wrappers. Live Atuin registration was not inspected.

[The detailed review](obsidian://open?vault=herdr-fedora-habitat.vault&file=95%20Genesis%2FJustfiles%20and%20Runbooks%20Review%202026-09-06) records the installed runner limitations, staged candidate boundary, complete source census and meaningful catalogue freshness controls. Return links lead here and to both source maps. Presence of `[verify]`, a generated recipe, or a passing parse does not certify a procedure. The historical transcripts above retain their original dates and subjects.

## Context preparation — 2026-09-09

[[70 Toolkit/skills#Habitat Context|Habitat Context]] ⇄ this note. Assemble selected runbook declarations, Justfiles and implementation into bounded context packets, preserving whole sources and exposing gaps. Static procedure relationships do not establish precondition, verification or runtime success.
