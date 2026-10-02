---
tags: [toolshed, workflows, candidates, orchestration, ultracode]
created: 2026-09-27
source: workflow wf_35217b62-85f (6 readers → merge → 3 lensed judges), read-only
status: candidates — none implemented
---

# Workflow candidates — mined from 19 runs (2026-09-27)

**Navigation:** [[60 Workflows/00 - Workflows|Workflows]] · [[00 - Toolshed Index|Toolshed master index]] ·
[Orchestration master index](obsidian://open?vault=herdr-habitat-orchistration.vault&file=00%20-%20Master%20Index) ·
[Herdr Habitat master index](obsidian://open?vault=herdr-fedora-habitat.vault&file=00%20-%20Fedora%20Master%20Index) ·
[Kinoite master index](obsidian://open?vault=fedora-kinoite.vault&file=00%20-%20Fedora%20Master%20Index)

**What this is.** A read-only study of every Workflow-tool script this habitat has run, 19 in all, from `hee-w3-*` on
2026-09-04 through `r21-*` on 2026-09-27, together with their `journal.jsonl` run records. Six readers raised
**38 candidates**. A merger reduced them to **12** and listed each one it dropped or merged, with its reason. Three
judges then scored every candidate, each from one angle: *evidence* (re-read the journals and recount), *duplication
and cost* (whether `~/agent-harness`, a `habitat-*`/`hee3-*` tool or a built-in already does it) and *standards* (fit
with `~/CLAUDE.md`, and false-pass risk). **11 of 12 kept 3/3; C12 kept 2/3.** The raw result is
`~/hee3-evidence/T00-plan-20260926/workflow-candidates-wf_35217b62-85f.json`.

> [!warning] Scope of the claim
> These are **candidates**, scored by agents from this same lineage. That is weaker evidence than a cross-lineage
> review, and nothing here is built. The counts below were re-measured by the evidence judge (FACT). The value
> estimates are INTERP.

## The measured problem (FACT, from the journals)

- **9 of the runs ended partial on a session or usage limit, and the tool still said `completed`.** The 9 runs hold
  **173 failed agents**. None of the `failed` records carries a cause or the unit being worked on (keys are
  `type/key/agentId` only). Every follow-up re-typed its state by hand.
- **43 reviewer agents in 15 runs hit `fatal: '<x>' is already used by worktree`**, and **0** saved scripts use
  `worktree add --detach`. Review subjects were `HEAD` while `main` moved underneath.
- **7 silent `.slice(0,N)` truncations in 5 scripts.** One design tournament judged and synthesised without ever
  seeing one of its three proposals.
- **The survival rule counted a vote nobody cast as a refutation.** In `r21-fact-check` L36, a defect whose refuters
  died reached synthesis as REFUTED.
- **34 of 55 run records keep their script under tmpfs `/tmp`, and 0 of those scripts still exist.**
- **Hand-derived copies of the landing chain:** 16 `*-publish.sh` and 19 `*-cold.sh` in `~/.cache`. **47 plant-battery
  scripts, 46 of them with no per-test timeout.**

## Ranked candidates

| # | Candidate | Kind | Judges | Mean | Recurrence |
|---|---|---|---|---|---|
| C1 | **Partial-run census** | hook + epilogue | 3/3 | 9.0 | 9 runs |
| C5 | **Three-state vote tally** | primitive | 3/3 | 8.7 | 3 |
| C7 | **Pinned subject + detached review worktree** | primitive | 3/3 | 8.3 | 15 |
| C6 | **passLarge: spill or refuse, never `.slice()`** | primitive | 3/3 | 7.7 | 5 |
| C11 | **`hee3-land` — the S5 stack-landing primitive** | primitive | 3/3 | 7.7 | 16 |
| C2 | **Pre-launch fan-out gate** | guard | 3/3 | 7.3 | 9 |
| C10 | **Shared plant-battery runner** | primitive | 3/3 | 7.3 | 47 |
| C3 | **Slice-landing chain** (build → lensed review → triage → bounded fix) | saved workflow | 3/3 | 7.0 | 14 |
| C8 | Resume from evidence (journal + git, commit per item) | primitive | 3/3 | 6.7 | 4 |
| C9 | Script library: one LAW file, one GATE fragment, off tmpfs | practice | 3/3 | 6.7 | 34 |
| C4 | Find → filter → refute → synthesise, as a saved audit workflow | saved workflow | 3/3 | 6.0 | 4 |
| C12 | Gate-pin reconciliation at integration | primitive | 2/3 | 5.3 | 4 |

### C1 · Partial-run census — strongest
Every saved script returns `{verdict: COMPLETE|PARTIAL|FAIL, per_phase:{started,result,failed}, unjudged:[ids]}`, and
a run with `failed > 0` is never COMPLETE. An advisory PostToolUse hook on `Workflow` reads the run's own
`journal.jsonl`, never the script's own summary (F134). It prints `WORKFLOW_PARTIAL run=<id> failed=N/M`, reads each
failed transcript's last message and classifies the cause as `session_limit | usage_limit | other` (an `other` is loud).
It also names an evidence-store copy target. Every `agent()` call carries a label and a phase, so the journal is its
own index. *Risk:* the limit message is vendor text and can drift, so an unknown cause prints `other` and is never
dropped. *Duplication:* none. No hook currently matches `Workflow`.

### C5 · Three-state vote tally
`tally(ids, votes, {quorum})` → per id `CONFIRMED | REFUTED | UNJUDGED | SPLIT`. REFUTED needs `judged_by ≥ quorum`.
The tally asserts `checked + unjudged == claimed` and refuses otherwise. The UNJUDGED list is a prompt fragment that
the synthesis must include. This turns W7 decision 13 (*a comparison that did not happen is never a catch*) into a
mechanism. The skill's own adversarial-verify example has the same flaw: a null vote vanishes in `filter(Boolean)`.

### C7 · Pinned subject and detached review worktree
The launcher resolves `git rev-parse <ref>` and `git status --porcelain | wc -l` once, and refuses on an empty result
(the toolbox host-path trap). It passes `{sha, dirty}` into every prompt, and every schema requires `measured_tree`
(F126). The emitted block is `worktree add --detach <scratch>/wt-rev-<lens>-<unit>-<round> <sha>`, with its own cold
`CARGO_TARGET_DIR`, then removal with a read-back. The synthesis flags any result whose tree is not the pinned sha.
*Duplication:* `isolation:'worktree'` is neither detached at a pinned sha nor cold.

### C6 · passLarge
Inline a value only when it fits. Otherwise the main loop writes it to the evidence store first (scripts have no
filesystem), and the prompt says `READ THIS FILE IN FULL: <path> bytes=N sha256=…`. The strict mode refuses by name
with both numbers. Phase results persist, so a failed synthesis leaves its inputs on disk.

### C11 · `hee3-land`
`hee3-land <worktree> <sha> <label>` composes the existing parts and re-implements nothing. It refuses to start
unless tip == sha, the tree is clean, and a battery log for that sha reads `verdict=PASS`. Then: the precount against
a declared exception list with reasons → `hee3-gate` → a cold clone, supervised through agent-harness and aggregated
by `lib/gates.py` into one refusal → `merge --ff-only` → host publication parameterised by sha (replacing the 16
copies) → restore the exec bit and read it back → **stop before the commit**, which stays its own command. It prints
`tree=/dirty=` before and after. This is S5 in the [New Way of Working](file:///var/home/Louranicas/handoffs/HEE3_NEW_WAY_OF_WORKING_20260926.md).
*Correction from the judges:* there is no reusable `hee3-cold.sh` to compose; the 19 copies are per-sha.

### C2 · Pre-launch fan-out gate
Plain code before the first `agent()`. It validates args (non-empty, ids exist, no target worktree or branch already
there) and computes `planned_agents` (fan-out × lenses, weighted for cargo/mutants), logging both numbers. Above a cap
the **caller** declares, it refuses unless `accept_cost` is set. Otherwise it batches per item (`wf_03ecad9c-487`
turned 98 planned refuters into 18) or admits work in severity order (HIGH 2 lenses, MEDIUM 1, LOW UNJUDGED), and puts
every dropped id in the return value. *Risk:* usage headroom is UNMEASURED, so the estimate is advisory, labelled
"suspected", and never reads as safe.

### C10 · Shared plant-battery runner
A plant spec is `{id, file, anchor, replacement, killer_target, killer_name, rule}`. For each plant: apply it through
the harness anchored edit, run the named killer under `--cap-lints=warn` with a per-test budget, and classify the
result as `KILLED | SURVIVED | NOT_COMPILED | HUNG` (only KILLED counts, and it must be the named test's FAILED line —
F133). Restore, then assert an empty `git diff`. The runner refuses a dirty index, holds a lock the gated-worktree
guard can see, and prints `verdict= plants=N` with a count per class. Compose with `agent-harness measure.py`
(per-case timeouts, resumable journal) rather than re-deriving it. This is not a Workflow script, because it runs
cargo.

### C3 · Slice-landing chain (saved workflow)
One saved workflow. `args: {repo, base_sha, units[{name, worktree, branch, brief_path, extra, law_line}], lenses,
max_rounds}`. Build (a receipt with `head`, `tree_clean`) → review on C7 worktrees (severity enum
`high|medium|low|info`, route `fix|owner|none`) → triage in plain code (dedupe, printing the merged groups; FAIL on any
blocker) → bounded fix and fresh-refuter rounds that **stop as STALLED when the blocker count is not falling** (F128).
It fixes a verified defect: three scripts share `verdict === 'FAIL'` as the only fix trigger, so findings carried
inside a PASS were dropped. *Risk:* an automatic fix loop can fit the reviewer, so the refuter is always fresh and
never sees the previous refute.

### C8, C9, C4, C12 — briefly
- **C8** — `resumePlan(prior_run_dir)` rebuilds completed/failed/never-started from the journal. `treeState(wt, base)`
  injects `git log`/`status`/`diff --stat` verbatim. Multi-item authors commit per item. *Partly built in:*
  `resumeFromRunId` works only within one session.
- **C9** — one canonical LAW file and one GATE fragment (every step through `gate`, printing `measured=N`), read by the
  main loop and passed as args. *Partly built in:* the tool now persists inline scripts under the session directory.
  The remaining value is the single LAW file (one door, not copies that drift).
- **C4** — best kept as a composition of C2, C5 and C6 plus canonical ids assigned in plain code. As its own saved
  workflow it is the costliest shape (`wf_1376e121-905`: 246 agents, about 9.6 M subagent tokens).
- **C12** — the dup-cost judge dissented: `~/.cache/hee3-precount.py` already reports `t25 COUNT MISMATCH`, and only
  the proposed diff output is new.

## Dropped (with reasons, not silently)
N-version independence by structure (one lineage; the remedy is the cross-lineage verifier cmd4) ·
brief-then-critic-before-fan-out (one instance, no failures; its slice defect lives in C6) · the detector quiet-case
rule (already in the F96/F125 family) · decisions-before-builders (one run, nothing proven) · budgeted measurement
review (already `lib/review.py`, `hee3-review-coverage`) · bounded design round (merged into C4). Twenty-nine further
raised candidates were merged into C1–C12. The full list is in the raw result.

## Suggested build order (INTERP)
1. **C5 and C1 first.** They are cheap plain code, and they stop partial runs and uncast votes from reading as clean.
2. **C7 + C6**, which every review fan-out needs.
3. **C11 `hee3-land`**, which retires 35 hand copies and is already named S5.
4. **C2**, then **C10**, then **C3** built on all of the above.

> [!note] Harness flag, relayed
> The workflow harness flagged the dup-cost judge's output for mentioning `~/.claude/settings.json`: it said no hook
> currently matches `Workflow`. That is an observation, not an instruction. No settings were changed.

> 🔗 **Cross-vault synergy** — [Orchestration master index](obsidian://open?vault=herdr-habitat-orchistration.vault&file=00%20-%20Master%20Index)
> (fleet and mission orchestration ⇄ Workflow-tool orchestration) ·
> [Herdr Habitat master index](obsidian://open?vault=herdr-fedora-habitat.vault&file=00%20-%20Fedora%20Master%20Index) ·
> [Kinoite master index](obsidian://open?vault=fedora-kinoite.vault&file=00%20-%20Fedora%20Master%20Index).
> Related: [[60 Workflows/Claim-Time Guard|Claim-Time Guard]] (C1 is the same move for workflows: the rule fires where
> the claim is made) · [[60 Workflows/Sandbox Fanout and Fusion|Sandbox Fanout and Fusion]].

<!-- practice-map:20260927 -->
> 🔗 **Cross-vault synergy (2026-09-27):** [Practice Map — What Earns Its Keep](obsidian://open?vault=herdr-fedora-habitat.vault&file=50%20Automation%2FPractice%20Map%20-%20What%20Earns%20Its%20Keep) places these candidates in the whole working loop (its §2.4 and §6 P4/P7).
<!-- /practice-map:20260927 -->
