---
tags: [workflow, mitigation, friction, hooks, insights, plan]
created: 2026-09-14
source: Claude Code Insights, 2026-09-01 → 2026-09-13 — 203 messages, 8 sessions analysed, 102 h
status: P1–P2 BUILT, controlled and LIVE (2026-09-14) · P3/P5/P6 held with reasons · P4 needs Luke's decision
verified: habitat-reflex verify → reflexes=8 unproven=0 · apply → installed=8 · doctor → drift=0 · both fired in production
---

# 🛠️ Mitigation Plan

The plan against the friction the [[Insights Reports - Opening Them Past the Sandbox|insights
report]] measured. One row per issue class, each with a mechanism, a cost, a control, a falsifier
and an owner — because a mitigation without those four is a recommendation, and this habitat has
measured that recommendations do not bind ([[Claim-Time Guard]]).

## What the report measured

```
Buggy Code 17 · Wrong Approach 5 · Permission Blocked 3 · Destructive Action 1
Environment Issues 1 · Misunderstood Request 1          (28 events / 203 messages / 102 h)
```

**The friction is in the agent's throwaway scripts, not in the codebase** — 17 of 28. So the
mitigation targets *authoring*, not the repository.

## The corroboration worth recording

The report's seventeen "buggy code" incidents map onto entries already written independently in
`my-diary.vault` → `Mistakes I Made`:

| report's shape | my register |
|---|---|
| an edit that silently did nothing | #15 |
| a job that continued past a failed step | #30 |
| checks chained to a commit | #36 |
| `grep -c` emitting a false "done" | #38 |
| a negative control that measured the real vault | #39 |
| a verdict taken from a pipe | #44 |

An outside reader, with no access to that vault, named the same failure modes. That is
[[Assimilation - Rules That Fire|cross-family review]] passing: the diagnosis is not self-flattery.
It is also the first time anything here has been checked by a reader that is not me.

## Status before the plan — what is already mechanised

