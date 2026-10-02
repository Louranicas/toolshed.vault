---
tags: [toolshed, prompting, astra, software-engineering, rust]
created: 2026-09-08
updated: 2026-09-08
status: authored
---

# ASTRA Coding Prompts

Select one task card, replace its bracketed fields, and attach the evidence needed for that task.

Parent: [[herdr-habitat-prompt-library|Herdr Habitat Prompt Library]]  
Related: [[70 Toolkit/ASTRA Prompting Guide]] · [[70 Toolkit/ASTRA Quality Review]]

These are locally authored templates, not measured performance claims. Cards specify their operating scope. Add C07 for Rust work or C08 when testing is the task; do not stack every card.

| Card | Use when | Scope |
|---|---|---|
| [[#C01 - Implement a feature\|C01]] | The desired behaviour is known | Implement |
| [[#C02 - Fix a defect\|C02]] | There is a failure or regression | Diagnose and fix |
| [[#C03 - Refactor a boundary\|C03]] | Structure obstructs a current change | Preserve behaviour while refactoring |
| [[#C04 - Decide an architecture\|C04]] | Ownership or design is unresolved | Design only |
| [[#C05 - Review a change\|C05]] | A candidate needs scrutiny | Read-only review |
| [[#C06 - Remove structural slop\|C06]] | A working implementation has needless machinery | Scoped simplification |
| [[#C07 - Add Rust criteria\|C07]] | The task touches Rust | Add to another task |
| [[#C08 - Prove a contract\|C08]] | Tests lack meaningful failure detection | Verification work |
| [[#C09 - Optimise a measured cost\|C09]] | A workload misses a resource target | Measure and optimise |
| [[#C10 - Resume an engineering task\|C10]] | There is a saved handoff | Resume existing scope |
| [[#C11 - Write a change report\|C11]] | Work needs a maintainer-facing account | Report only |

## C01 - Implement a feature

```text
Implement [behaviour] in [repository/worktree]. The consumer is [caller/user].
Acceptance: [ordinary case], [boundary case], [failure observation].
Preserve [invariants and compatibility]. Scope: [component and allowed effects].

Inspect the existing entry point, data flow and repository instructions.
Keep decisions separate from external effects where this clarifies ownership
or enables meaningful tests. Prefer the existing mechanism when it meets the
contract. Make errors, state transitions and resource limits explicit.

Deliver the complete scoped change, consumer-facing verification and required
repository checks. Inspect the diff for unused API, duplicated state, invented
configuration and unrelated edits. Report actual behaviour and evidence.
```

## C02 - Fix a defect

```text
Fix [observed failure] in [repository/worktree].
Reproducer: [input/steps]. Expected: [contract]. Evidence: [logs/source].
Scope and constraints: [boundaries].

Trace the cause through the public entry point to the owning component.
Separate observed facts from hypotheses. When reproducible, establish a case
that fails on the defect and passes after the fix, with an expectation derived
from the contract. Check a nearby valid case so rejection is not indiscriminate.

Repair the owning cause. Do not disguise it with a catch-all, unconditional
retry, empty value or success result. Preserve error information useful to the
caller. Complete relevant checks and state any reproduction limits honestly.
```

## C03 - Refactor a boundary

```text
Refactor [component] to address [present maintenance or ownership problem].
Behaviour to preserve: [public outputs, errors, ordering, state and compatibility].
Allowed scope: [files/component]. Evidence: [current tests and callers].

Identify characterization coverage for the protected behaviour before moving
code. Make state and effect ownership clearer and dependencies easier to trace.
Keep public interfaces as small as their callers require. Preserve necessary
extension and testing seams; avoid exposing implementation details for tests.

Validate the same consumer contract before and after. Review changes to error
propagation, defaults, ordering and persisted data explicitly. Explain the
concrete reduction in coupling or maintenance cost, plus remaining tradeoffs.
```

## C04 - Decide an architecture

```text
Design only: resolve [design question] for [component].
Requirements: [behaviours and invariants]. Constraints: [compatibility/resources].
Current evidence: [source paths, callers, workload].

Compare the existing mechanism, the simplest complete alternative, and a more
general design only if a current requirement justifies it. For each viable
option identify state ownership, external effects, failure/recovery behaviour,
public surface, dependencies and testability. Use a small data-flow sketch if
it makes an ownership boundary easier to inspect.

Recommend an option with a concrete tradeoff and a condition that would make
you reconsider. List only the unresolved decisions that affect implementation.
Keep the result a design; implementing it is a separate task.
```

## C05 - Review a change

```text
Review [diff/commit/worktree] against [requirements and compatibility contract].
This is read-only review. Inspect the callers and relevant surrounding code.

Look for incorrect behaviour, weak ownership, failure information loss,
unbounded resources, schema drift, unnecessary public surface, and tests whose
expectations share the implementation's faulty premise. Follow each suspected
issue to a concrete trigger and consequence.

For each material finding give location, triggering input/state, violated
contract, evidence or reproducer, and the smallest sound correction. Rank by
impact. Keep hypotheses distinct from confirmed defects. Do not invent findings
to meet a quota. If none are found, describe coverage and residual uncertainty.
```

## C06 - Remove structural slop

```text
Simplify [component/diff] within [scope], preserving [observable contract].

Find redundant wrappers, duplicated validation/state, unused configuration,
placeholder paths, success-shaped fallbacks, and comments that narrate syntax.
Treat each as a review candidate, not automatic grounds for deletion. Check
callers, compatibility, error behaviour and test seams before removing it.

Prefer a direct implementation whose ownership and failure cases remain clear.
Justify each retained abstraction by a current invariant or consumer. Verify
the preserved contract; fewer lines alone do not establish improvement.
```

## C07 - Add Rust criteria

```text
Apply these Rust criteria to the current task using this repository's toolchain,
MSRV, lint policy and established check commands.

Represent meaningful domain distinctions with types when doing so prevents a
real invalid state. Keep constructors and mutation at the owning boundary.
Choose borrowing, moves and cloning deliberately. Give each allocation, shared
owner, lock and task a reason tied to lifetime, access or measured workload.

Keep fallible external input and I/O on explicit error paths. Preserve useful
error context and distinguish absence from failure. Keep public items narrow.
Document invariants and non-obvious decisions rather than narrating syntax.

For async or shared-state code, inspect cancellation, ordering, bounded queues,
shutdown and lock lifetimes. Follow the project's safety restrictions. Use
specialised optimisation or verification tools only for a relevant measured
need or required invariant, and report what their result actually covers.
```

## C08 - Prove a contract

```text
Verify [changed contract] in [repository/worktree].
Requirement and consumer: [source]. Risk: [specific failure family].
Allowed test and fixture changes: [scope].

Choose an oracle independent of the implementation: a known answer, public
specification, external readback, or a justified property. Identify a plausible
wrong implementation that the test must reject. Exercise the public behaviour,
including one lawful case and the important failure/boundary case.

For a gate, verify that the faulty case fails for the intended reason, not
because setup broke; verify the lawful control still passes. For persistent or
concurrent effects, include the required interruption/recovery or ordering
checks. Record commands, subject, environment, counts and omissions. Complete
required checks; add further cases only for an unresolved risk.
```

## C09 - Optimise a measured cost

```text
Improve [latency/throughput/memory cost] for [representative workload] in [scope].
Target: [measurement and resource budget]. Preserve: [semantics and invariants].

Establish a reproducible baseline, profile the dominant cost, and select a
change supported by that evidence. Compare under the same inputs, build mode
and environment; repeat enough to expose variation. Retain correctness and
failure/recovery checks. Account for new cache, allocation, synchronisation,
dependency and maintenance costs.

Report measured results with limitations. If the candidate brings no reliable
benefit, leave the simpler implementation and record what was learned.
```

## C10 - Resume an engineering task

```text
Resume from [handoff path] within its still-applicable user-authorised scope.
Current correction or priority: [delta, or none].

Recover the objective, accepted decisions, applicable instructions, plan task
and dependencies. Check current worktree state and the source underlying the
next action; treat old receipts as evidence for their original subjects.
Reconcile stale progress claims before relying on them. Preserve other work.

Continue the next unblocked authorised slice through verification and update
the maintained progress record with actual results and remaining gaps. If the
saved scope is planning or review, preserve that mode.
```

## C11 - Write a change report

```text
Write a maintainer-facing report from [diff and verification evidence].
Describe the concrete problem and resulting behaviour, then explain the design
choice that a reviewer needs to assess. Include completed checks and material
limits. Keep planned, attempted and verified work distinct.

Use precise names and ordinary sentences. Remove promotional claims, generic
conclusions and repeated context. Do not call a result secure, exhaustive,
production-ready or faster without evidence for that property. Keep the length
proportional to the change; include a before/after example if it clarifies it.
```

## Filled example - configuration failure

Illustrative task; adapt paths to an inspected repository before use.

```text
Fix the config loader in the current worktree so malformed JSON is reported to
the caller. Currently the reported behaviour is that malformed input produces
the default config. First verify that report against the implementation.

Acceptance: valid input retains its meaning; malformed existing input returns
an error with useful file context; a read failure remains distinguishable from
a parse failure. Preserve the established policy for a missing optional file.
Reading must not rewrite the configuration. Scope: loader, caller and relevant
tests. Follow applicable repository instructions and existing error types.

Add a regression that would reject returning a default for malformed content,
plus the valid and missing-file controls. Complete required checks and report
the observed result without turning this fix into a configuration framework.
```

Related: [[herdr-habitat-prompt-library]] · [[70 Toolkit/ASTRA Prompting Guide]] · [[70 Toolkit/ASTRA Quality Review]] · [[70 Toolkit/ASTRA Evidence and Sources|Evidence-aware prompting and source ledger]]
