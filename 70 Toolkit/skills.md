---
tags: [toolshed, skills, agents, codex, claude-code, routing]
created: 2026-09-04
updated: 2026-09-09
---

# 🧭 skills — instruction routers for agents

A skill is a loadable instruction package: it tells an agent **when a workflow
applies, what evidence to inspect, which tools to use, and what must be true
before completion can be claimed**. It is not the tool itself.

> [!important] Four things that sound similar
> - A **skill** supplies procedure and judgment.
> - A **tool** performs one callable operation.
> - An **MCP server** exposes tools or resources across a protocol boundary.
> - A **plugin** bundles skills, MCP servers, apps, or supporting assets.

Availability is session-dependent. An installed skill is not necessarily
exposed to every agent or every run; the active session's skill catalog is the
authority.

## Review and examples — 2026-09-06

[[70 Toolkit/Skill Usage Guide|Skill Usage Guide]] reviews every installed skill
with an example request and guidance for how agents can use it effectively.
Keep this note as the router; open the relevant guide section, then the selected
skill's current entrypoint and required references.

| Scope reviewed | Installed | In this Codex session catalog |
|---|---:|---:|
| Habitat Claude skills | 5 | 0 |
| Codex system skills | 6 | 5 |
| Personal Codex workflows | 3 | 3 |
| Plugin workflow skills | 17 | 17 |
| Artifact templates | 20 | 0 |
| **Total** | **51** | **25** |

These counts preserve the original 2026-09-06 review snapshot, before the
Context Handoff addition below. Catalog
exposure does not establish working connectors or runtime dependencies. The
review checked source instructions and template resource presence; it did not
execute each workflow.

