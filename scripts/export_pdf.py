#!/usr/bin/env python3
"""Compile the Git-tracked Markdown notes into a navigable PDF."""
import hashlib
import html
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.parse import unquote, quote, urlparse, parse_qs

from markdown_it import MarkdownIt
from latex2mathml.converter import convert as mathml
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/pdf'
OUT.mkdir(parents=True, exist_ok=True)
TMP = Path(os.environ.get('PDF_BUILD_DIR', tempfile.mkdtemp(prefix='toolshed-pdf-')))
TMP.mkdir(parents=True, exist_ok=True)
paths = [Path(p) for p in subprocess.check_output(['git', 'ls-files', '-z', '*.md'], cwd=ROOT).decode().split('\0') if p and p != 'README.md' and not p.startswith(('scripts/', 'output/'))]
paths.sort(key=lambda p: (0 if str(p) == '00 - Toolshed Index.md' else 1 if len(p.parts) == 1 else 2, str(p).casefold()))
ids = {p: 'note-' + hashlib.sha256(str(p).encode()).hexdigest()[:12] for p in paths}
by_name = {}
for p in paths:
    by_name.setdefault(p.stem.casefold(), []).append(p)
headers = {}
md = MarkdownIt('commonmark', {'html': True}).enable('table')

def strip_frontmatter(s):
    return re.sub(r'\A---\s*\n.*?\n---\s*\n', '', s, count=1, flags=re.S)

sources = {p: strip_frontmatter((ROOT / p).read_text()) for p in paths}
for p, s in sources.items():
    tokens = md.parse(s)
    for i,t in enumerate(tokens):
        if t.type == 'heading_open':
            title = tokens[i+1].content
            key = (p, title.casefold())
            headers.setdefault(key, ids[p] + '-h' + str(i))

unresolved = set()
def target(raw, current):
    raw = unquote(raw)
    if raw.startswith('obsidian://'):
        q = parse_qs(urlparse(raw).query)
        if q.get('vault', [''])[0] != ROOT.name:
            return raw
        raw = q.get('file', [''])[0]
    if re.match(r'^[a-zA-Z][\w+.-]*:', raw) or raw.startswith('//'):
        return raw
    name, sep, fragment = raw.partition('#')
    name = name.removesuffix('.md')
    candidates = [current] if not name else [Path(name+'.md'), current.parent/(name+'.md')]
    if name.startswith(str(ROOT)):
        candidates.insert(0, Path(name+'.md').relative_to(ROOT))
    found = next((p for p in candidates if p in ids), None)
    if found is None and len(by_name.get(Path(name).name.casefold(), [])) == 1:
        found = by_name[Path(name).name.casefold()][0]
    if found:
        return '#' + headers.get((found, fragment.casefold()), ids[found]) if fragment else '#'+ids[found]
    if name:
        unresolved.add((str(current), raw))
    if raw.startswith('/'):
        return 'file://' + quote(raw)
    return 'https://github.com/Louranicas/toolshed.vault/blob/main/' + quote(str(current.parent / raw), safe='/#')

CURRENT = None
default_validate_link = md.validateLink
md.validateLink = lambda url: url.startswith('file://') or default_validate_link(url)
def link_open(tokens, idx, options, env):
    tokens[idx].attrSet('href', target(tokens[idx].attrGet('href') or '', CURRENT))
    return md.renderer.renderToken(tokens, idx, options, env)
md.renderer.rules['link_open'] = link_open

# Parse Obsidian links as inline tokens, so fenced/inline code remains literal.
def wikilink(state, silent):
    pos = state.pos
    if not state.src.startswith('[[', pos): return False
    end = state.src.find(']]', pos+2)
    if end < 0: return False
    raw = state.src[pos+2:end].replace('&#124;', '|').replace('\\|', '|')
    if '\n' in raw: return False
    dest, _, label = raw.partition('|')
    if not silent:
        tok = state.push('link_open', 'a', 1); tok.attrSet('href', dest)
        tok = state.push('text', '', 0); tok.content = label or dest.split('/')[-1]
        state.push('link_close', 'a', -1)
    state.pos = end+2
    return True
md.inline.ruler.before('link', 'wikilink', wikilink)

