---
tags: [hermes, recovery, location, workflow]
created: 2026-09-15
updated: 2026-09-15
---

# Hermes Recovery Location

Find the historical Hermes corpus without walking the disk.

```bash
# NVMe pointer (always present)
less ~/.hermes/RECOVERY-LOCATION.md

# Working address (symlink as of 2026-09-15)
readlink -f ~/.hermes/recovery
ls ~/.hermes/recovery

# README inside the archive
less ~/.hermes/recovery/README.md

# Spindle dest
ls /var/mnt/STORAGE-10TB/home-overflow/hermes-recovery
```

Expected `readlink -f` result:

```text
/var/mnt/STORAGE-10TB/home-overflow/hermes-recovery
```

Canonical record: [Hermes Recovery Location 2026-09-15](obsidian://open?vault=herdr-fedora-habitat.vault&file=40%20Agents%2FHermes%20Recovery%20Location%202026-09-15). Recovery *event* (2026-09-05): [Taco Hermes Corpus Recovery](obsidian://open?vault=herdr-fedora-habitat.vault&file=40%20Agents%2FTaco%20Hermes%20Corpus%20Recovery). OS placement: [Hermes Recovery on the Spindle](obsidian://open?vault=fedora-kinoite.vault&file=Hermes%20Recovery%20on%20the%20Spindle).

Do not mine the raw archive into MemPalace. Do not delete `pif-*` / `pi-harness-engine` cache as part of this location.

Related: [[00 - Toolshed Index]] · [[mempalace]]
