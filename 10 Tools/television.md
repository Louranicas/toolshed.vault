---
tags: [toolshed, tool, workspace-1, finder, channels]
tool: television (tv)
version: 0.15.9
upstream: https://github.com/alexpasmantier/television
workspace: W1 · pane w1:pF
agent_door: (human-first) — habitat pane television
---

# television (tv) — a fuzzy finder organised around channels

fzf's idea, restructured: instead of *"pipe me a list"*, tv has **channels** — named, configurable data sources with their own preview logic. Switch source without leaving the finder.

## Built-in channels (verified `tv list-channels`)

`files` · `dirs` · `text` (live grep) · `env` · `bash-history` · `git-repos` · `git-branch` · `git-log` · `git-diff` · `docker-images`

```bash
tv                      # default channel
tv files  ·  tv text  ·  tv env  ·  tv dirs
tv git-repos            # teleport across the 31 repos on the HDD
tv git-log  ·  tv git-diff  ·  tv git-branch
tv bash-history         # ⭐ overlaps atuin — see the note below
tv list-channels · tv update-channels · tv init <shell> · tv completions <shell>
```

## Key CLI options

`--preview-*` (`header`, `footer`, `offset`, `border`, `padding`, `size`, `word-wrap`) · `--source-display` / `--source-output` / `--source-entry-delimiter` · `--input-header` / `--input-prompt` / `--input-position` / `--input-border` · `--layout` · `--height` / `--inline` / `--ui-scale` · `--no-remote` · `--exact` · `--select-1` / `--take-1` · `--watch`.

`--source-output` and `--preview-*` are what make a channel composable: a channel can *display* one thing and *emit* another.

## Keys

`Ctrl+T` remote control (switch channel) · `Ctrl+X` actions on selection · `Ctrl+H` help · `Enter` print selection to stdout (composable, like fzf) · arrows/`Ctrl+N`/`Ctrl+P` move.

## Custom channels — the real feature ⭐

A channel is just a TOML file in `~/.config/television/cable/` declaring a **source command**, an optional **preview command**, and a `preview_delimiter` + index if only part of each line should be previewed. Global settings live in `~/.config/television/config.toml`.

That means *any* command that emits lines can become a first-class, previewable finder. The habitat channels worth building (queued in the herdr vault's Future Plugin Roadmap #5):

```toml
# ~/.config/television/cable/herdr-panes.toml   (sketch)
[metadata]
name = "herdr-panes"
[source]
command = "herdr pane list | jq -r '.result.panes[] | \"\\(.pane_id)\\t\\(.tab_id)\"'"
[preview]
command = "herdr pane read {0} --source visible --lines 40"
```

Same pattern gives `obsidian-notes` over the three vaults, and `habitat-services` over `habitat ls`.

> [!done] Built 2026-09-02 — four habitat channels now live in `~/.config/television/cable/`
> `habitat-services` (16 services → preview the live pane) · `herdr-panes` (every pane → preview
> its screen) · `vault-notes` (134 notes across three vaults → `bat` preview) · `atuin-scripts`
> (the script library → preview each body).
>
> **They are scriptable, not just interactive** ([[00 - Field Findings|F31]]):
> ```bash
> tv habitat-services --take-1 --input bacon     # → bacon  w1:pJ  Workspace 2
> ```
> `--take-1 --input <query>` turns any channel into an agent-usable selector, which makes tv a
> *programmatic* index over habitat state as well as the human switchboard [[Most-Used Tools]]
> identified it as.

## Overlap note: `tv bash-history` vs [[atuin]]

They answer different questions. tv reads the flat `~/.bash_history` file; atuin queries a SQLite DB **with cwd, exit code, duration and session**. Use tv for a fast visual scan, atuin when the filter matters (`--exit 0`, `--cwd .`). atuin owns `Ctrl+R` here by design.

## Chains

**Feeds into:** `cd $(tv dirs)` · `nvim $(tv)` · `git switch $(tv git-branch)`.
`tv → nvim` and `tv → atuin` are both live adjacencies in this habitat's own history ([[Most-Used Tools]]).

Related: [[fzf]] · [[yazi]] · [[atuin]] · [[Tool Clusters]] · [[00 - Toolshed Index]] ·
[[Arena Practice Ground]] · [[Command Matrix]] · [[Tool Chaining Patterns]] · [[lazyvim]]
