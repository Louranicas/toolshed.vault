---
tags: [jev, typesafe, model, api, primitives]
created: 2026-09-18
---

# 🧠 Jev — The Model

TypeSafe left stealth **2026-09-15** ($40M seed, DCVC; founder Diogo Almeida, ex-OpenAI, credited
co-inventor of RLHF). Jev is their first and only model, named for **William Stanley Jevons** — an
explicit bet on the Jevons paradox: make judgment cheap enough and usage explodes.

> "System 1 thinking is fast and intuitive. System 2 is slower and more deliberate."

The industry sells System 2 — longer reasoning traces. This is the deliberate opposite, and the
framing inversion is the product.

## What it will not do

- **No text generation at all.** No replies, no code, no explanation of its reasoning.
- Cannot emit a value outside your options — *"your code never has to recover a value from
  generated prose."*
- Text only. No images, audio or video.

> [!danger] "Zero hallucinations" means the schema is guaranteed, not that the answer is right
> The sharpest sentence in the corpus. [[Jev - Field Findings|F2]] is what it looks like in
> practice: a confidently wrong answer at 0.89 confidence.

## Economics — the reason the patterns look the way they do

| | |
|---|---|
| Input | **$0.042 / M tokens** |
| Output | **free — $0** |
| Server-side inference | **68–151 ms** measured (median ~112) |
| Context | 64k/request; **~32k for `state` + the longest question** (docs contradict themselves; assume 32k) |
| Rate limits | 1,200 req/min · 250k tok/s — *"adjusting dynamically… can change without notice"* |
| Choice options | max **255** (reliable to ~240) · Score levels max **10** |

Free output + flat latency ⇒ **N questions cost roughly one state, not N states.** Measured at
**12.2× cheaper and 10× faster** with identical answers. This is why *"ask a lot of questions"* is
the actual guidance rather than a slogan.

> [!note] You need far less concurrency than instinct suggests
> At ~0.25 s/call, saturating 1,200 req/min takes about **five** requests in flight. TypeSafe's own
> cookbooks never exceed **12** workers. Above ~20 you are manufacturing 429s.

## The contract

```http
POST https://api.typesafe.ai/v1/systemone
Authorization: Bearer $TYPESAFE_API_KEY
```
```json
{ "model": "jev-latest",
  "state":  "…string | object | array…",
  "questions": { "your_id": { "type": "choice|score|noul", "instructions": "…", "criteria": … } } }
```

Response: `model` (the **resolved versioned id**), `answers` keyed by your ids, `usage.input_tokens`
/ `output_tokens`. Errors: 401 · 422 · 429 · 529.

**Question IDs are not sent to the model.** Write the complete question in `instructions` even when
the id looks self-explanatory. Option *names*, by contrast, **are** sent and are meaningful input.

`GET /v1/models` lists only aliases; versioned ids work whether or not they appear. There is **no
streaming, no batch endpoint, no fine-tuning** — customisation is via `state`, `instructions` and
`criteria` only.

## The three primitives

| Type | Answers | Returns |
|---|---|---|
| **Choice** | which of these options? | `choice`, `probabilities`, `confidence` |
| **Score** | which level? | `score` (**continuous expected value**), `legend`, `probabilities`, `confidence` |
| **Noul** | is this true? | `noul` (0–1) — **no confidence field; the number is the uncertainty** |

Questions are evaluated **independently and in parallel** against the same state. One answer never
becomes hidden context for another — *"so adding more questions does not create context-rot."*

`criteria` accepts `string | object | array | null`. Escalate from string to object when two
options keep being confused, using parallel keys `{what, not_for, examples}`.

> [!caution] A fourth type `bounding_box` appears in an API error — but is probably NOT real
> The live 422 enumerates `noul, choice, score, bounding_box`, and sending it returns
> *"Bounding-box questions are not enabled for your organization."* **Do not read that as a gated
> feature.** Corrected 2026-09-18: the string appears in exactly one repo's *machine-generated*
> commits, which were then reverted against the real OpenAPI. It is absent from docs.typesafe.ai's
> full `llms.txt` dump, from the models page (which states "No image, audio, or video input"),
> from Vercel's AI SDK spec, and from ~10 community SDKs. The likeliest explanation is an agent
> inventing a fourth type by analogy with vision APIs. The server-side string may simply be a
> placeholder. **Reported here as confirmed on first pass; that was over-crediting a single
> ambiguous signal.**

## Confidence

`(p_max − 1/n) / (1 − 1/n)` for Choice — **derived and verified here**, not documented. See
[[Jev - Field Findings|F1]] and [[Jev - Field Findings|F3]] for why that means you should usually
threshold on `probabilities` instead.

TypeSafe's own position: *"you are never locked into our definition, which is exactly why we give
you the full `probabilities`."*

## RLCD, and what it claims

Not RLHF, not RLVR: **Reinforcement Learning for Calibrated Decisions.**

> "Outcomes assigned a probability of 0.2 should occur about 20% of the time… **These rates
> describe groups of predictions, not a guarantee about any single answer.**"

Their critique of RLHF is worth keeping: it *"can reward sycophancy and confident-sounding
hallucinations"*, and **mode dropping** — preference optimisation narrows the output distribution.
*"An output can be compelling to a person without being reliable enough for unattended
automation."*

## Documented weaknesses — they publish these themselves

`/model-jaggedness/jev-1.13` is unusually candid. Nine failure modes: literal reading of
instructions (*"it answers the question you wrote, not the one you meant"*); unreliable arithmetic;
worse at counting as lists grow; numeric representations (hex/RGB) worse than semantic (colour
names); dates read as text not ordered quantities; degraded by double negatives and indirection;
**context rot from large irrelevant state**; **not robust to adversarial content in state**; and
contradictory instructions-vs-criteria.

Plus: **no "I don't know" state.** Asked a genuinely information-free question it still answered
0.78/0.22 rather than refusing. The caller owns the floor.

Related: [[Jev - Ways of Working]] · [[Jev - Field Findings]] · [[Jev - Validation Discipline]] · [[jev-axi]]
