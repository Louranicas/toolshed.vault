---
tags: [toolshed, toolkit, forge, rust, deployment, zero-touch, verified]
built: 2026-09-02
source: /var/home/Louranicas/fedora-arena/forge
commit: 46959fa
---

# 🔨 Forge — a Rust codebase deployment framework


> **⚓ Code anchor** — `~/fedora-arena/forge/crates/forge-spec/src/lib.rs:447` · expects `pub fn build_order`
> The deterministic topological order, and the cycle rejection, are decided here. The blueprint grammar in this note is downstream of it.
> *Verified 2026-09-03 · re-check `just doc-anchors`; this note updates when the code does.*

Built end to end in [[Arena Practice Ground|the arena]] from everything in this vault: the
[[Cascade Engine|cascade]] discipline, the [[Sandbox Fanout and Fusion|sandbox]] pattern,
the [[Tool Chaining Patterns|verify loop]], and forty-five [[00 - Field Findings|field findings]] worth
of scar tissue. It is the **habitat factory prototype**: a tool that deploys Rust workspaces
from a blueprint, with nothing to touch by hand.

**Status:** three gates green — `cargo fmt --check`, `cargo clippy --workspace --all-targets
-- -D warnings` under **pedantic + nursery**, and **445 tests**. Verified twice: on the host,
and again per crate in five isolated podman sandboxes whose fused verdict matches exactly.

**Zero external dependencies.** Not a boast — a design constraint that paid for itself. The
JSON codec, the blueprint parser, the argument parser and the NDJSON transport are all `std`.
A framework whose selling point is bounded failure modes cannot import a dependency tree
larger than itself.

## The crate graph

| crate | kind | responsibility | tests |
|---|---|---|---|
| `forge-contracts` | lib | wire types, error taxonomy, std-only JSON codec. **Performs no I/O** — it is a leaf | 131 |
| `forge-spec` | lib | blueprint parser + validator, deterministic topological build order | 78 |
| `forge-socket` | lib | NDJSON over an owner-private Unix domain socket | 71 |
| `forge-scaffold` | lib | idempotent tree materialisation | 69 |
| `forge-cli` | lib + bin | argument parsing and orchestration; one dispatch path for two front doors | 96 |

Dependencies point one way only, and `forge-spec` rejects a cycle in *its input* using the
same topological sort that orders the build.

## The blueprint

Line-oriented, not TOML. The whole grammar fits on a page, every parse error carries a line
number, and the failure modes are enumerable.

```
name         = habitat-factory
edition      = 2021
rust-version = 1.75

crate forge-contracts : lib
    doc = wire types, JSON codec and the error taxonomy; performs no I/O
    dep =

crate forge-cli : bin
    doc = argument parsing and orchestration
    dep = forge-contracts, forge-spec, forge-socket, forge-scaffold

gate fmt    = cargo fmt --check
gate clippy = cargo clippy --all-targets -- -D warnings
gate test   = cargo test
```

**The framework describes itself.** `specs/habitat-factory.forge` *is* forge's own blueprint,
and `forge apply` on it produces a workspace that passes its own fmt/clippy/test gates. That
round trip is a test (`the_shipped_blueprint_deploys_and_the_result_builds`), not a claim.

## Zero-touch, demonstrated

```console
$ forge validate --spec specs/habitat-factory.forge
ok
  name: habitat-factory

$ forge plan --spec specs/habitat-factory.forge --root /tmp/out
ok
  actions: 25                    # writes nothing; the root is still absent

$ forge apply --spec specs/habitat-factory.forge --root /tmp/out
ok
  created: 25   skipped: 0   absent: 0   attempts: 1

$ forge apply --spec specs/habitat-factory.forge --root /tmp/out
ok
  created: 0    skipped: 25  absent: 0   attempts: 1     # idempotent

$ forge gates --spec specs/habitat-factory.forge --root /tmp/out
ok
  ran: 3        failed: 0                                # the deployed tree gates itself
```

## Command surface

| command | writes? | what it does |
|---|---|---|
| `forge ping` | no | liveness + protocol version + method list |
| `forge validate --spec S` | no | parse and check a blueprint; errors carry line numbers |
| `forge plan --spec S --root R` | no | what `apply` would do |
| `forge apply --spec S --root R` | **yes** | materialise, skipping what exists, then verify |
| `forge status --spec S --root R` | no | which paths are present |
| `forge gates --spec S --root R [--gate N]` | **yes** | run the blueprint's gates |
| `forge serve [--socket P]` | **yes** | listen on the Unix socket |

Flags: `--spec`, `--root`, `--socket`, `--attempts 1..=10`, `--json`.

## Three ideas worth stealing

### One dispatch, two front doors

