#!/usr/bin/env python3
"""Read-only inotify FD-reference census; run on the host for full PID scope.

Counts are references, not deduplicated kernel instances. Inherited/duplicated
FDs may overcount; permission errors and process exits may undercount. No process
arguments, environment, file contents, or terminal transcripts are collected.
"""
import argparse
import collections
import datetime
import json
import os
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--uid', type=int, default=os.getuid())
args = parser.parse_args()
errors = collections.Counter()
rows = []
scanned = 0
for proc in Path('/proc').iterdir():
    if not proc.name.isdecimal():
        continue
    try:
        status = dict(line.split(':', 1) for line in (proc / 'status').read_text().splitlines() if ':' in line)
        if int(status['Uid'].split()[0]) != args.uid:
            continue
        scanned += 1
        refs = watches = 0
        for fd in (proc / 'fd').iterdir():
            try:
                if 'inotify' not in os.readlink(fd):
                    continue
                refs += 1
                watches += sum(line.startswith('inotify wd:') for line in (proc / 'fdinfo' / fd.name).read_text().splitlines())
            except PermissionError:
                errors['fd_permission_denied'] += 1
            except (FileNotFoundError, ProcessLookupError):
                errors['fd_exited_during_scan'] += 1
        if refs:
            try:
                cwd = os.readlink(proc / 'cwd')
                namespace = os.readlink(proc / 'ns/user')
            except OSError:
                cwd = namespace = 'unavailable'
            rows.append(dict(pid=int(proc.name), name=status['Name'].strip(), fd_references=refs, watch_references=watches, cwd=cwd, user_namespace=namespace))
    except PermissionError:
        errors['process_permission_denied'] += 1
    except (FileNotFoundError, ProcessLookupError):
        errors['process_exited_during_scan'] += 1
limits = {}
for prefix, keys in [('fs/inotify', ['max_user_instances', 'max_user_watches', 'max_queued_events']), ('user', ['max_inotify_instances', 'max_inotify_watches'])]:
    for key in keys:
        try:
            limits[prefix.replace('/', '.') + '.' + key] = int((Path('/proc/sys') / prefix / key).read_text())
        except OSError:
            limits[prefix.replace('/', '.') + '.' + key] = None
print(json.dumps(dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(), uid=args.uid, hostname=os.uname().nodename, pid_namespace=os.readlink('/proc/self/ns/pid'), user_namespace=os.readlink('/proc/self/ns/user'), limits=limits, processes_scanned=scanned, inotify_processes=len(rows), fd_references=sum(r['fd_references'] for r in rows), watch_references=sum(r['watch_references'] for r in rows), limitations='Non-atomic FD-reference census; inherited/duplicated FDs can overcount; inaccessible or exiting processes can undercount. Not an exact quota-usage counter.', errors=dict(errors), processes=sorted(rows, key=lambda r: (-r['fd_references'], -r['watch_references']))), indent=2))
