#!/usr/bin/env python3
"""Atuin evidence only: read-only SQLite, normalized aggregates, no command replay.

Archive mode streams a bounded tar.zst and reads only history.db into memory.
No files are extracted; no historical key/config/script/prompt is executed or
imported. Archive WAL is deliberately not applied; that source is checkpoint-only.
"""
from pathlib import Path
import argparse, collections, datetime, hashlib, json, re, shlex, signal, sqlite3, tarfile

KNOWN=set('cd ls pwd find rg fd du df free top htop btm ps kill pkill killall echo printf cat less head tail clear exit exec command which type source bash zsh fish nu sudo flatpak flatpak-spawn toolbox podman docker systemctl journalctl rpm-ostree dnf apt git gh glab cargo rustc rustup make just bacon pytest python python3 node npm npx pnpm yarn uv pip curl wget tar unzip cp mv rm mkdir chmod chown rsync restic atuin zellij herdr tmux codex claude hermes pi gemini opencode aider mempalace hunk nvim vim nano lazygit yazi tv television fzf jqp tuicr repo-fleet-status podman-tui habitat habitat-cascade habitat-fleet habitat-sandbox habitat-runbook watch ollama xdg-open zen'.split())
def primary(command):
    try: parts=shlex.split(command,comments=True)
    except ValueError: return 'unparsed'
    while parts and re.match(r'^[A-Za-z_][A-Za-z0-9_]*=',parts[0]): parts.pop(0)
    if not parts:return 'empty'
    word=parts[0].rsplit('/',1)[-1]
    return word if word in KNOWN else 'other'

def timestamp(n):
    try:return datetime.datetime.fromtimestamp(n/1e9,datetime.timezone.utc).isoformat()
    except (ValueError,OverflowError,OSError):return 'unavailable'

