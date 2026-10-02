---
tags: [toolshed, reference, matrix]
created: 2026-09-02
updated: 2026-09-06
---

# Command Matrix — every service at a glance

<!-- habitat-highways:2026-09-08:start -->
## Corpus insight routes — 2026-09-08

Curated navigation added in this edition; the dated claims and evidence below retain their original scope.

| Purpose | Route |
|---|---|
| Cross the vault family by intent | [LLM Traversal - Cross-Vault Routes](obsidian://open?vault=herdr-fedora-habitat.vault&file=80%20Architecture%2FLLM%20Traversal%20-%20Cross-Vault%20Routes) · [file](</var/mnt/STORAGE-10TB/fedora-obsidian-vaults/herdr-fedora-habitat.vault/80 Architecture/LLM Traversal - Cross-Vault Routes.md>) |
<!-- habitat-highways:2026-09-08:end -->


**Parent:** [[00 - Toolshed Index#Command Matrix and Fedora navigation|Toolshed master index]]. **Within this note:** [[#Service command doors|Service doors]] · [[#Composition and verification routes|Composition]] · [[#Fedora and Herdr master indexes|Vault indexes]] · [[#Regenerating the reference dumps|Reference capture]] · [[#Version watch|Version watch]].

The matrix originated on 2026-09-02. This 2026-09-06 update connects the documented routes; the version table retains its original capture context.

One row per service: what it is, the **agent door** (non-interactive), the **pane door**, and whether it emits JSON (which decides if it can join a [[Tool Chaining Patterns|P2 JSON chain]]).

## Service command doors

Choose a service here, then follow [[#Composition and verification routes|the composition routes]]. Review [[#Version watch|the recorded version context]] before interpreting historical command details; [[#Regenerating the reference dumps|reference capture]] provides the refresh route.

| Service | W | Agent door | Pane door | JSON? | Cluster |
|---|---|---|---|---|---|
| [[10 Tools/atuin\|atuin]] | 1 | `atuin search --cmd-only` · `scripts run` | `habitat pane atuin` | — | [[20 Chaining/Tool Clusters#C1 · Memory — three layers of recall 🧠\|C1]] |
| [[10 Tools/mempalace\|mempalace]] | 1 | `mempalace search` · `wake-up` | `habitat pane mempalace` | — | [[20 Chaining/Tool Clusters#C1 · Memory — three layers of recall 🧠\|C1]] |
| [memex](obsidian://open?vault=herdr-fedora-habitat.vault&file=50%20Automation%2FPlugin%20-%20memex) | — | See the CLI reference in the linked note | — | — | [[20 Chaining/Tool Clusters#C1 · Memory — three layers of recall 🧠\|C1]] |
| [[10 Tools/television\|television]] | 1 | *(human-first)* | `habitat pane television` | — | [[20 Chaining/Tool Clusters#C2 · Finders — locate anything 🔎\|C2]] |
| [[10 Tools/fzf\|fzf]] | 1 | `fzf --filter=Q` | *(no pane)* | — | [[20 Chaining/Tool Clusters#C2 · Finders — locate anything 🔎\|C2]] |
| [[10 Tools/yazi\|yazi]] | 4 | *(human-first; fd/rg)* | `habitat pane yazi` | — | [[20 Chaining/Tool Clusters#C2 · Finders — locate anything 🔎\|C2]] |
| [[10 Tools/nushell\|nushell]] | 1 | `nu -c '<pipeline>'` | `habitat pane nushell` | ✅ in/out | [[20 Chaining/Tool Clusters#C5 · Data shaping — reshape anything 🧮\|C5]] |
| [[10 Tools/lazyvim\|lazyvim]] | 2 | `nvim --headless` · `--server --remote` | `habitat pane lazyvim` | — | — |
| [[10 Tools/bacon\|bacon]] | 2 | `cargo check` *(not `--headless`!)* | `habitat pane bacon` ⭐ | ✅ via cargo | [[20 Chaining/Tool Clusters#C4 · Build & verify — is it correct? 🔨\|C4]] |
| [[10 Tools/just\|just]] | 2 | `just --summary` · `--dump --dump-format json` | `habitat pane just` | ✅ | [[20 Chaining/Tool Clusters#C4 · Build & verify — is it correct? 🔨\|C4]] |
| [[10 Tools/lazygit\|lazygit]] | 3 | *(human-first; plain `git`)* | `habitat pane lazygit` | — | [[20 Chaining/Tool Clusters#C3 · Review — judging change ⚖️\|C3]] |
| [[10 Tools/hunk\|hunk]] | 3 | `hunk session … --json` ⭐ | `habitat pane hunk` | ✅ | [[20 Chaining/Tool Clusters#C3 · Review — judging change ⚖️\|C3]] |
| [[10 Tools/tuicr\|tuicr]] | 5 | `tuicr review list\|comments\|add` | `habitat pane tuicr` | partial | [[20 Chaining/Tool Clusters#C3 · Review — judging change ⚖️\|C3]] |
| [[10 Tools/gh-dash\|gh-dash]] | 3 | `gh … --json` (whole API) | `habitat pane gh-dash` | ✅ | [[20 Chaining/Tool Clusters#C3 · Review — judging change ⚖️\|C3]] |
| [[10 Tools/bottom\|bottom]] | 4 | *(display only; ps/free/df)* | `habitat pane bottom` | — | [[20 Chaining/Tool Clusters#C6 · System & containers 🖥️\|C6]] |
| [[10 Tools/podman-tui\|podman-tui]] | 4 | `flatpak-spawn --host podman --format json` | `habitat pane podman-tui` | ✅ | [[20 Chaining/Tool Clusters#C6 · System & containers 🖥️\|C6]] |
| [[10 Tools/jqp\|jqp]] | 5 | `jq` | `habitat pane jqp` | ✅ | [[20 Chaining/Tool Clusters#C5 · Data shaping — reshape anything 🧮\|C5]] |
| [[10 Tools/repo-fleet-status\|repo-fleet-status]] | 5 | `repo-fleet-status` | `habitat pane repo-fleet` | — | [[20 Chaining/Tool Clusters#C5 · Data shaping — reshape anything 🧮\|C5]] |
| [[10 Tools/herdr\|herdr]] | spine | entire CLI + NDJSON socket ⭐ | *(is the panes)* | ✅ | [[20 Chaining/Tool Clusters#C7 · The spine 🕸️\|C7]] |

**Ten of nineteen emit JSON** — that is the size of the C5 adapter surface.

## Composition and verification routes

Return to [[#Service command doors|the service table]] to choose an interface; use the companion that explains the next step. Continue through [[#Fedora and Herdr master indexes|the master-index map]] when the task crosses vault subjects.

- [[20 Chaining/Tool Chaining Patterns|Tool chaining patterns]] — Choose a filter, JSON, watcher, capture, discovery or verification pattern.
- [[20 Chaining/Tool Clusters|Tool clusters]] — Resolve C1–C7 into the memory, finder, review, build, data, system and spine groups.
- [[20 Chaining/Workflow Recipes|Workflow recipes]] — Follow a complete task sequence after choosing the required service doors.
- [[60 Workflows/Shape-Directed Tool Chaining|Shape-directed chaining]] — Connect a producer’s output shape to an appropriate consumer.
- [[60 Workflows/Knowledge Audit|Knowledge audit]] — Check note targets, source references and documentation freshness.
- [[70 Toolkit/00 - Habitat Toolkit|Habitat toolkit]] — Find the locally authored bridge, cascade, sandbox and related tools.
- [[60 Workflows/00 - Workflows|Workflows index]] — Place tool selection in the daily operating and verification cycle.
- [[10 Tools/podman|Podman command reference]] — Follow the container CLI companion to the matrix’s podman-tui row.
- [[40 Reference/Perfecting Rust - Performance Engineering|Perfecting Rust]] — Connect checker, runner and monitoring doors to measured Rust practice.
- [[40 Reference/rust-mastery/README|Rust corpus folder]] · [[40 Reference/rust-mastery/2026-09-06/README|lab and evidence]] — readable source routes, measured results and explicitly open practice work.

**Across the habitat:**

- [Developer Tool Loadout](obsidian://open?vault=herdr-fedora-habitat.vault&file=70%20Toolchain%2FDeveloper%20Tool%20Loadout) — Workspace placement, installation history and launch context.
- [Habitat Service Bridge](obsidian://open?vault=herdr-fedora-habitat.vault&file=70%20Toolchain%2FHabitat%20Service%20Bridge) — The bridge behind the agent and pane access paths.
- [memex reference](obsidian://open?vault=herdr-fedora-habitat.vault&file=50%20Automation%2FPlugin%20-%20memex) — The plugin, documented CLI and session-history interface.

These companions link back to the matrix. The memex reference contains a CLI section, so its former “plugin-only” matrix description has been replaced by that reference.

## Fedora and Herdr master indexes

Every entry index below links back to this matrix and directly to the other five indexes. Use the subject owner to continue; return through [[#Composition and verification routes|the composition routes]] for command-level work.

| Master index | Subject to continue with |
|---|---|
| [[00 - Toolshed Index\|Toolshed]] | Command surfaces, composition, verification and Rust practice. |
| [Herdr Habitat](obsidian://open?vault=herdr-fedora-habitat.vault&file=00%20-%20Fedora%20Master%20Index) | Workspace loadout, service bridge, architecture and automation. |
| [Fedora Kinoite](obsidian://open?vault=fedora-kinoite.vault&file=00%20-%20Fedora%20Master%20Index) | Host, Toolbx, container and operating-system boundaries. |
| [Fedora Fabric](obsidian://open?vault=fedora-fabric.vault&file=00%20Home%2FFedora%20Fabric%20Home) | Reusable prompt patterns and composable terminal workflows. |
| [Diary](obsidian://open?vault=my-diary.vault&file=00%20-%20Master%20Index) | Incident-backed reflections and the reasons behind working practices. |
| [Orchestration](obsidian://open?vault=herdr-habitat-orchistration.vault&file=00%20-%20Master%20Index) | Command seats, mission handoffs and fleet coordination records. |

Obsidian cross-vault links open the destination vault. Explicit return links provide navigation across vaults; the built-in graph and backlinks remain scoped to each open vault.

## Regenerating the reference dumps

Pair captured help with [[#Version watch|the corresponding version record]]; return to [[#Service command doors|the service table]] to select the subject.

`40 Reference/help/*.md` are verbatim captures from the **installed** builds. Refresh after any upgrade:

```bash
capture() {  # capture <binary> <outfile>
  bin="$1"; out="$2"; command -v "$bin" >/dev/null || return 0
  { echo "########## $bin — $($bin --version 2>&1|head -1) ##########"
    echo "===== TOP-LEVEL ====="; $bin --help 2>&1
    for s in $($bin --help 2>&1 | awk '/^ *(Commands|SUBCOMMANDS):/{f=1;next} /^[A-Za-z]/{f=0} f && /^ +[a-z][a-z0-9_-]*/ {print $1}' | grep -v '^help$' | sort -u); do
      echo; echo "===== SUBCOMMAND: $bin $s ====="; timeout 15 $bin "$s" --help 2>&1 | head -70
    done; } > "$out" 2>&1
}
for b in atuin fzf nu tv mempalace nvim bacon just lazygit hunk gh btm yazi podman-tui tuicr jqp herdr jq rg fd; do
  capture "$b" "40 Reference/help/$b.txt"
done
```

> mempalace and nushell use non-clap help formats — capture their subcommands explicitly (`mempalace <cmd> --help` in a loop; `nu -c 'help commands'`).

## Version watch

Read these recorded versions alongside [[#Service command doors|the service doors]]. [[#Regenerating the reference dumps|Reference capture]] describes the existing refresh recipe.

| Tool | Installed | Note |
|---|---|---|
| **atuin** | **18.12.1** | ⚠️ upstream ≥18.13 adds `mcp`, `ai`, `hex`, daemon-fuzzy — see [[atuin]] |
| bacon | 3.25.0 | `--headless` semantics differ from older docs |
| hunk | 0.20 | 0.21.0-beta available; staying on stable |
| gh-dash | 4.25.2 | |
| lazygit | 0.47 | upstream 0.64.x — Fedora copr lags |
| television | 0.15.9 | |
| nushell | 0.99.1 | |
| mempalace | 3.9.0 | |
| herdr | 0.8.2 | protocol 20 |

Related: [[00 - Toolshed Index]] · [[Tool Chaining Patterns]] · [[Tool Clusters]]
