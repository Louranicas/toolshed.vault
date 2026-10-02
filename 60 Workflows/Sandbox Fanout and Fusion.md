---
tags: [toolshed, workflow, podman, sandbox, parallel, fusion, W4]
created: 2026-09-02
updated: 2026-09-06
source: ~/.local/bin/habitat-sandbox · fedora-arena/scripts/fuse-modules.sh
---

# 📦 Sandbox Fanout & Fusion — isolated parallel workers

Fan work out to N Podman containers, then fuse their outputs and verify the join. Each worker
gets the source mounted **read-only** and its own writable `/out`. This separates their normal
output paths; the mounts, container names and lifecycle still need ownership.

The following commands describe the original four-worker demonstration. Inspect existing workers
and output ownership before repeating it; `create` replaces containers with the same names.

```bash
just sb-create 4          # habitat-sandbox create --n 4 --src <dir>
just sb-fanout            # one task per sandbox, in parallel
just sb-fuse              # consolidate into one keyed document
just sb-codegen           # generate modules in isolation → fuse into the crate → verify
just sb-destroy
```

The installed sandbox wrapper explicitly uses **host Podman** through `flatpak-spawn --host`.
The presence of a separate Podman binary inside a Toolbx does not change that execution boundary.

## Capacity and ownership — source checked 2026-09-06

`create` accepts `--n`, `--memory` and `--cpus`; its defaults are three workers, 512 MiB and one
CPU quota per worker. `fanout` sizes its pool to all task pairs and exposes no separate worker
cap. The demonstration's 512 MiB limit is not a measured allowance for large Rust builds.

The wrapper reuses names such as `hbx-1` and forcibly removes a same-named container during
creation. A different `--work` directory alone does not isolate concurrent experiment names.
Check ownership before creation/destruction; concurrent independent factories need a deliberate
naming/lease mechanism, which has not been added here.

Choose NVMe-backed `--work` storage and verify scratch paths inside each container. An isolated
`/out` does not redirect a program's `/tmp` automatically. Apply TMPDIR/target policy through the
actual worker environment, preserve mutation-runner isolation, and record what must survive
container retirement. The existing `--keep-out` option preserves outputs; automatic deletion of
untracked output is not proof that the output is unwanted.

See [[50 Field Notes/lukes workflows#The largest actionable finding: temporary data|the measured scratch issue]]
and [[60 Workflows/00 - Workflows#Daily operating cycle — reviewed 2026-09-06|the operating cycle]].

## Two demonstrations

### 1 · Parallel analysis, fused into one document

Four sandboxes each analysed a different dimension of the same read-only source:

| sandbox | module | result |
|---|---|---|
| hbx-1 | metrics | 2 rust files, 85 lines, 10 fns, 15 shell scripts |
| hbx-2 | deps | 2 crates, 1 pub mod |
| hbx-3 | docs | 5 pub fns, 5 doc lines, 10 markdown files |
| hbx-4 | tests | 5 test fns, 6 assertions, 2 test mods |

`wall 536 ms vs 1459 ms serial — saved 923 ms`. `habitat-sandbox fuse` merges them into a
**keyed** document (`modules.metrics`, `modules.deps`, …) rather than a flat `add`, which
would let identically-named fields from different workers silently overwrite each other.

### 2 · Code modules generated in isolation, fused and verified ⭐

Four sandboxes each emitted a Rust module — `variance`, `mode`, `percentile`, `normalize` —
with its own `#[cfg(test)]` block. None could see the others. `fuse-modules.sh` concatenated
them into `crates/arena-core/src/generated.rs`, declared the module, and then **verified the
join**:

```
fusing 4 module(s) from hbx-1 hbx-2 hbx-3 hbx-4
wrote crates/arena-core/src/generated.rs (108 lines)
── verifying the join ──
test result: ok. 13 passed; 0 failed
FUSION OK
```

13 tests = 5 original + 8 fused. The gate then confirmed the fused crate is clean:
`{"errors":0,"tests_passed":13,"clippy_lints":0}`.

> **The join is the risky part, not the isolation.** Four workers that each compile alone can
> still collide on names, imports or lints. Fusion is not done until `cargo test` says so —
> `fuse-modules.sh` exits non-zero and prints the errors if the join fails.

## Two traps

**[[00 - Field Findings|F33]] records a SELinux mount-label failure in the original experiment.**
The former blanket claim that `:Z` cannot accompany a read-only bind was too broad. Both `:z`
and `:Z` relabel host content; `z` is shared and `Z` is private. `ro` controls container write
access separately. Shared source across these workers needs compatible shared labelling and
appropriate host permissions; inspect the actual error instead of automatically disabling
SELinux labelling. [Podman volume labelling](https://docs.podman.io/en/latest/markdown/podman-run.1.html).

**[[00 - Field Findings|F34]] Alpine's BusyBox `grep` has no `--include`.** Analysis tasks
written against GNU grep returned confident zeros rather than errors — `test_fns: 0` on a crate
with five tests. The earlier `cat "$FILES"` example treated a multi-path string as one filename; use argument-safe
path handling such as `find … -exec grep … {} +`, with a checked aggregate/counting contract.
**A minimal sandbox image is a different userland, not just a smaller one.**

## Why this shape

- **Read-only source mount** prevents writes through that mount from the worker.
- **Per-sandbox `/out`** separates ordinary outputs when names and directories are uniquely owned.
- **`--memory 512m --cpus 1.0`** caps a runaway worker.
- **Explicit output retention** — destruction and retention are separate decisions.
  **Corrected 2026-09-03:** the original destroy removed the *containers* and left the `/out` trees — 609 MB across
  five stale workers, which is also what inflated `roundtrip`'s discovery walk. `destroy` now
  clears them, but **enumerates `git ls-files` first and skips any directory holding a tracked
  file, printing which**: four `hbx-*` dirs hold the fused code modules this note documents as
  evidence. `KEPT ×4 · cleaned out/hbx-5 · 609 M → 181 M · deleted-tracked 0`. `--keep-out` opts
  out. A mixed directory is exactly where a blanket `rm -rf` is most dangerous, so the enumeration
  is the implementation rather than a habit.

---
> 🔗 **Cross-vault synergy.** `:ro,z` vs `:Z`, the missing linker and the BusyBox userland are OS
> facts, not tool facts:
> [kinoite § Podman & Containers](obsidian://open?vault=fedora-kinoite.vault&file=Podman%20%26%20Containers).
> What a disposable machine can and cannot verify:
> [my-diary § Why I Stopped Trusting Green](obsidian://open?vault=my-diary.vault&file=Reflections%2FWhy%20I%20Stopped%20Trusting%20Green).

Related: [[Cascade Engine]] · [[podman-tui]] · [[00 - Field Findings]] · [[00 - Workflows]] ·
[[00 - Habitat Toolkit]] · [[00 - Toolshed Index]] · [[Assimilation - Rules That Fire]] ·
[[Clustering Shapes]] · [[Forge - Deployment Framework]]
