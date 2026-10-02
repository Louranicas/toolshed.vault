---
tags: [toolshed, workflow, ground-truth, code-anchors, drift, verified]
built: 2026-09-03
source: ~/fedora-arena/scripts/audit/codeanchors.py
---

# ⚓ Code Anchors — Notes That Land on Source

<!-- habitat-highways:2026-09-08:start -->
## Corpus insight routes — 2026-09-08

Curated navigation added in this edition; the dated claims and evidence below retain their original scope.

| Purpose | Route |
|---|---|
| Keep claims tied to their owner | [Synergy - Source-Owned Status and Memory](obsidian://open?vault=herdr-fedora-habitat.vault&file=80%20Architecture%2FSynergy%20-%20Source-Owned%20Status%20and%20Memory) · [file](</var/mnt/STORAGE-10TB/fedora-obsidian-vaults/herdr-fedora-habitat.vault/80 Architecture/Synergy - Source-Owned Status and Memory.md>) |
<!-- habitat-highways:2026-09-08:end -->


> **⚓ Code anchor** — `~/fedora-arena/scripts/audit/codeanchors.py:31` · expects `ANCHOR = re.compile`
> The anchor grammar itself. If this pattern changes, every anchor in every vault changes with it.
> *Verified 2026-09-03 · re-check `just doc-anchors`; this note updates when the code does.*

**The codebase is the source of truth. A vault note is a *claim* about it.** Claims rot silently
when the thing they describe moves, and a documentation set nobody can falsify is decoration.
This is the mechanism that keeps the four vaults honest.

## The format

```
> **⚓ Code anchor** — `PATH:LINE` · expects `EXACT FRAGMENT`
> <one line: what this note claims that this code decides>
> *Verified YYYY-MM-DD · re-check `just doc-anchors`*
```

`~` and `$REPOS` expand. **The `expects` fragment is the load-bearing part.** Verifying only that
a path exists proves nothing — the file survives every refactor that moves the thing it documents.
The fragment is searched for, which gives three outcomes rather than two:

| verdict | meaning | action |
|---|---|---|
| **OK** | fragment is on the stated line | none |
| **DRIFTED** | fragment moved within the file | `just doc-anchors-fix` rewrites the line number |
| **BROKEN** | fragment is **gone** | the note describes something that no longer exists — rewrite or retire it |

That third row is the point. A drifted line is bookkeeping; a broken anchor is a **false claim**
sitting in a vault.

## The standing rule

> **After any deployment or code change, run `just doc-anchors` and update the affected notes in
> the same pass.** Documentation is not downstream of a deploy — it is part of it.

Codified in `~/CLAUDE.md` § *Writing things down*, and enforced as a stage in
`cascades/assimilation.toml` (W3), so a cascade that ships also checks that the vaults still
describe reality.

```bash
just doc-anchors        # verify all four vaults; exit 1 on drift or breakage
just doc-anchors-fix    # repair drifted line numbers (BROKEN still fails)
just doc-anchors-json   # W5 review via jqp / tuicr
```

## Where the anchors are, and why there

Anchors are placed at **strategic points only** — a note that makes a load-bearing claim the code
decides. Not every note; a link on every page is noise, and noise gets ignored.

| Vault | Note | Anchored to | The claim the code decides |
|---|---|---|---|
| herdr | Habitat Service Bridge | `habitat:142` | the **two doors** are exactly two functions |
| herdr | Habitat Automation Stack | `habitat-cascade:107` | the wave scheduler behind every speed-up quoted |
| herdr | herdr Event Bus | `repos/herdr/…/events.rs:343` | the envelope shape, from herdr's own schema |
| herdr | Habitat Factory Prototype | `forge-cli/dispatch.rs:171` | the apply→verify loop |
| toolshed | 00 - Habitat Toolkit | `habitat-sandbox:60` | `:ro,z` — the isolation guarantee in one option |
| toolshed | Assimilation | `detectors/contract.py:37` | the detector contract, enforced at load |
| toolshed | Forge | `forge-spec/lib.rs:447` | deterministic build order + cycle rejection |
| toolshed | MCP Servers | `mcp2.py:116` | `server/discover` replaces `initialize` |
| toolshed | atuin | `repos/atuin/…/scripts.rs:33` | `--script` is a `PathBuf` — the type is the proof |
| kinoite | Podman & Containers | `forge/sandbox/Containerfile:11` | the missing linker, and its one-line fix |
| my-diary | Why I Stopped Trusting Green | `forge/clippy.toml:11` | P3 made structural |
| my-diary | The Antipattern Registers | `detectors/run.py:33` | the refusal that makes a clean scan mean something |
| my-diary | 00 - Principles | `forge-socket/lib.rs:300` | P3 in executable form, `+ 1` sentinel and all |
| my-diary | The Corpus of Me | `codeanchors.py:25` | the minimum viable "mark a claim stale" |

**14 anchors · 0 broken · 0 drifted** as of 2026-09-03.

## Proven, not asserted

The auditor was tested against a negative control before being trusted: the anchored line in
`forge-socket` was deliberately shifted by one, and the checker reported
`DRIFTED … moved 300 -> 301`, exit 1. `--fix` repaired it; restoring the source and re-running
returned it to 300. A checker that has never been shown to fail is not a checker —
[[Assimilation - Rules That Fire|the same contract the detectors carry]].

Related: [[Assimilation - Rules That Fire]] · [[Documented Surface and Source]] ·
[[Knowledge Audit]] · [[00 - Field Findings]] · [[Forge - Deployment Framework]] ·
[[00 - Toolshed Index]] · [[MCP Servers]] · [[Axiom Conformance]]

## Primary source routes — 2026-09-08

- [arena: scripts/audit/codeanchors.py](</var/home/Louranicas/fedora-arena/scripts/audit/codeanchors.py:42>) — Exact-fragment source-anchor checking; documentary link resolution alone cannot prove a behavioral claim.

> **⚓ Code anchor** — `/var/home/Louranicas/fedora-arena/scripts/audit/codeanchors.py:67` · expects `def check(path, line, frag):`
> [IFP] Source inspected for this route; no new behavioral or deployment verdict.

