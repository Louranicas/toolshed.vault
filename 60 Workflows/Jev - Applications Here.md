---
tags: [jev, typesafe, applications, workflows, habitat]
created: 2026-09-18
---

# 🎯 Jev — Applications in this habitat

What this is actually *for* here, mapped onto the shapes already in the vault:
`[[Tool Chaining Patterns|P1–P9]]`, `[[Clustering Shapes]]`, `[[Autonomous Triggers]]`.

Ranked by how defensible each one is, not by how exciting.

---

## A1 · Anchor re-verification — the best fit in the vault ⭐⭐

`[[Code Anchors - Notes That Land on Source]]` already frames the problem exactly right: *the
vaults are claims about the codebase*, so a claim carries an `expects` fragment and a claim gone
false is **detectable, not just a stale link**.

String matching catches half of it. Jev catches the half you can't:

```
1. string-match the `expects` fragment in source     ← code, free, catches "fabricated"
2. if it still matches, ask ONE 3-way Choice:
      supports / contradicts / says_nothing
   + an existence noul (F2 — never let the Choice answer alone)
3. auto-accept at confidence >= 0.8; everything else to a review queue
```

The case this catches and anchors cannot: **the fragment still exists, so the anchor holds, but
the surrounding code now means something different.** A silently-false claim that passes its own
check.

`just doc-anchors` already knows where all 58 documented flags land. At ~$0.0001 per anchor that's
**under a penny to re-verify the whole documented surface**, cheap enough to run on every deploy.

Straight from the `citation_check` cookbook, including the deterministic-first ordering you
already practise ([[Jev - Ways of Working|M8]]).

## A2 · Screening everything fetched ⭐

Issue bodies, vendored READMEs, third-party tool output, any page pulled from the web.

This is the one place where cheap-model-first is **not an optimisation but a different security
posture**: an expensive agent cannot judge whether text is hostile *before* the text is in its
context, and by then it is too late.

`P1`-shaped, and exit 3 makes it a clean gate:

```bash
curl -fsSL "$URL" -o page.md
jev-axi guard --state page.md || { echo "blocked: untrusted content" >&2; exit 1; }
process page.md
```

Verified in [[Jev - Field Findings|F7]].

> [!warning] It is a filter, not a boundary
> Stated in TypeSafe's docs, the community corpus, and the CLI docs. And the screener itself
> **is not robust to adversarial content in the state** — the thing reading hostile text can be
> steered by hostile text. Never the only thing between untrusted input and harm.

