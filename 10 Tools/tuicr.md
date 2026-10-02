---
tags: [toolshed, tool, workspace-5, review, agent-channel]
tool: tuicr
version: cargo
upstream: https://github.com/agavra/tuicr
workspace: W5 · pane w1:pR (on repos/deep-diff-forge)
agent_door: tuicr review list|comments|add  ⭐ by design
---

# tuicr — code review TUI with an explicit agent CLI

Signature design: **the TUI is for humans; the CLI is for agents.** Two halves of one review session, not a UI with an API bolted on.

## Commands

```bash
tuicr                            # review current repo (nearest git root; TUICR_ROOT overrides)
tuicr tui                        # explicit TUI
tuicr --no-update-check tui      # how the habitat pane pins it
tuicr pr <n>                     # review a GitHub PR / GitLab MR  (alias: mr)
tuicr review <sub>               # ⭐ the agent surface
tuicr update                     # self-update
```

**Options:** `-r/--revisions <REVSET>` (commit range; syntax follows the VCS backend) · `-p/--path <PATH>` scope to a file/dir · `-w/--working-tree` include uncommitted changes · `-A/--all-files` every tracked file · `--file <PATH>` annotate a file with **no VCS at all** · `--theme` / `--appearance light|dark|system` · `--stdout` (export to stdout instead of clipboard) · `--no-update-check`.

## ⭐ `tuicr review` — the agent half

```bash
tuicr review list                # persisted sessions for a checkout or forge repo
tuicr review comments            # print comments stored in a session
tuicr review add                 # add a local draft comment
```

So the loop is: **you** review in the TUI and type comments → **I** read them with `review comments` → I respond, or add my own with `review add` → you see them inline. `--stdout` exports the review; `:submit` inside the TUI posts to GitHub (unlocked by `gh` auth).

`--file <PATH>` is quietly useful: annotation without a repo, so prose or config can be reviewed the same way.

## TUI keys

`j`/`k` lines · `]`/`[` files · `v` visual-select a range · `c` comment → pick type (**note / suggestion / issue / praise**) · `:submit` export to forge · `q` quit — **the session persists** for the next launch.

## Overlap with [[hunk]]

Both are agent-aware review tools; they differ in direction and scope.

| | hunk | tuicr |
|---|---|---|
| Channel | local daemon, **live** session both sides share | persisted session, read/write via CLI |
| Strength | navigate + highlight *the human's live view* | forge integration (`pr`/`mr`, `:submit`) |
| Scope | any diff/patch/stash/stdin | repo revsets, PRs, or a bare file |

Use hunk while edits are in flight; use tuicr for a considered pass that ends in a posted review.

## Chains

**Feeds from:** git revsets, [[gh-dash]] (a PR number you hand me). **Feeds into:** GitHub via `:submit`, or me via `review comments`.

Related: [[hunk]] · [[gh-dash]] · [[Tool Clusters]] · [[00 - Toolshed Index]] ·
[[Arena Practice Ground]] · [[Command Matrix]] · [[Documented Surface and Source]] ·
[[Tool Chaining Patterns]] · [[lazygit]]
