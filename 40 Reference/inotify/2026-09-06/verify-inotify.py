#!/usr/bin/env python3
"""Bounded live check: 160 simultaneous instances, one watch and file event.

Only runs once the limit is at least 2048. All descriptors and the temporary
directory are released, including on failure. Never probes to exhaustion.
"""
import ctypes
import datetime
import json
import os
from pathlib import Path
import select
import struct
import tempfile

limit = int(Path('/proc/sys/fs/inotify/max_user_instances').read_text())
if limit < 2048:
    raise SystemExit('REFUSED: capacity change not active; will not consume scarce baseline instances.')
libc = ctypes.CDLL(None, use_errno=True)
libc.inotify_init1.argtypes = [ctypes.c_int]
libc.inotify_init1.restype = ctypes.c_int
libc.inotify_add_watch.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_uint32]
libc.inotify_add_watch.restype = ctypes.c_int
fds = []
received = False
try:
    for _ in range(160):
        fd = libc.inotify_init1(os.O_CLOEXEC | os.O_NONBLOCK)
        if fd < 0:
            code = ctypes.get_errno()
            raise OSError(code, os.strerror(code))
        fds.append(fd)
    with tempfile.TemporaryDirectory(prefix='herdr-inotify-check-') as directory:
        watch = libc.inotify_add_watch(fds[0], os.fsencode(directory), 0x100)
        if watch < 0:
            code = ctypes.get_errno()
            raise OSError(code, os.strerror(code))
        Path(directory, 'probe.txt').write_text('inotify verification\n')
        ready, _, _ = select.select([fds[0]], [], [], 2)
        if ready:
            data = os.read(fds[0], 4096)
            offset = 0
            while offset + 16 <= len(data):
                wd, mask, cookie, size = struct.unpack_from('iIII', data, offset)
                name = data[offset + 16:offset + 16 + size].split(b'\0', 1)[0]
                received |= wd == watch and bool(mask & 0x100) and name == b'probe.txt'
                offset += 16 + size
        if not received:
            raise RuntimeError('Expected file-create event was not received.')
finally:
    for fd in fds:
        os.close(fd)
print(json.dumps(dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(), host=os.uname().nodename, user_namespace=os.readlink('/proc/self/ns/user'), limit=limit, simultaneous_instances=len(fds), file_create_event_received=received, all_instances_closed=True, temporary_directory_removed=not Path(directory).exists(), result='PASS'), indent=2))
