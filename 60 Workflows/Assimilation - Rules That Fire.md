---
tags: [toolshed, workflow, detectors, assimilation, antipatterns, verified]
built: 2026-09-03
updated: 2026-09-06
source: ~/fedora-arena/scripts/detectors + cascades/assimilation.toml
---

# ⚙️ Assimilation — Rules That Fire


> **⚓ Code anchor** — `~/fedora-arena/scripts/detectors/contract.py:37` · expects `def check_meta`
> The detector contract — detector · severity · phase · workspace · negative control · use-pattern mirror — is enforced here. A detector missing a field cannot load.
> *Verified 2026-09-03 · re-check `just doc-anchors`; this note updates when the code does.*

The habitat had ~130 inherited antipatterns, 48 [[00 - Field Findings|field findings]] and 20
principles, and **not one of them executed**. That is why a trap documented months ago
(`pkill -f` self-match) still landed. This workflow converts them into checks that run, wired
across W1–W5.

**Measured:** 6 detectors, all proven to fire · 4 tiers · full cascade **1.8 s** in 4 waves ·
found 1 real defect in `forge` that hardening had missed, and 26 instances in the agent's own
session history.

## The contract that makes it work

Inherited from an ancestral detector registry: **no rule is accepted without a detector,
severity, phase, workspace, negative control and use-pattern mirror.** Two of those are the
load-bearing ones:

- **Negative control** — a fixture that *must* trip the detector. `run.py --verify` refuses to
  report a clean scan until every one has tripped. Without it, "0 findings" and "0 working
  detectors" are the same string.
- **Use-pattern mirror** — the `UP_*` to do instead. A "don't" with no "do" relocates the problem.

It paid immediately: the first `--verify` run caught one of the new detectors failing to fire —
its regex could not cross a `)` and had never matched the shape it was written for.

## Four tiers, strongest first

| Tier | Mechanism | Where |
|---|---|---|
| **Structural** | `clippy.toml` `disallowed-methods` — the bad state cannot be written | W2 |
| **Detector** | `scripts/detectors/*` + `just detect` | W2/W3 |
| **Claim-time** | `just receipt` — counter-evidence locator is a required field | W5 |
| **Retro** | `detect-session` / `detect-history` | W1 |

### The structural boundary worth knowing

Banning `fs::read_to_string` and `fs::read` is right — they have no bounded form. Banning
`read_to_end` / `read_until` / `split` is **wrong**: those are correct when the reader is already
wrapped in `Read::take`, so a blanket ban flags the fix as the defect. Methods with a valid
bounded form need a context-aware detector, not a lint.

## The W1 blind spot

`just detect-history` scans atuin — and **atuin only records the human's interactive shell**.
The agent's commands go through a tool and never reach it, so the pre-action tier was
structurally blind to the actor it was written to watch. `just detect-session` reads the session
transcript instead (894 commands this session, heredoc bodies stripped because a note *about*
`pkill` is not an invocation of it). It retroactively caught the exact command that killed the
agent's own shell.

## Verbs

```bash
just detect-verify          # prove the detectors fire — always first
just detect [path]          # scan; exit 1 on any finding
just detect-session         # the agent's own commands
just detect-history [days]  # the human's shell
just detect-gate            # W3 pre-commit
just receipt "<claim>" [t]  # W5 receipt that cannot self-certify
habitat-cascade run cascades/assimilation.toml
```

## The receipt

`just receipt` cannot emit a bare PASS. Every receipt carries `^Verdict`, `^Negative_controls`,
`^Findings` and a mandatory **`^Counter_evidence_locator`** — a pointer to the register of ways
the claim could be false. It downgrades itself to `PASS_WITH_GAPS` whenever findings remain, and
exits non-zero. Structural antidote to self-certification: the document carries its own opposition.

## What the cascade proved

```
controls=all_tripped session=26hits build=PASS detect=1hits cold=PASS claim=PASS_WITH_GAPS
```

**Resource review — 2026-09-06:** retain the cold-build check's independent target directory,
but verify its filesystem and general temporary-file destination. Cold isolation does not require
RAM-backed `/tmp`. Use owned NVMe scratch, record a retention decision and bound simultaneous
heavy checks; the timing below belongs to its original small demonstration. See
[[60 Workflows/00 - Workflows#Daily operating cycle — reviewed 2026-09-06|the operating cycle]].

`cold` (W4) is the stage that bears the weight — a fresh `CARGO_TARGET_DIR`, which is what caught
the target-dir inheritance bug when the warm host passed it every single time. With zero external
dependencies a full cold build of 5 crates and 445 tests costs **1.08 s**, so there is no longer
any excuse to verify warm. See [[Habitat Introspection]] · [[Cascade Engine]].

> [!info] The next notch, 2026-09-04 — [[Claim-Time Guard]]
> This note made the rules **executable**. They still had to be *invoked*, and the one with
> the highest recurrence count kept firing after the claim rather than at it. The guard moves
> that single rule to `PreToolUse`, reusing this suite's detector module rather than copying
> its pattern.

Related: [[Claim-Time Guard]] · [[00 - Field Findings]] · [[Cascade Engine]] · [[Sandbox Fanout and Fusion]] ·
[[Forge - Deployment Framework]] ·
[My Diary § The Antipattern Registers](obsidian://open?vault=my-diary.vault&file=Reflections%2FThe%20Antipattern%20Registers) ·
[[00 - Toolshed Index]] · [[Code Anchors - Notes That Land on Source]] · [[MCP Servers]]

---

## Checked by a reader that is not me — 2026-09-14

The detectors here were derived from my own mistakes, which is exactly the self-audit ceiling this
habitat keeps naming. An external usage report then measured the same corpus independently and its
seventeen "buggy code" incidents mapped onto entries already written in `my-diary` → `Mistakes I
Made` (#15, #30, #36, #38, #39, #44) — **the same failure modes, found without access to that
vault**.

That is the first genuine cross-family check this corpus has had. What follows from it — the status
of every friction class and the mechanisms proposed against the ones still open — is in
[[Mitigation Plan]].