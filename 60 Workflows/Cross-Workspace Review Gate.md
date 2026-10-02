---
tags: [toolshed, workflow, gate, W2, W3, W4, W5]
created: 2026-09-02
updated: 2026-09-06
source: fedora-arena/scripts/review-gate.sh
chain: W2 → W3 → W4 → W5
---

# Cross-Workspace Review Gate

<!-- habitat-highways:2026-09-08:start -->
## Corpus insight routes — 2026-09-08

Curated navigation added in this edition; the dated claims and evidence below retain their original scope.

| Purpose | Route |
|---|---|
| Cross the vault family by intent | [LLM Traversal - Cross-Vault Routes](obsidian://open?vault=herdr-fedora-habitat.vault&file=80%20Architecture%2FLLM%20Traversal%20-%20Cross-Vault%20Routes) · [file](</var/mnt/STORAGE-10TB/fedora-obsidian-vaults/herdr-fedora-habitat.vault/80 Architecture/LLM Traversal - Cross-Vault Routes.md>) |
| Follow the learning cycle | [Corpus Insights - Thematic Analysis](obsidian://open?vault=herdr-fedora-habitat.vault&file=80%20Architecture%2FCorpus%20Insights%20-%20Thematic%20Analysis) · [file](</var/mnt/STORAGE-10TB/fedora-obsidian-vaults/herdr-fedora-habitat.vault/80 Architecture/Corpus Insights - Thematic Analysis.md>) |
| Bind two views to one subject | [Synergy - Human and Agent Evidence Views](obsidian://open?vault=herdr-fedora-habitat.vault&file=80%20Architecture%2FSynergy%20-%20Human%20and%20Agent%20Evidence%20Views) · [file](</var/mnt/STORAGE-10TB/fedora-obsidian-vaults/herdr-fedora-habitat.vault/80 Architecture/Synergy - Human and Agent Evidence Views.md>) |
<!-- habitat-highways:2026-09-08:end -->


One command that asks all four workspaces whether a change is ready, and returns a single
verdict. It runs builds and tests, which write outputs and can execute project code; it is not
a passive resource snapshot. It does not itself mean a change has been approved or published.

Use it at an intentional review boundary. Give the build/test worker owned scratch and preserve
the underlying exit status when formatting its output. Repeated health polling should not rerun
this entire gate. A current watcher can help orientation but does not replace this gate's required
checks. See [[60 Workflows/00 - Workflows#Daily operating cycle — reviewed 2026-09-06|the daily cycle]].

## Usage

```bash
just gate                      # against the default base
just gate base=main
atuin scripts run gate -v repo=/path -v base=master
```

## What each workspace contributes

| W | Question | Source |
|---|---|---|
| **W2** | does it compile · do tests pass · what does clippy say | `cargo check --message-format json`, `cargo test`, `cargo clippy` |
| **W3** | is the diff annotated · **has a human weighed in** | `hunk session review --include-notes --json` |
| **W4** | is the machine healthy · how many TODOs | `/proc/loadavg`, `/proc/meminfo`, `podman ps` (via `flatpak-spawn --host`), `rg -c 'TODO\|FIXME'` |
| **W5** | is the wider repo fleet clean | `repo-fleet-status` |

## The verdict ladder

```
BLOCKED: build errors        errors > 0
BLOCKED: no passing tests    tests == 0
HOLD:    diff not reviewed   notes == 0
HOLD:    no human note yet   human == 0        ← the interesting one
READY (with N lint(s) noted) lints > 0
READY
```

**"No human note yet" is the rung that matters.** An agent can annotate a diff exhaustively and
that is still not review — the gate refuses to call it ready until a *person* has left a note.
Agent output is evidence, not approval.

## Sample output

```json
{
  "W2_build":  {"errors": 0, "tests_passed": 5, "clippy_lints": 0},
  "W3_review": {"notes": 4, "agent": 3, "human": 1, "files_changed": 2},
  "W4_system": {"load1": 0.46, "mem_avail_gb": 81.4, "containers": 1, "todos": 1},
  "W5_fleet":  {"dirty_repos": 3},
  "gate": "READY"
}
```

## Proven to actually block ⭐

A gate that only ever says READY is decoration. Both negative paths were injected and observed:

| Injected | Verdict |
|---|---|
| `let n: String = v.len();` | `{"errors": 6, …, "gate": "BLOCKED: build errors"}` |
| `assert_eq!(total(&[1,2,3]), 7)` | `{"errors": 0, "tests_passed": 0, "gate": "BLOCKED: no passing tests"}` |

**Test the failure path of anything that claims authority.**

## Composite form

```just
review base=BASE: check annotate-all (gate base)
```
`just review` = build ▶ annotate ▶ coverage ▶ gate. One verb, four workspaces, ending in a verdict.

> [!warning] This gate reads hunk JSON, which truncates through a pipe
> `hunk … --json | jq` is capped at one 64 KiB buffer ([[00 - Field Findings|F66]]), so on a
> large diff the W3 block fell back to `{"notes":0,...}` and a **reviewed** diff reported
> `HOLD: diff not reviewed`. Now captured to a file first. The `human` count keys on
> `author`, which is correct — `comment list --json` has no `source` field at all
> ([[00 - Field Findings|F69]]), so filtering on it would have counted agent notes as human
> and defeated this gate's most important rung. Measured by
> [[Weight Matrix - Which Gate Bore the Weight]].

Related: [[Weight Matrix - Which Gate Bore the Weight]] · [[Fabric Habitat 90-Point Promotion and Practice]] · [[Bridge - Diagnostics to Review]] · [[Bridge - Coverage to Review]] ·
[[00 - Workflows]] · [[00 - Toolshed Index]] · [[Arena Practice Ground]] · [[Cascade Engine]] ·
[[Runbooks]]

## Primary source routes — 2026-09-08

- [arena: scripts/review-gate.sh](</var/home/Louranicas/fedora-arena/scripts/review-gate.sh:25>) — Review-input acquisition and readiness composition; the existing script runs builds/tests and is not passive polling.

> **⚓ Code anchor** — `/var/home/Louranicas/fedora-arena/scripts/review-gate.sh:25` · expects `hunk session review --repo`
> [IFP] Source inspected for this route; no new behavioral or deployment verdict.