**Added after that review:** [[#Personal Codex `$context-handoff` — created 2026-09-06|Context Handoff]]
is installed and exposed in the current Codex session. It saves a Markdown
restart pointer and rebuilds context through Prime, the master index and a
focused deployment-atlas reading sequence.

- [[70 Toolkit/Skill Usage Guide#Personal Codex workflows|Personal workflows]] — orient, plan, reconcile, and code.
- [[70 Toolkit/Skill Usage Guide#Habitat skills|Habitat skills]] — operations, CLI evidence, containers, claims, and vaults.
- [[70 Toolkit/Skill Usage Guide#Codex system skills|System skills]] — images, product guidance, plugins, reviews, and skill management.
- [[70 Toolkit/Skill Usage Guide#Browser, visuals, and artifact files|Browser and artifacts]] — select the correct output and interaction surface.
- [[70 Toolkit/Skill Usage Guide#Connected Google files|Google workflows]] — file discovery, native structure, ranges, and comments.
- [[70 Toolkit/Skill Usage Guide#Sites, research, and reusable templates|Sites, research, and template creation]] — build, publish, investigate, and retain designs.
- [[70 Toolkit/Skill Usage Guide#Installed artifact templates|All twenty templates]] — separate document, presentation, and spreadsheet examples.
- [[70 Toolkit/Skill Usage Guide#Runbooks and justfiles|Runbooks and justfiles]] — procedure discovery, repository recipes, current examples, and execution evidence.
- [[70 Toolkit/Skill Usage Guide#Useful combinations|Workflow combinations]] and [[70 Toolkit/Skill Usage Guide#Review findings and limits|review findings]] — handoffs, routing conflicts, and evidence limits.

**Added 2026-09-09:** [[#Habitat Context|Habitat Context]] — compact, source-backed context from selected vault notes, code, Justfiles and runbooks.

## Which skill home to use

| Need | Source of truth | Durability |
|---|---|---|
| Habitat-specific judgment and operating practice | `~/.claude/skills/<name>/SKILL.md` | User-authored; captured by habitat backup |
| A personal Codex workflow | `~/.codex/skills/<name>/SKILL.md` | User-authored; keep outside `.system` |
| Codex product behavior and skill management | `~/.codex/skills/.system/` | Product-managed; do not hand-edit |
| Browser, artifacts, connected apps, Sites, or research | `~/.codex/plugins/cache/.../skills/` | Versioned cache; replaceable, not an authoring home |

The cache path can change after an update. Link to the skill by name and purpose,
not by a cache-version directory.

## Habitat-authored Claude skills

These five are the durable local knowledge layer:

| Skill | Load when | Owns |
|---|---|---|
| `claim-discipline` ⭐ | Before saying done, clean, verified, wired, or deployed | Evidence thresholds and false-pass prevention |
| `habitat-ops` | Working with W1–W5, panes, cascades, services, or repair | Cockpit operation |
| `cli-ground-truth` | A flag, zero, hang, or documented behavior is uncertain | Probe-first CLI truth |
| `kinoite-containers` | Crossing toolbox/host boundaries or debugging mounts | Fedora Kinoite and container durability |
| `vault-mining` | Editing, linking, checking, or mining any vault | Note shape, retrieval, backlinks, and cross-vault rules |

See [[Authored Skills]] for their progressive-disclosure layout, scars, and
reference files.

## Codex system skills installed here

- `imagegen` — generate or edit bitmap imagery.
- `openai-docs` — current OpenAI and Codex documentation.
- `plugin-creator` — scaffold and update Codex plugins.
- `review-agent` — structured code-review workflow when exposed.
- `skill-creator` — create or update a personal Codex skill.
- `skill-installer` — install curated or repository-hosted skills.

System skills are managed under `~/.codex/skills/.system`. Personal work should
be created beside that directory, never inside it.

## Personal Codex `$prime` skill

[[#Prime and Habitat Context|Comparison with Habitat Context and the conditional chaining workflow]].

`$prime` is the read-only cartographer for this machine's pinned Fedora knowledge
vaults. In Codex, invoke it as `$prime`; `/prime` is the workflow name used in
the package and in conversation. Its entrypoint is:

```text
~/.codex/skills/prime/SKILL.md
```

The skill answers *where should I look, what did I actually read, and how high
can this claim reach?* It does not ingest every note. It proves the registered
vaults, chooses the narrowest map for the requested focus, follows one relevant
link at a time, and produces a receipt naming its evidence and unread gaps.

### The five pinned vaults

| Obsidian ID | Focus name | Owns |
|---|---|---|
| `b41837ff933fdb5f` | `fabric` | Fabric patterns, Fedora setup, terminal workflows, and Obsidian capture |
| `690f76c62b219554` | `kinoite` | Immutable OS, rpm-ostree, KDE, toolbox, Podman, and recovery |
| `e664945624dab26a` | `habitat` | Herdr architecture, operations, automation, toolchain, and session maps |
| `ac9a363b333ab70e` | `toolshed` | Command surfaces, composition, workflows, findings, gates, and toolkit notes |
| `9a7bb950eb612f00` | `diary` | Incident-backed reflection and judgment; evidence, never policy |

These IDs are persistent **opaque registry keys**. They are verified against
Obsidian's current ID→path mapping; they must not be recomputed from a vault's
current path after a migration.

The skill's pinned set is intentionally closed. A narrative master index may
mention an additional vault such as Turso; that does not silently add it to
`$prime`. An unpinned corpus requires an explicit exact path after `--`.

### How progressive disclosure works

| Level | What enters context |
|---|---|
| L0 | The small `SKILL.md` entrypoint and its hard stops |
| L1 | The offline registration proof and deferred vault routing map |
| L2 | One entry map per selected vault; all five only for family focus |
| L3 | One note routed by the focus |
| L4 | Current source, configuration, or read-only state required by a live claim |
| L5 | An exact file or directory after `--`, read only through the containment gate |

This is **priming, not activation**. `$prime` does not edit vaults, open Obsidian
links, enable plugins, execute commands copied from notes, start services,
deploy, commit, or push. Green navigation proves neither freshness nor PASS.

### Exemplars

| Need | Example prompt | Expected disclosure |
|---|---|---|
| Map the whole pinned family | `Use $prime to map the Fedora vault family.` | Prove all five registrations; read only their entry maps |
| Learn Fabric provider setup | `Use $prime fabric provider setup for Codex.` | Fabric home → the one provider-setup note |
| Investigate a Kinoite container issue | `Use $prime kinoite podman bind mounts.` | Kinoite index → one Podman note; verify live syntax separately |
| Resume Herdr work | `Use $prime habitat session and show documented versus observed state.` | Habitat home → session map → read-only current-state evidence |
| Find a gate or tool workflow | `Use $prime toolshed gate claim-time guard.` | Toolshed index → the named gate/workflow note |
| Compare a cross-vault concept | `Use $prime cross-vault sandboxing across kinoite, toolshed, and diary.` | Three entry maps → at most one routed note in each selected vault |
| Load reflective judgment deliberately | `Use $prime diary principles about cold verification.` | Diary entry maps → one explicitly selected principle/reflection |
| Admit one Markdown source | `Use $prime toolshed -- "/exact/path/to/note.md".` | Admit the file, then securely read only that file |
| Admit a codebase or module | `Use $prime habitat -- "/exact/path/to/codebase".` | Admit the directory, list one level at a time, then securely read selected contained files |

The arguments can use a focus name or its Obsidian ID. Multiple IDs select
multiple **entry maps**, never a full-vault dump.

### Enforced `--` path containment

An exact-path corpus is consumed only through `prove-paths.py`. The script is
both the gate and the reader; an agent must not validate a path and then bypass
the result with `cat`, `sed`, `rg`, or a language runtime.

```bash
cd ~/.codex/skills/prime

# File or folder admission. A folder can be a codebase or module root.
python3 scripts/prove-paths.py admit -- "/exact/path"

# Map one directory level without following links.
python3 scripts/prove-paths.py list --root "/exact/path" -- "/exact/path/module"

# Read one selected UTF-8 text file through the admitted root.
python3 scripts/prove-paths.py read --root "/exact/path" -- "/exact/path/module/file.rs"

# A file admission authorizes only itself.
python3 scripts/prove-paths.py read --root "/exact/note.md" -- "/exact/note.md"
```

Containment is descriptor-relative and uses `O_NOFOLLOW` for every opened path
component, so `..`, an intermediate symlink, a final symlink, and a check/read
race cannot widen the admission. `list` is immediate and bounded (200 entries by
default). `read` accepts regular UTF-8 text without NUL bytes and defaults to
512 KiB; explicit increases stop at 16 MiB. Obsidian configuration/cache roots
and every pinned vault's `.obsidian/` directory remain unavailable.

Only `status: ok` authorizes the next step. `missing` means the named object is
absent; `unavailable` means policy, containment, type, symlink, encoding, or
size refused it. Admission proves bounded availability, never truth or authority.

### Proof and receipt

The deterministic proof is offline and read-only:

```bash
cd ~/.codex/skills/prime
python3 scripts/prove-vaults.py
python3 scripts/prove-paths.py admit -- "/exact/file-or-directory"
python3 -m unittest scripts/test_prove_paths.py
```

It distinguishes `ok`, `missing`, and `unavailable`, then stops at existence and
registration. A successful proof does not establish note accuracy or live
state. Every completed prime reports:

- focus and registry proof outcome;
- vault IDs and exact note paths actually read;
- a concise mental model;
- documented, observed, inferred, and unread state kept distinct;
- contradictions and missing evidence under `gaps`; and
- the fixed claim ceiling: cartography only, not activation, mutation, or PASS.

## Codex plugin skill families installed here

- **Browser and explanation:** in-app browser control and interactive
  visualization.
- **Artifacts:** documents, PDFs, presentations, spreadsheets, live Excel, and
  reusable artifact templates.
- **Google Drive:** Drive, Docs, Sheets, Slides, and comment workflows.
- **Sites:** site building and production hosting.
- **Research and administration:** deep research and plugin management.
- **Template packs:** purpose-built report, memo, dashboard, planning, and
  financial-workbook templates.

These are plugin-provided capabilities. Their trigger descriptions decide when
they load; a task should use the smallest set that completely covers it.

## Runbooks and justfiles

Skills guide agent judgment; runbooks define coordinated procedures; justfiles
expose a repository's executable recipes. See
[[70 Toolkit/Skill Usage Guide#Runbooks and justfiles|Runbooks and justfiles in the usage guide]]
for current Arena examples, inspection commands, source ownership, and how agents
combine these layers with plans and implementation checks.

Read [[60 Workflows/Runbooks|Runbooks]] for the procedure model,
[[10 Tools/just|just]] for recipe syntax, and
[[40 Reference/Cascade and Runbook Catalogue|Cascade and Runbook Catalogue]] for
the generated inventory. The guide distinguishes that older snapshot from the
six current definitions and two generated Just wrappers inspected on 2026-09-06.

### Bidirectional source links and monthly checks

[Justfile source map](file:///var/home/Louranicas/fedora-arena/justfiles/README.md)
links to all four current justfiles and returns to this note, the usage guide,
and the Just reference. Each justfile also carries an Obsidian return link to the
usage guide. These are links to the actual code, not copies of its recipes.

The `toolshed-justfile-monthly` cron job checks local justfiles, runbook definitions,
the installed runner, and reciprocal documentation links on the first day of each
month at 09:00 local time (Australia/ACT), using `0 9 1 * *`. It runs through the
existing Hermes cron-only timer, without a model or messaging delivery.

Results: [[70 Toolkit/Justfile Update Check|Justfile Update Check]]. Changes remain
visible until reviewed and explicitly accepted into the baseline. The source map
contains manual-check, acceptance, and job-management commands. The job reports
source changes; it does not run recipes, fetch updates, or upgrade software.

## Skill anatomy

A good `SKILL.md` contains:

1. a narrow description written as a trigger list;
2. the invariants and stop conditions that must always load;
3. exact routing to tools, scripts, templates, or references;
4. deferred detail in `reference/` when the material is situational; and
5. a verification path that can falsify the completion claim.

The durable lesson from this habitat is **route rather than repeat**. One fact
has one authoritative home; other skills link to it. Expensive failure knowledge
belongs in the skill, while discoverable happy-path help can stay deferred.

## Inventory commands

```bash
rg --files ~/.claude/skills -g 'SKILL.md'
rg --files --hidden ~/.codex/skills -g 'SKILL.md'
rg --files --hidden ~/.codex/plugins/cache -g 'SKILL.md'
```

Run the inventory before claiming a skill is available. Files on disk establish
installation, while the current agent session establishes exposure.

## Pi harness creation planning — 2026-09-06

[pi.vault — Herdr Integration](../../pi.vault/20%20Habitat/Herdr%20Integration.md) ⇄ this router. Proposed engine selects individually reviewed task capabilities rather than globally importing all Codex/Claude skills. [Pi capability recommendations](../../pi.vault/30%20Resources/Extensions%20Skills%20and%20Plugins.md) are planning candidates, not installed or qualified extensions.

## Relationships

[[Authored Skills]] · [[MCP Servers]] · [[00 - Habitat Toolkit]] ·
[[00 - Toolshed Index]]

## Personal Codex `$planwright` — recreated 2026-09-05

Planwright converts intent and existing requirements into an evidence-backed task graph plus a
compact human decision ledger. Rich output is one offline HTML resource with an embedded JSON
spine and Markdown fallback. It plans; it does not authorize coding, deployment or publication.

Entrypoint: `/var/home/Louranicas/.codex/skills/planwright/SKILL.md`.
Progressive disclosure: entrypoint → structured plan contract → HTML QA only when needed →
examples only for onboarding. No fixed legacy model roster, fleet services or autonomy score.

Examples:

- “Use $planwright on this approved plan; create detailed HTML/JSON/Markdown resources, without coding.”
- “Use /planwright to plan W1/W2 hardening only; preserve the other agent's W3+ work.”
- “Use $planwright to refresh this resource, checking source drift and showing unresolved gates.”

The script `scripts/plan_proof.py --root ROOT --target FILE_OR_DIRECTORY --bundle BUNDLE --stem NAME`
enforces exact contained reads, source digests, acyclic task/packet graphs and HTML/JSON security
invariants. The target can be a file or directory. This is **not a write sandbox**: approved edits
and final-destination verification remain necessary. Missing validators stay explicitly unavailable;
missing independent reviewers never become invented AUTO confirmations.

The first rich [Genesis HTML exemplar](obsidian://open?vault=herdr-fedora-habitat.vault&file=95%20Genesis%2FPlanwright%20HTML%20Resources) has 17 obligations / 51 packets / eight gates,
with search, filters, negative controls, closure rules and non-anthropocentric resource limits.
That Habitat hub links back here. [[00 - Toolshed Index]] records the cross-vault pairing.
Disk installation and current-session skill exposure remain distinct.

## Personal Codex `$consolidate-and-code` — created 2026-09-06

Consolidate learnings, update standards and conventions, refer to plans and
verify progress, then start coding. Use this workflow when resuming implementation
with accumulated context that needs to be reconciled with the project records.

Entrypoint: `/var/home/Louranicas/.codex/skills/consolidate-and-code/SKILL.md`.

### Invocation

```text
Use $consolidate-and-code to consolidate learnings, update standards and
conventions, verify progress against the plan, and start the next authorized
coding task.
```

### Workflow

1. Recover the active request, accepted decisions, applicable `AGENTS.md`,
   relevant plans and standards, and working-tree state.
2. Consolidate evidence-backed learnings, separating durable decisions from
   hypotheses, temporary workarounds, and open questions.
3. Update the existing authoritative standards and conventions where supported;
   preserve their structure and avoid duplicating guidance.
4. Verify plan tasks, dependencies, and acceptance criteria against current code
   and validation evidence; correct unsupported progress claims.
5. Implement the next authorized task in the same turn, run appropriate checks,
   and carry the requested scope through to completion. Update the progress record
   with the outcome, evidence, and remaining gaps.

### Progressive disclosure

Paths below are relative to `~/.codex/skills/consolidate-and-code/`.

| Resource | Load when | Purpose |
|---|---|---|
| Name and description | Skill selection | Identify the consolidation-to-implementation workflow |
| `SKILL.md` | The skill applies | Core workflow, scope, completion, and reference routing |
| `references/updating-standards.md` | A lesson may become a persistent rule or conflicts with guidance | Choose the authoritative destination, scope the rule, and resolve conflicts |
| `references/reconciling-progress.md` | Plans or evidence are missing, stale, incomplete, or contradictory | Establish the active plan, match status to evidence, and select the next task |

Supporting references load only when their conditions apply. Project documents
follow the same pattern: read the relevant section and dependencies, expanding
only as needed. The installed skill remains the source of truth for its procedure.

`$planwright` produces or refreshes plans; `$consolidate-and-code` reconciles
learnings and actual progress before carrying out authorized implementation.
A review-only, planning-only, or skill-creation request retains that scope.

Verified 2026-09-06: the installed skill passed `quick_validate.py`, matched the
prepared copy, and all relative reference links resolved. It is also present in
the current Codex session's skill catalog.

## Personal Codex `$context-handoff` — created 2026-09-06

Save the active task in a durable Markdown note and return a copyable pointer
for a new context window. On resume, recover the objective, decisions, evidence
and next action, then rebuild understanding from current sources.

Entrypoint: [Context Handoff SKILL.md](</var/home/Louranicas/.codex/skills/context-handoff/SKILL.md>).
The installed skill is the source of truth for the procedure; session notes live
with the project, or under `/var/home/Louranicas/handoffs/` when no project
location is available.

### Invocation

Save the current session:

```text
Use $context-handoff to save this session so I can restart in a new context
window. Include the master index, $prime habitat, and the relevant deployment
atlas reading sequence. Return the Markdown link and a copyable restart prompt.
```

Resume in the new window, replacing the example path with the saved note:

```text
Use $context-handoff to resume from /absolute/path/to/restart.md. Read the note,
use $prime habitat, open its Fedora Master Index link, and follow its deployment
atlas reading sequence. Revalidate the state needed for the next action, then
continue within the recorded user scope.
```

### Progressive disclosure

| Resource | Load when | Purpose |
|---|---|---|
| Name and description | Skill selection | Recognize checkpoint, restart and saved-handoff requests |
| [SKILL.md](</var/home/Louranicas/.codex/skills/context-handoff/SKILL.md>) | The skill applies | Choose save or resume; required navigation and completion |
| [Handoff note format](</var/home/Louranicas/.codex/skills/context-handoff/references/handoff-note.md>) | Saving or updating a handoff | Preserve task state, decisions, evidence, reading order and restart prompt |
| [Atlas reading route](</var/home/Louranicas/.codex/skills/context-handoff/references/atlas-reading.md>) | Resolving atlas links or rebuilding context | Apply Prime, select the atlas and follow relevant dependencies to current evidence |

The next window reads the handoff summary → Prime and the indexes → the selected
atlas guides, packet and prerequisites → relevant code, configuration and
receipts. References and project sources load only when needed for that route.

Every handoff links [Prime](</var/home/Louranicas/.codex/skills/prime/SKILL.md>), the
[Habitat Fedora Master Index](obsidian://open?vault=herdr-fedora-habitat.vault&file=00%20-%20Fedora%20Master%20Index),
and the selected atlas. The
[Engineering atlas](obsidian://open?vault=herdr-fedora-habitat.vault&file=95%20Genesis%2Fengineering-atlas%2FSTART_HERE)
provides the overview;
[Learning deployment](obsidian://open?vault=herdr-fedora-habitat.vault&file=95%20Genesis%2Flearning-deployment%2FSTART_HERE)
covers deployment obligations, and
[Codebase deployment](obsidian://open?vault=herdr-fedora-habitat.vault&file=95%20Genesis%2Fcodebase-deployment%2FSTART_HERE)
covers construction packets. Saved handoffs include resolved filesystem links
so the next agent can read the sources directly.

Deep atlas understanding must be demonstrated through a source-linked account
of purpose, architecture, contracts, dependency order, acceptance, recovery and
evidence limits. Unread areas and stale observations remain explicit. A saved
handoff preserves the user's scope; creating one does not start implementation.

Use `$context-handoff` to carry context between windows. Use `$prime` for bounded
orientation, `$planwright` to create or refresh a plan, and
`$consolidate-and-code` when authorized implementation needs learnings and
progress reconciled before coding.

Verified 2026-09-06: the installed skill passed `quick_validate.py`, all four
installed files matched the validated staging copy, and all 13 static links
resolved. It is present in this Codex session's skill catalog. These checks
validate the package and navigation; no project-resume workflow was executed.

<!-- astra-prompt-library-20260908:start -->
## ASTRA prompt library — 2026-09-08

| Resource | Relationship |
|---|---|
| [[herdr-habitat-prompt-library\|ASTRA prompt library]] ⇄ this note | Select a focused prompt alongside an applicable skill. Model guidance is documented separately from skill availability and repository instructions; reciprocal library route. |
<!-- astra-prompt-library-20260908:end -->

<!-- habitat-context-summary-20260909:start -->
## Habitat Context

[[#Prime and Habitat Context|Comparison with Prime and the conditional chaining workflow]].

Habitat Context gives the habitat a repeatable way to bring relevant knowledge into a new context window. It assembles selected vault notes, code, Justfiles, and runbooks into compact, traceable packets for a specific task.

**What it does:** Connects explanatory notes with implementation files and declared operational procedures. It supports onboarding additional vaults and codebases, navigating dependencies in both directions, and selecting material by owner, type, or topic.

**How it works:** An explicit manifest identifies the files to admit. The tooling reads them within defined limits, supports parallel capture, preserves whole source files, and records hashes and receipts. It derives relationships, builds a packet within the chosen byte budget, and reports missing material or interpretation gaps. Progressive disclosure loads only the guidance needed for the current action; reusable snapshots reduce repeated reading.

**Value to the habitat:**

- **Faster onboarding:** New sources follow a consistent admission process.
- **More efficient context:** Focused packets reduce repeated discovery and unnecessary reading.
- **Better connections:** Notes, recipes, runbooks, and code become easier to navigate together.
- **Clearer evidence:** Coverage, provenance, and limitations remain visible.

The skill prepares context for informed work. It reads source commands without executing them, and distinguishes declared procedures from observed runtime results. Derived reverse edges support navigation; they do not write backlinks into source files.

### Use and progressive disclosure

```text
Use $habitat-context to prepare context for <question> from <selected sources>,
within <byte budget>; report included sources, missing requirements and evidence limits.
```

Start with the [installed skill](file:///var/home/Louranicas/.codex/skills/habitat-context/SKILL.md). Read its command reference for packet construction, admission reference for a new source set, validation reference for requested testing or failures, and evidence reference for historical claims. Load only the reference needed. The local command is `/var/home/Louranicas/.local/bin/habitat-context`; the skill supplies the workflow, while that tool performs ingestion.

> [!info]- Validation and recorded limits — 2026-09-09
> Three behavior cases and two revision replays passed. The new-vault packet held all four selected sources in 6,699 bytes; the fixed 4 KiB case returned a 2,301-byte partial packet with explicit missing requirements. Two original evaluators had fresh contexts; the evidence evaluator and both replays were resumed. These are finite skill-behavior checks, not a universal correctness or runtime-readiness guarantee. [Findings and receipts](file:///var/home/Louranicas/habitat-webbing-lab-20260908/skill-evaluation-20260909/REPORT.md).

### Connected habitat routes

Each companion below carries a return link to this section.

| Companion | Relationship |
|---|---|
| [[10 Tools/just\|Just]] | Recipe declarations supply codebase context and static calls. |
| [[60 Workflows/Runbooks\|Runbooks]] | Procedure declarations connect selected notes and implementation. |
| [[20 Chaining/Tool Clusters\|Tool Clusters]] | Context packets support focused reading across the existing tool groups. |
| [[00 - Toolshed Index\|Toolshed master index]] | Discover the skill through the toolkit route. |
| [Habitat master index](obsidian://open?vault=herdr-fedora-habitat.vault&file=00%20-%20Fedora%20Master%20Index) | Architecture and workspace orientation. |
| [Kinoite master index](obsidian://open?vault=fedora-kinoite.vault&file=00%20-%20Fedora%20Master%20Index) | Fedora substrate and cross-vault orientation. |
| [CLAUDE.local.md](file:///var/home/Louranicas/CLAUDE.local.md) | Current machine anchor points agents back to this summary and the installed skill. |
<!-- habitat-context-summary-20260909:end -->

<!-- prime-context-comparison-20260909:start -->
## Prime and Habitat Context

**Assessment:** the skills share substantial groundwork, and chaining them adds value when the relevant sources are not yet known. Prime locates and explains the knowledge landscape; Habitat Context packages selected material for a task. Keep their roles distinct and use a conditional handoff.

| Area | Prime | Habitat Context |
|---|---|---|
| Main purpose | Find the relevant vault, owner, note or source | Build a bounded context packet |
| Starting point | Five registered vaults, or explicitly named paths | A selected-source manifest or existing capture |
| Reading strategy | Follow maps and relevant links progressively | Capture declared files with bounded parallel reads |
| Relationships | Navigate documented connections | Derive typed calls, dependencies and inverse edges |
| Output | Orientation receipt, evidence paths and unread gaps | Whole source content, graph information, hashes and coverage diagnostics |

The current [Prime instructions](file:///var/home/Louranicas/.codex/skills/prime/SKILL.md) and [Habitat Context instructions](file:///var/home/Louranicas/.codex/skills/habitat-context/SKILL.md) define these responsibilities. Both use progressive disclosure, bounded source reading, explicit evidence limits and a boundary against executing source commands.

The crossover is already partly implemented: Habitat Context calls Prime's `prove-paths.py` reader for admission and capture, and its instructions call for Prime when vault owners are unknown. The recorded reader hash in the earlier four-source capture matched the installed reader during this assessment. [Implementation](file:///var/home/Louranicas/habitat-webbing-lab-20260908/procedures/context_ingest.py), [capture receipt](file:///var/home/Louranicas/habitat-webbing-lab-20260908/skill-evaluation-20260909/admission-test/capture/receipt.json).

### Valuable chaining

```mermaid
flowchart LR
    A["Prime: locate relevant sources"] --> B["Select paths, required coverage and budget"]
    B --> C["Habitat Context: capture and build packet"]
    C --> D["Answer using included evidence and disclosed gaps"]
```

A shipping/review question can use Prime to locate Toolshed's procedure guidance and its source references. Habitat Context then assembles the selected runbook, Justfile, cascade and implementation into a reusable packet.

- **Use Prime conditionally.** Start directly with Habitat Context when suitable sources or a capture are already known. Repeating full orientation adds reading and latency.
- **Make the handoff explicit.** Carry the question, exact paths, required source groups, source roles, budget and unresolved questions. Prime returns an orientation receipt; the inspected Habitat Context interface expects a manifest, so the agent translates between them.
- **Budget the whole workflow.** The packet ceiling excludes prior Prime reading. A small packet alone does not establish a small total context footprint.
- **Return to Prime for location or ownership gaps.** Budget omissions need selection decisions; unsupported syntax needs interpretation work. More vault discovery is not an automatic remedy.

Adding a vault to Habitat Context does not register it with Prime. The shared reader enforces file admission; it does not automatically transfer every higher-level scope rule. Retain the user's source boundaries and Prime's evidence distinctions in the handoff.

The strongest expected value is better source selection followed by reproducible, reusable context. At the time of this assessment, shared-reader integration was evidenced, but an end-to-end speedup from chaining the full skills had not been measured.

### Practice and evidence

Practised on the real shipping/review sources on **2026-09-09**. Prime routed Toolshed index → Runbooks guidance; the handoff reused four manifest declarations and added the named installed executor. One capture supplied the full answer and subsequent questions.

| Case | Packet bytes / cap | Required source coverage |
|---|---:|---|
| Prime → shipping/review packet | 65,427 / 65,536 | 5/5 |
| Known sources → direct Habitat Context | 26,744 / 32,768 | 5/5; no Prime orientation |
| Follow-up from the same capture | 65,518 / 65,536 | 5/5; no recapture |
| Broad question at 16 KiB | 15,259 / 16,384 | 1/5; four budget omissions explicitly reported |
| Narrowed runbook/cascade question | 16,172 / 16,384 | 2/2 for the narrower question |

The original broad 16 KiB request remains incomplete. The focused iteration changed the question and type filters, preserved the cap, and reused the same capture. Snapshot fingerprints and whole-file checks passed.

**Iteration:** the installed command reference now names the built-in manifest paths and graph collections/hash fields. These corrections address an unnecessary manifest read and a helper's initial empty lookup under the wrong graph key. A focused replay located the review manifest directly and extracted three authenticated gaps without new capture or execution. The 392-word entrypoint and progressive-disclosure structure remain unchanged.

**Useful source finding:** the note's revised shipping example has explicit exit-status checks that the captured `ship.toml` lacks; the selected executor confirmed the distinction. The note already documents this limitation. No operational definition or executor was changed.

> [!info]- Evidence, overhead and limits
> Capture took 0.242 s; primary packet construction 0.099 s; a reused packet 0.095 s. These are single local command observations, not an end-to-end speed benchmark. Prime presented 30,323 bytes of index/guidance before capture. The instrumented agent session took 625.46 s including reasoning, coordination and reporting. The full packet retained all five sources but omitted graph routes; relevant edges were inspected in the authenticated capture. The evaluators used resumed contexts, no source procedure ran, and runtime success remains unestablished. [Full findings, ledgers and receipts](file:///var/home/Louranicas/habitat-webbing-lab-20260908/prime-context-practice-20260909/REPORT.md).

**Practised recipe:** use focused Prime only when source ownership/location is unknown → hand off the question, exact paths/roles, required coverage, scope, cap and gaps → reuse relevant manifest entries → capture once and seed required sources → inspect actual items → reuse the capture for follow-ups. For tight budgets, disclose missing requirements and make any narrower question explicit. Read graph `gaps` or relationships only when needed, after verifying their receipt hashes.

### Weighted workflow assessment — 2026-09-09

**82/100 overall.** The conditional **Prime → Habitat Context** workflow adds substantial value through reliable source selection, traceable evidence and reusable captures. Its main weakness is preserving the relationships needed to interpret those sources within the bounded packet.

These are judgment-based scores grounded in the [saved practice evidence](file:///var/home/Louranicas/habitat-webbing-lab-20260908/prime-context-practice-20260909/REPORT.md), assessing its current local use. They are not measured probabilities or a universal readiness rating.

| Impactful facet | Weight | Mark /100 | Assessment |
|---|---:|---:|---|
| Source discovery and routing | 15% | **88** | Prime successfully located relevant guidance. Known sources can bypass orientation, avoiding unnecessary discovery. |
| Evidence integrity and scope control | 20% | **94** | Whole-source hashes, authenticated captures, explicit omissions and honest partial results provide strong traceability. Some scope rules still depend on the agent carrying them forward. |
| Source and relationship completeness | 20% | **68** | The main packet contained all five required sources, but 16 of 17 relationships used in the explanation required supplemental graph inspection. |
| Context economy and progressive disclosure | 15% | **80** | Bounded packets, selected views and conditional references control reading. Orientation still presented roughly 30 KB before capture; total session context is not comprehensively budgeted. |
| Snapshot reuse and tool responsiveness | 10% | **92** | Follow-ups reused unchanged captures; packet construction took roughly 0.1 seconds locally. End-to-end time savings remain unmeasured. |
| Handoff and tool integration | 10% | **78** | Habitat Context actually shares Prime's admission reader. The higher-level handoff into a manifest remains agent-mediated. |
| Maintainability and extension | 5% | **82** | A compact six-file skill and targeted guidance corrections keep maintenance manageable. Adding a manifest root does not automatically extend Prime's vault registry. |
| Validation breadth | 5% | **65** | Five bounded cases and a successful guidance replay support the demonstrated behavior. Fresh-context, scale and comparative answer-quality testing remain outstanding. |

**Weighted result:** `Σ(facet mark × weight) ÷ 100 = 81.95 → 82/100`. The weights sum to 100%.

> [!info]- Cross-facet findings and priorities
> - **Discovery × reuse creates the strongest habitat benefit.** Prime finds the authoritative sources once; Habitat Context makes them available for subsequent questions without repeating orientation and capture.
> - **Budget discipline × relationship completeness creates the largest tradeoff.** Staying within the byte cap works, but source inclusion does not guarantee that important dependencies survive in packet routes. Supplemental inspection adds work and context outside that cap.
> - **Traceability × integration makes the chain dependable.** Shared admission checks and verified snapshots strengthen the transition between skills. Explicit handoffs preserve intent, although their manual construction remains a source of friction.
>
> The most valuable next improvement is **selecting task-critical relationships alongside required sources**. After that, a structured handoff and a fresh-context comparison against the existing workflow would address the largest remaining gaps. These are assessment recommendations, not completed changes.
>
> The evidence supports a useful, disciplined context-preparation workflow. It does not yet establish uniformly fast ingestion across arbitrary vaults or a measured improvement in answer accuracy. [Verification](file:///var/home/Louranicas/habitat-webbing-lab-20260908/prime-context-practice-20260909/verification.json) · [Measurement scope](file:///var/home/Louranicas/habitat-webbing-lab-20260908/prime-context-practice-20260909/practice/orientation/metrics.json).


[Habitat Context executive summary](#Habitat%20Context) · [Prime entrypoint](file:///var/home/Louranicas/.codex/skills/prime/SKILL.md) · [[00 - Toolshed Index|Toolshed master index]].
<!-- prime-context-comparison-20260909:end -->
