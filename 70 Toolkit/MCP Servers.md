---
tags: [toolshed, mcp, protocol, progressive-disclosure, servers]
created: 2026-09-02
protocol: "2026-07-28"
location: ~/.local/lib/habitat-mcp/
---

# 🔌 MCP Servers — the learnings as live tools


> **⚓ Code anchor** — `~/.local/lib/habitat-mcp/mcp2.py:134` · expects `if method == "server/discover":`
> Protocol 2026-07-28 replaces `initialize` with `server/discover`. The server speaks **both**: built to v2 only, it returned -32601 to Claude Code and was unreachable until 2026-09-03. Fragment made unique after a 3-way match showed the first one was ambiguous.
> *Verified 2026-09-03 · re-check `just doc-anchors`; this note updates when the code does.*

Two MCP servers built to protocol revision **2026-07-28**, registered at **user scope**
(`claude mcp list`). Where the [[Authored Skills|skills]] load *instructions*, these expose *live
state and callable probes* — the thing prose cannot be: current.

| Server | Tools | Templates | Resources | Prompts |
|---|---|---|---|---|
| **`cockpit`** | 8 | **4** | 7 | 3 |
| **`ground-truth`** | 4 | — | 3 | 1 |

`cockpit` supersedes an earlier 7-tool `habitat` server, which was retired rather than left
alongside it — two servers with overlapping tools make tool selection worse, not better.

## ⚠️ Built to spec, and unreachable (2026-09-03)

Both servers were written to protocol **2026-07-28**, which replaces the `initialize` handshake
with `server/discover`. Claude Code's default SDK generation still calls `initialize` — so both
servers answered `-32601: method not found: initialize` and **failed to connect**, for as long as
they had existed. They were registered, documented in this vault, indexed, and dead.

```
cockpit:      ✘ Failed to connect — -32601: method not found: initialize
ground-truth: ✘ Failed to connect — -32601: method not found: initialize
```

**Fix:** `mcp2.py` now answers *both* handshakes — `initialize` (echoing the client's
`protocolVersion`) and `server/discover`. Everything downstream was already v1-shaped
(`name`/`description`/`inputSchema`, `content:[{type:text}]`), so the handshake was the only gap.

```
cockpit:      ✔ Connected
ground-truth: ✔ Connected
```

**The lesson, and it is the sharpest one available:** *presence is not integration*. Registered,
documented and correct-to-spec are three different things from **reachable**. Nothing in the
build or the documentation could have caught this — only sending a real request from the real
client. Verify a server by handshaking with it, never by reading its source.
→ [[Code Anchors - Notes That Land on Source]] · [[Assimilation - Rules That Fire]]

## New tools — claims that have to be earned

| tool | what it does |
|---|---|
| `ws_check kind=verify` | **proves the detectors fire** (every negative control must trip) — run before any clean-scan claim |
| `ws_check kind=detect` | scan code for known antipatterns |
| `ws_check kind=anchors` | every vault note still lands on real source (`fix=true` repairs drift) |
| `ws_check kind=session` | scans **this agent's own** commands from the transcript — atuin records only the human's shell |
| `ws_check kind=gates` | fmt / clippy / test on **exit codes**, never through a pipe |
| `ws_check kind=cold` | re-run in a fresh target dir — the only run that catches warm-cache defects |
| `ws_check kind=all` | the W1→W5 assimilation cascade |
| `ws_receipt` | a receipt that **cannot self-certify**: typed verdict, proven-controls flag, finding count, mandatory counter-evidence locator; downgrades itself to `PASS_WITH_GAPS` |

`ws_dispatch` — **advanced tool calling as a callable tool** (2026-09-03)

| mode | what it does |
|---|---|
| `chain` | run a producer, route its output **by shape** (json→W5 · diagnostics→W2 quickfix + W3 hunk · diff→W3 · table→W1) |
| `chain` + `from_editor` | bind `{file} {line} {word} {dir}` from the **live cursor** — W2 as a query source |
| `battern` | one pattern across a named cluster in parallel — services(16) crates(5) vaults(4) detectors(6) repos(31) |
| `poly` | one question of several tools; **disagreement is the finding** — kinds: count, files, json, alive |
| `flow` | the tool-call graph that actually ran |

