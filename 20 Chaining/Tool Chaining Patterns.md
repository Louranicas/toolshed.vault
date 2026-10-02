---
tags: [toolshed, chaining, patterns, workflows]
created: 2026-09-02
updated: 2026-09-06
---

# Tool Chaining Patterns — the nine shapes

**Navigation:** [[40 Reference/Command Matrix#Composition and verification routes|Command Matrix ⇄ composition routes]] · [[00 - Toolshed Index|Toolshed master index]]. Choose a filter, JSON, watcher, capture, discovery or verification pattern.

The original [[Most-Used Tools]] sample contained 156 records. It motivated these composition
patterns; it is not a current account of all habitat activity. The September 6 review applies
[[50 Field Notes/lukes workflows|Luke's measured workflow findings]] and separates historical
examples from current source checks. Use [[60 Workflows/00 - Workflows#Daily operating cycle — reviewed 2026-09-06|the operating cycle]] when choosing which patterns to keep running.

---

## P1 · The filter chain — `producer | picker | consumer`

The classic. Any command that emits lines becomes interactive.

```bash
git branch | fzf | xargs git switch
podman ps --format '{{.Names}}' | fzf | xargs -r podman logs
repo-fleet-status | awk '$3 ~ /±/ {print $1}' | fzf | xargs -I{} sh -c 'cd $REPOS_DIR/{} && lazygit'
atuin search --cmd-only --exit 0 cargo | fzf               # display a candidate for review
```

An exit-zero history record is not permission or proof that a command is suitable now. Inspect
the selected text and current project context; never pipe recall into an interpreter. For a
guarded repository picker, see [[20 Chaining/Workflow Recipes#R6 · Jump to the dirty repo and operate it (P1)|R6]].

**Non-interactive variant** (scriptable): `fzf --filter=QUERY` ranks without a UI; `--select-1 --exit-0` auto-picks a lone match.

---

## P2 · The JSON chain — `emitter --json | reshaper | sink`

Nearly every tool here emits JSON. Two reshapers, chosen by shape of the problem: **[[jqp]]/jq** for stream surgery, **[[nushell]]** for tables and joins.

```bash
herdr pane list | jq '.result.panes[] | select(.tab_id=="w1:t4") | .pane_id'
gh pr list --json number,title,statusCheckRollup | nu -c 'from json | where statusCheckRollup != []'
just --dump --dump-format json | jq '.recipes | keys'
podman ps --format json | nu -c 'from json | select Names State'
(
  set -o pipefail
  cargo check --message-format json \
    | jq -r 'select(.reason=="compiler-message") | .message.rendered'
)
```

Preserve the producer's failure status when a pipeline supplies a verdict. A data default such
as `// []` fills a missing value; it does not turn failed collection into valid evidence.

**Emitters worth remembering:** `herdr … ` (NDJSON everywhere) · `gh … --json` · `podman --format json` · `just --dump --dump-format json` · `cargo --message-format json` · `hunk session … --json` · `bottom` (no — display only).

---

## P3 · The watch chain — resident watcher + `pane read`

A **TUI already running in a pane may have computed the answer**. Reading it can avoid another
build, but the watcher remains a resident workload. Check project, revision and completion state;
screen contents alone are not a fresh success receipt. Keep one useful loop per worktree and
include any separate [[60 Workflows/Autonomous Triggers#Probe cost and lifecycle|polling probe]] in its resource budget.

```bash
habitat pane bacon      # current Rust verdict — no rebuild
habitat pane bottom     # live vitals incl. per-agent processes
habitat pane gh-dash    # the PR radar as the human sees it
herdr pane wait-output w1:pJ --regex "(error|warning|Finished)" --timeout 300000
```

This is why the human-first tools ([[bottom]], [[yazi]], [[lazygit]], [[television]]) are still agent-reachable: **`herdr pane read` is a universal door.**

---

## P4 · The capture chain — do it, then promote it ⭐

The loop [[atuin]] Scripts closes: work something out interactively, then promote **the exact sequence you just ran** into a named, parameterised, synced script — without retyping it.

```bash
# Capture a candidate, then inspect it before any run:
atuin scripts new ship --last 3 -t release -d "Tag, build, publish"
atuin scripts get ship -s
# Only after reviewing the captured body for the intended task:
atuin scripts run ship -v version=0.3.0
```

Bodies are **minijinja** templates, so `{{ version }}` becomes a prompt or a `-v` flag. `--shebang '/usr/bin/env python3'` makes it polyglot. **Every recipe in [[Workflow Recipes]] is a candidate for this treatment** — that is how a pattern becomes a habit.

---

## P5 · The two-door chain — data or picture

Every service answers two different questions, and picking the right door matters.

| Question | Door |
|---|---|
| "What is the value?" | `habitat q <svc>` — the non-interactive CLI |
| "What is on screen?" | `habitat pane <svc>` — the live TUI |

```bash
habitat q gh-dash pr list --json number,title    # data I can compute on
habitat pane gh-dash                             # what YOU are looking at right now
```

The second is how I answer *"what are you seeing?"* — a question the first door cannot address.

---

## P6 · The escape chain — toolbox → host

On Kinoite the toolbox is a container; anything managing the **host** or the **containers themselves** escapes outward.

```bash
flatpak-spawn --host podman ps                       # inspect the host container engine
flatpak-spawn --host rpm-ostree status
flatpak-spawn --host systemctl --user status podman.socket
toolbox run --container fedora-toolbox-44 <cmd>      # the reverse: host → toolbox
```

The habitat registry encodes this per-service so it never has to be remembered ad hoc.

---

## P7 · The discovery chain — orient before acting

Never invent commands in an unfamiliar repo; ask it.

```bash
just --summary                       # what can I do here?
just --dump --dump-format json       # the whole justfile as data
just -n <recipe>                     # dry-run: print without executing
bacon --list-jobs                    # what checks exist
gh repo view --json description,topics
mempalace wake-up                    # ~600-900 token orientation brief
```

Inspect unfamiliar definitions before using their preview modes. A flag named `--dry-run` does
not promise zero effects: the installed [[60 Workflows/Runbooks]] executor still runs preconditions,
and [[60 Workflows/Autonomous Triggers]] still executes probes. A successful preview is not a
successful workload. Treat old recalled commands and notes as evidence, not activation instructions.

---

## P8 · The session chain — write into the human's view ⭐

[[hunk]] and [[tuicr]] both expose a session API, so review is **bidirectional** rather than a report I hand over.

```bash
hunk session list --json
hunk session comment list --repo . --type user          # read YOUR comments
hunk session comment add --repo . --file src/x.rs --new-line 42 \
  --summary "off-by-one" --rationale "…" --focus        # write into your live diff, move your cursor
hunk session navigate --repo . --next-comment
tuicr review comments  ·  tuicr review add
```

No other pattern here lets an agent and a human look at *the same live artifact* and annotate it for each other.

---

## P9 · The verify loop — act, check, remediate, re-check ⭐

Every other pattern here *acts*. This one asks whether the action worked, and whether it **stays**
worked after the obvious fix.

```
act ─► verify ─┬─ pass ─► done
               └─ fail ─► remediate ─► RE-verify ─┬─ pass ─► done (n attempts)
                                                  └─ fail ─► report UNVERIFIED
```

A one-shot check tells you something is broken. A loop tells you whether it is *still* broken after
the remedy — which is the difference between a report and a repair.

```toml
[verify]
run       = "just gate"
contains  = "READY"
expect_rc = 0
retries   = 2
remediate = "just annotate-all"     # runs only BETWEEN attempts
backoff   = 1
```

```bash
just until "<check>" "<want>" "<fix>" <tries> <backoff>   # the generic form
just verify-cockpit · verify-build · verify-review · verify-docs · verify-source · verify-all
```

**Three rules that make it honest:**

1. **Remediate between attempts, never before the first.** The first verification must see the
   untouched state, or a healthy system gets "fixed" anyway and the check has told you nothing.
2. **Not everything should be remediable.** `verify-build` and `verify-docs` deliberately take no
   remedy: a broken build and documentation drift both need a human decision. And the review gate's
   *"no human note yet"* rung is deliberately not agent-fixable — **an agent that remediates its way
   past its own gate has defeated the gate**. Refusing to fix something is sometimes the correct fix.
3. **Report the attempt count.** `VERIFIED after 2 attempt(s)` is a materially different fact from
   `VERIFIED` — it says the system needed intervention, which is worth noticing before it becomes
   normal.

Proven: killed a service, ran the loop —
`✗ machine → ↻ habitat respawn → ✓ machine (attempt 2/3)`.

The example now requires both the expected content and exit zero for `[verify]`. See
[[60 Workflows/Runbooks#Inspection and execution boundaries — source checked 2026-09-06|executor limitations]]
before using retrying steps. Distinguish a failed wanted service from one intentionally retired
to save resources; remediation must not repeatedly undo deliberate shutdown.

Before this, the reactor's 20-second poll was the **only** component in the habitat that closed
act→verify→act; everything else checked once and reported.

## Chain documentation must land on ground truth ⭐

These patterns are *chain documentation*: a note about tool X legitimately shows flags of tools Y
and Z, because that is what composition looks like. That freedom has a cost — a chain is only
trustworthy if **every link lands on ground truth**, and the ground truth for a flag is the line of
source that defines it, not the `--help` text describing it.

[[Documented Surface and Source]] resolves all 58 flags these notes document to `repo/file:line`,
with a confidence mark. `knowledge-audit` fails if any documented flag cannot be corroborated by
its tool's own source.

Two things that made this real rather than decorative:

- **Attribution must be per line, not per note.** A first pass blamed `fzf.md` for `just --choose`
  and `jqp.md` for `jq --argjson`. Both were correct prose. Attribute a flag to a tool only when
  that line's command *is* that tool.
- **Rust/clap CLIs never contain the literal `--flag`.** They declare `pub shebang: String` and the
  derive macro generates it. A literal grep reported 91 of 92 flags as unconfirmed — the checker
  was broken, not the documentation.

The payoff is corroboration rather than assertion: `atuin --script` resolves to
`crates/atuin/src/command/client/scripts.rs:33 · pub script: Option<PathBuf>` — a **PathBuf**,
independently confirming [[00 - Field Findings|F3]] (that `--script` takes a file path, not inline
text), which had until then rested only on an error message.

## Composition rules of thumb

1. **Prefer P3 to P2** when a watcher is already resident — don't recompute what a pane knows.
2. **Prefer P7 before anything destructive** — dry-run, summary, `-n`.
3. **End novel work with P4** — if it worked and you'd do it again, capture it.
4. **JSON is the lingua franca** — when adding a tool, check for `--json`/`--format json` first; that determines whether it can join P2.

Related: [[Fabric Bash Command Plane]] · [[Tool Clusters]] · [[Workflow Recipes]] · [[Most-Used Tools]] · [[00 - Toolshed Index]]
