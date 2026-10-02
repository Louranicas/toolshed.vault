---
tags: [toolshed, workflow, chaining, clustering, battern, nvim-rpc, verified]
built: 2026-09-03
source: ~/fedora-arena/scripts/habitat-chain + habitat-battern
updated: 2026-09-06
---

# 🔗 Shape-Directed Tool Chaining

**Navigation:** [[40 Reference/Command Matrix#Composition and verification routes|Command Matrix ⇄ composition routes]] · [[00 - Toolshed Index|Toolshed master index]]. Connect a producer’s output shape to an appropriate consumer.

Every chain in this habitat used to be hand-wired: the author knew the producer's output format
and picked the consumer. That does not compose — each new pair is new code. Three primitives
replace it.

## 1 · `habitat-chain` — route by what a tool EMITS

Shape is the interface. The caller names the consumer only when it disagrees with the router.

| shape | detected by | routes to |
|---|---|---|
| `json` | parses as JSON | **W5** jq / jqp |
| `diagnostics` | `file:line[:col]: msg` on ≥half the lines | **W2** nvim quickfix + **W3** hunk |
| `diff` | `diff --git` / `@@` markers | **W3** hunk |
| `table` | consistent tab columns, >2 rows | **W1** nu |
| `paths` | every sampled line is an existing path | **W1** fzf/tv |

```bash
just chain 'rg -H -n "\.unwrap\(\)" src/lib.rs'
#  shape=diagnostics (14/14 lines are file:line[:col]: message) -> W2+W3
#  W2 nvim: quickfix now holds 14 item(s)
```

**Ground truth:** `rg -n <pattern> <single file>` omits the filename — the result is `line:text`,
not `file:line:text`, and the router correctly rejects it. Use `-H`.

## 2 · The editor is a SOURCE, not only a sink

`nvim --server $NVIM_SOCK --remote-expr` works in **both** directions. Every prior chain treated
W2 as a destination; the cursor is a better query than anything typed, because it is where
attention already is.

```bash
just chain-cursor                      # rg the word under the cursor across its directory
just chain-cursor 'cargo test {word}'  # {file} {line} {word} {dir} {name} all bind
#  editor: stats.rs:33  word='return'  ->  6 results  ->  back into quickfix
```

W2 → W1 → W2, closed loop, no manual step.

## 3 · `habitat-battern` — one pattern, many targets, in parallel

A cascade is a DAG of *different* stages. Battern is orthogonal: **one pattern across a named
cluster**. Cascades express dependency; battern expresses breadth.

| cluster | n | `{}` binds to |
|---|---|---|
| `services` | 16 | cockpit service name |
| `crates` | 5 | forge crate path |
| `vaults` | 5 | registered vault path, resolved by pinned Obsidian ID |
| `detectors` | 6 | detector module |
| `repos` | 31 | git repo under STORAGE-10TB |

```bash
just battern 'cd {} && git rev-parse --abbrev-ref HEAD' repos 12
#  ok=31/31  wall=0.2s
just battern 'python3 scripts/audit/backlinks.py {} | tail -1' vaults 4
#  ok=4/4  wall=0.1s
```

`--chain` feeds the collected aggregate through `habitat-chain`, so a batch routes exactly like a
single tool. **The primitives compose:** battern → chain → editor.

## 4 · Continuous — bacon as the trigger

`forge/bacon.toml` gains `chain` (`c`) and `cursor` (`w`): on every save the detectors run and
their findings are shape-routed into the live quickfix. Event-driven rather than polled — edit,
save, `:copen`.

## 5 · Captured — atuin as the promotion point

A chain that worked once becomes a named, syncable script:

```bash
atuin scripts new chain-cursor --script <path> --no-edit   # --script takes a PATH (F3)
atuin scripts run battern-vaults
```

## `just clusterweb` — all three, across W1–W5

```
✓ W2 editor      221 ms  stats.rs:33 word='return'     ← W2 as SOURCE
✓ W3 repos       325 ms  ok=31/31
✓ W4 crates      957 ms  ok=5/5
✓ W1 vaults      283 ms  ok=4/4
✓ W2 detectors   217 ms  ok=6/6
✓ W5 routed      152 ms  shape=json                    ← battern aggregate, shape-routed
total 1111 ms · 46 targets · 5 in parallel, saved 1046 ms
```

## 6 · `habitat-poly` — one question, many substrates

The third axis. Chaining moves data *between* tools; battern runs one pattern over many
*targets*; poly asks one **question** of many **tools**. Agreement is the null result;
**disagreement is the finding**, and the report names the outlier rather than picking a winner.

```bash
just poly count '\.unwrap\(\)' src/lib.rs     # rg · grep · python · nu
just poly files '*.rs' crates                  # fd · find · python
just poly alive bacon                          # habitat registry · pgrep · herdr pane
```

**Four ground-truth findings in one session** ([[00 - Field Findings|F49–F52]]): `grep` BRE
`\(\)` is an empty group and over-counts; `grep` resolves to a different binary in different
shells; `fd`'s pattern is a regex not a glob; `nu open` infers format from the extension; and
service name ≠ process name for four of sixteen services. **Every one looked authoritative as a
single-tool answer.**

This is metamorphic testing applied to tool calls: no oracle for one call, but a **relation
between calls** that must hold.

### Provoked cases beat natural ones

A poly probe on tidy input returns AGREE and says almost nothing. Every finding here came from a
**constructed** case. `just provocations` (also a `falsify` stage) pins four of them as a
regression suite:

| provocation | disagreement |
|---|---|
| file with no trailing newline | `wc -l` **2** vs `awk END{NR}` **3** |
| multibyte text | `wc -c` **19** bytes vs `wc -m` **11** chars |
| a dotfile | `fd` **1** vs `fd -H` **2** |
| `\.unwrap\(\)` | grep **BRE 64** vs **ERE 61** |

A **CHANGED** case means a tool's default moved — re-derive the finding rather than updating the
expected value.

### Composing the axes

`battern × poly` — 16 services × 3 sources = 48 checks in **0.7 s**, resolving to 11 AGREE
(daemons) and 5 DISAGREE (shell-by-design, correctly).

## Registry boundary

The `vaults` cluster now resolves exactly the five pinned Obsidian IDs. A 2026-09-05 regression
found that the previous storage glob omitted Fabric, included adjacent Turso, and described four
vaults while returning a different set. The resolver now fails closed on missing IDs, unavailable
or duplicate paths; three offline tests cover exact selection, missing identity, and duplicate
path cases. A read-only five-target rehearsal returned all five registered vault names in 0.05 s.

The earlier `clusterweb` block above remains historical performance evidence from the four-vault
implementation; it must not be read as the current registry denominator. See [[Fabric Bash Command Plane]]
for the typed plan, validation and receipt boundary.

Related: [[Factory Roster Expansion - DevOps Toolbox]] · [[Fabric Bash Command Plane]] · [[Fabric Habitat 90-Point Promotion and Practice]] · [[Cascade Engine]] · [[Tool Chaining Patterns]] · [[Tool Clusters]] ·
[[Assimilation - Rules That Fire]] · [[Synchronised Review and Editor]] ·
[[00 - Toolshed Index]] · [[00 - Field Findings]] · [[Axiom Conformance]]
