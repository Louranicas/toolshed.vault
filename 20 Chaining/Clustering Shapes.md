---
tags: [toolshed, chaining, clustering, parallel, cascade, tree, matrix, web]
created: 2026-09-02
---

# 🕸️ Clustering Shapes — chain, tree, matrix, web

[[Tool Chaining Patterns]] gave the eight *shapes of composition*. This is about the **shape of
the fan-out itself** — how many things run, and who decides. Four shapes, in increasing order of
how much the runtime knows that the author did not.

| Shape | Width decided by | Example |
|---|---|---|
| **Chain** | the author | `producer \| filter \| consumer` |
| **DAG** | the author | `doctor.toml` — 9 declared stages, 1 wave |
| **Tree** ⭐ | **the runtime** | `tree-repos` — one child per repo *found* |
| **Matrix** ⭐ | **two axes**, one discovered | `matrix-quality` — repos × checks |
| **Web** ⭐ | converging + **bidirectional** | `web-review` — three producers → synthesis → round trip |

The last three needed a change to the engine: stages whose width is **not knowable when the spec
is written**.

## What had to change

A static DAG can be layered once, up front. A tree cannot — a `foreach` stage's width depends on
what an earlier stage returned. So the scheduler became **iterative**: expand what is now
expandable, run everything whose dependencies are satisfied, repeat.

```toml
foreach = "discover"                              # one child per element
matrix  = { repo = "repos", check = ["test","ci"] }   # cartesian product
```

Each child gets its own binding (`{{item}}`, or `{{repo}}`/`{{check}}`) and an id like
`probe[deep-diff-forge]`, printed with a `└` so the tree is visible in the run.

## Tree — width discovered at runtime

`tree-repos`: level 0 finds which repos have a justfile; levels 1–2 spawn one child *per repo*.
The spec never says "seven".

```
✓ W5 discover                      34 ms  ["deep-diff-forge", "difftastic", …]
✓ W2 └ probe[deep-diff-forge]      55 ms  {"repo":…,"branch":"main","dirty":0,"recipes":29}
✓ W2 └ probe[herdr]                90 ms  …
   wave 2: 14 in parallel — 90 ms wall vs 947 ms serial, saved 857 ms
```

**7 repos → 14 children → 98 ms total.** Add a repo to the machine and the tree grows itself.

## Matrix — dimensional fan-out

`matrix-quality`: one axis discovered (repos with a justfile), one declared
(`test`/`check`/`lint`/`ci`). **5 × 4 = 20 cells, 67 ms wall vs 1186 ms serial.** Nothing
enumerates the cells; adding a check to the list widens the matrix.

The output is a real quality map — `herdr` has all four recipes, `difftastic` none.

## Web — converging, and bidirectional

`web-review` is neither a chain nor a tree. Three independent producers converge on one
synthesis stage, which feeds a write, whose *effect* is read back:

```
   clippy ─┐
 coverage ─┼─► synthesise ─► push ─► pull ─► balance
      git ─┘                          ▲
                        (human writes ─┘ out of band, read back here)
```

**Bidirectional** because the review session is a two-way surface: `push` writes agent findings
into the human's live diff; `pull` reads what is there afterwards **including notes the agent did
not write**; `balance` reports the ratio and what it means.

| State | Verdict |
|---|---|
| clean diff, human note present | `agent=0 human=1 — human-only review` |
| two lints introduced | `agent=2 human=1 ratio=2 — two-way: both sides annotated` |

That distinction matters: agent annotation is **evidence**, human annotation is **review**. A
cascade that cannot tell them apart cannot gate on the difference.

## The bug this exposed ⭐

**`render` stringified captured JSON with Python's `str()`** — emitting `{'author': 'x'}`, which
is Python repr, *not* JSON: single quotes, `True`, `None`. Any downstream `jq --argjson` breaks.

It survived every earlier cascade because **`[]` and `{}` are identical in both notations**, and
every prior stage that passed structured data happened to pass an empty one. The web cascade was
the first to pass a populated array between stages. Fixed by re-encoding with `json.dumps` for
dict/list/bool/None.

> The general lesson: a serialisation bug hides wherever the empty case is the common case.
> Test structured hand-offs with data in them.

## Composed through every layer

