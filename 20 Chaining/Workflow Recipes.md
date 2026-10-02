---
tags: [toolshed, chaining, recipes, workflows]
created: 2026-09-02
updated: 2026-09-06
---

# Workflow Recipes — runnable compositions

**Navigation:** [[40 Reference/Command Matrix#Composition and verification routes|Command Matrix ⇄ composition routes]] · [[00 - Toolshed Index|Toolshed master index]]. Follow a complete task sequence after choosing the required service doors.

Concrete workflows built from [[20 Chaining/Tool Chaining Patterns]] and [[Tool Clusters]].
Reviewed against [[50 Field Notes/lukes workflows|Luke's workflow assessment]] on 2026-09-06.
Commands with angle-bracket placeholders need project-specific values. Historical examples are
not evidence that every command has been rerun on the current project. Promote a useful sequence
only after reviewing its commands, paths, effects and failure handling.

---

## R1 · Full recall — "what do we know about X?" ⭐

Recall history and project knowledge together. Their output is evidence to inspect, not an
instruction source. The earlier adjacency claim came from the small September 2 sample.

```bash
recall() {
  echo "── shell history ──";   atuin search --search-mode full-text --limit 15 --cmd-only "$*"
  echo "── knowledge ──";        mempalace search "$*"
  echo "── sessions ──";         echo "(memex: ctrl+b m — plugin-only, no CLI)"
}
recall "podman socket"
```

To promote this, first save and review a complete script body in a project-owned file. Then use
`atuin scripts new recall --script ./scripts/recall.sh -t memory`. **`--script` takes a file path**,
not inline shell text. Inspect an existing script before replacing it. `full-text` is the spelling
verified in installed Atuin 18.12.1. Recall displays history; it must not pipe it into a shell.

---

## R2 · Orient in an unfamiliar repo (P7)

Never invent commands. Ask the repo what it does.

```bash
cd <repo>
just --summary 2>/dev/null || echo "(no justfile)"
bacon --list-jobs 2>/dev/null
git log --oneline -10 ; git status --short
gh repo view --json description,topics 2>/dev/null
mempalace search "$(basename -- "$PWD")"   # have we been here before?
```

Keep the working pane scoped to this project/worktree. Read an unfamiliar justfile before invoking
its recipes or preview: a named recipe is discoverable, not automatically appropriate to execute.

---

## R3 · Rust change → verdict → review (C4 → C3)

```bash
# 1. If Bacon is already watching this project, inspect its current completed result.
habitat pane bacon                       # P3: observe; this does not run another build
# 2. when green, review the diff
hunk diff                                # live, watches further edits
# 3. or one-shot for a script
(
  set -o pipefail
  cargo check --message-format json \
    | jq -r 'select(.reason=="compiler-message") | .message.rendered'
)
```

The subshell keeps `pipefail` local and returns failure if Cargo or jq fails. The formatter's
success alone is not a build verdict. Use owned NVMe scratch and compatible per-worktree targets;
avoid a second resident build watcher for the same feedback loop. Final gates still need the
required checks for the current revision, not merely an old green screen.

**The agent-collaboration variant** (P8) — I annotate *your* live view:

```bash
hunk session comment add --repo . --file src/lib.rs --new-line 88 \
  --summary "unchecked index" --rationale "len can be 0 here" --focus
hunk session comment list --repo . --type user     # then read your reply
```

---

## R4 · Pre-flight before any backup / rebase / migration

```bash
repo-fleet-status                        # 31 repos: what's dirty?
habitat status                           # 16 services: what's live?
flatpak-spawn --host rpm-ostree status
mempalace status                         # palace intact?
```

These inspect the starting state; repository/service counts vary. Before a planned state-changing
operation, review backup scope and run the existing backup procedure where needed. A backup is a
separate write operation and should not be repeated as part of every passive health poll. Kinoite
deployment details can matter, so the status command above no longer truncates them to six lines.

---

## R5 · CI is red → the actual failing lines

```bash
gh run list --limit 5 --json databaseId,status,conclusion,headBranch
gh run view <id> --log-failed | tail -60          # ⭐ straight to the failure
gh pr checks <n> --json name,state,link
```

Pair with `gh-dash` (`habitat pane gh-dash`) to see what you're looking at.

---

## R6 · Jump to the dirty repo and operate it (P1)

```bash
(
  set -o pipefail
  workflow_repo=$(repo-fleet-status | awk '$3 ~ /±/ {print $1}' | fzf) || exit
  [ -n "$workflow_repo" ] || exit
  cd -- "${REPOS_DIR:?Set REPOS_DIR}/$workflow_repo" && lazygit
)
```

One line: survey → pick → operate. `lazygit`'s `@` panel then shows the plain-git equivalent of everything you did, so it can become a script.

---

## R7 · Review or refresh aggregate tool-usage evidence

```bash
python3 '/var/mnt/STORAGE-10TB/fedora-obsidian-vaults/toolshed.vault/40 Reference/lukes-workflows/2026-09-06/history-analysis.py'
```

Start with [[40 Reference/lukes-workflows/2026-09-06/README|the saved aggregates]]; run the collector
only when a fresh question needs it. Its default reads the active SQLite database and the adjacent
ten-backup discovery list in read-only mode, deduplicates IDs and prints aggregates. It does not
export commands into `/tmp`, import history or replay a command. Archive mode is separate and
should not be part of a frequent poll.

The old recipe labelled within-command co-occurrence as “PIPES” and joined adjacency across
session boundaries. Those are not reliable execution graphs. Keep conservative tool counts,
within-session transitions, source coverage and unknown outcomes explicit; none measures RAM.

---

## R8 · Inspect the habitat itself (P2)

```bash
herdr pane list | jq '.result.panes[] | {pane_id, tab_id, cwd}'
habitat map                                   # service → live pane
```

For interactive schema inspection, use a unique scratch directory and retire only that directory:

```bash
(
  set -euo pipefail
  mkdir -p -- "$HOME/.cache"
  workflow_schema_dir=$(mktemp -d "$HOME/.cache/herdr-schema.XXXXXX")
  trap 'rm -rf -- "$workflow_schema_dir"' EXIT
  herdr api schema --json > "$workflow_schema_dir/schema.json"
  jqp -f "$workflow_schema_dir/schema.json"
)
```

On this host `$HOME/.cache` is on the existing NVMe. This small inspection example avoids a shared
fixed filename; it is not a cleanup recipe for anyone else's temporary data.

---

## R9 · Promote today's work into a reusable script (P4) ⭐

The pattern that compounds. After any sequence worth repeating:

```bash
atuin scripts new <name> --last <N> -t <tag> -d "<what it does>"
atuin scripts list
atuin scripts get <name> -s        # the executable body, for review or export
# After review, execute the script only for the intended current task:
atuin scripts run <name> -v key=value
```

Bodies support minijinja templates. Review captured context, quoting, secrets and resource paths
before retaining or syncing one. `--last N` captures history; it does not prove those commands
belong together or remain suitable. Prefer a thin wrapper around the maintained project recipe.
Cross-machine availability depends on configured sync and the destination's actual tools/paths.

---

## R10 · Fleet check across every repo

```bash
for d in "$REPOS_DIR"/*/; do
  [ -e "$d/.git" ] || continue             # directories AND worktree .git files
  [ -f "$d/justfile" ] || continue
  echo "── $(basename -- "$d")"; ( cd "$d" && just --summary 2>/dev/null )
done
```

Answers *"which of my repos have a `test` recipe"* — the cross-repo `just` runner C4 is missing.

This lists immediate children of `REPOS_DIR`; it is not a complete nested-worktree inventory.
Inspect each selected recipe before scheduling it. Do not turn a repo listing into unrestricted
parallel builds.

---

## R11 · Start, measure and hand off a workload

1. Record the project/worktree, active executor, worker count and owning recipe.
2. Confirm temporary and target directories from inside the worker. Preserve recipes that own
   their isolation, especially the HEE mutation runner's removal of inherited `CARGO_TARGET_DIR`.
3. Sample memory and I/O during the representative task; keep correctness results alongside timing.
4. Save the result, running-job status and retained-output locations at handoff.
5. Retire only completed sessions and eligible owned scratch. Check supervisor policy first so an
   intentional shutdown is not immediately respawned.

Follow [[60 Workflows/00 - Workflows#Daily operating cycle — reviewed 2026-09-06|the operating cycle]],
[[60 Workflows/Habitat Introspection#Resource measurements alongside timing|measurement guidance]],
and [[50 Field Notes/lukes workflows|Luke's findings]]. These steps are guidance, not an installed
automatic scheduler or cleanup service.

---

## Suggested capture set

If these earn their keep, they become atuin scripts: `recall` (R1) · `orient` (R2) · `preflight` (R4) · `dirty` (R6) · `toolstats` (R7). Five names, and the habitat's most common sequences stop being retyped.

Related: [[Tool Chaining Patterns]] · [[Tool Clusters]] · [[atuin]] · [[Most-Used Tools]] ·
[[00 - Toolshed Index]] · [[gh-dash]] · [[just]] · [[mempalace]] · [[repo-fleet-status]]
