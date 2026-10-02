#!/usr/bin/env python3
"""Validate the documentation delta; no workload examples are executed.

Only a locally defined simulated compiler runs in the pipeline check. The real jq
formats its fixed fixture. Other changed Bash blocks undergo syntax parsing only.
"""
from pathlib import Path
import collections
import datetime
import hashlib
import json
import os
import re
import subprocess
import tomllib

BUNDLE = Path(__file__).resolve().parent
VAULT = BUNDLE.parents[2]
inputs = json.loads((BUNDLE / 'review-inputs.json').read_text())
errors = []
checked_links = 0
bash_checked = 0
bash_placeholders = 0
toml_checked = 0


def blocks(text):
    return re.findall(r'^```([^\n]*)\n(.*?)^```\s*$', text, re.M | re.S)


def prose(text):
    return re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.M | re.S)


def links(text):
    return [v.replace('\\|', '|') for v in re.findall(r'\[\[([^\]]+)\]\]', prose(text))]


def heading(value):
    return value.replace('`', '').replace('**', '').strip()


files = list(VAULT.rglob('*.md'))
names = [*inputs['target_notes'], str((BUNDLE / 'README.md').relative_to(VAULT))]
for name in names:
    path = VAULT / name
    text = path.read_text()
    if len(re.findall(r'^```', text, re.M)) % 2:
        errors.append(f'{name}: unbalanced fenced blocks')
    prior = collections.Counter(inputs.get('before_links', {}).get(name, []))
    new_links = collections.Counter(links(text)) - prior
    for raw in new_links.elements():
        target = raw.split('|', 1)[0]
        stem, mark, fragment = target.partition('#')
        found = ([path] if not stem else
                 [VAULT / (stem + '.md')] if '/' in stem else
                 [p for p in files if p.stem == stem])
        found = [p for p in found if p.exists()]
        if len(found) != 1:
            errors.append(f'{name}: link {raw!r} resolved {len(found)} times')
            continue
        if mark:
            headings = [heading(h) for h in re.findall(r'^#{1,6} (.+)$', found[0].read_text(), re.M)]
            if heading(fragment) not in headings:
                errors.append(f'{name}: missing heading in {raw!r}')
        checked_links += 1
    old_blocks = {tuple(b) for b in inputs.get('before_blocks', {}).get(name, [])}
    for lang, body in blocks(text):
        if (lang, body) in old_blocks:
            continue
        if lang in {'bash', 'sh'}:
            if re.search(r'<(?:repo|name|N|tag|what it does|recipe|cmd|id|n)>', body):
                bash_placeholders += 1
                continue
            env = dict(os.environ)
            env.pop('BASH_ENV', None)
            env.pop('ENV', None)
            result = subprocess.run(['bash', '--noprofile', '--norc', '-n'], input=body,
                                    text=True, capture_output=True, env=env, timeout=5)
            bash_checked += 1
            if result.returncode:
                errors.append(f'{name}: Bash syntax: {result.stderr.strip()}')
        if lang == 'toml':
            try:
                tomllib.loads(body)
                toml_checked += 1
            except tomllib.TOMLDecodeError as exc:
                errors.append(f'{name}: TOML syntax: {exc}')

# Execute only the isolated documented pipeline, with Cargo replaced by a fixture.
recipe = (VAULT / '20 Chaining/Workflow Recipes.md').read_text()
pipeline = re.search(r'\(\n  set -o pipefail\n  cargo check.*?\n\)', recipe, re.S)
pipeline_results = []
if not pipeline:
    errors.append('Documented Cargo pipeline missing')
else:
    env = dict(os.environ)
    env.pop('BASH_ENV', None)
    env.pop('ENV', None)
    fixture = json.dumps({'reason': 'compiler-message', 'message': {'rendered': 'fixture diagnostic'}})
    for code in [0, 42]:
        stub = "cargo() { printf '%s\\n' '" + fixture + "'; return " + str(code) + "; }\n"
        result = subprocess.run(['bash', '--noprofile', '--norc'],
                                input=stub + pipeline.group(0), text=True,
                                capture_output=True, timeout=5, env=env)
        ok = result.returncode == code and result.stdout.strip() == 'fixture diagnostic'
        pipeline_results.append({'simulated_cargo_exit': code, 'pipeline_exit': result.returncode,
                                 'diagnostic_preserved': result.stdout.strip() == 'fixture diagnostic',
                                 'passed': ok})
        if not ok:
            errors.append('Documented pipeline did not preserve fixture status/output')

source_changes = [name for name, digest in inputs['source_hashes'].items()
                  if not Path(name).exists() or hashlib.sha256(Path(name).read_bytes()).hexdigest() != digest]
if source_changes:
    errors.append('Inspected source changed since review: ' + ', '.join(source_changes))
after_changes = [name for name, digest in inputs['after_hashes'].items()
                 if hashlib.sha256((VAULT / name).read_bytes()).hexdigest() != digest]
if after_changes:
    errors.append('Reviewed notes changed since patch capture: ' + ', '.join(after_changes))

result = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'existing_notes_updated': len(inputs['after_hashes']),
          'new_or_changed_wikilinks_checked': checked_links,
          'changed_bash_blocks_syntax_checked': bash_checked,
          'placeholder_bash_blocks_not_syntax_checked': bash_placeholders,
          'changed_toml_blocks_parsed': toml_checked,
          'pipeline_fixture_checks': pipeline_results,
          'source_hashes_unchanged': not source_changes,
          'reviewed_note_hashes_match': not after_changes,
          'errors': errors, 'passed': not errors,
          'scope': 'Documentation delta; no builds, histories, supervisors, triggers or cleanup examples executed.'}
(BUNDLE / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
raise SystemExit(bool(errors))
