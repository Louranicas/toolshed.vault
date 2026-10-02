---
tags: [reference, evidence, workflows, memory, atuin]
created: 2026-09-06
author: SOL3
---

# Luke's workflow evidence — 2026-09-06

Assessment: [[50 Field Notes/lukes workflows|lukes workflows]]. Index: [[00 - Toolshed Index]]. Earlier system context: [[50 Field Notes/Linux Inotify Capacity - Herdr Habitat]].

This bundle contains newly authored analysis scripts and normalized observations. It contains **no raw Atuin database, historical command transcript, credentials, archive payload, copied agent memory or legacy configuration**. Local paths and process/workspace labels are retained where they establish provenance.

## Files and methods

| File | Evidence / method |
|---|---|
| [memory-baseline.json](memory-baseline.json) | Host `/proc/meminfo`, PSI, zram counters and readable UID 1000 process PSS; 2026-09-05 20:16 UTC / 6 September 06:16 ACT. |
| [memory-followup.json](memory-followup.json) | Second reading at 20:22 UTC, including the `user.slice` branch holding the main Toolbx cgroup. |
| [memory-audit.py](memory-audit.py) | Read-only collector; no process arguments or document/browser contents. Saved revision includes the cgroup branch added for the follow-up. |
| [tmp-usage.json](tmp-usage.json) | Host `du -x -B1 --max-depth=1 /tmp`, with a 30-second timeout. Exit 1 reflects twelve inaccessible service-private directories. |
| [tmp-attribution.json](tmp-attribution.json) | Bounded metadata inspection of selected directories and accessible process FD/cwd/exe references. No journal or task contents read. |
| [tmp-attribution.py](tmp-attribution.py) | Collector for that attribution; depth three and 5,000-entry limits per selected root. |
| [tmp-claude-subtrees.json](tmp-claude-subtrees.json) | Bounded `du` aggregation within `/tmp/claude-1000`; ancestor and descendant totals overlap. |
| [herdr-layout.json](herdr-layout.json) | Reduced live workspace/tab/pane layout: counts, roles, working directories and detected agent status. No terminal transcripts. |
| [storage-and-vmstat.json](storage-and-vmstat.json) | Host `findmnt`, `df -B1`, `lscpu -J`, and three `vmstat` reports. The first vmstat row is since-boot accounting, not the first one-second interval. |
| [io-attribution-sample.json](io-attribution-sample.json) | Paired PSI and diskstats, visible blocked-thread scans, and block-device metadata, over about three seconds. Stacked device rows overlap. |
| [atuin-cli-receipt.json](atuin-cli-receipt.json) | Installed Atuin version/help plus the verified global `full-text` query. Result format omits command text. All three invocations exited 0. |
| [history-discovery.json](history-discovery.json) | Narrowed filesystem discovery roots, ten found history databases, return status and coverage metadata. |
| [atuin-current-and-backups.json](atuin-current-and-backups.json) | Read-only SQLite summaries of the active database and ten Fedora backup databases; ID-based deduplication. |
| [atuin-legacy-checkpoint.json](atuin-legacy-checkpoint.json) | In-memory summary of an archived history checkpoint; archive-member names/sizes are metadata, not extracted contents. |
| [history-analysis.py](history-analysis.py) | Conservative tool classification and aggregate history analysis. Saved revision clarifies the upper-median statistic, bounds command prefixes and accepts explicit source paths. |
| [SHA256SUMS](SHA256SUMS) | Integrity manifest for the bundle files, excluding the manifest itself. |

The main narrative and master index are outside this evidence manifest because they remain living notes. The evidence files are dated observations, not live monitoring.

## History provenance and coverage

The current database is `/var/home/Louranicas/.local/share/atuin/history.db`. Ten additional databases were found below `/var/mnt/STORAGE-10TB/habitat-corpus-backup/*/shell-history/history.db`. They were read using SQLite `mode=ro`, `query_only=ON`, and `trusted_schema=OFF`, with active WAL visibility where applicable. Deleted history rows were excluded. The union of Fedora IDs is 287, equal to the active database's 287; backups add zero IDs.

The older source is:

```text
/var/mnt/STORAGE-10TB/habitat-archive/tier2-substrates/atuin/latest/atuin.tar.zst
```

