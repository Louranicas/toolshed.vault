---
tags: [workflow, hooks, detectors, claim-time, verified]
created: 2026-09-04
status: LIVE — PreToolUse hook armed and proven to fire
---

# 🛡️ The Claim-Time Guard

A rule that fires only when you remember to invoke it is one notch better than a rule with no
detector at all. This is that notch, closed.

## The three-day problem

`PIPE_SWALLOWS_VERDICT` — taking a gate's verdict from a pipeline's last stage instead of the
gated command — recurred on **three consecutive days**:

| date | instance | caught by |
|---|---|---|
| 2026-09-02 | `cargo clippy … \| grep -qE "^(error\|warning)"` → "clippy OK" | reading the corpus, next day |
| 2026-09-03 | five instances while auditing exactly this class | `just detect-session`, at session end |
| 2026-09-04 | `just rb-audit 2>&1 \| tail -40; echo "rc=$?"` — the session's **first** command, quoted as evidence | `just detect-session`, at session end |

The rule was written down. It had a detector. It had a `mirror`. **It ran after the claim.**

## The fix: same rule, moved to the moment

`~/.claude/hooks/pipe-verdict-guard.sh` — a `PreToolUse` hook on `Bash`.

```
Bash command  →  jq extracts .tool_input.command
              →  prefilter: no "|" ? exit 0            (~4 ms, the common case)
              →  import the ARENA's detector module     (one rule, one door)
              →  finding? emit systemMessage + additionalContext
```

**It does not block.** A guard that denies a shell is a guard that gets disabled. It warns, names
the mirror, and cites the recurrence count.

**The pattern is imported, never re-derived.** `d_pipe_swallows_verdict.py` remains the single
definition; the hook is a second *door* onto it, not a second copy. Two implementations of one
rule is a promise; one implementation reached two ways is a mechanism.

### Proven, in both directions

| input | required | observed |
|---|---|---|
| the exact command that opened this session | warn | ✅ warns, names #11/#19/#21 |
| `du -sh …\| sort -h \| tail -5` | silent | ✅ silent |
| `just falsify \| tail -5; echo rc=${PIPESTATUS[0]}` | silent | ✅ silent — it teaches the right form rather than nagging |
| no pipe at all | silent, fast | ✅ 4 ms |
| **live fire** in a real session | warn | ✅ fired on `cd ~/fedora-arena && just doc-anchors 2>&1 \| tail -1; echo "rc=$?"` |

**A false proof, kept because it is the useful part.** The first live test used
`just --justfile … doc-anchors` and produced nothing. The obvious conclusion was *"the settings
watcher isn't watching"* — the dramatic diagnosis. A sentinel prefix distinguished the two
possibilities in one command: **the hook was firing; the pattern did not match.** `just\s+\w+`
cannot cross the `--` of a flag. Detector widened (`_FLAGS` skips leading flags for both `cargo`
and `just`), with the flag-prefixed form added as a **second negative control** — a control is
worth having for a shape the detector has actually been shown to miss.

**The stated cost.** Commands touching `scripts/detectors/` or the guard's own source are
exempted: those files contain the pattern by construction, and the guard fired on its own
authorship twice while being written. That is P1-F's trade-off, now applying in a second place —
a genuine pipe-swallowed verdict inside such a command will not be warned about.

## The other half: make the right form the easy one

A guard catches the wrong shape. It does not make the right shape convenient — and the wrong
shape recurred three times precisely *because it is shorter to type*.

```bash
gate just falsify          # runs it, prints the tail, exits with FALSIFY's code
gate -n 20 cargo test      # 20 tail lines (default 8)
gate -q just detect        # verdict line only
LOG=path gate <cmd>        # keep the full log
```

`gate` redirects to a log, captures `$?` from the command itself, prints the tail, and reports
`rc=… log=… lines=…` on stderr — the denominator every claim needs. The contrast, measured:

```
gate bash -c '…; exit 7'   → gate exited: 7      ← the command's status
bash -c '…; exit 7' | tail → pipe reports: 0     ← tail's status
```

