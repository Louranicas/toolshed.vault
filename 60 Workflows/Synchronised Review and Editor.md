---
tags: [toolshed, workflow, nvim, hunk, W2, W3, synergy]
created: 2026-09-02
source: fedora-arena/scripts/goto-note.sh
chain: W3 review ⇄ W2 editor
---

# Synchronised Review ⇄ Editor

Takes note *N* from the live [[hunk]] session and moves **both** surfaces to it: the review pane
scrolls to the note, **and the running [[lazyvim|neovim]] opens that file at that line**. The
agent's attention, the reviewer's diff and the editor cursor stay in lockstep — across two
workspaces, driven from a third.

## Usage

```bash
just goto 0          # first note
just goto 2
just walk            # step through every note, both panes tracking
atuin scripts run goto -v repo=/path -v n=1
```

```
note[0] [clippy] crates/arena-core/src/stats.rs:11
  clippy::manual_is_multiple_of: manual implementation of `.is_multiple_of()`
  W3 ✓ hunk view moved
  W2 ✓ nvim → stats.rs:11
  W2   editor now at: stats.rs:11
```

## The unlock: nvim is already remote-controllable

**No `--listen` needed** — nvim serves an RPC socket by default at
`/run/user/$UID/nvim.<pid>.0` ([[00 - Field Findings|F19]]).

```bash
sock=$(ls /run/user/$(id -u)/nvim.*.0 | head -1)      # glob it — see below
nvim --server "$sock" --remote-send '<C-\><C-N>:edit /path/file.rs<CR>'
nvim --server "$sock" --remote-expr 'cursor(33,1)'
nvim --server "$sock" --remote-expr 'expand("%:p").":".line(".")'   # read state BACK
```

`--remote-expr` is the underrated half: the editor becomes **queryable**, so a script can verify
it landed where it intended rather than hoping.

## Three things that made this fiddly

1. **The socket belongs to nvim's child pid**, not the pid herdr reports as the pane's
   foreground process (10362 vs 10357). Glob for the socket; never derive it. ([[00 - Field Findings|F19]])
2. **A one-liner `:edit file<CR>:33<CR>` silently loses the jump** — LazyVim restores the last
   cursor position in a `BufReadPost` autocmd that fires afterwards. Split into `:edit`, a brief
   pause, then `cursor(N,1)`. ([[00 - Field Findings|F20]])
3. **`--remote-send zz` leaves a statusline artefact.** Harmless (`mode()` is `n`), but send view
   commands as `--remote-expr 'execute("normal! zz")'` for a clean state. ([[00 - Field Findings|F21]])

## Why this matters

The habitat's division of labour was *"your editor, my diffs"* — two surfaces that never met.
This makes the boundary crossable **in the direction that was missing**: an agent can now say
"look here" and the human's editor is already there. Combined with
[[Bridge - Diagnostics to Review]], the whole path is closed:

```
cargo diagnostic → inline note in the human's diff → cursor in the human's editor
```

Related: [[lazyvim]] · [[hunk]] · [[Bridge - Diagnostics to Review]] · [[00 - Workflows]] ·
[[00 - Toolshed Index]] · [[Shape-Directed Tool Chaining]]
