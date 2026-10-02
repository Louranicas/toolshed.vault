#!/usr/bin/env python3
"""Read-only host memory attribution; no command arguments or document content."""
from pathlib import Path
import collections, datetime, json, os

def fields(path):
    out={}
    for line in path.read_text().splitlines():
        if ':' not in line: continue
        key,value=line.split(':',1)
        parts=value.split()
        if parts and parts[0].isdigit(): out[key]=int(parts[0])
    return out

mem=fields(Path('/proc/meminfo'))
rows=[]
errors=collections.Counter()
for p in Path('/proc').iterdir():
    if not p.name.isdecimal(): continue
    try:
        status=dict(line.split(':',1) for line in (p/'status').read_text().splitlines() if ':' in line)
        if int(status['Uid'].split()[0])!=os.getuid(): continue
        record={'pid':int(p.name),'ppid':int(status['PPid']), 'name':status['Name'].strip(),'rss_kib':int(status.get('VmRSS','0').split()[0]),'swap_kib':int(status.get('VmSwap','0').split()[0])}
        try:
            s=fields(p/'smaps_rollup')
            record.update({k.lower()+'_kib':s[k] for k in ['Pss','Pss_Anon','Pss_File','Pss_Shmem','SwapPss','Private_Dirty'] if k in s})
        except PermissionError: errors['smaps_permission_denied']+=1
        except OSError: errors['smaps_unavailable']+=1
        try: record['cgroup']=(p/'cgroup').read_text().strip()
        except OSError: pass
        rows.append(record)
    except OSError: errors['process_exited_or_unavailable']+=1
groups={}
for row in rows:
    name=row['name']
    g=groups.setdefault(name,{'processes':0,'pss_readable_processes':0,'pss_kib':0,'rss_kib':0,'swap_pss_kib':0})
    g['processes']+=1;g['rss_kib']+=row['rss_kib']
    if 'pss_kib' in row:
        g['pss_readable_processes']+=1;g['pss_kib']+=row['pss_kib'];g['swap_pss_kib']+=row.get('swappss_kib',0)
scopes=[]
base=Path('/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service')
for branch in ['app.slice','session.slice','background.slice','user.slice']:
    parent=base/branch
    if not parent.exists(): continue
    for p in parent.iterdir():
        if not p.is_dir(): continue
        try:
            stats=dict(line.split() for line in (p/'memory.stat').read_text().splitlines())
            scopes.append({'scope':p.name,'branch':branch,'current_bytes':int((p/'memory.current').read_text()),'anon_bytes':int(stats.get('anon',0)),'file_bytes':int(stats.get('file',0)),'shmem_bytes':int(stats.get('shmem',0)),'swap_bytes':int((p/'memory.swap.current').read_text())})
        except OSError: errors['cgroup_unavailable']+=1
zram=[int(v) for v in Path('/sys/block/zram0/mm_stat').read_text().split()]
print(json.dumps({'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'hostname':os.uname().nodename,'uid':os.getuid(),'meminfo_kib':mem,'pressure':{key:Path('/proc/pressure',key).read_text().strip() for key in ['cpu','memory','io']},'zram':{'original_bytes':zram[0],'compressed_bytes':zram[1],'physical_total_bytes':zram[2]},'process_groups':dict(sorted(groups.items(),key=lambda kv:-kv[1]['pss_kib'])),'top_processes':sorted(rows,key=lambda row:-row.get('pss_kib',0))[:50],'named_mux_processes':[r for r in rows if r['name'] in ['herdr','zellij','tmux: server','tmux','ghostty','konsole']],'cgroups':sorted(scopes,key=lambda r:-r['current_bytes']),'errors':dict(errors),'limitations':'PSS proportionally apportions mapped shared memory; process totals omit inaccessible/system processes, unmapped tmpfs and kernel memory. Cgroup current includes descendants and file cache; shmem is a subset of file. Do not sum these different views together. Names, counts and memory only; no process arguments, browsing state or files read.'},indent=2))
