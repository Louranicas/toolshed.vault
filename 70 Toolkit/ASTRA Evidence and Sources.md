---
tags: [toolshed, prompting, astra, evidence, research, code-quality]
created: 2026-09-08
updated: 2026-09-08
status: curated
---

# ASTRA Evidence and Sources

Use evidence appropriate to the claim, and turn useful ideas into checks on the actual work.

Parent: [[herdr-habitat-prompt-library|Herdr Habitat Prompt Library]]  
Related: [[70 Toolkit/ASTRA Prompting Guide]] · [[70 Toolkit/ASTRA Quality Review]] · [[70 Toolkit/ASTRA Coding Prompts]]

## How this library weighs evidence

This is a bounded source review, not a systematic review or meta-analysis. Sources were selected for relevance to ASTRA behaviour, code-review practice, API structure and evaluation. All linked sources below were opened on 2026-09-08. No reviewed study directly evaluates this library or establishes ASTRA's effect on long-term code quality.

The following is this library's working appraisal method. Study design, directness, transparency and limitations matter more than a prestigious title or publication category alone.

| Question | Prefer | What that evidence cannot establish alone |
|---|---|---|
| What does the current model support? | Current primary vendor documentation and observed harness configuration | Independent proof of quality or productivity benefit |
| Does an intervention improve outcomes? | Relevant, critically appraised systematic reviews and replicated controlled studies; then well-designed individual experiments | Transfer to a different model, workload or organisation without checking applicability |
| What happens in everyday engineering? | Transparent field studies, repository data and reproducible local evaluations | Causality when selection, confounding or measurement problems remain |
| How should an interface or review be structured? | Language-project guidance and mature engineering practice, applied to current requirements | A universal optimum or automatic empirical validation |
| What might be worth trying? | Expert accounts, case studies and incident-backed observations | General effectiveness or authority over contrary measurements |

Peer review and evidence design are separate attributes. The two research papers below were inspected as arXiv versions; publication status elsewhere was not established. Official engineering guides, vendor docs, institutional reports and expert essays are grey literature here. They can be the best source for a product contract while remaining insufficient for causal claims about quality.

## Source ledger

### E01 - OpenAI model guidance

[OpenAI: ASTRA prompting guidance](https://developers.openai.com/api/docs/guides/latest-model#prompting-guidance), [ASTRA model specification](https://developers.openai.com/api/docs/models/gpt-6-astra), and [reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices).

**Type:** primary vendor documentation. **Use:** model-specific behaviour and supported settings; directness is high for this purpose. **Limit:** vendor recommendations are starting points, not independent trials of the prompts in this library. The companion prompting guide records the specific supported claims.

### E02 - A controlled Copilot experiment

Peng, Kalliamvakou, Cihon and Demirer (2023), [The Impact of AI on Developer Productivity: Evidence from GitHub Copilot](https://arxiv.org/html/2302.06590v1), sections Study Design, Results and Discussion.

**Type:** primary controlled experiment, arXiv v1. Ninety-five recruited professional programmers were randomised; the task was a JavaScript HTTP server. The reported 55.8% reduction in completion time was conditional on completing the task. The paper explicitly leaves code-quality effects unexamined. Its authors include Microsoft/GitHub affiliations.

**Use:** evidence that assistance can improve completion time in a defined setting. **Limit:** one task, older tools, and no established long-term maintainability outcome. Do not convert the result into an ASTRA speed or quality forecast.

### E03 - Experienced maintainers in mature repositories

Becker, Rush, Barnes and Rein (2025), [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://arxiv.org/html/2507.09089v2), abstract and study-design material.

**Type:** primary randomised field experiment, arXiv v2. Sixteen developers completed 246 tasks in familiar mature projects using early-2025 tools when permitted. The paper reports 19% longer completion time with AI, despite participants' perceived speedup.

**Use:** compare measured completion and review cost with subjective impressions. **Limit:** small developer population, specific tools and workflows, and a historical time window. It does not estimate present ASTRA performance or prove that AI assistance generally slows development.

### E04 - The follow-up's own measurement warning

Becker and colleagues / METR (2026-02-24), [We are Changing our Developer Productivity Experiment Design](https://metr.org/blog/2026-02-24-uplift-update/).

**Type:** primary institutional research update; grey literature. METR judged the follow-up's productivity signal unreliable because of participant/task selection and measurement problems, including concurrent agent work. The authors considered improvement plausible but treated its magnitude as weakly supported.

**Use:** record declined tasks, incomplete attempts and human review time; distinguish elapsed time from active human time. **Limit:** the update cannot supply a dependable current speedup percentage. A newer report is not automatically stronger evidence.

### E05 - Google's code-review practice

[Google Engineering Practices: What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html).

**Type:** primary institutional engineering guidance; grey literature. It examines design, functionality, complexity, tests, naming, comments and documentation, including whether tests reject broken code and whether generality serves a present need.

**Use:** the review dimensions in C05 and the quality worksheet. **Limit:** accumulated practice is not a randomised demonstration that a particular prompt improves code. Translate the principle into the repository's concrete contract.

### E06 - Rust API design guidance

[Rust API Guidelines checklist](https://rust-lang.github.io/api-guidelines/checklist.html), especially C-GOOD-ERR, C-FAILURE, C-NEWTYPE, C-CUSTOM-TYPE and C-STRUCT-PRIVATE.

**Type:** primary language-ecosystem guidance; grey literature. The selected items address meaningful errors, documented failure behaviour, domain distinctions and encapsulation.

**Use:** inspect the public boundaries touched by C07; choose applicable guidance. **Limit:** a library checklist does not imply that every internal helper needs every trait, example, builder or generic abstraction. Repository policy and current callers determine applicability.

### E07 - An expert perspective on generality

John Ousterhout, [author's account of the second edition of A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php), updated 2021-11-16.

**Type:** primary expert narrative. Ousterhout emphasises general-purpose modules and explicitly notes disagreements with Robert Martin about method length and comments. This review read the author's page, not the complete book.

**Use:** challenge rigid rules such as “all functions must be tiny” or “every abstraction is over-engineering.” **Limit:** expertise and a design philosophy are not comparative experimental evidence. Assess whether the proposed interface actually reduces what a caller must know.

## What changes in the prompts

E02 and E03 study different populations, tasks and tools; their estimates should not be pooled casually. E04 further limits claims about current productivity. The local inference is to measure completed behaviour, defects, human rework, elapsed time and maintainability separately. Neither faster typing nor more generated code establishes improvement.

E05's caution about speculative generality and E07's preference for useful general-purpose modules create a productive design question: does this boundary remove complexity from actual callers, or merely relocate and multiply it? The library uses present requirements, ownership and consumer evidence to decide. It adopts no universal function-length or abstraction-count rule.

Use this evidence-aware addition for an uncertain technical recommendation:

```text
For [decision], identify the claim that needs evidence. Prefer primary sources
and studies whose task, model and outcome match it. Record source type, date,
method, relevant limitations and conflicts of interest when reported. Separate
the source's finding from your inference for this repository. Treat expert
accounts as candidate explanations or techniques to test. Propose the smallest
local comparison that could change the decision; avoid an unsupported ranking.
```

For a Rust interface review, add this concrete question: “Which invalid state or caller obligation does this type or abstraction remove, and which new obligations does it introduce?” For prompt evaluation, record active human review/rework time separately from wall-clock time and retain failed or incomplete attempts.

Related: [[herdr-habitat-prompt-library]] · [[70 Toolkit/ASTRA Prompting Guide]] · [[70 Toolkit/ASTRA Quality Review]] · [[70 Toolkit/ASTRA Coding Prompts]]
