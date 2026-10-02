---
tags: [toolshed, workflow, bridge, W2, W3]
created: 2026-09-02
updated: 2026-09-06
source: fedora-arena/scripts/clippy-to-hunk.sh
chain: W2 build → W3 review
---

# Bridge · Diagnostics → live review

**The problem:** compiler diagnostics land in a log. A human reviewing a diff has to hold them
in their head and map file:line back to what they are looking at. The two views never meet.

**What this does:** turns every `cargo`/`clippy` diagnostic into a **comment inside the running
[[hunk]] review session**, anchored at its exact line — so findings appear *inline in the diff
the human is already reading*, attributed and boxed.

## Usage

```bash
just annotate                          # clippy (default)
just annotate job=check                # or any cargo job
./scripts/clippy-to-hunk.sh <repo> <job>
atuin scripts run annotate -v repo=/path -v job=clippy
```

**Prerequisite:** the hunk session must be launched with `--agent-notes`, or the comments land
but render nothing ([[00 - Field Findings|F7]]):
```bash
hunk diff master --agent-notes
```

## How it works

The fragment below illustrates data flow, not a standalone success gate. It launches a new
compiler job and mutates live review annotations. Capture compiler status independently when
diagnostics must still be processed after failure; a successful jq filter is not a successful
build. Coordinate target ownership with any existing watcher and avoid duplicate bridge passes.
For a one-shot pipeline whose exit status matters, see [[20 Chaining/Workflow Recipes#R3 · Rust change → verdict → review (C4 → C3)|the revised recipe]].

```bash
# 1. W2 — diagnostics as structured data
cargo clippy --all-targets --message-format json \
  | jq -s '[.[] | select(.reason=="compiler-message") | .message
      | select(.level=="warning" or .level=="error")
      | select((.spans|length) > 0)
      | {level, lint: (.code.code // .level), msg: .message,
         file: .spans[0].file_name, line: .spans[0].line_start,
         hint: (((.children // []) | map(select(.level=="help")) | .[0].message) // "")}]
    | unique_by([.file,.line,.lint])'

# 2. W3 — retract our previous pass FIRST (even when there are zero findings)
hunk session comment list --repo "$REPO" --json \
  | jq -r '.comments[]? | select(.author=="clippy") | .commentId' \
  | while read -r id; do hunk session comment rm --repo "$REPO" "$id"; done

# 3. W3 — annotate
hunk session comment add --repo "$REPO" --file "$file" --new-line "$line" \
  --summary "$lint: $msg" --rationale "$hint" --author clippy --json
```

## The retraction rule ⭐

The bridge **always clears its previous pass before deciding what to do** — including when the
diff is now clean. The first version exited early on zero diagnostics, which left *stale advice
pinned to code that had already been fixed*. That is worse than no annotation at all.

Keying on `--author clippy` means each producer owns its own notes: [[Bridge - Coverage to Review|coverage]]
retracts independently, and **human notes are never touched**.

## Proven

3 clippy diagnostics → 3 inline notes rendering in the live pane:

```
▌   11 +      if n % 2 == 0 {
    ╭─ clippy note - crates/arena-core/src/stats.rs (new) R11 ──────────╮
    │ clippy::manual_is_multiple_of: manual implementation of           │
    │ `.is_multiple_of()`                                               │
    ╰───────────────────────────────────────────────────────────────────╯
```

Loop closed: applied the three fixes → `clippy_lints: 0` → re-ran the bridge →
`W3 · retracted 3 stale annotation(s)` → `nothing to annotate — diff is clean`.

## Gotchas this encodes

- `commentId`, not `id` ([[00 - Field Findings|F8]]) — using `.id` deletes nothing, silently
- `--agent-notes` or it is invisible ([[00 - Field Findings|F7]])
- `unique_by([.file,.line,.lint])` — cargo emits the same diagnostic once per target

Related: [[Bridge - Coverage to Review]] · [[hunk]] · [[bacon]] ·
[[Cross-Workspace Review Gate]] · [[00 - Toolshed Index]] · [[00 - Workflows]] ·
[[Synchronised Review and Editor]]
