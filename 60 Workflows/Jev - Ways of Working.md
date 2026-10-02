---
tags: [jev, typesafe, patterns, question-design]
created: 2026-09-18
---

# 🧩 Jev — Ways of Working

The craft, distilled from all 4 pattern pages and all 18 cookbooks. **M-numbers are the recurring
structural moves; A-numbers are the anti-patterns.**

> [!tip] If you read one line
> *"Ask the most explicit, narrow, specific, atomic question you can."* The docs flag this as
> **"probably the most important concept in this guide."**

---

## The moves

### M1 · Pair a *relative* ranking question with an *absolute* existence check ⭐⭐
The most repeated move in the corpus, and the one [[Jev - Field Findings|F2]] proves the hard way.
A Choice's probabilities sum to 1, so something always wins; a Noul is independent of the option
set and can be near zero for everything.

> "Choice probabilities always add up to 1, so some line ranks first even when the document
> doesn't answer the question… the Noul probability doesn't depend on the other options, so it can
> fall near zero."

Surfaced as `match_exists`, `answer_exists`, `relevant_file_exists`. Below ~0.35, **the ranking is
only the least-bad option** — widen the search. The in-question variant is adding a `none` option.

### M2 · Decompose one judgment; compose in code
`is_spam` → six Nouls. `tool_calls_are_correct` → nine path-anchored Nouls. Per-field beats
holistic empirically: one cascade's overall judge read **0.56** where the field flag read **0.95**.
But see [[Jev - Field Findings|F5]] — decomposition buys inspectability; *fitting the weights on
real labels* buys the accuracy.

### M3 · Fan out speculatively — output tokens are free
State is sent once and ingested once; output costs $0. **12.2× cheaper, 10× faster, identical
answers.** Corollary: don't pre-filter candidate questions.

### M4 · The model never emits the value — it *picks* from spans code found
Regex/NER proposes candidates → Choice picks → code copies verbatim. *"It cannot invent a value or
transpose a digit."* Dates: seven Choices over closed sets, code does the calendar. This is the
direct consequence of *"jev-1.13 is not trained to generate text."*

### M5 · Thresholds live in one named dict; the question never asks "should I act?"
> "**None of the four asks whether to include the passage.** That call sits in the code below,
> where changing it means editing a number instead of rewording a question."

So one set of probabilities drives `strict` and `permissive` policies with no new call.

### M6 · Make abstention first-class — three variants, none costing a call
- a **band** on a Noul (`0.30–0.70` → uncertain)
- a **floor** on top-probability or confidence
- **answer coarsely** — report the parent label instead of abstaining (measured 40% → 70% useful
  on the unsure half)

### M7 · Aggregate with `max`/`min`, never mean or product
*"a `max`-style gate, so one confident red flag is enough instead of being averaged into
silence."* Composite confidence is the **minimum** over the parts — *"a product answers a
different question."* Mean only where it's genuinely a group property.

### M8 · Let code answer everything code can answer, first
String-match before any call (*"no model is needed to find that out"*). `if len(labels) == 1:
return`. Arithmetic in code. Hard allows and hard denies in code; **send Jev the ambiguous middle.**

### M9 · Two stages only when the second stage's *inputs* don't exist yet
Exactly three legitimate cases in the corpus: fetch the shortlist's full text; blocks that don't
exist until pass 1 answered; each answer picking the next question's options. Everything else is
one call.

### M10 · Score levels can *be* the outcomes
Three levels, three actions, route by round-to-nearest. *"There is no threshold constant anywhere
in this file… You can also write these descriptions before you have seen a single score, which is
not true of a number you have to fit."*

### M11 · Put IDs in the state so the model can point at things
`L052| …`, `B003| …`. Turns "where is it?" into a Choice over ID options.

### M12 · State is the *pair*, not the item
`{query, passage}`, `{entity_a, entity_b}`. Hence cost scales with *k*.

### M13 · Use JSON structure in `instructions` and `criteria`
Parallel keys across options — `{what, not_for, examples}` — *"so the model can compare them
directly."* Escalate string → object **when two options keep being confused**, or when scores keep
landing between neighbouring levels on inputs you think are clear.

### M14 · Reference state by backticked path
``"Does `ticket.messages[0].text` request a refund?"`` — directly counters the documented
weaknesses at indirection and large states.

---

## The anti-patterns

> The jaggedness page closes with: *"avoid the following: asking the model something code can
> compute exactly; hiding several judgments inside one question; System Two tasks; giving it more
> context in `state` than the question needs."*

