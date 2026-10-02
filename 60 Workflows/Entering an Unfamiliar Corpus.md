---
tags: [workflow, corpus, verification, skills, hooks, atuin, runbook, verified]
created: 2026-09-17
status: LIVE — 4 skills, 2 atuin scripts, 2 hooks, 1 runbook, 3 just recipes; all proven to fire
---

# 🧭 Entering an Unfamiliar Corpus

The procedure for the first hour with a large body of work you did not write — a repo, a vault, a
planning tree. It exists because on 2026-09-17 I produced **six confident findings about one corpus
and every one was an artefact of my own measurement**
([[50 Field Notes/00 - Field Findings#F148 · Six ways a corpus link or coverage measurement returns a confident false verdict|F148]],
[my-diary § Mistakes #46](obsidian://open?vault=my-diary.vault&file=Reflections%2FMistakes%20I%20Made)).

> **The governing rule.** A corpus built over weeks that documents its own gaps and ships its own
> checker is *not* the suspect. The instrument you wrote sixty seconds ago is. When two checkers
> disagree, that is a finding **about the checkers**.

## The order, cheapest first

```bash
just corpus-recon <path>                # seconds — shape, before reading anything
just layer-trace  <vault>               # link reciprocity, all six traps handled
habitat-runbook run corpus-entry        # the whole procedure, with preconditions

# just takes recipe arguments POSITIONALLY (manual, "Recipe Parameters": `just test server unit`).
# `name=value` on a just command line is a VARIABLE OVERRIDE, a different mechanism — verified:
#   just --evaluate root=/tmp
#   error: variable `root` overridden on the command line but not present in justfile
# So `just corpus-recon root=/tmp` passes the literal string as the positional arg. atuin is the
# opposite and DOES want the name: `atuin scripts run layer-trace -v root=<p>` with `{{ root }}`
# in the script. Verified on just 1.57.0; `{{x}}` and `{{ x }}` are both valid interpolations.
```

| Step | Skill | Question it answers |
|---|---|---|
| 1 · **broad** | `corpus-recon` | how big, how much is generated, what is the ID scheme, how does it cross-reference |
| 2 · **deepen** | `layer-trace` | who owns which fact, does every link come back, which "defects" are declared design |
| 3 · **parallel** | `workspace-cluster` | fan one question across W1–W5 in a single round; read a resident TUI's screen instead of re-running its work |
| 4 · **hone** | `hee-v3-corpus` (or the corpus's own module cards) | one subject, end to end |
| 5 · **before speaking** | `claim-discipline` | what input earns this verdict, and who checked it |

**Never skip step 1.** A `generated: 72%` reading means the projections have one owning record —
find *that* and audit it, rather than auditing five hundred notes downstream of it.

## What the recon tells you, and what to do with it

| Signal | Read it as |
|---|---|
| high `generated%` | audit the generator, not the projection |
| ID prefixes (`HEE3-`, `TASK-`, `UM-`, `F2-`) | the spine of every cross-reference — learn these first |
| `wikilink` count **0** in a codebase | the corpus addresses other vaults by `obsidian://` on purpose; that boundary is enforced |
| many `file://` links | it points outside itself — **verify the target from the right filesystem layer** |
| large duplicate bytes | ask whether the corpus *declares* the redundancy before calling it waste |

## The six traps, and why they are not a checklist

They are hooks, because a rule I have read is not a rule operating on me
([[60 Workflows/Claim-Time Guard]]):

- **`host-path-guard`** — a `/var/home/<sibling>` path read from inside the toolbox. An unmounted
  path and a missing path are byte-identical and neither names the layer. `cases=11/11`,
  `neutered=5 killed=5`.
- **`corpus-measure-guard`** — the *shape* of the measurement: wikilink parsing without the
  escaped-pipe (`[[A\|label]]` → `A\`) and code-fence fixes, first-match regex answering a
  membership question, counting breakage over a vault without splitting live notes from
  byte-preserved captures. `cases=14/14`, `neutered=7 killed=7`.

Both warn, neither blocks, and both fired in production the turn they were installed. The second's
live test is the lesson entire: it warned about the escaped pipe **in the same call whose output
printed `'A\\|label'`**.

## Proof it is wired, not just written

```
habitat-reflex verify → reflexes=10 unproven=0    doctor → drift=0
host-path-guard       cases=11/11   neutered=5 killed=5 survived=0
corpus-measure-guard  cases=14/14   neutered=7 killed=7 survived=0
layer-trace (v3)      verdict=PASS live_cross_vault_defects=0   38,642 links, 96% resolved
```

A green control proves a hook fires; only the **neuter sweep** proves each rule is load-bearing.

## Where the pieces live

| Piece | Path |
|---|---|
| Skills | `~/.claude/skills/{corpus-recon,layer-trace,workspace-cluster,hee-v3-corpus}` |
| Tools | `~/.local/share/corpus-tools/{corpus-recon,layer-trace}.py` |
| atuin | `atuin scripts run corpus-recon\|layer-trace -v root=<path>` |
| Hooks | `~/.claude/hooks/{host-path,corpus-measure}-guard.sh` |
| Runbook | `~/fedora-arena/runbooks/corpus-entry.toml` |
| Recipes | `just corpus-recon` · `just layer-trace` · `just corpus-entry` |

**atuin ground truth (18.12.1):** templates are `{{ var }}`, not `${var}` — a shell default becomes
atuin's cwd and walks your whole home. `delete` prompts (`yes | …`); `new` on an existing name
silently no-ops with `rc=0`. Re-read `atuin scripts get <name>` after registering.

## Falsifier, dated 2026-10-17

If neither hook has fired in a month, this class of error is not recurring and both are dead weight
— delete them. If either fires on measurements that were already correct, it is wrong about the
shape and should be deleted rather than tuned.

**Resume point for a new context window:** [habitat § Session State and Resume ▶ CONTINUE HERE](obsidian://open?vault=herdr-fedora-habitat.vault&file=00%20-%20Session%20State%20and%20Resume)

Related: [[Claim-Time Guard]] · [[Mitigation Plan]] · [[00 - Workflows]] · [[00 - Toolshed Index]] ·
[[50 Field Notes/00 - Field Findings]] ·
[v3 Quick Start](obsidian://open?vault=herdr-engineering-engine-v3.vault&file=Quick%20Start) ·
[my-diary § Mistakes #46](obsidian://open?vault=my-diary.vault&file=Reflections%2FMistakes%20I%20Made) ·
[Fedora Master Index](obsidian://open?vault=herdr-fedora-habitat.vault&file=00%20-%20Fedora%20Master%20Index)
