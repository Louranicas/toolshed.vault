---
tags: [toolshed, tool, workspace-1, memory, retrieval]
tool: MemPalace
version: 3.9.0
upstream: https://github.com/MemPalace/mempalace
workspace: W1 · pane w1:pQ
agent_door: habitat recall <query>   ·   mempalace search
---

# MemPalace — local-first verbatim memory over the vaults

**The most-used tool in this habitat** (24 of 156 recorded commands — [[Most-Used Tools]]). Stores content **verbatim**, never summarised, and retrieves it semantically. Structure is spatial: **wings** → **rooms** → **drawers**. ChromaDB + all-MiniLM embeddings on CPU; nothing leaves the machine.

Current palace: wing `fedora_obsidian_vaults`, rooms `herdr_fedora_habitat.vault` (589) + `fedora_kinoite.vault` (99) + this vault. Data in `~/.mempalace`.

## Complete command surface (3.9.0)

| Command | Purpose |
|---|---|
| `init <dir>` | detect rooms from folder structure, create a palace |
| **`mine <dir>`** | ingest files (incremental). `--mode projects\|convos\|extract` · `--source ADAPTER` · `--wing` · `--dry-run` ⭐ · `--no-gitignore` · `--include-ignored` · `--limit` · `--agent` · `--background` · `--max-chunks-per-file` |
| `sweep` | tandem miner — catches what the primary miner missed |
| `sync` | prune drawers whose sources were deleted/gitignored/moved |
| **`search <q>`** | semantic + exact-word retrieval (the agent door) |
| **`wake-up`** | L0+L1 session-priming brief, ~600–900 tokens |
| `compress` | AAAK-dialect drawer compression (~30×) |
| `split <file>` | split transcript mega-files before mining |
| `hook` | JSON stdin → JSON stdout; designed for editor/agent event hooks |
| `instructions` · `rules` | emit skill instructions / a shared-brain agent rules block for CLAUDE.md |
| `repair` · `repair-status` | rebuild the vector index; compare sqlite vs HNSW counts (read-only) |
| `daemon` | opt-in long-lived daemon (**off** here) |
| **`mcp`** | print the MCP setup command — wiring into Claude Code is still open — see [[00 - Toolshed Index]] |
| `serve` · `logstream` · `task` · `artifact` · `palace` · `hallways` · `status` · `migrate` · `update` | server, streaming, task/artifact stores, embedder identity, entity links, stats |

## The `--dry-run` rule ⭐

**Always dry-run a new mine source.** On 2026-09-02 a naive mine of the kinoite vault would have filed **13,881 drawers** of minified `.obsidian` plugin JS and swamped retrieval. The fix — a `.gitignore` with `.obsidian/` plus a `mempalace.yaml` room definition — is now standard for every vault here, including this one.

```bash
mempalace mine <dir> --wing fedora_obsidian_vaults --dry-run   # verify counts FIRST
mempalace mine <dir> --wing fedora_obsidian_vaults
mempalace status ; mempalace hallways
```

`hallways` surfaces **entity co-occurrence links** across drawers — the palace's own clustering signal, and a direct input to [[Tool Clusters]].

## Agent surface — the strongest in the toolchain

`search` and `wake-up` are pure CLI, so retrieval is available mid-thought. `rules` emits a block designed to be pasted into `CLAUDE.md`. `mcp` would make retrieval a native tool call instead of a shell-out — the single highest-leverage unwired integration in this habitat.

## Chains

**Feeds from:** the three Obsidian vaults (mined). **Feeds into:** everything — it is the recall layer.
The habitat's most common tool adjacency is `atuin → mempalace`: *what did I type* → *what do I know*. Those are the two halves of a memory question, and running them together is the highest-value chain here ([[Workflow Recipes]] R1).

Related: [[atuin]] · [[Most-Used Tools]] · [[Workflow Recipes]] · [[Arena Practice Ground]] ·
[[Command Matrix]]
