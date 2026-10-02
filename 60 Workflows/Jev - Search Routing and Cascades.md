---
tags: [jev, typesafe, search, routing, cascade, workflows]
created: 2026-09-18
---

# 🧭 Jev — Search Routing and Cascades

Using Jev to route *our own research* rather than to judge content. Built and measured
2026-09-18. This is the most productive use of Jev found so far, and the discovery in §3 was
not the one the tool was built for.

Sits between [[Jev - Ways of Working]] (how to word a question) and
[[Tool Chaining Patterns]] (what shape a chain takes). The fan-out reasoning is
[[Clustering Shapes]]; the abstention rule is [[Jev - Field Findings|F2]].

## 1 · The Choice form — routes an answerable question

One `Choice` over eight search pathways with a `none` option, plus three meta questions:
is the answer a **measured number** or a definition; how **volatile** is it; would a
secondhand summary be **materially worse** than the primary source.

Recipe: `~/.config/jev-axi/recipes/search-route.yaml` · runner `~/route-search.sh`
**$0.00003 and ~700 ms per routing decision.**

| question | routed to | |
|---|---|---|
| Max options a Choice accepts? | `vendor_docs` 0.84 | ✅ |
| What does RLCD optimise? | `academic` 0.93 | ✅ |
| Anyone in production, what broke? | `web_blog` 0.24, **escalate** | ✅ uncertain *because no answer exists* |
| Weather in Melbourne tomorrow? | **`none` 1.00** | ✅ |

## 2 · The matrix form — scores every pathway independently

Because **output tokens are free**, ask one Noul *per pathway* in a single call instead of
forcing a Choice to crown a winner. Same cost, and you get a ranked **portfolio** plus an
`answerable` gate. Recipe `search-matrix.yaml` · runner `~/matrix.sh` · wide caster `~/wide.sh`.

The two forms answer different questions:

> **Choice routes an answerable question. The matrix decides whether to bother.**

## 3 · The discovery: it is a research-gap detector ⭐⭐

Run wide over twenty questions; the rows where **every pathway scores below 0.5** are the
questions the public corpus cannot answer.

| answerable | pathways | question |
|---:|---|---|
| 0.79 | **none** | What does a Choice do when the right answer is absent? |
| 0.41 | **none** | Benchmarked against a properly fine-tuned DeBERTa? |
| 0.32 | **none** | Does a Platt calibration slope transfer across task families? |

**Those are exactly the three open questions identified independently the same day**, by
reading rather than routing. The first we then answered ourselves by experiment
([[Jev - Field Findings|F2]] — 0.93 and 0.97 confident nonsense). The second nobody has done.
The third is the load-bearing unknown for whether Jev can ever fill the
[[Jev - Applications Here|quality_floor socket]].

> [!warning] It over-declares silence
> It wrongly rejected every pathway for "has anyone measured reranking NDCG against a dedicated
> reranker" and "how do practitioners compose several Nouls" — **both exist and we had already
> read them.** Treat a no-pathway result as a prompt to look harder, never as proof of absence.

## 4 · The cascade — route, then actually dispatch

`~/cascade.sh`. Three stages: Jev routes → **code invokes the real service** → anything
fetched is screened by `jev-axi guard` (exit 3 blocks).

```
### What is the maximum number of options a Jev Choice accepts?
  answerable=0.63   pathway=github_code
  -> service: gh search (auth: yes)
     Anil-matcha/awesome-jev-by-typesafe …
     AbdelStark/awesome-typesafe …
```

It **found two source indexes we did not previously have.** Wiring routing to dispatch rather
than to a report makes the system discover its own sources. This is [[Tool Chaining Patterns|P2]]
(the JSON chain) with a probabilistic selector at the junction, and the guard stage is the
[[Jev - Applications Here|A2]] screening pattern inlined.

Legs wired: `vendor_docs` (curl), `github_code`/`github_issues` (gh, authenticated on ORAC),
`academic` (arxiv — **query construction wrong, returns nothing, needs fixing**),
`youtube` (yt-dlp). Unwired: `x_social`, `web_blog`, `hackernews`.

## 5 · Wording lessons, earned the hard way

- **A bad criterion shows up as a systematic miss, not as noise.** "Why does TypeSafe say
  constrained decoding makes models dumber" routed to `github_issues` and *explicitly rejected*
  `hackernews`, where the founder actually answered it. The fault was my wording —
  "someone explained their reasoning… in a public discussion thread". Sharpened to
  "**a maintainer, founder or engineer explained WHY they made a design decision**", and the
  same question then routed to `hackernews` correctly. One word — *why* — carried it.
- The meta questions earn their place. `measured` cleanly separates "wants evidence someone
  gathered by running something" from "wants a fact or a rationale", and that changes which
  pathway is right more than the topic does.

## Superseded in part

[[Jev and Fabric - Vendor-Free Chains]] adds two things this note lacks: Fabric renders state
with **no model call at all** (so the unwired `web_blog` and `hackernews` legs are now wirable),
and a **state-blind control** which showed that this note's `vendor_docs` criterion barely moves
from its prior — it is a passenger. Re-read that before reusing the search-matrix recipe.

## Related
[[Jev - Ways of Working]] · [[Jev - Field Findings]] · [[Jev - Applications Here]] ·
[[Jev - The Model]] · [[jev-axi]] · [[Tool Chaining Patterns]] · [[Clustering Shapes]] ·
[[Autonomous Triggers]] · [[00 - Jev Master Index]]
