---
tags: [toolshed, workflow, axioms, conformance, verified]
built: 2026-09-03
source: ~/fedora-arena/scripts/habitat-conform + scripts/audit/backup_integrity.py
---

# ⬡ Axiom Conformance — the axioms applied to W1–W5

Nine axioms ([My Diary § Axioms](obsidian://open?vault=my-diary.vault&file=Axioms)) tested
mathematically are still only claims about a corpus. `just conform` runs them against the **live
cockpit**: one probe per axiom per service, 16 doors in parallel.

| axiom | probe | violation looks like |
|---|---|---|
| AX-2 absence≡success | does a failing query differ from an empty one? | `AMBIGUOUS` |
| AX-3 unfailed≠works | can the door be made to fail at all? | `NEVER-FAILS` |
| AX-6 defaults answer | can the door state its defaults? | `OPAQUE` |
| AX-9 name≠thing | does `id → proc` resolve; does `habitat doc` land? | `NO-DOC` |

## A violation only means something relative to the door's kind

- **cmd** — a real command with flags; can and must reject nonsense
- **eval** — passes its argument to an interpreter (`nu -c`, `jq`); **any** string is valid input,
  so it cannot validate shape. Inherent — to be labelled, not "fixed".
- **pane** — no agent door; validation is out of scope, but a silent **discard** still is not.

Classifying doors took violations from 8 to 4 by removing false ones. **The measurement got more
honest in both directions.**

## What it found and fixed

**14 → 3 violations** across four fixes:

1. **The pane-only door ate its arguments.** `habitat q yazi --nonsense` returned byte-identical
   output to `habitat q yazi`. AX-2 applied to the *call*: "ignored" and "absent" were
   indistinguishable. It now names the discard.
2. **The scanner had the bug it was built to find** — `habitat q … | head -3` reported *head's*
   exit status, so the probe testing whether doors can fail could not see failure.
3. **Door kinds** (above).
4. **`args = none`, enforced.** `repo-fleet` accepted and ignored anything; the registry now
   declares it takes none and `habitat q` refuses rather than running the default and pretending.

**Update 2026-09-03 - the remaining three were not inherent after all.** Two were self-inflicted:
`habitat q <svc> --help` was *unaskable* because the `args=none` enforcement refused it and pane
doors died before reaching it, so AX-6 correctly reported doors that could not state their
defaults. `--help` is now answered as a question about the **door** -- before either refusal, one
mechanism for cmd/eval/pane rather than three exemptions. The third, `mempalace` AX-2, was a
mis-aimed probe: the "good" stimulus was itself a usage error, so two failures were being compared
and called indistinguishable. Doors now declare `probe_arg` in the registry (see
[[00 - Field Findings|F58]]) and both `conform` and `twodoors` read the same declaration.

**`verdict=PASS services=16 violations=0 unmeasured=0 measured=59/64`** - and the denominator is
load-bearing: the first version of this fix let nine doors report `n/a` and went green on nothing
measured ([[00 - Field Findings|F59]]). `UNMEASURED` now turns the gate red like a violation.

## `just roundtrip` - pairs, plus the ones nobody remembered

The six probes were the pairs I could recall, and `chainlog` had been a write-only sink for 111
records precisely because nobody recalled it. Durable-state paths are now enumerated **from
source**, and anything written but never read back is reported. It immediately found `reactor.log`
and `trigger.log` -- the reactor being the *self-healing* service, whose whole job is noticing that
something died. `just logs` is the reader; it checks the unit is alive, because a quiet log and a
dead writer are byte-identical.

## `just chart-since` - duration bounds

A stage that returns far faster than its own history has usually stopped checking. `twodoors`
returned FAIL in 2.5 s where it returns PASS in 92 s, and the cascade reported the resulting 13 s
total as a **speed-up**. Per-stage bounds now reach the verdict, with two rules: Shewhart's LNPL,
and a robust median rule for when a bimodal stage inflates its own limits so wide that nothing can
signal. After a known process change, re-baseline (`just chart-since <stamp>`) rather than reading
limits that mix two regimes.

## `just backup-integrity` — the recovery path

`habitat-settings-backup` runs after every change and **had never been restored**. Its `--dry-run`
is sound (it skips absent sources) — and silent skipping is exactly what an incomplete backup
looks like, so a dry-run cannot tell the two apart.

The completeness check found `home/herdr-plugins` **STALE**: the snapshot held
`herdr-plugins/herdr-plugins/habitat-services`, the `cp -a` nesting trap the restore side
explicitly guards against. A restore would have **silently lost the auto-respawn plugin**.
Full write-up: [[00 - Field Findings|F54]].

```bash
just conform            # 16 doors x 4 axioms, parallel
just backup-integrity   # every `back src dst` pair vs live
habitat-cascade run cascades/falsify.toml   # 9 stages, one wave
```

The same move, aimed at the gates instead of the doors: [[Weight Matrix - Which Gate Bore the Weight]]
— faults × gates, and the minimal set of gates that still covers every known fault class.

> [!info] AX-3 and AX-4, moved to the moment — [[Claim-Time Guard]] (2026-09-04)
> The axioms here say a check never shown to fail is not known to work (AX-3) and that
> enforcement depending on memory decays to zero (AX-4). `PIPE_SWALLOWS_VERDICT` had a
> working detector and still recurred three days running, because invoking it depended on
> memory. It now fires from a `PreToolUse` hook — AX-4 answered structurally rather than
> by discipline.

Related:[[Weight Matrix - Which Gate Bore the Weight]] · [[Fabric Habitat 90-Point Promotion and Practice]] · [[Assimilation - Rules That Fire]] · [[Shape-Directed Tool Chaining]] ·
[[Code Anchors - Notes That Land on Source]] · [[00 - Field Findings]] ·
[[00 - Toolshed Index]]
