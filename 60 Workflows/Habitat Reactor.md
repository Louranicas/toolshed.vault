---
tags: [toolshed, workflow, herdr, event-bus, self-healing, systemd]
created: 2026-09-02
updated: 2026-09-06
source: ~/.local/bin/habitat-reactor · ~/.config/systemd/user/habitat-reactor.service
---

# 🔁 Habitat Reactor — self-healing on the event bus

`local.habitat-services` respawns the cockpit **once**, at session start. Nothing noticed when a
service died *during* a session — the habitat could sit half-dead for hours looking fine. The
reactor closes that.

## What it is

A systemd user service that holds a subscription to herdr's socket event bus, keeps the
service→pane map fresh from topology events, and sweeps for dead services on a slow poll.

```bash
systemctl --user status habitat-reactor        # via flatpak-spawn --host
journalctl --user -u habitat-reactor -f
tail -f ~/.local/state/habitat/reactor.log
habitat-reactor --dry-run                      # observe/log; suppress respawn
habitat-reactor --once                         # print the next event and exit
```

## Discovery: herdr has an event bus nothing was using ⭐

`herdr api schema --json` exposes **`events.subscribe`** and **`events.wait`** over the NDJSON
socket, with 26 event types:

```
pane.created  pane.closed  pane.exited  pane.updated  pane.moved  pane.focused
pane.agent_detected  pane.agent_status_changed  pane.output_matched  pane.scroll_changed
tab.created/closed/focused/moved/renamed
workspace.created/updated/renamed/moved/closed/focused/reordered/metadata_updated
worktree.created/opened/removed        layout.updated
```

Subscribe by writing one NDJSON line to `~/.config/herdr/herdr.sock`:

```json
{"id":"sub","method":"events.subscribe","params":{"subscriptions":[{"type":"pane.exited"}]}}
→ {"id":"sub","result":{"type":"subscription_started"}}
```

`pane.output_matched` additionally takes `pane_id`, `source`, `strip_ansi`, `lines` and a
`match` of `{"type":"substring"|"regex","value":…}`.

## The hard finding: the bus has no service-death signal

Two independent facts, each verified:

- **[[00 - Field Findings|F17]] `pane.exited` is about the pane, not its process.** A dying TUI
  leaves the pane alive at a bash prompt; nothing is emitted.
- **[[00 - Field Findings|F22]] `pane.output_matched` fires only on newly-*written* output.** It
  works (verified by writing a sentinel and catching the event with its `matched_line`) — but an
  **alt-screen TUI exiting restores the primary screen without writing anything**, so a dying
  service produces no match.

There is no "foreground process changed" event. **So the bus cannot tell you a service died.**

## The resolution: bus for topology, poll for liveness

```python
POLL_SECONDS = 20
s.settimeout(POLL_SECONDS)
while True:
    try:
        chunk = s.recv(65536)          # topology events keep the map fresh
    except socket.timeout:
        sweep()                        # liveness: process-info vs registry `proc`
        continue
```

`sweep()` compares each service's expected `proc` (from `~/.config/habitat/services.json`)
against `herdr pane process-info`, and respawns only panes that are genuinely idle
(`fg ⊆ {bash, sh}` — a pane busy with something else is left alone).

The code excerpt above illustrates the original approach. The installed implementation also
checks elapsed time in the event loop, so a busy bus cannot indefinitely postpone a sweep.
The `pane.output_matched` descriptions here and in [[60 Workflows/Autonomous Triggers]] record
different earlier experiments; they are not a new verification of current Herdr event semantics.

## Intentional shutdown and recovery policy

The installed reactor examines registered process names and respawns missing services in idle
panes. It has **no explicit per-service intentional-suspension field in the inspected logic**.
Closing a managed TUI to save resources can therefore be undone by the next sweep. The
`--dry-run` path suppresses respawn but still connects, observes and appends to its log.

Before retiring a heavyweight service, identify whether this reactor, another supervisor or
the session-start configuration owns it. A future demand-based service policy needs an explicit
distinction between wanted, intentionally stopped and unexpectedly failed. Until that exists,
coordinate shutdown with the owning supervisor; do not use repeated process killing as a
resource-management loop. No supervisor was stopped or reconfigured by this review.

The sweep also launches several process-info commands, so its own polling cost belongs in the
budget. See [[50 Field Notes/lukes workflows#Process groups worth reviewing|measured process groups]]
and [[60 Workflows/00 - Workflows#Daily operating cycle — reviewed 2026-09-06|the daily cycle]].

## The envelope trap

Events do **not** look like responses ([[00 - Field Findings|F23]]):

```json
{"event": "pane_updated", "data": {"pane": {...}, "type": "..."}}
```

Name at the **top level, snake_case**; subscriptions use **dotted** names. Reading `result.type`
— the natural guess from the request schema — matches nothing, forever, silently. This cost three
debugging rounds and is the single most valuable thing in this note.

Also: **`pane.updated` is extremely chatty** ([[00 - Field Findings|F24]]) — agent status churn
floods it. Subscribe to specific topology events.

## Why systemd, not a background process

`setsid nohup … &` does not survive the agent harness ([[00 - Field Findings|F25]]). On Kinoite
the correct home is a user unit anyway — `$HOME`, restart policy, journal integration:

```ini
[Unit]
After=herdr-server.service
BindsTo=herdr-server.service
PartOf=graphical-session.target

[Service]
Type=exec
ExecStart=/usr/bin/toolbox run --container fedora-toolbox-44 %h/.local/bin/habitat-reactor
Restart=always
RestartSec=10

[Install]
WantedBy=graphical-session.target
```

`BindsTo=herdr-server.service`, together with `After=`, ties reactor lifetime to server
availability. It does not by itself guarantee the reactor will be started again whenever the
server returns; check the actual activation relationships when changing this policy.

## Proven

```
20:35:32  subscribed: 5 topology events + 16 prompt watches
20:35:32  pane_created: re-resolved service map (16 panes)
20:35:52  poll: tuicr down in w1:pR -- respawning
20:35:52    ->   1 started · 0 already running · 0 missing
```
`tuicr` killed → back within 20 s → `12 running · 4 shell · 0 stopped`.

Captured by `habitat-settings-backup`; `habitat-settings-restore` re-enables the unit.

Related: [[herdr]] · [[00 - Field Findings]] · [[00 - Workflows]] · [[00 - Habitat Toolkit]] ·
[[00 - Toolshed Index]] · [[Autonomous Triggers]] · [[Cascade Engine]]
