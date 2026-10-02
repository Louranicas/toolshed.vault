---
tags: [toolshed, rust, research, evidence, performance]
created: 2026-09-06
updated: 2026-09-06
---

# Rust mastery — sources and reproducible evidence

**Folder:** [[40 Reference/rust-mastery/README|Rust corpus index]]. **Reading:** [[40 Reference/rust-mastery/2026-09-06/Source and Reading Map|Source and Reading Map]]. **Status:** [[40 Reference/rust-mastery/2026-09-06/Learning Status and Next Steps|Completed work and remaining practice]].

Read [[40 Reference/Perfecting Rust - Performance Engineering|Perfecting Rust — Performance Engineering]] for the research synthesis, local reading map, builders, and practice program.

This pack contains original educational Rust code, the dependency lockfile, four heap profiles, semantic and benchmark smoke receipts, and source provenance. It records a study performed on 2026-09-06. The measurements establish allocation behavior for two small fixture distributions; no elapsed-time speedup or production improvement is claimed.

| File | Purpose |
|---|---|
| [sources.json](sources.json) | Pinned Performance Book revision and chapter hashes, historical commits, and cited web resources |
| [local-library.json](local-library.json) | Fourteen selected book paths, SHA-256 hashes, edition evidence and inspection limits |
| [lab/Cargo.toml](lab/Cargo.toml) and [lockfile](lab/Cargo.lock) | Isolated Rust 2024 project; Criterion 0.8.2 and optional dhat 0.3.3 |
| [lab/src/lib.rs](lab/src/lib.rs) | Baseline, reusable-buffer candidate and four semantic tests |
| [lab/src/main.rs](lab/src/main.rs) | CLI and optional process heap profiler |
| [lab/benches/allocations.rs](lab/benches/allocations.rs) | Eight Criterion cases with input preparation and equality checks outside timing |
| [verification.json](evidence/verification.json) | Actual toolchain, successful commands, outputs, source hashes and input hashes |
| [semantic-tests.log](evidence/semantic-tests.log), [criterion-smoke.log](evidence/criterion-smoke.log) | Four passing tests and eight successful smoke cases |
| [environment.json](evidence/environment.json) | Environment visible to this session, not a separate host inventory |
| [verify_lab.py](verify_lab.py) | Bounded reproduction of tests, smoke cases and heap reports |
| [manifest.json](manifest.json) | SHA-256 and size of each retained file except the manifest itself |
| [[40 Reference/rust-mastery/2026-09-06/prime-receipt\|Historical Prime receipt]] | Initial vault routing and evidence boundaries |

## Connected notes

