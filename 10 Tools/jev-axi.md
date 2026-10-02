---
tags: [jev, typesafe, cli, tool, axi]
created: 2026-09-18
source: https://github.com/shiftynick/jev-axi @ 0.4.2 (MIT)
---

# 🔧 jev-axi — the CLI

```sh
npm install -g jev-axi          # needs Node >= 22
jev-axi config set apiKey ...   # or TYPESAFE_API_KEY, or ./.env
jev-axi                         # home view: key, model, 24h usage, commands
```

Key resolution: **env → `./.env` in the working directory → `~/.config/jev-axi/config.json`**
(written mode 600). Installed and keyed on this machine 2026-09-18.

> [!note] The one-line description in the axi catalogue is wrong
> There is no `review` or `screen` verb. "semantic grep" = `find`, "diff review" = `diff`,
> "log triage" = `triage`, "injection screening" = `guard`.

## The verbs

| group | commands |
|---|---|
| **primitives** | `pick` (Choice) · `rate` (Score) · `check` (Noul) · `ask` (many questions, one call) |
| **batch** | `rank` · `filter` · `find` · `files` — auto-chunked, 4 concurrent by default |
| **recipes** | `diff` · `triage` · `guard` · `commit` · `recipe` |
| **safety** | `guard-exec` · `hook pre-tool-use` · `hook pre-commit` · `hook commit-msg` · `setup` |
| **meta** | `models` · `usage` · `stats` · `cache` · `config` |

Output is **TOON** by default (compact key/value + tabular arrays), `--json` for machines, `--full`
for untruncated distributions. Errors render as TOON **on stdout**.

Caching: hash of *(model, state, questions)*, reused 24 h — and **invalidated when `jev-latest`
resolves to a new version**, so a model update discards stale answers automatically.

## Exit codes — the pipeline contract

| code | meaning |
|---:|---|
| 0 | success, including `guard` verdicts `pass` and `review` |
| 1 | API problem (`AUTH_REQUIRED`, `RATE_LIMITED`, `NETWORK`) — retry once, then continue without it |
| 2 | usage error — fix the flags |
| **3** | **`guard` verdict `block`** |
| 126 | `guard-exec` blocked the command (shell "found but not executed") |
| 127 | `guard-exec` could not start the binary |
| — | otherwise `guard-exec` returns the wrapped command's own status |

Verified here: `guard` clean → 0, hostile → 3. See [[Jev - Field Findings|F7]].

## Confidence bands

`act ≥ 0.75` · `confirm 0.45–0.75` · `escalate < 0.45`. For Noul it **derives** one as
`|p − 0.5| × 2`, so `p=0.05` and `p=0.95` are both confidence 0.90.

> [!warning] `--act`/`--confirm` do NOT tighten the recipes
> `guard` (0.4/0.7), `diff` (0.6/0.9/1.5), `triage` (0.35/0.65) and the safety hook
> (0.45/0.8/1.5) use **fixed internal thresholds**. The band flags only change the displayed
> column. Real gotcha.

## Fail-open by default — everywhere

Git hooks, `guard-exec --on-error`, and `hook pre-tool-use --on-error` all **allow** when the key
is missing or the API is unreachable. A deliberate availability choice. Override per integration
with `--on-error deny`.

Also: `--on-ask prompt` **denies when there is no TTY**, so unattended runners need
`--on-ask allow` — or, better, `--on-ask deny --on-error deny` for jobs that must not run unchecked.

## The safety gate, specifically

`hook pre-tool-use` checks `Bash|Write|Edit|MultiEdit`. **Routine calls never leave the machine** —
read-only commands, project tests and builds, deleting build folders, edits inside the project are
all decided locally. Anything with command substitution, redirection, `eval` or `sudo` always gets
a real check.

What makes it worth more than an allowlist: **it reads the contents of local scripts the command
runs** (≤4000 chars), so `./scripts/cleanup.sh` is judged by what it *does*, not its name.

It **never auto-approves** — "allow" prints nothing, so the normal permission flow still runs.

> [!caution] Installing it writes `.claude/settings.json`
> `jev-axi setup safety` modifies agent settings. Don't run it casually.

## Cost ledger

The TypeSafe API has **no spend endpoint**, so jev-axi keeps its own: `~/.config/jev-axi/stats/usage.jsonl`,
one row per call with tokens, latency, cache status, **project** (enclosing git repo), and how many
answers landed in each confidence band. `jev-axi usage` / `stats` read it.

Two of its help lines are good fleet hygiene signals: *"over a quarter of answers land in the
escalate band — narrower questions usually raise confidence"*, and *"most calls ask a single
question; batching costs almost nothing extra"*.

Pricing is a **local assumption** (`$0.042` / `$0`), not fetched. Override with
`jev-axi config set price.input`.

## Honest limits, from the repo itself

> *"What it does not do is make agents cheaper at understanding code: agents told to use `files`
> read 25% fewer files but cost the same, because answering still meant reading the code.
> **Use it for judgments, not as a replacement for reading.**"*

And: agents **never pick this tool up unprompted** — skill alone, never used; SessionStart hook,
never used; custom subagent, Claude Code prefers its built-in. Only a name-override or explicit
instruction reaches it. Published against their own interest, and they re-scoped the roadmap on it.

Never send it secrets: *"when the task is to find or audit credentials in the user's own project,
use `grep` or a local secret scanner instead, and don't use jev-axi for that task at all."*

Related: [[Jev - The Model]] · [[Jev - Field Findings]] · [[Jev - Applications Here]]

Installed the same day (2026-09-18) as [[firstmate]], whose `quota-array-dispatch` skill states the rule this CLI also follows: a data-only tool publishes a comparable scalar and **never recommends, selects, ranks or infers a route**. The decision lives in a named owner, not in the tool.


**See also (2026-09-29):** `~/.local/bin/jev-scout` wraps `jev-axi filter` and sizes `--preview` from the files. The default of 600 chars per item judged titles, not notes: 0 of 8 recall versus 5 of 8 at a 40,000-char preview, with misses flagged partial. [Consolidation note](obsidian://open?vault=jev.vault&file=70%20Workflows%2FAssimilating%20Jev%20into%20Claude%20Workflows%202026-09-29).
