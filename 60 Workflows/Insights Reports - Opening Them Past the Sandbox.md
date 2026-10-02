---
tags: [workflow, claude-code, flatpak, kinoite, sandbox, hooks, verified]
created: 2026-09-14
status: LIVE — Stop reflex armed, proven to fire, and confirmed rendering in Chrome
---

# 📊 Insights Reports — Opening Them Past the Sandbox

## The current report

**file:///var/home/Louranicas/Documents/claude-insights-2026-09-14-055623.html**

`71,943 bytes · 203 messages across 8 sessions (11 total) · 2026-09-01 → 2026-09-13`
Source of record: `~/.claude/usage-data/report-2026-09-14-055623.html` — the same bytes, in a
directory your browser cannot read. Confirmed rendering in Chrome at the published path.

*(Earlier: `~/Documents/claude-insights-2026-09-11.html`, the 2026-09-11 edition.)*

## Why the link `/insights` prints does not work

`/insights` writes to `~/.claude/usage-data/` and prints a `file://` link into it. Chrome on this
machine is a **flatpak**, and its sandbox grants exactly:

```
filesystems = host-etc; xdg-music; xdg-pictures; xdg-videos; xdg-download;
              xdg-documents; xdg-run/dconf; xdg-run/pipewire-0     shared = ipc; network
```

`~/.claude` is in none of them, so the link is `ERR_FILE_NOT_FOUND` — twice now, 2026-09-11 and
2026-09-14. **The file is fine; the reader cannot reach it.** On an immutable distribution this is
the normal state of affairs rather than a fault: applications are sandboxed, and the filesystem is
the thing you do *not* reshape.

> The question is never *"how do I widen the sandbox?"* first. It is **"which door is already
> open?"** — a granted directory, the network, or the portal. Widening a sandbox is the last
> resort, not the first fix.

## The three doors, all measured on this machine

| # | route | how | evidence |
|---|---|---|---|
| 1 | **A granted directory** | copy into `~/Documents` (`xdg-documents` is granted) | `71,943 bytes, mode 644`, renders |
| 2 | **The network** | `shared=network` is granted, so serve over loopback | `HTTP 200 bytes=71943 <title>Claude Code Insights` |
| 3 | **The portal** | `xdg-desktop-portal` + `-kde` + `-gtk` are `active`; open with the browser's own dialog (Ctrl+O) or drag the file in — the portal grants access to *that file* | portal services `active` |

**The route deliberately not taken**, although it works and was authorised:

```bash
flatpak override --user --filesystem=~/.claude/usage-data:ro com.google.Chrome   # ← declined
```

It permanently widens a **browser's** sandbox to reach an **agent's state directory**, whose sibling
paths hold transcripts and credentials. That is a poor trade for a convenience link. It also needs
a browser restart, because a running flatpak keeps the permissions it started with.
Reversible with `--nofilesystem=~/.claude/usage-data`.

## It is automatic now — two layers

**`~/.claude/hooks/insights-publish.sh`** — a **`Stop` reflex**. At the end of any turn in which a
new report appeared, it publishes the report into `~/Documents`, **verifies the copy by size and
readability** rather than trusting `cp`'s exit status, and surfaces the working link. Idempotent: an
ordinary turn costs one `stat` and prints nothing.

```
habitat-reflex verify → reflexes=6 unproven=0        apply → installed=6
control   a fresh report  → INSIGHTS_READY + published
repeat    same report      → silent
quiet     no report at all → silent
LIVE      fired in production the turn it was installed
```

**`~/.local/bin/insights-link`** — the on-demand form, for a human with no agent present:

```bash
insights-link            # publish the newest report, print the working file:// link
insights-link --serve    # route 2 instead: serve ~/.claude/usage-data on 127.0.0.1:8731
```

Both refusal paths are controlled: no report, and an unwritable destination — each exits `rc=1` and
prints **no link**, rather than a link to nothing.

## Opening it from a shell — `xdg-open` will not do it

```bash
# ✗ silently does nothing: xdg-open → ~/.local/bin/kde-open → exec flatpak-spawn (absent on the host)
flatpak-spawn --host xdg-open "file://$HOME/Documents/claude-insights-….html"

# ✓ the route that works
flatpak-spawn --host flatpak run com.google.Chrome "file://$HOME/Documents/claude-insights-….html"
```

See **F145**. The wrapper assumes it is being called from *inside* a container; called from the host
it `exec`s a binary that is not there, prints one line, and opens nothing.

## What the report found, and what is being done about it

The report is not only a link — it measured 28 friction events across 203 messages, 17 of them defects in the agent's own throwaway scripts. The response, one row per issue class with a mechanism, a cost, a control, a falsifier and an owner:
**[[Mitigation Plan]]**.

## Where the evidence lives

- [[50 Field Notes/00 - Field Findings#F144 · A flatpak browser cannot open `~/.claude` — three routes fix it without touching the sandbox|F144]] — the sandbox boundary and the three routes
- [[50 Field Notes/00 - Field Findings#F145 · `xdg-open` is broken on this machine — `kde-open` calls `flatpak-spawn` from the host|F145]] — the launcher shim, and the pipe that hid its failure
- [[60 Workflows/Claim-Time Guard]] — the reflex surface this hook is installed through
- [Deploying the Diary's Learnings § Move 8](obsidian://open?vault=herdr-fedora-habitat.vault&file=50%20Automation%2FDeploying%20the%20Diary%27s%20Learnings) — the deployment record
- [my-diary § Mistakes #44](obsidian://open?vault=my-diary.vault&file=Reflections%2FMistakes%20I%20Made) — the fifth pipe-swallowed verdict, which is how the broken `xdg-open` first read as a success

## Falsifier, dated 2026-10-14

If `/insights` ever writes somewhere the sandbox can read, or the browser gains access to
`~/.claude`, the hook is dead weight — **delete it**. If it fires on a turn where no report was
made, it is noise — **delete it rather than tune it**. A mechanism that survives on neither piece
of evidence is ceremony.

> 🔗 **Cross-vault synergy.** The boundary this note is about is the OS layer's, not Claude's:
> [kinoite § Podman & Containers](obsidian://open?vault=fedora-kinoite.vault&file=Podman%20%26%20Containers) ·
> [kinoite § Immutable OS Concepts](obsidian://open?vault=fedora-kinoite.vault&file=Immutable%20OS%20Concepts) ·
> [kinoite Master Index](obsidian://open?vault=fedora-kinoite.vault&file=00%20-%20Fedora%20Master%20Index) —
> each carries a row back here. A sandboxed app that cannot read a path is the distribution working
> as designed; the fix is to find the open door, not to widen the wall.

Related: [[00 - Workflows]] · [[Claim-Time Guard]] · [[Mitigation Plan]] · [[00 - Toolshed Index]] ·
[[50 Field Notes/00 - Field Findings]] ·
[Fedora Master Index](obsidian://open?vault=herdr-fedora-habitat.vault&file=00%20-%20Fedora%20Master%20Index)
