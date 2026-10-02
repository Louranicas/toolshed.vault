---
tags: [toolshed, tool, workspace-4, containers]
tool: podman-tui
version: 1.11
upstream: https://github.com/containers/podman-tui
workspace: W4 · pane w1:pP
agent_door: habitat q podman-tui <args>  →  flatpak-spawn --host podman
---

# podman-tui — container dashboard

Function-key navigated TUI over the podman API. On Kinoite podman **is** the container runtime (no docker).

## Views

`F1` help · `F2` **system** · `F3` pods · `F4` containers · `F5` volumes · `F6` images · `F7` networks · `F8` secrets. Header shows connection status, kernel, API version, OCI runtime (crun), conmon/buildah versions, memory/swap gauges.

Within a view: arrows/`Tab` move · `Enter` inspect · `c` create · `d` delete · `s` start · `t` stop · `r` restart · `p` pause · `l` logs · `e` exec · `/` filter · `?` commands menu.

## ⚠️ Two Kinoite facts this tool depends on

1. **`podman` does not exist inside the toolbox.** The toolbox *is* a podman container; podman is host-side. Every scripted call must escape: `flatpak-spawn --host podman …` — which is exactly what `habitat q podman-tui` does.
2. **The user socket ships disabled.** podman-tui talks to `/run/user/1000/podman/podman.sock`; Kinoite leaves it inactive *and* disabled, so the TUI opens on a connection-error dialog until:
   ```bash
   flatpak-spawn --host systemctl --user enable --now podman.socket
   ```
   Enabled here 2026-09-02 — now reports `Connection: ✅ STATUS_OK` and sees `fedora-toolbox-44` itself. The toolbox bind-mounts `/run/user/$UID`, so the socket appears inside the container with no restart.

## The agent door — `podman` CLI

```bash
podman ps --format json  ·  --format '{{.Names}} {{.Status}}'
podman images --format json  ·  podman logs <ctr>  ·  podman inspect <ctr>
podman stats --no-stream --format json
podman system df  ·  podman system prune -a
podman generate systemd / Quadlet          # run containers as user services
podman run --rm -it fedora:45 bash
```

**Quadlet** is the modern autostart path: a `.container` unit in `~/.config/containers/systemd/` *(user-authored; absent until you create it)*, then `systemctl --user daemon-reload && start`. Survives reboot with `loginctl enable-linger`.

## Chains

**Feeds into:** `--format json` → [[jqp]]/[[nushell]]. `podman ps --format '{{.Names}}' | fzf | xargs -r podman logs` is the canonical [[fzf]] chain.

> [!info] The CLI beneath this TUI — [[podman]]
> `podman-tui` is the human-first face; the agent door is the verb surface, including the
> socket this TUI needs (`systemctl --user enable --now podman.socket` — Kinoite ships it
> **disabled**).

Related: [[bottom]] · [[jqp]] · [[Tool Clusters]] · [[00 - Toolshed Index]] ·
[[Command Matrix]] · [[Sandbox Fanout and Fusion]]
