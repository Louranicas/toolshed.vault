---
tags: [toolshed, moc, index]
created: 2026-09-02
updated: 2026-09-24
---

# 🧰 Toolshed — complete command & feature reference

<!-- habitat-highways:2026-09-08:start -->
## Corpus insight routes — 2026-09-08

Curated navigation added in this edition; the dated claims and evidence below retain their original scope.

| Purpose | Route |
|---|---|
| Cross the vault family by intent | [LLM Traversal - Cross-Vault Routes](obsidian://open?vault=herdr-fedora-habitat.vault&file=80%20Architecture%2FLLM%20Traversal%20-%20Cross-Vault%20Routes) · [file](</var/mnt/STORAGE-10TB/fedora-obsidian-vaults/herdr-fedora-habitat.vault/80 Architecture/LLM Traversal - Cross-Vault Routes.md>) |
| Choose a short route | [00 - LLM Traversal Map](obsidian://open?vault=herdr-fedora-habitat.vault&file=00%20-%20LLM%20Traversal%20Map) · [file](</var/mnt/STORAGE-10TB/fedora-obsidian-vaults/herdr-fedora-habitat.vault/00 - LLM Traversal Map.md>) |
| Connect restore to failure qualification | [Synergy - Recovery as a Test Environment](obsidian://open?vault=herdr-fedora-habitat.vault&file=80%20Architecture%2FSynergy%20-%20Recovery%20as%20a%20Test%20Environment) · [file](</var/mnt/STORAGE-10TB/fedora-obsidian-vaults/herdr-fedora-habitat.vault/80 Architecture/Synergy - Recovery as a Test Environment.md>) |
| Keep claims tied to their owner | [Synergy - Source-Owned Status and Memory](obsidian://open?vault=herdr-fedora-habitat.vault&file=80%20Architecture%2FSynergy%20-%20Source-Owned%20Status%20and%20Memory) · [file](</var/mnt/STORAGE-10TB/fedora-obsidian-vaults/herdr-fedora-habitat.vault/80 Architecture/Synergy - Source-Owned Status and Memory.md>) |
| Follow the learning cycle | [Corpus Insights - Thematic Analysis](obsidian://open?vault=herdr-fedora-habitat.vault&file=80%20Architecture%2FCorpus%20Insights%20-%20Thematic%20Analysis) · [file](</var/mnt/STORAGE-10TB/fedora-obsidian-vaults/herdr-fedora-habitat.vault/80 Architecture/Corpus Insights - Thematic Analysis.md>) |
| Connect concurrency to accepted work | [Synergy - Verified Throughput and Review Capacity](obsidian://open?vault=herdr-fedora-habitat.vault&file=80%20Architecture%2FSynergy%20-%20Verified%20Throughput%20and%20Review%20Capacity) · [file](</var/mnt/STORAGE-10TB/fedora-obsidian-vaults/herdr-fedora-habitat.vault/80 Architecture/Synergy - Verified Throughput and Review Capacity.md>) |
| Bind two views to one subject | [Synergy - Human and Agent Evidence Views](obsidian://open?vault=herdr-fedora-habitat.vault&file=80%20Architecture%2FSynergy%20-%20Human%20and%20Agent%20Evidence%20Views) · [file](</var/mnt/STORAGE-10TB/fedora-obsidian-vaults/herdr-fedora-habitat.vault/80 Architecture/Synergy - Human and Agent Evidence Views.md>) |
<!-- habitat-highways:2026-09-08:end -->


Every tool in the herdr habitat, documented to the level needed to **use all of it**: full command surfaces, features, keybindings, config, agent doors — and, more importantly, how they **compose**.

Built 2026-09-02 from three sources, in this order of authority:
1. **The installed binaries** — `--help` for every tool and subcommand, captured verbatim into `40 Reference/help/` (4,800 lines). Ground truth for *this machine*.
2. **Upstream docs and blogs** — features that never appear in `--help` (atuin's Scripts and MCP surface, television's cable channels, yazi's plugins, lazygit's custom commands).
3. **This habitat's own atuin history** — 156 real commands, analysed for frequency, piping and adjacency.

> [!warning] Where the three disagree, the binary wins
> Two documented claims turned out to be **false against the installed build**, both caught by running them: `bacon --headless` is not a one-shot verdict (it watches forever), and `atuin mcp` does not exist in 18.12.1. Both are recorded in their notes.

## Command Matrix and Fedora navigation

[[40 Reference/Command Matrix|Command Matrix — services, agent doors, pane doors and composition]] ⇄ this index. Command surfaces, composition, verification and Rust practice.

**Other master indexes:** [Herdr Habitat](obsidian://open?vault=herdr-fedora-habitat.vault&file=00%20-%20Fedora%20Master%20Index) · [Fedora Kinoite](obsidian://open?vault=fedora-kinoite.vault&file=00%20-%20Fedora%20Master%20Index) · [Fedora Fabric](obsidian://open?vault=fedora-fabric.vault&file=00%20Home%2FFedora%20Fabric%20Home) · [Diary](obsidian://open?vault=my-diary.vault&file=00%20-%20Master%20Index) · [Orchestration](obsidian://open?vault=herdr-habitat-orchistration.vault&file=00%20-%20Master%20Index) · [Jev](obsidian://open?vault=jev.vault&file=00%20-%20Jev%20Master%20Index). Each destination carries an explicit return route.

## Deployed habitat assessment — 2026-09-23

[Deployed Habitat Systems Assessment](obsidian://open?vault=herdr-fedora-habitat.vault&file=80%20Architecture%2FDeployed%20Habitat%20Systems%20Assessment%202026-09-23) ⇄ this index.
The assessment exercises the tool chain against the running system and records the exact boundary between resident services, intentional shell doors, inactive catalogue entries and `[wip]` work.
This index's formerly ambiguous short links for Atuin, Bacon, fzf, Herdr, Hunk, jqp, Just, Lazygit, MemPalace, podman-tui, tuicr and Yazi now use their qualified `10 Tools/` paths.

**Orac disk offload (2026-09-21):** `~/planning` and `~/.local/share/herdr-exec-summary` now live on the 10TB HDD; old paths are symlinks. Map and recovery: [SSD offload to 10TB HDD](obsidian://open?vault=fedora-kinoite.vault&file=SSD%20offload%20to%2010TB%20HDD) ⇄ this index. On-disk: `/var/home/Louranicas/SSD-OFFLOAD.md` ⇄ `/var/mnt/STORAGE-10TB/Louranicas-ssd-offload/README.md`.

**Kun Cheng clones (2026-09-22):** Firstmate-named axi/pipeline tools plus Jev-first pick `kun` live at `/var/mnt/STORAGE-10TB/repos/`. Index: [KUNCHENGUID_REPOS.md](file:///var/mnt/STORAGE-10TB/repos/KUNCHENGUID_REPOS.md) ⇄ this index.

Within Toolshed: [[40 Reference/Command Matrix#Service command doors|service table]] · [[40 Reference/Command Matrix#Composition and verification routes|tool and workflow companions]] · [[40 Reference/Command Matrix#Fedora and Herdr master indexes|vault ownership map]] · [[#Rust mastery|Rust mastery]].

## The tools

> **New 2026-09-04:** [[podman]] 🐋 — the full container verb surface as this habitat uses it:
> run/exec/mount, images, secrets (with the *unencrypted-by-default* caveat the docs omit),
> **`podman quadlet`** (a top-level command in 5.8.4 that the published docs do not mention),
> the Rust sandbox recipe with a scar attached to every flag, and 8 measured traps.


**W1 · Shell & memory** — [[10 Tools/atuin|atuin]] ⭐ · [[television]] · [[10 Tools/fzf|fzf]] · [[nushell]] · [[10 Tools/mempalace|mempalace]] ⭐
**W2 · Editor & build** — [[lazyvim]] · [[10 Tools/bacon|bacon]] · [[10 Tools/just|just]]
**W3 · Git & review** — [[10 Tools/lazygit|lazygit]] · [[10 Tools/hunk|hunk]] ⭐ · [[gh-dash]]
**W4 · Files & system** — [[bottom]] · [[10 Tools/yazi|yazi]] · [[10 Tools/podman-tui|podman-tui]]
**W5 · Review, data & fleet** — [[10 Tools/tuicr|tuicr]] · [[10 Tools/jqp|jqp]] · [[repo-fleet-status]]
**Spine** — [[10 Tools/herdr|herdr]] ⭐
**Judgment** — [[00 - Jev Master Index|jev]] ⭐ · [[jev-axi]] · [[firstmate]] — a model that returns calibrated probabilities instead of text (added 2026-09-18)

⭐ = unusually deep agent surface worth reading in full.

## Composition — the point of the vault

- [[Tool Chaining Patterns]] — **the nine shapes**: filter · JSON · watch · capture · two-door · escape · discovery · session · verify
- [[Clustering Shapes]] ⭐ — **chain · tree · matrix · web**: who decides the fan-out width, and the engine change that made runtime fan-out possible
- [[Tool Clusters]] — **the seven groups**, with a map and an honest list of where each is thin
- [[20 Chaining/Workflow Recipes|Workflow Recipes]] — **eleven workflow recipes**, reviewed 2026-09-06: recall, build-status preservation, aggregate Atuin analysis, reviewed script capture, worktree-aware discovery, and workload handoff.
- [[Most-Used Tools]] — what the history actually says, and its limits

> **New 2026-09-04:** [[Claim-Time Guard]] 🛡️ — a `PreToolUse` hook that fires the
> `PIPE_SWALLOWS_VERDICT` rule at the moment a command is issued, plus `gate` (right form,
> fewer keystrokes than the wrong one). Findings **F76–F78**: the settings backup and restore
> declared different sets while the integrity check read PASS; MemPalace's config was never
> backed up; a verdict line computed from different facts than its exit code.

## Field notes & workflows ⭐

- [[50 Field Notes/lukes workflows|lukes workflows]] — SOL3, assessed 2026-09-06: **about 66 GiB available**, 16.36 GiB of readable tmpfs allocation, process PSS, and current plus historical Atuin evidence. Ranked workflow recommendations, project scratch placement, session lifecycle, Kinoite/factory management, a schematic, conditional hardware advice, and an unresolved I/O-pressure question; no cleanup or session termination performed.
- [[50 Field Notes/Linux Inotify Capacity - Herdr Habitat|Linux Inotify Capacity — Herdr Habitat]] — SOL3, applied and verified 2026-09-06: host instance limit **128 → 2,048**, KDE-reported usage **92% → about 6%**, and file-event tests passed on the host and Herdr Toolbx. Includes [[50 Field Notes/Linux Inotify Capacity - Herdr Habitat#Future management narrative|future management]], Kinoite maintenance/recovery, two schematics, [[50 Field Notes/Linux Inotify Capacity - Herdr Habitat#Hardware assessment and recommendations|conditional hardware recommendations]], primary web resources, diagnostics and rollback; boot-time configuration verified without rebooting.

Built and verified by driving the toolchain hard against real code:

- [[00 - Field Findings]] — **25 corrections** from running things, grouped by failure class
- [[60 Workflows/Insights Reports - Opening Them Past the Sandbox|Insights Reports]] 📊 — where the `/insights` report actually is, why the printed `file://` link fails inside a flatpak browser, and the three doors that are already open (F144, F145). The current report's working link lives at the top of that note.
- [[60 Workflows/Mitigation Plan|Mitigation Plan]] 🛠️ — the response to what that report measured: 28 friction events, 17 of them in the agent's own scripts. Status of every class (what is already mechanised, what is open), P1–P6 with controls and falsifiers, and what is deliberately NOT being built.
  (silent wrong answers · hangs · wrong mental model · ergonomic traps · corrections to this vault)
- [[60 Workflows/00 - Workflows|Workflows]] — the compositions and layered stack
  `atuin → just → bridge → tools`, plus the [[60 Workflows/00 - Workflows#Daily operating cycle — reviewed 2026-09-06|daily operating cycle]] for project scope, scratch, concurrency, verification and session retirement.
- [[60 Workflows/Workflow Candidates - Mined From 19 Runs|Workflow Candidates]] 🧭 — 2026-09-27: 19 Workflow-tool runs mined; 12 candidates judged 3-lens (C1 partial-run census, C5 three-state vote tally, C7 pinned detached review worktree lead). Candidates only, none built.
- [[Bridge - Diagnostics to Review]] · [[Bridge - Coverage to Review]] — compiler findings and
  coverage gaps as **inline notes in the human's live diff**
- [[Cross-Workspace Review Gate]] — W2→W5 readiness verdict, proven to block
- [[Synchronised Review and Editor]] — review pane and neovim moving in lockstep
- [[Habitat Reactor]] — self-healing via herdr's previously-unused event bus
- [[Cascade Engine]] ⭐ — parallel DAGs across W1–W5 (2.24× measured), with palace-mineable receipts
- [[Autonomous Triggers]] ⭐ — one edit fires detection → cascade → annotation, no commands
- [[Knowledge Audit]] — testing the documentation like code; it found a symlink broken for a day
- [[Documented Surface and Source]] 🔗 — every documented flag resolved to **the line of source
  that defines it**; the codebase is the reference point of truth, not `--help`
- [[Cascade and Runbook Catalogue]] — every cascade and runbook, **generated from the specs**
- [[Runbooks]] ⭐ — the layer above atuin/just/cascades: one definition, generated into every entry point
- [Habitat Benchmark](obsidian://open?vault=herdr-fedora-habitat.vault&file=80%20Architecture%2FFirstmate%20and%20Habitat%2F07%20-%20Habitat%20Benchmark) — installed Rust measurement across fourteen facets, with baseline evidence and explicit rollout gaps; the note links back to this index.
- [[Fabric Bash Command Plane]] 🧵 — typed Fabric plans translated into reviewable Bash, Just and runbook surfaces across W1–W5; [seven-facet assessment and integrated recommendations](obsidian://open?vault=fedora-fabric.vault&file=04%20Workflows%2FFabric%20Habitat%20Assessment%20and%20Integration)
- [[Fabric Habitat 90-Point Promotion and Practice]] 🎯 — a measured route from 79 toward 92, sustained W1–W5 dry-run practice, adversarial policy cases and mutation evidence
- [[Factory Roster Expansion - DevOps Toolbox]] — repository assessment, qualified Arena Hurl/ShellCheck/Restic capabilities, and proposed W6–W7 delivery/recovery roles
- [[Habitat Introspection]] ⭐ — the habitat profiling itself from its own receipts, and the 620→375 ms fix that came out of it
- [[Sandbox Fanout and Fusion]] ⭐ — isolated podman workers generating code modules, fused and verified
- [[Arena Practice Ground]] — the sandbox all of it was proven in

## The toolkit

- [[skills]] 🧭 — cross-agent skill router: durable habitat-authored skills,
  Codex system and plugin skills, their trust boundaries, and where each source
  of truth lives
- [[70 Toolkit/skills#Habitat Context|Habitat Context]] — executive summary, bounded cross-vault context preparation, progressive disclosure and tested evidence limits.
- [[70 Toolkit/Skill Usage Guide|Skill Usage Guide]] — examples and agent-use guidance for all 51 installed skills, with session availability and review findings (2026-09-06)
- [[70 Toolkit/Justfile Update Check|Justfile Update Check]] — monthly source-change and reciprocal-link report; [[70 Toolkit/skills#Runbooks and justfiles|runbooks and justfiles documentation]] links to the maintained code map.
- [[MCP Servers]] 🔌 — two servers on protocol **2026-07-28** exposing the habitat as live tools;
  progressive disclosure applied to `tools/list` vs `resources/read`
- [[Authored Skills]] 🎓 — four Claude Code skills distilled from these findings, built with
  progressive disclosure (76% of the material deferred to `reference/`)
- [[Code Anchors - Notes That Land on Source]] ⚓ ⭐ — the vaults are claims about the codebase;
  anchors carry an `expects` fragment so a claim that has gone false is **detectable**, not just
  a stale link. **Notes update with every deployment** — `just doc-anchors`
- [[Weight Matrix - Which Gate Bore the Weight]] ⚖️ ⭐ — mutation testing applied to the
  habitat's own gates: which catch nothing, which are irreplaceable, and the minimal set;
  plus `weightweb`, the clustered webbed tree that closes bidirectionally through W3
- [[Axiom Conformance]] ⬡ ⭐ — nine axioms run against the **live** W1–W5 doors; found and fixed
  a backup that would have silently lost the cockpit's respawn plugin on restore
- [[Shape-Directed Tool Chaining]] 🔗 ⭐ — route by what a tool **emits**, not its name; the
  editor as a *source* via nvim RPC; **battern** = one pattern across a named cluster in parallel
- [[Assimilation - Rules That Fire]] ⚙️ ⭐ — the habitat's ~130 inherited antipatterns and 48 field
  findings turned into **detectors that execute**; four tiers across W1–W5, negative controls
  mandatory, receipts that cannot self-certify
- [[Forge - Deployment Framework]] 🔨 ⭐ — the **habitat factory prototype**: a zero-dependency
  Rust framework that deploys a workspace from a blueprint. 5 crates, 445 tests, clippy
  pedantic+nursery clean, verified twice — host and five isolated podman sandboxes
- [[00 - Habitat Toolkit]] 🧰 — the **six tools built here** (`habitat`, `-reactor`, `-cascade`,
  `-trigger`, `-sandbox`, `-fleet`): full command surfaces, what each exists to solve, durability

## Rust mastery

- [[40 Reference/rust-mastery/README|Rust corpus folder index]] · [[40 Reference/rust-mastery/2026-09-06/Source and Reading Map|Source and Reading Map]] · [[40 Reference/rust-mastery/2026-09-06/Learning Status and Next Steps|Learning Status and Next Steps]].

For service selection and vault ownership, return to [[#Command Matrix and Fedora navigation|Command Matrix and Fedora navigation]].

- [[40 Reference/Perfecting Rust - Performance Engineering|Perfecting Rust — Performance Engineering]] — the 19-chapter Performance Book synthesis and its connected learning map.
- [[40 Reference/Perfecting Rust - Performance Engineering#Benchmark the question you actually care about|Benchmarking]] · [[40 Reference/Perfecting Rust - Performance Engineering#Profile to explain the cost|Profiling]] · [[40 Reference/Perfecting Rust - Performance Engineering#Understand ownership and heap costs|Heap allocations and ownership]].
- [[40 Reference/Perfecting Rust - Performance Engineering#Your local Rust bookshelf|Local books and edition checks]] · [[40 Reference/Perfecting Rust - Performance Engineering#Builders worth studying|Rust authors and builders]] · [[40 Reference/Perfecting Rust - Performance Engineering#Practice until the reasoning is reproducible|Practice program]].
- [[40 Reference/rust-mastery/2026-09-06/README|Runnable lab, source ledger and measurements]] — reciprocal routes to the tools and workflows used for practice.

Across vaults: [Habitat master index](obsidian://open?vault=herdr-fedora-habitat.vault&file=00%20-%20Fedora%20Master%20Index) ⇄ [Kinoite master index](obsidian://open?vault=fedora-kinoite.vault&file=00%20-%20Fedora%20Master%20Index); both carry the Rust corpus route.

## Reference

- [[40 Reference/herdr-keybindings/2026-09-06/README|Herdr Ctrl+Alt+End shortcut — 2026-09-06]] — user-confirmed persistent Left/Right tab navigation after Ctrl+Alt+End, Ghostty key-table configuration, live reload evidence, backups and rollback.
- [[40 Reference/workflow-review/2026-09-06/README|Workflow documentation review — 2026-09-06]] — applied note corrections, inspected source hashes, runtime limitations, validation and a reviewable change patch; no workflows executed or supervisors changed.
- [[40 Reference/lukes-workflows/2026-09-06/README|Luke's workflow evidence — 2026-09-06]] — proportional memory, tmpfs ownership metadata, Herdr layout, installed Atuin query receipt, deduplicated Fedora histories and an older archive's aggregate analysis; methods, coverage gaps, reusable read-only scripts and SHA-256 manifest. No raw history imported.
- [[40 Reference/inotify/2026-09-06/README|Inotify capacity evidence — 2026-09-06]] — before/after measurements, workspace context, exact host configuration, audit/apply/rollback/verification scripts, functional-test receipts, hardware/pressure and Kinoite state snapshots, source provenance, and checked SHA-256 manifest.
- [[Command Matrix]] — every service's agent door, pane door, JSON capability, cluster
- `40 Reference/help/` — verbatim `--help` capture per tool (regeneration script in the matrix)

## The three findings that matter most

1. **Chaining is nearly absent.** In 156 recorded commands there was exactly **one** genuine pipe pair (`herdr | jqp`). Sixteen capable tools were being used as sixteen destinations. Everything in `20 Chaining/` exists to close that.
2. **`atuin scripts` closes the automation loop.** `--last N` promotes *the sequence you just ran* into a named, minijinja-templated, synced script. It is the natural capture point for every recipe here — and it is available in the installed build.
3. **Upstream atuin is an agent platform this build predates.** `atuin mcp` exposes history as native agent tools (`atuin_history`, `atuin_output`) with author-tagging that distinguishes *your* commands from an agent's. Not in 18.12.1 — see [[10 Tools/atuin|atuin]] for the upgrade decision.

## Pi planning synergy — 2026-09-06

| Toolshed responsibility | Pi planning counterpart |
|---|---|
| [[skills]] — instruction routing and tool boundaries | [pi.vault — Home](../pi.vault/Home.md) ⇄ [Herdr Integration](../pi.vault/20%20Habitat/Herdr%20Integration.md): specialised harness composition and evaluation design; no skills imported or plugins installed |
| [[Runbooks]] and [[10 Tools/just|just]] — one procedure, discoverable thin doors | [Genesis Justfiles and Runbooks](obsidian://open?vault=pi.vault&file=95%20Genesis%2FGenesis%20Justfiles%20and%20Runbooks) ⇄ Pi Home: GR16 planning contracts, inert inspection and effect-aware recovery; no runner activation |

## Related vaults

- [fedora-fabric vault](obsidian://open?vault=fedora-fabric.vault&file=00%20Home%2FFedora%20Fabric%20Home) 🧵 — reusable Fabric patterns and the reciprocal command-plan contract
- [herdr habitat vault](obsidian://open?vault=herdr-fedora-habitat.vault&file=00%20-%20Fedora%20Master%20Index) — where these tools live: workspaces, panes, the service bridge, the loadout
- [fedora-kinoite vault](obsidian://open?vault=fedora-kinoite.vault&file=00%20-%20Fedora%20Master%20Index) — the OS constraints that shape them (toolbox boundary, `flatpak-spawn --host`, durability)
- [my-diary vault](obsidian://open?vault=my-diary.vault&file=00%20-%20Master%20Index) 📔 — the judgment layer: why a rule exists, which findings here became executable detectors, and the recurring mistakes that produced them
- [What the Workflow Is Worth](obsidian://open?vault=my-diary.vault&file=Reflections%2FWhat%20the%20Workflow%20Is%20Worth) ⚖️ — this register **measured**, 2026-09-11: F1–F140 with no gaps, and **110 of the 140 carry no date in their body**, in the corpus P17 was written for. `just corpus-health` is the check; the median finding has grown 45 → 335 words since F1–F20. Return route to the toolshed at both ends.

This vault sits inside `fedora-obsidian-vaults/`, so `mempalace mine .` picks it up with the others — every command on these pages is semantically retrievable via `habitat recall`.

## Turso community-video findings — 2026-09-23

[Community Video Findings - DevOps Toolbox libSQL](obsidian://open?vault=turso.vault&file=10%20Concepts%2FCommunity%20Video%20Findings%20-%20DevOps%20Toolbox%20libSQL%202026-09-23) ⇄ this index — a Turso-vault note capturing the DevOps Toolbox SQLite-fork video with Fabric (local Ollama) and reconciling it against [docs.turso.tech/introduction](https://docs.turso.tech/introduction). Relevant here as a worked [[Fabric Bash Command Plane|Fabric]] `--transcript`/`youtube_summary` capture; video claims are kept separate from official docs. Supersedes the 2026-09-22 capture, and records that today's local-model summary again garbled the product name and folded the sponsor ad into a features bullet — read claims from the raw transcript.
[Jev in Turso Workflows](obsidian://open?vault=turso.vault&file=20%20Build%20Guides%2FJev%20in%20Turso%20Workflows) ⇄ [Jev: Turso](obsidian://open?vault=jev.vault&file=70%20Workflows%2FTurso) ⇄ this index — Turso retrieves; Jev judges the snippet; code writes the typed answer back.

[Architectural schematic](obsidian://open?vault=turso.vault&file=50%20Agent%20Knowledge%20System%2FSchema%20Sketch#Architectural%20schematic) ⇄ this index — private read-only Unix socket and API for the habitat database. Not the engine control socket. Not the Turso catalogue. Cloud MCP and MCPv2 are not connected.

## Planwright planning-resource synergy — 2026-09-05

| Toolshed workflow | Habitat resource |
|---|---|
| [[skills]] — personal Codex Planwright, proof process and examples | [Planwright HTML Resources](obsidian://open?vault=herdr-fedora-habitat.vault&file=95%20Genesis%2FPlanwright%20HTML%20Resources) — detailed Genesis planning exemplar; reciprocal pair with Habitat master index |

<!-- orchestration-master-return:start -->
## Herdr Habitat Orchestration — reciprocal index

[Orchestration Master Index](obsidian://open?vault=herdr-habitat-orchistration.vault&file=00%20-%20Master%20Index) ⇄ this index. Cmd1–Cmd3, Fleet-Alpha through Fleet-Delta, pane identities, vision, and mission/handoff records.

This vault contributes: Tool command surfaces, workflow composition, and verification utilities.
<!-- orchestration-master-return:end -->

<!-- cmd3-procedure-review-20260906 -->
## Engineering atlas and procedure review — 2026-09-06

[Engineering planning atlas](obsidian://open?vault=herdr-fedora-habitat.vault&file=95%20Genesis%2Fengineering-atlas%2FSTART_HERE) covers 22 module specifications, 22 schematics, 32 quality standards, meaningful integration/mutation testing, and explicit Rust excellence, SLOP, DRIFT and OVER-ENGINEERING controls. The 116 original planning task records retain their evidence states.

[Justfiles and runbooks review](obsidian://open?vault=herdr-fedora-habitat.vault&file=95%20Genesis%2FJustfiles%20and%20Runbooks%20Review%202026-09-06) ⇄ this index. Completed source/navigation review: five justfiles / 129 recipes parsed, six installed runbooks inventoried, and the stale catalogue refreshed to 13 cascades / six runbooks with source fingerprints and a non-writing freshness check. Only two Arena Just runbook wrappers exist; installed-runner defects and uninspected Atuin registration remain explicit. No operational recipe, runtime repair or promotion is certified by this review. The review links both Fedora master indexes and the Toolshed index.

<!-- astra-prompt-library-20260908:start -->
## ASTRA prompt library — 2026-09-08

| Resource | Relationship |
|---|---|
| [[herdr-habitat-prompt-library\|ASTRA prompt library]] ⇄ this note | Canonical library: starter prompt, 11 coding cards, ASTRA guidance, SLOP and structure review, and evidence-ranked research/grey literature. Authored prompts; comparative task evaluation remains open. |
<!-- astra-prompt-library-20260908:end -->


<!-- herdr-engineering-engine-v3-20260915:start -->
## Herdr Engineering Engine v3 — dedicated planning atlas · 2026-09-15

[Vault Home](obsidian://open?vault=herdr-engineering-engine-v3.vault&file=Home) · [Master index](obsidian://open?vault=herdr-engineering-engine-v3.vault&file=00%20-%20Master%20Index) · [local Home](</var/mnt/STORAGE-10TB/fedora-obsidian-vaults/herdr-engineering-engine-v3.vault/Home.md>) · [reciprocal context map](</var/mnt/STORAGE-10TB/fedora-obsidian-vaults/herdr-engineering-engine-v3.vault/90 Evidence/Cross-vault Context.md>) ⇄ this index.

The dedicated vault contains the reviewed end-to-end Rust/Julia plan: 22 modules, six synergy clusters, 20 bidirectional contextual flows, ten API mappings, seven IPC custody records, 21 proposed command/tool actions, 24 schematics and 29 implementation/qualification tasks. Full acceptance contracts, exact research snapshots and review limitations accompany the native notes. Toolshed commands, skills and chaining is the contribution of this source hub; source ownership and historical claim dates remain intact.

The final review tightens roster authority, candidate-code verification isolation, evidence durability, context relationship coverage, literal template handoff, drift-baseline acceptance and meaningful gate qualification. This is planning/documentation only: engine implementation remains unstarted. The vault folder does not imply app registration or a change to Prime's five pinned vaults. Earlier family-count tables retain their historical scope.
<!-- herdr-engineering-engine-v3-20260915:end -->

<!-- hermes-recovery-location-20260915:start -->
## Hermes recovery location — 2026-09-15

[[60 Workflows/Hermes Recovery Location|Hermes Recovery Location]] ⇄ [habitat canonical](obsidian://open?vault=herdr-fedora-habitat.vault&file=40%20Agents%2FHermes%20Recovery%20Location%202026-09-15) ⇄ [kinoite spindle placement](obsidian://open?vault=fedora-kinoite.vault&file=Hermes%20Recovery%20on%20the%20Spindle). `~/.hermes/recovery` remains the address; it is a symlink onto `/var/mnt/STORAGE-10TB/home-overflow/hermes-recovery/`. NVMe pointer: `~/.hermes/RECOVERY-LOCATION.md`. Commands live in the Toolshed note; the 2026-09-05 recovery event stays on [Taco Hermes Corpus Recovery](obsidian://open?vault=herdr-fedora-habitat.vault&file=40%20Agents%2FTaco%20Hermes%20Corpus%20Recovery).
<!-- hermes-recovery-location-20260915:end -->

<!-- mempalace-location-20260915:start -->
## MemPalace location — 2026-09-15

[MemPalace Location 2026-09-15](obsidian://open?vault=herdr-fedora-habitat.vault&file=70%20Toolchain%2FMemPalace%20Location%202026-09-15) ⇄ [MemPalace on the Spindle](obsidian://open?vault=fedora-kinoite.vault&file=MemPalace%20on%20the%20Spindle) ⇄ this index. `~/.mempalace` remains the address; it is a symlink onto `/var/mnt/STORAGE-10TB/home-overflow/mempalace/`. NVMe pointer: `~/.MEMPALACE-LOCATION.md`. Commands stay on the habitat [Tool - MemPalace](obsidian://open?vault=herdr-fedora-habitat.vault&file=70%20Toolchain/Tool%20-%20MemPalace) note (path in that vault).
<!-- mempalace-location-20260915:end -->


<!-- firstmate-habitat-atlas:20260924 -->
## Firstmate and Habitat architecture — 2026-09-24

[End-to-End Atlas](obsidian://open?vault=herdr-fedora-habitat.vault&file=80%20Architecture%2FFirstmate%20and%20Habitat%2F00%20-%20End-to-End%20Atlas) ⇄ this index.

<!-- habitat-reliability-plan:20260925 -->
[Habitat Reliability and Integration Plan](obsidian://open?vault=herdr-fedora-habitat.vault&file=80%20Architecture%2FFirstmate%20and%20Habitat%2F11%20-%20Habitat%20Reliability%20and%20Integration%20Plan) ⇄ this index. The full H00-H14 plan preserves separate evidence, recovery, integration and engine-owner gates; implementation remains planned.
Ten schematics map execution, supervision, deployment, data ownership and the WIP boundary; exact evidence and current-versus-supported distinctions are attached.


<!-- reliability-schematics:20260925 -->
[Habitat reliability schematics](obsidian://open?vault=herdr-fedora-habitat.vault&file=80%20Architecture%2FFirstmate%20and%20Habitat%2F12%20-%20Reliability%20Schematics) — twelve source-bound diagrams, exact H00-H14 dependency/owner coverage and recovery/authority reading aids; runtime packages remain planned.
<!-- /reliability-schematics:20260925 -->

<!-- practice-map:20260927 -->
## Practice map and deployment kit — 2026-09-27

[Practice Map — What Earns Its Keep](obsidian://open?vault=herdr-fedora-habitat.vault&file=50%20Automation%2FPractice%20Map%20-%20What%20Earns%20Its%20Keep) · [file](</var/mnt/STORAGE-10TB/fedora-obsidian-vaults/herdr-fedora-habitat.vault/50 Automation/Practice Map - What Earns Its Keep.md>) ⇄ this index. Which tools, reflexes and workflows measurably earned their keep, with counts re-checked at the source, and a deployment kit for the next codebase.
<!-- /practice-map:20260927 -->

<!-- mvp-agents-tooling:20260927 -->
## MVP agents and tooling — 2026-09-27

[MVP Agents and Tooling](obsidian://open?vault=herdr-fedora-habitat.vault&file=40%20Agents%2FMVP%20Agents%20and%20Tooling) ⇄ this index. The tooling table (gate, hee3-gate, hee3-precount, hee3-review-coverage, the chain scripts, reflexes, doc-anchors, the Workflow tool, jev-*) with the incident that proves each and its known gap.
<!-- /mvp-agents-tooling:20260927 -->