`forge apply` and a `forge.apply` request over the socket both build a `Request` and call the
same `dispatch()`. There is exactly one implementation of what a method means, so the CLI and
the socket cannot drift — and every CLI test is also a socket test. This is the same shape as
[the habitat's two doors](obsidian://open?vault=herdr-fedora-habitat.vault&file=70%20Toolchain%2FHabitat%20Service%20Bridge) (`habitat q` vs `habitat pane`), applied
one level down.

### Apply never overwrites — and says so

An existing path is **skipped and reported as skipped**, never clobbered. That single rule is
what makes re-running safe, and it is why `apply` on a materialised tree is a no-op that still
verifies. Same property that makes `habitat respawn` safe at any time.

### The verify loop is in the tool, not the runbook

`apply` writes, then **re-reads the filesystem** and only reports success if nothing is
absent. Not "I believe I wrote 25 files" but "I read the tree back and it is complete."
Bounded at `--attempts` (default 3, max 10), because a path that *cannot* be created must
stop the machine rather than be retried forever. See [[Tool Chaining Patterns#P9 · The verify loop — act, check, remediate, re-check|P9]] and [[Runbooks#The verify loop]].

## What the process caught

Three real defects, each found by a specific practice, each now a test.

**A cold sandbox found what a warm target dir hid.** The self-hosting test spawns
`cargo build` in a generated workspace whose crate names are *identical* to the outer ones.
The child inherits `CARGO_TARGET_DIR` and overwrote the real `libforge_contracts.rlib` with
the scaffold's stub — surfacing much later as an unrelated doctest import failure. It passed
on the host every time, because the host's target dir was warm. Five isolated sandboxes with
cold target dirs failed it immediately. → [[00 - Field Findings#F46]]

**A bound that bounded nothing.** `MAX_LINE = 1 MiB` was checked *after*
`BufRead::split` had already allocated the whole line, so a client sending gigabytes without a
newline was an unbounded allocation. Now read through `Read::take`, with a test that measures
how many bytes the server actually consumes rather than trusting the response.
→ [[00 - Field Findings#F47]]

**The same shape, found by looking for it.** Having fixed one post-hoc limit, the obvious
question was where else the pattern occurred: `read_to_string` on a caller-supplied blueprint
path ran before `forge-spec`'s `MAX_BLUEPRINT` could apply. → [[00 - Field Findings#F48]]

## Hardening

`docs/HARDENING.md` in the repo is the full table: every bound with the test that proves it,
plus an explicit **"not defended against"** section — gates run arbitrary shell by design,
`serve` is one connection at a time, and `0600` on the socket is the entire access-control
model. An unlisted gap reads as a covered one.

Socket discipline follows the habitat's existing rule: directory `0700` and socket `0600`,
both **verified after creation** because `create_dir_all` respects the umask. A stale socket
is *probed* before removal, so a second server can never displace a live one.

## The clippy deadlock, and why forge-cli has a library

`unreachable_pub` wants `pub(crate)` for items in a binary's private module.
`redundant_pub_crate` (nursery) wants `pub` for the same items. Under `-D warnings` both fire
and neither can be satisfied. Suppressing one would have been the easy answer; instead
`forge-cli` gained a real `lib.rs` with `main.rs` as a thin shell over it. Both lints go quiet,
and the test suite now drives real invocations instead of spawning a process and parsing
output. **A lint conflict is often a design question in disguise.**

Similarly, `unsafe_code = "forbid"` cannot be locally overridden — which makes
`std::env::set_var` unavailable to tests. So `SocketPath::resolve_with` takes its environment
as a parameter and the tests inject it. A stricter lint produced a more testable API.

## Rebuilding

```bash
cd ~/fedora-arena/forge
cargo fmt --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace                      # 445
```

Isolated per-crate verification (the verdict that counts):

```bash
habitat-sandbox create --n 5 --image localhost/forge-sandbox:1 \
  --src ~/fedora-arena/forge \
  --mount ~/.rustup/toolchains/stable-x86_64-unknown-linux-gnu:/rust \
  --memory 2g --cpus 2.0
habitat-sandbox fanout --tasks forge-tasks.json
habitat-sandbox destroy
```

`--mount` was added to [[00 - Habitat Toolkit|habitat-sandbox]] for exactly this: rustup keeps
the compiler in `$HOME/.rustup`, outside any `--src` tree. The sandbox image
(`forge/sandbox/Containerfile`) exists for one reason — the base toolbox image has **no
linker**, so `cargo check` and `cargo clippy` work but `cargo test` fails at the link step.

Related: [[00 - Habitat Toolkit]] · [[Sandbox Fanout and Fusion]] · [[Cascade Engine]] ·
[[Tool Chaining Patterns]] · [[00 - Field Findings]] · [[Arena Practice Ground]] ·
[herdr habitat § Habitat Factory Prototype](obsidian://open?vault=herdr-fedora-habitat.vault&file=50%20Automation%2FHabitat%20Factory%20Prototype) ·
[[00 - Toolshed Index]] · [[Assimilation - Rules That Fire]]