The shapes are reachable from each layer of the stack, and adding one requires touching only the
bottom:

```
atuin scripts run shape -v shape=matrix      # synced, templated
        └─ just matrix                        # the project's verb
             └─ habitat-cascade run …         # the engine
                  └─ rg · jq · git · just     # the tools
```

And the **`cockpit` MCP server picked up all three new cascades without being modified** — it
lists specs from the filesystem, so a new `.toml` is immediately callable as
`ws_cascade name=tree-repos`. One caveat: `action=graph` shows the *declared* shape (2 stages),
not the expanded one, because expansion is a runtime event.

## Distributed — fan-out × isolation ⭐

A stage may declare `sandbox = true`, and the engine routes it through `podman exec` into a
[[Sandbox Fanout and Fusion|habitat sandbox]] instead of running it locally. Combined with
`foreach`, that is a **distributed cascade**: N children of one stage, each in its own container,
sharing nothing but a read-only mount.

```
✓ W4 discover                34 ms  ["…/stats.rs", "…/generated.rs", "…/lib.rs"]
✓ W2 └ analyse[stats.rs]    181 ms  {"file":…,"lines":55,"fns":6,"host":"85aa9c046fe0"}
✓ W2 └ analyse[generated.rs] 223 ms  …
✓ W2 └ analyse[lib.rs]      374 ms  …
   wave 2: 4 in parallel — 374 ms wall vs 812 ms serial
```

**A tree cascade decides how many. A sandboxed stage decides where.** Together: distributed
execution with DAG semantics — no shared cwd, no shared filesystem writes, no shared process tree.

### Two bugs this exposed

**F38 · Truncating a label from the FRONT collapses distinct children.** Child ids were built by
truncating each binding to 18 chars — but file paths share prefixes, so three different files all
produced `analyse[crates_arena-core_]`, collided in the dict, and **only one child ran**. The run
looked successful. Label from the *tail*, and disambiguate anything still equal.

**F39 · `hash()` on strings is salted per process.** Round-robin placement via
`abs(hash(id)) % len(boxes)` put all three children in one box on one run and spread them over
three on the next — the same input, different placement, because `PYTHONHASHSEED` is random per
process. Use a stable digest (`hashlib.md5`) for anything that must be reproducible. Note the
trade: a stable digest is deterministic and *statistically* balanced, not perfectly balanced —
perfect balance needs wave-level assignment, and would give up per-child placement stability.

## Closing the loop: MCP inside a cascade ⭐

The stack was one-directional — MCP tools shelled out to `habitat-cascade`. `mcp-bridge` reverses
it: cascade **stages call MCP tools** through `mcpc`, so a server becomes a composable unit inside
a parallel DAG rather than only an entry point to one.

```
✓ W1 overview      142 ms  12          ← mcpc cockpit call ws_overview
✓ W2 bacon_state   130 ms  {…}         ← mcpc cockpit read ws://service/bacon/state
✓ W1 trap           85 ms  …           ← mcpc ground-truth call recall_trap
   wave 1: 3 in parallel — 142 ms wall vs 357 ms serial
✓ W2 verify        253 ms  {…}         ← mcpc ground-truth call hang_check
✓ W5 join           32 ms  {"services_running":12,"bacon_idle":false,…}
```

Three MCP calls across **two different servers**, in parallel, joined by a fifth stage. The same
protocol runs in both directions: `MCP → cascade → mcpc → MCP`.

`mcpc` (`~/.local/bin/mcpc`) is the small stateless client that makes this possible —
`discover · tools · resources · templates · prompts · call · read · prompt · surface`. Its
`surface` action reports what a server costs a client **by tier**, which is how the missing
per-tool output budgets on `ground-truth` were caught:

```
tier 1  tools/list      8 tools   869 chars of description  [PAID EVERY SESSION]
tier 2  templates/list  4 templates                         [on demand]
tier 3  resources/list  7 resources                         [on demand]
per-tool output budgets declared: 8/8
```

Related: [[Tool Chaining Patterns]] · [[Tool Clusters]] · [[Cascade Engine]] · [[MCP Servers]] ·
[[00 - Toolshed Index]] · [[Cascade and Runbook Catalogue]] · [[Habitat Introspection]] ·
[[Runbooks]]
