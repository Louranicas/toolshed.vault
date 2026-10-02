---
tags: [jev, typesafe, validation, calibration, process]
created: 2026-09-18
---

# 📐 Jev — Validation Discipline

The seven-stage procedure for putting a cheap classifier behind an expensive one.

> [!important] This is the most valuable thing in the whole corpus
> It is **model-agnostic**. It survives Jev disappearing tomorrow, and applies to any cheap
> classifier you put in front of an expensive one. Read it as general engineering, not vendor docs.

Opening line sets the stakes: *"Jev is cheap enough that the temptation is to switch first and
measure later. **Every project that reported trouble skipped this part.**"*

---

## 1 · Shadow mode first
Run the questions **next to** the existing implementation, acting on nothing. Log five things:
state, question version, **every probability**, the current system's decision, and what Jev would
have done.

> "A day or two of real traffic gives you a labeled set and a disagreement list for free."

Annotate-only mode is the same idea for hooks and CI: report what it *would* have blocked.

## 2 · Build a labelled set from real traffic
- A few hundred examples, **from production rather than invented**, including the rare classes.
- **Label from outcomes where you can** — what the human actually did, whether the ticket was
  reopened, whether the commit was reverted. Not opinions.
- Hold out a test split you don't look at while tuning.
- **Beware label noise:** in one security benchmark *at least 38% of the apparent false positives
  were wrong labels, not wrong answers.* Hand-audit disagreements before believing your own FP rate.
- Public corpora may be in the training data. Prefer your own.

## 3 · Compare against three baselines, not one ⭐
1. **What runs today** — the LLM call, the regex, the human queue.
2. **The dumb baseline** — a keyword list or two-line rule. *In the phishing benchmark this scored
   **91.8%** and beat Jev's best single question.* → **"If it wins, ship it and stop."**
3. **An LLM asked the same decomposed questions.** *Twice now, that matched Jev's accuracy at
   roughly 27× the cost.* **This is the comparison that tells you whether you are buying accuracy
   or price** — and keeps you honest about which one you needed.

TypeSafe publish `system-one-adapter` (Python), a drop-in client backed by OpenAI or Anthropic, so
the same questions can run against an LLM for the A/B.

## 4 · Measure all four axes

| Axis | How |
|---|---|
| **Accuracy** | Per class, not overall. Confusion matrix; recall on the class that matters |
| **Cost** | Input tokens × $0.042/M, per 1,000 items, against the current bill |
| **Latency** | p50 and p95 at your real payload size, from where your code runs |
| **Coverage** | What fraction decides automatically at your thresholds, and how much goes to review |

> *"A result like 'same accuracy, 1/300th the cost, 0.3 s instead of 8.5 s' is the shape of a good
> outcome. **'Slightly better accuracy' usually isn't real.**"*

## 5 · Set thresholds from the data
- Sweep over the labelled set; pick from the precision or recall you need — **per action, not per
  question.** One probability can drive several actions at different cutoffs.
- **Keep a review band.** Probabilities move ~0.01 between runs and borderline labels flip. Worked
  example: routing the 0.3–0.7 band (**4.6% of mail**) to a human left **99.50%** accuracy on the rest.
- Set the band by what a mistake costs. A wrong auto-block needs a wider band than a wrong hint.
- **Re-check after any wording change.** *"Higher confidence is not evidence of better wording;
  only the held-out set is."*

> [!warning] And see [[Jev - Field Findings|F1]]
> Confidence is `(p_max − 1/n)/(1 − 1/n)`, so it is **not comparable across questions with
> different option counts**. Sweep thresholds on `probabilities` unless the option count is fixed.

## 6 · Roll out in stages
1. Shadow, acting on nothing.
2. **Act only in the confident band**; everything else keeps the old path.
3. Widen the band once the logs show the confident band is right.
4. Keep the old path behind a flag, and **alert on rate: a silent drift in the "review" share is
   the first sign something changed.**

> **"Pin the model version before stage 2, or a model update will move your thresholds under you."**

The drift alarm is on the **review-band share**, not accuracy — a rate metric you can compute with
no labels at all. That is the clever part.

## 7 · Keep the eval
Save the labelled set and a script that runs it. *"It costs cents to re-run, catches regressions
when someone edits a question, and tells you whether the next model version is better or worse for
your data."*

---

## Why pinning matters more here than with an ordinary LLM

The whole programming model is: **code owns the decision, the model supplies a calibrated
probability, you threshold it.** Your thresholds are *fitted constants tuned against one version's
calibration*.

When an alias moves: probabilities shift → your auto-approve rate shifts → your review share
shifts. **Nothing errors. No test fails. Nothing in your code changed.** The quietest possible
production regression.

Operationally:
1. Pin the versioned ID (`jev-1.13.0`, never `jev-latest`, never `jev-preview`).
2. **Log `response.model` on every call** and dimension metrics by it — two model IDs on a
   dashboard means a config leak.
3. Keep a golden set; diff **distributions**, not just labels, before switching.
4. Treat `(model_version, threshold_set)` as one atomic unit that ships together.
5. `model` is a per-call parameter, so **canarying is trivial** — a genuine advantage over
   providers that bake the model into the client.

> [!caution] Both SDKs default to `jev-latest`
> Unpinned is the out-of-the-box state. So does `jev-axi`. Opt in deliberately.

---

## The honest caveat about the corpus these numbers come from

Almost every figure above is a **citation**, not a measurement the publishing repo made. It says
so: *"Compiled from the TypeSafe docs, cookbooks, workflow evals, and about 30 community
projects."* It measured two things itself — an 88-case smoke test of hand-written fixtures against
its own questions (**violating its own stage-2 rule**), and an N=6 agent benchmark whose raw data
is gitignored.

Its most credible passage is the one against its own interest: *"the differences are within
run-to-run noise… file ranking does not make it cheaper. Forcing jev-axi adds turns."* They
re-scoped the product on that negative result.

Related: [[Jev - Field Findings]] · [[Jev - Ways of Working]] · [[Jev - The Model]]
