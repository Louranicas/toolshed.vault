---
tags: [toolshed, tool, workspace-2, editor]
tool: LazyVim on Neovim
version: nvim 0.12 · LazyVim starter
upstream: https://www.lazyvim.org
workspace: W2 · pane w1:p8
agent_door: (human-first) — I edit files directly; nvim --headless / --server for automation
---

# LazyVim — the editor pane

A curated Neovim distribution (lazy.nvim + LSP + Telescope + neo-tree + which-key). **Leader = `Space`.**

## Essential keys

| Key | Action |
|---|---|
| `Space Space` | find files (Telescope) |
| `Space /` | live grep across project |
| `Space e` | file explorer (neo-tree) |
| `Space g g` | **lazygit inside nvim** ([[lazygit]] synergy) |
| `Space s k` | search keymaps — the self-documenting escape hatch |
| `Space c a` | code action · `Space c r` rename |
| `g d` / `g r` / `K` | definition / references / hover |
| `] d` / `[ d` | next/prev diagnostic |
| `Space b d` | close buffer · `Space q q` quit |
| `Ctrl+h/j/k/l` | window nav (herdr's `ctrl+b` prefix stays clear) |

`:Lazy` plugin manager · `:Mason` LSP/formatter installer · `:LazyHealth` checkup · `:LazyExtras` opt-in extras.

## Headless / remote — the automation surface

```bash
nvim --headless -c '<ex command>' -c 'qa'      # scripted edits, no UI
nvim --headless +'lua print(vim.version())' +q
nvim --listen /tmp/nvim.sock                   # expose an RPC socket
nvim --server /tmp/nvim.sock --remote-send ':e file.rs<CR>'
nvim --server /tmp/nvim.sock --remote          # open a file in the RUNNING instance ⭐
```

`--server`/`--remote` is the unexplored integration: *"open the file I just edited in your W2 nvim"* (Future Plugin Roadmap #11 in the herdr vault). It needs the pane's nvim started with `--listen`.

## Config

`~/.config/nvim/lua/plugins/*.lua` (add specs) · `lua/config/options.lua`, `keymaps.lua`, `autocmds.lua`. Installed from the upstream `LazyVim/starter` with `.git` removed.

## Chains

**Division of labour:** *your editor, my diffs*. I don't drive nvim interactively — I edit files directly and you review. The meeting points are [[hunk]] and reviewr.
`tv → nvim` (find then edit) is a live adjacency in this habitat's history.

Related: [[lazygit]] · [[hunk]] · [[television]] · [[00 - Toolshed Index]] · [[Command Matrix]] ·
[[Synchronised Review and Editor]]
