#!/usr/bin/env python3
"""Save this reviewed incident bundle and add one link to the Toolshed index."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile

SOURCE = Path('/var/home/Louranicas/herdr-inotify-20260906')
VAULT = Path('/var/mnt/STORAGE-10TB/fedora-obsidian-vaults/toolshed.vault')
ARCHIVE = VAULT / '40 Reference/inotify/2026-09-06'
NOTE = VAULT / '50 Field Notes/Linux Inotify Capacity - Herdr Habitat.md'
INDEX = VAULT / '00 - Toolshed Index.md'
LINK = '- [[50 Field Notes/Linux Inotify Capacity - Herdr Habitat|Linux Inotify Capacity — Herdr Habitat]] — SOL3: reproduced KDE’s 92% instance warning, applied host limit 2,048, verified host/Toolbx file events, and archived diagnostics plus rollback (2026-09-06).\n'
ANCHOR = '## Field notes & workflows ⭐\n'
FILES = ['README.md', 'Prime Receipt.md', 'host-before.json', 'kde-before.json', 'kde-after.json', 'herdr-context.json', '90-herdr-inotify.conf', 'apply-inotify.py', 'apply-result.json', 'inotify-audit.py', 'verify-inotify.py', 'verify-host.json', 'verify-toolbx-sandbox.json', 'verify-herdr-toolbx.json', 'persistence-and-refresh.json', 'save-to-toolshed.py']

def atomic_write(path, data):
    if path.is_symlink():
        raise RuntimeError(f'Refusing symlink: {path}')
    fd, name = tempfile.mkstemp(prefix='.inotify-save-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            os.fchmod(stream.fileno(), 0o644)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)

if not VAULT.is_dir() or VAULT.is_symlink():
    raise SystemExit('Toolshed vault missing or symlinked.')
before = INDEX.read_bytes()
index = before.decode()
if LINK not in index and index.count(ANCHOR) != 1:
    raise SystemExit('Index anchor changed; review before publishing.')
payloads = {ARCHIVE / name: (SOURCE / name).read_bytes() for name in FILES}
payloads[ARCHIVE / 'original-context.png'] = Path('/tmp/codex-clipboard-eClfGV.png').read_bytes()
payloads[NOTE] = (SOURCE / NOTE.name).read_bytes()
for path, data in payloads.items():
    if path.is_symlink() or (path.exists() and path.read_bytes() != data):
        raise SystemExit(f'Refusing to replace a different existing artifact: {path}')
ARCHIVE.mkdir(parents=True, exist_ok=True)
for path, data in payloads.items():
    atomic_write(path, data)
checksums = ''.join(f'{hashlib.sha256(data).hexdigest()}  {path.name}\n' for path, data in sorted(payloads.items()) if path.parent == ARCHIVE)
atomic_write(ARCHIVE / 'SHA256SUMS', checksums.encode())
if LINK not in index:
    if INDEX.read_bytes() != before:
        raise SystemExit('Concurrent index edit detected; artifacts saved, index untouched. Rerun after review.')
    atomic_write(INDEX, index.replace(ANCHOR, ANCHOR + '\n' + LINK, 1).encode())
for path, data in payloads.items():
    if path.read_bytes() != data:
        raise SystemExit(f'Verification failed: {path}')
if LINK not in INDEX.read_text():
    raise SystemExit('Saved index link missing.')
print(json.dumps(dict(result='PASS', note=str(NOTE), archive=str(ARCHIVE), archive_files=len(FILES) + 2, index_link_verified=True, all_payloads_verified=True, note_sha256=hashlib.sha256(payloads[NOTE]).hexdigest()), indent=2))
