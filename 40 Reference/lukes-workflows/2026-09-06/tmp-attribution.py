#!/usr/bin/env python3
"""Bounded /tmp metadata/liveness survey; never reads payloads or removes files."""
from pathlib import Path
import collections, datetime, json, os, stat
roots=[Path('/tmp/claude-1000'),Path('/tmp/.tmpwMcd2m'),Path('/tmp/.tmpD0g5Ez'),Path('/tmp/.tmpKHO6XS')]
inventory=[]
for root in roots:
    if not root.exists(): continue
    largest=[];todo=[(root,0)];visited=0;truncated=False
    while todo:
        directory,depth=todo.pop()
        try:
            for entry in os.scandir(directory):
                visited+=1
                if visited>5000: truncated=True;todo=[];break
                if entry.is_symlink(): continue
                s=entry.stat(follow_symlinks=False)
                if stat.S_ISREG(s.st_mode):
                    largest.append({'path':entry.path,'bytes':s.st_size,'allocated_bytes':s.st_blocks*512,'mtime_utc':datetime.datetime.fromtimestamp(s.st_mtime,datetime.timezone.utc).isoformat()})
                elif stat.S_ISDIR(s.st_mode) and depth<3: todo.append((Path(entry.path),depth+1))
        except OSError: pass
    inventory.append({'root':str(root),'top_level_names':[p.name for p in list(root.iterdir())[:15]],'entries_visited':visited,'truncated':truncated,'largest_files':sorted(largest,key=lambda x:-x['bytes'])[:8]})
refs=[];errors=collections.Counter()
for proc in Path('/proc').iterdir():
    if not proc.name.isdecimal(): continue
    try:
        status=dict(line.split(':',1) for line in (proc/'status').read_text().splitlines() if ':' in line)
        if int(status['Uid'].split()[0])!=os.getuid(): continue
        links=[proc/'cwd',proc/'exe']
        try: links+=list((proc/'fd').iterdir())
        except OSError: errors['fd_list_inaccessible']+=1
        for link in links:
            try: target=os.readlink(link)
            except OSError: continue
            if any(target==str(root) or target.startswith(str(root)+'/') for root in roots):
                refs.append({'pid':int(proc.name),'name':status['Name'].strip(),'reference':link.name,'target':target})
    except OSError: errors['process_inaccessible']+=1
print(json.dumps({'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'roots':inventory,'observed_live_references':refs[:100],'reference_count':len(refs),'errors':dict(errors),'limitations':'Metadata only; depth and entry bounds apply. No open FD in this snapshot does not prove data is disposable: processes can reopen paths, retain mappings, or require logs as evidence. No cleanup performed.'},indent=2))
