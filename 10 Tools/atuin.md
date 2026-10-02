---
tags: [toolshed, tool, workspace-1, memory, scripting]
tool: atuin
updated: 2026-09-06
version: 18.12.1
upstream: https://github.com/atuinsh/atuin
docs: https://docs.atuin.sh
workspace: W1 · pane w1:pG
agent_door: habitat history <term>
---

# atuin — shell history as a queryable database (+ a scripting engine)


> **⚓ Code anchor** — `$REPOS/atuin/crates/atuin/src/command/client/scripts.rs:33` · expects `pub script: Option<PathBuf>`
> `--script` takes a **file path**, not a script body. The type is the proof; `--help` is not.
> *Verified 2026-09-03 · re-check `just doc-anchors`; this note updates when the code does.*

SQLite-backed shell history recording **exit code, cwd, duration, session and hostname** per command. But the history search is only the front door: 18.x ships `scripts`, `kv`, `dotfiles` and a `store` — atuin is really a **synced, end-to-end-encrypted personal data store** that happens to start with history.

## Complete command surface (18.12.1)

| Command | What it does |
|---|---|
| `history` | manipulate history: `start`/`end`/`list`/`last`/`init-store`/`prune`/`dedup` |
| `import` | ingest pre-atuin history: `auto`, `bash`, `zsh`, `fish`, `nu`, `resh`, `replxx`, `xonsh`, `zsh-hist-db` |
| `stats` | most-used commands; accepts a period (`day`, `week`, `month`, `year`, `all`) |
| `search` | interactive TUI **and** non-interactive query (the agent door) |
| **`scripts`** | **`new` · `run` · `list` · `get` · `edit` · `delete`** — see below |
| `kv` | `set` / `get` / `list` / `delete` — small key/value pairs, synced |
| `dotfiles` | `alias` and `var` management, synced across machines |
| `store` | `status` / `purge` / `push` / `pull` / `rebuild` / `verify` — the sync data store |
| `sync` · `login` · `logout` · `register` · `account` · `key` · `status` | sync lifecycle (optional; self-hostable) |
| `init` | print the shell init script (`bash`/`zsh`/`fish`/`nu`/`xonsh`) |
| `doctor` | diagnose common issues — first stop when Ctrl+R stops working |
| `daemon` | *experimental* background daemon |
| `wrapped` | year-in-review stats |
| `default-config` | print a fully commented `config.toml` |
| `info` | dotfile locations and env vars |
| `uuid` · `gen-completions` · `contributors` | utilities |

## ⭐ `atuin scripts` — the feature that changes how workflows are built

Turn any command, or the **last N commands you actually ran**, into a named, tagged, parameterized, synced script.

```bash
# capture what you just did — the killer move
atuin scripts new deploy --last 3 -t infra -d "Deploys the prod stack"
atuin scripts new quickfix --last          # just the last command
atuin scripts new x --last 5 --no-edit     # skip the editor

# author directly
atuin scripts new hello-py --shebang '/usr/bin/env python3'
atuin scripts new build --script ./scripts/build.sh   # ⚠️ --script takes a FILE PATH, not inline text

atuin scripts run deploy                   # prompts for any missing variables
atuin scripts run deploy -v env=production -v region=eu-west-1
atuin scripts list
atuin scripts get deploy            # full record
atuin scripts get deploy -s         # just the executable script + shebang
atuin scripts edit deploy --rename ship -t infra,prod
atuin scripts delete deploy -f
```

> [!warning] Two traps found by running it (arena, 2026-09-02)
> 1. **`--script` is a file path, not inline content.** `--script 'echo hi'` fails with `No such file or directory (os error 2)` and a panic at `scripts.rs:264`. Write the body to a file first. (The help text is just `--script <SCRIPT>` with no description.)
> 2. **minijinja renders the whole body — including shell comments.** Any `{{ … }}` collides: **Go-template CLIs cannot be embedded**. `podman ps --format '{{.Names}}'` dies with ``syntax error: unexpected `.` ``, and so does the same text inside a `#` comment. Use `--format json | jq` instead, or `{% raw %}`.

**Templating:** script bodies are **minijinja** templates. `{{ env }}` in the body becomes a runtime prompt, or is filled by `-v env=…`. Full minijinja syntax is available — conditionals, loops, filters — so one script covers a family of invocations instead of five near-duplicate aliases.

**Shebang:** default `bash`, but `-s '/usr/bin/env python3'` (or nu, or anything) makes atuin a polyglot snippet runner.

**Sync:** scripts ride atuin's end-to-end-encrypted sync, so they follow you to any machine that logs in. (Sharing with *other people* is on the roadmap, not shipped.)

> [!tip] Why this matters here
> `--last N` closes the loop between *doing* and *automating*. Work something out interactively in a pane, then promote the exact sequence to a named script without retyping it. It is the natural capture point for every recipe in [[Workflow Recipes]].

## Non-interactive search — the agent door

```bash
atuin search --cmd-only <term>                    # bare commands, no formatting
atuin search --cwd . --limit 10                   # this directory's history
atuin search --exit 0 --after "1 day ago" cargo   # only successful cargo runs, last 24h
atuin search --before "2026-09-01" --exclude-exit 0 --format "{time} {command}"
atuin history list --cmd-only --print0            # NUL-terminated, multiline-safe
atuin stats day
```

