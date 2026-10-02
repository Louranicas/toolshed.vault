---
tags: [toolshed, skills, claude-code, progressive-disclosure]
created: 2026-09-02
location: ~/.claude/skills/
---

# 🎓 Authored Skills — the learnings, made loadable

**Five** Claude Code skills distilled from this habitat's field findings, workflows and — since
2026-09-03 — the reflection corpus of earlier instances. They live in
`~/.claude/skills/<name>/SKILL.md` and are captured by `habitat-settings-backup`.

| skill | always-loaded | deferred | progressive | owns |
|---|---|---|---|---|
| `claim-discipline` ⭐ | 57 | 232 | **80%** | when a result may be called true |
| `habitat-ops` | 83 | 240 | 74% | the W1–W5 cockpit: services, cascades, repair |
| `cli-ground-truth` | 74 | 135 | 63% | what a CLI actually does, before scripting it |
| `kinoite-containers` | 57 | 232 | **80%** | containers, immutability, sandbox builds |
| `vault-mining` | 63 | 191 | 75% | writing to the vaults, keeping the palace retrievable |
| **total** | **334** | **1030** | **76%** | |

**They route rather than repeat.** Every skill points at `claim-discipline` before a completion
claim; `claim-discipline` points at none of them, because it is the terminal authority on
judgement. One topic, one home — the same rule that governs `CLAUDE.md` / `CLAUDE.local.md` /
`my-diary.vault`, and it is why trimming duplication *shortened* three of them.

## Updated 2026-09-03 — what the session added

- **`habitat-ops`** — the `cockpit` MCP tools (`ws_check`, `ws_receipt`) now that the servers
  actually connect; the `just detect*` verbs; **kill by PID, not by pattern** (`pkill -f` matches
  your own shell — the `&&`-chain story was the symptom); never take a verdict from a pipe.
- **`cli-ground-truth`** — *"where the binary and the recorded **mechanism** disagree, probe
  again"*; **prove the failure path** (a link checker, a detector suite and an anchor auditor all
  passed their first run while one could not fire at all); **handshake, don't read**; ⚓ code
  anchors; a cloned repo can be *ahead* of the installed binary.
- **`kinoite-containers`** — no linker in the base toolbox image; `--mount` for toolchains living
  in `$HOME`; cold verification costs ~1.1 s so it is the default; **immutable OS does not imply
  reproducible builds**; mounting a foreign disk `ro`.
- **`vault-mining`** — the fourth vault; *bidirectional is checked, not asserted*
  (`backlinks.py`); hubs by **out-degree**, not filename; the basename-collision bug that made the
  checker resolve the wrong file; code anchors as rule 5.


## `claim-discipline` ⭐ (2026-09-03)

The judgment layer, and the one that was missing: everything else in this vault says *how to run
a tool*; this says **when a result is allowed to be called true**.

`SKILL.md` is 57 lines — four questions to ask before any completion claim, the verbs to run
instead of asserting, and five things never to do. 232 lines deferred to `reference/`
(**80% progressive disclosure**):

| reference | contents |
|---|---|
| `false-pass-family.md` | the nine ways a claim of "done" is false, each with detector + mirror; the **counter-evidence locator**; three shapes of instrument that over-report |
| `suppression-ladder.md` | four rungs, the test-specific rung-1 answers, and the flow-state checkpoint |
| `verification-mechanics.md` | cold-not-warm · exit-codes-not-pipes · seams-not-functions · limits at acquisition · doc-to-code anchors · cross-family review |
| `spellbook.md` | eleven inherited moves, each with a trigger and the scar that earned it |

Triggered before reporting anything done, clean, verified, wired or deployed — and before
suppressing a lint or trusting a green result.

## Updated 2026-09-03 (evening) - two rules that cost something to learn

- **`claim-discipline`** - `FP_UNMEASURED_PASS`: a check reporting `violations=0` while most of
  what it covers was never interrogated. Created *by a fix*, in the tool built to catch it. Every
  verdict now carries its denominator, and `UNMEASURED` is as red as a violation.
- **`cli-ground-truth`** - *never let a probe inherit stdin* (`capture_output` redirects stdout and
  stderr only; `jq` then blocks for the whole timeout), and *a large timing ratio is a structural
  claim* -- 37x is a fixed constant, not a load story. Both came from a mechanism I got wrong and
  published before probing.

## Progressive disclosure

Each skill is a lean `SKILL.md` plus `reference/` files read **only when needed**:

| Skill | SKILL.md | reference/ | Loads when |
|---|---|---|---|
| **`habitat-ops`** | 60 lines | 4 files, 205 lines | Workspace 1–5, panes, "is X running", respawn, cascades, sandboxes |
| **`kinoite-containers`** | 41 | 4 files, 167 | podman, bind mounts, `Permission denied` in a container, "will this survive a rebuild" |
| **`cli-ground-truth`** | 46 | 1 file, 101 | scripting an unfamiliar flag, suspicious zeros, hangs, docs vs behaviour |
| **`vault-mining`** | 42 | 2 files, 137 | editing any `*.vault`, cross-vault linking, `mempalace mine`, bad retrieval |

**76% of the material is deferred.** The always-loaded portion is 189 lines total; the depth
(610 lines) costs nothing until a task actually needs it. That ratio is the point — a skill that
inlines everything is just a large prompt.

## What each carries

**`habitat-ops`** — the two-door model (`habitat q` for a value, `habitat pane` for a screen), the
`✓`/`✗`/`·` distinction that stops a healthy shell service reading as a fault, and the fact that
panes survive a restart while processes do not. Deferred: safe pane driving, cascade authoring
with its four silent TOML/jq traps, sandbox fanout, and a **services table generated from the live
registry** so it cannot drift.

**`kinoite-containers`** — three rules (escape to the host, never install into `/usr`, `$HOME`
surviving ≠ durable). Deferred: `:z` vs `:Z` and why `:Z` cannot be used on a read-only mount;
the durability table and the uv/venv trap; BusyBox vs GNU; systemd user units for long-running
helpers.

**`cli-ground-truth`** — the most transferable. A symptom→cause→probe table (confident zeros ·
hangs · "succeeded but nothing changed"), a five-step method, and quick reflexes (`timeout 5` to
detect a stdin block). Deferred: 30+ verified traps grouped by symptom.

**`vault-mining`** — the four standing rules, including that cross-vault links must be
`obsidian://` URLs because a wikilink to another vault silently resolves to nothing. Deferred:
room-keyword semantics (they match the path *relative to the mined dir*), retrieval dilution and
its repair, the link-integrity checker, and note-shape conventions.

## Design choices worth keeping

- **Descriptions are trigger lists, not summaries.** They name the symptoms and phrases that should
  load the skill ("is X running", "Permission denied", "suspicious zeros"), because the description
  is what the decision is made on.
- **Skills cross-refer rather than duplicate.** `habitat-ops` sends container questions to
  `kinoite-containers` and flag-verification to `cli-ground-truth`. Each fact has one home.
- **Generated where possible.** `habitat-ops/reference/services.md` is built from
  `~/.config/habitat/services.json`, so it cannot drift from reality.
- **They encode failures, not just recipes.** The traps are the expensive knowledge; the happy path
  is usually discoverable from `--help`.

Related: [[00 - Habitat Toolkit]] · [[skills]] · [[00 - Field Findings]] · [[00 - Workflows]] ·
[[00 - Toolshed Index]] · [[MCP Servers]]