diagrams = []
def fence(tokens, idx, options, env):
    t = tokens[idx]
    if t.info.strip() != 'mermaid':
        return '<pre><code>'+html.escape(t.content)+'</code></pre>'
    n = len(diagrams)+1
    source = TMP/f'diagram-{n}.mmd'; image = TMP/f'diagram-{n}.png'
    source.write_text(t.content)
    cfg = TMP/'mermaid.json'; cfg.write_text(json.dumps({'theme':'neutral','flowchart':{'htmlLabels':False,'useMaxWidth':False},'themeVariables':{'fontFamily':'Liberation Sans','fontSize':'18px'}}))
    cmd = [os.environ.get('MMDC','mmdc'), '-i',str(source),'-o',str(image),'-c',str(cfg),'-b','white','--size','2200','-q']
    if os.environ.get('PUPPETEER_EXECUTABLE_PATH'):
        pc = TMP/'puppeteer.json'; pc.write_text(json.dumps({'executablePath':os.environ['PUPPETEER_EXECUTABLE_PATH'],'args':['--no-sandbox']})); cmd += ['-p',str(pc)]
    subprocess.run(cmd, check=True)
    diagrams.append({'note':str(CURRENT),'number':n})
    return f'<figure><img src="{image.as_uri()}"/><figcaption>Diagram {n} · {html.escape(CURRENT.stem)}</figcaption></figure>'
md.renderer.rules['fence'] = fence