[P2](obsidian://open?vault=my-diary.vault&file=Principles%2F00%20-%20Principles): when the remedy begins with *"remember to"*, it is a design problem in a discipline
costume. The guard is the detector; `gate` is the use-pattern mirror, made shorter than the
antipattern.

## Declaring a deliberate control

Proving a detector fires means issuing the exact shape it detects. `detect-session` scans raw
transcript text and cannot tell a proof from an accident, so this session's run reported
`findings=5` — of which **2 were accidents (both before the hook existed) and 3 were deliberate**.
A count a later reader cannot act on is how an auditor starts being ignored (F41).

Append the token to any command issued as a control:

```bash
just detect 2>&1 | tail -1; echo "rc=$?"   # DETECT-SESSION-CONTROL
```

`session_commands.py` **blanks** the line rather than dropping it — line numbers stay truthful —
and reports `# declared_controls=N` on stderr, so the exemption is counted, never hidden.
Proven against a synthetic transcript: the real accident survives, the declared control is blanked,
the count is reported, numbering is preserved.

**The honest measure of the hook, this session:** two accidental instances, both *before* it was
armed; zero after. That is consistent with working — it is not yet proof. One session is n=1; the
test is whether tomorrow's transcript carries zero undeclared instances.

## What it does not fix

The hook sees **Bash tool calls only**. A verdict taken from a pipe inside a script, a cascade
stage, or a justfile recipe is out of its scope — `just detect` and `just detect-session` still
own those. And it is `PreToolUse`, so it fires on the command as written; it cannot know whether
the resulting number is later quoted as evidence. It narrows the gap; it does not close it.

Related: [[podman]] · [[Assimilation - Rules That Fire]] · [[Axiom Conformance]] · [[Fabric Bash Command Plane]] · [[Fabric Habitat Seven-Facet Assessment]] · [[00 - Workflows]] ·
[[Weight Matrix - Which Gate Bore the Weight]] · [[00 - Toolshed Index]] ·
[Field Findings](obsidian://open?vault=toolshed.vault&file=50%20Field%20Notes%2F00%20-%20Field%20Findings) F76–F78

---

## The reflex family this started — 2026-09-14

This guard was the first. There are now **eleven** reflexes on the same surface, each refused by
`habitat-reflex` unless it can be shown to fire *and* to stay silent (`reflexes=11 unproven=0`,
`drift=0`): `pipe-verdict` · `pattern-kill` · `commit-chain` · `new-artifact` · `control-change` ·
`insights-publish` · `lint-on-write` · `destructive-guard` · **`host-path`** · **`corpus-measure`** ·
**`justfile-pair`**.

**`justfile-pair-guard`** (`PreToolUse`, `Write|Edit`) fires on any justfile write: it parses the
recipe names out of the content, reports **which have no `runbooks/<name>.toml`**, and carries the
`just` semantics verified against the manual *and* the binary — arguments are positional, and
`just recipe name=value` is a **variable override**, not a parameter (`error: variable 'x'
overridden on the command line but not present in justfile`). A recipe records *what* to run; only
the runbook holds preconditions, the failure path and the verification. `cases=10/10`,
`neutered=5 killed=5`.

The last two landed 2026-09-17 and are the first built against **my own measurement errors** rather
than against a defect in the work:

- **`host-path-guard`** (`PreToolUse`, `Bash`) — a path absent from this container may be present on
  the host. `ls /var/home/<sibling>` from the toolbox returned nothing and I reported a 985 MB
  codebase as nonexistent with 7,139 broken links. An unmounted path and a missing path produce
  **byte-identical output, and neither names the layer**. `cases=11/11`, `neutered=5 killed=5`.
- **`corpus-measure-guard`** (`PreToolUse`, `Bash`) — fires on the *shape* of a corpus measurement
  that has returned a false verdict here: wikilink parsing without the escaped-pipe and code-fence
  fixes, first-match regex answering a membership question, and counting breakage over a vault
  without splitting live notes from byte-preserved captures. `cases=14/14`, `neutered=7 killed=7`.

The last two landed 2026-09-14 as P1 and P2 of the [[Mitigation Plan]], and they are the first on
this surface built against **externally measured** evidence rather than my own register — an
insights report counted 28 friction events over 203 messages and named the same failure modes the
diary had recorded independently.

- **`lint-on-write`** (`PostToolUse`, `Write|Edit`) — `bash -n` / `ast.parse` at the moment a file is
  written, because the largest friction class by a factor of three was *defects in scripts I wrote*,
  one of which crashed 31 minutes into a run.
- **`destructive-guard`** (`PreToolUse`, `Bash`) — the deletion half of `pattern-kill`'s rule. It
  enumerates what an `rm -rf` / `git clean` / `find -delete` would destroy, reading the habitat's
  **own** `corpus-sources.json` for what is irreplaceable *and*, from the same file, what is
  disposable. `rules=10/10 cases=14/14`, and `neutered=10 killed=10 survived=0` — every rule proven
  load-bearing, not merely covered.

Two of the family are documented in their own right, and both link back here:
[[Insights Reports - Opening Them Past the Sandbox]] (the `Stop` reflex that publishes a report past
the flatpak sandbox) and [[Mitigation Plan]] (what the insights report measured, the mechanisms
against it, and the evidence each one carries).

**The limit worth carrying:** this guard did not fire on the fifth occurrence of the very defect it
was built for, because the verdict was read one statement after the pipeline rather than from it
(my-diary `Mistakes I Made` #44, toolshed **F145**). *A guard is a claim about the shapes it has
seen* — and the answer there was `gate`, not a wider pattern.

**The limit's twin, found the same way 2026-09-14:** a guard can also be silent because a
dependency it resolved through `$HOME` was never loaded — no error, no red, a wrong verdict.
See [[50 Field Notes/00 - Field Findings#F146 · A script that resolves its own dependencies through `$HOME` is untestable — and degrades silently|F146]].