**Turso-retrieved snippets (2026-09-22).** When the text is a database row rather than a raw fetch, do not stop at `guard`. SQL retrieves (`vector32` blob, `vector_distance_cos`, linear scan, `WHERE` to shrink). One Jev fan-out judges the snippet. Code writes `jev_judgments`. Full loop: [Jev in Turso Workflows](obsidian://open?vault=turso.vault&file=20%20Build%20Guides%2FJev%20in%20Turso%20Workflows). Official batteries: [classifying RAG passages](https://docs.typesafe.ai/cookbooks/classifying_rag_passages) and [re-ranking](https://docs.typesafe.ai/cookbooks/rerank_typesafe). Do not send `TURSO_TOKEN` or engine-private rows. `tursodb mcp` is an LLM-to-SQL path, not this one.

## A3 · Log triage on every failed job ⭐

`P2` + `P9`. A 255-line tail costs ~$0.0004 and returns root-cause line, category, severity and a
**flakiness probability** in one call.

The two thresholds that pay for themselves:

- `flaky >= 0.6` → **retry automatically** instead of waking an agent to read 2,000 lines
- `has_error < 0.35` → **"no failure detected"** — stops an agent hunting a bug that isn't there

Verified in [[Jev - Field Findings|F6]], including the negative case.

Natural home: the `on-break` cascade in [[Autonomous Triggers]], and `mode: triage` in CI.

## A4 · Jev in the `verify` slot of P9 — never the `remediate` slot ⭐

[[Tool Chaining Patterns|P9]] holds that **an agent which remediates its way past its own gate has
defeated the gate**. Jev is unusually safe in the *verify* position, precisely because of what it
cannot do:

| P9 requires | Why Jev suits |
|---|---|
| the check must not be gameable by the thing being checked | it has no tools, cannot act, cannot generate text, cannot be argued with |
| the verdict must be inspectable | you get a number your own code thresholds, not an assertion |
| some gates must be deliberately un-remediable | it has no remediation capability at all |

**And the inverse holds absolutely: never put it in `remediate`.** That builds the exact thing the
rule forbids.

Second-order fit: P9 reports attempt counts because *"VERIFIED after 2 attempts"* differs
materially from *"VERIFIED"*. With a probabilistic verifier, log the **probability at each
attempt**. A check passing 0.62 → 0.71 → 0.83 is a system converging. One passing at 0.51 after
three tries is a system being fixed until the check stops complaining.

## A5 · Triggers — Jev as the predicate, never the event source

[[Autonomous Triggers]] landed on *probe the state, don't subscribe to an event*, fire on the
**rising edge**, with a `debounce`. All three survive contact with a probabilistic predicate —
and the debounce becomes load-bearing rather than defensive:

> Probabilities wobble by ~0.01 between runs and borderline cases genuinely flip. A naive
> threshold trigger would chatter. **Rising-edge-only + debounce is hysteresis**, which is the
> same device as the "review band" the TypeSafe corpus arrived at from the opposite direction.

What Jev adds to a probe is matching on **meaning** rather than syntax:

```toml
# regex catches what you thought to enumerate
regex = "^error|could not compile"

# a noul catches what you didn't
# "has this build started failing for a reason it was not failing for before?"
```

Keep the finding that probes beat events. **Jev goes inside a probe as its predicate. It is not
an event source** — it has no push, no stream, no subscription.

## A6 · Matrix fan-out, with one axis now free

[[Clustering Shapes]] organises fan-out by *who decides the width*. Jev changes the economics of
one axis only:

- **items axis** — still costs one request per item. State is sent per request.
- **questions axis** — **effectively free.** Output tokens cost $0, the state is ingested once,
  and every question is evaluated against it in parallel. Measured at **12.2× cheaper and 10×
  faster** than the same questions as separate calls, with identical answers.

So `matrix-quality`'s repos × checks shape inverts: widen the *questions* dimension without
thinking about it, and keep discipline on the *items* dimension. Twenty questions about one
artifact cost about the same as one.

Corollary from the `autoresearch` cookbook: **don't pre-filter your candidate questions.** One more
question costs no extra request.

## A7 · Fleet dispatch routing

Already live in firstmate: one Choice over rule conditions, every gate in local code afterwards,
every outcome exits 0 so it can never block a dispatch. See [[Jev - The Model]] for the wire
contract it uses.

---

## A8 · Routing our own research ⭐

Built and measured — see [[Jev - Search Routing and Cascades]]. Jev picks which of eight search
pathways will answer a question, code dispatches to the real service, and anything fetched is
screened. The matrix variant doubles as a **research-gap detector**: questions where every
pathway scores below 0.5 are ones the public corpus cannot answer.

## Where not to bother

> [!danger] A regex that already decides, wins
> Their own phishing benchmark: a **two-line rule scored 91.8%** and beat Jev's best single
> question. The corpus instruction is *"if it wins, ship it and stop."* This habitat already
> works that way — `[[Claim-Time Guard]]` fires local rules at command time and should stay local
> rules. `[[Assimilation - Rules That Fire]]` is the same instinct. Don't probabilise a decided
> question.

**Exploration.** Measured and refuted by its own authors: agents told to rank files read 25% fewer
files **and cost the same**, because answering still meant reading the code. See
[[Jev - Field Findings|F8]] — accurate is not the same as economically useful.

**Anything touching `my-diary.vault`.** Personal content to a third party whose data-residency and
retention terms are not published. The corpus is blunt about this: *"don't point jev-axi at data
you can't share with TypeSafe."*

**Merge decisions and anything needing an auditable rationale.** You get numbers with no reasoning.
Firstmate already escalates merges to the captain; that is correct and this doesn't change it.

**Counting, arithmetic, dates.** Documented weaknesses. Extract the parts with Choices and let code
do the calendar — [[Jev - Ways of Working|M4]].

---

## What I'd build first

1. **A2** — a one-line shell gate, no state, no calibration, immediate value.
2. **A3** — one command on the existing `on-break` cascade.
3. **A1** — the genuinely novel one, and it extends work already half-done.

A4/A5/A6 are *how to think about* wiring it into the habitat, not standalone builds.

Related: [[Jev - Field Findings]] · [[Jev - Ways of Working]] · [[Jev - Validation Discipline]] ·
[[Tool Chaining Patterns]] · [[Clustering Shapes]] · [[Autonomous Triggers]] · [[Cascade Engine]]