| class | n | mechanism today | verdict |
|---|---|---|---|
| Buggy code | 17 | `commit-chain-guard` (#36) · `gate` + `pipe-verdict-guard` (#44, with a known gap) · `control-change-guard` + `selftest` (#39) | **PARTIAL** — 3 of ~7 shapes |
| Wrong approach (scope) | 5 | none — Mistakes #41 recorded; deferral `⏳ owner=luke expires=2026-09-25` | **OPEN** |
| Permission blocked | 3 | none — procedural | **OPEN** |
| Destructive action | 1 | **prose only** in `~/CLAUDE.md`; verified: six reflexes, none covers `rm` | **OPEN** |
| Environment (404, silent chmod) | 1 | none | **OPEN** |
| Misunderstood request | 1 | — | no action: 1 in 203 |

Uncovered shapes inside the dominant class: an incomplete refactor crashing 31 minutes in ·
`grep -c` count-vs-status · unescaped backticks and `${PIPESTATUS}` inside heredocs · a variable
reassigned after argument parsing · an edit landing in the wrong function.

## The plan

### P1 · Syntax-gate on write — ✅ **BUILT, INSTALLED, FIRED LIVE** (2026-09-14)

A `PostToolUse` reflex on `Write|Edit`: `bash -n` for `*.sh`, `python3 -m py_compile` for `*.py`.
Catches the broken script **at authoring time**, before it is pointed at anything that takes
31 minutes to fail.

- **Measured constraint:** `shellcheck`, `ruff` and `pyflakes` are **ABSENT** on this machine;
  `bash` and `python3` are present. So this uses only what is here. Installing `shellcheck` into the
  toolbox would strengthen it and is a separate decision.
- **Cost:** ~40 lines on the existing reflex surface. **Control:** a deliberately broken script must
  trip it; a valid one must stay silent. **Falsifier:** 30 days — never fired ⇒ delete.
- **Closes:** the 31-minute crash, most heredoc-escaping defects, some wrong-place edits.

**As built** — `~/.claude/hooks/lint-on-write.sh`, `PostToolUse` on `Write|Edit`, non-blocking,
fails open on every path. `bash -n` for `*.sh`/`*.bash`, `ast.parse` for `*.py`; it detects
`shellcheck`/`ruff` on `PATH` and upgrades to them automatically the moment either is installed,
and says so in its own message while they are absent.

**Proof, in production, through the real tool** — a deliberately broken script written with the
Write tool:

```
⚠ SYNTAX_ERROR — live-probe.sh does not parse (bash -n)
  live-probe.sh: line 6: syntax error: unexpected end of file from `if' command on line 4
```

**The control was wrong first, and bash settled it.** My first fixture was
`if [ -z "$x" ; then` — which **bash parses happily** (`bash -n` rc=0); it fails at *runtime* with
``[: missing `]'``. So the control asserted a syntax error over an input that has none, and the
detector's silence was correct. Establishing which side was wrong from a source outside both
(Mistakes #40's rule, and the reason `control-change-guard` exists) meant asking bash, not editing
until green. Replaced with an unterminated `if`, verified `bash -n` rc=2. **The requirement never
moved; only the input did** — and the three premises for that change are recorded in the hook's own
header.

**The ceiling that mistake exposed, stated rather than hidden:** `bash -n` would not have caught
`[ -z "$x" ;` either. A missing `]` is a runtime fault; `shellcheck` catches it, `bash -n` cannot.
**The gap between what this hook checks and what actually breaks scripts is exactly the size of the
missing linter** — which makes L1 below a measured request, not a preference.

### P2 · Destructive-command guard — ✅ **BUILT, CONTROLLED, FIRED LIVE** (2026-09-14)

A `PreToolUse` reflex on Bash: on `rm -rf` / `rm -fr` / `git clean -fd` / `find … -delete`, run
`git ls-files <target>` and **name the tracked files that would be lost**. Non-blocking, like every
other guard here.

- **Why it is overdue:** the rule exists in `~/CLAUDE.md`, in the insights report's top
  recommendation, and in Mistakes #20 — *three places, and it has never once executed*.
- **Cost:** ~50 lines + control. **Control:** an `rm -rf` over a directory containing a tracked file
  must fire and name it; the same command over an untracked temp dir must stay silent.
  **Falsifier:** 30 days — fires only on safe deletions ⇒ it is a tax, delete it.

**As built** — `~/.claude/hooks/destructive-guard.sh` + `destructive_guard.py`, `PreToolUse` on
`Bash`, warns and never blocks. It reads **two declarations neither of which it invents** (F65 — an
include list I maintain is a promise; a declaration the world maintains is a mechanism):

1. `~/.config/habitat/corpus-sources.json` — the 13 roots `habitat-corpus-backup` already calls
   irreplaceable, **and, in the same file, each root's `excludes`**, which is the habitat's own
   declaration of what is *disposable* (`target/`, `cache/`, `__pycache__/`, `node_modules/`). One
   file answers both sides, so the quiet case is declared rather than guessed.
2. `git status --porcelain` over the target — which separates what git can restore from what it
   cannot.

**Where it departs from this plan, and why.** The plan said *"name the tracked files that would be
lost"*. As built it does **not** fire on a tracked-and-clean tree: `git checkout` brings those back,
so calling them "lost" would be a false alarm, and a guard that reddens correct work is one the team
routes around (F121) — which is how quality falls so a gate can stay green. It fires on what is
genuinely unrecoverable — untracked-not-ignored, modified-uncommitted, or inside a corpus root — and
reports the restorable count as reassurance rather than as an alarm. The plan's control still holds
verbatim, using a *modified* tracked file.

**Ten rules, fourteen cases, and every rule proven load-bearing.** The rules are enumerated from the
detector's **own docstring**, so a rule added without a case refuses. Then each rule was neutered in
a *copy* and the control required to go red:

```
rules=10/10 cases=14/14 uncovered=0 orphan=0   verdict=PASS
neutered=10 killed=10 survived=0               verdict=PASS every rule is load-bearing
```

The control found **three defects before installation**, which is the entire argument for building
it first: two in the hook (see [[50 Field Notes/00 - Field Findings#F146 · A script that resolves its own dependencies through `$HOME` is untestable — and degrades silently|F146]])
and one in the control itself — `Q3` survived its neuter because its fixture was kept quiet by a
*neighbouring* rule rather than by Q3 (F125b).

**Measured discrimination on real command shapes** — the false-positive check, because a false
positive is the invisible failure:

| command | verdict |
|---|---|
| `rm -rf $HOME/.cache/hee-target` · `rm -rf ~/fedora-arena/target` · `rm -f file` · `ls -R` | **silent** |
| `rm -rf ~/.claude/hooks` | UNRECOVERABLE — *inside `agent-memory`, 13 entries* |
| `rm -rf …/my-diary.vault` | UNRECOVERABLE — *inside `vaults-obsidian`, 38 entries* |
| `rm -rf …/fedora-obsidian-vaults` | ☠ CATASTROPHIC — *IS the `vaults-obsidian` root* |
| `git clean -fdx` from `$HOME` | ☠ CATASTROPHIC — *names all 10 corpus roots it would erase* |

Cost on the quiet path: **~28 ms**. Fired live in production the minute it was installed, and did
not block the deletion.

**Two blind spots, stated now rather than discovered later.** `rm -rf "$d"` — a target held in a
shell variable is opaque to anything that does not execute the shell; the guard sees the literal
`$d` and stays silent. And a symlink is judged by its own path, because `rm -rf link` removes the
link. Neither is fixable without running the command, which is the one thing a pre-execution guard
must not do.

### P3 · Count-vs-status detector — **held**

`grep -c` returning `0` with exit 1, and `$(cmd || echo 0)` — Mistakes #38. A new detector module
plus a reflex. Medium value, medium cost. **Held until P1 and P2 have run a week**, so the reflex
surface is not grown three at a time on one day's evidence.

### P4 · Scope declaration — **needs Luke's decision** (`⏳ owner=luke expires=2026-09-25`)

A declared in-bounds path set, and a guard that warns when a heavy command runs outside it. It is
the mitigation for the five scope-drift events and for Mistakes #41. **Not invented unilaterally**:
it needs a convention that does not exist, the noise risk is real, and inventing the convention
would be the same overreach in a new costume.

### P5 · Privileged-step batching · P6 · URL preflight — **held**

Procedural and rare respectively. Better as a skill that emits one `sudo` block at the start of
environment work than as a guard. The COPR 404 and the silent `chmod` are one event each in 102
hours; a mechanism for each would cost more than they do.

## What will deliberately NOT be built, and why

- **A test-suite requirement for every helper script** — the report's headline "on the horizon".
  Most of these scripts are genuine one-shots; a rule demanding fixtures for throwaway code gets
  routed around (F121), and P1 captures most of the value at a fraction of the cost.
- **Widening `pipe-verdict-guard`** to catch `… | head; echo rc=$?`. It cannot be distinguished from
  the legitimate `cmd | tee log; echo $?`. Mistakes #44's conclusion stands: the fix is *using*
  `gate`, not a broader pattern that reddens correct work.
- **Parallel adversarial subagents.** It multiplies load on a machine other agents are building on —
  Mistakes #41, three days old.

## Sequencing

1. ~~**P1 and P2** — build control-first, install through `habitat-reflex`.~~ ✅ **DONE 2026-09-14.**
   `habitat-reflex verify → reflexes=8 unproven=0` · `apply → installed=8` · `doctor → drift=0`.
   The foreign herdr hook was preserved, not owned. Both fired in production the same turn.
2. **One week of running**, then re-read the falsifiers: a guard that has fired only on correct work
   is deleted, not tuned.
3. **P3** only if the week produces a count-vs-status incident.
4. **P4** on Luke's word.

### L1 · Install `ShellCheck` + `python3-ruff` — **needs Luke's password** (the one open item)

```bash
toolbox run sudo dnf install -y ShellCheck python3-ruff
```

Both are packaged for `fedora-toolbox-44` (`ShellCheck 0.11.0`, `python3-ruff 0.16.6`) and neither
is installed. **P1 already uses them the moment they appear on `PATH`** — no further work, no change
to the hook. This is not a preference: the fixture mistake above proved that the defect class P1 was
built for (`[ -z "$x" ;`) is *outside* what `bash -n` can see and *inside* what shellcheck sees.
Record it in `~/.local/bin/toolbox-bootstrap` so it survives a container rebuild.

## Scoreboard, 2026-09-14

| class | n | before | now |
|---|---|---|---|
| Buggy code | 17 | PARTIAL — 3 of ~7 shapes | **PARTIAL+ — syntax caught at authoring time, every `.sh`/`.py` written** |
| Destructive action | 1 | prose in three documents, zero mechanisms | **MECHANISED — enumerates, names the corpus roots, never blocks** |
| Wrong approach (scope) | 5 | OPEN | OPEN — P4, `⏳ owner=luke expires=2026-09-25` |
| Permission blocked | 3 | OPEN | OPEN — P5 held, procedural |
| Environment | 1 | OPEN | OPEN — P6 held, one event in 102 h |
| Misunderstood request | 1 | — | no action: 1 in 203 |

Reflex surface: **8 reflexes, `unproven=0`, `drift=0`.** Two of the eight are new today.

Related: [[Insights Reports - Opening Them Past the Sandbox]] · [[Claim-Time Guard]] ·
[[Assimilation - Rules That Fire]] · [[00 - Workflows]] · [[00 - Toolshed Index]] ·
[[50 Field Notes/00 - Field Findings]] ·
[Deploying the Diary's Learnings § Move 9](obsidian://open?vault=herdr-fedora-habitat.vault&file=50%20Automation%2FDeploying%20the%20Diary%27s%20Learnings) — the deployment record for P1 and P2 ·
[my-diary § Mistakes I Made](obsidian://open?vault=my-diary.vault&file=Reflections%2FMistakes%20I%20Made)

---

## Successor — 2026-09-22

The next usage report (41 sessions, 2026-09-01..22) was assimilated the same way, and its finding
set had moved: `buggy_code` rose from 17 incidents to **35** and stayed the largest category,
still "almost all self-inflicted" — the agent's own throwaway orchestration scripts. P1/P2 here
(`lint-on-write`, `destructive-guard`) catch a *syntax error* and a *destructive glob*; they cannot
catch a swallowed exit code inside a script that parses fine.

The answer that round was a **tested primitive library** rather than another detector —
`~/agent-harness`, 16 cases with 16 negative controls — plus four reflexes taking the habitat to
`reflexes=15 unproven=0 drift=0`, and six recommendations **refused** because the rules they
proposed writing down were already firing at the keystroke.

→ [Usage Report Assimilation 2026-09-22](obsidian://open?vault=herdr-fedora-habitat.vault&file=50%20Automation%2FUsage%20Report%20Assimilation%202026-09-22)
· new findings [[00 - Field Findings|F156–F158]]
