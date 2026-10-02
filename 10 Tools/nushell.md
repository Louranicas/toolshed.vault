---
tags: [toolshed, tool, workspace-1, shell, structured-data]
tool: nushell (nu)
version: 0.99.1
upstream: https://github.com/nushell/nushell
docs: https://www.nushell.sh/book/
workspace: W1 · pane w1:p7
agent_door: nu -c '<pipeline>'  ·  piped input needs: nu --stdin -c '$in | ...'
---

# nushell — the shell where pipes carry tables, not text

**428 built-in commands** in this build (`help commands | length`). The premise: every pipeline stage passes *structured* data — records, lists, tables — so you filter and project instead of parsing.

## Why it matters for chaining

Most habitat tools emit JSON (`herdr`, `gh --json`, `podman --format json`, `cargo --message-format json`). nu ingests all of them **without a parse step**, which makes it the natural glue between JSON-emitting tools and human-readable output.

> [!warning] `nu -c` does NOT read stdin — corrected 2026-09-02 in the arena
> Piping into `nu -c '…'` silently yields *nothing* (`from json` errors with "nothing doesn't support cell paths"). You must pass **`--stdin`** and start the pipeline with **`$in`**:
> ```bash
> herdr pane list | nu --stdin -c '$in | from json | get result.panes'   # ✅
> herdr pane list | nu -c 'from json | get result.panes'                 # ❌ silently empty
> ```
> Also: `open x.csv` **auto-types** columns — `where exit == "1"` matches nothing when the column is an int. Check with `open x.csv | first 1 | describe`.

```bash
herdr pane list | nu --stdin -c '$in | from json | get result.panes | select pane_id tab_id'
nu -c 'open Cargo.toml | get dependencies | transpose name spec'
nu -c 'gh pr list --json number,title,author | from json | where author.login != "me"'
nu -c 'ps | where cpu > 5 | select name cpu mem'
nu -c 'sys disks | where mount =~ STORAGE'
```

## Command families (the 428, grouped)

| Family | Representative commands |
|---|---|
| **Filters** | `where` `select` `get` `first` `last` `skip` `take` `sort-by` `group-by` `uniq` `reverse` `flatten` `transpose` `reduce` `each` `par-each` `zip` `window` `enumerate` `compact` `default` |
| **Formats** | `from json/yaml/toml/csv/tsv/xml/ods/xlsx` · `to json/yaml/toml/csv/md/text` · `open` / `save` (auto-detect by extension) |
| **Strings** | `str trim/replace/contains/starts-with/upcase/downcase/substring` `split row/column/chars` `parse` `format` `detect columns` |
| **Filesystem** | `ls` `cd` `cp` `mv` `rm` `mkdir` `open` `save` `glob` `watch` |
| **System** | `ps` `sys` (`host`/`disks`/`mem`/`cpu`/`net`/`temp`) `which` `exec` `run-external` |
| **Network** | `http get/post/put/delete/head/patch/options` |
| **DB** | `open x.sqlite`, `query db` |
| **Language** | `def` (custom commands) `export` `use` `module` `overlay` `let`/`mut`/`const` `if`/`match`/`for`/`while`/`loop` `try`/`catch` `error make` `do` closures |
| **Meta** | `help` `describe` `explain` `inspect` `debug` `metadata` `version` `explore` |

`par-each` gives free parallelism. `explore` is an interactive table viewer — pipe anything into it.

## Language features

- **Custom commands:** `def greet [name: string] { $"Hello ($name)" }` — typed params, flags, defaults
- **Closures:** `each { |it| $it.name }`
- **Modules & overlays:** namespaced reuse; `overlay use` for scoped environments
- **Hooks:** `pre_prompt`, `pre_execution`, `env_change` — event-driven automation in `config.nu`
- **Plugins:** separate binaries registered with `plugin add`
- **Error handling:** `try/catch`, `error make {msg: ...}`
- **String interpolation:** `$"text ($expr)"`

## Config

`~/.config/nushell/config.nu` (behaviour, keybindings, hooks, menus) and `env.nu` (PATH, env). Created with defaults on first run — done here 2026-09-01. History at `history.txt` (or SQLite if configured) — **separate from [[atuin]]**, which is why nu-pane commands don't appear in `atuin stats`.

## Chains

**Feeds from:** any JSON/CSV/TOML emitter — `herdr`, `gh --json`, `podman --format json`, `cargo --message-format json`, `mempalace` (text).
**Feeds into:** `to json` → `jq`/`jqp`, or `table` for humans.
`nu -c '…| to json'` is the cleanest way to hand structured data *back* to a JSON tool after a table-shaped transform.

> herdr's socket API speaks NDJSON, which is nushell's native food — `herdr pane list | from json` is a one-liner where jq needs a filter.

Related: [[jqp]] · [[herdr]] · [[Tool Chaining Patterns]] · [[00 - Field Findings]] ·
[[00 - Toolshed Index]] · [[Arena Practice Ground]] · [[Command Matrix]] ·
[[Documented Surface and Source]] · [[Tool Clusters]] · [[gh-dash]] · [[podman-tui]]