**A1 · Broad or compound questions.** The named bad versions: `is_spam`, `tool_calls_are_correct`,
"is this extraction good?"

**A2 · Asking it to compute.** Counting (*"the error grows with the size of the thing being
counted"*), date ordering and duration, hex/RGB over colour names. **And never interpolate a
Score** — the levels are weak in numerical calibration.

**A3 · Asking it to generate.** *"While you can force it to by chaining choices, this will not work
well and will be very slow."*

**A4 · Dumping the whole record into `state`.** *"Accuracy falls as the state grows with content
unrelated to the decision. Jev suffers from context rot."*

**A5 · Wording that names the wrong fact.** "same paragraph" vs "mid-sentence" scored 0.77 vs 0.22
on the same line. **When a judgment feeds a threshold, name the narrowest fact that decides it.**

**A6 · Inverted polarity.** A Noul whose `true` case describes the negative performs worse. Frame
questions so the **escalate case is the `true` case**.

**A7 · Relying on structural invariants.** Same question as Noul vs 2-option Choice: `0.22` vs
`yes 0.01 / no 0.99`. A claim and its negation: `0.72 + 0.47 = 1.19`. **Don't carry a threshold
tuned on a Noul over to a Choice.** Confirmed here — [[Jev - Field Findings|F4]].

**A8 · A single global threshold.** *"We picked these four numbers for this corpus. Treat them as a
starting point, not defaults."* And [[Jev - Field Findings|F1]] gives the structural reason:
confidence isn't comparable across differing option counts.

**A9 · One question per call.** *"Coding agents fall into the one question per call habit more than
people do."* Given M3, this is pure waste.

**A10 · Trusting `state` as non-adversarial.** *"State is data, and jev-1.13 does not treat it as
hostile by default."*

**A11 · Reading repeatability as accuracy.** Both consistency cookbooks carry it in the chart
itself: *"100% repeatability does not imply correctness."*

**A12 · Fixing a bad answer by moving the threshold.** *"The right fix is usually to phrase the
condition better, not to move the threshold."*

**A13 · Using a Noul for degree.** `0.5` means *unsure*, not *medium*.

**A14 · Aliases as a silent version change.** Pin the versioned ID once thresholds are tuned.

---

## Decision guide — task shape → move

| Task shape | Reach for |
|---|---|
| Several judgments about one document | One request, all questions — **including ones you may not use** |
| One judgment from several independent factors | Composite scoring: one Score per factor, weights in code |
| A category picks the code path, paths differ in risk | Intent routing + **per-action** confidence thresholds |
| Some cases too hard to act on | Confidence gate → human, or **answer one level up** if labels are hierarchical |
| Find the right item among thousands | Cheap recall (BM25/embeddings) → one Noul per pair → sort |
| Find the right line inside one document (≤255 units) | Choice over line IDs **+ existence Noul** (M1, M11) |
| Pick from a large catalogue of similar-looking entries | Wide Choice → shortlist 3 → re-read with full text; **both stages may abstain** |
| Deep taxonomy | Per-node Choice over direct children; beam search K=3 (measured 4/4 vs greedy 2/4) |
| Two records may be the same entity | One Score whose **levels are the outcomes** (M10) |
| Retrieved context may be hostile or irrelevant | Nouls per (query, passage) → ordered threshold cascade |
| State lives in Turso | SQL shortlist (`vector_distance_cos`, `WHERE` on a linear scan) → one Jev fan-out on the snippet → code writes `jev_judgments`. [Jev in Turso Workflows](obsidian://open?vault=turso.vault&file=20%20Build%20Guides%2FJev%20in%20Turso%20Workflows) |
| A cheap model's structured output might be wrong | Per-field **"bad = TRUE"** Nouls → `max` gate → escalate (M7, A6) |
| Pull a value out of text | **Never ask for the value.** Spans from code → Choice picks → code normalises (M4) |
| Natural language → typed function call | Routing Choice + per-arg Choice over literals + a `stated` Noul; confidence = **min** |
| Are my answers stable enough to threshold? | Repeat N times; look at **per-question std dev**, not the label |

**Type selection:** Choice for one of a known unordered set — *and add `other`/`none` when the list
may not cover every input*. Score for an ordered rubric you can describe. Noul when the probability
itself is the signal. Tie-break: *prefer the type whose answer your code can act on directly.*

Related: [[Jev - Field Findings]] · [[Jev - Applications Here]] · [[Jev - Validation Discipline]] ·
[[Jev - Search Routing and Cascades]] — these devices applied to routing our own research
