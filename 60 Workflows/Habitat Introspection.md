---
tags: [toolshed, workflow, introspection, profiling, telemetry, self-improvement]
created: 2026-09-02
updated: 2026-09-06
source: ~/.local/bin/habitat-introspect
---

# 🔬 Habitat Introspection — the system profiling itself

Every cascade run leaves a dated receipt with per-stage ms/rc/value and the wave structure.
Across enough runs that is a **telemetry corpus the habitat produced about itself**. This reads
it back and turns it into a decision.

```bash
just introspect            # habitat-introspect
just reprofile 4           # run doctor N times, then profile — verify a change
habitat-introspect --json --top 10
```

## What it reports

- **Slowest stages** by median, with range and sample count
- **Recent vs earlier** — the last third of each stage's runs against the rest
- **Most erratic** — coefficient of variation, to find unreliable stages
- **Parallel efficiency** per cascade — serial cost ÷ wall time
- **Cost by workspace**, and any failing stages

## Resource measurements alongside timing

The receipt-based timing analysis below does not measure peak RAM, tmpfs growth or the cause of
I/O stalls. Pair a representative run with available memory, PSS, memory/I/O pressure, worker
counts and scratch sizes from [[40 Reference/lukes-workflows/2026-09-06/README|the resource collectors]].
Take comparable before/during/after observations; `just reprofile` actually reruns work.

Change one variable at a time: scratch placement, worker count, polling interval or session
lifecycle. Require equivalent correctness results before accepting a faster run. The September 6
audit found about 66 GiB available but unresolved high I/O pressure; neither an old speedup ratio
nor Atuin elapsed command duration explains that signal. See [[50 Field Notes/lukes workflows#An unresolved performance signal: I/O pressure|the open measurement question]].

The timings and ratios below remain historical receipts, not measurements of today's maximum
useful factory concurrency.

## The loop it closed ⭐

Over 25 runs it identified `palace` as the doctor's **critical path**: ~550 ms of a ~620 ms run.
`mempalace status` opens ChromaDB to count drawers.

**The important part is what came next.** A `sqlite3` count over the palace database returns in
~10 ms — but the obvious query gave **1578**, not 1208. That is a *different metric*, and swapping
it would have traded correctness for speed while looking like a win. Breaking it down by
collection found the exact one:

```sql
select count(e.id) from collections c
  join embeddings e on e.segment_id in (select id from segments where collection = c.id)
 where c.name = 'mempalace_drawers';     -- 1208, exactly what `mempalace status` reports
```

Verified equal before adopting, with a fallback to `mempalace status` if the schema ever moves.

| | before | after |
|---|---|---|
| `palace` stage | ~550 ms | **~35 ms** (−94%) |
| whole `doctor` cascade | ~620 ms | **~375 ms** (−40%) |

> **Measure, then verify equivalence, then adopt.** A faster query that answers a different
> question is not an optimisation.

## Two findings about profiling itself

**F36 · A median over all history hides a recent change.** After the fix, `doctor::palace` still
showed a 543 ms median — the eight old runs dominated — while its range had quietly become
`34–600`. A profiler that cannot see an improvement cannot verify one. Fixed by comparing the most
recent third of each stage's runs against the rest, flagging IMPROVED/REGRESSED beyond ±25%.

**F37 · The slowest stage in a parallel wave slows its siblings.** Removing `palace` improved
**seven other stages by 28–46%** — stages that ran *concurrently* with it and were never waiting
on it. ChromaDB's CPU and IO burst was contending with them. So the cost of a slow stage is not
just its own wall time; in a parallel wave it taxes everything beside it. **Optimising the
critical path of a parallel wave pays twice.**

## Parallel efficiency, measured

Serial cost ÷ wall time across all recorded runs:

| cascade | efficiency | shape |
|---|---|---|
| `matrix-quality` | **11.49×** | dimensional fan-out, 20 cells |
| `tree-repos` | **7.95×** | runtime tree, 14 children |
| `full-sweep` | 2.72× | 11 declared parallel probes |
| `doctor` | 2.65× | 9 parallel checks |
| `mcp-bridge` | 1.49× | 3 parallel MCP calls, then a chain |
| `web-review` | 1.09× | ← inherently sequential |

`web-review` scoring 1.09× is **correct, not a failure**: a bidirectional round trip
(push → pull → balance) cannot be parallelised, because each step depends on the previous one's
effect on a shared surface. The number is telling the truth about the shape.

## Rust performance practice

The historical equivalence check here connects to [[40 Reference/Perfecting Rust - Performance Engineering#The engineering loop|the Rust performance engineering loop]]. Use [[40 Reference/Perfecting Rust - Performance Engineering#Benchmark the question you actually care about|the benchmark contract]] to define comparable work, then inspect [[40 Reference/rust-mastery/2026-09-06/README#Results to inspect|the Rust allocation lab’s evidence]] for an example that separates allocation activity from peak memory.

Related: [[Cascade Engine]] · [[Clustering Shapes]] · [[00 - Field Findings]] ·
[[00 - Workflows]] · [[00 - Habitat Toolkit]] · [[00 - Toolshed Index]] ·
[[Assimilation - Rules That Fire]] · [[Knowledge Audit]] · [[Runbooks]]
