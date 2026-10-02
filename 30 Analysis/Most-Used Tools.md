---
tags: [toolshed, analysis, atuin, telemetry]
created: 2026-09-02
source: atuin history (156 commands after `atuin import auto`)
---

# Most-Used Tools — what the shell history actually says

Derived from [[atuin]]'s database on 2026-09-02, after running `atuin import auto` (which folded 59 pre-atuin bash commands in: 97 → **156**).

> [!warning] Read this as a weak signal, honestly
> 156 commands over ~2 days is a **small sample**, and it is skewed: it covers the habitat's *setup* sessions, and it only sees the user's interactive shells — **not** the hundreds of commands agents run through tool harnesses, and not nushell (which keeps its own separate history). Treat the rankings as directional, and the *adjacencies* as the more interesting half.

## Frequency

| n | tool | |
|---|---|---|
| 24 | **mempalace** | recall dominates — the habitat's most-used tool by a factor of 2.5 |
| 9 | herdr | the spine |
| 8 | codex | agent |
| 7 | tv · podman-tui | |
| 6 | repo-fleet-status | |
| 5 | nvim · lazygit · hunk · yazi · gh · atuin · bacon · just | a flat plateau — the loadout is evenly exercised |
| 4 | claude · tuicr · jqp | |
| 3 | nu | |

**Reading:** the flat 4–5 plateau says no tool has become vestigial; the mempalace spike says the dominant activity is *asking what we know*.

## Co-occurrence in a single command line (true piping)

| n | pair |
|---|---|
| 4 | `herdr` ⇄ `jqp` |

Only one real pipe pair, and it is the habitat inspecting itself (`herdr pane list | jqp`). **This is the finding that matters: the toolchain is barely being chained.** Sixteen capable tools are being used as sixteen destinations rather than as a pipeline. That gap is what [[Tool Chaining Patterns]] and [[Workflow Recipes]] exist to close.

## Sequential adjacency — what follows what

| n | chain | reading |
|---|---|---|
| 3 | `atuin` → `mempalace` | *what did I type* → *what do I know* — the two halves of a memory question |
| 2 | `lazygit` → `hunk` | operate the repo → review the result |
| 2 | `tv` → `nvim` | find → edit |
| 2 | `yazi` → `podman-tui` | browse files → check containers |
| 2 | `nu` → `tv`, `tv` → `atuin`, `podman-tui` → `tv` | tv as the hub you return to |
| 2 | `claude` → `codex`, `codex` → `nu` | agent handoff, then structured inspection |

**`tv` appears in four adjacency pairs — more than any other tool.** It is behaving as the *switchboard*: the thing you go through between two other tools. That argues for investing in [[television]] custom channels (a `herdr-panes` channel, an `obsidian-notes` channel) more than in any other single integration.

## What the data implies

1. **Recall is the primary activity** → the [[mempalace]] MCP wiring is the highest-leverage unwired integration.
2. **Chaining is nearly absent** → the wins are in composition, not more tools.
3. **`tv` is the natural hub** → custom channels turn a finder into a habitat-wide teleporter.
4. **`atuin → mempalace` is the signature move** → worth making one command ([[Workflow Recipes]] R1).

## Reproducing this

```bash
atuin stats            # or: atuin stats day|week|month|year|all
atuin history list --cmd-only > hist.txt
# frequency / pipe co-occurrence / adjacency analysis: see the script in Workflow Recipes R7
```

Re-run periodically — the sample grows, and the adjacency table is the part that will sharpen.

Related: [[atuin]] · [[Tool Chaining Patterns]] · [[Tool Clusters]] · [[Workflow Recipes]] ·
[[00 - Toolshed Index]] · [[00 - Workflows]]
