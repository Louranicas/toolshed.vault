---
aliases:
  - Fabric Habitat Assessment
  - Seven-Facet Fabric Command Plane Assessment
tags: [toolshed, assessment, fabric, habitat, w1-w5, safety, integration]
created: 2026-09-04
status: assessed — first recommendation tranche integrated
baseline_mark: 79
---

# Fabric Habitat — Seven-Facet Assessment

Parent: [[00 - Toolshed Index]]  
Related: [[Fabric Bash Command Plane]] · [[Fabric Habitat 90-Point Promotion and Practice]] · [[Axiom Conformance]] · [[Weight Matrix - Which Gate Bore the Weight]] · [[Claim-Time Guard]]

Cross-vault: [Fabric pattern contract](obsidian://open?vault=fedora-fabric.vault&file=04%20Workflows%2FHabitat%20Bash%20Command%20Contract) ⇄ [Habitat placement](obsidian://open?vault=herdr-fedora-habitat.vault&file=70%20Toolchain%2FFabric%20Bash%20Command%20Plane)  
Executable evidence: [Arena runbook](file:///var/home/Louranicas/fedora-arena/runbooks/Fabric%20Habitat%20W1-W5%20Lab.md) · [post-integration receipt](file:///var/home/Louranicas/fedora-arena/receipts/fabric-habitat-lab-20260904T132203Z-2292056/verdict.json)

## Verdict

**Baseline mark: 79/100 — exceptional systems prototype; not yet a production command plane.**

The system's design quality is near 90: it turns natural-language intent into typed proposals, routes work by W1–W5 responsibility, separates authority across five vaults, and records deterministic receipts. The overall mark stays below 80 because the first general validator trusted interpreter source carried inside a typed `argv`, and because the successful experiment remains a fixed read-only slice rather than a model-driven or mutating end-to-end path.

## Weighted facets

| Facet | Weight | Mark | Contribution | Assessment |
|---|---:|---:|---:|---|
| Strategic originality | 12% | 94 | 11.28 | Natural language → typed plan → workspace routing → receipts → durable knowledge is a high-leverage synthesis. |
| Architectural coherence | 15% | 91 | 13.65 | Fabric, Toolshed, Habitat, Kinoite and Diary have explicit, complementary ownership. |
| W1–W5 interoperability | 17% | 84 | 14.28 | Sixteen live services, five parallel lanes and one W5 → W1 → W5 return are demonstrated; W2–W4 are not yet full value exchanges. |
| Safety and governance | 20% | 68 | 13.60 | The fixed harness is safe, but the first validator accepted a mutating Nushell payload labelled read-only. |
| Evidence and observability | 14% | 82 | 11.48 | Receipts preserve argv, output, error, timing and verdict; the original pane predicate proved only non-empty output. |
| Knowledge topology | 10% | 78 | 7.80 | Authority and backlinks are strong; older indexes and recall configuration had drifted from the five-vault registry. |
| Operational maturity | 12% | 55 | 6.60 | No model provider, no generated-plan trial, no typed runbook executor, raw `bash -lc` seams and intermittent storage stalls remain. |

`94×0.12 + 91×0.15 + 84×0.17 + 68×0.20 + 82×0.14 + 78×0.10 + 55×0.12 = 78.69`, rounded to **79**.

## The finding that bears the most weight

The plan envelope used an `argv` array and banned a top-level `command` field. That protected the shell boundary but not the interpreter boundary: a Nushell query is source code even when it is one string inside an array. A data-only adversarial probe replaced the approved W1 query with `rm --recursive /var/home/Louranicas/fedora-arena`; the first validator returned `true`. The payload was never executed.

This is the important general law:

> Typed transport does not make an embedded language safe. Admission belongs to the capability's semantics, not merely to the outer JSON shape.

## Recommendation assimilation register

| ID | Recommendation | Disposition | Integrated evidence / remaining gate |
|---|---|---|---|
| SF-1 | Replace general interpreter payload admission with capability-specific schemas or AST allowlists | **Integrated for v1** | The bounded validator now accepts only five exact `argv` contracts. The same mutating Nushell specimen returns non-zero. General dynamic planning still needs capability-specific compilers. |
| SF-2 | Replace non-empty pane checks with service-specific predicates | **Integrated for v1** | Bacon must expose watcher/pager evidence, Lazygit review vocabulary, and Bottom process/resource evidence. All three passed after the change. |
| SF-3 | Exercise an actual model-produced non-mutating plan against an adversarial corpus | **Partially integrated** | The 33-case invocation corpus matches 100%, all ten policy mutants are killed, and 120 dry-run cycles passed. No provider was invented, so the model-produced half remains HOLD. |
| SF-4 | Unify five-vault lookup and correct identity drift | **Partially integrated** | `services.json` now carries all five registered paths and `habitat vault` describes that boundary. Obsidian remains identity authority. Family-wide scans can still stall behind the mounted journal. |
| SF-5 | Version, install and promote the control surface through typed runbook and review stages | **Staged** | Arena Bash, Just, pattern, validator and receipts exist. They remain untracked; no commit, PATH installation, typed Fabric runbook step, W3 approval flow or cold W4 rehearsal is claimed. |

## Post-integration controls

The post-integration lab requires all of these to pass:

1. exactly five workspace/service contracts;
2. W1 workspace-count semantics;
3. service-specific evidence from W2/Bacon, W3/Lazygit and W4/Bottom;
4. W5 JSON semantics;
5. W5 → W1 → W5 count `5`;
6. five-vault registry alignment;
7. rejection of a shell-string field;
8. rejection of a mutating Nushell payload;
9. rejection of an unknown service;
10. rejection of an unbounded pane read;
11. Fabric dry-run with no model call or generated-shell execution.

The receipt at the top of this note records PASS for the bounded suite. This closes the specific defects found by the assessment; it does not retroactively raise the baseline mark or activate the wider command plane.

## Sixty-minute promotion evidence — 2026-09-05

[[Fabric Habitat 90-Point Promotion and Practice]] completed 3,600 measured seconds with 120/120 passing cycles, 600 lane attempts and 2,400 checks. An independent auditor reopened all 120 receipts, found zero inconsistencies and bound them into one evidence manifest. This strengthens the safety, observability, knowledge and operational facets, but the 79 baseline remains the last full assessment until model, W3 human-review and W4 cold-rehearsal evidence exists.

## Next promotion gate

The next meaningful experiment is not broader shell access. It is one model-produced, read-only plan compiled through a capability-specific adapter, rejected by a multi-case adversarial corpus when malformed, routed through W3 as a visible artifact, and independently verified from its receipt. Until that path exists, Fabric remains a proposal surface and the fixed Bash harness remains the only executor.