Thirteen tools total. `ws_check` is one tool with seven modes rather than seven tools — progressive
disclosure applied to `tools/list` itself.

## Why hand-written, not an SDK

No MCP SDK is installed, and this revision changed the protocol shape enough that SDKs are
likely to lag it. `~/.local/lib/habitat-mcp/mcp2.py` implements the data layer directly (~150
lines), which also documents the revision in the place it matters.

## What changed in 2026-07-28

Worth knowing before writing any server against it:

- **Stateless.** There is **no `initialize` handshake**. Every request carries the protocol
  version, client capabilities and client identity in `params._meta` under
  `io.modelcontextprotocol/*`, so a server may infer nothing from earlier requests.
- **`server/discover`** is the mandatory discovery request (every server MUST implement it),
  returning `supportedVersions` + `capabilities`. Clients *may* skip it and send any request
  directly, handling a version error if one comes back.
- **Results carry `resultType`**, and cacheable listings carry **`ttlMs` + `cacheScope`**.
- **Notifications are opt-in**: a client opens a long-lived `subscriptions/listen` stream naming
  the types it wants; the server acknowledges with `notifications/subscriptions/acknowledged`
  and only then delivers. Every notification is tagged with the subscription id.
- **`sampling` and `logging` are deprecated.** Stdio servers log to **stderr**; integrate an LLM
  provider directly if you need completions. **`elicitation`** is the remaining client primitive.

## Progressive disclosure, at the protocol level

This is the design constraint that shaped both servers:

> **`tools/list` is the surface every client pays for on every session. `resources/read` costs
> nothing until something needs it.**

So: **few tools, one-line descriptions**, and the depth behind resources — with tool descriptions
*pointing at* resources rather than inlining them.

```
habitat_cascade  →  "Run a declarative parallel DAG …. See habitat://reference/cascades."
```

`habitat` exposes 7 tools totalling ~90 words of description, while `habitat://reference/*`
carries the pane-driving rules, the four silent cascade traps and the sandbox shape — hundreds of
lines, fetched only when a task actually reaches for them.

Two resources are **generated, not stored**: `habitat://state/panes.json` shells out to
`herdr pane list`, and `habitat://reference/services` is rendered from the live registry — so
neither can drift from reality.

## `cockpit` — all 16 services, three tiers

**The design problem:** 16 services across 5 workspaces. The naive shape is 16+ tools — but
`tools/list` is the surface a client pays for on **every** session, so that taxes every
conversation whether or not it touches the cockpit.

**The answer — three tiers, each paid for only when reached:**

| Tier | Surface | Cost | Contents |
|---|---|---|---|
| 1 | `tools/list` | every session | **8** parameterised tools, one-line descriptions |
| 2 | `resources/templates/list` | on demand | **4 templates** covering all 16 services and all 5 workspaces |
| 3 | `resources/read` | on demand | the depth — pane rules, cascade traps, sandbox shape |

```
ws://service/{service}/screen | /state | /doc      ← 16 services, 3 listing entries
ws://workspace/{n}/summary                          ← 5 workspaces, 1 entry
```

**The enum trick:** the 16 service ids live in the tool's **JSON Schema**
(`inputSchema.properties.service.enum`), not in its description. The model gets the complete list
machine-readably without it costing description text — schema is data, descriptions are prose.

Tools: `ws_overview` · `ws_service` (verb: screen|query|state|doc|restart) · `ws_workspace` ·
`ws_exec` · `ws_cascade` · `ws_sandbox` · `ws_diagnose` · `ws_recall`.

The **two-door model** is encoded in one tool's verbs rather than two tools: `verb=query` returns
a **value**, `verb=screen` returns **what is on screen**.

`ws_exec` defaults to `dry_run=true` and reports whether the target pane is idle or busy —
because sending keys to an already-idle pane types them literally and corrupts the next command.

