---
tags: [reference, workflows, documentation-review, resource-management]
created: 2026-09-06
author: SOL3
status: documentation-updated
---

# Workflow documentation review — 2026-09-06

The workflow section now incorporates [[50 Field Notes/lukes workflows|Luke's resource assessment]].
Start at [[60 Workflows/00 - Workflows|the workflow index]] or
[[20 Chaining/Workflow Recipes|the revised eleven recipes]]. The [[00 - Toolshed Index|master index]]
links both the operating cycle and this receipt.

## Review scope

Scanned the 23 notes in `60 Workflows` for resource, scratch, concurrency, watcher, lifecycle and
execution-boundary claims. Read the ten central/index, engine, runbook, trigger, reactor, sandbox,
profiling, Arena, gate and diagnostics notes in full; inspected the resource-relevant passages in
the other workflow notes. Also reviewed the linked chaining patterns, recipes and Atuin reference.
This is a targeted documentation review, not a fresh certification of every historical experiment.

Seventeen existing notes were updated. Historical timings, transcripts and original proof records
remain dated evidence. Generated runbook/catalogue outputs and running services were not regenerated
or changed. No build, mutation campaign, trigger, respawn, container creation/destruction, history
import, history replay or cleanup procedure was launched by this review.

## Changes applied

| Area | Correction or operational addition |
|---|---|
| Workflow index and master index | Daily cycle: project scope → owned scratch → bounded work → verification → handoff → intentional retirement. Original 156-record sample identified as historical. |
| Workflow recipes | Correct Atuin file-path input and `full-text` spelling; review before captured-script execution; compiler status preserved through formatting; aggregate history analysis replaces raw `/tmp/hist.txt`; unique schema scratch; worktree `.git` files included; R11 covers workload handoff. |
| Chaining patterns and Atuin reference | Removed direct history-to-shell execution; distinguished record framing from execution safety; current watcher result from a fresh gate; preview labels from actual effects. |
| Cascade | Installed ready-stage pool has no configurable concurrency cap; `--seq` and bounded groups are current options, while a general cap remains implementation work. |
| Triggers | Default four-second poll still runs probes under `--dry-run`; debounce reduces action frequency, not probe cost. Existing build probe remains unchanged. |
| Reactor | Intentional closure can be respawned; no explicit per-service suspension mechanism found in the inspected logic. Dry-run still observes/logs; server dependency and restart explanation corrected. |
| Runbooks | Atuin bodies are inspectable; export generates material but does not install/synchronise both entry points. Dry-run executes preconditions. Examples require exit status as well as content, with retry-step limitations documented. |
| Sandbox | Worker/output ownership and fixed-name replacement explained; defaults are not large-build recommendations. Both SELinux `z` and `Z` relabel, independently of `ro`; the earlier blanket rule was corrected against upstream docs. |
| Profiling, Arena and gate | Peak memory, I/O and scratch observations accompany timing; watcher reads still need freshness; running builds/tests is not passive read-only inspection. |
| Diagnostics, weight matrix and cold builds | Compiler status, duplicate build cost, per-copy isolation and NVMe scratch retained as distinct concerns. |
| Luke's findings | Added workflow integration and directly confirmed the HEE runner's six jobs, NVMe temporary path and removal of inherited target-directory settings. |

## Source checks and unresolved implementation limits

Source hashes and the note inventory are in [review-inputs.json](review-inputs.json). The reviewed
local implementations were `~/.local/bin/habitat-{cascade,trigger,reactor,sandbox,runbook}`, Arena's
`cascades/triggers.toml`, and `repos/herdr-engineering-engine-v2/scripts/mutants.py`.

| Source observation | Consequence |
|---|---|
| Cascade pool uses the number of ready stages; sandbox fanout uses all task pairs | Do not invent a `--jobs` flag or assume a host-wide queue exists. |
| HEE runner requests six mutation jobs and owns temporary/target policy | Outer fleet width can multiply this concurrency; Cargo build jobs alone do not cap mutation jobs. |
| Runbook preconditions run before the dry-run branch | Inspect definitions before calling a preview a read-only operation. |
| `[verify]` supports explicit `expect_rc`; retrying steps with content expectations omit an exit requirement | Updated examples use supported checks. A general executor fix was not made; unsupported step fields are not a remedy. |
| Trigger probe executes before the dry-run action suppression | An unused trigger can still cause repeated compiler work. |
| Reactor compares expected foreground processes and respawns eligible idle panes | Demand-based shutdown needs an intentional-stop policy and ownership. |
| Sandbox create forcibly replaces its fixed-prefix names | Separate output directories alone do not permit independent concurrent runs. |

The local `systemd.unit(5)` manual was checked for dependency semantics. The upstream site could
not be read in this pass; the installed manual supplied the check. SELinux advice was checked
against [Podman's volume documentation](https://docs.podman.io/en/latest/markdown/podman-run.1.html).
Installed Atuin help confirms `scripts get -s`; its search/version receipt from the preceding audit
is in [[40 Reference/lukes-workflows/2026-09-06/README|the resource evidence bundle]].

The unresolved high I/O-pressure signal remains an investigation item from that audit. These
documentation changes neither diagnose it nor demonstrate runtime resource savings.

## Validation and review materials

- [changes.patch](changes.patch) contains the reviewable before/after patch for the 17 existing notes.
- [validation.json](validation.json) records link/heading, Markdown fence, Bash syntax and TOML checks;
  a simulated failing compiler verifies that the documented pipeline preserves its failure status
  while still printing the diagnostic. No real compiler or project test suite is run by that check.
- [validate-review.py](validate-review.py) is the focused validation script. It executes only its own
  simulated compiler function for the pipeline check; other shell examples are parsed, not run.
- [SHA256SUMS](SHA256SUMS) verifies this receipt bundle. Living notes are represented by the patch
  and recorded after-hashes; they may change later.

Archived commands and prior habitat prose remained evidence, not instructions to activate. The
bundle contains authored documentation/validation and source hashes; no old environment or agent
configuration was imported.