Only its `atuin/history.db` member was materialized in memory. The source database was 317,566,976 bytes. Its SHA-256 before an in-memory SQLite header adjustment was:

```text
487d7e6ce0cf109ab8fc2c2a9118a5566d559c2e4811aaa66a2c22435c619ed6
```

Archive traversal was bounded to 100 member headers, 4 GiB uncompressed offsets, and 55 seconds. The initial 128 MiB history-member allowance was too small; the successful run used a 1 GiB ceiling. The archive was not extracted to disk. Member payloads other than history were skipped, not inspected for meaning. Key/config filenames can appear in the metadata header list; their contents were not read into the analysis.

The in-memory copy's SQLite header bytes 18/19 were changed to rollback-journal format solely to permit `deserialize` without disk WAL files. The original archive was untouched. All 21 member headers were traversed and no `history.db-wal` member was present. This remains an archived base-checkpoint analysis, not a guarantee that every historical event was captured.

The checkpoint contains 127,613 non-deleted records spanning 2026-01-10 through 2026-08-30 UTC. Its counts remain separate from the Fedora line; no cross-lineage unique lifetime total is claimed. Other older daily archives were not all decompressed.

Discovery covered the listed STORAGE-10TB archive, migration and corpus-backup locations and the current `/var/mnt/mint-nvme15t` directory. Node/dependency/build trees were excluded from the narrowed filename search. SATA and USB historical partitions were unmounted at the later block-device snapshot; their internal files were not examined. A directory named after an old mount is not proof that the old filesystem is mounted there now.

## Interpretation limits

- Process PSS apportions shared mapped memory. It omits unreadable mappings, other users, kernel allocations and unmapped tmpfs. Process names are not exact application/service boundaries.
- The first memory census had six permission-denied smaps reads, four unavailable smaps reads and four exited/unavailable processes. See each JSON's own error counters for its sample.
- Cgroup `memory.current` includes descendants and file cache. `shmem` is a subset of `file`; PSS, cgroup totals, tmpfs allocation and zram sizes must not be summed.
- Thirty-five process FD lists were inaccessible in the temporary-file attribution. Absence of an observed open reference is not proof a directory can be deleted.
- Diskstats, PSI and vmstat have different intervals and visibility. The short samples leave the I/O-pressure cause unresolved.
- Atuin counts are records, not proven human actions. Leading-token classification does not parse a complete shell program. Keyword counts are mentions, not execution counts.
- Archive command inspection was limited to the first 4,096 characters per record. This can undercount keywords and classify truncated quoting as unparsed. Saved analysis code applies that bound to future database runs too.
- Recorded durations are elapsed spans. The statistic originally called `median_seconds` has been relabeled **`upper_median_seconds`** in these aggregates because even samples used the upper middle item. Values were not changed. Neither duration statistic measures CPU, RAM or productive time.
- Exit `-1` is unknown/unfinished; 137 is not by itself evidence of an OOM event. GUI activity and all agent tool calls are not comprehensively represented.

## Reuse

The memory collector is specific to this Linux host's UID 1000, cgroup layout and zram device. Invoke it from Toolbx through the host boundary for a comparable reading:

```bash
flatpak-spawn --host python3 \
  '/var/mnt/STORAGE-10TB/fedora-obsidian-vaults/toolshed.vault/40 Reference/lukes-workflows/2026-09-06/memory-audit.py'
```

It prints a fresh JSON snapshot. Save new readings under a new timestamp; do not overwrite these dated baseline files. A representative build needs sampling during the workload to establish its peak.

The history script's default mode reads the active database and the adjacent discovery list. It accepts `--active` and `--discovery` overrides. Archive mode takes `--archive` and requires Python 3.14+ for standard-library Zstandard support. Reading a large archive transiently uses memory; routine management should use the saved aggregates unless a new question requires another pass. Do not substitute a copied historical binary or import old history/configuration just to reproduce this analysis.

Check bundle integrity from this directory with:

```bash
sha256sum --check SHA256SUMS
```

No workload limits, cleanup timers, shell startup changes or service shutdowns were installed. Recommended next trials and primary web references are in [[50 Field Notes/lukes workflows|the assessment]].
