---
tags: [toolshed, tool, workspace-3, review, agent-channel]
tool: hunk (npm package "hunkdiff")
version: 0.20
upstream: https://github.com/modem-dev/hunk
workspace: W3 · pane w1:pK (on repos/herdr)
agent_door: hunk session <sub> --json   ⭐ the richest agent surface in the toolchain
---

# hunk — review-first diff TUI with a live agent channel

A diff viewer that runs a **local daemon**, so a human in the TUI and an agent on the CLI are looking at *the same live session*. Comments written by either side appear in the other's view.

## Viewing commands

```bash
hunk diff                    # working-tree changes — LIVE, watches agent edits
hunk diff --staged
hunk diff main               # against a ref/revset
hunk diff -- src/            # pathspec scoping
hunk show [ref]              # review a commit (what pane pK runs; HEAD by default)
hunk stash show
hunk patch <file|->          # review a patch file or stdin
hunk pager                   # use as git pager, with diff detection
hunk markup guide            # STML note-markup authoring guide
hunk update <version>
```

> Bare `hunk` / `hunk diff` **exits immediately on a clean repo** (nothing to show) — the 2026-09-01 audit lesson. Use `hunk show` for history, `hunk diff` while edits are in flight.

## ⭐ `hunk session` — the full agent API (all subcommands accept `--json`)

```bash
hunk session list [--json]
hunk session get      (<id> | --repo <path>) [--json]
hunk session context  (<id> | --repo <path>) [--json]
hunk session review   (<id> | --repo <path>) [--include-patch] [--include-notes] [--json]

# navigate the human's view
hunk session navigate (<id>|--repo <p>) --file <path> (--hunk <n> | --old-line <n> | --new-line <n>)
hunk session navigate (<id>|--repo <p>) (--next-comment | --prev-comment)

# reload the session onto a different diff
hunk session reload (<id>|--repo <p>) [--source <p>] -- diff [ref] [-- <pathspec...>]
hunk session reload (<id>|--repo <p>) [--source <p>] -- show [ref] [-- <pathspec...>]

# comments — write INTO the human's live diff view
hunk session comment add (<id>|--repo <p>) --file <path> (--old-line <n>|--new-line <n>) \
     --summary <text> [--rationale <text>] [--author <name>] [--markup <stml>] [--focus]
hunk session comment apply (<id>|--repo <p>) --stdin        # bulk, from JSON
hunk session comment list (<id>|--repo <p>) [--file <p>] [--type live|all|ai|agent|user]
hunk session comment rm (<id>|--repo <p>) <comment-id>
hunk session comment clear (<id>|--repo <p>) [--file <p>] [--include-user|--all] --yes

# highlights — draw attention to a span
hunk session highlight add (<id>|--repo <p>) --file <path> (--old-line <n>|--new-line <n>) \
     --start <n> --end <n> [--tone <tone>] [--focus]
hunk session highlight clear (<id>|--repo <p>) [--file <p>]
```

**Why this is the strongest channel here.** `comment list --type user` lets me read *your* typed comments; `comment add --focus` lets me write one and jump your cursor to it. `--markup <stml>` gives rich notes. Combined with `navigate`, an agent can *walk you through* a diff in your own TUI.

Verified live 2026-09-02: `hunk session list` returned an active session (`a368da40-…  herdr show HEAD`), so the daemon is running and the channel is open.

## TUI

Menus: File · View · Navigate · **Agent** · Help. Header shows the session (`herdr show HEAD  17 files  +394 -64`).

## Chains

**Feeds from:** git (`diff`/`show`/`stash`/patch), and *my edits* when running `hunk diff` in watch mode.
**Feeds into:** you, visually — and back to me via `comment list --type user`.
`lazygit → hunk` (operate the repo, then review it) is a live adjacency in this habitat's history.

Related: [[lazygit]] · [[tuicr]] · [[bacon]] · [[Tool Clusters]] · [[00 - Toolshed Index]] ·
[[Arena Practice Ground]] · [[Bridge - Coverage to Review]] ·
[[Bridge - Diagnostics to Review]] · [[Command Matrix]] · [[Documented Surface and Source]] ·
[[Synchronised Review and Editor]] · [[Tool Chaining Patterns]] · [[lazyvim]]
