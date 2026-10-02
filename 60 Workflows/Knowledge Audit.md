---
tags: [toolshed, workflow, audit, documentation, integrity]
created: 2026-09-02
source: fedora-arena/cascades/knowledge-audit.toml · scripts/audit/
updated: 2026-09-06
---

# 🔎 Knowledge Audit — testing the documentation like code

<!-- habitat-highways:2026-09-08:start -->
## Corpus insight routes — 2026-09-08

Curated navigation added in this edition; the dated claims and evidence below retain their original scope.

| Purpose | Route |
|---|---|
| Cross the vault family by intent | [LLM Traversal - Cross-Vault Routes](obsidian://open?vault=herdr-fedora-habitat.vault&file=80%20Architecture%2FLLM%20Traversal%20-%20Cross-Vault%20Routes) · [file](</var/mnt/STORAGE-10TB/fedora-obsidian-vaults/herdr-fedora-habitat.vault/80 Architecture/LLM Traversal - Cross-Vault Routes.md>) |
| Keep claims tied to their owner | [Synergy - Source-Owned Status and Memory](obsidian://open?vault=herdr-fedora-habitat.vault&file=80%20Architecture%2FSynergy%20-%20Source-Owned%20Status%20and%20Memory) · [file](</var/mnt/STORAGE-10TB/fedora-obsidian-vaults/herdr-fedora-habitat.vault/80 Architecture/Synergy - Source-Owned Status and Memory.md>) |
| Follow the learning cycle | [Corpus Insights - Thematic Analysis](obsidian://open?vault=herdr-fedora-habitat.vault&file=80%20Architecture%2FCorpus%20Insights%20-%20Thematic%20Analysis) · [file](</var/mnt/STORAGE-10TB/fedora-obsidian-vaults/herdr-fedora-habitat.vault/80 Architecture/Corpus Insights - Thematic Analysis.md>) |
<!-- habitat-highways:2026-09-08:end -->


**Navigation:** [[40 Reference/Command Matrix#Composition and verification routes|Command Matrix ⇄ composition routes]] · [[00 - Toolshed Index|Toolshed master index]]. Check note targets, source references and documentation freshness.

Every other cascade measures the **machine**. This measures the **knowledge about the machine**.
Documentation rots silently: nothing errors when a note goes stale, so the only defence is to test
it.

```bash
just rb-audit                                    # machine + knowledge, one procedure
habitat-cascade run cascades/knowledge-audit.toml
```

## The four checks

| check | asks | script |
|---|---|---|
| `undocumented` | is every locally-built tool mentioned in a vault? | `scripts/audit/undocumented.sh` |
| `orphans` | are there notes nothing links to? | `scripts/audit/orphans.py` |
| `deadpaths` | do notes cite filesystem paths that no longer exist? | `scripts/audit/deadpaths.py` |
| `drift` | does the **generated** services reference still match the live registry? | `scripts/audit/drift.py` |

Four parallel probes, joined into one verdict:
`undocumented=0 orphans=0 deadpaths=19 services-drift=0`.

## What it caught ⭐

**A genuinely broken symlink, silently broken for a day.** The audit flagged
`~/.local/bin/herdr-reviewr` as a dead path. First instinct was that the auditor was wrong —
`ls` showed the file there. It was a **broken symlink** pointing at
`.tmp-install-28276-…/checkout/bin/`, a temporary install directory cleaned up after the plugin
installed on 2026-09-01. `os.path.exists()` follows symlinks; `ls` does not. So the standalone
`herdr-reviewr` command documented in [the vault](obsidian://open?vault=herdr-fedora-habitat.vault&file=50%20Automation%2FPlugin%20-%20reviewr) had **never worked**.
Repointed at the real binary under the plugin root; it was the only broken link in `~/.local/bin`.

> `ls` showing a file is not evidence the file resolves. For symlinks, `test -e` is the check.

**It caught me.** Minutes after `habitat-runbook` was written, the audit reported
`undocumented=1`. Documenting it cleared the count to zero. The loop closes on its author.

## A false positive worth fixing

The first run reported **8 orphans** — all of them `40 Reference/help/*.md`, the verbatim `--help`
appendix that is *deliberately* unlinked and *deliberately* kept out of the palace. Counting them
buried the real signal.

> **An auditor that cries wolf gets ignored.** Excluding a known-intentional class is not
> weakening the check; it is what makes the remaining output worth reading.

Orphans: 0 after the exclusion.

## From counting to classifying to *reading the note* ⭐

`deadpaths` went through three designs, and the second was wrong in an instructive way.

**v1 — count.** Reported `deadpaths=19`. Nearly useless: most non-existent paths in these vaults
are *correctly* absent — a config file the tool creates on demand, a directory you author
yourself, a path behind the HEE-v2 gate that is deliberately not built. A number mixing rot with
intent is a number people learn to ignore.

**v2 — classify with a hardcoded allow-list.** Better output (`suspect: 0`), but the knowledge
lived **in the auditor** as a list of path prefixes. That drifts the moment a note changes, and it
gives the author of a claim no way to say *why* a path is absent. The auditor was asserting things
about notes it had no right to assert.

**v3 — read what the note declares.** The status moves to where the claim is authored:

```markdown
`~/.config/bacon/prefs.toml` *(created on demand by `bacon --prefs`)*
`~/.config/yazi/` *(user-authored; absent until you create it)*
`~/.local/state/hee` *(planned)*
`/home/louranicas/Indy_dev_dan` *(historical; prototype-era path on another machine)*
```

Recognised markers: **planned · created on demand · created when · user-authored · historical**.
Every one was *verified* before being written — `bacon --help` confirms `--prefs` creates the file;
`~/.config/yazi/` genuinely has no auto-creation. The markers are not auditor-appeasement; they make
the documentation **more accurate for a human reader**, which is why this is the right place for
them.

The only rule left in code is that **DBus object paths are not filesystem paths** — `/kglobalaccel`
and `/VirtualDesktopManager` merely look like files. That is a category error, not an exception, so
it belongs in the auditor.

Result: 21 unresolved paths, **0 suspect** — 2 DBus, 3 created-on-demand, 6 created-when-configured,
4 user-authored, 3 planned, 1 historical. Anything unresolved *and* undeclared is now genuinely
worth looking at: it is either rot, or a claim whose author has not said why.

> The general lesson: when a checker needs an exception list, ask whether the exception is really
> **knowledge the subject should carry about itself**. Move it there and the checker stops drifting.

## Why generation beats discipline

Two notes here are **generated from their subject**, not written about it:

- `habitat-ops/reference/services.md` ← the live service registry
- [[Cascade and Runbook Catalogue]] ← `cascades/*.toml` and `runbooks/*.toml`

The `drift` check exists to prove the first one stayed true (it reports `0`). The second cannot
drift by construction. **Where a document can be derived, derive it** — the alternative is relying
on someone remembering.

Related: [[Runbooks]] · [[Habitat Introspection]] · [[Cascade and Runbook Catalogue]] ·
[[00 - Field Findings]] · [[00 - Toolshed Index]] · [[00 - Workflows]] ·
[[Documented Surface and Source]] · [[Code Anchors - Notes That Land on Source]]
