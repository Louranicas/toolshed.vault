# Inotify incident evidence — 2026-09-06

SOL3 investigated and resolved KDE's reported inotify instance capacity warning on the Fedora Kinoite Herdr habitat. Read [[50 Field Notes/Linux Inotify Capacity - Herdr Habitat|the operational finding]] for the decision, sources, measurements, and rollback procedure.

| Artifact | Purpose |
|---|---|
| `host-before.json` | Independent host FD-reference census, namespace IDs, limits and visibility limitations |
| `kde-before.json` | KDE warning metric before application; command arguments removed |
| `kde-after.json` | KDE measurement after host and nested sandbox functional tests; command arguments removed |
| `herdr-context.json` | Reduced live layout, roles and working directories; no terminal transcript or agent session identifiers |
| `90-herdr-inotify.conf` | Exact host configuration payload |
| `apply-inotify.py` | Guarded host apply and explicit rollback, with recovery on application failure |
| `apply-result.json` | Host root operation receipt: 128 → 2048 |
| `inotify-audit.py` | Reusable read-only process census; explicitly labels FD-reference limitations |
| `verify-inotify.py` | Bounded functional test with descriptor and scratch cleanup |
| `verify-host.json` | 160-instance and file-event proof on the host |
| `verify-toolbx-sandbox.json` | Same proof in the nested execution sandbox |
| `verify-herdr-toolbx.json` | Same proof in the actual Herdr Toolbx user namespace |
| `persistence-and-refresh.json` | Host file metadata, relevant merged boot-configuration lines and successful KDE refresh |
| `management-hardware-snapshot.json` | Follow-up five-second host measurement: CPU/RAM/storage, pressure, disk activity and attribution limitations |
| `management-kinoite-state.json` | Filtered booted/staged/live deployment state, cgroup version and Herdr service location |
| `hardware-capacity-snapshot.py` | Reusable read-only interval collector; no benchmark or disk self-test |
| `save-to-toolshed.py` | Historical initial publication helper; subsequent note edits supersede its original home-directory payloads |
| `Prime Receipt.md` | Bounded vault navigation and evidence ceiling |
| `original-context.png` | User-supplied screenshot of terminal/workspace context; not a transcription of the warning |
| `SHA256SUMS` | Checksums of this evidence bundle, excluding the checksum file itself |

Times in JSON use UTC; the task date is 2026-09-06 in Australia/ACT. All scripts are standard-library Python and are invoked with `python3`; no dependency installation or monitoring daemon was added. Privileged scripts require normal host administrator authentication. The bootstrap work directory was `/var/home/Louranicas/herdr-inotify-20260906`.

Persistence was inspected without rebooting. Rollback was documented and code-reviewed, not executed on the live system. KDE refresh was invoked successfully; GUI dismissal was not visually inspected. No terminal messages were sent to other agents, and no fleet runtime was activated.

## Future management addition — 2026-09-06

The operational finding now includes a future management narrative, Kinoite maintenance/recovery considerations, two Mermaid schematics, workload budgeting, a hardware assessment and conditional recommendations, with primary web references. Follow-up read-only evidence found ample available RAM and NVMe space, high reported I/O pressure without a busy device established by the short interval, and staged/live rpm-ostree state to review before planned maintenance. No upgrade, migration, reboot, scheduler gate, UPS service, backup job or hardware purchase was performed.

Additional local notes consulted: Kinoite `Fedora Kinoite - System Overview.md`, `System Maintenance.md`, and the relevant portion of `Podman Quadlets and Rootless Mastery.md`. Historical notes were kept distinct from current observed state, including the old HDD mount path. Related architecture and backup notes are navigation references, not claims that their entire contents were reread or revalidated. The SHA-256 manifest was regenerated after adding these artifacts and updating this inventory.
