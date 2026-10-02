---
tags: [toolshed, tool, workspace-1, primitive]
tool: fzf
version: 0.74.3
upstream: https://github.com/junegunn/fzf
workspace: W1 · shell-wide (bindings in every pane)
agent_door: fzf --filter=<query>  (non-interactive ranking)
---

# fzf — the universal fuzzy filter

The **composable primitive** under half this toolchain. Pipe any newline-separated list in, get the selection out. Not a pane resident — it is a verb every other tool borrows.

## Invocation surface

```bash
cmd | fzf                          # basic
fzf --multi                        # -m, Tab/Shift-Tab to mark several
fzf --filter=QUERY                 # ⭐ NON-INTERACTIVE: rank + print, no UI (the agent door)
fzf --query=QUERY                  # pre-seed the interactive prompt
fzf --select-1 --exit-0            # -1 -0: auto-pick a lone match, exit silently on none
fzf --print0 --read0               # NUL-delimited I/O for filenames with newlines
fzf --preview 'bat --color=always {}' --preview-window=right:60%:wrap
fzf --bind 'ctrl-r:reload(rg --files)' --bind 'enter:become(nvim {})'
fzf --height=40% --layout=reverse --border
fzf --tmux center,80%              # popup mode
```

Placeholders inside `--preview`/`--bind`: `{}` selection · `{1}`,`{2}` fields · `{q}` current query · `{+}` all selections · `{n}` index.

**Actions worth knowing** for `--bind`: `reload(cmd)` (live re-source — turns fzf into an interactive front-end for *any* command), `become(cmd)` (replace fzf with cmd), `execute(cmd)` / `execute-silent`, `change-prompt`, `toggle-preview`, `accept`, `abort`, `put`.

## Search syntax (inside the picker)

| Pattern | Meaning |
|---|---|
| `sbtrkt` | fuzzy match |
| `'wild` | exact substring |
| `^music` | prefix · `.mp3$` suffix |
| `!fire` | **negate** |
| `a \| b` | OR |

Space-separated terms are AND.

## Shell bindings (active in every habitat pane)

`Ctrl+T` insert fuzzy-picked path · `Alt+C` cd into picked dir · `Ctrl+R` history — **but [[atuin]] wins here**, loaded after fzf in `.bashrc`, which is deliberate.

## Env config

`FZF_DEFAULT_COMMAND` (e.g. `fd --type f --hidden --exclude .git`) · `FZF_DEFAULT_OPTS` · `FZF_CTRL_T_COMMAND` · `FZF_ALT_C_COMMAND`.

## Chains — fzf is almost pure chain

```bash
git branch | fzf | xargs git switch
podman ps --format '{{.Names}}' | fzf | xargs -r podman logs
atuin search --cmd-only --exit 0 | fzf | bash          # rerun a proven command
just --summary | tr ' ' '\n' | fzf | xargs just         # (or just --choose, which embeds fzf)
rg --files | fzf -m --print0 | xargs -0 nvim
```

**Feeds from:** anything that prints lines. **Feeds into:** `xargs`, `$( )`, `become()`.
**Agent note:** `--filter` makes fzf scriptable — ranking without a UI. For pure search I use `rg`/`fd` directly; fzf's value to me is as the *ranking* function inside a pipeline.

Related: [[television]] · [[atuin]] · [[just]] · [[Tool Chaining Patterns]] ·
[[00 - Toolshed Index]] · [[Arena Practice Ground]] · [[Bridge - Coverage to Review]] ·
[[Command Matrix]] · [[Documented Surface and Source]] · [[Tool Clusters]] · [[podman-tui]] ·
[[yazi]]
