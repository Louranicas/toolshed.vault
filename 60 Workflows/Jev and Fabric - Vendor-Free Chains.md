---
tags: [jev, fabric, chaining, clustering, pioneering, workflows]
created: 2026-09-18
---

# 🔗 Jev and Fabric — vendor-free chains

Two discoveries made on ORAC, 2026-09-18, neither of which appears anywhere in the public
corpus. Both follow from reading Fabric's source rather than its documentation.

Extends [[Jev - Search Routing and Cascades]]. Shape vocabulary from
[[Tool Chaining Patterns]] and [[Clustering Shapes]].

---

## 1 · Fabric is a composition engine that needs no LLM ⭐⭐

Fabric's 257 patterns are dead without a configured vendor. **Its extraction and templating
are not.**

`IsChatRequest()` returns false when none of pattern, message, context, session or attachment is
set — and on that path Fabric prints the fetched content and **never calls a model**. Verified:

```sh
fabric -u https://news.ycombinator.com/item?id=49717558     # 60,000 bytes of clean markdown
fabric -y <url> --transcript                                # YouTube transcript
```
Both with **no vendor and no Jina key configured**. Fabric is a universal extractor, today.

**And `--dry-run` renders a pattern with every plugin resolved, also without a model:**

```
## host
orac · user Louranicas · 2026-09-18        <- {{plugin:sys:*}}, {{plugin:datetime:today}}
## live fetch
# Models …                                  <- {{plugin:fetch:get:URL}} actually fetched it
```

The built-in plugins need no registration: `fetch:get`, `file:read`, `sys:*`, `datetime:*`,
`text:*`, `hash`. They nest, resolving inside-out.

> [!important] The synergy
> **A custom Fabric pattern becomes a committed, version-controlled STATE BUILDER for Jev.**
> Fabric assembles the state — remote pages, local files, host facts, `{{input}}` from stdin,
> `-v=#key:value` variables — and Jev judges the result. **Neither half needs an LLM.**

Built as `~/.local/bin/state-judge`. Measured: 7,763 bytes of state assembled including a
live-fetched docs page, zero model calls, then nine typed verdicts in 793 ms for **$0.00012**.

The full chain, `~/.local/bin/fetch-judge`:

```
fabric extracts   (no model)  ->  jev guard screens  (exit 3 blocks)
                              ->  jev recipe judges  ->  code decides
```

On the Hacker News launch thread: 60,000 bytes → six typed verdicts, **1.1 s, $0.00074**,
`contradicts_vendor 0.96`, `marketing_only 0.09`, and `independent_test 0.38 escalate` because the
thread genuinely is mixed. This is [[Tool Chaining Patterns|P2]], the JSON chain, with a
probabilistic selector at the junction and a **safety gate between fetch and read**.

---

## 2 · The state-blind control — and the dead criterion it found ⭐⭐

Borrowed from a community calibration audit and, as far as I can find, **run by almost nobody**.

**Method.** Ask the same question set twice: once with the real state, once with the state replaced
by `REDACTED`. One extra call per question. **No labels needed.**

**What it distinguishes:** a question that *discriminates* from a question that merely *has a prior*.

Run over my own eight-pathway search router, five questions:

| pathway | prior (state blind) | moves with state? |
|---|---:|---|
| `academic` | 0.31 | ✅ +0.49 on an RLCD question |
| `hackernews` | 0.39 | ✅ +0.35 on a design-rationale question |
| `x_social` | 0.34 | ✅ +0.29 on a practitioner question |
| `github_code` | 0.23 | ✅ +0.22 to +0.38 consistently |
| **`vendor_docs`** | **0.39** | ❌ **mean +0.03 across five very different questions** |

> [!warning] One criterion in nine was a passenger, and it looked fine
> `vendor_docs` returned 0.59 / 0.45 / 0.43 / 0.39 / 0.23 — plausible, varied, useful-looking
> numbers. Against its 0.39 prior it moved **+0.03 on average**. It was answering from its own
> wording, not from the question. **A bad criterion produces confident-looking output, not obvious
> garbage**, which is exactly why inspection cannot catch it and a control can.

**The general rule, which matters more than the fix:**

> Run the state-blind control on every question set before trusting it. It costs one call per
> question, needs no ground truth, and it is the only thing I have found that surfaces a dead
> criterion.

Corollary: the blind numbers **are** a free calibration map of your question set's priors. Worth
recording alongside the questions.

---

## 3 · Where this sits against the rest

- [[Jev - Field Findings|F2]] said never let a Choice answer alone. This says **never trust a
  question you have not run blind.**
- The abstention work bounds what the model may decide; the state-blind control bounds whether the
  question is measuring anything at all. Different failure, different control.
- Composition has its own limit — multiplying mid-range nouls understates the conjunction by ~0.1
  (measured; see [[Jev - Field Findings]]). So: **blind-test each question, then compose with max,
  and only multiply outside 0.2–0.8.**

## Related
[[Jev - Search Routing and Cascades]] · [[Jev - Field Findings]] · [[Jev - Ways of Working]] ·
[[jev-axi]] · [[Tool Chaining Patterns]] · [[Clustering Shapes]] · [[00 - Jev Master Index]]

---

## 2026-09-19 — two traps, both of which produced confident wrong answers

Measured on ORAC, fabric in `fedora-toolbox-44`. The claim above is **correct** — plugins
do render with no model — but *where* you put the template decides everything.

**Trap 1 — plugins expand only inside a pattern's `system.md`.**

```sh
# pattern file contains {{plugin:sys:hostname}} / {{plugin:datetime:today}}
echo x | fabric --dry-run -p jevprobe2      # -> "host toolbx"  "today 2026-09-19"   RENDERED
echo "{{plugin:sys:hostname}}" | fabric --dry-run    # -> "{{plugin:sys:hostname}}"  VERBATIM
```

Same template, same flag, opposite result. I tested it in *input* position first, concluded
"no plugin expands under `--dry-run`", and nearly wrote that correction into this note.
Fabric templates the **pattern**, not your input.

**Trap 2 — `{{plugin:fetch:get:URL}}` inside a pattern fails.**

```
could not get pattern jevfetch: missing required variable:
    margin: "1.25rem 0"
```

That `margin:` is CSS *from the fetched page*. Fabric fetches, then re-templates the fetched
content, and chokes on template-ish syntax inside the document. Use `-u`:

```sh
fabric -u https://docs.typesafe.ai/primitives/choice.md --dry-run   # 26,796 bytes, no vendor
```

**The working chain** — `jev-verify <claim> <url|path>`, on both machines:

| step | mechanism | vendor |
|---|---|---|
| fetch | `fabric -u <url> --dry-run`, curl fallback | none |
| judge | `jev-axi ask` — supported / contradicted / absent | none (Jev cannot generate text) |

Measured on the error that motivated it — *"Choice questions accept at most 255 options"*:

| source | supported | absent | verdict |
|---|---|---|---|
| `/primitives/choice.md` (real) | **0.96** | 0.02 | supported |
| `/primitives/score.md` (the page I wrongly cited) | 0.03 | **0.95** | NOT IN THIS SOURCE |

**A fetch is now validated before it is judged.** An earlier version accepted 274 bytes of
dry-run boilerplate as if it were the document and reported a confident "NOT IN THIS SOURCE"
about a 26kB page it had never read — a false negative from a phantom fetch, which is worse
than no answer. It now refuses to judge anything under 400 bytes or containing `{{plugin:`.

Related: [[Jev - Validation Discipline]], [[Jev - Field Findings]], [[00 - Jev Master Index]]
