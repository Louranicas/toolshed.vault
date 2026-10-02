---
title: Rust mastery — source and reading map
tags: [rust, toolshed, reference]
created: 2026-09-06
updated: 2026-09-06
---

# Rust mastery — source and reading map

**Parent:** [[40 Reference/rust-mastery/README|Rust corpus index]]. **Related:** [[40 Reference/Perfecting Rust - Performance Engineering|Deep learning note]] · [[40 Reference/rust-mastery/2026-09-06/README|Evidence and reproduction]] · [[40 Reference/rust-mastery/2026-09-06/Learning Status and Next Steps|Learning status]] · [[00 - Toolshed Index#Rust mastery|Toolshed master index]].

This readable map accompanies [sources.json](sources.json) and [local-library.json](local-library.json). It organizes the recorded research; it does not mark an entire book as read merely because its contents were inspected.

## Performance Book routes

All 19 chapters below were reviewed at commit `a05dd0f15595e98aef45e5a15072c2a71dbe37ba` (2026-04-23). The source ledger retains chapter hashes. Use [[40 Reference/Perfecting Rust - Performance Engineering#The whole Performance Book as a decision map|the decision map]] for the learning and tradeoff associated with each chapter.

| Reading route | Chapters | Apply it in the learning note |
|---|---|---|
| Frame the problem | [Introduction](https://nnethercote.github.io/perf-book/introduction.html) · [General Tips](https://nnethercote.github.io/perf-book/general-tips.html) | [[40 Reference/Perfecting Rust - Performance Engineering#The engineering loop\|The engineering loop]] |
| Measure and attribute | [Benchmarking](https://nnethercote.github.io/perf-book/benchmarking.html) · [Profiling](https://nnethercote.github.io/perf-book/profiling.html) | [[40 Reference/Perfecting Rust - Performance Engineering#Benchmark the question you actually care about\|Benchmark the question you actually care about]] |
| Own and represent data | [Heap Allocations](https://nnethercote.github.io/perf-book/heap-allocations.html) · [Type Sizes](https://nnethercote.github.io/perf-book/type-sizes.html) · [Standard Library Types](https://nnethercote.github.io/perf-book/standard-library-types.html) · [Hashing](https://nnethercote.github.io/perf-book/hashing.html) · [Wrapper Types](https://nnethercote.github.io/perf-book/wrapper-types.html) | [[40 Reference/Perfecting Rust - Performance Engineering#Understand ownership and heap costs\|Understand ownership and heap costs]] |
| Shape the hot path | [Iterators](https://nnethercote.github.io/perf-book/iterators.html) · [Bounds Checks](https://nnethercote.github.io/perf-book/bounds-checks.html) · [Inlining](https://nnethercote.github.io/perf-book/inlining.html) · [Machine Code](https://nnethercote.github.io/perf-book/machine-code.html) | [[40 Reference/Perfecting Rust - Performance Engineering#The whole Performance Book as a decision map\|The whole Performance Book as a decision map]] |
| Control external and concurrent work | [I/O](https://nnethercote.github.io/perf-book/io.html) · [Logging and Debugging](https://nnethercote.github.io/perf-book/logging-and-debugging.html) · [Parallelism](https://nnethercote.github.io/perf-book/parallelism.html) | [[40 Reference/Perfecting Rust - Performance Engineering#Profile to explain the cost\|Profile to explain the cost]] |
| Build and maintain | [Build Configuration](https://nnethercote.github.io/perf-book/build-configuration.html) · [Linting](https://nnethercote.github.io/perf-book/linting.html) · [Compile Times](https://nnethercote.github.io/perf-book/compile-times.html) | [[40 Reference/Perfecting Rust - Performance Engineering#Practice until the reasoning is reproducible\|Practice until the reasoning is reproducible]] |

The three pinned implementation diffs are analyzed in [[40 Reference/Perfecting Rust - Performance Engineering#Learn from linked commits, including their limitations|the historical-commit audit]]. Their author-reported results retain their historical scope.

## Local library routes

The inventory contains 14 selected files from a filename search that returned 92 candidates, including duplicates and unrelated matches. Exact file hashes and inspection scope are in [local-library.json](local-library.json). Use [[40 Reference/Perfecting Rust - Performance Engineering#Your local Rust bookshelf|the fuller bookshelf section]] for the proposed exercises.

| Local book | Reading route | Recorded inspection status |
|---|---|---|
| [Rust for Rustaceans](</var/mnt/STORAGE-10TB/Book Library/Jon Gjengset - Rust For Rustaceans_ Idiomatic Programming for Experienced Developers (2021, No Starch Press) - libgen.li.pdf>) | Available early-access chapters 2–9; later listed chapters are absent. | Front matter and contents inspected; full reading remains open |
| [Rust Atomics and Locks — Mara Bos](</var/mnt/STORAGE-10TB/Book Library/Mara Bos - Rust Atomics and Locks (2023, O'Reilly Media) - libgen.li.pdf>) | Ch. 3 memory ordering → 6 Arc → 7 processor → 8 operating-system primitives | Front matter and contents inspected; full reading remains open |
| [Programming Rust, third edition early release](</var/mnt/STORAGE-10TB/Book Library/Jim Blandy, Jason Orendorff, and Leonora F. S. Tindall - Programming Rust (2025, O'Reilly Media, Inc.) - libgen.li.epub>) | Five-chapter early release; use the local 2021 second edition for the wider route. | Front matter and contents inspected; full reading remains open |
| [Programming Rust, 2nd edition — Blandy, Orendorff, Tindall](</var/mnt/STORAGE-10TB/Book Library/Jim Blandy_ Jason Orendorff_ Leonora F.S. Tindall - Programming Rust, 2nd Edition (2021, O'Reilly Media, Inc.) - libgen.li.epub>) | Ch. 4–5 ownership/references → 15–18 iterators, collections, text and I/O → 19–20 concurrency/async → 22 unsafe | Front matter and contents inspected; full reading remains open |
| [Effective Rust — David Drysdale](</var/mnt/STORAGE-10TB/Book Library/David Drysdale - Effective Rust (2024, O'Reilly Media, Inc.) - libgen.li.epub>) | Items 8–9 pointers/iterators, 11–12 RAII/dispatch, 14–17 lifetimes/parallelism, 20 optimization, 25–32 dependencies/tooling/CI | Contents inspected; selected prose from Items 20 and 32 read |
| [Zero To Production In Rust — Luca Palmieri](</var/mnt/STORAGE-10TB/Book Library/Luca Palmieri - Zero To Production In Rust_ An introduction to backend development (Updated) (2023) - libgen.li.epub>) | Ch. 4 telemetry, 5 deployment, 8 errors, 11 fault-tolerant workflows | Front matter and contents inspected; full reading remains open |
| [Rust in Action — Tim McNamara](</var/mnt/STORAGE-10TB/Book Library/Tim McNamara - Rust in Action_ Systems programming concepts and techniques (2021, Manning Publications Co.) - libgen.li.epub>) | Ch. 4 ownership → 6 memory → 7 storage → 8 networking → 10 processes/threads/containers | Front matter and contents inspected; full reading remains open |
| [Command-Line Rust — Ken Youens-Clark](</var/mnt/STORAGE-10TB/Book Library/Ken Youens-Clark - Command-Line Rust_ A Project-Based Primer for Writing Rust CLIs 1 (2022, O'Reilly Media) - libgen.li.pdf>) | Ch. 3–6 cat, head, wc and uniq; then Ch. 9 grep | Front matter and contents inspected; full reading remains open |
| [Code Like a Pro in Rust — Brenden Matthews](</var/mnt/STORAGE-10TB/Book Library/Brenden Matthews - Code Like a Pro in Rust (2024, Manning) - libgen.li.pdf>) | Ch. 4–5 data structures/memory → 6–7 tests → 8–9 async/services → 11 optimizations | Front matter and contents inspected; full reading remains open |
| [Rust Servers, Services, and Apps — Prabhu Eshwarla](</var/mnt/STORAGE-10TB/Book Library/Prabhu Eshwarla - Rust Servers, Services, and Apps (Final Release) (2023, Manning) - libgen.li.pdf>) | Ch. 5 errors → 6 API refactoring → 10 async → 12 Docker deployment | Front matter and contents inspected; full reading remains open |
| [The Accelerated Guide to Smart Pointers in Rust — Tim McNamara](</var/mnt/STORAGE-10TB/Book Library/Tim McNamara - Smart Pointers in Rust (2023, Accelerant Press) - libgen.li.pdf>) | §6 standard pointers/locks → §7 Drop and Deref → §8 cycles and extensions | Front matter and contents inspected; full reading remains open |
| [Write Powerful Rust Macros — Sam Van Overmeire](</var/mnt/STORAGE-10TB/Book Library/Van Overmeire, Sam_ - Write Powerful Rust Macros (2024, Manning Publications Co. LLC) - libgen.li.epub>) | Ch. 3 procedural macros → 6 testing → 7 errors → 9 infrastructure DSL | Front matter and contents inspected; full reading remains open |
| [Linux Containers and Virtualization — Shashank Mohan Jain](</var/mnt/STORAGE-10TB/Book Library/Shashank Mohan Jain - Linux Containers and Virtualization_ Utilizing Rust for Linux Containers (2023, Apress) [10.1007_978-1-4842-9768-1] - libgen.li.epub>) | Ch. 3 namespaces → 4 cgroups → 5 layered filesystems → 8 containers with Rust | Front matter and contents inspected; full reading remains open |
| [The Rust Programming Language, 2nd edition — Klabnik and Nichols](</var/mnt/STORAGE-10TB/Book Library/Steve Klabnik_ Carol Nichols - The Rust Programming Language, 2nd Edition (2023, No Starch Press) - libgen.li.epub>) | Ch. 4 ownership, 8 collections, 10 lifetimes, 13 iterators, 15 smart pointers, 16 concurrency | Front matter and contents inspected; full reading remains open |

For the two partial editions, see [[40 Reference/rust-mastery/2026-09-06/Learning Status and Next Steps#Partial books and available alternatives|the available alternatives]]. Local book links rely on the storage mount keeping its current path.

## Other sources and builders

Continue through [[40 Reference/Perfecting Rust - Performance Engineering#The wider Rust library|the wider Rust library]] for official references, courses, async, serialization and delivery tools, and [[40 Reference/Perfecting Rust - Performance Engineering#Builders worth studying|the builder map]] for the associated primary work and exercises. The machine-readable ledger contains 57 additional cited web links; a link is a reading route, not an assertion that every page of the linked project was reviewed.

Turn a chosen source into a bounded exercise using [[40 Reference/rust-mastery/2026-09-06/Learning Status and Next Steps#Next practice work|the next-practice checklist]], then attach the resulting evidence to [[40 Reference/rust-mastery/2026-09-06/README|the lab record]].
