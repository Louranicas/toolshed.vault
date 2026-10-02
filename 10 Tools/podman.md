---
tags: [tool, podman, containers, sandboxes, reference, verified]
created: 2026-09-04
verified_on: podman 5.8.4 · rootless · cgroups v2 · netavark + crun + pasta · Fedora Kinoite 44
source: the installed binary first, docs.podman.io second
updated: 2026-09-06
---

# 🐋 podman — the command surface I actually need

**Navigation:** [[40 Reference/Command Matrix#Composition and verification routes|Command Matrix ⇄ composition routes]] · [[00 - Toolshed Index|Toolshed master index]]. Follow the container CLI companion to the matrix’s podman-tui row.

Companion to [Podman & Containers](obsidian://open?vault=fedora-kinoite.vault&file=Podman%20%26%20Containers)
(OS integration) and [Podman Quadlets and Rootless Mastery](obsidian://open?vault=fedora-kinoite.vault&file=Podman%20Quadlets%20and%20Rootless%20Mastery)
(containers as systemd units). **This note is the verb surface** — organised by what I am trying to
do, because alphabetical reference is what `--help` is for.

> [!important] Podman runs on the HOST. I do not.
> Every command below is prefixed `flatpak-spawn --host` when issued from inside the toolbox.
> Omitting it is the single most common failure, and the error never names the layer.
> ```bash
> H() { flatpak-spawn --host "$@"; }     # then: H podman ps
> ```

## Ground truth `[VBR]`

```
podman 5.8.4   rootless=true   cgroups=v2   netavark + crun + pasta
graphroot  ~/.local/share/containers/storage      runroot  /run/user/1000/containers
subuid/gid Louranicas:524288:65536                socket   /run/user/1000/podman/podman.sock
```

**60 top-level commands.** The ones below are the ones this habitat uses; the rest exist.

## 1 · Run, exec, inspect — the daily verbs

```bash
podman run --rm -it <image> <cmd>              # throwaway, interactive
podman run -d --name <n> --replace <image>     # daemonised; --replace kills a stale same-name
podman run --rm -v "$PWD:/src:ro,z" alpine ls /src        # LOWERCASE z — see traps
podman exec -it <ctr> bash                     # into a running container
podman exec <ctr> sh -lc 'cmd'                 # one-shot, scriptable
podman ps            / podman ps -a            # running / all
podman ps --format '{{.Names}} {{.Status}}'    # scriptable, no jq needed
podman inspect <ctr> --format '{{.State.Health.Status}}'
podman logs -f <ctr>          podman top <ctr>        podman stats --no-stream
podman kill / stop / start / restart / rm [-f] <ctr>
podman wait <ctr>                              # block until exit, print the code
podman cp <ctr>:/path ./local  /  podman cp ./local <ctr>:/path
podman diff <ctr>                              # what changed in its filesystem
podman events --since 5m --format json         # the event stream
```

**Resource caps — always, for anything that might run away:**
```bash
--memory 4g --memory-reservation 2g --cpus 4.0 --pids-limit 512
```
`--memory`/`--cpus` are **unsupported on cgroups v1 rootless**; v2 here, so they apply `[VBR]`.

## 2 · Mounts — where the SELinux traps live

| form | meaning |
|---|---|
| `-v host:ctr:ro` | read-only |
| `-v host:ctr:ro,z` | **shared** SELinux label — several containers may read it |
| `-v host:ctr:Z` | **private** label; **relabels the host path** → needs write → **fails on `:ro`** |
| `-v host:ctr:U` | recursively chown source to the container's UID/GID |
| `--mount type=tmpfs,dst=/tmp` | the explicit form; supports `tmpfs`, `image`, `artifact`, `glob`, `ramfs` that `-v` cannot |
| `--read-only --read-only-tmpfs` | immutable rootfs with writable `/dev /run /tmp /var/tmp` |

## 3 · Images & builds

```bash
podman images --format '{{.Repository}}:{{.Tag}} {{.Size}}'
podman pull <ref>            podman rmi <img>          podman tag <img> <new>
podman build -t <tag> -f Containerfile .
podman save -o out.tar <img>       podman load -i out.tar
podman history <img>               podman image prune -f
podman search <term>               podman login / logout <registry>
```
**Digest-pin anything that matters** — a `:latest` in a FleetPodSpec fails contract validation by
design ([Schematic - Advanced Deployment Architecture](obsidian://open?vault=herdr-fedora-habitat.vault&file=95%20Genesis%2FSchematic%20-%20Advanced%20Deployment%20Architecture)).

## 4 · Volumes, networks, pods

```bash
podman volume create/ls/inspect/rm <v>     podman volume prune
podman network create/ls/inspect/rm <n>    # netavark backend here
podman pod create --name <p>               podman pod ps / start / stop / rm
```
Rootless networking is **pasta** (`/usr/bin/pasta` *(host-only; verified on the host — it is not in the toolbox's `/usr`)* `[VBR]`) — it preserves the original source IP
on forwarded ports. Without it, rootless containers must share the host netns.

## 5 · Secrets `[VBE]`

```bash
podman secret create <name> <file>          # or: printf '%s' "$v" | podman secret create <name> -
podman secret create --env <name> ENVVAR    # read from an env var
podman secret create --driver pass <name> <file>     # GPG-encrypted
podman secret ls / inspect / rm / exists <name>
podman run --secret source=<name>,type=mount,target=/run/secrets/x,uid=1001,gid=1001,mode=440 …
podman run --secret <name>,type=env,target=MY_VAR …
```
Drivers: **`file`** (read-protected), **`pass`** (GPG-encrypted), **`shell`** (custom scripts, given
`SECRET_ID`, over stdin/stdout).

> [!warning] The docs do not say the `file` driver is encrypted at rest
> They say only *"read-protected file"*, and they do not state where rootless secrets are stored.
> **Treat the default driver as unencrypted until proven otherwise** — use `pass` for anything that
> matters, and verify by reading the store rather than the documentation.

## 6 · Quadlet — and a subcommand the published docs do not mention

`podman quadlet` is a **top-level command in 5.8.4** `[VBR]`; the docs I fetched described only the
systemd generator. **Ground truth beats docs, again.**

```bash
podman quadlet list            # NAME · UNIT NAME · PATH ON DISK · STATUS · APPLICATION
podman quadlet print <name>    # show the file
podman quadlet install <file>  # install a quadlet or a whole application
podman quadlet rm <name>
```

Still the mechanism underneath:
```bash
~/.config/containers/systemd/<name>.container      # rootless location
systemctl --user daemon-reload                     # the generator runs HERE, not on write
systemctl --user start <name>.service
/usr/libexec/podman/quadlet --user --dryrun        # print the generated unit, install nothing
```

## 7 · System, storage, diagnostics

```bash
podman system df            # what storage is actually costing
podman system prune -a      # ⚠ enumerate first — see traps
podman system info --format '{{.Host.CgroupsVersion}}'
podman system migrate       # after a subuid/subgid change
podman unshare <cmd>        # run inside your user namespace — how to touch mapped-subuid files
podman healthcheck run <ctr>
podman auto-update          # honours AutoUpdate= in quadlets
```

## 8 · Scripting flags

```bash
--log-level error            # quiet the noise in cascades
--url unix:///run/user/1000/podman/podman.sock     # or CONTAINER_HOST
--root / --runroot           # alternate storage — useful for a truly isolated experiment
--format json | --format '{{.Field}}'              # every list/inspect verb takes it
```

## 9 · The sandbox recipes this habitat actually runs

`habitat-sandbox` wraps these, but the underlying command is what to reach for when debugging it.

```bash
# a Rust build sandbox — every flag here is a scar
podman run --rm \
  -v "$REPO:/src:ro,z" \
  -v "$HOME/.rustup/toolchains/stable-x86_64-unknown-linux-gnu:/rust:ro,z" \
  -v "$OUT:/out:z" \
  -e CARGO_HOME=/out/cargo -e CARGO_TARGET_DIR=/out/target \
  -e PATH=/rust/bin:/usr/bin:/bin \
  --memory 4g --cpus 4.0 --pids-limit 512 \
  localhost/forge-sandbox:1 \
  bash -lc 'cd /src && cargo test --locked'
```

| flag | the scar |
|---|---|
| `forge-sandbox:1`, not the toolbox base | the base image has **no `cc`/`ld`/`gcc`** `[VBR]` — `cargo test` dies at link |
| `:ro,z` | `:Z` relabels, relabelling needs write, so `:ro,Z` fails as a bare "Permission denied" (F33) |
| `/rust` mounted | rustup keeps the compiler in `$HOME/.rustup`, **outside any project tree** |
| `CARGO_HOME=/out/cargo` | `CARGO_HOME` is unset here → all cargo shares `~/.cargo/.package-cache`, **one global lock across every repo**; the loser prints `Blocking waiting for file lock` (**F80**) |
| `CARGO_TARGET_DIR=/out/target` | a child cargo **inherits** it and can overwrite the crates under test (**F46**) |
| own `/out` | two workers cannot corrupt each other's results *even if a task is written badly* — and one was |

## 10 · Traps, all paid for here

1. **`:Z` cannot relabel a read-only mount** — use `:ro,z` (F33).
2. **A minimal image is a different userland, not a smaller one** — Alpine's BusyBox `grep` has no
   `--include` and returns confident zeros (F34).
3. **The user socket ships disabled on Kinoite** — `systemctl --user enable --now podman.socket`;
   `podman-tui` and any `DOCKER_HOST` client need it.
4. **`podman system prune -a` is a blanket command** — enumerate before running it. A directory
   label true of 99.9% of its contents is exactly where a blanket is most dangerous.
5. **`podman-user-wait-network-online.service` fails by timeout** on this box (podman issue #22197).
   `podman.service` is unaffected — but a health sweep that treats any failed unit as fatal will
   trip on it forever.
6. **`--memory`/`--cpus` are silently unsupported on cgroups v1 rootless.** v2 here, so they work —
   check `podman info --format '{{.Host.CgroupsVersion}}'` before assuming on another box.
7. **Rootless Quadlet forbids `User=`/`Group=`/`DynamicUser=`** in `[Service]`.
8. **Generated units are `STATE=generated`** — `systemctl --user enable` does not persist them; the
   generator applies `[Install]` at `daemon-reload`.

## Rust performance practice

Use [[40 Reference/Perfecting Rust - Performance Engineering#Write an experiment contract|the Rust experiment contract]] alongside this note’s sandbox recipes to record the actual execution boundary, compiler, features and resource limits. [[40 Reference/Perfecting Rust - Performance Engineering#Linux command recipes|The profiling recipes]] distinguish session-visible tools from host capability; [[40 Reference/rust-mastery/2026-09-06/README#Reproduce in a working copy|the lab guide]] gives a bounded reproduction exercise.

Related: [[00 - Toolshed Index]] · [[podman-tui]] · [[Sandbox Fanout and Fusion]] ·
[[Claim-Time Guard]] · [[00 - Field Findings]] · [[Cascade Engine]] · [[Arena Practice Ground]]

---
> 🔗 **Cross-vault.** OS integration and the quadlet contract:
> [Podman & Containers](obsidian://open?vault=fedora-kinoite.vault&file=Podman%20%26%20Containers) ·
> [Podman Quadlets and Rootless Mastery](obsidian://open?vault=fedora-kinoite.vault&file=Podman%20Quadlets%20and%20Rootless%20Mastery) ·
> where these recipes are used: [Wave Deployment Architecture](obsidian://open?vault=herdr-fedora-habitat.vault&file=95%20Genesis%2FWave%20Deployment%20Architecture) ·
> the layer lesson: [Working in Sandboxes on Kinoite](obsidian://open?vault=my-diary.vault&file=Reflections%2FWorking%20in%20Sandboxes%20on%20Kinoite)