**Search-mode precision (historical Arena sample):** the query `nu` returned **19** results fuzzy,
**3** full-text, **1** prefix. Installed 18.12.1 help and a real query were checked on 2026-09-06:
the flag spelling is **`--search-mode full-text`**. Choose the mode for the question; these old
result counts are not a current inventory.

Filter flags worth knowing: `--exit` / `--exclude-exit`, `--exclude-cwd`, `--before` / `--after`, `--limit`, `--offset`, `--search-mode` (`prefix|full-text|fuzzy|skim`), `--filter-mode` (`global|host|session|directory|workspace`), `--format` (`{command} {directory} {duration} {user} {host} {time} {exit} {relativetime}`), `--delete` / `--delete-it-all`, `--reverse`, `--print0`.

`--print0` + `--cmd-only` preserves record boundaries for a NUL-aware consumer. It does not make
historical commands safe to execute. `global` searches the current database's contexts, not
separate archives across drives; see [[50 Field Notes/lukes workflows#What Atuin reveals, and what it cannot tell us|coverage and interpretation]].

## Interactive keys

`Ctrl+R` full search · `Ctrl+↑` (or `↑`) directory-filtered · `Tab` cycle filter mode · `Ctrl+O` inspect a command's stats · `Enter` run · `Tab`-to-edit. Search syntax: `-` prefix negates, and the mode is switchable live. **18.x added full custom keybinding support for the search TUI.**

## Config

`~/.config/atuin/config.toml` — `filter_mode`, `search_mode`, `inline_height`, `style`, `show_preview`, `enter_accept`, `workspaces`, `history_filter` (regex exclusions — **the place to stop secrets being recorded**), `secrets_filter`, `sync_frequency`. Print a fully commented default with `atuin default-config`. Data: `~/.local/share/atuin/history.db`.

## Chains

**Feeds from:** every shell in every pane (via `atuin init bash` + bash-preexec).
**Feeds into:** `fzf` / `tv` (pick a past command) · `atuin scripts new --last` (promote to script) · [[mempalace]] (shell recall → knowledge recall — the most common adjacency in this habitat's own history).

```bash
atuin search --cmd-only --exit 0 cargo | fzf                # display a candidate for review
atuin search --cmd-only --cwd . | tv                       # directory history through television
```

Inspect the selected command against today's task, paths and resource policy before deciding
to run it. A recorded exit zero is not current verification. Do not pipe history into an
interpreter. The revised [[20 Chaining/Workflow Recipes|workflow recipes]] use reviewed capture
and aggregate analysis without exporting raw history into `/tmp`.

## ⚠️ Upstream has an AI/agent surface this build does not

atuin has become an **agent platform**, and the installed Fedora RPM (`atuin-18.12.1-1.fc44`) predates all of it. Verified locally 2026-09-02 — `atuin mcp` and `atuin setup` both return *"unrecognized subcommand"*.

| Feature | Upstream | Here (18.12.1) |
|---|---|---|
| `scripts` (snippets, minijinja, sync) | ✅ | ✅ **available** |
| **`atuin mcp`** — MCP server exposing history as native agent tools | ✅ | ❌ missing |
| **Command output capture** (`atuin_output`) | ✅ needs daemon + pty-proxy | ❌ |
| **`atuin ai`** — natural language → shell, `?` on an empty prompt | 18.13 | ❌ |
| **`atuin hex`** — PTY proxy, popups without clearing scrollback | 18.13 | ❌ |
| `search_mode = "daemon-fuzzy"` in-memory index | 18.13 | ❌ |
| `switch-context` | 18.13 | ❌ |
| Agent hooks tagging command **author** (Claude Code, Codex, OpenCode, pi) | installer-provided | ❌ not configured |

**What the MCP server would give me** — two read-only tools, all data staying local:

- `atuin_history` — fuzzy history search with filters for *mode* (global/host/directory/workspace/session), failed-only, and **author** (your commands vs. a specific agent's). No extra setup; reads the DB directly.
- `atuin_output` — retrieves **captured terminal output** for a history ID, with line ranges. Requires the daemon **and** pty-proxy running.

```bash
claude mcp add atuin -- atuin mcp        # the whole setup, once atuin is new enough
```

Author-tagging is the quietly important part: it lets an agent distinguish *your* commands from *its own*, which is what makes "how did we do this before" answerable rather than self-referential.

**Upgrade path:** the Fedora package lags upstream. `cargo install atuin` or the upstream installer would deliver it — at the cost of moving atuin from the dnf lane to the `$HOME` lane (which, per the habitat's durability audit, is actually the *more* durable lane). Not done unilaterally: it changes package provenance and `toolbox-bootstrap` would need to match. **Open decision.**

## Habitat notes

Installed via dnf in the toolbox (**disposable layer** — reinstalled by `toolbox-bootstrap`); the database in `~/.local/share/atuin` is `$HOME` and durable. `atuin import auto` was run 2026-09-02, folding 59 pre-atuin bash commands into the store (97 → 156). Sync is **not** configured — everything is local-only, which matches the habitat's local-first posture; self-hosting is the option if a second machine ever joins.

Related: [[fzf]] · [[mempalace]] · [[Tool Chaining Patterns]] · [[Most-Used Tools]] ·
[[00 - Toolshed Index]] · [[Command Matrix]] · [[Documented Surface and Source]] · [[Runbooks]] ·
[[Tool Clusters]] · [[nushell]] · [[television]]