def summarize(connection,label):
    connection.execute('PRAGMA trusted_schema=OFF')
    connection.execute('PRAGMA query_only=ON')
    schema=connection.execute("SELECT type FROM sqlite_master WHERE name='history'").fetchone()
    if schema!=('table',):raise ValueError('Expected a real history table')
    columns={r[1] for r in connection.execute('PRAGMA table_info(history)')}
    required={'id','timestamp','duration','exit','command','cwd','session','hostname'}
    if not required<=columns:raise ValueError('Unsupported history schema')
    sql='SELECT id,timestamp,duration,exit,substr(command,1,4096),cwd,session,hostname FROM history'
    if 'deleted_at' in columns:sql+=' WHERE deleted_at IS NULL'
    rows=connection.execute(sql+' ORDER BY timestamp').fetchall()
    heads=collections.Counter();keywords=collections.Counter();exits=collections.Counter();cwd=collections.Counter();hosts=collections.Counter();days=collections.Counter();adj=collections.Counter();last_by_session={};ids=set();durations=collections.defaultdict(list)
    long_tools=collections.Counter();memory_related=collections.Counter()
    for uid,ts,dur,code,cmd,directory,session,host in rows:
        tool=primary(cmd);heads[tool]+=1;exits[str(code)]+=1;cwd[directory]+=1;hosts[host]+=1;ids.add(uid);days[timestamp(ts)[:10]]+=1
        for keyword in ['zellij','herdr','tmux','CARGO_TARGET_DIR','TMPDIR','cargo mutants','drop_caches','swapoff','swapon','free -h','btop','btm','htop','systemd-run','mempalace','ollama']:
            if re.search(r'(?<![A-Za-z0-9_])'+re.escape(keyword)+r'(?![A-Za-z0-9_])',cmd):keywords[keyword]+=1
        if code!=-1 and dur>=0:
            durations[tool].append(dur/1e9)
            if dur>3600*1e9:long_tools[tool]+=1
        if directory!='unknown' and session:
            previous=last_by_session.get(session)
            if previous and previous[0]!=tool:adj[(previous[0],tool)]+=1
            last_by_session[session]=(tool,ts)
    duration_summary={}
    for tool,values in durations.items():
        values.sort();duration_summary[tool]={'closed_records':len(values),'upper_median_seconds':round(values[len(values)//2],2),'max_seconds':round(max(values),2)}
    result={'source':label,'records':len(rows),'unique_ids':len(ids),'first_utc':timestamp(rows[0][1]) if rows else None,'last_utc':timestamp(rows[-1][1]) if rows else None,'sessions':len({r[6] for r in rows}),'host_counts':dict(hosts),'primary_tool_counts':dict(heads.most_common()),'keyword_record_counts':dict(keywords),'exit_counts':dict(exits),'top_cwds':dict(cwd.most_common(15)),'records_by_day':dict(days),'transitions_in_same_recorded_session':[{'from':a,'to':b,'count':n} for (a,b),n in adj.most_common(15)],'closed_command_durations':duration_summary,'closed_over_one_hour_by_tool':dict(long_tools),'limitations':'Only the first 4096 command characters are classified. Primary tool is a conservative first-token classification; wrappers and multiline commands may conceal later tools. Keyword counts are lower bounds when command prefixes are truncated. Keyword counts are mentions, not executions. Durations are wall-clock spans, not CPU/RAM use. Exit -1 is unknown/unfinished, not a proven failure. History does not establish human authorship or capture GUI activity/all agent tool calls.'}
    return result,ids

parser=argparse.ArgumentParser()
parser.add_argument('--archive',type=Path)
parser.add_argument('--active',type=Path,default=Path('/var/home/Louranicas/.local/share/atuin/history.db'))
parser.add_argument('--discovery',type=Path,default=Path(__file__).with_name('history-discovery.json'))
args=parser.parse_args()
if args.archive:
    from compression import zstd  # Archive mode requires Python 3.14+.
    signal.alarm(55)
    headers=[];payload=None;wal_seen=False;complete=False
    with zstd.open(args.archive,'rb') as stream,tarfile.open(fileobj=stream,mode='r|') as archive:
        for member in archive:
            headers.append({'name':member.name,'bytes':member.size})
            if len(headers)>100 or member.offset_data+member.size>4*1024**3:
                break
            if member.name=='atuin/history.db' and member.isfile():
                if member.size>1024*1024**2:raise ValueError(f'History member {member.size} bytes exceeds 1 GiB in-memory bound')
                payload=bytearray(archive.extractfile(member).read())
            if member.name=='atuin/history.db-wal' and member.size:wal_seen=True
        else:complete=True
    signal.alarm(0)
    if payload is None:raise ValueError('No history.db within the bounded archive traversal')
    digest=hashlib.sha256(payload).hexdigest()
    if payload[:16]!=b'SQLite format 3\x00':raise ValueError('Not a SQLite history database')
    # The archived checkpoint is consistent independently of newer WAL records.
    # In-memory rollback-journal header permits deserialize without disk/WAL files.
    payload[18]=payload[19]=1
    con=sqlite3.connect(':memory:');con.deserialize(bytes(payload))
    summary,ids=summarize(con,str(args.archive)+'::atuin/history.db')
    con.close()
    print(json.dumps({'archive':str(args.archive),'checkpoint_sha256':digest,'history_bytes':len(payload),'member_headers':headers,'archive_headers_complete':complete,'wal_present_not_applied':wal_seen,'scope':'Archived base checkpoint only; any uncheckpointed WAL history omitted. Temporary in-memory format header changed for SQLite deserialize; original archive untouched. No credentials or payload files extracted.','summary':summary},indent=2))
else:
    active=args.active.resolve()
    discovered=json.loads(args.discovery.read_text()).get('paths',[])
    outputs=[];all_ids=set();active_ids=set()
    for p in [active,*map(Path,discovered)]:
        con=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True,timeout=3)
        try:
            summary,ids=summarize(con,str(p))
            if p==active:active_ids=ids
            summary['ids_not_in_active']=len(ids-active_ids)
            all_ids|=ids;outputs.append(summary)
        finally:con.close()
    print(json.dumps({'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'databases':outputs,'union_distinct_ids':len(all_ids),'active_distinct_ids':len(active_ids),'backup_ids_not_in_active':len(all_ids-active_ids),'note':'Sources read via SQLite mode=ro/query_only with WAL visibility. Backups deduplicated by ID; counts must not be added as independent behavior.'},indent=2))
