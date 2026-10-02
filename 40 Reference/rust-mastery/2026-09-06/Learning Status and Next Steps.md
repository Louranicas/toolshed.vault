---
title: Rust mastery — learning status and next steps
tags: [rust, toolshed, learning, status]
created: 2026-09-06
updated: 2026-09-06
---

# Rust mastery — learning status and next steps

**Parent:** [[40 Reference/rust-mastery/README|Rust corpus index]]. **Related:** [[40 Reference/rust-mastery/2026-09-06/Source and Reading Map|Source and Reading Map]] · [[40 Reference/Perfecting Rust - Performance Engineering#Practice until the reasoning is reproducible|Practice program]] · [[40 Reference/rust-mastery/2026-09-06/README|Lab evidence]] · [[00 - Toolshed Index#Rust mastery|Toolshed master index]].

This status records the evidence available from the 2026-09-06 study. The documentation and navigation are complete for that study; the longer practice program remains open. It makes no claim about a reader’s proficiency.

## Completed and evidenced

| Work | Evidence | Limit |
|---|---|---|
| Performance Book synthesis | [Pinned source ledger](sources.json); 19 chapters and three historical diffs | Other linked projects were not exhaustively reviewed |
| Local reading routes | [Selected-file inventory](local-library.json); 14 inspected files | Most chapters remain to be read; two copies are partial early releases |
| Selected deeper local reading | Effective Rust Items 20 and 32, developed in the main note | Does not establish full-book completion |
| Semantic checks | [Test log](evidence/semantic-tests.log); four tests including line-boundary, encoding and error cases | Educational fixture coverage, not a complete correctness proof |
| Benchmark wiring | [Criterion smoke log](evidence/criterion-smoke.log); eight cases | Smoke execution collected no timing statistics |
| Heap allocation experiment | [Verification receipt](evidence/verification.json); four separate process profiles | Counts include argument, input and output work within the profiler lifetime |

Read the interpretation in [[40 Reference/rust-mastery/2026-09-06/README#Results to inspect|the lab results]] and the rationale in [[40 Reference/Perfecting Rust - Performance Engineering#A verified allocation laboratory|the allocation laboratory]].

## Partial books and available alternatives

- [Rust for Rustaceans, local Early Access PDF](</var/mnt/STORAGE-10TB/Book Library/Jon Gjengset - Rust For Rustaceans_ Idiomatic Programming for Experienced Developers (2021, No Starch Press) - libgen.li.pdf>) includes chapters 2–9 according to its colored contents page. For the missing concurrency and unsafe material, use the relevant routes in [Programming Rust, 2nd edition](</var/mnt/STORAGE-10TB/Book Library/Jim Blandy_ Jason Orendorff_ Leonora F.S. Tindall - Programming Rust, 2nd Edition (2021, O'Reilly Media, Inc.) - libgen.li.epub>), [Rust Atomics and Locks](</var/mnt/STORAGE-10TB/Book Library/Mara Bos - Rust Atomics and Locks (2023, O'Reilly Media) - libgen.li.pdf>) and the references in [[40 Reference/Perfecting Rust - Performance Engineering#The wider Rust library|the wider library]].
- [Programming Rust, the 2025-named EPUB](</var/mnt/STORAGE-10TB/Book Library/Jim Blandy, Jason Orendorff, and Leonora F. S. Tindall - Programming Rust (2025, O'Reilly Media, Inc.) - libgen.li.epub>) is a five-chapter third-edition early release. [The local 2021 second edition](</var/mnt/STORAGE-10TB/Book Library/Jim Blandy_ Jason Orendorff_ Leonora F.S. Tindall - Programming Rust, 2nd Edition (2021, O'Reilly Media, Inc.) - libgen.li.epub>) has the 23-chapter contents used for the wider study route.
- The 2022 Command-Line Rust copy and older Rust Programming Language copy retain their edition-specific APIs and chapter numbering. Follow [[40 Reference/Perfecting Rust - Performance Engineering#Edition checks that change the route|the edition checks]] before matching code examples to online material.

A missing chapter cannot be completed by relabeling the file. The alternatives above are reading routes; they have not all been read or executed in this study.

## Next practice work

Each item has a concrete completion criterion. Leave it open until its evidence exists.

- [ ] **Collect ordinary Criterion timing results.** Run the documented benchmark in a fresh working copy with the heap feature disabled; save raw samples, environment and timing boundaries. A smoke run does not close this item.
- [ ] **Broaden the allocation workloads.** Vary duplicate rate and record length separately, including a long record followed by short records; retain complete-result comparisons and heap reports.
- [ ] **Test a representation change.** Choose an actual hot type and compare layout, footprint and elapsed cost for the relevant workload.
- [ ] **Collect a CPU profile.** Select a representative optimized workload, establish usable stacks, and retain the before/after profile plus the predicted metric.
- [ ] **Study bounded concurrency.** Record throughput, latency, errors and retained memory across a concurrency sweep.
- [ ] **Rehearse build and delivery behavior.** Collect build timing and test/shutdown/recovery evidence for the chosen project.
- [ ] **Complete selected book chapters.** Record the exact edition, chapter, explanation and a small demonstrated application using the source map.
- [ ] **Reproduce independently.** Repeat a retained result after a toolchain or relevant machine change and state which conclusions transfer.

Use [[40 Reference/rust-mastery/2026-09-06/Source and Reading Map|the reading map]] to select material and [[40 Reference/rust-mastery/2026-09-06/README#Reproduce in a working copy|the reproduction guide]] for the existing lab. The session sequence and reusable experiment template remain in [[40 Reference/Perfecting Rust - Performance Engineering#Practice until the reasoning is reproducible|the main practice program]].

## Update this record

When an item is completed, add the date, subject revision, exact input and environment, observed result, and a link to its receipt. Store new measurements separately from the original run. Link a new note from [[40 Reference/rust-mastery/README|the folder index]] and add the return link. Keep [[#Completed and evidenced|completed evidence]] distinct from [[#Next practice work|open practice work]].
