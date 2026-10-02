---
tags: [toolshed, skills, agents, examples, reference]
created: 2026-09-06
updated: 2026-09-06
---

# Skill usage guide

Use this guide to choose a skill, frame a useful request, and understand what an
agent should inspect and verify. Return to [[skills]] for installation homes,
the detailed personal workflows, and the wider skill map.

This review covers **51 installed skills**: five habitat skills, six Codex system
skills, three personal Codex skills, seventeen plugin skills, and twenty artifact
templates. **25 appear in the current Codex session catalog**. The five habitat
skills, `review-agent`, and twenty templates were found on disk but are absent
from that catalog. These are observations from 2026-09-06, not permanent availability
guarantees. A listed skill does not prove that its connector, desktop application,
credentials, or runtime dependencies are working.

Examples below are suggested requests, not actions performed during this review.
Select the matching skill from the current agent's catalog. Examples for skills
found only on disk apply in a host that exposes them or through an explicitly
authorized source-loading workflow; naming one does not enable it automatically.

## Choose the workflow

| Need | Start here | Expand only when needed |
|---|---|---|
| Locate project knowledge | `prime` | Read one routed note, then current source for implementation claims |
| Build or refresh an engineering plan | `planwright` | Structured plan contract, then HTML guidance for an HTML deliverable |
| Reconcile learnings and resume coding | `consolidate-and-code` | Standards promotion or plan reconciliation references |
| Create an Office file | Documents, Presentations, or Spreadsheets | The chosen format's create/edit, template, and verification guidance |
| Change a connected Google file | Google Drive, then its file-specific skill | Native structure, exact ranges, or comment evidence |
| Change the workbook open in Excel | `excel-live-control` | Live session setup, target selection, and advertised workbook commands |
| Explain an adjustable relationship in chat | `visualize` | The applicable chart, map, or simulation guidance |
| Build a website | `sites-building` | Required capabilities, then `sites-hosting` for deployment |
| Reuse a particular artifact design | The selected artifact-template skill | Its retained reference and matching format skill |
| Save a design as a reusable personal template | `template-creator` | Reference capture, preview, and packaging |

Give the agent the target, desired outcome, governing source or template, and a
useful acceptance condition. For example: “Update only the Revenue tab in this
Sheet from this CSV, preserve formulas, and verify the monthly totals.” Follow
the selected skill's required reads; defer unrelated references. Carry the exact
file ID, path, range, task IDs, and remaining evidence gaps into any handoff.

## Personal Codex workflows

Source: `~/.codex/skills/<name>/SKILL.md`. All three are in this session's catalog.

