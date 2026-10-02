---
tags: [jev, typesafe, moc, index]
created: 2026-09-18
---

# 🎲 Jev — TypeSafe's System One model

> Dedicated vault as of 2026-09-20: [jev.vault master index](obsidian://open?vault=jev.vault&file=00%20-%20Jev%20Master%20Index). Fleet findings, skills, recipes, and agent surface live there. These Toolshed notes remain the 2026-09-18 measured corpus.

A model that **cannot write text**. Give it unstructured content and a typed question; it
returns a probability distribution. No replies, no code, no explanation of its reasoning.
That constraint *is* the product.

## The notes

- [[Jev - The Model]] — what it is, the economics, the three primitives, the wire contract
- [[Jev - Field Findings]] ⭐ — **eight things verified against the live API here**, including
  the undocumented confidence formula and the confidently-wrong Choice
- [[Jev - Ways of Working]] ⭐ — the fourteen structural moves, the sixteen anti-patterns,
  and the task-shape → pattern decision guide
- [[Jev - Applications Here]] ⭐ — what it's for *in this habitat*, mapped onto
  `[[Tool Chaining Patterns|P1–P9]]`, `[[Clustering Shapes]]` and `[[Autonomous Triggers]]`
- [[Jev - Search Routing and Cascades]] ⭐ — using Jev to route *our own research*; the
  matrix form turns out to be a **research-gap detector**
- [[Jev and Fabric - Vendor-Free Chains]] ⭐ — Fabric composes state with no LLM at all;
- [[Jev - Error Reduction Loop]] ⭐ — Stop hook + jev-verify; every session error had one shape:
  a checkable fact asserted without checking. Threshold 0.70 measured over 121 real sentences.
  and the **state-blind control** that found a dead criterion in my own router
- [[jev-axi]] — the CLI: twenty verbs, TOON output, confidence bands, local cost ledger
- [[Jev - Validation Discipline]] — the seven-stage procedure for putting a cheap classifier
  behind an expensive one. **Model-agnostic; survives Jev disappearing tomorrow**

## The three things to remember

1. **A Choice always picks a winner.** Probabilities sum to 1, so *something* wins even when
   nothing fits. Verified here: asked which of three absent topics a refund policy covered, it
   answered one at **p=0.93, confidence 0.89**. Always pair a ranking question with an
   absolute existence Noul. See [[Jev - Field Findings|F2]].
2. **Confidence is not comparable across questions.** It is `(p_max − 1/n)/(1 − 1/n)`, so option
   count inflates it mechanically. Threshold on `probabilities`. See [[Jev - Field Findings|F1]].
3. **Cheaper and faster, not smarter.** Their own framing. An ordinary LLM asked the same
   decomposed questions matched Jev's accuracy twice, at ~27x the cost. Buy the price and the
   latency; do not buy judgment.

## Provenance

Built 2026-09-18 from four parallel research passes — the full `docs.typesafe.ai` corpus
(every non-cookbook page), all 18 cookbooks and 4 pattern pages, the `jev-axi` skill corpus and
benchmarks, and both SDKs' source — then **every load-bearing claim tested against the live API**
from this machine. Where a documented claim failed to reproduce, [[Jev - Field Findings]] says so.

> [!note] Epistemic health warning
> Almost every number in the community `adopting-jev` corpus is a *citation*, not a measurement
> that repo made. It is honest about this; downstream readers usually aren't. Numbers in
> [[Jev - Field Findings]] were measured here and are marked as such.

**Turso (2026-09-22).** Turso retrieves; Jev judges the snippet; code writes the typed answer. [Jev in Turso Workflows](obsidian://open?vault=turso.vault&file=20%20Build%20Guides%2FJev%20in%20Turso%20Workflows) ⇄ [Jev: Turso](obsidian://open?vault=jev.vault&file=70%20Workflows%2FTurso).

**Database schematic (2026-09-22).** [Architectural schematic](obsidian://open?vault=turso.vault&file=50%20Agent%20Knowledge%20System%2FSchema%20Sketch#Architectural%20schematic) ⇄ this index. Private read-only socket and API. Not the engine control socket. Cloud MCP and MCPv2 are not connected.

**Ten levels inside the agent (2026-09-29).** IndyDevDan's "10 Levels of Jev" (video + `disler/ten-levels-of-jev`) captured, code-read and measured in jev.vault. Levels 8–10 route a file, a glob or a command's output to Jev and never into the agent's context; `jev-axi` here already covers 8–9 as a CLI. [IndyDevDan source note](obsidian://open?vault=jev.vault&file=95%20Ecosystem%2FIndyDevDan%20-%2010%20Levels%20of%20Jev) · [Levels 8–10 engineering](obsidian://open?vault=jev.vault&file=70%20Workflows%2FLevels%208-10%20-%20Jev%20Inside%20the%20Agent) · [Harness ecosystem survey](obsidian://open?vault=jev.vault&file=95%20Ecosystem%2FAgent%20Harness%20Ecosystem%20Survey%202026-09-29) · [Novel agentic use cases](obsidian://open?vault=jev.vault&file=50%20Agents%2FNovel%20Agentic%20Use%20Cases%202026-09-29) · [Read-gate measurement](obsidian://open?vault=jev.vault&file=20%20Findings%2FRead%20Gate%20Measurement%202026-09-29) ⇄ this index. Fabric `-y --transcript` hung on this video; `yt-dlp` auto-subs worked.

Related: [[00 - Toolshed Index]] · [jev.vault master index](obsidian://open?vault=jev.vault&file=00%20-%20Jev%20Master%20Index) · [Firstmate and Jev on Kinoite](obsidian://open?vault=herdr-fedora-habitat.vault&file=10%20Setup%2FFirstmate%20and%20Jev%20on%20Kinoite) · [Jev in Turso Workflows](obsidian://open?vault=turso.vault&file=20%20Build%20Guides%2FJev%20in%20Turso%20Workflows)
