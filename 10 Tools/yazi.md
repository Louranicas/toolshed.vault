---
tags: [toolshed, tool, workspace-4, files]
tool: yazi
version: copr lihaohong/yazi
upstream: https://yazi-rs.github.io
workspace: W4 · pane w1:pN (on repos/)
agent_door: (human-first) — fd / ls / rg
---

# yazi — blazing file manager with async previews

## Keys

**Navigate:** `k`/`j` or arrows · `h` parent · `l` enter · `K`/`J` seek preview ±5 · `gg`/`G` top/bottom · `gt` trash · `z` fzf jump · `Z` zoxide jump
**Select:** `Space` toggle · `v`/`V` visual / unset mode · `Ctrl+a` all · `Ctrl+r` invert · `Esc` cancel
**Files:** `o`/`O` open / open-interactively · `Enter` open · `Tab` info · `y` copy · `x` cut · `p`/`P` paste / overwrite · `d` trash · `D` **permanent delete** · `a` create · `r` rename · `.` toggle hidden
**Links:** `-` symlink (absolute) · `_` symlink (relative) · `Ctrl+-` hardlink
**Copy path:** `c` then `c` path / `d` dir / `f` filename / `n` stem
**Shell:** `;` async command · `:` blocking command
**Search:** `f` filter · `/`,`?` find next/prev · `n`/`N` cycle · `s` search by name (**fd**) · `S` search by content (**ripgrep**) · `Ctrl+s` cancel
**Sort:** `,` then `m`/`b`/`e`/`a`/`n`/`s`/`r` = modified / birth / extension / alphabetical / natural / size / random (capital = reverse)
**Tabs:** `t` new · `1`–`9` switch · `[`/`]` prev/next · `{`/`}` swap · `Ctrl+c` close
**Tasks:** `w` task manager · `F1`/`~` help

## The `y` shell wrapper ⭐

Plain `yazi` cannot change your shell's cwd on exit. The documented wrapper (shipped for bash, fish, nu, POSIX, elvish, PowerShell, xonsh) makes `y` **cd to wherever you ended up**; `q` quits with cd, `Q` quits without. Worth adding to `.bashrc` here — currently the pane runs bare `yazi`, so its navigation is display-only.

## Config

`~/.config/yazi/` *(user-authored; absent until you create it)* — `yazi.toml` (behaviour, openers, previewers), `keymap.toml` (full rebind; the default is published in the repo), `theme.toml`. **Plugins (beta)** are Lua — previewers, git-status flags per file, custom commands. **Flavors (beta)** are shareable colour schemes.

## Chains

`s`/`S` delegate to **fd** and **ripgrep** — the same engines I use directly, which is why the division of labour is clean: yazi is your visual front-end to the tools I call as CLIs.
**Feeds into:** `;`/`:` shell commands on the selection; the `y` wrapper feeds cwd back to the shell.

Related: [[television]] · [[fzf]] · [[bottom]] · [[00 - Toolshed Index]] · [[Command Matrix]] ·
[[Tool Chaining Patterns]] · [[Tool Clusters]]
