---
tags: [toolshed, workflow, mutation, gates, falsify, verified]
built: 2026-09-03
updated: 2026-09-06
source: ~/fedora-arena/scripts/audit/weight_matrix.py · cascades/weightweb.toml
---

# ⚖️ The Weight Matrix — which gate actually bore the weight?

<!-- habitat-highways:2026-09-08:start -->
## Corpus insight routes — 2026-09-08

Curated navigation added in this edition; the dated claims and evidence below retain their original scope.

| Purpose | Route |
|---|---|
| Cross the vault family by intent | [LLM Traversal - Cross-Vault Routes](obsidian://open?vault=herdr-fedora-habitat.vault&file=80%20Architecture%2FLLM%20Traversal%20-%20Cross-Vault%20Routes) · [file](</var/mnt/STORAGE-10TB/fedora-obsidian-vaults/herdr-fedora-habitat.vault/80 Architecture/LLM Traversal - Cross-Vault Routes.md>) |
| Connect restore to failure qualification | [Synergy - Recovery as a Test Environment](obsidian://open?vault=herdr-fedora-habitat.vault&file=80%20Architecture%2FSynergy%20-%20Recovery%20as%20a%20Test%20Environment) · [file](</var/mnt/STORAGE-10TB/fedora-obsidian-vaults/herdr-fedora-habitat.vault/80 Architecture/Synergy - Recovery as a Test Environment.md>) |
<!-- habitat-highways:2026-09-08:end -->


Every gate in this habitat is green. Until now, none had ever been asked what it would **catch**.
The Spellbook names the gap and nothing had closed it:

> *"'It passed every gate' is not 'I knew which gate bore the weight.'"*

So: **mutation testing, applied one level up** — not to forge's source, but to the habitat's own
verification stack. Each **fault** is a constructed defect drawn from a real field finding,
injected into a disposable copy; each **gate** is run against it; the cell records whether the
gate went red.

```bash
just weight-matrix            # 15 faults x 8 gates, ~10.6 s
atuin scripts run weight-matrix
habitat-cascade run cascades/weightweb.toml
```

## What only the matrix can say

| gate | ws | caught | unique | reading |
|---|---|---|---|---|
| `clippy` | W2 | 7/14 | **4** | `clippy_lint`, `secret_in_source`, `unbounded_read`, `unwrap_in_lib` |
| `detect` | W2 | 5/14 | **4** | `file_scope_allow`, `noop_test`, `pipe_verdict`, `pkill_self` |
| `anchors` | W3 | 3/7 | **3** | `broken_anchor`, `drifted_anchor`, `weak_anchor` |
| `orphans` | W1 | 3/7 | 1 | `orphan_note` |
| `receipts` | W5 | 2/14 | 1 | `stale_receipt` — the gate this exercise created |
| `test` | W2 | 2/14 | 1 | `test_failure` |
| `deadpaths` | W4 | 1/7 | 1 | `dead_path` |
| `fmt` · `specparse` · `backlinks` | W2/W5/W1 | 1, 1, 2 | 0 | covered by others *at this corpus size* |

**21 faults × 10 gates · ceremonial=0 · blind=0 · minimal covering set 7 of 10.**

> [!important] "Irreplaceable" is corpus-relative, and the corpus moved it twice
> At 15 faults `specparse` and `backlinks` were each uniquely responsible for a class. At 21 they
> are not — other gates now cover `toml_break` and `broken_wikilink`. Nothing about those gates
> changed; the **question** did. A `unique=0` means *"no fault in this corpus distinguishes it"*,
> never *"this gate is redundant"*, and the two are easy to confuse in a table that does not say
> so. Read every row with its denominator attached.

> [!warning] These numbers replace an earlier table, and the way they were wrong is the point
> The first run reported **`fmt` 7/11 as the widest net** and **`clippy` and `test` as redundant
> (unique=0)**. That was an artifact of my own payloads: I appended Rust like
> `pub fn wm_lint(v: &[i32]) -> bool { return v.len() == 0; }`, which `cargo fmt --check` rejects
> **for its formatting**. So `fmt` scored a CAUGHT on nearly every Rust fault by objecting to my
> typing, and the gates that caught the actual defect looked redundant beside it.
>
> Measured directly: a rustfmt-clean append leaves `fmt rc=0`; the one-liner leaves `fmt rc=1`.
> With every payload rewritten rustfmt-clean, `fmt` drops 7 → 1 and both `clippy` and `test`
> become irreplaceable. **I came within one commit of publishing that two working gates were
> redundant.**
>
> This is the same lesson as the three "ceremonial" verdicts below, in the opposite direction: a
> fault corpus that is sloppy in a way one gate happens to notice will credit that gate and
> discredit every other. **The matrix measures the corpus at least as much as the gates.**

## What the matrix does NOT measure — its own denominator

The habitat exposes **22 gate-like verbs**; the matrix exercises **10**. That gap is structural,
not an oversight, and stating it changes how the verdict line must be read:

> `ceremonial=0` means **none of the ten measured gates is ceremonial** — never *no gate in this
> habitat is*. The other twelve have still never been asked what they would catch.

The method needs a fault injected into a **disposable copy**. That works for anything reading a
tree — code, specs, vault notes, receipts. It cannot reach the gates whose subject is **live
habitat state**:

| unmeasured | why the copy cannot hold it |
|---|---|
| `conform` | interrogates 16 live service doors |
| `roundtrip` | live palace, registry, atuin, chain log |
| `backup-integrity` · `restore-rehearsal` | live snapshot against live files |
| `twodoors` | a running MCP server and a running shell door |
| `palace-entropy` · `logs` · `control-chart` | live index, live units, accumulated receipt history |
| `chaos` | kills a running service — destructive by construction |
| `metamorphic` · `provocations` · `selftest` | their subject is the *instruments*, not a tree |

So the honest shape of the result is: **10 gates measured against 21 faults; 12 gates unmeasured
because a disposable copy is the wrong instrument for them.**

> [!warning] And the obvious next step is not the one I first wrote here
> I originally said extending to those twelve "means a disposable *machine* rather than a
> disposable directory — eight minutes with `habitat-sandbox`". That is wrong, and worth leaving
> visible. A sandbox gives a cold **build** environment; it cannot host a **live cockpit** — no
> herdr server, no 16 service panes, no palace index, no systemd units, no accumulated receipt
> history. `conform` and `twodoors` need doors that answer; `roundtrip` needs a palace to write
> into and read back; `chaos` needs a service worth killing.
>
> Measuring those honestly needs a **disposable habitat**, which is a different and much larger
> thing than a disposable directory — closer to the Fleet-Alpha introduction bay in the Genesis
> plan than to `habitat-sandbox create`. Recorded as a real limit rather than a task estimate,
> because an under-priced next step is how a plan starts outrunning its evidence.

## Determinism, checked rather than assumed

Three consecutive runs: **identical coverage matrices**, identical blind and ceremonial sets, only
wall-clock ms varying (14012 / 13577 / 13836). A measurement instrument whose verdict wanders is
worse than none, and this one had never been asked. Each fault gets its own tree copy and its own
`CARGO_TARGET_DIR`, which is what makes the parallel run reproducible rather than merely fast.

**Resource review — 2026-09-06:** preserve per-fault isolation while choosing storage and
concurrency. A fresh target directory can still be on RAM-backed `/tmp`; inspect both target
and general temporary paths. Use owned NVMe scratch and retain the receipt before retiring
completed copies. Do not replace per-copy target ownership with one shared inherited directory.
See [[50 Field Notes/lukes workflows#The largest actionable finding: temporary data|scratch findings]]
and [[60 Workflows/00 - Workflows#Daily operating cycle — reviewed 2026-09-06|the operating cycle]].

## The floors that make it a measurement rather than a scoreboard

- **Non-vacuity.** Every gate must be GREEN on an unmutated copy first. A gate red at baseline
  cannot discriminate and is **excluded with its name printed**, never silently scored.
- **Only live gates score.** Counting an excluded gate turned "nothing caught this" into a false
  CAUGHT and hid the blind spots the matrix exists to find.
- **Out-of-scope renders `n/a`, not `-`.** Unmeasured must not read as not-caught (F59).
- **Each fault gets its own `CARGO_TARGET_DIR`** — F46, in the harness that hunts F46.

## The lesson the first three runs taught

**A `CAUGHT`-less column measures the fault, not the gate — and a CAUGHT-ful one can too.** Three separate times the matrix
called a working gate ceremonial because the fault aimed at it was mis-constructed:

- `pkill_self` — the detector fires only on a *true* self-match (the pattern also present
  elsewhere on the line). A bare `pkill -f some-daemon` is not that, so a **precise** detector
  read as blind.
- `one_way_link` — aimed at `[[Axioms]]`, a **hub**, correctly excluded from one-way accounting
  by out-degree.
- `broken_anchor` / `weak_anchor` — the auditor was ignoring its path argument entirely
  ([[00 - Field Findings|F68]]), so it never read the mutated copy.

Corrected, all three gates score and `ceremonial=0 blind=0`. **The matrix is as much a test of the
fault corpus as of the gates** — which is AX-3 turned on the corpus: a fault never shown to be
catchable proves nothing about the gate that missed it.

## `weightweb` — the clustered, webbed tree

`cascades/weightweb.toml` composes three shapes that no one of them can express:

```
matrix ─► discover ─► probe[detect] ┐
  (dimensional)  (TREE: width      ├─► probe_ok ─► synth ─► push ──► balance
                  discovered at    │                        (W3 out)  (W3 back in)
                  runtime, 8 ∥)    ┘
```

- **TREE** — one child per irreplaceable gate; nobody writes "eight" anywhere. `wave 3: 8 in
  parallel — 36 ms wall vs 277 ms serial`.
- **WEB** — the children converge, and the synthesis is *pushed into a surface a human reads*,
  then read back, so the graph cycles through the review session rather than ending in a report.
- **BIDIRECTIONAL** — `push` writes agent findings into the live diff; `balance` reads what is
  there afterwards **including notes the agent did not write**, and reports the ratio:
  `{"agent": 8, "human": 0, "state": "agent-only evidence"}`. Agent annotation is evidence;
  human annotation is review. A cascade that cannot tell them apart cannot gate on the difference.

Building it found two engine defects ([[00 - Field Findings|F67]]): a `foreach` parent could not
be joined, so the web shape was literally unexpressible — and a cascade with four of seven stages
never executed still exited `0`.

---
> 🔗 **Cross-vault synergy.** The gates measured here are the habitat's, and the engine the matrix
> stresses is `habitat-cascade`:
> [herdr habitat § Habitat Automation Stack](obsidian://open?vault=herdr-fedora-habitat.vault&file=50%20Automation%2FHabitat%20Automation%20Stack) ·
> [Session State](obsidian://open?vault=herdr-fedora-habitat.vault&file=00%20-%20Session%20State%20and%20Resume).
> The judgment half — why a `unique=0` is a statement about the corpus, not the gate —
> [my-diary § Measuring the Gates](obsidian://open?vault=my-diary.vault&file=Entries%2F2026-09-03%20-%20Measuring%20the%20Gates).
> Ledger rows: [both Fedora Master Indexes](obsidian://open?vault=herdr-fedora-habitat.vault&file=00%20-%20Fedora%20Master%20Index).

Related: [[Assimilation - Rules That Fire]] · [[Axiom Conformance]] · [[Fabric Habitat 90-Point Promotion and Practice]] · [[Cascade Engine]] ·
[[Clustering Shapes]] · [[00 - Field Findings]] · [[Cross-Workspace Review Gate]] ·
[[00 - Workflows]] · [[00 - Toolshed Index]]

## Primary source routes — 2026-09-08

- [arena: scripts/audit/weight_matrix.py](</var/home/Louranicas/fedora-arena/scripts/audit/weight_matrix.py:205>) — Disposable-copy experiment materialization; the documented live-habitat measurement limit remains a separate question.

> **⚓ Code anchor** — `/var/home/Louranicas/fedora-arena/scripts/audit/weight_matrix.py:206` · expects `def materialise(scope, tag):`
> [IFP] Source inspected for this route; no new behavioral or deployment verdict.

