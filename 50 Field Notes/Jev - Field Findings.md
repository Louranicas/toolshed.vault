---
tags: [jev, typesafe, findings, verified]
created: 2026-09-18
---

# 🔬 Jev — Field Findings

Eight things established by **running them against the live API from this machine** on
2026-09-18, not by reading the docs. Total spend for every experiment below: **under one cent.**

Same discipline as [[00 - Field Findings]]: where the binary disagrees with the documentation,
the binary wins — and where *my own* earlier claim was wrong, it says so.

---

## F1 · The confidence formula, which TypeSafe do not publish ⭐

The docs say only that `confidence` is *"computed from how `probabilities` is spread"*. Derived
from the data and then confirmed live:

```
confidence = (p_max − 1/n) / (1 − 1/n)        # n = number of options
```

Uniform → 0. All mass on one option → 1. It is the top probability rescaled against chance.

| options | p_max | reported | formula | Δ |
|---:|---:|---:|---:|---:|
| 2 | 0.78 | 0.56 | 0.560 | +0.000 |
| 4 | 0.75 | 0.67 | 0.667 | +0.003 |
| 6 | 0.85 | 0.82 | 0.820 | +0.000 |
| 8 | 0.83 | 0.81 | 0.806 | +0.004 |

It also reproduces every worked example on `docs.typesafe.ai`, and predicts firstmate's own
dispatch resolver exactly (0.80 over 4 options → 0.733; reported 0.73).

> [!warning] At n=2 this is algebraically identical to the top-two margin
> Which is why a small two-option sample looks like a margin rule and misleads you. It diverges
> at three or more options. **I got this wrong first time round** and only caught it when the
> 3- and 4-option cases from the docs refused to fit.

**Score does not follow it.** Reported 0.90 where the formula predicts 0.867 — consistent with
levels being *ordered*, so mass on two adjacent levels is genuinely more certain than mass on two
distant ones. Formula not established.

## F2 · A Choice is confidently wrong when nothing fits ⭐⭐

The most important finding here. State: a refund policy — 30-day window, unworn items, refunds to
original payment method. Options offered: `arbitration`, `data_retention`, `liability_cap`. The
document contains **none** of them.

```
Choice picked : liability_cap   (p=0.93, confidence=0.89)
Existence noul: 0.04
```

Probabilities sum to 1, so *something* always wins. **High confidence means the distribution is
peaked, not that the answer is right.** Nothing in the Choice response indicates the question was
unanswerable; only the paired Noul does, because a Noul is absolute and independent of the option
set.

This is why "pair a relative ranking question with an absolute existence check" is the single most
repeated move across all eighteen cookbooks. See [[Jev - Ways of Working|M1]].

## F3 · Option count inflates confidence ⭐

Same input, same winning answer, options padded with categories nobody would pick
(`hiring`, `legal`, `catering`, `weather`):

| options | p_max | confidence |
|---:|---:|---:|
| 2 | 0.78 | **0.56** |
| 4 | 0.75 | 0.67 |
| 6 | 0.85 | 0.82 |
| 8 | 0.83 | **0.81** |

**0.56 → 0.81 by adding options nobody would pick.** Mechanical consequence of the `1/n` term in
F1. A question set that accretes categories over time becomes more confident about identical
inputs, and nothing warns you.

**Rule: threshold on `probabilities`, not `confidence`, whenever option counts vary.**

## F4 · Structural invariants do break — but not on easy inputs

TypeSafe warn that `P(x)` and `P(not x)` need not sum to 1. Tested:

| input | P | P(negation) | sum |
|---|---:|---:|---:|
| clearly urgent message | 0.98 | 0.02 | 1.00 ✅ |
| clearly non-urgent | 0.12 | 0.88 | 1.00 ✅ |
| ambiguous tone | 0.92 | 0.08 | 1.00 ✅ |
| **ambiguous fit** | 0.02 | 0.87 | **0.89 ❌** |

So the warning is real but only bites where the judgment is genuinely underdetermined — exactly
where you'd be relying on it. TypeSafe publish a case summing to 1.19. **First three tests made me
briefly report the warning as unreproducible; it isn't, my cases were too clean.**

