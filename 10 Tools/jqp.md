---
tags: [toolshed, tool, workspace-5, json]
tool: jqp (+ jq)
version: jqp 0.8.0 · jq 1.8.1
upstream: https://github.com/noahgorstein/jqp
workspace: W5 · pane w1:pT (seeded with live herdr JSON)
agent_door: jq  (jqp is the human query-authoring surface)
---

# jqp — an interactive playground for jq

Ends the write-run-tweak-rerun jq loop: query pane on top, live output, input browser.

```bash
jqp -f data.json                 # open a file
cat data.json | jqp              # or stdin  ⭐ needs one or the other — jqp alone has no input
jqp -f x.json -q '.items[]'      # seed a query
jqp -t <theme>  ·  --config ~/.jqp.yaml
herdr pane list | jqp            # what W5 pT runs — the habitat's own live API as the subject
```

Keys: `Enter` run · `Tab` switch section · `Ctrl+y` copy query · `Ctrl+s` save output · `Ctrl+t` hide input panel · `?` help.

## jq — the engine (the agent door)

```bash
jq '.result.panes[] | {pane_id, tab_id}'          # project
jq -r '.[] | "\(.name) \(.status)"'               # raw strings
jq -s 'add'  ·  jq -c  ·  jq -n  ·  jq --arg k v  ·  jq --argjson k '{}'
jq 'map(select(.exit == 0)) | group_by(.cwd) | map({dir: .[0].cwd, n: length})'
jq --slurpfile / --rawfile / --tab / --indent N / -e (exit status from output)
```

Core verbs: `select` `map` `group_by` `sort_by` `unique_by` `add` `length` `keys` `to_entries`/`from_entries` `with_entries` `paths` `getpath`/`setpath` `del` `env` `@csv`/`@tsv`/`@json`/`@base64` · `//` alternative · `?` error suppression · `reduce`/`foreach` · user `def`s.

## jq vs [[nushell]]

Same job, different shape. jq is a *stream* language over JSON; nu is a *table* language over many formats. For deep JSON reshaping jq wins; for tabular work, joins and `where` filters over mixed sources, nu is cleaner. Both are installed; `nu -c '… | to json'` hands data back to jq.

## Chains

**Feeds from:** every `--json` emitter — [[herdr]] (NDJSON socket API), [[gh-dash]] (`gh … --json`), [[podman-tui]] (`--format json`), `cargo --message-format json`, [[just]] (`--dump --dump-format json`).
**The handoff:** you prototype a filter in jqp, `Ctrl+y` copies it, and it lands verbatim in a script or a herdr Quick Action.

Related: [[nushell]] · [[herdr]] · [[gh-dash]] · [[Tool Chaining Patterns]] ·
[[00 - Toolshed Index]] · [[Arena Practice Ground]] · [[Command Matrix]] · [[Tool Clusters]]
