#!/usr/bin/env python3
"""Read-only five-second host snapshot; no benchmark, disk test or process changes."""
import datetime
import json
from pathlib import Path
import os
import subprocess
import time

def pressure():
    return {name: (Path('/proc/pressure') / name).read_text().strip() for name in ['cpu', 'memory', 'io']}

def block_stats():
    return {name: [int(x) for x in (Path('/sys/block') / name / 'stat').read_text().split()] for name in ['sda', 'sdb', 'sdc', 'nvme0n1'] if (Path('/sys/block') / name / 'stat').exists()}

start_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
first = block_stats()
before_pressure = pressure()
start = time.monotonic()
time.sleep(5)
elapsed = time.monotonic() - start
last = block_stats()
disks = {}
for name, b in first.items():
    a = last[name]
    completions = a[0] - b[0] + a[4] - b[4]
    disks[name] = {
        'read_iops': round((a[0] - b[0]) / elapsed, 2),
        'write_iops': round((a[4] - b[4]) / elapsed, 2),
        'read_mib_per_s': round((a[2] - b[2]) * 512 / elapsed / 1048576, 2),
        'write_mib_per_s': round((a[6] - b[6]) * 512 / elapsed / 1048576, 2),
        'busy_time_percent': round((a[9] - b[9]) / elapsed / 10, 2),
        'average_outstanding_io': round((a[10] - b[10]) / elapsed / 1000, 2),
        'approx_completed_io_wait_ms': round((a[3] - b[3] + a[7] - b[7]) / completions, 2) if completions else None,
        'inflight_at_end': a[8],
    }
blocked = []
for p in Path('/proc').iterdir():
    if not p.name.isdecimal():
        continue
    try:
        status = dict(line.split(':', 1) for line in (p/'status').read_text().splitlines() if ':' in line)
        if status['State'].strip().startswith('D'):
            blocked.append({'pid': int(p.name), 'name': status['Name'].strip(), 'wchan': (p/'wchan').read_text().strip()})
    except (OSError, KeyError):
        continue
memory = {}
for line in Path('/proc/meminfo').read_text().splitlines():
    key, value = line.split(':', 1)
    if key in ['MemTotal','MemAvailable','SwapTotal','SwapFree','Dirty','Writeback','Shmem']:
        memory[key] = value.strip()
topology = subprocess.run(['lsblk','-J','-o','NAME,SIZE,ROTA,MODEL,FSTYPE,MOUNTPOINTS'], capture_output=True, text=True, check=True)
cpu = subprocess.run(['lscpu','-J'], capture_output=True, text=True, check=True)
cpu_fields = {entry['field']: entry['data'] for entry in json.loads(cpu.stdout)['lscpu'] if entry['field'] in ['Model name:', 'CPU(s):', 'Core(s) per socket:', 'Socket(s):', 'Thread(s) per core:']}
capacity = {}
for directory in ['/var/home/Louranicas', '/var/mnt/STORAGE-10TB', '/tmp']:
    v = os.statvfs(directory)
    capacity[directory] = {'total_bytes': v.f_blocks * v.f_frsize, 'available_bytes': v.f_bavail * v.f_frsize, 'available_inodes': v.f_favail}
print(json.dumps({'started_utc': start_time, 'hostname': os.uname().nodename, 'elapsed_seconds': elapsed, 'cpu': cpu_fields, 'memory': memory, 'pressure_before': before_pressure, 'pressure_after': pressure(), 'disk_interval': disks, 'disk_topology': json.loads(topology.stdout), 'filesystem_capacity': capacity, 'blocked_processes': blocked[:40], 'blocked_process_count': len(blocked), 'limitations': 'Five-second observation of an uncontrolled workload, not a performance benchmark. Block-device counters do not attribute individual processes or prove hardware health. Busy time is not a universal SSD saturation metric. No command arguments, file contents, serial numbers or destructive tests collected.'}, indent=2))
