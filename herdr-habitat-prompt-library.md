---
aliases: [Herdr Habitat Prompt Library, ASTRA Prompt Library]
tags: [toolshed, prompting, astra, code-quality, moc]
created: 2026-09-08
updated: 2026-09-08
source: https://developers.openai.com/api/docs/guides/latest-model#prompting-guidance
status: authored
---

# Herdr Habitat Prompt Library

Reusable ASTRA prompts for code that is correct, clear, economical to maintain, and supported by evidence.

Parent: [[00 - Toolshed Index]]  
Related: [[70 Toolkit/ASTRA Prompting Guide|Prompting guide]] · [[70 Toolkit/ASTRA Coding Prompts|Coding prompts]] · [[70 Toolkit/ASTRA Quality Review|Quality review]]

## Start with one task

Use the starter below for ordinary implementation. For a narrower job, use one card from the coding prompts. Add the Rust or review criteria only when relevant. Reading a library note does not install instructions or change the selected model.

```text
Implement [observable outcome] in [repository or worktree].

Acceptance: [input or trigger → expected result], [important failure case].
Preserve: [public behaviour, compatibility, resource or safety constraints].
Scope: [allowed files or component and authorised effects].
Evidence: [reproducer, specification, relevant note or source paths].

Read the applicable repository instructions and trace the existing consumer
and implementation before editing. Reuse the established design where it
fits. Give each piece of state and each external effect a clear owner. Add
abstractions only for a present requirement, invariant, or useful test seam.

Handle real failures explicitly. Keep the public API small and names precise.
Test the observable contract with expectations derived independently of the
new implementation. Complete the repository's required checks and inspect
the final diff for accidental scope changes and redundant scaffolding.

Finish the authorised work. Use existing context to settle routine details;
surface missing information when it changes the contract or permitted action.
Report the behaviour delivered, checks actually completed, and remaining gaps.
Write plainly; replace claims of quality with the evidence supporting them.
```

Replace every bracketed field. For example, `Acceptance: a malformed config returns a parse error; the caller's existing config file is unchanged` gives a reviewer something to verify. `Make it world class` does not.

## Choose a route

| Need | Open |
|---|---|
| Understand ASTRA, instruction placement, autonomy and effort | [[70 Toolkit/ASTRA Prompting Guide]] |
| Implement, debug, refactor, design or review | [[70 Toolkit/ASTRA Coding Prompts]] |
| Recognise SLOP and assess code structure and evidence | [[70 Toolkit/ASTRA Quality Review]] |
| Weigh research, grey literature and expert claims | [[70 Toolkit/ASTRA Evidence and Sources]] |
| Reconcile available skills and their scope | [[70 Toolkit/skills\|Skills router]] |
| Place the task in the existing build and review cycle | [[60 Workflows/00 - Workflows\|Workflows index]] |

## What SLOP means here

SLOP is work whose apparent completeness exceeds its substance: a success-shaped fallback, a decorative abstraction, a test that repeats the implementation's mistake, or a report that calls an unmeasured property proven. Fluent prose and short code can both contain it. Review observable behaviour, structure, failure handling and claim accuracy.

The library translates the habitat's existing engineering standards into task prompts. The ambition is the highest defensible quality for the requirement and constraints; no prompt establishes an objective best implementation or guarantees correctness.

## Master indexes and reciprocal routes

Each destination below contains a direct return link to this note. Toolshed owns the library; the other indexes explain where to apply it.

| Index | Relationship |
|---|---|
| [[00 - Toolshed Index\|Toolshed]] | Prompt library and command/workflow reference |
| [Herdr Habitat](obsidian://open?vault=herdr-fedora-habitat.vault&file=00%20-%20Fedora%20Master%20Index) | Engineering contracts, planning and habitat integration |
| [Fedora Kinoite](obsidian://open?vault=fedora-kinoite.vault&file=00%20-%20Fedora%20Master%20Index) | Explicit host, Toolbx and container boundaries |
| [Fedora Fabric](obsidian://open?vault=fedora-fabric.vault&file=00%20Home%2FFedora%20Fabric%20Home) | Reusable pattern authoring and evaluation |
| [Diary master index](obsidian://open?vault=my-diary.vault&file=00%20-%20Master%20Index) | Incident-backed judgment; reference prompts remain here |
| [Orchestration](obsidian://open?vault=herdr-habitat-orchistration.vault&file=00%20-%20Master%20Index) | Explicit task ownership and bounded handoffs |
| [Herdr source grand index](obsidian://open?vault=herdr.vault&file=00%20-%20Grand%20Master%20Cross-Vault%20Index) | Source-architecture and repository navigation |
| [Outer Grand Master Index](</var/mnt/STORAGE-10TB/repos/GRAND_MASTER_INDEX.md>) | Entry from the repository-wide knowledge map |

Topic bridges: [Engineering atlas](obsidian://open?vault=herdr-fedora-habitat.vault&file=95%20Genesis%2Fengineering-atlas%2FSTART_HERE) · [Fabric pattern authoring](obsidian://open?vault=fedora-fabric.vault&file=03%20Patterns%2FPattern%20Anatomy%20and%20Authoring). Both link back here. The atlas routes to its quality-controls and Rust-excellence guides; their project-specific requirements retain their original scope.

## Provenance and maintenance

Authored 2026-09-08 for GPT-6 Astra from the user's [official OpenAI guide](https://developers.openai.com/api/docs/guides/latest-model#prompting-guidance), verified model documentation, and the local conventions recorded in the companion guide. Prompts and examples are locally authored starting points. They have not undergone comparative ASTRA evaluation; note/link validation is a separate check.

Version the prompt when changing its intended behaviour. Keep a previous successful task and a difficult failure case, then compare actual results using the quality-review worksheet. Recheck the official model-specific guidance when the model or harness changes; the `latest-model` page can change its default model.

Related: [[70 Toolkit/ASTRA Prompting Guide]] · [[70 Toolkit/ASTRA Coding Prompts]] · [[70 Toolkit/ASTRA Quality Review]] · [[70 Toolkit/ASTRA Evidence and Sources]] · [[70 Toolkit/skills]] · [[60 Workflows/00 - Workflows]] · [[00 - Toolshed Index]]