parts = []
manifest=[]
for p in paths:
    CURRENT = p
    s = sources[p]
    s = '\n'.join(re.sub(r'\[\[([^\]\n]+)\]\]', lambda m: '[[' + m.group(1).replace('\\|', '|').replace('|', '&#124;') + ']]', line) if line.lstrip().startswith('|') else line for line in s.split('\n'))
    # Display mathematics appears outside code in these source notes.
    s = re.sub(r'^\$\$([^\n]+)\$\$[ \t]*$', lambda m: '\n<div class="math">'+mathml(m.group(1), display='block')+'</div>\n',s,flags=re.M)
    tokens = md.parse(s)
    for i,t in enumerate(tokens):
        if t.type == 'heading_open':
            t.attrSet('id',headers.get((p,tokens[i+1].content.casefold()),ids[p]+'-h'+str(i)))
            t.tag = 'h'+str(min(int(t.tag[1])+2,6))
        elif t.type == 'heading_close':
            t.tag = 'h'+str(min(int(t.tag[1])+2,6))
    body = md.renderer.render(tokens, md.options, {})
    parts.append(f'<article><h2 id="{ids[p]}">{html.escape(p.stem)}</h2><div class="source">{html.escape(str(p))}</div>{body}</article>')
    manifest.append({'path':str(p),'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest()})

css = '''
@page { size: A4; margin: 18mm 16mm 18mm;
 @top-left { content: "TOOLSHED / REFERENCE EDITION"; font: 7pt "Liberation Sans"; color:#607080; }
 @bottom-left { content: string(note); font: 7pt "Liberation Sans"; color:#607080; max-width: 150mm; }
 @bottom-right { content: counter(page); font: 8pt "Liberation Sans"; color:#244c60; }
}
@page:first { @top-left {content:none} @bottom-left {content:none} @bottom-right {content:none} }
body { font: 9.5pt/1.45 "Liberation Sans", "Noto Sans", "Noto Emoji", sans-serif; color:#20313d; }
h1,h2,h3,h4,h5,h6 { color:#163e52; line-height:1.2; break-after:avoid; }
h1 {font-size:40pt; bookmark-level:none;}
h2 {font-size:24pt; string-set:note content(); bookmark-level:1;}
h3 {font-size:17pt; bookmark-level:2;}
h4 {font-size:13pt; bookmark-level:3;}
h5,h6 {font-size:11pt;bookmark-level:none;}
p {orphans:3;widows:3;}
a { color:#166582; text-decoration:none; overflow-wrap:anywhere; }
article {break-before:page;}
.source {font:8pt "Liberation Mono"; color:#607080; margin-bottom:9mm; overflow-wrap:anywhere;}
.cover {padding-top:40mm;break-after:page;}
.eyebrow {font-size:10pt;letter-spacing:2pt;color:#166582;}
.subtitle {font-size:19pt;max-width:140mm;}
.cover-meta {border-top:2pt solid #166582; padding-top:8mm;margin-top:25mm;}
.toc {break-after:page;}
.toc h2 {string-set:note "Contents";bookmark-level:1;}
.toc ul {list-style:none;padding:0;}
.toc li {font-size:9pt;line-height:1.6;}
.toc a::after {content:leader('.') target-counter(attr(href),page);}
.toc-group {font-weight:bold;color:#163e52;margin-top:5mm;break-after:avoid;}
pre {white-space:pre-wrap;overflow-wrap:anywhere;font:7.3pt/1.4 "Liberation Mono";background:#f1f5f7;border-left:2pt solid #a8c5d0;padding:7pt;tab-size:4;}
code {font-family:"Liberation Mono";font-size:0.88em;overflow-wrap:anywhere;}
pre code {font-size:inherit;}
table {width:100%;border-collapse:collapse;table-layout:fixed;font-size:7.5pt;line-height:1.35;margin:8pt 0;}
th,td {border:0.5pt solid #c8d5dc;padding:5pt;vertical-align:top;overflow-wrap:anywhere;}
th {background:#e7f0f3;text-align:left;color:#163e52;}
thead {display:table-header-group;}
tr {break-inside:avoid;}
blockquote {border-left:2pt solid #9dbbc9;margin-left:0;padding-left:12pt;color:#405663;}
figure {margin:12pt 0;break-inside:avoid;text-align:center;}
figure img {max-width:100%;max-height:210mm;}
figcaption {font-size:7.5pt;color:#607080;margin-top:5pt;}
img {max-width:100%;}
hr {border:0;border-top:0.5pt solid #c8d5dc;margin:12pt 0;}
.math {text-align:center;margin:10pt 0;}
'''
css = '@font-face { font-family: \"Noto Emoji\"; src: url(' + (ROOT / 'scripts/fonts/NotoEmoji.ttf').as_uri() + '); }\n' + css
toc=[]; group=None
for p in paths:
    g=p.parts[0] if len(p.parts)>1 else 'Vault indexes and overview'
    if g!=group:
        if group is not None:toc.append('</ul>')
        toc.append(f'<div class="toc-group">{html.escape(g)}</div><ul>');group=g
    toc.append(f'<li><a href="#{ids[p]}">{html.escape(p.stem)}</a></li>')
toc.append('</ul>')
rev=subprocess.check_output(['git','rev-parse','--short','HEAD'],cwd=ROOT).decode().strip()
doc=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Toolshed Vault - Reference Edition</title><meta name="author" content="Louranicas"><style>{css}</style></head><body>
<section class="cover"><div class="eyebrow">TOOLS / WORKFLOWS / KNOWLEDGE</div><h1>Toolshed</h1><p class="subtitle">The complete Obsidian vault<br>Reference edition</p><div class="cover-meta"><p><b>2 October 2026</b> · {len(paths)} notes · {len(diagrams)} diagrams</p><p>Published by Louranicas<br>Source snapshot: {rev}</p><p><a href="https://github.com/Louranicas/toolshed.vault">github.com/Louranicas/toolshed.vault</a></p></div></section>
<section class="toc"><h2>Contents</h2><p>All Git-tracked Markdown notes, ordered by vault section. Note links within this edition are clickable; PDF bookmarks provide another route through the collection.</p><p>Cross-vault and local-file references require their original resources. Non-Markdown evidence remains in the repository. Local backups, Obsidian state and ignored help dumps are excluded. Source notes retain their original dates, claims and scope.</p>{''.join(toc)}</section>{''.join(parts)}</body></html>'''
(TMP/'toolshed.html').write_text(doc)
pdf_temp = OUT/'toolshed-vault.building.pdf'
HTML(string=doc,base_url=str(ROOT)).write_pdf(pdf_temp)
pdf_temp.replace(OUT/'toolshed-vault.pdf')
(OUT/'manifest.json').write_text(json.dumps({'source_commit':rev,'notes':manifest,'diagrams':diagrams,'external_or_unresolved_local_links':[{'note':p,'target':t} for p,t in sorted(unresolved)]},indent=2)+'\n')
print(json.dumps({'pdf':str(OUT/'toolshed-vault.pdf'),'notes':len(paths),'diagrams':len(diagrams),'build_dir':str(TMP)}))