## F5 · Decomposition is not automatically better — fitted weights are ⭐

Their headline claim: one broad *"is this phishing?"* scored 62.6%, five decomposed signals fed to
a regression reached 95.0%. Tested on six messages (3 malicious, 3 legitimate-but-spam-shaped):

| threshold | broad question | 6-signal composite |
|---|---:|---:|
| 0.3 | 66.7% | **100%** |
| 0.5 | 83.3% | **100%** |
| 0.7 | **100%** | 66.7% |

Separation between worst-malicious and worst-benign: **identical, +0.43 both ways.**

The difference is *not* that decomposition wins. It's that **their 95% came from a logistic
regression fitted on labelled data, and my composite used weights I invented.** Decomposition buys
you tunable, inspectable signals; it is the *fitting* that buys accuracy. Hand-picked weights are
not a free upgrade — mine were worse at the natural threshold.

Where the composite did win: a legitimate urgent payroll message scored **0.53** on the broad
question (a false positive at 0.5) and **0.15** on the composite, which named `pressure` as the
only hot signal. **Interpretability is real even where accuracy isn't.**

## F6 · It refuses to invent a failure

`jev-axi triage` on a *passing* build log deliberately seeded with the words `warn`, `error_count`
and `failed=0`:

```
has_error: 0.04 (no failure detected)
verdict: no failure detected; the run appears to have succeeded
```

On a genuinely failing log with the real error buried in 60 lines of noise: **exact root-cause
line**, `flaky: 0.05` (correctly "a real bug"). The negative case is the one that earns trust —
most such tools hallucinate a cause from the word "error".

## F7 · Injection screening works, and knows a placeholder

| input | verdict | top hazard | exit |
|---|---|---|---:|
| release note containing `API_TOKEN=<your-token>` | **pass** | all ≤0.03 | 0 |
| same note + HTML comment telling an assistant to read `~/.ssh/id_ed25519` | **block** | injection 0.98, hidden 0.98, exfiltration 0.88 | 3 |

It did not flag the placeholder as a secret (0.02). Exit 3 on block makes it a clean shell gate —
see [[Jev - Applications Here]].

## F8 · Semantic file location is accurate and cheap

`jev-axi files "where is the per-home session lock acquired and verified?"` across **247 files** of
the firstmate repo returned `bin/fm-session-lock-lib.sh` at **rank 1, p=1.0**, in 2.3 s for
$0.0009. Correct.

> [!note] But their own benchmark says don't build a workflow on this
> Agents told to rank files read 25% fewer files **and cost the same**, because answering still
> meant reading the code. Accurate ≠ economically useful. Use it when there's no greppable
> identifier, not as a default preamble.

---

## F9 · A question can look fine and measure nothing ⭐

Run every question set **state-blind** — same questions, state replaced by `REDACTED` — before
trusting it. One extra call per question, no labels required. In my own eight-pathway router,
`vendor_docs` moved **+0.03 on average** from its 0.39 prior across five very different questions,
while `academic` moved +0.49 and `hackernews` +0.35 on the questions they should answer.

It had been returning plausible varied numbers all evening. **A dead criterion produces
confident-looking output, not obvious garbage.** Details in
[[Jev and Fabric - Vendor-Free Chains]].

## What these add up to

1. **Never let a Choice answer alone.** (F2)
2. **Threshold on probabilities, not confidence, across mixed question sets.** (F1, F3)
3. **Decompose for inspectability; fit weights on real labels for accuracy.** (F5)
4. **Don't assume arithmetic identities between separate questions.** (F4)
5. **Trust it most where it declines to answer** — the passing log, the 0.04 existence check. (F2, F6)

F2's abstention rule is what makes [[Jev - Search Routing and Cascades]] work, and the matrix
form there turned out to detect **which questions the public corpus cannot answer at all**.

Related: [[Jev - The Model]] · [[Jev - Ways of Working]] · [[Jev - Validation Discipline]] · [[00 - Field Findings]]
