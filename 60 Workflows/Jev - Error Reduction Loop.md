---
tags: [jev, fabric, workflow, error-reduction, hooks]
created: 2026-09-19
---

# 🛡️ Jev — the error-reduction loop

Built after a session in which **every error had one shape**: a checkable fact asserted
without checking it. Not sloppiness about hard things — confidence about easy ones.

## The two halves

| half | tool | question | vendor |
|---|---|---|---|
| **flag** | `jev-stop-guard` (Stop hook) | "is anything in this response a claim you never checked?" | none |
| **settle** | `jev-verify <claim> <src>` | "does that source actually say it?" | none ([[Jev and Fabric - Vendor-Free Chains]]) |

Flagging alone just nags. The loop only closes because the second half can *resolve* the
flag — the block message emits a runnable `jev-verify` command when the claim names a source.

## Four measurements that shaped it

**1. Latency is flat per call, not per question.** jev-axi 0.4.2: 1 question 1.46s,
5 questions 1.9s, **20 questions 1.75s**. So "ask one cheap triage question first" saves
nothing. The whole response goes in **one call**, one question per sentence per criterion.

**2. Batching bleeds.** Batched vs per-sentence scores: mean |gap| 0.056 (≈ the 0.05 noise
ceiling) but **max 0.28**. All 4 verdicts still agreed — only because the min-gate sat far
from 0.5. So a score landing in **0.35–0.65 is re-run alone** before it is trusted.

**3. The evidence is in the tool calls, not the prose.** Judged alone, *"the linter reported
0 drift signals"* and *"nobody has benchmarked this"* are indistinguishable — both bare
negatives citing nothing. Feeding the turn's **actual commands** in as an `evidence` state
field dropped the block rate on 24 real messages from **54% → 42%**.

**4. The threshold is measured, not picked.** Swept over 121 sentences of real prose against
four known errors:

| threshold | real messages blocked | known errors caught |
|---|---|---|
| 0.50 | 29% | 2 of 4 |
| 0.65 | 8% | 2 of 4 |
| **0.70** | **4%** | **2 of 4** ← chosen |
| 0.80 | 0% | 1 of 4 |

## Two gates, not one

```python
settle  = min(is_factual, cheaply_checkable, unverified)   # one command would end it
absence = min(is_factual, absence_claim,     unverified)   # "nobody has…" needs a survey
```

A single `min` **cannot** flag an absence claim — an absence is exactly what is *not* cheaply
checkable. But dropping `unverified` from path B over-corrects the other way: it then fires on
every *measured* negative ("0 drift signals"), which put the block rate at 62%. Drop
`cheaply_checkable` only. That one term is what separates a surveyed absence from an invented one.

## Honest limits

- Catches **2 of 4** known errors. `bounding_box` (0.54) and `vendor_docs` (0.40/0.50) slip
  through. This is a cheap filter, **not a safety net**.
- Sentence-level judging has no context. *"Same recipe, same probes, nothing changed"* is
  flagged fairly — standing alone it carries none of its evidence.
- **Fails open** everywhere (network, key, timeout, malformed input → silent exit 0), and caps
  at 3 blocks per session. A guard that blocks work when it breaks is worse than no guard —
  same posture as `jev-axi hook pre-tool-use --on-error allow`.
- Repeated runs returned identical scores because jev-axi caches responses; that is **not**
  measured run-to-run stability.

## Install

`jev-axi setup safety` writes `.claude/settings.json`. Not touched without the captain's word.

```json
{ "hooks": { "Stop": [ { "hooks": [ { "type": "command", "command": "jev-stop-guard" } ] } ] } }
```

Related: [[Jev - Validation Discipline]] · [[Jev - Field Findings]] · [[jev-axi]] · [[00 - Jev Master Index]]
