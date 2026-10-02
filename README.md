# Toolshed vault

A practical knowledge base for command-line tools, software engineering workflows, agent-assisted development, and the evidence behind them. Toolshed brings together tool references, ways to compose those tools, measured field findings, and reusable prompts in an Obsidian vault.

The notes grew out of a Fedora Kinoite / Toolbx / Herdr working environment. Many patterns are useful elsewhere; paths, configurations, measurements, and deployment claims retain the context and dates recorded in their source notes.

**[Download the complete PDF](https://github.com/Louranicas/toolshed.vault/raw/refs/heads/main/output/pdf/toolshed-vault.pdf)** · [Toolshed index](00%20-%20Toolshed%20Index.md) · [Workflow index](60%20Workflows/00%20-%20Workflows.md) · [Toolkit index](70%20Toolkit/00%20-%20Habitat%20Toolkit.md)

The **2 October 2026 PDF edition** contains **390 pages, 96 Markdown notes, six rendered diagrams, linked contents, and PDF bookmarks**. It is a reading edition of the published notes; the repository also holds supporting evidence and the export tooling.

## Contents

- [What you will find](#what-you-will-find)
- [Start reading](#start-reading)
- [Repository map](#repository-map)
- [Reading routes by task](#reading-routes-by-task)
- [How to interpret the notes](#how-to-interpret-the-notes)
- [Links, dependencies, and portability](#links-dependencies-and-portability)
- [The PDF edition](#the-pdf-edition)
- [Rebuild the PDF](#rebuild-the-pdf)
- [Maintain or extend the vault](#maintain-or-extend-the-vault)
- [Licensing and attribution](#licensing-and-attribution)

## What you will find

### Tool references

The [10 Tools](10%20Tools) folder documents command surfaces, flags, usage patterns, and integration points for tools used in the author's environment. Examples include:

- **Finding and navigating:** Atuin, fzf, Television, and Yazi.
- **Editing, building, and reviewing:** LazyVim, Just, Bacon, Lazygit, Hunk, Tuicr, and gh-dash.
- **Structured data and system inspection:** Nushell, jqp, Podman, podman-tui, bottom, and repo-fleet-status.
- **Agent workspaces and knowledge:** Herdr, Firstmate, MemPalace, and Jev / jev-axi.

Use the [Command Matrix](40%20Reference/Command%20Matrix.md) to compare documented command surfaces and [Documented Surface and Source](40%20Reference/Documented%20Surface%20and%20Source.md) for the dated mapping from documented flags to source locations.

### Tool composition and workflow design

[Tool Chaining Patterns](20%20Chaining/Tool%20Chaining%20Patterns.md) covers filters, structured-data pipelines, watchers, capture, and other ways to connect tools. [Tool Clusters](20%20Chaining/Tool%20Clusters.md) groups related capabilities; [Clustering Shapes](20%20Chaining/Clustering%20Shapes.md) explores different arrangements; [Workflow Recipes](20%20Chaining/Workflow%20Recipes.md) provides worked compositions.

The workflow collection extends those ideas into diagnostics, review, runbooks, automation, knowledge audits, and resource-aware operation. It includes both local implementations and proposed practices; individual notes explain their status.

### Field findings and supporting evidence

[Field Findings](50%20Field%20Notes/00%20-%20Field%20Findings.md) records observed behavior, failed assumptions, and lessons from actual work. Other field notes cover Jev, Linux inotify capacity, and workstation workflows.

The [reference collection](40%20Reference) contains source maps, dated evidence packs, configuration snapshots, JSON receipts, patches, and learning records. [Perfecting Rust - Performance Engineering](40%20Reference/Perfecting%20Rust%20-%20Performance%20Engineering.md) connects performance study to a cycle of baselines, profiling, hypotheses, and verification.

### Agent guidance and prompts

The [Habitat Prompt Library](herdr-habitat-prompt-library.md) routes to ASTRA guidance on prompting, coding, quality review, and evidence. The toolkit also documents skills, MCP surfaces, and local development practices. [80 Prompt Library](80%20Prompt%20Library) and [Luke's Scratchpad](Lukes-Scratchpad/luke-scratchpad.md) contain additional prompts and working material.

### Jev research

The [Jev Master Index](00%20-%20Jev%20Master%20Index.md) connects model notes, field findings, application patterns, search routing, and validation practices. Its introduction identifies the retained Toolshed research as the **18 September 2026 measured corpus** and points to a separate `jev.vault` for continuing work. That companion vault is not included here.

## Start reading

### On GitHub

Open the [Toolshed index](00%20-%20Toolshed%20Index.md) or choose a route below. Standard Markdown links in this README work on GitHub. Many source notes use Obsidian `[[wikilinks]]`, which GitHub does not turn into the same vault navigation experience.

### In Obsidian

1. Clone or download this repository:

   ```bash
   git clone https://github.com/Louranicas/toolshed.vault.git
   ```

2. Open the cloned `toolshed.vault` directory as a vault in Obsidian.
3. Start with `00 - Toolshed Index.md`, then follow the folder indexes and note links.

The repository excludes the author's `.obsidian/` configuration. Obsidian will maintain its own local settings for your copy. External tools described in the notes are not required merely to read the Markdown.

### As a PDF

Use the download link at the top for a single portable reading copy. The contents pages and document bookmarks let you jump between notes. See [the PDF edition](#the-pdf-edition) for what the export includes and how links behave.

### In a text editor or terminal

The knowledge base is plain Markdown and can be searched without Obsidian. For example, from the repository root, with `rg` installed:

```bash
rg -n 'pipefail' '20 Chaining' '60 Workflows'
rg -n 'inotify' '50 Field Notes'
rg --files '70 Toolkit'
```

## Repository map

| Location | Purpose |
|---|---|
| [00 - Toolshed Index.md](00%20-%20Toolshed%20Index.md) | Main entry point and cross-topic navigation. |
| [00 - Jev Master Index.md](00%20-%20Jev%20Master%20Index.md) | Index of the retained Jev research and links to related work. |
| [10 Tools/](10%20Tools) | Individual tool references and command surfaces. |
| [20 Chaining/](20%20Chaining) | Composition patterns, capability groups, and workflow recipes. |
| [30 Analysis/](30%20Analysis) | Analysis of tool use. |
| [40 Reference/](40%20Reference) | Matrices, source mappings, performance study, and dated evidence packs. |
| [50 Field Notes/](50%20Field%20Notes) | Findings, measurements, and operational lessons. |
| [60 Workflows/](60%20Workflows) | Workflow guidance, automation, review, and validation practices. |
| [70 Toolkit/](70%20Toolkit) | Habitat toolkit, skills, MCP, prompting, and engineering guidance. |
| [80 Prompt Library/](80%20Prompt%20Library) | Additional prompt reference material. |
| [Lukes-Scratchpad/](Lukes-Scratchpad) | Working prompts and personal scratch notes. |
| [herdr-habitat-prompt-library.md](herdr-habitat-prompt-library.md) | Router for the ASTRA prompt and review notes. |
| [output/pdf/](output/pdf) | Published PDF, source manifest, and recorded validation. |
| [scripts/](scripts) | PDF exporter, pinned Python dependencies, and the bundled emoji font. |
| [mempalace.yaml](mempalace.yaml) | MemPalace classification metadata for the vault. |
| [.habitat-gates](.habitat-gates) | Opt-in declaration for the surrounding habitat's backlink, orphan, path, and anchor checks. |

## Reading routes by task

| I want to… | Suggested route |
|---|---|
| Find the right tool or command | [Toolshed index](00%20-%20Toolshed%20Index.md) → [Command Matrix](40%20Reference/Command%20Matrix.md) → the relevant note in [10 Tools](10%20Tools). |
| Connect tools into a repeatable workflow | [Tool Chaining Patterns](20%20Chaining/Tool%20Chaining%20Patterns.md) → [Workflow Recipes](20%20Chaining/Workflow%20Recipes.md) → [Runbooks](60%20Workflows/Runbooks.md). |
| Improve an engineering review | [ASTRA Quality Review](70%20Toolkit/ASTRA%20Quality%20Review.md) → [Cross-Workspace Review Gate](60%20Workflows/Cross-Workspace%20Review%20Gate.md) → [Weight Matrix - Which Gate Bore the Weight](60%20Workflows/Weight%20Matrix%20-%20Which%20Gate%20Bore%20the%20Weight.md). |
| Turn diagnostics into review evidence | [Bridge - Diagnostics to Review](60%20Workflows/Bridge%20-%20Diagnostics%20to%20Review.md) → [Bridge - Coverage to Review](60%20Workflows/Bridge%20-%20Coverage%20to%20Review.md) → [Field Findings](50%20Field%20Notes/00%20-%20Field%20Findings.md). |
| Investigate resource pressure or worker capacity | [Linux Inotify Capacity - Herdr Habitat](50%20Field%20Notes/Linux%20Inotify%20Capacity%20-%20Herdr%20Habitat.md) → [lukes workflows](50%20Field%20Notes/lukes%20workflows.md) → [Autonomous Triggers](60%20Workflows/Autonomous%20Triggers.md). |
| Study Rust performance methodically | [Perfecting Rust - Performance Engineering](40%20Reference/Perfecting%20Rust%20-%20Performance%20Engineering.md) → [Source and Reading Map](40%20Reference/rust-mastery/2026-09-06/Source%20and%20Reading%20Map.md) → [Learning Status and Next Steps](40%20Reference/rust-mastery/2026-09-06/Learning%20Status%20and%20Next%20Steps.md). |
| Understand the retained Jev experiments | [Jev Master Index](00%20-%20Jev%20Master%20Index.md) → [Jev - Field Findings](50%20Field%20Notes/Jev%20-%20Field%20Findings.md) → [Jev - Validation Discipline](60%20Workflows/Jev%20-%20Validation%20Discipline.md). |
| Choose a prompt or documented skill | [Habitat Prompt Library](herdr-habitat-prompt-library.md) → [ASTRA Prompting Guide](70%20Toolkit/ASTRA%20Prompting%20Guide.md) → [Skills router](70%20Toolkit/skills.md). |
| Understand a claim's evidence and limits | [ASTRA Evidence and Sources](70%20Toolkit/ASTRA%20Evidence%20and%20Sources.md) → the cited note or dated evidence pack. |

## How to interpret the notes

Read the date, source references, and scope alongside each claim. The vault contains several kinds of material:

- **Tool documentation and source mappings** describe the versions and source trees inspected at the time.
- **Measured findings** report a particular experiment or observed environment; their numbers do not automatically generalize to another machine or workload.
- **Proposals and workflow candidates** describe work to assess or try. Their presence does not establish deployment or adoption.
- **Evidence packs** preserve receipts and context for a specific change or investigation.
- **Prompt and scratch material** includes reusable wording and working ideas; it has a different role from a verified finding.

A note's documented command, a source implementation, and a successful local execution are different kinds of evidence. Follow the linked records when that distinction matters. Historical model, product, and command descriptions should be checked against the version you intend to use.

## Links, dependencies, and portability

The notes were authored within a larger collection of Fedora and engineering vaults. You will encounter:

| Reference type | What to expect |
|---|---|
| `[[Note]]` or `[[Note#Heading]]` | Obsidian navigation to a note or heading. The PDF resolves supported references to included notes. |
| `obsidian://open?...` | An Obsidian deep link, sometimes into a separate vault that must exist locally. |
| `file://...` or absolute filesystem paths | Resources on the author's machine. They are not downloaded by cloning this repository. |
| Web URLs | External documentation, repositories, or source material. |
| Source file paths and line numbers | Locations in the source snapshot examined by a note; they can change in later revisions. |

Companion vaults, source checkouts, the running Herdr environment, shared habitat checks, and locally installed skills are not bundled with this repository. `mempalace.yaml` supplies classification metadata; it does not include a populated search database. `.habitat-gates` declares participation in external checks; it is not itself a runnable test suite.

The exclusions in [.gitignore](.gitignore) are `.obsidian/`, `.trash/`, `.note-review-backups/`, and `40 Reference/help/`. The published PDF follows the tracked-note selection rather than exporting every file that may exist in the author's local vault.

## The PDF edition

| Property | Published edition |
|---|---|
| Edition date | 2 October 2026 |
| Length | 390 A4 pages |
| Included notes | 96 Markdown files |
| Diagrams | Six Mermaid diagrams rendered as images |
| Navigation | Linked contents, note and heading destinations, and PDF bookmarks |
| Source snapshot | `ab519ce`, with individual note SHA-256 hashes in the manifest |
| Recorded internal-link check | 1,668 internal links resolved |
| Recorded layout checks | No out-of-margin words detected; representative pages and all six diagrams visually reviewed |

The snapshot identifier describes the notes used for this edition. Later README or tooling commits do not imply that the PDF has been regenerated.

The exporter removes YAML frontmatter from the reading layout, adds a cover and contents, retains code as text, and converts the supported standalone display-math form. Non-Markdown evidence remains in the repository. External vaults and local-file targets are references, not embedded attachments.

If a heading cannot be matched but its note can, the exporter links to the note's start. Other unresolved relative targets fall back to repository URLs and may still be unavailable. Resolution of internal destinations is therefore not a claim that every external link works or that every original heading reference lands at the exact heading.

Three files describe the edition:

- [toolshed-vault.pdf](output/pdf/toolshed-vault.pdf) — the published reading copy.
- [manifest.json](output/pdf/manifest.json) — source commit, note hashes, diagram-to-note mapping, and external or unresolved local targets recorded by the exporter.
- [validation.json](output/pdf/validation.json) — checks recorded for the published PDF, including its SHA-256 and the pages visually inspected.

`validation.json` is a retained validation record. The export script does **not** regenerate it automatically.

## Rebuild the PDF

### Prerequisites

Run the exporter from a Git checkout with Python 3, Node.js/npm, and a Chromium browser usable by Mermaid CLI. WeasyPrint requires its platform libraries, including Pango. Liberation and Noto fonts provide the intended text typography; the emoji font is bundled in `scripts/fonts/`.

The Python renderer dependencies are pinned in [scripts/pdf-requirements.txt](scripts/pdf-requirements.txt). The published build used Mermaid CLI `12.0.0`. A rebuild can differ in layout when fonts or system rendering libraries differ.

### Install dependencies and export

From the repository root:

```bash
python3 -m venv /tmp/toolshed-pdf-venv
/tmp/toolshed-pdf-venv/bin/pip install -r scripts/pdf-requirements.txt
npm install --prefix /tmp/toolshed-pdf-tools @mermaid-js/mermaid-cli@12.0.0

MMDC=/tmp/toolshed-pdf-tools/node_modules/.bin/mmdc \
  /tmp/toolshed-pdf-venv/bin/python scripts/export_pdf.py
```

Alternatively, where `uv` is available, the Python setup is:

```bash
uv venv /tmp/toolshed-pdf-venv
uv pip install --python /tmp/toolshed-pdf-venv/bin/python \
  -r scripts/pdf-requirements.txt
```

The build writes `output/pdf/toolshed-vault.pdf` and `output/pdf/manifest.json`. It prints the build directory, note count, diagram count, and output path. HTML and diagram intermediates are retained in the temporary build directory for inspection.

### Optional environment variables

| Variable | Meaning |
|---|---|
| `MMDC` | Path to the Mermaid CLI executable; defaults to `mmdc` on `PATH`. |
| `PUPPETEER_EXECUTABLE_PATH` | Explicit Chromium executable; otherwise Mermaid CLI uses its default browser discovery. |
| `PDF_BUILD_DIR` | Directory for intermediate HTML, Mermaid source, images, and renderer configuration; otherwise a temporary directory is created. |

Example using an existing browser:

```bash
MMDC=/tmp/toolshed-pdf-tools/node_modules/.bin/mmdc \
PUPPETEER_EXECUTABLE_PATH=/path/to/chromium \
PDF_BUILD_DIR=/tmp/toolshed-pdf-review \
  /tmp/toolshed-pdf-venv/bin/python scripts/export_pdf.py
```

Replace `/path/to/chromium` with the actual executable. With an explicit browser path, the current exporter supplies `--no-sandbox` to Chromium for local diagram rendering; use trusted source notes.

### Source selection and validation

The exporter enumerates `git ls-files '*.md'`, excluding the root `README.md` and files under `scripts/` and `output/`. It reads those files from the working tree. Add new notes to Git before exporting; commit the intended source snapshot first if the manifest's `HEAD` identifier is to describe that snapshot precisely. Individual hashes identify the bytes read even when tracked files have uncommitted edits.

The edition date is currently written in [scripts/export_pdf.py](scripts/export_pdf.py). Update it intentionally when publishing a new edition. A README-only change does not require a PDF rebuild because the README is excluded.

Before publishing a rebuilt PDF:

1. Check the note list and hashes in the manifest against the intended sources.
2. Inspect contents, bookmarks, and internal links.
3. Render pages and review tables, code blocks, diagrams, typography, and page boundaries.
4. Refresh the validation record for the new PDF; the old record belongs to the old file.

With Poppler installed, a minimal inspection starts with:

```bash
pdfinfo output/pdf/toolshed-vault.pdf
pdftotext -layout output/pdf/toolshed-vault.pdf /tmp/toolshed-vault.txt
pdftoppm -f 1 -l 3 -scale-to 1400 -png \
  output/pdf/toolshed-vault.pdf /tmp/toolshed-preview
sha256sum output/pdf/toolshed-vault.pdf
```

Text extraction is useful for completeness checks; rendered-page inspection is needed to assess layout.

### Common build issues

| Symptom | Check |
|---|---|
| `mmdc` is not found | Install the pinned Mermaid CLI and set `MMDC` to its executable. |
| Chromium fails to launch | Confirm the browser executable and its platform dependencies; use `PUPPETEER_EXECUTABLE_PATH` when needed. |
| WeasyPrint reports missing native libraries | Install its required platform libraries in the environment running Python. |
| A new note is absent | Check that Git tracks the file and that it is outside the excluded paths. |
| A local or cross-vault link cannot open | Check whether the referenced resource exists on your machine; these resources are not bundled. |
| Validation no longer matches the PDF | Repeat the checks and update the retained record after rebuilding. |

## Maintain or extend the vault

Place new material in the relevant numbered section and connect it to an existing index. Keep titles, links, dates, source references, and evidence locations consistent with nearby notes. When a result changes, distinguish the new observation from the historical result rather than silently expanding the old claim.

For a useful correction or proposed addition, include the affected note, the concrete claim or behavior, the version or date being discussed, and the evidence supporting the change. Preserve the distinction between a suggested workflow and one actually tested or deployed.

Review changes with `git diff` before publishing. Keep local application state and recovery copies out of commits. Regenerate the PDF when the published note corpus changes, and update its validation record together with the new artifact. There is no automatic PDF publishing workflow in this repository.

## Licensing and attribution

The bundled **Noto Emoji** font is distributed under the **SIL Open Font License 1.1**; its license is retained in [scripts/fonts/OFL.txt](scripts/fonts/OFL.txt). That font license does not apply to the vault's notes or export code.

The repository currently has no repository-wide license file. Public availability alone does not specify reuse permissions for the authored content. Source references and third-party material retain their own attribution and applicable terms.
