#!/usr/bin/env python3
"""Apply one reviewed host sysctl, or explicitly roll back this exact change.

Run on the Fedora host via sudo or pkexec. Refuses foreign configuration,
unexpected runtime limits, and container execution. No restarts or other tunings.
"""
import argparse
import datetime
import json
import os
from pathlib import Path
import subprocess
import tempfile

CONFIG = b'''# Herdr habitat on Fedora Kinoite; investigated 2026-09-06 by SOL3.
# KDE reported 118/128 instances (92%); 594/827880 watches.
# Host-wide per-user ceiling. Capacity is allocated only as applications use it.
# Preserve the existing watch and queue limits; tune them only from evidence.
fs.inotify.max_user_instances = 2048
'''
TARGET = Path('/etc/sysctl.d/90-herdr-inotify.conf')
KEY = 'fs.inotify.max_user_instances'
PROC = Path('/proc/sys/fs/inotify/max_user_instances')
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--rollback', action='store_true')
args = parser.parse_args()
if os.geteuid() != 0:
    raise SystemExit('Administrator authentication required; run this on the host with sudo or pkexec.')
if not Path('/run/ostree-booted').exists() or Path('/run/.containerenv').exists():
    raise SystemExit('Refusing: this must run on the Kinoite host, not inside Toolbx.')
if TARGET.is_symlink():
    raise SystemExit('Refusing to replace a symlink.')
original = TARGET.read_bytes() if TARGET.exists() else None
if original not in (None, CONFIG):
    raise SystemExit('Refusing to overwrite configuration changed by someone else.')
before = int(PROC.read_text())
if before not in (128, 2048):
    raise SystemExit(f'Refusing unexpected runtime limit {before}; reassess before applying.')
others = {key: int((PROC.parent / key).read_text()) for key in ['max_user_watches', 'max_queued_events']}

def install(data):
    fd, name = tempfile.mkstemp(prefix='.herdr-inotify-', dir=TARGET.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            os.fchmod(stream.fileno(), 0o644)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, TARGET)
    finally:
        if os.path.exists(name):
            os.unlink(name)

def sysctl(*argv):
    result = subprocess.run(['/usr/sbin/sysctl', *argv], capture_output=True, text=True, check=True)
    return result.stdout.strip()

try:
    if args.rollback:
        if original is None:
            raise RuntimeError('Managed file absent; refusing to roll back unrelated runtime state.')
        TARGET.unlink()
        output = sysctl('-w', KEY + '=128')
        expected = 128
    else:
        install(CONFIG)
        output = sysctl('-p', str(TARGET))
        expected = 2048
    after = int(PROC.read_text())
    if after != expected:
        raise RuntimeError(f'Runtime readback mismatch: {after} != {expected}')
    for key, value in others.items():
        if int((PROC.parent / key).read_text()) != value:
            raise RuntimeError(f'Concurrent change detected to {key}')
except Exception:
    if original is None:
        TARGET.unlink(missing_ok=True)
    else:
        install(original)
    sysctl('-w', KEY + '=' + str(before))
    raise
print(json.dumps(dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(), action='rollback' if args.rollback else 'apply', host=os.uname().nodename, path=str(TARGET), before=before, after=after, other_limits=others, file_present=TARGET.exists(), sysctl_output=output, result='PASS'), indent=2))