[[40 Reference/Command Matrix|Command Matrix]] connects the service and composition routes to all six Fedora master indexes. [[40 Reference/rust-mastery/README#Fedora master indexes|The Rust folder index]] supplies the corresponding corpus returns.

Return to [[40 Reference/Perfecting Rust - Performance Engineering#Connected notes and master indexes|the Rust learning map]] or [[00 - Toolshed Index#Rust mastery|the Toolshed master index]].

Practice companions: [[10 Tools/bacon#Rust performance practice|bacon]] · [[10 Tools/just#Rust performance practice|just]] · [[10 Tools/bottom#Rust performance practice|bottom]] · [[10 Tools/podman#Rust performance practice|podman]] · [[60 Workflows/Habitat Introspection#Rust performance practice|Habitat Introspection]] · [[60 Workflows/00 - Workflows#Rust performance practice|Workflows index]].

Cross-vault returns: [Habitat master index](obsidian://open?vault=herdr-fedora-habitat.vault&file=00%20-%20Fedora%20Master%20Index) · [Kinoite master index](obsidian://open?vault=fedora-kinoite.vault&file=00%20-%20Fedora%20Master%20Index).

## Results to inspect

The recorded process measurements are summarized here for reading directly in Obsidian.

| Input | Variant | Total blocks | Total allocated bytes | Peak tracked heap bytes |
|---|---|---:|---:|---:|
| Repeated | Owned | 10,020 | 119,846 | 8,616 |
| Repeated | Reused | 10 | 9,703 | 8,607 |
| Unique | Owned | 10,037 | 1,241,167 | 927,055 |
| Unique | Reused | 10,021 | 1,230,967 | 919,857 |

Buffer reuse sharply reduced allocation churn for repeated input, while retained distinct keys still required storage. Peak tracked heap changed little on repeated input. These observations do not establish elapsed-time improvement. See [[40 Reference/Perfecting Rust - Performance Engineering#What was actually measured on 2026-09-06|the measurement boundary and interpretation]] and [[40 Reference/rust-mastery/2026-09-06/Learning Status and Next Steps#Next practice work|the open timing experiment]].

| Fixture | Baseline profile | Candidate profile |
|---|---|---|
| 10,000 identical records | [repeated-owned.dhat.json](evidence/repeated-owned.dhat.json) | [repeated-reused.dhat.json](evidence/repeated-reused.dhat.json) |
| 10,000 distinct records | [unique-owned.dhat.json](evidence/unique-owned.dhat.json) | [unique-reused.dhat.json](evidence/unique-reused.dhat.json) |

The corresponding `.log` files include total, peak and end-of-measurement heap summaries. Open the JSON with the viewer described in the [dhat documentation](https://docs.rs/dhat/0.3.3/dhat/). Raw reports include stack paths from the original build environment.

Tests cover LF, CRLF, an unterminated final line, whitespace, blank lines, Unicode, small reader capacities, a long Unicode line, invalid UTF-8 and injected I/O errors. Complete maps are compared, rather than only aggregate counts. The full matrix is visible in `lab/src/lib.rs`; these tests are not a proof for all possible inputs.

## Reproduce in a working copy

Copy this directory to a new dated working directory before running commands. `verify_lab.py` writes fixtures, logs and profiles into its adjacent `evidence/` directory and replaces its verification receipt. Keep the archived evidence unchanged when comparing another run.

From the copied `lab/` directory, fetch the pinned dependencies if they are not cached:

```bash
cargo fetch --locked
```

From the copied pack root:

```bash
python3 verify_lab.py
```

The script runs release semantic tests, a Criterion smoke check, an optimized profiling build and four standalone processes. It uses Cargo's offline mode after dependencies are present. It records its run date and compiler. Numeric heap results can change with compiler, standard library, input paths and runtime behavior; look first for the predicted distribution-dependent effect. Argument strings and stdout are within the profiling boundary.

To collect actual time measurements, run from the copied `lab/` directory:

```bash
cargo bench --bench allocations --locked
```

This command was **not** run as a statistical timing study in the archived experiment. It uses the ordinary allocator by default; leave the `dhat-heap` feature disabled for timing. Record the execution environment, workload boundary and raw Criterion output with the experiment template in the main note.

## Research coverage

The Performance Book's 19 substantive chapters were read at commit `a05dd0f15595e98aef45e5a15072c2a71dbe37ba`. Three linked historical changes were examined in their diffs. Primary documentation qualified allocator, collection, profiling and benchmark claims. Other resources were inspected to create a learning route, with selected technical articles read more deeply.

For the local bookshelf, 92 filename matches included duplicates, different formats, archives and unrelated material. Fourteen chosen PDF/EPUB files were inspected for metadata and contents. Effective Rust Items 20 and 32 received selected prose reading. The Rust for Rustaceans contents page was rendered and inspected because color identifies included early-access chapters. The 2025-named Programming Rust EPUB is also a partial early release. Neither local file was treated as a complete published edition.

Only paths, hashes, bibliographic observations and original synthesis are retained here. The original books, extracted prose, binaries and Cargo build cache remain outside this pack. This artifact does not install tools, create scheduled learning jobs or change a production project.

The main note uses absolute links for books on the existing storage mount and Obsidian wikilinks for vault navigation. Keep source assertions dated; use the current primary documentation and new measurements when promoting a learning into a project standard.
