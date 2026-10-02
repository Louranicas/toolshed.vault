---
tags: [toolshed, tool, workspace-2, task-runner]
tool: just
version: 1.57
upstream: https://github.com/casey/just
docs: https://just.systems/man/en/
workspace: W2 · pane w1:pS
agent_door: habitat q just  (→ just --summary)
updated: 2026-09-09
---

# just — the project's own verb list

A command runner (not a build system). Its habitat value is **discoverability**: a `justfile` turns a repo's operations into a machine-readable list, so I can ask *"what can I do here"* instead of guessing.

## Linked source and monthly maintenance

[Justfile source map](file:///var/home/Louranicas/fedora-arena/justfiles/README.md)
points to the current Arena, Fabric, factory-experiment, and runbook-candidate
justfiles and links back here. Each source has an Obsidian return link to the
[[70 Toolkit/Skill Usage Guide#Runbooks and justfiles|runbooks and justfiles guide]].

[[70 Toolkit/Justfile Update Check|Justfile Update Check]] records the monthly
comparison against an explicitly accepted baseline, including additions, changes,
removals, and broken documentation links. The cron schedule is `0 9 1 * *` in local
Australia/ACT time. The source map contains the checker and management commands.

## Pi Genesis planning seam — 2026-09-06
[Genesis Justfiles and Runbooks](obsidian://open?vault=pi.vault&file=95%20Genesis%2FGenesis%20Justfiles%20and%20Runbooks) links back here. Its proposed justfiles are thin reviewed doors to Rust tooling or authenticated engine procedures, with generated-wrapper/source freshness and an inert help default. Untrusted recipe inspection begins with bounded source reading; the guide's dry-run example below is not a sandbox guarantee for arbitrary justfiles. No Genesis justfile or operational runner is installed by that planning work.

## Discovery & execution

```bash
just -l                    # --list, with doc comments and groups
just --summary             # ⭐ names only, space-separated — the agent door
just --groups              # group names
just --choose              # fzf recipe picker ([[fzf]] synergy)
just <recipe> [args]
just -n <recipe>           # --dry-run: print without executing ⭐ safe probe
just --explain             # show a recipe's doc comment
just --evaluate            # dump variables (or one: --evaluate VAR)
just --variables           # variable names only
just --show <recipe>       # source of one recipe
just --fmt --check         # format / verify formatting
just --json  ·  --dump --dump-format json     # ⭐ full machine-readable AST
just -f path/justfile -d .                    # run another project's justfile
just --init  ·  --man  ·  --completions <shell>
```

Other flags worth knowing: `--set VAR=VAL` · `--yes` (skip confirmations) · `--no-deps` · `--one` · `--timestamp` · `--highlight`/`--no-highlight` · `--shell`/`--shell-arg` · `--dotenv-command`/`--no-dotenv` · `--allow-missing` · `--unstable` · `--jobs`.

**`--dump --dump-format json` is the strongest agent surface** — the whole justfile as structured data (recipes, params, dependencies, doc comments), which beats scraping `--list`.

## Justfile anatomy

```just
set shell := ["bash", "-cu"]
set dotenv-load

default: check              # first recipe is the default

# Doc comments become --list descriptions
[group('ci')]
check:
    cargo check

test filter="":             # parameterised, with a default
    cargo test {{filter}}

deploy: check test          # dependencies run first
    ./scripts/deploy.sh

[confirm("really?")]
dangerous:
    rm -rf build
```

Features: parameters + defaults + variadics · dependencies (and `&&` post-deps) · `[group]`, `[confirm]`, `[private]`, `[linux]`/`[macos]` attributes · `set` options · dotenv loading · string interpolation `{{ }}` · modules/submodules · shebang recipes (any interpreter).

## Live example — `deep-diff-forge` (29 recipes)

Groups: `[receipts]` `[release]` `[review]` `[security]` — e.g. `review *ref=""`, `review-probe` (headless render for CI), `security-sbom`, `security-soak`, `gate-release`. The W2 `pS` pane opens on `just --list`, making it a live menu of that project's operations.

## Chains

**Feeds from:** repo convention. **Feeds into:** `bacon` (a bacon job can run `just`), `fzf`/`tv` (pick a recipe), CI.
**Rule I follow:** check for a justfile *before inventing commands* — `just --summary` is the cheapest possible orientation in an unfamiliar repo.

## Rust performance practice

Use [[40 Reference/Perfecting Rust - Performance Engineering#A reusable experiment record|the Rust experiment record]] when designing benchmark or profiling recipes: preserve the input, build configuration, measurement boundary and raw results. [[40 Reference/rust-mastery/2026-09-06/README#Reproduce in a working copy|The lab reproduction guide]] supplies concrete commands to adapt to a project justfile. Return to [[40 Reference/Perfecting Rust - Performance Engineering#Connected notes and master indexes|the Rust learning map]] for the surrounding workflow.

Related: [[bacon]] · [[fzf]] · [[Workflow Recipes]] · [[00 - Toolshed Index]] ·
[[Arena Practice Ground]] · [[Command Matrix]] · [[Documented Surface and Source]] ·
[[Runbooks]] · [[Tool Clusters]] · [[jqp]]

## Context preparation — 2026-09-09

[[70 Toolkit/skills#Habitat Context|Habitat Context]] ⇄ this note. Admit selected Justfiles with related notes and runbooks into bounded, source-backed context packets. Declared calls and derived inverse edges support navigation; ingestion does not execute recipes.