Prompts: `workspace_triage` (knows `·` is not a fault), `workspace_tour`, `service_deep_dive`
(which insists on verifying a documented door before scripting it).

## Claude Code specifics (the "v2" client)

Claude Code runs a v2 MCP client runtime (`MCP_SDK_GENERATION=v1|v2`) with
`MCP_PROTOCOL_NEGOTIATION=auto|legacy`. Two things worth honouring:

- **`MAX_MCP_OUTPUT_TOKENS`** caps total MCP output (default 25,000), and a server may declare a
  **per-tool** character budget in the tool's `_meta`:
  ```json
  "_meta": { "anthropic/maxResultSizeChars": 60000 }
  ```
  Every `cockpit` tool declares one, sized to what it can return (20k for a status line, 80k for a
  whole workspace with screens). Declaring it *is* progressive disclosure — a tool that can return
  a document should say so rather than silently consuming the client's budget.
- **`timeout`** is per tool call, set at registration:
  ```bash
  claude mcp add-json --scope user cockpit \
    '{"type":"stdio","command":"~/.local/bin/workspace-mcp","timeout":600000}'
  ```

Tool names reach the model as `mcp_<server>_<tool>` at user scope — so `mcp_cockpit_ws_overview`.
Scope precedence is local → project (`.mcp.json`) → user → plugin → connectors. `workspace` is a
**reserved** server name; `cockpit` is not.

## `ground-truth` — verify before you script

`probe` · `hang_check` · `shape_check` · `recall_trap`, over the verified-traps catalogue.

**`hang_check` distinguishes three different causes of "no output"** by running the command twice
— once with stdin as an **open pipe that never delivers**, once at EOF:

| Result | Meaning |
|---|---|
| BLOCKED ON STDIN | hung open, finished at EOF → missing path argument (`rg PATTERN` with no path) |
| HANGS REGARDLESS | a watcher that never exits by design (`bacon --headless`) |
| DOES NOT HANG | completed under both |

## Two bugs my own tools had, caught by testing against known answers ⭐

Both found by running the servers against traps whose answers were already documented — the exact
method `ground-truth` preaches.

1. **`hang_check` reported "does not hang" for the known `rg` block.** `subprocess.run`,
   `communicate()` and inherited stdin all give the child **EOF**, and a tool that blocks on stdin
   does not block at EOF. The probe was measuring an approximation of the condition. Fixed by
   `Popen(stdin=PIPE)` with output to temp files and `wait()` — **never touching the pipe**.
   Verified against ground truth: open pipe → 124, EOF → 0, explicit path → 0.
2. **`shape_check` said "EMPTY output with exit 0"** when the exit was 1 — turning a plain failure
   into a spurious "silent no-op" diagnosis. Now branches on the actual exit code.

> The lesson generalises: **a verification tool must reproduce the failure condition, not an
> approximation of it.** A probe that is easier to write than the real thing usually is not the
> real thing.

## Registration

```bash
claude mcp add-json --scope user cockpit \
  '{"type":"stdio","command":"/var/home/Louranicas/.local/bin/workspace-mcp","timeout":600000}'
claude mcp add --scope user ground-truth -- ~/.local/bin/ground-truth-mcp
claude mcp list · claude mcp get <name> · claude mcp remove <name> -s user
```

Note the `--` separator is required for the stdio form of `claude mcp add`; `add-json` takes the
config object instead and is the way to set `timeout` or `alwaysLoad`.

Both are captured by `habitat-settings-backup` and restored by `habitat-settings-restore`.

> `claude mcp list` performs a health check that opens each stdio server; a server waiting on
> stdin can make it appear to hang. Inspect `~/.claude.json` directly if it stalls.

Related: [[Authored Skills]] · [[00 - Habitat Toolkit]] · [[00 - Field Findings]] ·
[[00 - Workflows]] · [[00 - Toolshed Index]] · [[Clustering Shapes]] · [[Runbooks]]
