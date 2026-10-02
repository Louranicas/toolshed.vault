---
tags: [toolshed, tool, spine, multiplexer, api]
tool: herdr
updated: 2026-09-06
version: 0.8.2 (protocol 20)
upstream: https://herdr.dev
workspace: the spine — every pane lives inside it
agent_door: the entire CLI + NDJSON socket   ⭐
---

# herdr — the multiplexer that is also an API

## Habitat tab shortcut — 2026-09-06

In Ghostty on Fedora Kinoite, **Ctrl+Alt+End → next Herdr tab**, wrapping within the current
workspace. Ctrl+B, then N remains available. Herdr 0.8.2 does not accept `End` in its configurable
key parser, so Ghostty translates the chord using `csi:110;7u`; Herdr binds the resulting
Ctrl+Alt+N to `next_tab`. Both configs validated and were live-reloaded without restarting panes.

The mapping affects Herdr's inner tabs. Ghostty's outer tabs retain their existing shortcuts.
Outside Herdr, Ghostty sends Ctrl+Alt+N to the foreground terminal application.
[[40 Reference/herdr-keybindings/2026-09-06/README|Configuration, verification limits and rollback]].

Not one of the 16 workspace services: the **substrate** they run in. Everything is scriptable over a Unix-domain socket speaking newline-delimited JSON, and the `herdr` CLI is a thin wrapper over it.

## Transport

Socket `~/.config/herdr/herdr.sock` (named sessions: `~/.config/herdr/sessions/<name>/herdr.sock`). Resolution order: `--session` flag → `$HERDR_SOCKET_PATH` → `$HERDR_SESSION` → default.

```bash
printf '%s\n' '{"id":"1","method":"ping","params":{}}' | socat - UNIX-CONNECT:$HOME/.config/herdr/herdr.sock
herdr api schema --json          # ⭐ the authoritative contract: every method, response, event
```

## Command groups

`workspace` · `tab` · `pane` · `agent` · `session` · `worktree` · `plugin` · `notification` · `integration` · `config` · `channel` · `api` · `server`

### pane — the workhorse
`list` `current` `get` `layout` `process-info` `neighbor` `edges` `focus` `resize` `zoom` **`read`** `rename` `input` `split` `swap` `move` `close` **`send-text`** **`send-keys`** **`wait-output`** **`run`** `report-agent` `report-agent-session` `release-agent` `report-metadata`

```bash
herdr pane run <id> "cmd"                       # atomically types + Enter
herdr pane read <id> --source visible|recent|recent-unwrapped|detection --lines N [--format ansi]
herdr pane wait-output <id> --match TEXT | --regex RE [--timeout MS]
herdr pane split --pane <id> --direction right|down --cwd PATH --no-focus
herdr pane process-info --pane <id>             # ⭐ foreground_processes[].name — idle vs busy
```

`process-info` is the primitive behind idempotent respawn: a pane at a prompt reports `["bash"]`.

### agent — lifecycle-aware
`list` `get` `wait` `prompt` `start` `explain` `read` `send-keys` `attach`
States: `working` · `blocked` (approval UI detected) · `done` · `idle` · `unknown`.
```bash
herdr agent start reviewer --kind codex --pane <id> -- <agent args>
herdr agent prompt reviewer "…" --wait --timeout 120000
herdr agent wait reviewer --until blocked
herdr agent explain <target> --json    # WHY herdr thinks the state is X
```

### plugin
`install` `link` `enable` `disable` `list` `config-dir` `action list|invoke` `log list` `pane`
⚠️ **action id first, `--plugin` after**: `herdr plugin action invoke respawn --plugin local.habitat-services`

### others
`layout export/apply` (declarative layouts as dotfiles) · `worktree create/open/remove` · `events subscribe/wait` · `server stop|reload-config` · `config check|reset-keys`.

## Plugin manifest surface

`herdr-plugin.toml`: `[[build]]` · `[[panes]]` (placement `zoomed|split|overlay|popup|tab`) · `[[actions]]` (`contexts`, bindable) · `[[events]]` (`on = "worktree.created"` …) · **`[[startup]]`** (once per session start, *after* restore — what `local.habitat-services` uses to respawn the cockpit). Injected env: `HERDR_SOCKET_PATH`, `HERDR_BIN_PATH`, `HERDR_PLUGIN_ID`, `HERDR_PLUGIN_CONFIG_DIR`, `HERDR_PLUGIN_STATE_DIR`, `HERDR_PLUGIN_EVENT`.

## Chains — herdr is the chaining *medium*

Every other tool becomes agent-reachable through `pane read` even when it has no CLI. That is the whole basis of the two-door model in the habitat bridge: **agent door** where one exists, **pane read** always.

```bash
herdr pane list | jq '.result.panes[] | select(.tab_id=="w1:t4")'
herdr pane list | jqp                    # W5 pT
herdr pane list | nu -c 'from json | get result.panes | table'
```

Related: [[jqp]] · [[nushell]] · [[Tool Chaining Patterns]] · [[Tool Clusters]] ·
[[00 - Toolshed Index]] · [[Command Matrix]] · [[Habitat Reactor]] · [[bacon]] · [[bottom]]
