---
tags: [toolshed, tool, workspace-3, git]
tool: lazygit
version: 0.47
upstream: https://github.com/jesseduffield/lazygit
docs: https://lazygit.dev/docs/configuration/
workspace: W3 · pane w1:p9 (on repos/herdr)
agent_door: (human-first) — habitat q lazygit → plain git
---

# lazygit — operating the repo

For *operating* a repository (staging, branching, rebasing, undoing). For *reviewing agent diffs* the purpose-built tools are [[hunk]], [[tuicr]] and reviewr.

## Panels & navigation

Numbered panels: `1` Status · `2` Files/Worktrees/Submodules · `3` Local branches · `4` Commits · `5` Stash. `Tab`/`[`/`]` cycle, `?` shows **the current panel's** keybindings (the escape hatch — 144 bindings total).

| Key | Action |
|---|---|
| `Space` | stage/unstage file or hunk · `a` stage all |
| `c` | commit · `C` commit with editor · `A` amend |
| `p` / `P` | pull / push · `f` fetch |
| `d` | delete / discard (context-dependent) |
| `e` | edit · `o` open · `i` ignore |
| `s` / `S` | stash / stash options |
| `Enter` | drill into (file → hunks, commit → files) |
| `+` / `_` | expand/collapse diff view |
| `z` / `Ctrl+z` | **undo / redo** (reflog-backed) |
| `m` | merge · `r` rebase · `R` rename |
| `w` | worktrees · `Ctrl+o` copy to clipboard |
| `@` | **command log** — every git command lazygit ran ⭐ |
| `x` | open the menu · `q` quit |

**`@` is the bridge for me:** it shows the plain-git equivalent of everything lazygit does, so any human action is reproducible as a script.

## Custom commands ⭐

`~/.config/lazygit/config.yml` binds arbitrary shell to keys, with prompts and repo context:

```yaml
customCommands:
  - key: '<c-r>'
    context: 'commits'
    command: 'hunk show {{.SelectedLocalCommit.Sha}}'
    output: terminal      # none | terminal | log | logWithPty | popup
    prompts:
      - type: 'input'     # input | menu | confirm | menuFromCommand
        title: 'Ref?'
```

`output: terminal` suspends lazygit and runs in the terminal; `popup` shows it inline. Template vars expose the selected file/commit/branch — which makes **`lazygit → hunk` bindable to a single key**, turning this habitat's most common git adjacency into one keystroke.

Config also covers `git.paging` (delta/hunk as pager), themes, and command overrides. Press `e` on the status panel to open it.

## Chains

**Feeds into:** [[hunk]] (review what you just staged), `git` (via `@`), [[gh-dash]] (push → PR).
**Inside nvim:** `Space g g` opens lazygit without leaving the editor ([[lazyvim]]).

Related: [[hunk]] · [[gh-dash]] · [[lazyvim]] · [[Tool Clusters]] · [[00 - Toolshed Index]] ·
[[Arena Practice Ground]] · [[Command Matrix]] · [[Tool Chaining Patterns]] ·
[[repo-fleet-status]]
