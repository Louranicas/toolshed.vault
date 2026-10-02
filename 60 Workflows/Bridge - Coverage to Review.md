---
tags: [toolshed, workflow, bridge, W2, W3, W4]
created: 2026-09-02
source: fedora-arena/scripts/untested-to-hunk.sh
chain: W4 search → W2 tests → W3 review
---

# Bridge · Coverage gaps → live review

Finds every `pub fn` that **no assertion in the crate mentions**, and annotates it in the live
[[hunk]] diff. A poor-man's coverage signal that needs no instrumentation, no `cargo-tarpaulin`,
and no build — just [[fzf|ripgrep]] and set arithmetic.

## Usage

```bash
just coverage
./scripts/untested-to-hunk.sh <repo>
atuin scripts run coverage -v repo=/path
```

## How it works

```bash
# W4 — every public function, with file+line (rg's structured output)
pubs=$(rg --json '^\s*pub fn (\w+)' -r '$1' --glob '!target' -- . \
  | jq -s -c '[.[] | select(.type=="match")
      | {name: (.data.submatches[0].match.text | sub("^\\s*pub fn ";"")),
         file: (.data.path.text | sub("^\\./";"")), line: .data.line_number}]')

# W2 — names referenced inside any assertion
tested=$(rg -o --no-filename 'assert\w*!\(\s*(\w+)\(' -r '$1' --glob '!target' -- . \
  | sort -u | jq -R -s -c 'split("\n") | map(select(length>0))')

# set difference -> W3 annotate (author "coverage", retracts independently)
gaps=$(jq -c --argjson t "$tested" '[.[] | select(.name as $n | ($t | index($n)) | not)]' <<<"$pubs")
```

## Three rg traps this encodes

All three failed **silently or fatally** on the first attempt:

1. **`rg` with no path blocks on stdin forever** ([[00 - Field Findings|F11]]) — cost a 2-minute
   timeout. Hence `-- .`
2. **`-r '$1'` is ignored in `--json` mode** ([[00 - Field Findings|F12]]) — you get
   `pub fn median`, not `median`. Hence the `sub()` in jq.
3. **`-- .` prefixes paths with `./`** ([[00 - Field Findings|F13]]) — hunk rejected every
   comment without error. Hence the second `sub()`.

## Proven

5 public fns found, 2 referenced in assertions → 3 gaps annotated (`median`, `spread`, `above`).
Wrote the three tests → re-ran → `W3 · 0 untested public fn(s)` / *"full coverage of public API"*,
all three annotations auto-retracted.

## Honest limits

It matches **names in assertions**, not execution. A function called only indirectly reads as
untested; a function named in an assertion but never actually exercised reads as tested. It is a
*prompt for attention*, not a coverage metric — which is exactly what a review annotation should be.

Related: [[Bridge - Diagnostics to Review]] · [[hunk]] · [[Cross-Workspace Review Gate]] ·
[[00 - Toolshed Index]] · [[00 - Workflows]]
