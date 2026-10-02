---
tags: [toolshed, prompting, astra, code-quality, testing]
created: 2026-09-08
updated: 2026-09-08
status: authored
---

# ASTRA Quality Review

Assess the delivered behaviour and its evidence before accepting claims of quality.

Parent: [[herdr-habitat-prompt-library|Herdr Habitat Prompt Library]]  
Related: [[70 Toolkit/ASTRA Prompting Guide]] · [[70 Toolkit/ASTRA Coding Prompts]]

This worksheet adapts the existing engineering atlas's SLOP, drift, over-engineering and Rust-excellence guidance. Reach those source guides through the parent library's reciprocal atlas route. Apply project-specific requirements from current source, rather than treating this worksheet as a replacement policy.

## Recognise the failure, then choose the check

| Signal | Why it matters | Useful check |
|---|---|---|
| Default or empty result after unexpected failure | The caller cannot tell success from failure | Trigger the failure and inspect the public result |
| Wrapper, trait or service with no clear responsibility | More surface to maintain without an identified need | Trace callers; compare with a concrete implementation |
| Multiple writable copies of the same state | Readers can disagree about what happened | Identify the owner and exercise an update through every relevant reader |
| Boolean flags or string values encode incompatible states | Invalid combinations remain representable | State the valid transitions; consider a domain type where it removes an actual ambiguity |
| Test computes expected output using the code being tested | Both sides can share the same bug | Derive a known answer or property from the contract |
| Gate's negative case fails during setup | The purported detector was never reached | Verify reachability and the intended rejection reason |
| Retry, queue, task or retained data has no bound | Failure can amplify resource use | Define a limit and exercise exhaustion, cancellation or shutdown |
| “Fully verified” report cites another revision | Evidence does not cover the claim's subject | Compare source identity, configuration and validation scope |
| Comments explain every obvious operation | Noise conceals the few important invariants | Keep rationale, units, compatibility and failure semantics |
| New abstraction justified only by future flexibility | Maintenance cost arrives before a requirement | Identify the present consumer, invariant or test seam |

These signals require judgment. An adapter, clone, trait, retry or long function can be appropriate. A word search, line count, lint score or blanket prohibition cannot establish design quality.

## Review structure at its boundaries

| Dimension | Acceptance question |
|---|---|
| Contract | Can a caller tell successful output, expected absence and failure apart? |
| Ownership | Is there a clear owner for state, mutation, external effects and cleanup? |
| Cohesion | Does each module have a coherent responsibility explained by the domain? |
| Coupling | Can dependencies and data flow be followed without hidden global coordination? |
| Interface | Are public items, configuration and dependencies limited to actual needs? |
| Compatibility | Do current consumers and relevant old persisted/schema forms still behave as required? |
| Resources | Are work, memory, retries and concurrency bounded where the contract requires it? |
| Recovery | Are partial completion, interruption and retry semantics defined where effects persist? |
| Evidence | Could the checks reject a plausible incorrect implementation, for the intended reason? |
| Maintenance | Can another maintainer explain the invariant and change its owner without scattered edits? |

Choose the least complicated design that satisfies the complete contract. Necessary failure handling, recovery and meaningful verification are part of completeness. A single consumer can justify a seam for ownership or testing; imagined future reuse alone is a weak reason.

## Example - a compact failure can still be slop

Illustrative Rust fragment, not a compiled patch or repository prescription:

```rust
let config = serde_json::from_str(&text).unwrap_or_default();
```

If malformed configuration must be reported, this collapses invalid input into a legitimate-looking default. The correction is an error path owned by the loader and surfaced by its caller, using the repository's error conventions. A successful parse test does not detect this defect. A malformed-input regression with an independently specified error expectation does. Also check the legitimate missing-file policy, which may intentionally allow a default.

## Match verification to the consequence

| Change | Useful minimum direction, subject to repository requirements |
|---|---|
| Documentation or prompt text | Read for factual accuracy, scope and contradictions; check links and placeholders |
| Local behaviour fix | Reproducer, important valid/boundary cases, relevant consumer and required checks |
| Public API or schema | Consumer and compatibility cases, error semantics, affected documentation |
| Durable effects or lifecycle | Real writer/readback, partial failure, interruption and recovery as applicable |
| Concurrent state | Ordering, ownership, resource bounds, cancellation and shutdown; specialised tools only when suitable |
| Verification gate | Lawful control and plausible faulty control, correct rejection cause, honest coverage denominator |
| Performance | Equivalent semantics, representative baseline, controlled comparisons and variation |

Do not weaken mandatory checks to fit a smaller test budget. Do not repeat a passing check without a new change or unresolved concern. A blocked check stays blocked in the report; passing static checks do not imply successful runtime behaviour.

## Evaluate the prompts themselves

Current status: authored and reviewed as documentation; comparative ASTRA task evaluation has not been run.

Use the same repository snapshots, fixtures and acceptance criteria for a baseline prompt and a candidate. Keep model, effective reasoning effort, tools and budgets comparable. Separate task attempts so one candidate does not inherit the other's patch. Start with these cases:

| Trial | Discriminating observation |
|---|---|
| Small typo or documentation correction | Finishes correctly without creating irrelevant code tests or expanding scope |
| Malformed configuration with valid controls | Preserves error semantics rather than returning a default |
| Refactor with an existing consumer | Improves ownership while retaining observable compatibility |
| Gate that can reject for the wrong reason | Establishes intended detector reachability and preserves lawful acceptance |
| Change report with an unrun check | Keeps the unverified property explicit and avoids a blanket completion claim |

Record failures and abandoned attempts as well as successful outcomes. Multiple runs help expose variation. Where practical, have a reviewer assess anonymised diffs before seeing which prompt produced them. An additional model opinion is not automatically an independent oracle.

```text
Task and repository revision:
Prompt version; exact task inputs:
Model; effective effort; harness/tool versions:
Required behaviour and independently derived oracle:
Outcome: satisfied / failed / unverified, with evidence:
Material defects and required rework:
Public API, dependency and configuration changes with justification:
Checks completed; omissions and why:
Elapsed time; active human review/rework time; available token/resource measurements:
Writing problems that obscured a decision or evidence limit:
Adopt / revise / reject, with the decisive observation:
```

Do not average a failed correctness or permission requirement into a passing quality score. Prefer the prompt that consistently meets the contract with fewer defects and reasonable maintenance cost; verbosity and test counts alone are weak proxies.

## Compact completion check

- The delivered behaviour matches a named requirement and current scope.
- State and effects have clear owners; every added surface has a present reason.
- Relevant failure, compatibility and resource constraints remain intact.
- Verification observes the contract and can distinguish a plausible wrong result.
- The final diff and explanation are free of redundant machinery and unsupported claims.
- Evidence identifies its actual subject; open risks and unrun checks remain visible.

Related: [[herdr-habitat-prompt-library]] · [[70 Toolkit/ASTRA Prompting Guide]] · [[70 Toolkit/ASTRA Coding Prompts]] · [[70 Toolkit/ASTRA Evidence and Sources|Research, grey literature and expert-source appraisal]]
