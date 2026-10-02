# Toolshed vault

Tools, workflows, reference notes, field findings, and prompt libraries maintained as an Obsidian vault.

**[Download the complete PDF](https://github.com/Louranicas/toolshed.vault/raw/refs/heads/main/output/pdf/toolshed-vault.pdf)**

The 390-page PDF edition includes all 96 published Markdown notes, a linked table of contents, PDF bookmarks, and six rendered Mermaid diagrams. Notes retain their original dates and scope. Cross-vault and local-file references require their original resources; non-Markdown evidence is available in this repository. Obsidian state, review backups, and ignored raw help dumps are excluded.

Start with [the Toolshed index](00%20-%20Toolshed%20Index.md), or open this directory as a vault in Obsidian.

## Rebuild the PDF

The exporter uses Git-tracked Markdown notes, excluding this README and generated output. It preserves the source notes and writes `output/pdf/toolshed-vault.pdf` and a source hash manifest. Build intermediates go to a temporary directory.

Prerequisites: Python 3, Node.js/npm, Chromium, and WeasyPrint's system libraries (including Pango). Install Liberation and Noto fonts for the intended typography.

```bash
python3 -m venv /tmp/toolshed-pdf-venv
/tmp/toolshed-pdf-venv/bin/pip install -r scripts/pdf-requirements.txt
npm install --prefix /tmp/toolshed-pdf-tools @mermaid-js/mermaid-cli@12.0.0
MMDC=/tmp/toolshed-pdf-tools/node_modules/.bin/mmdc \
  /tmp/toolshed-pdf-venv/bin/python scripts/export_pdf.py
```

If using an existing Chromium installation, set `PUPPETEER_EXECUTABLE_PATH` to its executable. Otherwise Mermaid CLI uses its Puppeteer-managed browser. The exporter disables the Chromium sandbox for local diagram rendering when an executable is explicitly supplied; use trusted source notes.

The edition date is set in the exporter. `output/pdf/manifest.json` records the source commit, individual note hashes, rendered diagram sources, and external or unresolved local links. Local references are retained rather than represented as bundled resources.

The bundled Noto Emoji font is distributed under the SIL Open Font License; see `scripts/fonts/OFL.txt`.