| Skill                  | Example request                                                                                                                        | How an agent can use it best                                                                                                                                                                                                                                                       |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prime`                | “Use $prime toolshed to locate the note explaining review gates and distinguish documentation from current evidence.”                  | Use it for bounded orientation. Prove registration, read the selected map and one relevant note, and state unread gaps. Use the enforced reader for an exact path after `--`. Its receipt establishes navigation; implementation needs current source and a scoped request.        |
| `planwright`           | “Use $planwright to refresh the implementation plan for this module, preserving task IDs and showing unresolved dependencies.”         | Use it when another executor needs an interpretable plan. Match depth to the job, preserve authoritative requirements, and connect acceptance criteria to evidence. Run the graph/source proof for structured artifacts and separate artifact QA from implementation verification. |
| `consolidate-and-code` | “Use $consolidate-and-code to reconcile these findings with our conventions and plan, then implement the next unfinished parser task.” | Use it to turn accumulated context into action. Promote only supported durable lessons, verify progress against code and checks, then complete the authorized implementation. Keep one progress record; use conditional references for conflicting standards or stale plans.       |

## Habitat skills

Source: `~/.claude/skills/<name>/SKILL.md`. These five were found on disk and are
not advertised in this Codex session. Their commands and recorded machine state
need verification in the target habitat before use.

| Skill | Example request | How an agent can use it best |
|---|---|---|
| `claim-discipline` | “Check whether the evidence actually supports marking this habitat repair complete.” | Use it to assess the evidence behind a verdict. Inspect the real producer's exit status, relevant cold-state assumptions, detector negative controls, and review independence. Load the false-pass reference for a completion review. Apply habitat commands only where that workspace supplies them. |
| `cli-ground-truth` | “This command returns an empty list even for known input; isolate the cause before scripting it.” | Build a small bounded reproduction, vary one input, inspect output shape and exit status, and compare installed version with the source being cited. Test protocol handshakes or round trips when relevant. A timeout alone does not diagnose stdin blocking. |
| `habitat-ops` | “Find why the W2 build pane is idle, then repair the stopped watcher.” | Start from current status and the service registry. Distinguish one-shot shell services from stopped daemons; choose the query door for values and pane door for visible state. Read only the pane, cascade, or sandbox reference needed for the task and verify the repair. |
| `kinoite-containers` | “Investigate this Podman bind-mount permission failure and explain whether the proposed fix survives a toolbox rebuild.” | Establish the actual host/container boundary first. Load SELinux guidance for mounts and durability guidance for artifact lifetime. Check the installed toolchain and linker for builds. Treat historical timings and image contents as recorded examples, not properties of every container. |
| `vault-mining` | “Save this verified tool finding in Toolshed, link its related note, and make it retrievable.” | Keep one authoritative note, use local wikilinks within a vault and Obsidian URLs between vaults, and verify the links changed. If mining is requested, inspect the source with a dry run, exclude configuration/cache material, then test retrieval. Historical vault-wide clean claims need a fresh audit. |

## Codex system skills

Source: `~/.codex/skills/.system/<name>/SKILL.md`. All except `review-agent`
appear in this session's catalog. These are managed sources; author personal
skills beside `.system`.

| Skill | Example request | How an agent can use it best |
|---|---|---|
| `imagegen` | “Create a transparent product cutout from this photo, preserving the label and proportions.” | Use the built-in image tool for raster generation or edits. Identify the edit target and reference roles, preserve specified details, inspect the output, and save project assets into the project. Existing SVG/icon systems are better edited in their native format. |
| `openai-docs` | “Explain how Codex skill discovery works and cite the relevant official documentation.” | Use the OpenAI Docs workflow for product guidance, keeping claims tied to fetched official pages and the exact requested topic or model. Select at most one primary route reference. Obey the current host's source-order rules when they differ from the packaged skill. |
| `plugin-creator` | “Create a personal plugin containing this workflow skill and an MCP configuration.” | Use the scaffold and validator to produce a valid manifest and only needed folders. Preserve the personal-versus-team destination. For existing local plugins, use the identifier, cachebuster, and reinstall guidance; do not patch a managed cache as the development source. |
| `review-agent` | “Review the change against main for introduced defects; report actionable findings without editing.” | In a review host that exposes it, inspect the complete merge-base diff, relevant call sites, and tests. Report demonstrated regressions by severity with narrow changed-line references. Return “No findings” when appropriate; do not invent style issues or treat self-review as independent review. |
| `skill-creator` | “Turn our release-note workflow into a personal skill with conditional references.” | Write a discriminating trigger and a compact core; defer substantial conditional procedures. Add scripts only when they improve reliability. Use the initializer when useful, validate the finished skill, and evaluate whether its instructions make sound decisions beyond merely passing the validator. |
| `skill-installer` | “Install the skill at this GitHub repository path and ref into my personal skills folder.” | Use the bundled listing or installation helper, honor the named source/ref, and check the destination before writing. Distinguish curated, experimental, and user-specified sources. Confirm installation separately from exposure in a subsequent catalog. |

## Browser, visuals, and artifact files

These seven plugin skills appear in this session's catalog. The exact names below
include their plugin namespaces. Read the current catalog path, not an old cache
version copied into a command.

| Skill | Example request | How an agent can use it best |
|---|---|---|
| `browser:control-in-app-browser` | “Open the local app in the in-app browser and verify the filter and empty state.” | Use the requested browser and inspect visible or interactive state. Reuse its connection and tab. For semantic file operations without explicit browser intent, discover a suitable connector/API first. Verify the UI after actions rather than assuming a click completed the task. |
| `visualize:visualize` | “Show in this conversation how queue length changes when I adjust arrival and service rates.” | Choose an inline interactive visual when changing inputs improves understanding. Embed bounded data, verify that controls update the result, and keep the visual focused. Use a Markdown table or Mermaid for simple static comparisons; use an exportable plotting tool for scientific figures. |
| `documents:documents` | “Revise this DOCX proposal using tracked changes and preserve its existing styles.” | Use the edit/redline path and only the necessary supporting guides. Preserve source meaning and structure, render with `render_docx.py`, inspect every page, and repair layout defects before delivery. Text extraction alone cannot verify pagination or clipping. |
| `pdf:pdf` | “Fill this PDF form with the supplied values and keep the result interactive.” | Inspect canonical form fields and page widgets, fill the intended fields, then reopen the saved PDF. Check both logical values and rendered appearances. Preserve interactivity unless flattening is requested; visual correctness alone does not prove the stored field data is correct. |
| `presentations:Presentations` | “Create a six-slide PPTX from this brief using our supplied deck as the design reference.” | Preserve the requested total slide count and template. Use the format's implementation guidance, keep evidence charts/tables editable, and inspect rendered slides for fit and completeness. Read Google Slides routing before choosing a native output path. |
| `spreadsheets:Spreadsheets` | “Create an XLSX comparing these scenarios, with editable assumptions and formulas.” | Use the standalone workbook workflow and its provided API. Keep source inputs and calculations understandable, inspect key values/formulas, scan errors, and render affected sheets. Deliver the requested workbook; a local XLSX request does not imply live Excel control. |
| `spreadsheets:excel-live-control` | “In my open Excel workbook, repair the selected range's formulas and update its chart.” | Verify the intended workbook and connected session first. Use that session's advertised schemas for reads/writes, preserve target identity, read values and formulas back, and inspect the changed range visually. If a required live capability is unavailable, explain it; do not silently substitute a separate XLSX. |

## Connected Google files

These five plugin skills appear in the catalog. Start with file identity and
MIME type, then load the specific content workflow. Use the supplied native
reference as a structural constraint when the user asks to follow it.

| Skill | Example request | How an agent can use it best |
|---|---|---|
| `google-drive:google-drive` | “Find the latest project brief in this folder and compare it with its previous revision.” | Ground the exact file through metadata and revision tools. Keep file discovery, moves, copies, exports, and sharing in this router; load a sibling only for content-specific work. Verify final metadata for lifecycle changes and choose export/fetch from the actual MIME type. |
| `google-drive:google-docs` | “Create this month's report from that multi-tab Google Doc, adapting every retained tab.” | Inspect the complete native tab tree and section/table roles, then copy and adapt the native reference. Distinguish retained structure from stale content. Use the trusted-read workflow before existing-document writes; verify tab coverage, native elements, and final layout where relevant. |
| `google-drive:google-sheets` | “Repair the totals in Budget!G12:G20 in this Sheet while preserving validation and formatting.” | Read metadata and the exact current range before editing through the connector. Preserve workbook identity and unrelated tabs. For a new deliverable based on a native template, copy the whole workbook unless a narrower extraction is explicit. Read back changed values/formulas and verify the relevant view. |
| `google-drive:google-slides` | “Update last quarter's native Google Slides deck for this quarter, preserving its layouts and replacing old figures.” | Read, parse, and render the native reference once. Copy it for a new deliverable, map each output slide to an appropriate exemplar, and account for every media slot. Verify slide IDs/order and inspect every final slide. For a new deck without a native reference, use Presentations. |
| `google-drive:google-drive-comments` | “Leave comments on ambiguous assumptions in this Sheet, naming each affected range.” | Read the target before drafting. Include the actual sheet/range, slide number, or quoted passage in the comment body and relevant evidence fields. Use live thread IDs for replies/resolves and verify results. API-created comments may appear unanchored, so location must remain understandable in plain text. |

## Sites, research, and reusable templates

These five plugin skills appear in the catalog.

| Skill | Example request | How an agent can use it best |
|---|---|---|
| `sites:sites-building` | “Build a project tracker with owner filters and persistent task status.” | Let the owning agent manage the project and lifecycle. Choose capabilities from the actual request, build a complete useful first view, and validate the implementation. Follow the hosting workflow unless the user requested local-only work. Asset contributors should return assets without independently deploying the site. |
| `sites:sites-hosting` | “Publish this validated site using its existing access settings.” | Reuse the exact successful build when source is unchanged, preserve project identity, and verify the current access mode. Follow the shared/public approval rules where required and not already authorized. Wait for successful deployment status before reporting the deployed URL. |
| `deep-research-work:deep-research` | “Do Deep research on these three approaches for our stated decision, with primary sources and a comparison.” | Use only for an explicit Deep research request. Establish scope and consequential claims, gather primary evidence, track gaps and contradictions, and follow up on unresolved claims. Separate evidence from interpretation and verify the requested deliverable. Do not activate it for an ordinary lookup. |
| `plugin-management:plugin-management` | “Find an integration that can access our project tracker, and explain its permissions.” | Check existing capabilities first, then search for the smallest useful missing integration. Distinguish installed, pending, and connected states. Inspect permissions and dependencies before explaining them; change permissions or remove an app only within the user's request. |
| `template-creator:template-creator` | “Save this approved monthly report as a reusable personal template.” | Capture the supplied reference and an accurate preview, then use the template packaging helper. Create a new personal template by default; update only an explicitly selected existing personal template. A one-off artifact made from a template belongs to the chosen template and format skill instead. |

## Installed artifact templates

All twenty were found under the `openai-templates` plugin cache and are absent
from this session's catalog. Each `artifact-template.json` resolves to an existing
retained reference and preview. This checks file presence, not rendering quality
or end-to-end execution.

For every row: use the template only when the user selects or names it, read its
metadata, copy/import the retained reference, and use the advertised matching
document, presentation, or spreadsheet skill. Preserve the reference itself and
its design unless the user requests a change. Adapt content from actual sources;
do not invent facts to fill slots. Render and verify the finished output. If the
required authoring capability cannot be identified and read, report that limit.

### Document templates

| Skill | Example request | How an agent can use it best |
|---|---|---|
| `artifact-template-design-report` | “Use Design Report to explain the findings from these usability sessions.” | Organize the supplied findings, implications, and recommendations in the reference structure; preserve sections/styles and distinguish observations from interpretation. |
| `artifact-template-experiment-analysis` | “Use Experiment Analysis for this experiment's protocol and results.” | Connect the stated hypothesis, method, results, limitations, and next steps. Preserve uncertainty and missing evidence instead of turning an inconclusive result into a positive claim. |
| `artifact-template-investment-committee-memo` | “Use Investment Committee Memo to summarize the supplied diligence materials.” | Keep the thesis, transaction details, financial evidence, risks, and proposed recommendation traceable to the input. Separate assumptions from reported results. |
| `artifact-template-legal-memorandum` | “Use Legal Memorandum to organize these supplied authorities and case facts.” | Retain issue, brief answer, facts, analysis, and conclusion roles. Keep authorities and factual assertions traceable; formatting the memo does not validate the legal analysis. |
| `artifact-template-minimal-letterhead` | “Use Minimal Letterhead for this business letter with these sender and recipient details.” | Preserve the letterhead, page setup, and signature area. Fill the exact supplied identities and message without adding commitments or inventing a signature. |
| `artifact-template-strategy-memorandum` | “Use Strategy Memorandum to compare these options and record our recommendation.” | Connect context, choices, rationale, risks, and milestones. Preserve the difference between an option under consideration and an accepted decision. |
| `artifact-template-system-design` | “Use System Design to document this service's requirements, APIs, and data flows.” | Ground components and relationships in the supplied design or code. Label proposed behavior, preserve tradeoffs, and avoid implying that documented components have been implemented. |

### Presentation templates

| Skill | Example request | How an agent can use it best |
|---|---|---|
| `artifact-template-business-review` | “Use Business Review for our quarterly KPIs, segment results, and priorities.” | Match the review period and comparison basis across slides. Retain the reference layouts and replace all prior-period facts with supported current inputs. |
| `artifact-template-market-trends-report` | “Use Market Trends Report to present this supplied industry research.” | Pair each trend with its evidence, timeframe, and implication. Use the retained chart/layout system and avoid converting correlations into unsupported recommendations. |
| `artifact-template-operating-review` | “Use Operating Review for this week's scorecard, risks, decisions, and actions.” | Keep the operational cadence and scorecard consistent. Distinguish status, decisions, and next actions; retain supplied owners and dates. |
| `artifact-template-project-kickoff` | “Use Project Kickoff to present this project's agreed scope and milestones.” | Preserve goal, scope, role, milestone, risk, and working-model sections. Show unresolved decisions explicitly rather than inventing agreement. |
| `artifact-template-simple-dark-mode` | “Use Simple Dark Mode for this six-slide technical briefing.” | Apply the retained dark layouts to the supplied content. Check contrast, chart labels, and image crops while keeping evidence objects editable. |
| `artifact-template-simple-light-mode` | “Use Simple Light Mode for this six-slide customer briefing.” | Preserve the reference's spacing and typography. Fit content by editing repetition before shrinking text; check the requested slide count and final rendering. |
| `artifact-template-team-alignment` | “Use Team Alignment for our offsite goals, priorities, and decisions.” | Separate discussion topics from decisions already made. Retain action items, owners, and follow-up dates only when the source supplies them. |

### Spreadsheet templates

| Skill | Example request | How an agent can use it best |
|---|---|---|
| `artifact-template-analytics-dashboard` | “Use Analytics Dashboard with these acquisition, retention, and revenue exports.” | Reconcile KPI definitions, denominators, and periods before populating charts. Preserve the template's formulas, tables, and filters; verify results against source totals. |
| `artifact-template-financial-budget` | “Use Financial Budget with these actuals, departmental plans, and scenario assumptions.” | Keep actuals separate from assumptions, preserve variance and runway relationships, and check formula outputs rather than filling calculated cells with constants. |
| `artifact-template-operating-calendar` | “Use Operating Calendar for these launches and recurring monthly deadlines.” | Preserve the calendar's date structure and recurring-event conventions. Use supplied milestones and check date placement across month/year boundaries. |
| `artifact-template-project-tracker` | “Use Project Tracker for these workstreams, owners, due dates, and task statuses.” | Retain validation, task identifiers, and schedule/Gantt relationships. Treat status as source data requiring evidence, not proof that a task is complete. |
| `artifact-template-sales-pipeline` | “Use Sales Pipeline to organize these opportunities and their next steps.” | Preserve stages, probabilities, owners, and forecast formulas. Keep missing commercial facts visible and verify weighted totals against source deal amounts. |
| `artifact-template-three-statement-forecast` | “Use Three-Statement Forecast with these historical statements and supplied assumptions.” | Preserve the integrated statement formulas and assumption inputs. Check balance-sheet balance, cash movement, and statement linkages; disclose missing inputs instead of forcing reconciliation. |

## Runbooks and justfiles

Skills tell an agent how to judge and carry out a task. Runbooks record a named
procedure with ordered steps and checks. Justfiles expose a project's executable
recipes. Use these layers together, with each definition maintained at its own
authoritative source. Runbooks and recipes are not additional skills in the
51-skill inventory above.

| Layer | Best use | Source to inspect |
|---|---|---|
| Skill | Select the workflow, evidence standard, and required references | The selected `SKILL.md` |
| Runbook | Coordinate preconditions, ordered steps, remediation, and final verification | `~/fedora-arena/runbooks/<name>.toml` and the installed `habitat-runbook` runner |
| Justfile | Discover and invoke the repository's established checks and operations | The target project's `justfile`, `.justfile`, or `Justfile`, including imported files and dependencies |

Read [[60 Workflows/Runbooks|Runbooks]] for the procedure model and
[[10 Tools/just|just]] for recipe syntax and the command surface.
[[40 Reference/Cascade and Runbook Catalogue|Cascade and Runbook Catalogue]] is
a generated snapshot: compare it with current definitions before relying on its
counts or claims.

### Runbooks

Start with inspection, then expand into the selected specification and the
commands it references:

```bash
habitat-runbook list
habitat-runbook show ship
```

`show` is a summary and truncates displayed step commands. Read the TOML for full
commands, working directory, expectations, retries, timeouts, and remediation.
Inspect referenced recipes/cascades/scripts before executing a procedure whose
effects matter to the request.

Current installed definitions, inspected 2026-09-06:

| Runbook | Example request | How an agent can use it best |
|---|---|---|
| `audit` | “Review the habitat audit procedure, then run the checks and service repair covered by my request.” | Inspect its six steps and final knowledge check. It can respawn services and invokes health, documentation, evidence, gate, and performance work. Treat its actual side effects as part of the task's scope. |
| `ship` | “Run the existing review procedure for this authorized Arena change and report any unmet gate.” | Follow its build, test, review-cascade, and topology steps. Inspect its branch and service preconditions and preserve the human-review requirement. Its name does not imply that it publishes or deploys. |
| `corpus-backup` | “Back up the corpus using the existing procedure and verify the restore drill.” | Read both the backup and drill implementations to establish destinations and effects. Report snapshot, restore comparison, and negative-control evidence separately; a manifest alone does not establish recoverability. |
| `factory-baseline` | “Inspect the T1-A baseline procedure and its expected evidence before using it.” | Follow the definition into the experiment's `factory-case T1-A` command. Confirm the delegated script's behavior; the runbook purpose's “read-only” wording does not itself prove the full command's effects. |
| `factory-ddf-pilot` | “Run the authorized offline DDF experiment and report its native test and review evidence.” | Keep the experiment's working directory and timeout, inspect its delegated script, and distinguish experiment results from promotion or production readiness. |
| `factory-roster-lab` | “Run the staged capability qualification and synthetic recovery exercise.” | Preserve the installed-binary hash precondition, inspect `./verify`, and report capability qualification and recovery evidence. The definition describes a lab exercise, not production activation. |

The three `factory-*` definitions currently have no separate `[verify]` block.
Their delegated scripts may implement checks; inspect those before deciding what
successful completion establishes.

**Runner behavior that changes how agents should use it:**

- `habitat-runbook run ship --dry-run` still executes the selected runbook's
  precondition commands. It previews steps and skips final verification; inspect
  preconditions before using this option as a preview.
- The `verified` word in `habitat-runbook list` means a `[verify]` block exists.
  It is not a passing result from an execution.
- Step output expectations use `expect`; final `[verify]` output expectations
  use `contains`. The loader rejects unsupported keys. In the current final
  verification loop, `contains` alone does not also enforce a zero exit status;
  inspect `expect_rc` and the actual command result before claiming success.
- `habitat-runbook export ship` writes an Atuin script body and prints a Just
  wrapper plus registration guidance. It does not automatically update the
  justfile or register the Atuin script. Treat export as a file mutation, and
  verify each generated entry point when updating the procedure.

These details were checked in `~/.local/bin/habitat-runbook`: `cmd_run` evaluates
preconditions before its step-level dry-run branch; `cmd_list` labels block
presence; `verify_loop` handles output and return-code checks separately; and
`cmd_export` writes the script body.

### Justfiles

Start from the target repository. Select the file explicitly when the workspace
contains several projects or inherited justfiles, then inspect one recipe and
its dependencies before choosing an execution command.

```bash
just --justfile /var/home/Louranicas/fedora-arena/justfile --summary
just --justfile /var/home/Louranicas/fedora-arena/justfile --list
just --justfile /var/home/Louranicas/fedora-arena/justfile --show check
just --justfile /var/home/Louranicas/fedora-arena/justfile --show test
just --justfile /var/home/Louranicas/fedora-arena/justfile --dump --dump-format json
```

Use `--summary` for names, `--list` for descriptions/groups, `--show` for one
recipe path, and the JSON dump when dependencies and parameters need structured
inspection. On this installed Just 1.57.0 build, `--show check test` is interpreted
as a recipe path through a submodule, so inspect those two recipes separately.

| Need | Example request | How an agent can use it best |
|---|---|---|
| Discover repository operations | “Find this project's existing build and test recipes before choosing commands.” | Inspect the actual justfile and its imports. Reuse established recipes when they cover the requested work; do not assume another repository's `check` or `test` has the same meaning. |
| Run a specific check | “Use Arena's existing type-check recipe and report the compiler result.” | The inspected `check` recipe invokes `cargo check --message-format short`. Run it only as part of the authorized task and retain the producer's exit status and useful diagnostics. |
| Run targeted tests | “Use the project's test recipe with the filter relevant to this change.” | Arena's `test` accepts an optional filter. Inspect parameter interpolation, dependencies, and working directory before supplying values; verify that the expected tests ran. |
| Inspect before execution | “Show what this recipe would do before running it.” | Read its source and dependencies first, then use `--dry-run` when appropriate. A preview does not verify success. `--explain` prints a recipe description before executing; it is not a substitute for `--show`. |
| Reach a runbook through Just | “Use the existing Just wrapper for the approved ship procedure.” | Arena currently exposes `rb-ship` and `rb-audit`, which call the corresponding runbook runner. Apply the same procedure scope and verification expectations regardless of entry point. |
| Maintain a recurring operation | “Add a reusable recipe for this repeated repository check.” | Follow the existing naming, parameters, comments, and groups. Check the project's formatting convention and validate the changed recipe in context. For a generated `rb-*` wrapper, update the runbook source and regenerate the affected surface instead of hand-editing generated commands. |

Bare `just` may execute the default recipe. Discovery should name an inspection
option. Avoid `--evaluate` merely to list variable names; `--variables` supplies
names without intentionally printing their values.

### How agents combine the layers

For a coding task, use `consolidate-and-code` to establish the next accepted task,
then inspect the project's justfile for its implementation checks. Use a runbook
when the task needs the existing coordinated procedure. Carry the target path,
selected recipe/runbook, parameters, relevant preconditions, and observed results
into the plan's progress record.

When a procedure changes, maintain its TOML source and verify any generated Just
or Atuin entry points used by the task. The current Arena snapshot has **six TOML
definitions and two `rb-*` Just wrappers**; do not infer that every definition has
been exported. The older reference catalogue lists only `audit` and `ship` and
records an earlier shape for `audit`.

Progressive disclosure: this section → the selected reference note → the current
runbook or recipe → only the commands and acceptance checks needed for the task.
This documentation update used source inspection, runner list/show, and Just
help/list/show. No runbook, recipe, backup, export, or remediation was executed.

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

## Useful combinations

| Task | Suggested sequence | What to hand forward |
|---|---|---|
| Resume a code change | `prime` when orientation is needed → `planwright` if the plan needs work → `consolidate-and-code` | Authoritative note paths, task IDs, dependencies, acceptance criteria, and actual validation evidence. Planning remains separate from permission to implement. |
| Turn a verified incident into practice | `cli-ground-truth` → `claim-discipline` → `vault-mining` → `consolidate-and-code` when implementation is requested | Reproduction, supported mechanism, scoped rule, note location, and next coding task. Use habitat skills only in a host that makes them available. |
| Refresh a native report | Google Drive discovery → Google Docs/Sheets/Slides native-reference workflow | Exact source and destination IDs, complete native structure, content to replace, and verification results. Do not let a deep link silently narrow copy scope. |
| Produce and reuse a reviewed artifact | Chosen template + matching format skill → `template-creator` only when asked to save it for reuse | Verified deliverable and the reference/design to retain. Making one report does not automatically create a reusable template. |
| Ship a site | `sites-building` → `imagegen` for requested raster assets → `sites-hosting` | Complete validated source, required assets, site identity, current access, and deployment result. Keep lifecycle ownership with the owning agent. |

When a separate reviewer is available and delegation is authorized, give it an
exact review target, governing instructions, and expected findings format. Do
not ask another agent to repeat the whole task. State whether verification was
performed by the author, a tool, or a separate reviewer.

## Review findings and limits

1. **Availability needs two checks.** The disk inventory contains 51 skills, while
   this session advertises 25. Template asset presence and a skill description do
   not prove that the corresponding tools can run. Recheck the catalog and required
   capabilities at task time.
2. **Google routing text conflicts.** The Google Drive router describes a blanket
   DOCX-first creation path, while Google Docs explicitly separates native
   references, basic native creation, and polished DOCX import. Google Sheets says
   existing edits use its connector, but its final-answer section broadly calls
   for XLSX creation/import. Follow the user's exact target and the applicable
   specialized route; an in-place edit must not become a replacement file. These
   package inconsistencies are recorded here; their managed sources were not edited.
3. **A timeout does not identify its cause.** `cli-ground-truth` equates exit 124
   with waiting on stdin in one example. The installed `timeout --help` says 124
   means the command timed out when status preservation is not enabled. Test stdin
   separately before recording that mechanism.
4. **Habitat snapshots are historical evidence.** `vault-mining` describes four
   STORAGE-10TB vaults; `prime` covers those plus Fabric under the home directory.
   These are different scopes. Old clean-link claims, service counts, toolbox
   contents, and build timings must not substitute for current checks.
5. **Progressive disclosure is selection followed by required reads.** This guide
   provides examples and routing. It does not replace a selected skill's core
   constraints, required references, or tool schemas. Large artifact entrypoints
   are a reason to avoid loading unrelated skills, not to skip required guidance.

Review method: inspected the installed entrypoint descriptions and relevant
routing, workflow, preservation, and verification sections; compared them with
the session catalog and this note's existing claims. Checked all twenty template
metadata files and the existence/containment of their references and previews.
Used the installed CLI's help to verify the timeout finding. No template was
rendered, connector exercised, service repaired, code change implemented, or
end-to-end skill execution certified by this documentation review.

## Source discovery

| Source family | Resolve the current entrypoint |
|---|---|
| Habitat | `~/.claude/skills/<name>/SKILL.md` |
| Personal Codex | `~/.codex/skills/<name>/SKILL.md` |
| Codex system | `~/.codex/skills/.system/<name>/SKILL.md` |
| Bundled browser, Sites, visualization | Current catalog path under `~/.codex/plugins/cache/openai-bundled/` |
| Google Drive, Deep research, plugin management | Current catalog path under `~/.codex/plugins/cache/openai-curated-remote/` |
| Documents, PDF, presentations, spreadsheets, template creator | Current catalog path under `~/.codex/plugins/cache/openai-primary-runtime/` |
| Artifact templates | `openai-curated-remote/openai-templates/<version>/skills/<name>/SKILL.md`, then its `artifact-template.json` |

Resolve cached paths from the current catalog or a fresh bounded inventory.
For reproduction, [[skills#Inventory commands]] contains the inventory commands.
Supporting references were inspected only where needed for this review; using a
skill may require additional reads.

Related: [[skills]] · [[Authored Skills]] · [[00 - Toolshed Index]]
