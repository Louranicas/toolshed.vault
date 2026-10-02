---
tags: [toolshed, workflows, moc, chaining]
created: 2026-09-02
updated: 2026-09-08
---

# ⚙️ Workflows — what was actually built

**Navigation:** [[40 Reference/Command Matrix#Composition and verification routes|Command Matrix ⇄ composition routes]] · [[00 - Toolshed Index|Toolshed master index]]. Place tool selection in the daily operating and verification cycle.

The original [[Most-Used Tools]] analysis found **one** genuine pipe pair in 156 recorded
commands on 2 September. That small historical sample motivated these compositions. The newer
[[50 Field Notes/lukes workflows|workflow assessment]] separates 287 Fedora records from a
127,613-record older checkpoint and explains their coverage limits. Demonstrations below record
what was tested at the time; this index is not a fresh runtime certification of every workflow.

## Daily operating cycle — reviewed 2026-09-06

The measured session had about **66 GiB available RAM**, while readable `/tmp` allocation was
**16.36 GiB** and Herdr itself used about **59 MiB PSS**. Preserve useful pane organisation and
manage the workloads and temporary data within it. These are dated observations, not live limits.

| Phase | Operating guidance | Detail |
|---|---|---|
| Orient | Choose the project/worktree and inspect its maintained recipe; recall history as evidence. | [[20 Chaining/Workflow Recipes#R1 · Full recall — "what do we know about X?" ⭐\|Recall]] · [[20 Chaining/Workflow Recipes#R2 · Orient in an unfamiliar repo (P7)\|Project entry]] |
| Focus | Keep one primary feedback loop for that worktree; use a current watcher result when suitable. | [[20 Chaining/Tool Chaining Patterns#P3 · The watch chain — resident watcher + `pane read`\|Watcher use]] |
| Build/review | Assign NVMe scratch, isolated targets and a bounded set of workers. Preserve runners that own these settings. | [[50 Field Notes/lukes workflows#The largest actionable finding: temporary data\|Scratch]] · [[60 Workflows/Cascade Engine#Capacity and scheduling — source checked 2026-09-06\|Scheduling]] |
| Verify | Require the operation's exit status and its intended result; collect pressure during the same workload. | [[60 Workflows/Cross-Workspace Review Gate\|Review gate]] · [[60 Workflows/Habitat Introspection#Resource measurements alongside timing\|Resource measurement]] |
| Handoff | Save results, active-job ownership and retained-output locations before retiring a completed session. | [[50 Field Notes/lukes workflows#Recommended working rhythm\|Working rhythm]] |
| Retire | Review only completed, owned scratch. Check restart policy so intentionally closed services stay closed. | [[60 Workflows/Habitat Reactor#Intentional shutdown and recovery policy\|Reactor lifecycle]] · [[60 Workflows/Sandbox Fanout and Fusion#Capacity and ownership — source checked 2026-09-06\|Sandbox ownership]] |

This is operating guidance. Per-service suspension, a global worker queue and automated retention
have not been installed. Source-confirmed limitations and the documentation changes are recorded in
[[40 Reference/workflow-review/2026-09-06/README|the workflow review receipt]].

> [!success] [[Claim-Time Guard]] 🛡️ — the rule that fires WHERE THE CLAIM IS MADE
> `PIPE_SWALLOWS_VERDICT` recurred three days running with a working detector, because the
> detector only ever ran at session end. It is now a `PreToolUse` hook importing the same
> detector module, plus `gate` — which makes the correct form shorter to type than the wrong
> one. Proven to fire live, in both directions.

## The layered stack

```
atuin script          synced · minijinja-templated · capturable with --last N
      │  -v repo=… -v recipe=…
      ▼
just recipe           the project's own verb; discoverable (--summary, --dump --dump-format json)
      │
      ▼
bridge script         cross-workspace orchestration (annotate · coverage · gate · goto)
      │
      ▼
tools                 cargo · rg · hunk · nvim · herdr event bus · podman · jq
```

Each layer adds one property the one below lacks: **tools** do the work, **bridges** cross
workspaces, **just** makes it discoverable per repo, **atuin** makes it parameterised, synced
and portable. The same atuin script drove `deep-diff-forge` (9 recipe groups) and degraded
gracefully on `mempalace` (no justfile).

## Rust performance practice

[[40 Reference/Perfecting Rust - Performance Engineering|Perfecting Rust — Performance Engineering]] extends the operating cycle into workload definition, semantic checks, benchmarking, profiling and recorded optimization decisions. Start with [[40 Reference/Perfecting Rust - Performance Engineering#Practice until the reasoning is reproducible|the practice program]] and retain results using [[40 Reference/rust-mastery/2026-09-06/README|the lab and evidence guide]].

## The workflows

| Workflow | Chain | Note |
|---|---|---|
| **Diagnostics → live review** | W2 build → W3 | [[Bridge - Diagnostics to Review]] |
| **Insights report → a browser that can read it** | `/insights` → `Stop` reflex → `~/Documents` | [[Insights Reports - Opening Them Past the Sandbox]] |
| **Insights findings → mechanisms** | report → status table → guards | [[Mitigation Plan]] |
| **Coverage gaps → live review** | W4 search → W2 tests → W3 | [[Bridge - Coverage to Review]] |
| **Cross-workspace readiness gate** | W2 → W3 → W4 → W5 | [[Cross-Workspace Review Gate]] |
| **Review ⇄ editor in lockstep** | W3 ⇄ W2 | [[Synchronised Review and Editor]] |
| **Self-healing habitat** | herdr event bus + poll | [[Habitat Reactor]] |
| **Parallel cascades** ⭐ | DAG across W1–W5; historical 2.24× demonstration | [[Cascade Engine]] |
| **Autonomous triggers** ⭐ | edge-detected state → cascade | [[Autonomous Triggers]] |
| **Weight matrix** ⭐ | faults × gates → which gate bore the weight | [[Weight Matrix - Which Gate Bore the Weight]] |
| **Agent supervision** | `habitat-fleet --why` | [[Cascade Engine]] §doctor |
| **Runbooks** ⭐ | one definition → just + atuin + MCP | [[Runbooks]] |
| **Knowledge audit** | tools/notes/paths tested like code | [[Knowledge Audit]] |
| **Self-profiling** ⭐ | receipts → bottleneck → verified fix | [[Habitat Introspection]] |
| **Sandbox fanout & fusion** ⭐ | N isolated podman workers → verified join | [[Sandbox Fanout and Fusion]] |
| **Five-cluster health pulse** | C4·C5·C6·C7 | [[Arena Practice Ground]] §arena-pulse |
| **Workflow-tool candidates** (2026-09-27, not built) | 19 runs → 12 judged candidates → build order | [[Workflow Candidates - Mined From 19 Runs]] |

## The full picture

```
        edit a file
             │
   habitat-trigger        probe: cargo check ... (edge-detected)
             │
   habitat-cascade        DAG: 11 stages parallel → 2 → 1
        ┌────┴────┬─────────┬─────────┐
       W2        W3        W4        W5
     build   annotate    system     fleet
             │
   hunk session          notes appear in the live diff
             │
   nvim --server         cursor follows (just goto)
             │
   receipt → palace      the habitat remembers the run
```

Nothing in that chain requires a human command after the edit.

## The justfile layer

`fedora-arena/justfile` — groups mirror the workspaces:

```
[W2-build]   check · test · lint · diagnostics
[W3-review]  annotate · coverage · annotate-all · retract · goto · walk
[W4-W5]      gate · pulse · telemetry · fleet
[cascade]    doctor · sweep · dag · bench · fleet-agents
[composite]  review (check ▶ annotate-all ▶ gate) · survey (all four workspaces)
```

`just survey` is the fastest "what can an agent see right now" across every workspace.

## The atuin library (10)

| Script | Template vars | Does |
|---|---|---|
| `recall` | `{{ q }}` | shell-history recall + palace search; installed Atuin mode spelling is `full-text` |
| `arena-pulse` | — | five-cluster health JSON |
| `arena-slice` | `{{ cluster }}` | telemetry rows for one cluster |
| `gate` | `{{ repo }}` `{{ base }}` | cross-workspace readiness verdict |
| `annotate` | `{{ repo }}` `{{ job }}` | diagnostics → live diff |
| `coverage` | `{{ repo }}` | untested fns → live diff |
| `goto` | `{{ repo }}` `{{ n }}` | move review + editor to note N |
| `j` | `{{ repo }}` `{{ recipe }}` | run any just recipe in any repo |
| `review` | `{{ repo }}` `{{ base }}` | full W2–W5 pass via just |
| `survey` | `{{ repo }}` | cross-workspace survey, with fallback |

Created with `atuin scripts new <name> --no-edit --script <FILE>` — remember [[00 - Field Findings|F3]]:
`--script` is a **file path**, and [[00 - Field Findings|F4]]: no `{{ }}` Go templates anywhere in the body,
comments included.

## Design principles that emerged

1. **Agent annotations are ephemeral; human notes persist.** Every bridge retracts its own
   prior pass (keyed on `--author`) before re-annotating, so fixing a lint retracts its advice
   automatically. Nothing an agent writes accumulates as stale advice.
2. **Reuse a suitable current result.** A pane read avoids another build, but the watcher still
   consumes resources. Check its project, revision and completion state before relying on it.
3. **Inspect before running.** Read the recipe/source and its preview behaviour. Some dry-runs
   still execute probes or preconditions: see [[60 Workflows/Autonomous Triggers]] and
   [[60 Workflows/Runbooks]]. A preview is not a successful execution receipt.
4. **Verify the door before trusting it.** Two documented agent doors in this very vault were
   wrong (`bacon --headless`, `nu -c`). Run it once before writing it down.
5. **Gate on evidence, not intent.** The readiness gate was only trustworthy once it was shown
   to *block* — injected a type error and a failing assertion to prove it.
6. **Budget work, not pane count.** Separate worker count, compiler/test concurrency, scratch
   allocation and service lifetime. The operating cycle above is the default review path.

Related: [[00 - Toolshed Index]] · [[00 - Field Findings]] · [[Tool Chaining Patterns]] · [[Tool Clusters]]

<!-- astra-prompt-library-20260908:start -->
## ASTRA prompt library — 2026-09-08

| Resource | Relationship |
|---|---|
| [[herdr-habitat-prompt-library\|ASTRA prompt library]] ⇄ this note | Prompt cards for implementation, debugging, review and resumption; align acceptance and evidence with the existing operating cycle. Documentation guidance, not a newly deployed workflow. |
<!-- astra-prompt-library-20260908:end -->
- [[Entering an Unfamiliar Corpus]] — the first hour with a corpus you did not write: recon → layer-trace → cluster → hone, and the six traps that made six false findings in one day (2026-09-17)
