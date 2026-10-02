---
tags: [toolshed, tool, workspace-4, monitoring]
tool: bottom (btm)
version: 0.12
upstream: https://github.com/ClementTsang/bottom
workspace: W4 · pane w1:pA
agent_door: habitat pane bottom  (pane-readable vitals) · ps/free/df for scripts
updated: 2026-09-06
---

# bottom (btm) — system vitals, readable from the pane

Graphical process/resource monitor. Its value to an agent is **not** its CLI — it is that a resident pane is *already computing* live vitals, including per-agent `claude`/`codex`/`grok` processes, so `habitat pane bottom` is a zero-cost fleet resource check during multi-agent work.

## Widgets

CPU (per-core graph) · Memory + swap · Network (RX/TX) · Disk usage · Temperatures · Processes · Battery.

## Keys

| Key | Action |
|---|---|
| `?` | help · `q`/`Ctrl+c` quit |
| `Tab`/arrows | move between widgets · `Enter` select |
| `e` | **expand** focused widget full-screen |
| `f` | **freeze** display for inspection ⭐ |
| `dd` | kill selected process (confirm) |
| `t` / `T` | tree view / toggle |
| `%` / `s` | memory as percent / sort menu |
| `/` | search processes · `n`/`N` next/prev match |
| `c`,`m`,`p`,`n` | sort by CPU / mem / PID / name |
| `+`/`-` | zoom time axis · `g`/`G` top/bottom |

## CLI options

`-b`/`--basic` (compact, no graphs) · `--process_command` (full command lines) · `-t`/`--tree` · `-g`/`--group_processes` · `--default_widget_type` · `-r`/`--rate <ms>` · `--celsius`/`--fahrenheit` · `-C`/`--config <path>` · `--battery` · `--enable_gpu` · `--time_delta` · `--dot_marker` · `--regex`/`--case_sensitive`/`--whole_word` for the process filter.

## Config

`~/.config/bottom/bottom.toml` — `[flags]`, `[colors]` (theming), and `[[row]]`/`[[row.child]]` **custom layouts**: the widget grid is fully user-defined, so a habitat layout could show only CPU + processes filtered to agent binaries.

## Chains

**Feeds into:** me, via `habitat pane bottom`. For scripted checks I use `ps`/`free`/`df` directly — btm is a *display*, not a data source.
`yazi → podman-tui → tv` shows up as an adjacency triple in this habitat's history: browse files, check containers, jump elsewhere.

## Rust performance practice

Pair the resource observations described here with [[40 Reference/Perfecting Rust - Performance Engineering#Profile to explain the cost|Rust profiling methods]] and [[40 Reference/Perfecting Rust - Performance Engineering#Keep four measurements separate|the allocation and footprint distinctions]]. [[40 Reference/rust-mastery/2026-09-06/README#Results to inspect|The lab reports]] show how cumulative allocation and peak tracked heap answer different questions.

Related: [[podman-tui]] · [[herdr]] · [[Tool Clusters]] · [[00 - Toolshed Index]] ·
[[Command Matrix]] · [[Tool Chaining Patterns]] · [[yazi]]
