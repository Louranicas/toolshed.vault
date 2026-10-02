---
tags: [toolshed, findings, corrections, field-notes]
created: 2026-09-02
method: every finding below was produced by running the thing, not by reading about it
---

# 🔬 Field Findings — 166 corrections from actually running the toolchain

> *Count re-measured 2026-09-23 night: 166 distinct ids, F1–F165 plus F125b, no gaps and no
> duplicates (it read 161 while F161 and F162 already existed). The heading read **114** until then — a claim with no validity interval
> cannot go stale, only silently wrong. Re-measure before editing it.*

Documentation says what a tool *should* do. This note records what the installed builds
**actually did** when driven hard in [[Arena Practice Ground|the arena]]. Several of these
contradict upstream docs, this vault's own earlier notes, or both — where they disagree,
**the binary wins** and the note here is authoritative.

Ordered by how expensive the mistake was to find.

---

## Class 1 · Silent wrong answers (worst — no error, wrong result)

### F1 · `nu -c` does not read stdin
Piping into `nu -c '…'` yields **nothing**; `from json` fails with *"nothing doesn't support
cell paths"*. There is no warning that input was dropped.

```bash
herdr pane list | nu -c 'from json | get result.panes'            # ❌ silently empty
herdr pane list | nu --stdin -c '$in | from json | get result.panes'   # ✅
```
**Both `--stdin` and a leading `$in` are required.** This vault's [[nushell]] note originally
documented the broken form — corrected.

### F2 · nushell auto-types CSV columns
`open x.csv | where exit == "1"` returns an empty list when the column is an int. No type error.
```bash
open data/readings.csv | first 1 | describe
# table<id: int, ts: string, tool: string, cluster: string, duration_ms: int, exit: int, …>
```
**`describe` is the diagnostic.** Always run it before filtering an `open`ed file.

### F5 · atuin's default search over-matches by ~6×
Same query `nu`, same database:

| mode | hits |
|---|---|
| fuzzy (**default**) | **19** |
| fulltext | 3 |
| prefix | 1 |

Fuzzy matched commands that do not contain the term in any meaningful sense. **Scripts must
pass `--search-mode fulltext`**; the default is tuned for a human eye scanning a picker.

### F8 · hunk names the same id differently per subcommand
`session comment list` → **`commentId`** · `session review --include-notes` → **`noteId`**.
Using `.id` (the obvious guess) matches nothing, so a retraction loop reports success while
deleting zero comments.

### F9 · `hunk session review --json` returns **null** notes without `--include-notes`
`reviewNoteCount` is populated *either way*, so a count-only sanity check passes while the
array is null. Two traps stacked.

### F12 · `rg -r '$1'` does not apply to `--json` submatch text
`.data.submatches[0].match.text` is the **whole match**, replacement ignored — so
`rg --json 'pub fn (\w+)' -r '$1'` yields `pub fn median`, not `median`. Strip in jq instead.
(`-r` works normally with `-o` and no `--json`.)

### F13 · `rg -- .` prefixes every path with `./`
Downstream tools that expect repo-relative paths reject them **silently** — hunk accepted the
command and created nothing. `sub("^\\./";"")`.

### F20 · A one-liner nvim jump silently loses the line
`--remote-send ':edit file<CR>:33<CR>'` lands on the *previous* cursor position: LazyVim
restores it in a `BufReadPost` autocmd that fires after the whole send is processed.
Split it — `:edit`, brief pause, then `cursor(33,1)` as a separate `--remote-expr`.

### F23 · The herdr event envelope is not what the schema implies
Events arrive as:
```json
{"event": "pane_updated", "data": {"pane": {...}, "type": "..."}}
```
The name is **top level and snake_case**, while *subscriptions* use dotted names
(`pane.updated`). Reading `result.type` — the natural guess from the request schema — matches
nothing, forever, with no error. Cost three debugging rounds.

---

## Class 2 · Hangs and crashes

### F11 · `rg` with no path argument blocks on stdin
In a script (no tty) it waits forever. Cost a 2-minute timeout before diagnosis.
```bash
timeout 5 rg --json 'pattern'      # exit 124 — blocked on stdin
timeout 5 rg --json 'pattern' .    # exit 0
```
**Always pass an explicit path**: `rg PATTERN -- .`

### F3 · `atuin scripts new --script` takes a FILE PATH, not inline text
`--script 'echo hi'` → `Error: No such file or directory (os error 2)` plus a panic at
`scripts.rs:264:34`. The help text is bare (`--script <SCRIPT>`, no description), and the
failure looks like a bug in atuin rather than a usage error. Write the body to a file first.

### F4 · atuin renders script bodies through minijinja — **including shell comments**
Any `{{ … }}` collides, so **Go-template CLIs cannot be embedded**:
```bash
podman ps --format '{{.Names}}'     # → syntax error: unexpected `.` (in script:26)
```
Moving it into a `#` comment does **not** help — minijinja renders comments too. Use
`--format json | jq`, or `{% raw %}`.

### F25 · `setsid nohup … &` does not survive this harness
Backgrounded helpers die with the wrapper. Long-running processes belong in a **systemd user
service** — which is the Kinoite-correct answer anyway ($HOME, restart policy, journal).

---

## Class 3 · Wrong mental model

### F17 · `pane.exited` does not fire when a TUI dies
It is about the **pane**, not its foreground process. A dying TUI leaves the pane alive at a
bash prompt, so nothing is emitted.

### F22 · `pane.output_matched` fires only on newly-**written** output
It genuinely works — verified by writing a sentinel into a pane and catching the event with its
`matched_line`. But an **alt-screen TUI exiting restores the primary screen without writing
anything**, so a dying service produces no match.

> **Together F17 + F22 mean the herdr event bus has _no_ service-death signal.** This is why
> [[Habitat Reactor]] uses the bus for topology and a poll for liveness.

### F10 · hunk's `source` is the channel, not the person
A comment added via CLI is `source: "agent"` **even with `--author Louranicas`**. Filter on
`author` for attribution, `source` for provenance.

### F19 · nvim already serves an RPC socket — and it belongs to the *child* pid
No `--listen` needed: `/run/user/1000/nvim.<pid>.0` exists by default. But the socket's pid
(10362) is nvim's **child**, not the pid herdr reports as the pane's foreground process (10357).
**Glob for the socket; do not derive it from the pane.**

### F14 · The default branch was `master`, not `main`
`hunk diff main` → *"Check the revision or range and try again."* `git init` here produced
`master`. Never assume — `git symbolic-ref --short HEAD` or `git branch`.

---

## Class 4 · Ergonomic traps

### F6 · `habitat respawn` did not enforce the registry cwd
`herdr pane run` executes in the pane's **current** directory, so panes driven elsewhere
relaunched their tools there. Fixed: respawn now prefixes `cd <registry cwd> &&` unless the
launch string already cds.

### F7 · hunk hides agent notes by default
`showAgentNotes: false`. Comments land (`liveCommentCount` rises, they read back over the CLI)
but **render nothing**. Launch with `hunk diff <base> --agent-notes`. This was the open question
from the first session — the human *does* see them, boxed and attributed, but only with the flag.

### F15 · Sending `q` to an already-idle pane types a literal `q`
It corrupts the next command (`qcd /var/…` → *command not found*). Check
`herdr pane process-info --pane <id>` **and act on the result** before sending TUI keys.

### F16 · `just` takes the doc comment immediately above a recipe
Including a decorative `# ─── section ───` separator, which then appears as the recipe's
description in `--list`. Leave a blank line between separator and recipe.

### F21 · `--remote-send zz` leaves an artefact in the LazyVim statusline
It is a display widget, not pending input — `mode()` returns `n`, `reg_recording()` is empty.
Send view commands as `--remote-expr 'execute("normal! zz")'` for a clean state.

### F24 · `pane.updated` is extremely chatty
Agent status churn floods it. Subscribe to specific topology events instead.

### F18 · Prompt-regex matching needs `\]\$\s*$`, not `\$ $`
The idle prompt renders as `⬢ [Louranicas@toolbx <dir>]$` with the **trailing space stripped**
by `strip_ansi`. (Moot given F22, but correct if output-matching is used for anything else.)

---

---

## Class 6 · Found by building the cascade engine and triggers

### F27 · A poll that only runs in the recv-timeout branch **starves**
`habitat-reactor` swept for dead services only when `socket.recv` timed out. Topology churn kept
resetting that timeout, so liveness was never checked and a dead service sat unnoticed. Track the
deadline explicitly:
```python
if time.time() - last_sweep >= POLL_SECONDS:
    sweep(); last_sweep = time.time()
```
Fixed and immediately proven: `poll: hunk down in w1:pK -- respawning` → 12 running, 0 stopped.
**Any "do X on idle" loop over a busy channel has this bug.**

### F28 · `pane.output_matched` is a *check now*, not a *watch*
It evaluates the pane snapshot **at subscribe time**, fires at most once, and is then consumed.
Arming on an already-broken pane fired instantly; arming on a clean pane and then breaking the
build produced **nothing**. A long-lived watcher must re-subscribe after every event — and even
then it cannot see **alt-screen** rendering, so no resident TUI can be a trigger source. Watch
*state* (run the command yourself) rather than screens.

### F29 · A top-level TOML key after `[[array]]` belongs to that table
`verdict = "..."` at the end of a spec silently became a field of the last `[[stage]]`.
`"verdict" in spec` was False and no verdict ever rendered — no error anywhere. **Document-root
keys must appear before the first array-of-tables.** (Related: TOML also forbids
`id = "x"; ws = "W1"` on one line.)

### F30 · Greedy `.*` swallows all but the last digit
`sed -E 's/.*([0-9]+) running.*/\1/'` on `"12 running"` yields **2**. The habitat doctor
confidently reported 2 of 12 services running. Use `grep -oE '[0-9]+ running'` per field rather
than one sed with backreferences.

### F31 · television custom channels are scriptable, not just interactive
`tv habitat-services --take-1 --input bacon` → `bacon  w1:pJ  Workspace 2`. A channel is a TOML
file declaring a `source` command and a `preview` command, so **any** line-emitting command
becomes both a human picker and an agent-usable selector. Four habitat channels now exist:
`habitat-services`, `herdr-panes`, `vault-notes`, `atuin-scripts`.

### F32 · mempalace room keywords must match subdirectory names for a project mined at its root
(Extends [[00 - Field Findings#F26 · mempalace room keywords match the path relative to the mined dir|F26]].)
Adding `receipts` and `cascades` to the arena room's keywords moved 20 misfiled drawers out of
`general`. Re-mining after `touch` re-files without a purge.

### F33 · SELinux `:Z` cannot be used on a read-only bind mount
`-v src:/src:ro,Z` starts the container successfully and then denies every path inside it.
The private label **relabels** the mount, which requires write access. Use the lowercase
shared label `:ro,z`. The failure presents as a container bug rather than a mount-option
mistake, which is what makes it expensive.

### F34 · A minimal sandbox image is a different userland, not a smaller one
Alpine's BusyBox `grep` has **no `--include`**. Analysis tasks written against GNU grep
returned confident **zeros** — `test_fns: 0` on a crate with five tests — with exit status 0.
Portable form: `FILES=$(find . -name '*.rs')` then `cat $FILES | grep -cE …`. Assume nothing
about `grep`, `sed`, `awk`, `find` or `printf` flags inside a small image.

### F35 · `str()` on captured JSON emits Python repr, not JSON
A template renderer that interpolated a stage's captured value with `str()` produced
`{'author': 'x'}` — single quotes, `True`, `None` — which breaks every downstream
`jq --argjson`. It survived months of use because **`[]` and `{}` are identical in both
notations**, and every earlier structured hand-off happened to be empty. The first populated
array broke it. Re-encode with `json.dumps` for dict/list/bool/None.

**A serialisation bug hides wherever the empty case is the common case.** Test structured
hand-offs with data in them, not just with the shape.

### F36 · A median over all history hides a recent change
After optimising a stage from 550 ms to 35 ms, its all-time median barely moved — the older runs
dominated — while only its *range* quietly widened to `34–600`. **A profiler that cannot see an
improvement cannot verify one.** Compare the most recent slice of each stage's runs against the
rest and flag movement beyond a threshold.

### F37 · The slowest stage in a parallel wave slows its siblings
Removing one 550 ms stage improved **seven other stages by 28–46%** — stages that ran concurrently
with it and never waited on it. Its CPU/IO burst was contending with them. The cost of a slow
stage is not only its own wall time; in a parallel wave it taxes everything beside it, so
**optimising the critical path of a wave pays twice**.

### F38 · Truncating an identifier from the front collapses distinct items
Dynamic child ids were built by truncating each value to 18 chars. File paths share prefixes, so
three different files produced the *same* id, collided in a dict, and **only one child ran** — with
no error and a successful-looking run. Build labels from the **tail**, and disambiguate collisions
explicitly rather than assuming uniqueness.

### F39 · `hash()` on strings is salted per process
`abs(hash(x)) % n` is not reproducible across runs: `PYTHONHASHSEED` is random per process. Used
for work placement it put every child on one worker in one run and spread them across three in the
next, from identical input. Use `hashlib.md5`/`sha1` for anything that must be stable. (A stable
digest is deterministic and statistically balanced — not perfectly balanced.)

### F40 · `ls` showing a file is not evidence that it resolves
`~/.local/bin/herdr-reviewr` listed fine but was a **broken symlink** to a temporary install
directory (`.tmp-install-…/checkout/bin/`) removed after the plugin installed. `ls` lists the
link; `os.path.exists()` / `test -e` follow it. The documented standalone command had never
worked, silently, for a day. **For symlinks, `test -e` is the check** — and a knowledge audit that
resolves paths will find these when a human reading the same note will not.

### F41 · An auditor that cries wolf gets ignored
The first knowledge-audit run reported 8 "orphan" notes — all of them the verbatim `--help`
appendix, deliberately unlinked. Real orphans would have been invisible in that noise. Excluding a
known-intentional class is not weakening a check; it is what makes the remaining output worth
reading. **But record the exclusion** — an unexplained filter is how a check quietly stops
checking.

### F42 · A search pattern beginning with `--` is parsed as an option
`rg -l --fixed-strings "--list" -- <dir>` fails with *"unrecognized flag --list"*: the pattern
itself looks like an option. Use `-e <pattern>`. Passed positionally, a source-corroboration
checker reported **91 of 92** documented flags as unconfirmed — a broken tool loudly indicting
correct documentation.

### F43 · Rust/clap derive CLIs never contain the literal `--flag`
They declare `pub shebang: String` under `#[arg(long)]` and the macro generates the flag. Grepping
the literal finds nothing. Resolve the identifier too (`--export-locations` → `export_locations`)
— and match it on **word boundaries**, or `after` matches `empty_line_after_outer_attr`.

### F44 · Attribute a documented flag per LINE, not per note
Chain documentation means a note about X legitimately shows flags of Y and Z. Blaming `fzf.md` for
`just --choose` is a checker bug, not a documentation error. Take each command segment's head
binary and only attribute flags to *that* tool.

### F45 · Cloned source can be AHEAD of the installed binary
`repos/atuin` is at **18.21.0**; the installed Fedora RPM is **18.12.1** — nine minor versions
behind. The clone independently corroborated the upstream/installed gap first found on the web
(`atuin mcp` exists in source, not in the installed build). **Check the clone's version before
treating it as ground truth for the thing you are running** — it is ground truth for *some*
version.

## Class 5 · Corrections to earlier claims in these vaults

| Claim | Reality |
|---|---|
| `bacon --headless` is a "one-shot verdict" | It *watches forever* — help says "run the default job **on change**". It hangs the caller. Use `cargo check`, or read the resident pane. |
| MemPalace "mines both fedora vaults" | It mined **one** until 2026-09-02 — the kinoite vault sat above the palace root. |
| `toolbox-bootstrap` "needs updating to cover this loadout" | Stale — it already covered it. (It *did* need `uv` and `socat`, now added.) |
| `atuin scripts new --script 'inline text'` (this vault) | `--script` is a file path — see F3. |
| `nu -c 'from json \| …'` as the agent door (this vault) | Needs `--stdin` and `$in` — see F1. |

### F26 · mempalace room keywords match the path **relative to the mined dir**
Mining `fedora-obsidian-vaults/` yields paths like `toolshed.vault/50 Field Notes/…`, so a
`toolshed` keyword matches. Mining `fedora-arena/` **itself** yields `notes/findings.md` — which
contains no "arena" — so an `arena` keyword matches nothing and everything falls into `general`.

Two consequences:
- A room for a project mined at its own root must name its **subdirectories** (`notes`, `scripts`,
  `crates`, `data`), not the project.
- The parent vault's `mempalace.yaml` must list a room per sub-vault, or `mine .` files that
  sub-vault into `general` even though the sub-vault has its own correct config.

**Re-mining after `touch` re-files into the corrected room** — no purge needed. This is how the
95 misfiled drawers here were repaired.

### F46 · A child `cargo` inherits `CARGO_TARGET_DIR` — and can overwrite the crates under test

Spawning `cargo build` from a test, in a generated workspace whose crate names collide with the
outer workspace's, writes the child's artefacts into the **parent's** target directory. The
scaffold's stub `libforge_contracts.rlib` replaced the real one; the symptom appeared much later
and somewhere else entirely, as a doctest failing to resolve `forge_contracts::json`.

```rust
// Wrong: the child inherits CARGO_TARGET_DIR from this process.
Command::new("cargo").args(["build"]).current_dir(generated_root).output()

// Right: pin it inside the generated tree.
Command::new("cargo").args(["build"]).current_dir(generated_root)
    .env("CARGO_TARGET_DIR", generated_root.join("target")).output()
```

**Why it stayed hidden:** on a *warm* target directory the real rlibs were already present and
newer, so the host build passed every time. Only a **cold** target dir exposes it — which is
what five fresh podman sandboxes are. The isolated run was not a formality; it was the only
thing that failed. See [[Forge - Deployment Framework]].

### F47 · `BufRead::split` allocates the whole line *before* your length check

A length cap applied to an already-materialised buffer bounds nothing:

```rust
for line in reader.split(b'\n') {      // grows without limit
    let line = line?;
    if line.len() > MAX_LINE { ... }    // runs after the allocation it should prevent
```

`read_until` and `split` grow the `Vec` until they find the delimiter. A client sending
gigabytes with no newline is an unbounded allocation in the server process. The cap becomes real
only by reading through `take`:

```rust
let n = (&mut reader).take(MAX_LINE as u64 + 1).read_until(b'\n', &mut line)?;
let complete = line.last() == Some(&b'\n');
if !complete && line.len() > MAX_LINE { /* refuse; the tail is unframable */ }
```

The `+ 1` sentinel byte is what distinguishes "line that ends exactly at the limit" from "line
that runs past it". **Test the bound by measuring what the reader consumed**, not by asserting on
the error message — an assertion on the response passes against the broken version too.

### F48 · The same shape hides wherever a limit lives downstream of a read

`forge-spec` enforced `MAX_BLUEPRINT`, so the blueprint size looked handled — but the caller did
`fs::read_to_string(path)` first, and only then handed the string to the parser. A named pipe or
`/dev/zero` at that path is an unbounded read before the limit is ever consulted.

**The generalisation, worth a sweep of any codebase:** a limit is only a limit if it is applied
at the point of acquisition. After F47, searching for the same pattern found F48 immediately —
`read_to_string`, `read_to_end`, `split`, `lines`, `collect()` on anything caller-controlled.

### F49 · `grep -c '\.unwrap\(\)'` over-counts by 5% — BRE `\(\)` is an EMPTY GROUP

```
/usr/bin/grep -c  '\.unwrap\(\)'   64      <- BRE: matches `.unwrap` + an empty group
/usr/bin/grep -cE '\.unwrap\(\)'   61      <- ERE: literal parens
/usr/bin/grep -cF '.unwrap()'        61
rg -c / python re.findall             61
```

In **basic** regex `\(` and `\)` are *grouping* metacharacters, so `\.unwrap\(\)` means
"`.unwrap` followed by an empty group" — which also matches `.unwrap_err()`, `.unwrap_or()`. Exit
status 0, confident number, wrong by three. Use `-E`, or `-F` for a fixed string.

**And `grep` is not one program here.** In the agent's shell it resolves to a *function* wrapping
**ugrep 7.8.4**, which *rejects* the empty subexpression outright (`error at position 15`) and
yields 0. Under `bash -lc` it is `/usr/bin/grep`. **The same command gives 0, 61 or 64 depending
on which shell runs it.** Any script that greps and is invoked both ways is unreliable by
construction.

### F50 · `fd`'s pattern is a REGEX, not a glob

`fd -t f '*.rs'` matches nothing — `*.rs` is an invalid regex (leading quantifier), and fd reports
the pattern rather than failing loudly. Use `fd -e rs` (extension) or `fd -g '*.rs'` (glob mode).
`find -name '*.rs'` and `fd -e rs` both give 10; the naive `fd` call gives 0.

### F51 · `nu open` infers format from the extension — it answers a different question

`open x.toml | columns | length` succeeds on a **TOML** file where `jq` and `python -m json` both
correctly fail. Convenient interactively, dangerous in a probe: nu will happily answer *a*
question about a file that is not the one you asked. When comparing tools, pin the parser
(`open --raw` + `from json`).

**All three found the same way:** [[Shape-Directed Tool Chaining|habitat-poly]] asked one question
of several tools at once. A single-tool answer looked authoritative in every case.

### F52 · Service name is not process name — `pgrep -x <service>` lies for four of sixteen

```
television -> tv      lazyvim -> nvim      bottom -> btm      nushell -> nu
```

Any liveness check, chaos experiment or respawn guard written as `pgrep -x <service>` reports
**stopped** for those four while they are running. My own chaos harness had this bug; it happened
to be aimed at `jqp`, whose names coincide, so it passed.

The registry has always known — `~/.config/habitat/services.json` carries `proc` per service —
and nothing was reading it. `scripts/svc-proc <service>` resolves it; shell-only services carry
`proc: null` and fall back to their own name.

**Registry shape, since I guessed it wrong twice:** services live at
`workspaces[i].services[j]`, keyed by **`id`**, not `name`. Walk the tree; do not assume a flat
map. Both wrong guesses returned the input unchanged — a silent identity function that looks
exactly like a successful lookup.

After the fix, `battern × poly` over all 16 services gives **11 AGREE** (resident daemons) and
**5 DISAGREE** — precisely the shell-by-design services, where the disagreement is correct.

### F53 · `wc -l` counts NEWLINES, not lines — off by one without a trailing newline

```
printf 'alpha\nbeta\ngamma'  > noeol.txt     # 3 lines, no final newline
  wc      2        <- counts newline characters
  rg      3        python 3        awk 3
```

Add the trailing newline and all four agree at 3. So any `wc -l` over output that may lack a final
newline — `printf`, a truncated write, a partially flushed pipe, a here-string — under-counts
silently, exit 0.

**Checked this habitat's own uses** (`justfile` detect-history / detect-session / receipt,
`review-gate.sh`, `fuse-modules.sh`): all currently correct — **but only because their producers
(`python3 print`, `git`) happen to emit trailing newlines.** The guard is a property of the
*producer*, not of the counter, and nothing states or checks it. Prefer `awk 'END{print NR}'`,
`rg -c ''`, or a python count when the producer is not known to terminate its output.

Found by [[Shape-Directed Tool Chaining|habitat-poly]] on a deliberately constructed case, after
the same probe returned a clean AGREE on a well-formed file — **the null result was real and the
disagreement had to be provoked.** A probe that only ever runs on tidy inputs is a probe that only
ever agrees.

### F54 · `cp -a dir dest/` nests; `cp -aT dir dest` does not — and a backup/restore pair must agree

```
cp -a  ~/.local/share/herdr-plugins  snap/home/herdr-plugins/
   ->  snap/home/herdr-plugins/herdr-plugins/habitat-services     WRONG (nested)
cp -aT ~/.local/share/herdr-plugins  snap/home/herdr-plugins
   ->  snap/home/herdr-plugins/habitat-services                   right
```

`habitat-settings-restore` documented this trap and used `-T`. `habitat-settings-backup` did not.
**The two sides of a round trip disagreed**, so a restore would have written
`~/.local/share/herdr-plugins/herdr-plugins/…` and **silently lost the plugin that respawns the
cockpit** — discovered only in the one situation where recovery matters.

**And `-T` is not a blanket fix.** Two call forms exist:

```
copy ~/.config/nushell             config               # put it IN there   -> no -T
copy ~/.local/share/herdr-plugins  home/herdr-plugins   # that IS its path  ->    -T
```

Applying `-T` to the first **renames the source to the destination directory** and swallows the
tree: doing exactly that removed five config trees from the snapshot in one run. The condition is
whether the destination's basename equals the source's.

**Neither error is visible to `--dry-run`**, which correctly skips absent sources — and silent
skipping is precisely what an incomplete backup looks like. Found by
`scripts/audit/backup_integrity.py`, which compares each `back src dst` pair against live:
`entries=26 ok=26 STALE=0 MISSING=0`.

**A backup that has never been restored is not known to be a backup.**

### F55 - A check that returns much faster than usual has probably stopped checking

`twodoors.py` verdicts, same code, same machine, minutes apart:

```
2521 ms  ->  verdict=FAIL   (inside a 10-stage parallel wave)
92468 ms ->  verdict=PASS   (run alone)
```

37x faster and the opposite answer. Under contention the MCP door timed out and rendered emptiness
as `"(no output)"` while the shell door returned `""` - the doors **disagree about how to say
nothing**, an AX-2 flaw in the rendering layer that is invisible except under load.

> [!error] **CORRECTED 2026-09-03.** The contention explanation above was WRONG, and the timing
> that seemed to prove it was the symptom, not the cause. `twodoors` called
> `subprocess.run(["habitat","q",svc], capture_output=True)` -- which redirects stdout and stderr
> **but inherits stdin**. `habitat q jqp` runs bare `jq`, which then blocked on the inherited
> stdin for the entire 90 s timeout. **That single hang WAS the "92 s run."** When stdin happened
> to be closed already (inside the cascade) jq returned instantly and the run took 2.5 s. So the
> fast runs were not degraded by load; the *slow* ones were a hang I had mistaken for thorough
> work. Isolating the stage into its own wave "fixed" nothing and was reverted.
>
> Fix: `stdin=subprocess.DEVNULL` on both doors, plus a declared `probe_arg` so `jqp` is exercised
> with real input. Now **3.2 s, 14/14 agree, three consecutive runs**. Same family as *`rg` with
> no path hangs*: **a probe must never inherit stdin.**
>
> The general lesson is the one from `pkill -f`: I had a description of the symptom that predicted
> the observations and named the wrong mechanism -- and the wrong mechanism produced a wrong fix.

**Duration belongs in the verdict.** A stage that normally takes 90 s and returns in 2 s did not
get faster; it stopped doing the work. Record expected wall time next to expected output.

### F56 - A cascade stage's tick came from `grep`, not from the check

```toml
run = "python3 audit.py | grep -oE 'verdict=[A-Z]+' | cut -d= -f2"   # FAIL renders as a green tick
run = "v=$(... ); echo \"$v\"; [ \"$v\" = PASS ]"                      # verdict reaches exit code
```

`grep` exits 0 whenever it matched, so `verdict=FAIL` was captured, displayed, and marked OK. The
"never take a verdict from a pipe" rule was violated **inside the cascade written to enforce it**.
See [[Axiom Conformance]], AX-1.

### F57 - `capture_output=True` does NOT redirect stdin, and the child inherits yours

```python
subprocess.run(cmd, capture_output=True)                       # stdin INHERITED -> can block
subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True)   # correct for a probe
```

`capture_output` sets stdout and stderr only. Any child that reads stdin when given no input --
`jq`, `rg` with no path, `cat` -- blocks until the timeout. In `twodoors.py` that produced a 90 s
hang I read as *thorough work* and a 2.5 s no-hang I read as *degraded by contention*, which is how
the wrong mechanism reached [[00 - Field Findings|F55]]. Same class as the `rg` finding.

**A probe must never inherit stdin.** Fixed in `twodoors.py` and in the cockpit MCP's `sh()`.

### F58 - Declare the one valid invocation per door; do not let each checker invent one

`habitat-conform` and `twodoors.py` both need "call this service in a way that should succeed".
Calling with no arguments is not neutral: for `mempalace search` it is a usage error, for `jq` it
is a hang. Both checkers were comparing a *failure* against a *failure* and reporting the pair as
indistinguishable.

The registry now carries `probe_arg` per service and both read it:

```json
{"id": "mempalace", "query": "mempalace search", "probe_arg": "axioms"}
{"id": "jqp",       "query": "jq",               "probe_arg": "-n 1+1"}
```

Two checkers keeping one rule is a promise; one declaration is a mechanism. Same shape as the
`READS = (...)` convention that lets a log reader state what it reads, for paths a scanner cannot
resolve -- **declare, do not infer**: a heuristic that guesses readers invents ones that are not
there; a declaration cannot.

### F59 - An unmeasured check is not a passed check

Fixing the AX-2 stimulus made nine doors report `n/a` and `habitat-conform` went **green on nothing
measured** -- `violations=0` where the real state was *not asked*. That is the loosening the checker
exists to catch, produced by the fix to it.

The verdict now separates the three states and counts them:

```
verdict=PASS services=16 violations=0 unmeasured=0 measured=59/64
```

`UNMEASURED` turns the gate red exactly as a violation does; `n/a` is reserved for cases that are
genuinely out of scope (a pane door has no agent door to interrogate). **Any check that can report
a pass should have to say how much it looked at.**

### F60 - The detectors were detecting their own negative controls

`just detect` reported four high/critical findings, all of them inside `scripts/detectors/d_*.py`:
the detector for `pkill -f` self-match matched the `pkill -f` string in its own inline control, and
so on. A detector file contains the pattern it looks for **by construction** -- the contract
*requires* an inline negative control -- so scanning the detectors yields guaranteed self-matches
and zero signal, and a permanently-red gate is one nobody runs.

Excluded, with the exclusion **printed** rather than assumed:

```
verdict=PASS files_scanned=63 findings=0 detectors=6 excluded_by_construction=6
```

The trade-off is real and stated: a genuine defect in detector code is no longer caught by the
scan. It is still caught by `--verify`, which requires every detector to trip its own control
before any clean result is reported. **A silent exclusion would have been the exact defect this
suite exists to find** -- so the count is in the verdict line, next to the denominator.

### F61 · A cascade receipt reported the run's wave structure from a PLACEHOLDER

`habitat-cascade` computes waves twice: a static Kahn layering up front, and the iterative
scheduler that actually runs. When runtime fan-out (`foreach`/`matrix`) forced the scheduler to
become iterative, the static value was replaced by:

```python
layers = [[k] for k in results]      # keep the receipt/doc shape below working
```

One singleton wave per stage. `graph` still printed the truth ("11 stages in 1 waves") and the
runner still printed `wave 1: 11 in parallel`, but the **receipt** — the durable, palace-mined
artifact — said `across 11 waves` / `wave 1: 1 · wave 2: 1 · …` for the *same run*.

Dated from the receipts themselves: last correct `full-sweep-20260902-210309` (3 waves/14
stages), first wrong `doctor-20260902-220912` (10/10). Every receipt in between claimed fully
serial execution while saving ~28 s per run to parallelism.

**The tell is arithmetic:** total 13375 ms with a max stage of 13373 ms cannot be 11 serial
waves. A structural claim that contradicts the timing beside it is checkable without a debugger.

**Fix:** record the wave that actually ran (`executed.append(list(ready))`) and render that.
Also correct for `foreach` children, which the static layering never saw.

### F62 · The F52 fix never reached the chaos harness — `pgrep -x <service>` still lied

`svc-proc`, `habitat-poly` and `battern` were all corrected to resolve service → process. `just
chaos` was not:

```
just chaos television   ->  verdict=SKIP reason=television_not_running    # tv IS running
```

So the habitat's **only** verification that self-healing works silently skipped 4 of 16 services
(television→tv, lazyvim→nvim, bottom→btm, nushell→nu), and a SKIP reads as fine — AX-2 in the one
check that proves recovery. After routing through `svc-proc`: `verdict=PASS recovery=4.1s`.

**A fix lands where you applied it, not where the class lives.** When a finding names a class,
grep the whole habitat for the shape before closing it.

### F63 · A structural postcondition keyed on file EXTENSION cannot see this habitat's own tools

`scripts/edit.py` parses `.py`/`.toml`/`.json` after every edit and reverts if the file no longer
parses. Every locally-built tool — `habitat`, `habitat-cascade`, `habitat-reactor`, `mcpc` … —
is an **extensionless** executable in `~/.local/bin`, so all of them got *no* structural check:
the guard was blind precisely to the files it was written to protect.

**Fix:** fall back to the shebang, which is what the kernel reads. Negative control: an
extensionless `#!/usr/bin/env python3` file edited to `def broken(:` now trips
`structural postcondition failed, reverted` and restores byte-identical.

### F64 · A one-sided check with a two-sided summary — and `[A-Z]+` cannot cross a hyphen

Two defects in the same instrument, found together.

**The claim.** `control_chart.py` tests only the LOWER limit (F55: a check that returns far
faster than usual has stopped checking) and then printed *"stage durations: all within their own
natural limits"* — while `roundtrip last=18389` sat outside its UNPL of `12046`. The verdict was
stronger than the check that earned it. Now the upper side is reported as a **notice** (a slow
point is a signal worth a look; chasing common-cause variation is tampering), and the summary
names what was actually tested.

**The noise floor.** Reporting every exceedance flagged `651 > 650` and `179 > 178` — 1 ms, below
the resolution the limits are computed at, and an auditor that cries wolf gets ignored (F41). A
point must now clear the limit by more than **one average moving range** — the chart's own
yardstick, not an invented threshold. That leaves exactly the real signal.

**The truncation.** The cascade stage extracting the verdict used `grep -oE 'verdict=[A-Z]+'`,
which stops at the hyphen and captured `TOO` from `TOO-FAST` — a different, well-formed-looking
token, and the same family as the `cut -c1-118` that turned `PASS_WITH_GAPS` into `PASS`.
Hyphen-aware, de-duplicated, single-line: `SIGNAL/TOO-FAST`.

### F65 · The backup omitted the cascade ENGINE, and the integrity check read 26/26 PASS

`habitat-settings-backup` declared 12 of the 16 tools in `~/.local/bin`. Missing:
**`habitat-cascade`** (the parallel DAG engine every cascade runs on), `habitat-trigger`,
`habitat-sandbox`, `habitat-fleet`. The toolshed's own Habitat Toolkit table listed all of them
under *"captured by `habitat-settings-backup`"*. It was aspirational for four.

**Why nothing caught it.** `backup_integrity.py` parses `habitat-settings-restore` for
`back <src> <dst>` and reconciles **that list** against live — so it verified 26 declared entries
and reported `entries=26 ok=26 STALE=0 MISSING=0 verdict=PASS`. A tool that was never declared is
indistinguishable from one backed up and unchanged. The checker's denominator was its own prior
record, not the world — the *regenerator that reads its own output* shape, in the recovery path.

**And fixing the backup alone left the pair half-closed.** After adding the four to the backup,
the files were snapshotted and `entries` stayed at **26**, because restore still did not name
them: backed up and not restorable. Both halves must declare the same set (AX-10). After closing
both: `entries=30 ok=30 STALE=0 MISSING=0`, and the rehearsal that actually restores into a
disposable target goes `files=69` → **`files=73 same=73 differs=0`**.

**The generalisable rule:** a recovery path can only restore what something enumerated, so the
enumeration is the artifact to audit — not the diff. Ask of any backup: *what would tell me a
file is missing from the list?* If the answer is the list, nothing would.

### F66 · `hunk … --json` is capped at ONE PIPE BUFFER — 65536 bytes, exactly

```
hunk session list --json > file   ->  89034 bytes   (3/3 runs)
hunk session list --json | wc -c  ->  65536 bytes   (3/3 runs)
```

65536 is one pipe buffer. The process writes and exits without draining, so everything past the
buffer is lost — and what survives is **valid-looking truncated JSON**: `jq` reports
*"Unfinished JSON term at EOF at line 1656"*, or worse, parses if the cut lands on a boundary.

**It hides wherever the diff is small.** Every bridge here uses `hunk … --json | jq`, and every
one of them worked, because the sessions they were tested against were under 64 KiB. The first
316-file session broke them all at once — the same shape as F35, where a serialisation bug hid
wherever the empty case was the common case.

**Where it bites hardest:** `review-gate.sh` piped `session review --include-notes --json` into
jq and fell back to `{"notes":0,"agent":0,"human":0}` on parse failure. So a **reviewed** diff
large enough to truncate reported `HOLD: diff not reviewed`, and nothing in the output
distinguished truncation from absence. It fails closed, which is the safe direction, and it is
still a gate that silently stops working on exactly the large changes most worth gating.

**Fix:** never pipe hunk JSON. `hunk … --json > "$tmp" 2>/dev/null` then read `<"$tmp"`.

### F67 · A `foreach` fan-out could not be joined, and unrun stages returned rc=0

Two defects in `habitat-cascade`, found by building a cascade that fans out and then converges.

**The parent never entered `results`.** A `foreach` stage expands into children (`probe[detect]`,
`probe[fmt]`, …); the parent was popped from `pending` but never recorded, so any stage declaring
`needs = ["probe"]` could never become ready. A tree could only ever be a leaf — the **web** shape
(converge after a fan-out) was unexpressible. The parent is now recorded as an aggregate over its
children (`rc = max(child rc)`).

**And the cascade reported success anyway.** The engine returned
`0 if all(r["rc"] == 0 for r in results.values())` — stages that never ran are not in `results`,
so they could not fail it. A run with **four of seven stages never executed** exited `0`:

```
! 4 stage(s) never became ready {'probe_ok': ['probe'], 'synth': ['probe_ok'], ...}
REAL rc=0
```

That is absence and success made indistinguishable in the engine every other check is built on.
Unrun stages now fail the cascade and are named.

### F68 · `codeanchors.py` ignored its path argument; `backlinks.py` had no floor

Pointed at an **empty directory** — and at a path that does not exist — the anchor auditor
reported `verdict=PASS anchors=16 broken=0`. It hardcoded `VAULTS` and never read argv, so it
audited the live vaults whatever you asked it about: a confident pass concerning a tree it never
opened. `just receipt "clean" /nonexistent → PASS`, recurring in the doc-to-code contract.

`backlinks.py` was a different mechanism with the same shape: it *does* honour its path, but zero
notes yielded `one_way=0 broken=0 PASS` — zero findings from zero input.

Both now carry a denominator and a floor: `vaults=4 notes_scanned=185 anchors=16`, and an empty
target returns `BLOCKED`, not `PASS`. Verified by control: the anchor auditor pointed at a copy
with a deliberately broken fragment now returns `FAIL vaults=3 notes_scanned=172 broken=1` —
which it could not do before, because it was never looking at the copy.

**Consequence worth stating:** until this, no gate could audit a *restored* tree, a candidate
vault, or a copy — the restore rehearsal could not have checked anchors even in principle.

### F69 · `hunk session comment list --json` has no `source` field

Keys are `author, commentId, createdAt, filePath, hunkIndex, line, rationale, side, summary`.
[[00 - Field Findings|F10]] says to filter `source` for provenance and `author` for attribution;
in hunk 0.20 that subcommand emits **no `source` at all**, so `select(.source=="agent")` matches
nothing and every agent comment falls through to the human branch. A balance check built that way
reported `human: 8` for eight comments the agent had just written — *a two-way review that never
happened*.

`review-gate.sh` was already correct here (it keys on `author=="Louranicas"`), which is why its
"no human note yet" rung still holds. Attribute by the field that exists.

### F70 · A source scan read 914 MB because `~/.local/bin` holds the agent binaries

`roundtrip`'s discovery walks `SRC_DIRS`, which includes `~/.local/bin` — and that directory holds
`codex` (255 MB), `claude` (217 MB), `grok` (166 MB), `agent` (166 MB), `cua-driver` (48 MB).
Discovery **read every one of them as text** looking for `open(...)` calls: 914 MB across 280
files, 7.3 s per pass, and P1-D had added a second pass. That is the whole of the 11.2 s → 18.4 s
regression.

**Two hypotheses were wrong before the right one**, and both were discarded on measurements:
pruning `target/.git/__pycache__` moved it 7336 → 7180 ms; pruning `sandboxes/` (287 MB of
leftover worker binaries) moved it to 7282 ms. Neither was the bulk. Only listing the files by
size found it — *the biggest thing in a directory nobody thinks of as source*.

**Fix — skip by content, not by name:** a NUL byte in the first 8 KB is a definitive binary
marker, plus a 2 MB cap (no habitat source file is megabytes long).

```
discover        7336 ms -> 15 ms
discover_shell  7222 ms ->  8 ms     (14.6 s -> 23 ms)
```

Equivalence proven against a baseline captured *before* the change: the same 4 durable-state
files, the same readers and writers. **A faster answer to a different question is not an
optimisation** — and the first comparator I wrote for that proof was itself wrong, stringifying
Python **sets** whose repr order is unstable and reporting DIFFERS on identical data. Compare
sorted structures, never `str(set)`.

### F71 · `FP_STALE_RECEIPT` had no detector because the evidence lacked the field one needs

The weight matrix, widened to 18 faults, found exactly one class nothing caught: a **stale
receipt**. Chasing it produced a correction and then a fix.

**The first framing was wrong.** I aimed the fault at a receipt *file* asserting
`^Verdict: PASS ^Target: /nonexistent`. But `just receipt` **prints to stdout** — nothing
persists it — so that shape does not exist here, and the non-vacuity floor already stops such a
receipt being *issued*.

**The live instance is elsewhere, and it was real.** 136 **cascade** receipts sit in
`receipts/*.md`, asserting `cold=PASS`, `build=PASS`, `brokenlinks=0`. They are read back by
`control_chart.py`, `roundtrip.py`, `habitat-flow`, `catalogue.py`, and mined into the palace so
`habitat recall` can quote them. **Not one recorded which tree it described** — no commit, digest
or dirty count. So the question *"does this receipt still apply?"* had no answer, and no detector
could have been written: the antipattern register named the class, and **the evidence lacked the
field a check would need.**

**Fix, in two halves.** Receipts now carry provenance —
`- provenance: \`tree=<head> dirty=<n> spec=<digest>\`` — and `scripts/audit/receipt_freshness.py`
(`just receipt-fresh`, and a `falsify` stage) reads it back:

```
verdict=PASS receipts=140 verifiable=4/140 fresh=4 stale=0 unverifiable=136
```

The denominator is doing real work: the 136 pre-provenance receipts are **UNVERIFIABLE**, reported
and never counted as fresh. Controls trip on both axes independently
(`tree deadbeefdead != c76493c864be`, `spec ffffffffffff != e6d0a475cd0e`).

**Three mistakes while building it — the same conflation, three times, in the detector built to
prevent it:**
1. The tree axis needs `git`, and a copied tree has none, so `rev-parse HEAD` returned nothing and
   the first version called **every** receipt STALE. *Unknown on the current side.*
2. Fixing that, I returned UNVERIFIABLE *before* checking the spec digest — an axis needing no git
   — so the detector could not catch its own fault. **Verify every axis you can reach.**
3. Then a real receipt read STALE with `tree - != c76493c864be`: `knowledge-audit`'s cwd is the
   **vaults** directory, which is not a repo, so it had honestly recorded `tree=-`. *Unknown on
   the recorded side.* Provenance is now anchored to the **spec's** directory — the code that
   produced the verdict, not the data directory it ran in — so those receipts became verifiable
   rather than merely excusable.

Each fix was re-tested against **both** controls afterwards, because narrowing a check to clear a
red is the one move this habitat forbids: `tree deadbeefdead != c76493c864be` and
`spec ffffffffffff != 0a9c3054e1c9` both still trip.

Also caught in passing: `hashlib` was imported *inside a function*, so the digest silently failed
and my guard `"import hashlib" in source` matched that local import — a substring check standing
in for the real condition.

**Two probes aimed at other named classes came back CAUGHT**, one with a caveat:

| probe | result | reading |
|---|---|---|
| `unwrap_in_lib` | CAUGHT by clippy | the lint law works: `unwrap_used = deny` |
| `secret_in_source` | CAUGHT by clippy | **plausibly for the wrong reason** — an unused, undocumented `pub const` trips other lints. A hardcoded token in *used, documented* code would likely pass; GA-3's secret-absence control is a Genesis plan item, not a live gate. |

**Then the detector found the operational consequence of its own existence.** Editing
`falsify.toml` changed its digest, so **15 prior falsify receipts became STALE at once** —
`spec 0a9c3054e1c9 != fb50d5a2a04f`. That is correct: those receipts assert verdicts produced by a
spec that no longer exists. But it means **every spec edit invalidates that spec's whole receipt
history**, the gate goes red permanently, and a permanently red gate is one nobody runs (F41).

The answer is not to loosen the comparator — it is **retirement**. `--retire` moves stale receipts
to `receipts/retired/` (kept, never deleted): they remain readable evidence and stop being quoted
as current. That is D10/GA-5's *generation retirement* from the Genesis plan, arriving early and
for receipts rather than journal generations. Explicit only — never automatic. Verified: 15
retired → `PASS`, and a freshly planted stale receipt still trips it → `FAIL`.

**And retirement had a side effect I had to go looking for.** `control_chart.py` and
`habitat-introspect` both read receipts with a **top-level `os.listdir`**, so anything moved into
`receipts/retired/` leaves their timing series: retiring 15 falsify receipts took that chart from
**n=53 to n=38** without a word. Defensible on the merits — a retired receipt describes a
superseded spec, so its timings belong to a different process, which is precisely the
regime-change argument — but it happened *silently*, and a cleanup that quietly re-baselines
another instrument is how a chart ends up describing a process nobody chose. `--retire` now says
so on every run. **A tool that moves evidence must name every reader it moves it away from.**

**The generalisable point:** a blind spot is only discoverable by a corpus containing the fault,
and only *fixable* if the evidence carries enough identity to check. Every gate was green against
15 faults and still green against 18 — the coverage did not change, the question did.

### F72 · A credential in ordinary-looking code passed every gate — now it does not

The weight matrix scored `secret_in_source` as CAUGHT, and the caveat I attached to it turned out
to be the finding. That payload was an unused, undocumented `pub const`, so **clippy objected to
its shape, not to the secret**. Put the same token in code that is used, documented, tested and
rustfmt-clean:

```
fmt rc=0 · clippy rc=0 · test rc=0 · detect findings=0
```

Every gate green, with a live credential in the source. GA-3 (secrets provisioning) and HAP-04
(secrets in journal/logs/errors/argv) both name the class; both lived in the Genesis **plan**, not
in a running gate.

**`d_hardcoded_secret.py`** now closes it — the seventh detector, carrying the full contract
(severity · phase · workspace · negative control · use-pattern mirror `UP_SECRET_REF`). It matches
**provider-prefixed shapes only** (`ghp_`, `github_pat_`, `xox[abposr]-`, `sk-`, `AKIA`, `AIza`,
PEM private-key blocks), deliberately *not* a generic high-entropy rule: entropy flags digests,
UUIDs and test vectors, and an auditor that cries wolf gets ignored (F41). Narrow and certain
beats broad and noisy.

The same token, rescanned: `critical HARDCODED_SECRET crates/forge-spec/src/lib.rs:1036`.
`detect-verify` → `detectors=7 negative_controls=all_tripped`.

**The contract caught me on the way in:** I wrote `phase: "pre-commit"`, and `check_meta` refused
to load the module — `phase='pre-commit' not in ('pre-action', 'build', 'review', 'claim')`. A
detector with a malformed field cannot register at all, which is exactly what the contract is for.

**False-positive rate, measured on a corpus it had never seen:** 31 upstream repos,
**97,612 files scanned, 6 findings in 2 files** — and both are secret-*detection* source
(`atuin-client/src/secrets.rs`, `habitat-graph-core/src/guard/secrets.rs`), which carry example
tokens by construction. Effectively zero false positives on real code, which is the whole argument
for provider-prefixed patterns over an entropy rule. It also generalises the fixture problem:
**any file whose job is to hunt a pattern contains that pattern**, so `detect-mask` is not a
detector-module convention, it is a class.

**And the fault had to be made honest twice.** I first split the literal (`"ghp_" "wmMATRIX…"`) so
the corpus file would not self-match — but that file already sits inside `detect-mask` markers, so
the split was unnecessary *and* made the fault unrepresentative: the token never appeared
contiguously, so the new detector missed it while clippy and test caught the broken construction
instead. Contiguous literal, and `detect` becomes uniquely responsible for the class.

### F73 · A `.gitignore` answers a different question than "what is disposable"

Building the corpus backup, I used `rsync --filter=':- .gitignore'`, reasoning that each tree
already declares what is throwaway. Measured against the sources:

```
source .md (excl .obsidian/.trash): 175      backup .md: 155      → 20 notes silently absent
```

The 20 are `toolshed.vault/40 Reference/help/`, ignored so `mempalace mine` does not index them —
and that ignore file's own comment says they **"stay in the vault to READ"**. The arena's
`.gitignore` was worse: `sandboxes/*/` covers four **git-tracked** files (the fused modules from
the fanout demonstration), the exact artifacts my-diary #20 nearly deleted.

`.gitignore` answers *"what should git track / the palace mine"*. Neither is *"what may be lost."*
Three questions, one file, and the file is only authoritative for the first.

**Rule:** a backup declares its own exclusions per source. Prefer **declare over infer** — a
heuristic invents a policy that was never written; a declaration cannot.

### F74 · `find <symlink> -mindepth 1` descends nothing, and returns success doing it

`habitat-corpus-restore` enumerates the labels in a snapshot with
`find "$FROM" -mindepth 1 -maxdepth 1 -type d`. `$FROM` defaults to `.../current`, which is a
**symlink** to the stamped directory. `find` does not follow it without `-L`, so the enumeration
returned zero labels — with **exit 0**. Paths *through* the symlink work fine (`$FROM/MANIFEST.sha256`
opened, `cd "$FROM"` succeeded), which is what makes it convincing: everything else behaved.

Caught only by the tool's own non-vacuity floor (`verdict=BLOCKED reason=restored_nothing files=0`).
Fix: `FROM=$(readlink -f "$FROM")` — resolve the name to the thing.

**Class, not instance:** `find`, `du`, `chmod -R`, `rsync` without a trailing slash and `tar` all
treat a symlink argument differently from a directory argument, and none of them errors.

### F75 · `habitat-runbook` silently ignored an unknown key, and still printed VERIFIED

A `[[step]]` gates on `expect`; a `[verify]` block gates on `contains`. Writing `expect` in
`[verify]` is not an error — the key is simply never read, the block falls back to "exit code was
0", and the run reports:

```
✓ verify   ...   VERIFIED  expected 'rc=0'
```

The gate I thought I had written was not running. The *output even says so* (`expected 'rc=0'`,
not my string), which is the only reason it was caught — read what the instrument reports, not
what you asked it for.

Fixed structurally: the loader now rejects any key it does not read, per section, with a hint for
this exact confusion. **Building the key set is where it got interesting** — the first version was
derived from one sample runbook and rejected `ship.toml`, which uses the perfectly real
`expect_not`. Sampling all three, then checking each key against the *implementation* (does the
code read it?), gave the true set. The asymmetry between `expect` and `contains` is kept
deliberately: allowing both spellings everywhere would re-create the silent no-op the guard exists
to stop. Negative control: a runbook with `expect` in `[verify]` now exits 1 with a named reason.

### F76 · The backup and the restore declared different sets, and the integrity check read PASS

`habitat-settings-backup` declares what to copy with `copy` lines; `habitat-settings-restore`
declares what to put back with `back` lines. **They are two separate lists.**
`backup_integrity.py` enumerated only the restore's list and reconciled it against the snapshot:

```
copy lines: 50    back lines: 30    →  20 backed-up items had NO restore counterpart
verdict=PASS entries=30 ok=30 STALE=0 MISSING=0
```

Among the 20: `~/CLAUDE.md`, `kdeglobals`, the Plasma appletsrc, atuin/bottom/yazi/lazygit configs,
and all three `habitat-corpus-*` tools. A restore would have put back 30 of 50 items and reported
success, because **the checker's denominator was its own declaration** — HAP-16, live, in the very
pair [AX-10](obsidian://open?vault=my-diary.vault&file=Axioms) was earned on (F54, the `cp -a`/`cp -aT` disagreement).

Found only because a *new* declaration was added to one half and the count did not move.

**Fix, both halves:** 18 `back` lines added; the 2 genuinely-deliberate exclusions now carry an
explicit `# RESTORE-EXCLUDE:` marker (overwriting a bash script while it executes is a real
hazard); and `backup_integrity.py` now enumerates **both** scripts and reports
`copies=N unrestorable=M declared_excluded=K`, exiting non-zero on any unrestorable item.
Control: plant a backup-only `copy` line → `unrestorable=1`, rc=1.

**Class:** whenever one rule is kept by two declarations, the check must read both. One list
checking itself is a mirror, not a gate.

### F77 · `~/.mempalace/config.toml` *(historical; a phantom declaration — that it does not exist IS the finding)* does not exist — the file is `config.json`

The settings backup had declared `copy ~/.mempalace/config.toml` *(historical; never existed)* for the life of the script.
`copy()` began with `[ -e "$1" ] || return 0` — so a declared source that does not exist vanished
**without a word**, and every run reported success. MemPalace's configuration has therefore never
been backed up.

Two more declarations were phantoms the same way: `~/.memex/config.toml` *(historical; never existed)* and `~/.config/yazi`
*(historical; never existed)* — neither exists on this machine.

**Root-cause fix, not just the path:** `copy()` now prints `DECLARED-ABSENT <path> (nothing
copied)` to stderr. It still does not fail — a genuinely optional source should not break a backup
— but the gap is now legible, which is the entire difference (AX-2).

**The tell was arithmetic, not inspection:** `entries` did not change when three declarations were
added.

### F78 · A verdict line computed from different facts than the exit code

Adding the F76 cross-check, the script exited 1 on an unrestorable item while still printing:

```
verdict=PASS ... unrestorable=1        rc=1
```

The `verdict=` line was computed from `(missing or stale)` and the exit from
`(missing or stale or unrestorable)`. Everything downstream — cascades, receipts, the control
chart — parses the **printed** line, so a well-formed falsehood would have propagated while the
exit code quietly disagreed.

Caught by its own negative control, in the same run that proved the new check works.

**Rule:** the verdict string and the exit status must be derived from **one** expression. If they
are computed separately they will diverge, and the printed one is the one that travels.

### F79 · `twodoors` failed once in the wave and the receipt could not say where

One `falsify` run out of three on 2026-09-04 reported `doors=FAIL`. Standalone, immediately before
and after: `verdict=PASS agree=14 differ=0`. **1 failure in 3 in-wave runs, and no mechanism.**

Deliberately NOT diagnosed. This is the F55 shape — a small split, a plausible contention story,
and a confident mechanism published from a correlation. That entry had to be retracted. So the
finding recorded here is the *undiagnosability*, not a cause:

```
| W5 | twodoors | 5197 | 1 | `FAIL` |     ← the entire evidence
```

The stage extracted `verdict=[A-Z]+` and discarded `agree=/differ=/error=` **and** the per-service
`DIFFER`/`TIMEOUT` lines. So an intermittent failure in the differential gate — the one gate whose
whole job is catching disagreement — leaves nothing to investigate. The evidence lacked the field a
check would need (D15, F71), one layer up from where F71 found it.

**Fix:** the stage now emits `PASS/agree=14/differ=0/error=0`, and on failure appends
`/at=<service,service>`. Control against synthetic output:
`FAIL/agree=12/differ=1/error=1/at=jqp,bacon`, exit 1.

**Not fixed, and deliberately so:** the comparator was not loosened, the stage was not isolated
from the wave, and the intermittency stands open. The next occurrence will name a service; until
then there is nothing honest to say about the cause.

### F80 · Cargo's package-cache lock is GLOBAL, so parallel gates on different repos contend

F79's intermittent named `bacon` once the stage verdict carried its denominator. The mechanism was
then **demonstrated, not inferred**:

```bash
( flock ~/.cargo/.package-cache -c 'sleep 6' & ) ; sleep 0.5
cargo check --message-format short          # in a completely different repo
→     Blocking waiting for file lock on package cache
      Finished `dev` profile … in 5.53s
```

`CARGO_HOME` is unset, so **every** cargo on this machine shares `~/.cargo/.package-cache` —
across repos. In a `falsify` wave, `mutants` (arena), `weight` (disposable copies) and bacon's own
door (`cargo check` in deep-diff-forge) all contend on one lock. The loser prints an **extra
line**, which survives `twodoors`' digit-normalisation (`re.sub(r"\d+", "N", …)`), so the two
doors disagree and the differential gate goes red for a reason that has nothing to do with the
doors.

**Two wrong hypotheses died first, each on a measurement:**
1. *Target-dir lock contention* — probed by running two `cargo check`s concurrently in the same
   repo. Both finished in 0.03 s warm; no contention possible. **The probe was too weak, and its
   silence proved nothing** — a warm cache cannot exhibit a contention bug, which is the whole
   [P1](obsidian://open?vault=my-diary.vault&file=Principles%2F00%20-%20Principles) lesson arriving from a new direction.
2. *Differing elapsed times* — killed by **reading the code** rather than running anything:
   `norm` replaces every digit with `N`, so `0.03s` and `5.53s` are already identical.

**Fix:** a narrow, **named** exception in `twodoors` for `Blocking waiting for file lock` lines —
the second such exception after `EMPTY`, and stated as one. Controls prove it is narrow: a real
extra line (`Compiling …`) and a compile error both still differ.

**The structural fix is not the filter.** Per-worker `CARGO_HOME` inside a podman sandbox removes
the shared lock entirely, which is what this habitat's own cold-verification standard already
prescribes. The filter buys a quiet gate; isolation would buy a correct one.

**Class:** a "hermetic" build tool can still share global mutable state. Before running two of
anything in parallel, ask what single file they both lock.

### F81 · Both ways of naming a scope are wrong; declared participation is the third

A fifth vault (`turso.vault`, 289 notes) appeared mid-session, and the habitat's two ways of
answering *"which vaults do the gates cover?"* both failed, in opposite directions, within an hour:

| approach | failure |
|---|---|
| **hardcoded list** (`codeanchors.py` VAULTS = 4) | went stale instantly — reported `vaults=4`, blind to the fifth. HAP-16: the denominator was its own declaration |
| **enumerate everything** (`orphans`/`deadpaths`/`backlinks` over `*/`) | held a newcomer to a standard nobody had agreed to — `broken=289`, three shared gates red, `gates_measured` 10 → 7 |

**The third answer: a vault opts in** with a `.habitat-gates` marker. Always **counted**, blocks a
gate only if it **declared**. Adding a vault can neither silently redden the habitat nor silently
escape it.

**One definition, not three.** `scripts/audit/participation.py` holds the predicate; every
parent-walking gate imports it. Patching each call site would have been two doors keeping one
rule — a promise, not a mechanism — and I had already patched one before catching it.

**Controls, both directions:**
```
declined  → deadpaths count=0 files_scanned=181   weight gates=10/10 blind=0  rc=0
opted in  → deadpaths count=6 files_scanned=470   weight gates=7    blind=3   rc=1
```
470 total `.md` − 289 turso = 181. The skip is **reported** (`declined_vaults:["turso.vault"]`),
never silent.

**Class:** whenever a check covers a set that can grow, neither a literal list nor a glob is right.
The set must be able to *declare itself*, and the check must report who declined.

### F82 · A cargo workspace glob that matches NOTHING does not load at all

Building the HEE-v2 W0 foundation, `members = ["crates/*"]` on a workspace with no crates yet:

```
cargo metadata --no-deps                 rc=101
error: failed to load manifest for workspace member `.../crates/*`
```

Measured three ways — `crates/` **absent**, `crates/` **present and empty**, and `members = []`:
only the third loads (`rc=0`). An empty glob is not an empty member list; cargo treats the
unexpanded pattern as a literal path and fails to find a manifest there.

**Why it bit.** The plan's W0 exit was *"`just proof` green on an empty-but-lawful workspace"*.
There are two separate problems and the second is the interesting one:

1. The manifest will not load at all with a glob, so "lawful" forces `members = []`.
2. Even fixed, `cargo clippy --workspace` on zero members errors
   (`the workspace has no members`) — and if it *had* passed, it would have been a **pass over
   nothing**. fmt, clippy and test over zero crates are all green by scanning nothing (AX-2).

**The fix is a detector, not a reminder.** `members = []` must widen to `["crates/*"]` the moment
the first crate lands, and *"remember to widen members"* is a design problem in a discipline
costume (P2). So `proof.py` enumerates `crates/*/Cargo.toml` **on the filesystem** and fails on any
crate that is not a workspace member — the denominator is the world, never the manifest's own
declaration (HAP-16, the same shape as F65/F76 where a checker reconciled its own list). Proven in
both directions: a planted crate gives `FAIL reason=orphan_crates(1)` naming it; removing it
returns `BLOCKED crates=0`.

**And the gate now refuses instead of passing:** `verdict=BLOCKED crates=0 ... reason=no_crates`,
exit 1. A gate that can report a pass must report how much it looked at (F59); over zero crates
the honest answer is not "pass", it is "nothing to certify".

**Second finding, same session:** `cargo deny check` flags a workspace's **own unpublished
crates** as `unlicensed` (rc=4, `licenses FAILED`), because `publish = false` does not exempt them.
`[licenses.private] ignore = true` is the correct fix — the licence check governs the *supply
chain*, and a crate you wrote and never publish is not in anyone's supply chain. Controlled both
ways: with the allowlist emptied and a real third-party dep present, `licenses FAILED` still fires,
so the exemption did not neuter the check.

### F83 · `<&str>::deserialize` only works on a BORROWING deserializer

Building a zero-sized schema tag whose `Deserialize` validated a constant:

```
serde_json::from_str::<Tag<T>>(...)    ->  Ok       (borrows from the input buffer)
serde_json::from_value::<Tag<T>>(...)  ->  Err      "invalid type: string, expected a borrowed string"
```

A `serde_json::Value` **owns** its data, so nothing can borrow `&str` out of it. The tag therefore
validated correctly when parsing bytes and failed when parsing an already-parsed document — two
entry points to one rule, disagreeing.

**Fix:** a `Visitor` with `visit_str`, which covers borrowed *and* owned uniformly and still costs
no allocation where the format can borrow. **Class:** any hand-written `Deserialize` that reaches
for `&str` has this split. Test both `from_str` and `from_value`, always — the failure is
invisible from either one alone (AX-10, the untested round trip, in a new costume).

### F84 · An exemption keyed on `line:column` stops applying the moment anything shifts

`cargo mutants` reports survivors as `path:LINE:COL: description`. Keying a known-equivalent-mutant
exemption on that whole string meant adding a seven-line doc comment above the function silently
un-exempted it, and the gate went red for a reason unrelated to the code.

**Fix:** key on `(path, description)` — the parts that survive reformatting. **Class:** the same
brittleness as a code anchor matching by byte-exact fragment (F86 below), and the same fix: match
on what the claim *means*, not on where it currently sits.

### F85 · `forbid` breaks third-party derive macros for lints they manage internally

Hardening the workspace lint law, `unused_imports = "forbid"` produced:

```
error[E0453]: allow(unused_imports) incompatible with previous forbid
  --> ... #[derive(JsonSchema)]  overruled by previous forbid
```

`schemars` emits `#[allow(unused_imports)]` **inside its own expansion**, which is legitimate, and
`forbid` cannot be locally overridden — that is the whole point of `forbid`, and here it is the
problem. Same applies to any macro that tidies up after itself.

**Rule:** `forbid` only for lints *this codebase owns* (`unsafe_code`, `dead_code`); everything
else is `deny`, which is still not overridable by accident. Measured, not assumed: `dead_code =
"forbid"` compiles clean through the same derives.

### F86 · A code anchor whose fragment also appears in a COMMENT is a false pass

Normalising whitespace in the anchor checker (so realigning a TOML table would not break a semantic
claim) made the W0 anchor match this:

```
31: # `unsafe_code = "forbid"` is the W0 acceptance anchor...   <- a COMMENT
47: unsafe_code    = "forbid"                                   <- the declaration
```

It reported `ok` against line 31. The anchor would have kept passing after the lint itself was
deleted, as long as the comment survived — **a false pass introduced by a fix, inside the checker
whose entire job is to make false claims impossible.**

The anchor spec already said fragments must be unique. Nothing enforced it. Now a fragment matching
more than one line is `AMBIGUOUS` and fails, naming every line it hit. Proven by weakening the real
declaration to `"deny"` and watching the anchor go `BROKEN`.

**Class:** documentation that quotes a declaration verbatim makes any checker keyed on that text
ambiguous. Enforce uniqueness rather than trusting authors not to quote.

### F87 · `cargo deny` flags your OWN unpublished crates as `unlicensed`

```
cargo deny check licenses   ->  rc=4   error[unlicensed]: p = 0.0.0 is unlicensed
                                       advisories ok, bans ok, licenses FAILED, sources ok
```

`publish = false` does **not** exempt a workspace member from the licence check. Discovered by
running the binary against a probe crate — `deny.toml` parsed fine, so nothing else would have
caught it until W1 landed a real crate and `just proof` went red.

**Fix:** `[licenses.private] ignore = true`. This is not a suppression: the licence check governs
the *supply chain*, and a crate you wrote and never publish is not in anyone's supply chain.
Controlled both ways — with the allowlist emptied and a real third-party dependency present,
`licenses FAILED` still fires, so the exemption did not neuter the check.

### F88 · A test that asserts only the empty case AGREES with the mutant

Mutation testing over a contracts crate scored **58%** on a suite that looked thorough. The
survivors were not obscure:

| survivor | why the test agreed with it |
|---|---|
| `Labels::len -> 0` | `len()` was only ever asserted on an **empty** set |
| `Labels::is_empty -> true` | same fixture, same blind spot |
| `ModelCatalog::get -> None` | no test at all |
| `From<SemVer> for String -> Default` | `Display` was tested; the **serde** path is a different function |
| `MonitoringEvent::is_about -> true` | the staleness predicate — a hardcoded `true` makes every stale record read as current |
| `index + 1` → `index - 1` | the parse error's line number, the entire value of that error, was never read back |

Closing them took the score to **99.2%** (131/132). The single survivor is a genuine **equivalent
mutant** — a zero-sized type with one inhabitant, where `Clone` and `Default` produce the same
value by construction — recorded with its reason rather than killed by a test that would only look
like it worked.

**The rule:** a green suite is not evidence that tests are *meaningful*, and inspection cannot tell
the difference. Mutation testing is the only control for a suite fitted to its implementation
rather than to its contract. **Assert the populated case, both branches, and the rendered output —
not just the default one.**

### F89 · A representation that makes a TOTAL operation look partial is the wrong representation

Building the journal's chain link, the first cut wrapped a 64-character hex `String`:

```rust
pub struct ChainLink(TailHash);        // validated hex string
fn from_hash(h: &blake3::Hash) -> Self // ...must handle a parse failure that cannot happen
```

blake3 always produces 32 bytes, which always render as 64 lowercase hex characters, which
`TailHash` always accepts. So `from_hash` had a `Result` for a branch no execution can reach —
and because the lint law forbids `unwrap`/`expect`/`panic`, that unreachable branch had to be
*written*, producing a placeholder link and a recursive fallback that were pure noise.

**The tell:** when the lint law makes a piece of code awkward, the usual reflex is to fight the
law. Here the law was pointing at a real defect — the representation was wrong.

```rust
pub struct ChainLink([u8; 32]);        // hex only at the serde boundary
const fn from_hash(h: &blake3::Hash) -> Self { Self(*h.as_bytes()) }   // total
```

Construction becomes total, an allocation per record disappears from the append path, comparison
becomes a 32-byte memcmp instead of a string compare, and the unreachable branch is gone because
it no longer exists to be reached.

**Class:** any type that stores a *rendering* of a value rather than the value. Store the thing;
render at the boundary that needs it.

### F90 · A syscall that returns success may have done nothing — read it back

`FS_IOC_SETFLAGS` with `FS_NOCOW_FL` returns `Ok(())` on filesystems and kernels that silently
ignore the request. The journal's bootstrap record would then assert a substrate property the
filesystem does not have — and the flag is **not retrofittable**, so the mistake is permanent by
the time anyone notices fragmentation.

```rust
ioctl_setflags(dir, current | IFlags::NOCOW)?;      // returns Ok
match ioctl_getflags(dir) {                          // ...but did it TAKE?
    Ok(f) if f.contains(IFlags::NOCOW) => Applied,
    Ok(_) => Err(kernel accepted the request and did not honour it),
}
```

**Class:** the same shape as *send signal through the wire* — presence is not integration, and a
successful call is not a changed state. Any set-then-assume pair over a kernel, a daemon or a
remote service needs the read-back. Verified live on this machine: btrfs `0x9123683e` →
`nocow: Applied`, read back.

### F91 · A reader STRICTER than the schema it reads refuses data that is valid

Adding a parsed `Timestamp` type, the obvious move was to use it everywhere including the v1
compatibility structs. The v1 schema says:

```json
"occurred_at": { "type": "string", "minLength": 1, "maxLength": 64 }
```

Any string. It never promised RFC 3339. A v1 reader that demands RFC 3339 will refuse a corpus
that is **valid by the contract it claims to support** — and it is the only tool that understands
that corpus's shape, so the refusal is unrecoverable in practice.

**Rule:** a compatibility type mirrors the schema it reads, including its looseness. Tightening
happens at the **migration boundary**, where a malformed value becomes a named error and the
caller can decide. That also puts the `Result` back on the function that genuinely can fail,
instead of on every read.

**Class:** the inverse of the usual worry. Everyone checks that a reader is not too permissive;
almost nobody checks that it is not too strict.

### F92 · rustdoc cannot link into a `#[cfg(test)]` module

```
error: unresolved link to `tests::canonical_bytes_are_stable_across_serialisations`
```

Test modules are compiled out of a normal `cargo doc` run, so an intra-doc link to a test is
**broken by construction** — it can never resolve, in any build. Name the test in prose instead.

Found because `RUSTDOCFLAGS="-D rustdoc::broken_intra_doc_links"` is part of the gate. The same
gate had just caught something better: a link to a test that **did not exist**, because the module
docs promised a property nobody had asserted. The doc build is a real checker, not a formality —
*if the docs cannot tell the story, the structure is wrong* has an executable form.

### F93 · An anchor fragment can be ambiguous through REAL code, not only through comments

[F86](#f86) recorded an anchor matching a *comment* that quoted its declaration. The uniqueness
rule added to fix it then fired twice more on ordinary code:

```
AMBIG  blake3::Hasher::new()  — matches 2 lines [431, 494]   (the chain, and a test)
AMBIG  IFlags::NOCOW          — matches 2 lines [161, 170]   (the set, and the read-back)
```

Neither is a mistake in the source; both are perfectly normal repetition. The finding is that
**a generic fragment cannot say where it landed**, so the rule forces a better anchor — one that
pins the *specific claim* rather than mentioning the right library:

| was | became | why |
|---|---|---|
| `blake3::Hasher::new()` | `hasher.update(prev.as_bytes());` | mixing the predecessor in is what makes it a chain rather than a list |
| `IFlags::NOCOW` | `current \| IFlags::NOCOW` | the application, not the read-back |

**Class:** an anchor should name the operation the note claims, not the API it uses. Enforcing
uniqueness is what surfaces the difference.

### F94 · A known-answer test whose answers come from the same head as the code is not one

Hand-rolling RFC 3339 formatting for the journal (rather than pulling a date library in for one
call), I wrote a known-answer test with five dates computed by hand. It failed:

```
left:  "2026-08-29T10:40:00Z"     <- what the code produced
right: "2026-09-07T04:00:00Z"     <- what I had written down
```

**The code was right.** `python3 -c "datetime.fromtimestamp(1788000000, UTC)"` gives
`2026-08-29T10:40:00Z`. My expectation was wrong by nine days.

The dangerous version of this session is the one where the test passes: had I mis-derived the
expectation in the same direction as a bug in `civil_from_days`, both would have agreed and the
test would have certified the error. Four of the five cases *did* pass, including the 2000 leap
year — so the suite looked like it was working.

**Rule:** a known-answer test's answers must come from an **independent** source — another
implementation, a published table, a different language — never from the same reasoning that
produced the code. Otherwise it measures self-consistency, which is exactly what a bug preserves.

**And note the second-order hazard:** the natural reflex on a red test is to change the code. Here
that would have broken a correct implementation to match a wrong expectation. Check which side is
wrong *before* fixing either.

### F95 · If a decision can only be exercised by real I/O, extract it — three times in one wave

Building the journal, mutation testing and plain untestability found the same shape three times:

| decision | could only be reached by | after extraction |
|---|---|---|
| no-CoW flag outcome | mounting the right filesystem | `InodeFlags` trait + fake: all four branches |
| segment rotation | writing 64 MiB or waiting 24 h | pure `should_rotate(bytes, age)`: both boundaries |
| record timestamps | reading the host clock | `Clock` trait + fake: deterministic records |

The first was found by a surviving mutant — the read-back guard could be replaced with `true` or
`false` and every test still passed, because whether that branch ran at all depended on what the
test runner's `/tmp` was mounted on. **That is not a missing test; no number of tests against a
real directory fixes it.**

**The rule:** when a branch's reachability depends on the environment rather than on the input,
the policy and the I/O are tangled. Split them and the policy becomes provable in microseconds
while the shell stays thin enough to read.

**The tell, and it is cheap to check:** *can I make this branch run by choosing an argument?* If
the answer is "only by arranging the world", extract the decision.

### F96 · A negative control must be shown to fail **for the reason you intend**

Proving `missing_docs = "deny"` actually bites, I appended an undocumented struct to a source
file and ran clippy:

```
rc=101
error: items after a test module          <- THIS is why it failed
warning: `hee-event-store` (lib) generated 1 warning
```

The control "worked" — non-zero exit, red gate, box ticked. It failed because I had appended
*after* `#[cfg(test)] mod tests`, which is its own error. The missing-docs rule was never
exercised at all, and the one warning I could see was unattributed.

Redone with the item where a real one would live:

```
error: missing documentation for a struct      <- the reason I meant
```

**The rule:** a control that trips is not a control that discriminates. Assert on the *reason* —
grep the diagnostic for the rule's own name — not merely on a non-zero exit. Every control in
this habitat's lint law now does: `grep -q 'missing documentation'`, `grep -q 'unwrap_used'`,
`grep -q 'E0453'`.

**Why it matters more than it looks.** This is AX-3 one level deeper. AX-3 says a check never
shown to fail is not known to work; F96 says a check shown to fail *for the wrong reason* is in
exactly the same position, while looking like it has been cleared. The second is worse, because
it comes with evidence.

### F97 · A lint left at `warn` is a latent warning, and the count only ever creeps

`missing_docs = "warn"` sat in the workspace lint law with a comment scheduling it for `deny`
several phases later. It was reporting zero — because everything happened to be documented.

A lint that can only warn **fails nothing**. So the first undocumented item lands silently, the
second is unremarkable next to the first, and by the scheduled promotion date there is a backlog
that makes promoting it expensive. The schedule was self-defeating: the reason to defer was to
avoid the cost, and deferring is what creates it.

Promoted while the count was zero, which costs nothing and is the only moment it is free.
Measured after: `build/clippy/test/doc` all rc=0, **warnings=0**, from a `cargo clean`.

**Rule:** if a lint is at zero, deny it now. "We will tighten it later" prices in a backlog that
does not exist yet.

### F98 · Two scripts running "the same" check with different flags is two doors

`just gate` and `just proof` both run clippy. One passed and the other failed on the same tree:

```
gate:  cargo clippy --workspace --all-targets                    -> rc=0
proof: cargo clippy --workspace --all-targets -- -D warnings     -> rc=101
```

`non_snake_case` was not in the manifest, so it was a *warning* — invisible to one door and fatal
to the other. Both were "running clippy"; neither was wrong; the pair was incoherent.

**Two fixes, and only the second is a mechanism.** Aligning the invocations makes them agree
today. Putting the rule in the **manifest** (`nonstandard_style = "deny"`) makes them agree for
every future invocation, including ones nobody has written — and lets both drop the `-D warnings`
flag, which is the real tell: if a gate needs a flag to enforce a rule, the rule is not in the
artifact.

**Class:** this is the `F58`/`AX-10` shape again — two implementations of one rule, each correct
against its own spec, disagreeing about each other. The aggregate gate caught it *one commit
after* the rule "two doors keeping one rule is a promise" was written into the standards. Writing
a rule down does not apply it.

### F99 · My own mutation gate had an INCLUDE list, and it silently skipped a crate

`just mutants` targeted a hand-maintained list:

```python
EVIDENCE_BEARING = ["hee-contracts", "hee-event-store", "hee-rules", "hee-ladder"]
```

Two of those did not exist yet, which was handled. The one that *did* exist and was **not on the
list** — `hee-registry`, holding the admission invariant, the crate whose whole purpose is a
compile-time gate on deployment — was skipped, silently, and the gate reported `verdict=PASS`
with a score computed over the crates it happened to remember.

**This is HAP-16 in the tool built to catch that class:** a completeness check whose denominator
is its own declaration. It reconciles the list it was given and cannot see an omission, because
an omission is indistinguishable from a crate that does not exist.

**Fix: enumerate the world.** The world is `crates/*/Cargo.toml`. Everything found there is
mutated unless *explicitly excluded with a stated reason*, and the verdict carries the ratio:

```
verdict=PASS crates=3/3 targeted=hee-contracts,hee-event-store,hee-registry ...
```

A crate added tomorrow is covered by default. Forgetting to mention it now makes the gate
**stricter**, not blinder — which is the direction a default should always fail in.

**The general form, and it keeps recurring:** an include list is a promise, an exclusion list with
reasons is a mechanism. Same shape as [F65](#f65) (the backup declared 12 of 16 tools and the
integrity check read 30/30 PASS), [F76](#f76) (backup and restore declared different sets), and
[F81](#f81) (a hardcoded vault list went stale the moment a fifth vault appeared). Four instances,
one lesson: **whenever a check covers a set that can grow, the set must be enumerated, and every
absence must be argued for rather than assumed.**

### F100 · `cargo-mutants` takes a global lock on `mutants.out/lock.json`

Two runs in the same tree do not queue politely; the second blocks:

```
INFO Waiting for lock on .../mutants.out/lock.json ...: Resource temporarily unavailable (os error 11)
```

It waits indefinitely, printing nothing further, so a backgrounded second run looks like a slow
first run. Same family as [F80](#f80) (`cargo`'s package-cache lock is global to `CARGO_HOME`) and
the same question answers both: **before running two of anything in parallel, ask what single file
they both lock.**

**And the cleanup is where the real cost was.** With three processes contending, `ps` named them
by their `--package` flags — and I sorted on elapsed time instead, killing the only run covering
the crate I had just added. Recorded in my-diary as Mistake #26: the input that earns "keep this
one" is the argument list, not the age.

**Practical:** one run per tree. `rm -rf mutants.out` clears a stale lock after a kill.

### F101 · A test double that discards its argument turns a seam into a blindfold

The `no-CoW` seam was built exactly as [F95](#f95) prescribes — a trait, a fake, every branch
reachable including the one no real filesystem would produce. Eight tests, all green.

The fake:

```rust
fn set(&self, _flags: IFlags) -> Result<(), Errno> { self.set }   // scripted answer
fn get(&self) -> Result<IFlags, Errno> { self.get[call] }         // scripted answer
```

Mutation testing then showed `flags.set(current | IFlags::NOCOW)` could be changed to `&` or `^`
**without one test failing**. Of course it could: `set` threw the value away, and `get` returned a
canned sequence that had never seen it. The seam had made the branch *reachable*; nothing had made
the computed value *observable*.

The fix is a **model, not a script** — the double holds the state, `set` writes into it, `get`
reads it back:

```rust
struct FakeFlags { state: Cell<IFlags>, on_set: SetBehaviour, get_fails_at: Option<(usize, Errno)> }
enum SetBehaviour { Honour, Silent, Refuse(Errno) }   // Silent = the lying kernel, the case that matters
```

Two tests then fall out that could not previously be written at all, and each kills one mutant:
setting the flag **preserves flags already there** (kills `&`), and applying it where it is already
set **is idempotent** (kills `^`). Both are real requirements — the first stops a silent act of
vandalism on an administrator's flags, the second is the ordinary restart path.

> **The detector is a grep.** An underscore-prefixed parameter in a test double — `fn set(&self,
> _flags: …)` — is a value that nothing in the suite can assert on. Rust's own `unused_variables`
> lint points straight at it and the underscore silences it.

Same family as [F95](#f95): a seam is necessary and not sufficient. **Reachable ≠ observable.**

---

### F102 · An unbounded `while` in a test is a hang, not a failure — and mutation testing says TIMEOUT

```rust
while writer.rotation_due().is_none() {          // waits for a policy that may never fire
    writer.append(...)?;
}
```

Mutate `should_rotate` to return `None` and this does not fail — it runs until `cargo-mutants`
gives up at 120 s and reports `TIMEOUT`, which is neither `caught` nor `missed` and reads as a
tooling problem rather than as the test defect it is. The same loop in CI is a hung job.

**Bound it, and assert on the budget:**

```rust
const BUDGET: usize = 64;
let mut appended = 0;
while writer.rotation_due().is_none() {
    assert!(appended < BUDGET, "{BUDGET} records ({} bytes) did not reach a {}-byte limit",
            writer.bytes_in_segment, policy.max_bytes);
    ...
}
```

The mutant is then caught in milliseconds with a message carrying the two numbers you need.
**Every loop in a test needs a budget**, for the same reason every read of caller-controlled input
needs a limit: the terminating condition is exactly the thing under test.

---

### F103 · Integer division absorbs a wrong term — so "semantically interesting" inputs miss it

Hinnant's `civil_from_days` shifts the year to begin on **1 March**, so the leap day falls last:

```rust
let yoe = (doe - doe / 1_460 + doe / 36_524 - doe / 146_096) / 365;
```

The date table pinned against python's `datetime` covered 1970-01-01, 1969-12-31, 2000-02-29 and
2026-08-29 — leap years, a century rule, an era boundary, the epoch. Every case a human would
choose. **Both correction terms could be deleted or negated with the whole suite green.**

Why: those terms contribute at most ±3, and the result is divided by 365. The perturbation only
changes the answer when the numerator sits within a few units of a multiple of 365 — and for
January and February dates it never does. The first input that kills all three mutants is
**day 59, 1970-03-01**: the first day of the algorithm's *shifted* year.

> **Generalisation.** When an algorithm ends in integer division, the inputs that discriminate are
> the ones near the division boundary, not the ones that are semantically notable. Choosing test
> inputs by domain meaning and choosing them by arithmetic sensitivity are two different jobs, and
> a calendar tempts you to do only the first.

**How to find them without thinking:** implement the original and each mutant in ten lines of
python, scan the reachable domain, print the first differing input. That is where day 59 came
from — and see [Mistake #27](obsidian://open?vault=my-diary.vault&file=Reflections%2FMistakes%20I%20Made)
for the trap in choosing the scan range.

---

### F104 · `-> Result` in a test becomes a pedantic **error** the moment the body stops using `?`

The rung-1 answer to `unwrap` in tests is `fn t() -> Result<(), Box<dyn Error>>` and `?`. But
`clippy::unnecessary_wraps` (pedantic, denied here) fires on any such test whose body never
actually uses `?`:

```
error: this function's return value is unnecessary
```

Five new tests hit it at once. The two rules are not in conflict, they just have a boundary:
**`-> R` when the body uses `?`, a plain `fn` otherwise.** Writing `Ok(())` at the end of a test
that never fallibly does anything is ceremony, and pedantic clippy is right to say so.

Sibling: `clippy::items_after_statements` rejects a `const` declared mid-function — hoist test
constants to the test module's scope.

---

### F105 · A gate step's caption is not its check — "zero warnings" printed beside an rc test, for five commits

`just gate` had this step:

```python
("clippy", ["cargo", "clippy", "--workspace", "--all-targets", "--all-features", "--locked", "--quiet"],
 "lint law from the manifest alone, zero warnings"),
```

and judged it by `returncode` alone. The string on the right is a **caption**. Nothing computed it.

Meanwhile seven lifecycle tests did `spec.advance(...)?;` on a `#[must_use]` `Transition`, and
rustc printed `warning: unused `Transition` that must be used` on **every build** — clippy's
included. Measured cold, in a worktree at the last "green" commit, with the gate's exact argv:

```
rc=0  warning_lines=7  must_be_used=7
```

So `--quiet` does **not** hide rustc diagnostics (that was my first guess, and it was wrong — cargo's
`-q` silences cargo's own status lines only). The warnings were *in the gate's captured output*.
The exit code was 0 because `unused_must_use` was at `warn`, the caption said zero, and I quoted
the caption in five commit messages and two state notes.

**Three fixes, all structural:**

1. `gate.py` counts `warning:` lines in every compile step's output and **fails on any**, printing
   `warnings=N` — the number is the verdict, the caption is gone. (Excluding cargo's own tally
   line, ``warning: `crate` generated 7 warnings``, which would double-count.)
2. `unused_must_use = "deny"` in the manifest — the same drop is now a compile error under every
   driver, not a warning under one. §4: *if a lint is at zero, deny it now* — this one had already
   gone latent, which is the case the rule exists for.
3. A negative control (`cases=8/8`): a planted dropped value must fail **with `must be used` in
   the diagnostic**, F96-style.

And the seven sites use the value: a test helper `advanced(&mut spec, to)` asserts
`transition.to == to`, which is what a returned `Transition` is *for*.

> **The detector.** Any step whose *label* makes a claim — "zero", "clean", "none", "all" — that the
> step's *code* does not compute. `grep -n '"[^"]*\(zero\|clean\|no \)[^"]*"' scripts/gate.py`
> finds the captions; the question for each is *which line of code makes this true?* If the
> answer is "the exit code", the caption is describing a hope.

Same family as [[00 - Field Findings#F96|F96]] (a control that trips for the wrong reason) and
the arena's `FT-12` (a PASS while a sub-check failed) — and the exact shape of *verdicts carry
denominators*: a "zero" with no `N` beside it was never counted.

---

### F106 · A truly cold Rust build in a container: vendor, cut the network, and do not relabel the host

The W1 cold run mounted the toolchain and the source through `habitat-sandbox`, which labels
mounts `:ro,z` — a **relabel of the host directory** to `container_file_t`. Earlier this session
the same flag on `~/.claude/skills` needed `restorecon -RF` to undo (plain `restorecon` refused:
podman writes a "customized" label). A verification run should leave no fingerprint on the host.

What worked, and what each flag buys:

```bash
cargo vendor --locked "$S/vendor"            # host: every crate in Cargo.lock, 177 dirs, from the local cache
flatpak-spawn --host podman run --rm \
  --network none \                           # offline is the CLAIM, so it is a flag, not a hope
  --security-opt label=disable \             # no :z/:Z → no host relabel; the container is disposable anyway
  -v "$R":/src:ro -v ~/.rustup/toolchains/stable-x86_64-unknown-linux-gnu:/rust:ro \
  -v "$S/vendor":/vendor:ro -v "$S/cold-out":/out:rw \
  -w /src -e PATH=/rust/bin:/usr/bin:/bin -e CARGO_HOME=/out/cargo -e CARGO_TARGET_DIR=/out/target \
  localhost/forge-sandbox:1 bash /inner.sh
```

Inside, before any cargo call, `$CARGO_HOME/config.toml` redirects crates-io to `/vendor`:

```toml
[source.crates-io]
replace-with = "vendored"
[source.vendored]
directory = "/vendor"
```

and every build runs `--locked --offline`. Then `CARGO_HOME` is fresh (no `.package-cache` lock
shared with the host — [F80](#f80) cannot occur), the target is fresh, and the network is gone.

**Measured (W2, 2026-09-04):** `fmt_rc=0 clippy_rc=0 clippy_warnings=0 test_rc=0 tests=286
rlibs_built_from_scratch=153 sqlite_c_compiled=1`. That last number is D19's falsifier passing
for the intended reason — the base `fedora-toolbox:44` image has no compiler, `forge-sandbox:1`
adds gcc, and the SQLite amalgamation was compiled *inside the container*, not inherited.

Three things that would have looked like success and were not: (1) mounting `~/.cargo` read-only
at `CARGO_HOME` fails on the lock file, late; (2) `rust-toolchain.toml` is read by *rustup's
proxy*, which is not in the container — call `/rust/bin/cargo` directly and record
`cargo --version` in the log; (3) `bc` is not in the image — sum test counts with `awk`.

---

### F107 · A strict lint law hides behaviour-deleting mutants from the mutation control

`cargo-mutants` compiles each mutant under the crate's own lints. With `dead_code = forbid` and
`unused_imports = deny` in the manifest, a mutant that empties a function or deletes a match arm
orphans an import or a variant, **fails to compile, and is counted `unviable`** — the same bucket
as `Default::default()` on a type with no `Default`. Measured on `hee-rules` at W3: six such
mutants, all behaviour-deleting, none measured.

```
cargo mutants --package hee-rules                     92 mutants: 72 caught  0 missed  20 unviable
cargo mutants --package hee-rules --cap-lints true    92 mutants: 76 caught  0 missed  16 unviable
```

Capped, the four inherent ones compile and are **caught**. The remaining unviable are the genuine
kind. So the control had a blind spot exactly proportional to how strict the lint law was — the
stricter the tree, the more of its own mutants it refused to measure.

**Fix:** `--cap-lints true` in `scripts/mutants.py` (cargo-mutants 27.1). The lint law still
governs the real tree through `just gate`; it no longer governs what the control can see. Two of
the six were also closed structurally (single-use imports spelled at the use site), which is the
better fix where it applies.

---

### F108 · A property test can over-claim: "whatever surrounds it" was wider than the rule

`hee-collector`'s planted-token property generated `before in "[a-zA-Z0-9 =:'\"]{0,16}"` and
asserted the token never survived. It failed on `aghp_…` — a letter glued to the prefix. My first
move was to weaken the **redactor** (drop the leading-boundary check). Two existing unit tests
then went red: `desk-ant-…` is not `sk-ant-…`, and `x/ghp_…` is a path segment, not a token.

The boundary rule was the design; the property was the over-claim. Under-redaction is the worse
failure (GA-3) — but a scanner that redacts on the strength of a *suffix* redacts ordinary text,
and the two unit tests had already decided that. **On a red property, establish which side is
wrong before touching either** (Mistakes #25, again): here the generator's alphabet was the bug.
It now ends at a boundary, and the comment names the unit test that pins the other direction.

The tell: a property whose generator alphabet was chosen for *coverage* rather than for the
*rule's domain* — the same shape as F103 (inputs chosen for meaning, not for the arithmetic).

---

### F109 · A workflow that hits the session limit drops agents as `failed` — reconcile from the worktrees, not the receipts

Nineteen agents were launched for W3; twelve were refused mid-run with *"You've hit your session
limit"*. The workflow completed with exit 0 and a result array in which two crates simply had no
receipt — and one of those (`hee-fleet`) was **fully built and committed** on its branch, its
agent having died at the reporting step; the other (`hee-collector`) had six uncommitted test
files that did not compile.

Neither state was visible from the result. What was visible was `git log main..w3/<crate>`,
`git status --short`, and a clippy run in each worktree. **The receipts are the agents' claims;
the worktrees are the evidence.** The fuser reconciles from the trees first, every time, and
treats a missing receipt as "unknown", not as "not built".

Also worth knowing: the reset time is printed in the failure text (`resets 9pm`), so a refused
fan-out is a scheduling fact, not a defect; the fuser can finish the work inline (this one did)
and re-run the *review* fan-out after the reset.

---

### F110 · Rootless Quadlet teardown: stop → remove → daemon-reload still leaves a unit — `reset-failed` is the last step

The W3 fleet drill deployed a rendered `.container` as a transient rootless Quadlet, started it,
stopped it, removed the file and ran `daemon-reload`. Containers 0, volumes 0, files 0 — and
`systemctl --user list-units --all 'hee-drill*'` still printed one line:

```
● hee-drill.service   not-found   failed   failed
LoadState=not-found ActiveState=failed FragmentPath=
```

`systemctl stop` on a Quadlet whose container was killed (`sleep 20` interrupted) leaves the
service in `failed`; a failed unit **object** outlives its file and survives `daemon-reload`.
It is not on disk and not running, but it is state an operator sees, and "zero residue" that
excludes systemd's memory is a definition chosen to pass.

```bash
systemctl --user reset-failed hee-drill.service     # then list-units --all shows 0
```

So the teardown order is **stop → rm unit file → daemon-reload → reset-failed**, and the
residue count reads units from `list-units --all`, not just `list-unit-files`. Recorded in
`just fleet-drill` and in `hee-fleet`'s `TeardownPlan`, which had the first three.

---

### F111 · A Rust `target/` on the 10 TB spindle can wedge ext4's journal — and then `git status` blocks too

Symptom: `git status` in a repo on `/var/mnt/STORAGE-10TB` hung past 120 s; so did `rm -f` of
a lock file, and eventually so did reading `/proc/<pid>/cmdline` of the hung processes. Nothing
was using CPU. The diagnosis chain that worked, in order, none of it touching the disk:

```
/proc/pressure/io          → some avg10=94.89          (I/O stall, 95 % of the time)
/proc/<pid>/wchan          → __jbd2_log_wait_for_space (ext4 journal out of space)
/sys/block/sdb/inflight    → 0 32                      (32 writes in flight, always)
/sys/block/sdb/stat        → +3179 writes / 20 s       (~160 writes/s: a saturated HDD)
grep Dirty /proc/meminfo   → 830 MB                    (writeback backlog)
```

Cause: the repo's `target/` lived on the spindle and a nine-crate `cargo build` plus a
mutation run had produced hundreds of thousands of small writes; under `bfq` the journal
checkpoint could not keep up, and every metadata write on that filesystem — including a
`.git/index.lock` create — queued behind it. `dmesg` showed nothing; the disk was healthy.

Fix, structural: `CARGO_TARGET_DIR=$HOME/.cache/hee-target` (the LUKS NVMe) for every build
of a repo that lives on the spindle. The gate and `just` inherit it from the environment. The
spindle keeps the source and the git objects; it never sees a build artefact again.

**Do not** "fix" it by killing the D-state processes (they cannot be killed while in the
journal wait) or by `sync` (it queues behind the same journal). Wait, and stop adding writes.

---

### F112 · A refused agent leaves `index.lock` under `.git/worktrees/<name>/`, not under `.git/`

When a fix agent was refused mid-`git commit` by the session limit, the lock it left was
`.git/worktrees/wt-fix-hardening/index.lock` — the per-worktree index, which `git` names in
the error but which a habit of looking for `.git/index.lock` does not find. Before removing it:

```bash
for p in $(pgrep -x git); do echo "$p $(readlink /proc/$p/cwd)"; done   # any git IN that worktree?
```

The two live `git` processes turned out to be a `git fetch` from lazygit in a *different*
repository — unrelated, and themselves stuck in the journal wait of F111. Only then is the
lock stale, and only then is `rm -f` safe. Same family as F109: reconcile from the evidence
(process table, lock path), not from the assumption that "the agent is dead so its lock is stale".

---

### F113 · A hand-written wire schema beside the Rust type is a second door — and the refuter found the drift within the hour

W4's design synthesis offered a default I took: the daemon wire's envelope would be validated
"positively" against a hand-written `contracts/v2/hee-rpc.schema.json`, derived from the measured
herdr sample and the plan's method map, "not from the Rust type". One author wrote it and nine
tests around it; every test was green.

The refuting reviewer then constructed frames the Rust type emits and reads that the file
rejects, and showed the file's top-level `oneOf` misclassifying frames the reader accepts. Two
renderings of one shape — the type and the file — had already diverged in the domain, and the
tests only sampled the two measured frames. That is exactly the two-doors rule (`~/CLAUDE.md` §3)
in a costume that looked like independence.

What independence actually is here: **direction 1** (`schemars::schema_for!` of the same type,
validated in both doors with a smuggled field named in the diagnostic) plus the **measured herdr
lines verbatim** as decoder known-answers, plus the **v1 evaluation schema as a negative control**
(a herdr-idiom frame must fail it, naming `jsonrpc`/`protocol`/`method`). An independent source is
a *measurement*, never a second hand-written description. The file is deleted; the decision is
recorded as reversed (W4 decision 2′), not quietly.

The tell, for next time: "hand-written so it is independent" — a description written by the same
head that wrote the type is not independent of it; only something the world produced is.

---

### F114 · A cargo feature check that reads dependency EDGES misses a crate enabling the feature through its own `[features]` table

The W4 gate had to prove that no projection enables `hee-contracts`'s `daemon` feature (the
one that exposes the daemon-side reader). The first detector read the feature two ways — the
projection's dependency edge (`cargo metadata` → `dependencies[].features`) and a
`cargo tree -e normal,features` walk — and its control planted the feature on the edge and
through an intermediate crate. Both tripped. Green.

The refuting reviewer then wrote, in a scratch projection:

```toml
[features]
default = ["hee-contracts/daemon"]
```

Nothing on the edge. Nothing in the `-e features` walk (which lists `feature "…"` nodes only
for features named on edges). `Request::parse_line` compiled. The detector printed
`daemon_feature=absent`.

What sees it: the **per-node** resolved feature list —

```bash
cargo tree -p hee-cli -e normal --prefix none -f '{p}\t{f}'     # hee-contracts v2.1.0 <tab> daemon
```

— and, independently, compiling the projection **alone** (`cargo check -p hee-cli --offline`),
so the compiler's own refusal of the gated symbol is what the gate exercises, not an inference
from the workspace's unified resolve (which, MEASURED, shows `daemon` on the spine's node for
every member the moment the spine dev-depends on itself for its own tests).

The control now has an `own_features` case for exactly this manifest. Same family as F96 (a
control must trip for the reason intended) and F99 (enumerate the world): the world of ways to
enable a feature has three doors, and the detector had covered two.

---

### F115 · A control written before the real thing existed must be re-run the moment it lands — half-editing a real crate is incoherent by construction

*Found 2026-09-05, first fused W4 gate, `scripts/uds_only.py --control`.*

The UDS-only control had only ever run against a tree with **no** `hee-cli`: it wrote a scratch
crate where the real one was absent and, for its `feature_gate` case, wrote a probe `lib.rs`
that calls `Request::parse_line`. On the first tree where the real crate existed it kept the
real `main.rs` and overwrote only `lib.rs` — `cargo check` failed **E0432** (`no run in the
root`), red for the wrong reason, and the control aborted at `cases=1/7`.

Two rules, both mechanical:

- A control that edits a real artifact must replace it **whole** or work on a scratch sibling.
  `copy_tree` now displaces every projection with a scratch crate and prints
  `real_projections_displaced=N/2`, so the number says which world the control ran in.
- The `pending` case models the tree *before* arming; once the live tree is armed it must
  disarm its copy first — the second stop, at `cases=4/7`, was this.

Same family as F96 (a control must trip for the reason intended). The trigger: **the moment the
world the control was written against changes shape, run the control before the gate does.**

---

### F116 · A disposable copy that shares the live `CARGO_TARGET_DIR` is not disposable — cargo's metadata hash and dep-info are relative to the workspace root

*Found 2026-09-05; mechanism established with `cargo doc -v`, a fresh target dir, and the
`.d` file.*

`cargo_env` used `env.setdefault("CARGO_TARGET_DIR", copy/"target")`. With the variable
exported (mandatory here — F111) every control copy built crates **named `hee-cli`** into the
live target dir. Cargo hashes path packages by their path *relative to the workspace root* and
writes dep-info the same way (`hee_cli-680a49b3.d` reads `crates/hee-cli/src/lib.rs`, no
prefix), so a copy at the same relative layout **collides** with the real crate: same
`-C metadata`, same fingerprint dir. The live `cargo doc --workspace` was then handed a
**3290-byte** probe rmeta as the real `hee_cli` and failed E0432 — while `cargo doc -p hee-cli`
alone passed (different unit hash) and the same command in a fresh target dir passed.

Discriminating test: **run it once more in a fresh target dir.** If that passes, the tree is
innocent and the target is polluted. Remedy: `cargo clean -p <crate>` for every colliding name
(package-scoped, not a blanket), then re-run. Prevention: a control sets its own
`CARGO_TARGET_DIR` **unconditionally** (`CONTROL_TARGET`), never `setdefault`; agent worktrees at
the same relative layout carry the same hazard.

The thirteen instant `hee-cli --test uds` failures in the same gate run (never reproduced) are
*consistent* with this family — a `target/debug/hee` from another same-layout tree — but their
mechanism was **not** established; recorded as suspected, not as cause.

---

### F117 · A gate that prints a tail has thrown away the failure

*Found 2026-09-05, `scripts/gate.py`.*

The gate printed the last twelve non-empty lines of a failed step. For a test step that is the
list of failing names and cargo's `error: test failed` line — the **panic text** is above the
cut, and gone: the failure could not be diagnosed after the fact, only re-run, and it did not
reproduce. `gate.py` now writes a failed step's whole output to `$TMPDIR/hee-gate-<label>.log`
and prints `log=<path> lines=<n>` beside the tail. Extends F105 (a caption is not its check):
a failure is evidence only while its text still exists.

---

### F118 · cargo-mutants files a build that died of a full disk as `unviable` — and Fedora's `/tmp` is a tmpfs with `usrquota`

*Found 2026-09-05, the first eleven-crate `just mutants` at W4.*

`findmnt -no OPTIONS /tmp` → `rw,nosuid,nodev,seclabel,nr_inodes=1048576,inode64,usrquota`. Six
cargo-mutants jobs, each a copy of the tree with its own build directory, crossed the per-user
quota part-way through 2116 mutants: `failed to overwrite "…/crates/hee-mcp/src/mcp.rs" — Disk
quota exceeded (os error 122)`. cargo-mutants recorded each such mutant as **`Unviable`** (build
failed) and finished with a plausible line — `mutants=1513 caught=1507 missed=6 score=99.6%` —
over 588 "unviable" of which **70 were never built at all**. `df` showed 29 GB free the whole
time: a quota is not a full disk, and nothing on the console said so until the writes failed.

Same shape as F107 (the lint law hid behaviour-deleting mutants as unviable): an *unviable*
count is a claim that the compiler refused the mutant, and it must be earned. `scripts/mutants.py`
now (a) reads `mutants.out/outcomes.json` and greps every `Unviable` log for an OS-level failure
(`os error`, `failed to overwrite`, `failed to copy`), printing `found= tested= unviable=
timeouts= tool_errors=` and refusing `verdict=FAIL reason=incomplete` on any tool error or
shortfall; and (b) owns its scratch — `TMPDIR=$HOME/.cache/hee-mutants-tmp` (NVMe, no quota) and
`CARGO_TARGET_DIR` unset *inside the script*, so the invocation cannot get either wrong (F116).
Checked against the flawed run before the fix was trusted: `(found=2115 tested=2115 unviable=588
timeouts=14 tool_errors=70)` → refused.

The trigger: **an `unviable` fraction that moves between runs of the same tree.** It was 20 % at
the 700-mutant mark and 28 % at the end; the tree had not changed.

---

### F119 · `schemars` FOLLOWS `#[serde(try_from = "Wire")]` — the published schema becomes the wire type's, not the type's own

*Found 2026-09-05 building the W5 proposal types; measured against the landed `SemVer`.*

The obvious way to make a validated newtype's wire form go through its constructor is
`#[serde(try_from = "WeightsWire")]`. Under `schemars`, the derived `JsonSchema` then publishes
**`WeightsWire`'s** schema — the unvalidated struct — in place of the type's own, so the schema a
consumer validates against no longer describes the type the code refuses to build. The
conformance test still passes: both doors agree, on the wrong shape.

What works: a **hand-written `Deserialize`** that parses the wire struct and calls the real
constructor, leaving `JsonSchema` derived on the validated type. Same one-door effect, same
refusal, and the emitted schema is the type's.

The tell: a schema whose `title`/`$ref` names a type the public API never mentions. Check with
`serde_json::to_value(schema_for!(T))?["title"]` in the conformance test — a known-answer, not a
glance.

---

### F120 · `cargo metadata`'s resolve walks enabled NORMAL edges only — a build edge or an optional edge is a declared door no closure walk sees

*Found 2026-09-06, the W5 exit detector's adversarial verify pass.*

A dependency detector built on `cargo metadata`'s `resolve` graph answers "what does this crate
link". It does **not** answer "what may this crate reach":

- a `[build-dependencies]` edge is compiled into `build.rs` — shipped source the detector's own
  source scan reads — and appears in no normal closure;
- an `optional = true` edge is absent from the resolve until a feature enables it, and
  `cargo check -p <crate>` compiles fine without it;
- a `dev` edge is likewise outside the normal closure.

Both evasions were planted (`socket2` on a build edge with a `build.rs` that calls it, and the
same crate as an optional normal edge) against a detector that walked the closure and did an
isolated compile — **the gate said PASS**. The fix is to read the DECLARED edges too, from
`pkg["dependencies"]`, where each carries `kind` and `optional`, and to judge them against the
same allowlist. Same family as F65: the closure is what the resolve chose, the manifest is what
the crate declared, and only the second enumerates the world of doors.

---

### F121 · A rule stated for one edge kind and applied to all of them made two crates' tests worse

*Found 2026-09-06 when both W5 sandboxes reported the workaround, not the rule.*

The allowlist above enforces "zero NEW external crates". Written to cover every declared edge, it
also refused `dev` edges — including `proptest` and `tempfile`, which landed crates in the same
workspace already dev-depend on. Neither sandbox argued with the gate. Both worked around it:
one replaced proptest with a **fixed-seed 256-draw sweep that cannot shrink**, the other
hand-rolled a scratch directory in place of tempfile. Two crates' test quality fell so a rule
could stay green, and the receipts recorded the workaround as a deviation rather than the rule as
a defect.

Two mechanical lessons:

- **Scope a rule to the harm it names.** A dev edge is in no shipped artifact and adds no new
  external crate; the rule's own justification excluded it and its implementation did not.
- **A workaround in a receipt is a finding about the rule.** When an agent reports "I did X
  because the gate refused Y", read it as evidence about the gate first.

And the fix's own control caught a third: computing the dev half of the allowlist from *every*
member let the crate under judgment license itself (its own `dev` edge on the planted crate made
that crate "already tested with", and the planted fault went unreported, `cases=2/6`). The world
that licenses a crate must exclude that crate.

---

### F122 · A constant every test compares against is pinned by nothing — and mutation testing does not cover it

*Found 2026-09-06 by the REFUTE lens on `hee-ml`; the planted change passed the whole suite.*

The crate's headline claim is that the routing weights are frozen at the Corpus Review's
0.40/0.25/0.20/0.15. Twelve tests exercised the scorer, several of them comparing a computed
total against the weighted sum — **all of them through `FROZEN` itself**. The lens replaced the
constant:

```
sed -i 's/Weights::literal::<4000, 2500, 2000, 1500>()/Weights::literal::<3500, 1000, 2500, 3000>()/' \
  crates/hee-ml/src/weights.rs
cargo test -p hee-ml        # test result: ok. 60 passed; 0 failed
```

Every test still passed, because every one of them was self-consistent with whatever the constant
said. And **`cargo-mutants` cannot find this**: it mutates function bodies and match arms, not the
digits of a `const`, so a 100 %-caught mutation score says nothing about a frozen table. Two
controls that both looked strong were blind to the same thing.

The fix is a **read-back test against an independent source**: assert each component by name
(`FROZEN.fit().get() == 4000`, …) with the document the number came from cited in the test's doc
comment (F94 — a known answer may not come from the head that wrote the code).

**It is now a gate step**, because a rule without a detector is a slogan:
`scripts/constants.py` (+ `--control`, 5 cases) in HEE-v2 requires, for every `pub const` whose
expression carries a literal, an assertion in that crate's own tests naming the value the
expression RESOLVES to. Exemptions are declared in the source (`pin: <reason>` in the doc), never
in a list, and counted.

**Writing it produced five false readings, every one a clean sweep over a tree with real gaps** —
worth knowing, because each is a plausible way to write this check:

| draft's predicate | what it missed |
|---|---|
| the literal appears anywhere in the crate | doc comments restating a value; **all 22 constants read as pinned** |
| assertion **lines** carry the value | rustfmt puts a long `assert_eq!`'s value on its own line, which has no `assert` on it |
| substring-match digits over one workspace blob | `999999` matched inside an unrelated string; a scratch crate's constant read as pinned by *another crate's* test |
| the test module is `mod tests` | `wire/tests.rs` (included by `#[path]`) and a second `mod ceiling_tests` were invisible |
| arithmetic is `+ - * /` | `1 << 20` resolved to nothing, so its real pin went unseen |

The final predicate: a pin is a **number an assertion in the constant's own crate names**, resolved
from the expression (arithmetic, shifts, and a `Duration`'s whole seconds) — and an assertion that
merely echoes the definition's expression does not count, because it compares an expression with
itself.

**The trigger:** any constant that encodes a policy — weights, thresholds, floors, a schema
version, a frozen table. Grep the suite for a test that names the *value*, not the constant. If
every reference is the constant's own name, the value is unpinned.

---

### F123 · A deviation recorded only in a code comment is not recorded — two reviewers raised the same finding because the pointer named a file section that did not exist

*Found 2026-09-06; two of three `hee-ml` lenses raised the cost-standing pin independently.*

The crate deliberately departed from its brief on one number and said so in a test comment:
"Recorded as a deviation in the receipt rather than special-cased here." No such receipt section
existed — the receipt was still a draft in another process's hands. Two reviewers spent a full
probe each measuring a disagreement that was already known and already decided.

A deviation is recorded when it is **in the append-only evidence file, with the brief line it
departs from, the measured value, and the independent recomputation** — and the code comment
cites *that*, not the other way round. Same family as Mistakes #28/#29: a caption pointing at a
check that does not exist reads exactly like one that does.

---

### F124 · A `contains` assertion on a rendered line is satisfied by a renderer that reads none of its fields

*Found three times in one wave, 2026-09-05/06, every one by a verify pass planting the literal.*

```rust
let rendered = SynergyError::RowCapExceeded { cap: 7, observed: 8 }.to_string();
assert!(rendered.contains("cap 7") && rendered.contains("8 rows"), "{rendered}");
```

Replace the format string with the constant `"row cap 7 exceeded: 8 rows were handed in; nothing
was decoded"` and **the whole suite stays green** — as does clippy, and as does mutation testing.
The crate's own `println!("{err}")` then prints that constant from a renderer reading neither
field.

Why the other controls miss it: `cargo-mutants` replaces a `-> String` body with a placeholder
like `"xyzzy".into()`, which a `contains` assertion *does* catch. It never generates the
**plausible** hard-coded line — which is exactly what a test fitted to one fixture invites
someone to write.

**The fix, and it is cheap:** assert the WHOLE line for **two** fixtures whose fields all differ.
One `assert_eq!` becomes two; a renderer cannot hard-code both. Applied here to a report's
`verdict_line`, to nine of ten `hee-ml` refusal renderings and to both `hee-synergy` cap refusals.

**The trigger:** any `Display`/`thiserror` message, any `verdict_line`, any log line a reader is
expected to act on. If a rendering is asserted once, or with `contains`, it is not pinned.

---

### F125 · A detector's negative control proves the detector fires, not that each of its rules is load-bearing — mutate the detector

*Found 2026-09-06 on the W6 exit criterion, by a review lens that thought to mutate the checker
rather than the code.*

`scripts/ordering.py` is the wave's exit criterion: the policy-decision record must precede the
effect call. Its control planted thirteen faults and required each by its printed diagnostic —
`cases=7/7 faults=13/13`, the discipline this habitat has used since F96. The lens then applied
**eight one-line mutants to the detector itself** and re-ran `--control`:

```python
if "PolicyDecision" in statement:   →   if True:      # ANY append counts as the record
end = text.find(";", match.end())   →   end = -1      # the statement bound removed
def documented(...): ...            →   return True   # the "documented" exemption always granted
if constants > 1:                   →   if False:     # the one-constant rule off
```

**The control stayed green for several of them, including the first** — which erases the wave's
entire exit claim. Thirteen planted faults, and the rule that distinguishes a policy-decision
record from any other append was exercised by none of them: every fixture that tripped the rule
also tripped a neighbouring one, so a fixture set that *looks* exhaustive tested the conjunction
and not the terms.

Two more shapes fell out of the same pass:

- **An unfalsifiable needle counted as a check.** `forbid(out, "line=6 detail", …)` — the
  detector formats that finding without any `detail=` field, so no output can ever contain it.
  It was counted into a printed `exemption_quiet=2/2`. A caption inside a control (Mistakes #28,
  one level in).
- **A diagnostic that names the innocent file.** The door was chosen by `sites.sort(); sites[0]`
  — lexicographic filename — so when a bypass existed the finding named the clean file, and the
  control had *enshrined that inverted attribution* as its required output. The control was
  asserting on a diagnostic, exactly as F96 requires, and the diagnostic was wrong.

**The rule:** for each rule a detector states, apply the smallest mutant that neuters that rule
and require the control to fail. Enumerate the rules from the detector's own docstring, not from
the author's list. A control that survives a mutant of the rule it was written for is a fixture
set, not a control.

### F125b · …and "enumerate from the docstring" is not enough as an instruction — the control must derive its own clause set

*Measured 2026-09-06, the round after F125 was written and acted on.*

The fix round did what F125 says: it built **twenty-one mutants, one per rule, every one killing
the control**, and reported that as decision 20 met. The adversarial pass then enumerated the
clauses **from the module docstring** and built **85 mutants**, of which **26 survived** — nine
with a constructed input showing a false pass on the criterion itself: a policy record handed to a
*metrics* sink rather than the journal; a record in a *sibling* function; the executor call inside
a *nested* `fn`; a second door spelled UFCS; a whole *submodule directory* evading three rules
because the source walk was not recursive; `unbounded()`; `stream.peer_cred()`, which is std's own
API and precisely the spelling the rule exists to catch.

The author's twenty-one were one per rule **on a hand-kept list**. The docstring stated materially
more clauses than the list held — and **F65 says an include list cannot see an omission**. The
instruction was right and unenforceable; only a mechanism closes it:

> **The control derives the clause set from the docstring and REFUSES when any clause has no
> case** — printing `clauses=N/N` the way a detector prints its denominators. A clause without a
> case is a control failure, not a note.

**And the dangerous direction is the one you do not expect.** Three of the surviving mutants were
*false positives*: the detector reddening a CORRECT daemon — including `blocking_send`, the
writer-actor handoff the wave's own decision mandates, and a `tests/` directory the docstring
already excluded. A false pass lets a defect through; a false positive makes the team route around
the gate, and the routing-around is invisible. When you mutate a detector, classify every survivor
as false-pass, false-positive, unpinned-value or equivalent, and construct the input for each.

---

### F126 · A fan-out agent can write into the MAIN checkout, and a gate line does not say which tree it measured

*Found 2026-09-06 during a W6 fan-out; caught only because the change happened to add a gate step.*

Every sandbox brief in this habitat says the main checkout is READ-ONLY and names the worktree the
agent owns. One nevertheless left three files in the main checkout — two modified, one untracked —
while a fan-out ran. `git status --short` on main had been clean an hour earlier and was clean
again in my head, so I ran `just gate` and read `PASS`. **The run measured someone else's
unreviewed work.** What gave it away was the step count moving 13 → 14; had the change not added
a step, a measurement over an unknown tree would have gone into a receipt.

The change itself turned out to be right — `genesis_status.py` printed `verdict=BLOCKED` and
returned rc=0, this codebase's own founding antipattern — so it was verified and kept, the way a
human's commit is (authorship decides nothing; the gate does). That is not the finding.

**The finding is that a verdict named no tree.** `verdict=PASS steps=14 passed=14 failed=0` is a
claim *about a tree*, and every gate line ever quoted into a receipt here omitted which one. The
fix is a mechanism, not a habit:

```
verdict=PASS steps=14 passed=14 failed=0 tree=9b0af05 dirty=1
```

`dirty` is what a reader checks before believing the rest of the line. Extends F109 (a fan-out's
receipts are its agents' claims; the worktrees are the evidence) with the case F109 did not cover:
the tree the *fuser* is standing in is also evidence, and it can move under you.

---

### F127 · `juliaup`'s launcher reaches the network on every run — in an offline container, call the real `julia` binary instead

*Found 2026-09-06 provisioning the HEE-v2 deep-verify lane on Fedora Kinoite.*

Three separate traps, all on the way to one working `julia`:

**1. The installer's own downloader times out where `curl` succeeds.** `sh install.julialang.org
--yes` installed `juliaup` itself and then died: `Failed to download from url
…julia-1.12.7-linux-x86_64.tar.gz … operation timed out`. The endpoint was fine — a `HEAD`
request hung for 55 s, while a ranged `GET` pulled 1 MiB immediately. Fetch the tarball yourself
with `curl -C -` (resume), verify it against
`https://julialang-s3.julialang.org/bin/checksums/julia-<version>.sha256`, and extract into
juliaup's own layout:

```
~/.julia/juliaup/julia-1.12.7+0.x64.linux.gnu/     # --strip-components=1
```

then register it by editing `~/.julia/juliaup/juliaup.json` (`InstalledVersions`,
`InstalledChannels`, `Default`). `juliaup status` then lists it as if it had installed it. The
version key is in `~/.julia/juliaup/versiondb-*.json` — read it, do not guess the `+0.x64.linux.gnu`
suffix.

**2. The installer does not create the `julia` entry point when it dies partway.** `~/.juliaup/bin`
held `juliaup` and `julialauncher` but no `julia`; it is a symlink to `julialauncher`.

**3. `julialauncher` needs the network even for an already-installed version.** Inside
`podman run --network none` it fails before starting Julia:

```
Failed to download from url `https://julialang-s3.julialang.org/juliaup/RELEASECHANNELDBVERSION`
… dns error … The Julia launcher failed to figure out which juliaup channel to use.
```

So a cold, offline run must bypass it and exec the real binary:
`<depot>/juliaup/julia-1.12.7+0.x64.linux.gnu/bin/julia`.

**The offline recipe that works**, and it needs no new container image — the depot mounts the way
the Rust toolchain already does:

```bash
podman run --rm --network none --security-opt label=disable \
  -v "$HOME/.julia":/juliadepot:ro -v "$PROJECT":/proj:ro -v "$OUT":/out:rw \
  -e JULIA_DEPOT_PATH=/out/depot:/juliadepot -e JULIA_PKG_OFFLINE=true -e HOME=/out \
  localhost/forge-sandbox:1 \
  /juliadepot/juliaup/julia-1.12.7+0.x64.linux.gnu/bin/julia --project=/proj -e '…'
```

The **writable first entry** of `JULIA_DEPOT_PATH` is what makes a read-only depot usable: Julia
writes precompilation output to the first entry and reads packages from the rest. Without it the
run dies trying to write into the mount.

**Kinoite note:** all of this lives under `$HOME` (LUKS NVMe), so it survives a toolbox rebuild —
unlike a `dnf install` into the container's `/usr`. `~/.bash_profile` carries the PATH block the
installer wrote, and that is `$HOME` too.

---

### F128 · A receding horizon is evidence about the design — when a check's rule surface grows faster than you can cover it, the language can model it better

*Measured over three rounds on one detector, 2026-09-06.*

`scripts/ordering.py` existed to prove HEE-v2's W6 exit criterion: the policy-decision record is
written before the effect call, and no other door to the executor exists. It is a textual scan over
Rust source. Three adversarial rounds, each closing everything the last one found:

| round | what the author measured | what the next pass measured |
|---|---|---|
| 1 | 13 planted faults, `cases=7/7` | 8 mutants of the detector survived, one erasing the whole criterion |
| 2 | **21 mutants, one per rule, all killed** | **85 mutants from the docstring, 26 survived**, 9 false passes |
| 3 | **63 clause markers, all covered**, `clauses=63/63` | **127 mutants, 36 survived**, 8 on stated sub-clauses |

Every round did more than the last and every round was found wanting. That is not an implementation
problem. **A regex over Rust has an unbounded rule surface**: each alternation, anchor, case-fold
and bounded repetition is another clause a mutant can neuter, and the detector was being asked to
model Rust's call graph — nested functions, UFCS spellings, submodule directories, five spellings
of a channel send.

**The fix was to stop scanning and make the bad state unrepresentable.** The executor no longer
takes an intent; it takes a `Journaled<EffectIntent>`, a newtype with a private field whose *only*
constructor performs the journal handoff — so the append and the token are one call. A second door
cannot compile because it cannot obtain a token; an effect before its record cannot compile because
the token does not exist yet. The detector keeps only what a type cannot express: the source walk's
scope, no unbounded channel, no shared-state lock, no identity from the peer, no state-dir default —
each a small closed surface a control can actually cover.

**The trigger, and it is countable:** track surviving mutants per round. If the count is not
falling, the next round is not the answer. Ask what the compiler could refuse instead. *What the
compiler refuses, no check has to catch* — and this codebase already owned the pattern
(`Spec<Admitted>` is the only thing that can mint a `DeployToken`).

Related: F125/F125b (mutate the detector; the control must derive its own clause set) — those tell
you the check is weak; **this one tells you when to stop strengthening it and change the design.**

---

### F129 · A value pinned only where the right answer is the identity element is unpinned — `1`, `0`, `GENESIS`, `dispatch-1` and an empty set all agree with a constant

*Measured by three review lenses over sandbox A of HEE-v2 W6, 2026-09-06.*

The router mints two records per effect and cites, on the outcome row, the sequence number of the
decision that licensed it — "so the pairing is checkable in the journal rather than inferred from
adjacency". Every test dispatched **once** on a **fresh** bench. The first ordinal is 1, the first
sequence is `Seq::GENESIS`, the first event id is `dispatch-1`. So each of these survived being
**frozen to a constant** (`cargo test` rc=0 every time):

| line | planted | result |
|---|---|---|
| `Ok(Self { value, at })` | `at: Seq::GENESIS` | survived |
| `("decided_at", effected.decided_at().to_string())` | `"1"` | survived |
| `EventId::parse(ordinal_id("dispatch", self.dispatched))` | `ordinal_id("dispatch", 1)` | survived |
| `sequence: Seq::new(self.dispatched)` | `Seq::new(1)` | survived |
| `cost_microunits: Some(self.limits.effect_cost())` | `Some(Microunits::new(1))` | survived |

The suite was thorough by every reading measure and **mutation testing cannot see this either**:
`cargo-mutants` does not plant `1` for a computed ordinal, and its `Default::default()` replacements
were all unviable. The test asserted the right value; the right value just happened to be the value
a broken renderer would also produce.

**The fix is by construction, not by inspection:** dispatch **three** times on **one** bench and
assert the whole bodies of rows 2 and 3 as two fixtures that differ in every field. A test whose
expected value equals the initial/identity element of the thing computed (first ordinal, empty
collection, zero cost, genesis sequence) discriminates nothing; move it off the origin.

Same family as F122 (a constant every test reads through) and F124 (a `contains` on a rendered
line): all three are values a suite reads *past* rather than *at*. Trigger: any assertion whose
expected literal is `0`, `1`, `GENESIS`, `""`, `[]` or `<prefix>-1` — ask what the second one is.

---

### F130 · A needle that the failing diagnostic's own quoted source line contains is not a needle — the control passed on an error that never reached the rule

*Measured by the refute lens over sandbox B of HEE-v2 W6, 2026-09-06.*

The daemon crate bans `std::os::unix::net::UnixStream::peer_cred` in `clippy.toml` (no identity
from the peer). Sandbox B's negative control planted the call, saw `rc=101`, grepped the output for
`peer_cred`, found it, and printed `case=peer_cred rc=101 diagnostic=named` — a pass.

The error was **`E0658: use of unstable library feature`**. The path is unstable on rustc 1.98.0,
so the compiler refused it *before clippy's lint ever ran*. And rustc's rendering **quotes the
offending source line**, which of course contains `peer_cred`. The needle was supplied by the
plant, not by the rule.

Meanwhile the spelling the acceptor can actually reach — `tokio::net::UnixStream::peer_cred`, the
type it holds — passed `cargo clippy --all-targets --all-features` at rc=0 with a uid-derived
refusal planted. **The ban banned nothing the code could call** (that half is F131).

F96 says: assert on the diagnostic, not on a non-zero exit. This is one level under it: **assert on
the diagnostic the *rule* emits** — here `use of a disallowed method` and the path it names — never
on a substring that the planted source itself carries, because every compiler error quotes the
source. The test of a needle: could this output contain it if the rule did not exist?

---

### F131 · A `disallowed-methods` entry whose path the toolchain cannot call bans nothing — and clippy ignores an unresolvable path silently

*Measured 2026-09-06 on clippy 0.1.98, HEE-v2 W6.*

Two ways for a clippy.toml ban to be a rule that does not exist:

1. **The path is unstable or gated.** `std::os::unix::net::UnixStream::peer_cred` needs
   `peer_credentials_unix_socket`; nothing on stable can spell it, so the entry is a
   *stabilisation tripwire* at best, and the callable spelling (`tokio::net::UnixStream::peer_cred`)
   went unbanned.
2. **The path does not resolve at all** (typo, crate not linked, renamed item). Measured by
   sandbox B: an unresolvable entry produces no warning and no error — the config is accepted and
   the rule is simply absent. In a crate that does not link `tokio`, the four `tokio::sync::*`
   entries were exactly this until fusion.

So a `disallowed-*` entry needs a **loud negative control on the tree it is meant to bind** — plant
the callable spelling, require the lint's own diagnostic naming that path (F130) — and the control
must run again whenever the dependency set changes, because resolution is a property of the linked
crates, not of the config file. An include list of banned paths is still an include list (F65):
enumerate the *types the code actually holds* and ban the door on each of those.

---

### F132 · "Written before the effect" was true of a buffer — an acknowledgement is a claim about the disk, and the kill test must run against the real writer

*Found by the refute lens on the fused HEE-v2 daemon, 2026-09-07.*

The W6 hypothesis: the policy-decision record is written before the effect. The type proved the
order, the runtime test proved it on every path, the golden path proved it through a real socket.
Then the refuter sent N refusals, waited for each acknowledgement, and `SIGKILL`ed the daemon:

| acknowledged | rows on disk |
|---|---|
| 1 | 0 |
| 10 | 0 |
| 50 | 34 |
| 200 | 187 |

The event-store's `Writer::append` writes into an 8 KiB `BufWriter`; only `sync()` flushes and
fsyncs, and the daemon called it once — at the seal. Every row was "written" into memory the
process owned, and the peer was handed a `decided_at` for a row that did not exist yet. The
segment sizes on disk (15 859 and 87 485 bytes) are multiples of the buffer, which is the
mechanism showing itself.

Why three layers of proof missed it: the kill-between-them test ran against an **in-memory
double**, and the process-level kill test killed a daemon that had **written no row before the
kill**. Both were correct tests of the thing they held; neither held the real writer with rows in
flight. **Durability is a property only the real writer under a real kill can show**, and "written"
in a claim must mean *fsynced before the acknowledgement*, or the claim is about the buffer.

Fix: `sync()` after every append, before the ack; a sync failure is the refusal the ack carries.
The probe became the test: N ∈ {1, 10, 50, 200}, `rows_on_disk == N`, torn = 0.

Trigger: any sentence of the form *X is recorded before Y* — ask what "recorded" means at the
moment the caller is told, and whether the test that proves it holds the real sink.

---

### F133 · A reviewer's plant killed by `forbid(dead_code)` is a kill for the wrong reason — re-run plants under `--cap-lints=warn`, as cargo-mutants does

*Measured on the W6 post-fusion verify, 2026-09-07.*

Four plants a reviewer had recorded as "killed by name" died under the tree's own lint law
(`forbid(dead_code)`, `deny(unused_imports)`) before any test ran: the plant left a function or
import unused, the build refused, the verifier read `rc=101` and a test name in the output, and
called it a kill. Under `RUSTFLAGS=--cap-lints=warn` — which is how `cargo-mutants` builds every
mutant, precisely so that a lint cannot masquerade as a test — two of the four were still killed
by the intended assertion and two were not.

This is F96 (a control that fails for the wrong reason) applied to plant batteries: a plant must
be killed by the test the finding names, and a lint kill is silence about the test. Rule for any
plant battery: build with `--cap-lints=warn`, require the named test in the failure output, and
record a lint-only kill as `killed_by=lint` — a survivor until the test exists.

---

### F134 · A completeness check whose denominator comes from the same side as its numerator cannot see truncation

*Found by a second agent on the same codebase, 2026-09-07, in my own mutation gate.*

`scripts/mutants.py` refused an incomplete run — that was the whole point of the check, added at
W4 after a quota-killed run (F118). It read `found` and `tested` from `outcomes.json` and refused
when `tested < found`. Both numbers came from the **completed outcomes**, so they were equal by
construction. An interrupted run that enumerated 2732 mutants and completed 1187 printed
`found=1187 tested=1187 … verdict=PASS`.

The enumeration lives in a different file — `mutants.json`, written before testing starts. The
denominator has to come from there, and the check now compares identities (not counts) between the
enumeration and the outcomes, refusing on a missing, duplicate or unknown outcome, and on the
tool's own non-zero exit.

**The general shape:** a completeness check is a claim about what was *not* done, and the record of
work done cannot supply it. Ask of any "N of N" line: *where does each N come from?* If both come
from the same collection, the line says only that the collection is self-consistent — F65's
include-list problem, wearing a denominator.

It cost nothing to hold this belief for four waves because no run was interrupted in a way that
mattered; that is luck, not evidence. Related: F118 (the quota-killed run that motivated the check),
F65 (an include list cannot see an omission), F125 (mutate the detector).

---

### F135 · A watcher that checks liveness after content calls a finished run "gone" — re-read the artifact before declaring failure

*Measured twice in one evening, 2026-09-07, on my own Monitor loops.*

The loop is the obvious one:

```bash
while true; do
  grep -qE "^verdict=" "$LOG" && { grep -E "^verdict=" "$LOG"; exit 0; }
  kill -0 "$PID" 2>/dev/null || { echo "RUN GONE without a verdict"; exit 1; }
  sleep 30
done
```

Between the `grep` and the `kill -0`, the run can write its verdict and exit. The watcher then
reports **GONE without a verdict** on a run that passed — twice here, once on a cold-container run
whose log said `verdict=PASS cold=YES checks=6/6 tests=1663`, and the false alarm cost a diagnostic
detour into a script that was working.

The fix is one line: on the not-alive branch, **read the artifact again** before deciding.

```bash
  kill -0 "$PID" 2>/dev/null || {
    grep -qE "^verdict=" "$LOG" && { grep -E "^verdict=" "$LOG"; exit 0; }   # finished between checks
    echo "RUN GONE without a verdict"; exit 1; }
```

Same shape as F132 and W6 decision 118: the check asked a *different* source (the process table)
than the one that carries the answer (the log), and the two disagree for an instant on every
successful run. Whenever a watcher has a fast path and a failure path, the failure path re-reads
what the fast path reads.

---

### F136 · A divergence gate that counts "the comparison did not happen" as a catch is the false pass it was built to prevent

*Found by three review lenses on HEE-v2's W7 second-opinion lane, 2026-09-08.*

The wave exists because of an audit finding: *agreement is the pass condition, so a lane that
computes on zero rows, errors into a default, or is never invoked passes perfectly — and more
reliably than a working one.* The answer was a **divergence family**: plant a mutation, require the
two lanes to disagree, print `divergence_planted=N caught=N`.

The driver counted a plant as caught with `if !comparison.is_agreement()`. Its four outcomes are
`Agree`, `Disagree`, `Inert` and **`Incomparable`** — the last meaning *the two lanes described
different subjects or different windows*, which the comparator's own docstring calls "a comparison
that did not happen … the false pass this codebase exists to prevent". One family member perturbed
the window, so the lanes answered about different spans, and the non-comparison scored as a catch.
The published `9/9` was `8/9` under the wave's own written criterion.

Three further shapes travelled with it, and all four are the same mistake at different altitudes:

- **The criterion ran only when a human typed the recipe.** Neither the gate nor the exit runbook
  invoked the driver; a reviewer wrote three lines of non-Julia into the lane's hash module and the
  18-step gate still printed `PASS`. *Enforcement belongs in the artifact, not the invocation.*
- **Two lanes rejecting one window for unrelated findings returned `Agree`,** because the comparison
  reduced each verdict to its *kind*. Both said "no"; nobody asked whether they said no to the same
  thing.
- **The generated half could be switched off silently:** `sampled=0/0` satisfied `sampled == samples`.

**The rule:** a pass predicate names the outcomes that count, and every denominator it prints must
be unable to reach zero unnoticed. Ask of any `N/N`: *which outcomes does the numerator admit, and
can the denominator be zero?* Then plant the outcome you did not think to admit.

Related: F134 (a completeness check whose denominator comes from its own numerator), F125 (mutate
the detector), and the founding rule that a recipe printing BLOCKED must not exit 0.

---

### F137 · `setsid nohup cmd &` gives you the wrapper's PID, not the job's — watch the artifact, not a PID you guessed

*Measured twice in one session, 2026-09-08.*

Detaching a long job so a tool timeout cannot kill it:

```bash
setsid nohup bash scripts/cold.sh "$TREE" > run.log 2>&1 < /dev/null &
echo "pid=$!"        # ← this is SETSID's pid, and setsid exits immediately
```

`setsid` forks, hands the work to the child, and returns. `$!` therefore names a process that is
already gone seconds later. A watcher built on it reports **"GONE without a verdict"** while the
job is still building, and the false alarm is indistinguishable from the real failure it was
written to catch — here, on a cold-container run that was fifteen minutes from finishing.

Two fixes, and the second is the one that generalises:

1. Capture the real child: `setsid … & sleep 1; pid=$(pgrep -f "scripts/cold.sh $TREE")`.
2. **Watch the artifact.** The verdict line in the log is the thing you actually want; a process
   table is a proxy for it. Poll the log for the verdict, and use liveness only as a secondary
   check — on the job's *command name*, not a captured id — re-reading the log before declaring
   failure (F135).

**Strengthened the same evening, after a THIRD false alarm.** Fixing the pid did not fix the class:
a watcher whose loop is `check the artifact, else check liveness` produces a false "gone" whenever
the two disagree for an instant, and they disagree on every successful run and on every process
that has not yet settled. Naming the job by command instead of by pid moved the race, it did not
remove it — the third alarm fired on a runbook that was visibly mid-`cargo test`.

**The rule that ends it: poll the artifact ONLY.** Give the watcher a generous timeout and let the
timeout be the failure signal. A liveness branch buys nothing a timeout does not, and it costs a
false alarm indistinguishable from the real one:

```bash
while true; do
  grep -qE "^verdict=" "$LOG" && { grep -E "^verdict=" "$LOG"; exit 0; }
  sleep 60
done      # the watcher's own timeout is the only failure path
```

Same family as F135 (a watcher whose failure path does not re-read what its success path reads) and
W6 decision 118 (a check whose input comes from a different world than the thing it certifies).
Three times the proxy was cheaper to consult and wrong.

---

### F138 · A gate that exits 0 having examined nothing is indistinguishable, by exit code, from a gate that examined everything and found it clean

*Found in this habitat's own gate stack, 2026-09-08, while chasing a regression in the weight matrix.*

Three vault gates — `backlinks`, `orphans`, `deadpaths` — are written as:

```bash
for v in */; do [ -f "$v/.habitat-gates" ] || continue; python3 <checker> "$v" || exit 1; done
```

They iterate the **caller's working directory**. The gate stack runs them from the arena, which has
no `*/.habitat-gates` marker anywhere (measured: 0). The loop body never executes, the loop exits 0,
and three gates have been reporting green while checking **zero vaults**.

The weight matrix then counted them *live* (its liveness test is "baseline exit code is 0") and
listed the four faults they exist to catch — `one_way_link`, `broken_wikilink`, `orphan_note`,
`dead_path` — among nine "blind spots", with no hint that the gates for them were the reason. A
regression that reads as *"the stack got worse"* was really *"three gates went dark and the report
could not say so."*

**Two repairs, and the second is the general one:**

1. `scripts/audit/gated_vaults.sh` enumerates `*.vault` under the vault **root**, requires the
   opt-in marker, and refuses `verdict=BLOCKED reason=no_gated_vaults` rc=1 when it would check
   nothing.
2. **The matrix now reads the denominator each gate prints** (`vaults=`, `notes_scanned=`, `tests=`,
   `cases=`, `N passed`, …). A gate that exits 0 with a denominator of **zero** is marked `VACUOUS`,
   is NOT counted live, and is listed by name; a gate that prints no denominator at all reads
   `measured=?` and is reported as unknown rather than guessed either way — that is a gap in the
   gate, and saying so is better than assuming.

**The rule:** an exit code says whether a check *completed*, never whether it *measured*. Any gate
worth trusting prints what it looked at, and any aggregate over gates must refuse to count one that
looked at nothing. This is F136 ("no denominator reaches zero unnoticed") applied one level up —
to the thing that scores the gates.

The sting: the fault list the matrix reported as uncaught includes `pkill_self`, and the author of
this note committed exactly that fault the same morning (Mistakes #37). The detector that would
have caught it was one of the dark ones.

---

### F139

**A command substitution does not return while a backgrounded child still holds its stdout pipe —
and `timeout` on the inner command does not bound the wait.**

`pids=$(loadgen 12)`, where `loadgen` forks twelve `(while :; do :; done) &` spinners and echoes
each `$!`, never returns. The PIDs are written immediately, but `$( )` reads until **end of file**,
and EOF arrives only when every writer closes the pipe — including the background children, which
inherited it. So the capture blocks for the children's entire lifetime. Mine blocked **2 h 45 min**
on a hunt script, with twelve busy-loops pinning the machine at load average 21 the whole time, and
the script's own log frozen mid-run at two of four runs so it read as merely slow.

Measured both ways, 30-second children:

| case | elapsed | PIDs captured |
|---|---|---|
| child inherits the pipe | **30 s** | 2 |
| child redirects its stdout | **0 s** | 2 |

The redirect costs nothing and captures the same PIDs, because `echo $!` runs in the function, not
in the child.

**The part that makes it dangerous:** the probe above ran the generator under `timeout 5`, and the
elapsed time was still 30 s. Killing the inner command does not close the pipe — the orphaned
grandchildren still hold it, in the **outer** shell's substitution. A budget on the command is not
a budget on the wait, which is W6's shutdown finding in a different costume, and F102's
"every loop needs a budget" one level out: the thing that needed bounding was not the loop.

```bash
gen() { for i in $(seq 1 12); do (while :; do :; done) >/dev/null 2>&1 & echo $!; done; }  # returns
gen() { for i in $(seq 1 12); do (while :; do :; done) &                    echo $!; done; }  # hangs
```

Better still, take no substitution at all — build the list in the current shell, where the PIDs are
already in scope:

```bash
pids=""; for i in $(seq 1 12); do (while :; do :; done) >/dev/null 2>&1 & pids="$pids $!"; done
```

**The trigger:** any `$(...)` around a function that backgrounds anything long-lived. Also any
`x=$(cmd &)`, and any pipeline whose producer forks a daemon. If a capture can outlive the command
it captured, redirect the child or drop the substitution.

**How it surfaced:** the watcher on the hunt timed out with no output, per F137 — poll the artifact,
never the process. The artifact was three hours stale while the process was very much alive, which
is exactly the state a liveness check would have called healthy.

---

### F140

**A census over reason NAMES cannot see a reason raised from two places. Count the SITES.**

A detector declared twelve refusal reasons and its control printed `reasons=12/12`. Then a sweep —
each refusal neutered to `pass` in turn, the full control re-run — killed only eleven of eighteen:

```
SWEEP tested=18 killed=11 survivors=7
  SURVIVED  raise Refusal("packets_unreadable", f"{path} is not a file")
  SURVIVED  raise Refusal("packets_unreadable", f"{path} does not declare schema ...")
  SURVIVED  raise Refusal("packets_unreadable", f"{path} declares no packets object")
  ...
```

`packets_unreadable` is raised from **three** places and one planted case covered all three. The
name was covered; the rules were not. Same for `gate_unreadable`, `dispositions_unreadable` and
`tier_unreadable`, each of which has an "is not a file" site and a "cannot be parsed" site.

**The fix has two halves, and the first alone is not enough.**

*Enumerate sites, not names.* The world is every `Refusal(...)` construction, read from the
detector's own source with `ast` so a site added tomorrow is missing from the denominator rather
than absent from a list somebody maintains. Where a detector refuses two ways — `raise` for what
stops the measurement, `append` for what it collects — traceback attribution only sees the first;
recording the caller's line in `__init__` (`sys._getframe(1).f_lineno`) covers both through one door.

*And assert the site's own diagnostic.* With a case per site the absent-file site STILL survived:
neutering the raise let the absent file fall through to `read_text`, raise `OSError`, and the NEXT
site raise **the same reason**. A case that asserts only the reason passes while the rule it was
written for is gone. Each case must assert the detail only its site produces — `is not a file` vs
`is not JSON` vs `does not declare schema`.

Result after both halves: `SWEEP tested=19 killed=19 survivors=0`, control `reasons=12/12
sites=19/19`.

**The trigger:** any control printing `reasons=N/N`, `cases=N/N` or `clauses=N/N` where a reason can
be raised from more than one place. Grep the detector for its reason strings; a name appearing twice
is a name doing the work of two rules. This is F125b one level in — that finding says a control must
enumerate its rules from the detector rather than from the author; this says the *unit* of
enumeration is the raise site, because the author picked the names.

**Related, same file, same afternoon:** a regex reading a declared tuple stopped at the first `)`,
which was inside `"DG1-d anchor venue (UNMEASURED)"`, and reported **one** open item where three
were declared. That error ran in the flattering direction — it made the system look closer to
complete than it is. Parse a declaration with `ast`, never with a non-greedy paren match. And twice
in the same file a neighbouring artefact's field name was read from memory rather than from its
schema (`path` for `module`, `excluded_reason` for `excluded`); both made a rule go **quiet** rather
than loud, which is the direction that costs you.

---

## Method note

Every finding here came from a failure with a visible symptom, then a bounded experiment to
isolate the cause — e.g. F11 was found by `timeout 5 rg …` with and without a path argument;
F3 by testing `--script` values with and without spaces until the ENOENT made the semantics
obvious. **The habit that produced them: when something behaves oddly, shrink it to a
two-line repro before theorising.**

Related: [[00 - Toolshed Index]] · [[00 - Workflows]] · [[Habitat Reactor]] · [[Arena Practice Ground]] · [[Forge - Deployment Framework]]


### F141 · `PostToolUse` does not fire for a FAILED Bash call

*Measured on this machine, claude 2.1.266, 2026-09-11.*

Building a novel-failure channel as a `PostToolUse` hook on Bash, the hook never saw a single
failure. Two probes with unique tokens, one command each:

```
failing command  (exit 5, token ZZUNIQFAIL)  → occurrences in the hook's own log: 0
succeeding command      (token ZZUNIQPASS)   → occurrences in the hook's own log: 1
```

The documentation states it plainly — *"PostToolUse fires after a tool call succeeds"* — and it
means the tool call, not the shell command: a non-zero exit is a tool ERROR and the event is never
emitted. **Any hook that reacts to command failures cannot live at `PostToolUse`.**

Two further facts from the same probe, neither documented:

- The payload's `tool_response` for Bash is
  `{interrupted, isImage, noOutputExpected, stderr, stdout}` — **there is no exit code in it**, and
  `stderr` is empty because the harness merges it into `stdout`. The `{code, stdout, stderr,
  interrupted}` objects visible in the binary are the INTERNAL shell result, not the hook payload;
  reading them and assuming otherwise cost two wrong implementations.
- A user-level hook fires for **every agent on the machine**, including subagents (`agent_id` /
  `agent_type` appear in the payload). Another session's `git status` showed up in the log within
  seconds.

**AMENDED 2026-09-14 — the venue exists after all, and it is not `PostToolUse`.** Reading the
binary's declared hook events turned up **`PostToolUseFailure`**, alongside `FileChanged`,
`PostToolBatch`, `SessionEnd`, `StopFailure` and others. So the finding above is correct as written
— a failure never reaches `PostToolUse` — but the conclusion a reader might draw from it, *"no hook
can see a failed command"*, is **false**. There is a dedicated event for exactly that.

What does not change: the check still belongs where the exit code is owned, and `gate` already owns
it for every verdict this habitat quotes. What does change is that a hook-based version is now
possible and unbuilt. Recorded rather than built, because the working implementation exists and a
second door on one rule is a promise, not a mechanism.

**Where such a check belongs instead:** a command wrapper that owns the exit code by construction —
here `~/.local/bin/gate`, which already exists for the pipe-verdict rule. Position, not existence.

**Mirror:** my-diary `Mistakes I Made` #40 · `00 - Principles` P8 ·
[Deploying the Diary's Learnings](obsidian://open?vault=herdr-fedora-habitat.vault&file=50%20Automation%2FDeploying%20the%20Diary%27s%20Learnings)

### F142 · `open(path, "w")` truncates BEFORE the value is computed — a failed rewrite leaves zero bytes

*Measured on this machine, python 3.14, 2026-09-13.*

A one-shot script rewrote `assurance/packets.json` "in the original style": detect the style, then
`open(p, "w").write(json.dumps(d, indent=style[0]))`. The style lookup returned `None`, the call
raised `TypeError` — and the file was already **0 bytes**, because the `open(..., "w")` on the
left of the expression ran first. The next command in the same shell line was `git commit`, which
recorded the empty file; the gate that started after it measured a tree whose plan was unreadable.

```
original style: None
TypeError: 'NoneType' object is not subscriptable
 assurance/packets.json | 1851 ++++++++++----------   ← 929 deletions, all of them the file
```

Two rules, one mechanism each:

- **Compute the whole new content, and parse or validate it, BEFORE the target is opened for
  writing.** `out = transform(text); json.loads(out); open(p, "w").write(out)` — or write to a
  sibling temp file and `os.replace` it, which is atomic and leaves the old bytes on any failure.
- **`git commit` is its own command** (Mistakes #36): a commit chained after a step that can fail
  commits whatever that step left behind. `set -e` does not help under the harness's `eval`.

The repair was textual (`git show HEAD~1:path`, edit the three lines, `json.loads` before writing),
and the local commit was amended. Nothing was pushed in between.

**Mirror:** my-diary `Mistakes I Made` #42 · `~/CLAUDE.md` §3 (commit alone).

### F143 · A temporary that owns a channel sender drops at the end of its statement — and the other side has two exit doors

*Measured on this machine, HEE-v2 W14 join `def8a5a`, 2026-09-13. Passed on the warm host every time (two unit gates, one join gate, 25 repeats); failed once, cold, under load.*

```
test workflows::tests::the_golden_walk_performs_every_step_stage_by_stage_from_rows_minted_first ... FAILED
assertion `left == right` failed
  left: (3, false)
 right: (3, true)
```

The runner was a temporary — `runtime.block_on(within("the run", Runner::new(handle).run(..)))` — and
it owned the effect queue's sender. It dropped when `block_on` returned, before `stop.cancel()`. The
executor on the other end exits by EITHER of two doors: the token (`cancelled: true`) or
`recv() -> None` when every sender is gone (`cancelled: false`). Warm, the executor task was never
polled between the drop and the cancel; in the cold container a worker thread was, and the
closed-channel door won. The test asserted WHICH door ended the executor while controlling only one
of them.

Three rules:

- **A test that asserts which of two doors fired must hold the other one shut.** Bind the value that
  owns the sender (`let runner = Runner::new(handle);`) until after the door you mean to fire.
- **A temporary in a `block_on(...)` argument lives to the end of that statement, not the block.**
  Anything it owns — a sender, a guard, a file — is released there.
- **The cold run is the evidence; repetition on the warm host is not.** Twenty-five warm repeats
  before the fix were green; one cold run was red. The cold container is loaded and freshly built, so
  its scheduling differs, which is exactly what makes it the discriminating input (P: cold verification).

**Mirror:** `~/CLAUDE.local.md` Gate 3b (verify cold, on exit codes) · HEE-v2 `evidence/receipts/w14-wave-exit.md`.


### F144 · A flatpak browser cannot open `~/.claude` — three routes fix it without touching the sandbox

*Measured on Fedora Kinoite, Chrome flatpak `com.google.Chrome`, 2026-09-14 (second occurrence; the
first was 2026-09-11).*

`/insights` writes its report to `~/.claude/usage-data/` and prints a `file://` link. The link is
**ERR_FILE_NOT_FOUND**. The file is fine — the reader cannot reach it. Chrome's sandbox grants
exactly:

```
filesystems = host-etc; xdg-music; xdg-pictures; xdg-videos; xdg-download; xdg-documents;
              xdg-run/dconf; xdg-run/pipewire-0          shared = ipc; network
```

`~/.claude` is in none of them. **On an immutable distribution this is the normal state, not a
fault**: the app is sandboxed and the filesystem is the thing you do not reshape. So the first
question is never "how do I widen the sandbox" — it is "which door is already open".

| # | route | evidence on this machine | cost |
|---|---|---|---|
| 1 | **Put it where the sandbox already looks** — copy into `~/Documents` (`xdg-documents` granted) | `71,943 bytes, mode 644`, loads | a duplicate file |
| 2 | **Transport, not filesystem** — `shared=network` is granted, so serve over loopback | `HTTP 200 bytes=71943 <title>Claude Code Insights` | a process while it runs |
| 3 | **The portal** — `xdg-desktop-portal` + `-kde` + `-gtk` all active; open via the app's own dialog (Ctrl+O) or drag the file in, granting access to THAT file dynamically | portal services `active` | manual, per file |

**The route to think twice about.**
`flatpak override --user --filesystem=~/.claude/usage-data:ro com.google.Chrome` is the documented
answer and it works — but it permanently widens a **browser's** sandbox to reach an **agent's state
directory**, whose sibling paths hold transcripts and credentials. A poor trade for a convenience
link. It also needs a browser restart: a running flatpak keeps the permissions it started with.

**Workflow note:** [[60 Workflows/Insights Reports - Opening Them Past the Sandbox]] — the current report's working link, the three doors, and the reflex that publishes it. The response to what that report measured is [[60 Workflows/Mitigation Plan]].

**Mechanised:** `~/.local/bin/insights-link` copies the newest report into `~/Documents`, verifies
the copy by size and readability rather than trusting `cp`'s exit status, and prints the working
link; `--serve` gives route 2. Both refusal paths are controlled — no report, and an unwritable
destination — each exits `rc=1` and prints no link.

**MECHANISED 2026-09-14, so it stops needing a person.** `~/.claude/hooks/insights-publish.sh` is a
`Stop` reflex: at the end of any turn in which a new report appeared, it publishes the report into
`~/Documents`, **verifies the copy by size and readability** rather than trusting `cp`'s exit
status, and surfaces the working `file://` link. Idempotent — an ordinary turn costs one `stat` and
prints nothing. Proven to fire on a fresh report, to stay silent on a repeat, and to stay silent
when no report exists (`habitat-reflex verify` → `reflexes=6 unproven=0`).

The precise alternative, available and not taken: a `SessionStart` hook returning `watchPaths` plus
a `FileChanged` hook (`hookEventName:"FileChanged", file_path`) would fire on the file itself rather
than at turn end. It is two hooks and a settings shape not yet observed working; the `Stop` route
uses only mechanics already proven here. Upgrade if the turn-end timing ever proves wrong.

**The general shape, worth more than the instance:** when a sandboxed app cannot see a file, ask
which doors are already open — a granted directory, the network, or the portal — and only then
whether the sandbox should change. **Widening a sandbox is the last resort, not the first fix.**

### F145 · `xdg-open` is broken on this machine — `kde-open` calls `flatpak-spawn` from the host

*Measured 2026-09-14, opening an HTML report from inside the toolbox.*

```
$ flatpak-spawn --host xdg-open "file:///…/report.html"
/var/home/Louranicas/.local/bin/kde-open: line 5: exec: flatpak-spawn: not found
```

`xdg-open` resolves to `~/.local/bin/kde-open`, a shim whose last line `exec`s **`flatpak-spawn`**.
That works when it is called from *inside* a container — but here it is already running **on the
host** (because the call was `flatpak-spawn --host xdg-open …`), and `flatpak-spawn` does not exist
in the host namespace. The shim assumes a direction of travel it cannot check.

**Nothing opened, and nothing said so.** The wrapper exited and the desktop did nothing.

**The route that works**, bypassing the shim entirely:

```
flatpak-spawn --host flatpak run com.google.Chrome "file:///…/report.html"
→ Opening in existing browser session.        (5 chrome processes, tab opened)
```

**The trap inside the trap.** The first attempt was reported as succeeding, because the command was
`… | head -3; echo "rc=$?"` — the status read was **head's**. `PIPE_SWALLOWS_VERDICT` for the fifth
time (Mistakes #11, #19, #21, #22, and this), caught this time only by reading the OUTPUT rather
than the number. The `PreToolUse` guard did not fire on this shape: `flatpak-spawn … | head` with a
separate `echo rc=$?` is a pipeline whose verdict is taken one statement later, which the detector's
pattern does not cover. **A guard is a claim about the shapes it has seen.**

**Why it matters beyond one link:** anything on this machine that shells out to `xdg-open` from a
host context — a notifier, a runbook step, a hook that wants to show a file — fails silently the
same way. The layer model (host / toolbox / sandbox, my-diary `Working in Sandboxes on Kinoite`) is
the diagnosis: *the error message never names the layer*, and this one names a missing binary
instead of a wrong direction.

---

### F146 · A script that resolves its own dependencies through `$HOME` is untestable — and degrades silently

*Measured 2026-09-14, building the `destructive-guard` PreToolUse reflex. Found by its own control,
twice, before the hook was installed.*

A guard's negative control has to plant a world: a fixture `HOME`, a fixture corpus map, a fixture
git repo — never the live one (Mistakes #39 is a control that measured the real vault). So the
control sets `HOME` to a tempdir and runs the hook. Two defects hid behind exactly that, and they
are the same defect wearing two coats.

**One — the loud one.** The wrapper located its own Python body as `"$HOME/.claude/hooks/…"`. Under
the fixture `HOME` that path does not exist, python exits non-zero, `|| exit 0` swallows it, and the
hook prints nothing. The control's case read **silent**, which is indistinguishable from "the rule
decided there was nothing to report".

**Two — the one worth the finding.** The body imports `strip_heredocs` from the arena:

```python
try:
    sys.path.insert(0, os.path.expanduser("~/fedora-arena/scripts/detectors"))
    from session_commands import strip_heredocs
    cmd = strip_heredocs(cmd)
except Exception:
    pass                      # ← fails open, as a guard should
```

`os.path.expanduser("~")` reads **`$HOME`**. Under the fixture home the import fails, the `except`
swallows it — correctly, by design, a broken guard must not break Bash — and the command is then
scanned **with its heredocs intact**. A `rm -rf <vault>` sitting inside a heredoc as prose was read
as a live deletion and the guard fired on it. Not a crash. Not a red. A *wrong verdict*, produced by
a fail-open path doing exactly what it was written to do.

**The fix is to take the two facts from somewhere the environment cannot move:**

```bash
SELFDIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)    # siblings: relative to THIS file
```
```python
home = pwd.getpwuid(os.getuid()).pw_dir     # the real home, from the passwd database, not $HOME
```

**Why this generalises past hooks.** `$HOME` is the most commonly *overridden* variable on this
machine — every podman sandbox, every `HOME=… ` prefix, every fixture, every container that mounts a
different home. Anything reached through it is a dependency on the caller's environment that the
code never declares and cannot verify. The combination that makes it invisible is specific and
common: **a path resolved from the environment, inside a `try`/`except` that fails open.** The first
makes it wrong; the second makes it quiet.

**The third thing the sweep caught, recorded because it is the same afternoon.** With all ten rules
covered and `cases=14/14`, a per-rule neuter sweep (each rule disabled in a *copy*, the control
required to go red) killed nine and left one standing: `Q3`, "a target that does not exist is
silent". Its fixture was a nonexistent path *outside* every corpus root — so it stayed quiet whether
Q3 worked or not, because Q1 and Q2 were doing the work. A case kept quiet by a **neighbouring**
rule is a false pass inside the control (F125b). Changing the fixture to a nonexistent path *inside*
a corpus root — one that would fire if it existed — made the tenth mutant die:

```
rules=10/10 cases=14/14 uncovered=0 orphan=0   verdict=PASS
neutered=10 killed=10 survived=0               verdict=PASS every rule is load-bearing
```

> **The transferable test**: for any case in a control, ask *which rule keeps this one quiet?* If
> more than one could, it measures nothing.

Related: [[60 Workflows/Mitigation Plan]] · [[60 Workflows/Claim-Time Guard]] ·
[[Insights Reports - Opening Them Past the Sandbox]] ·
[my-diary § Mistakes #39, #40](obsidian://open?vault=my-diary.vault&file=Reflections%2FMistakes%20I%20Made)

### F147 · A docstring that names the rule it satisfies is not the rule — and a world read from one directory reports nothing when it stops being one

*Measured on HEE-v2, 2026-09-14, on the round-2 fusion. Latent, not live: no run ever printed a wrong number, and the fix arrived with the change that would have exposed it.*

`scripts/mutants.py` decided which packages the workspace mutation sweep would cover:

```python
def workspace_crates() -> list[str]:
    """Every crate directory that is a real crate. The WORLD, not a list of it."""
    crates = ROOT / "crates"
    ...
```

The docstring asserts F65 compliance in so many words. The code is an include list of one
directory. It agreed with the world only because `Cargo.toml` happened to read
`members = ["crates/*"]`, and it answers the wrong question: *which crate directories exist*, not
*which packages does this workspace build*.

W8's CB-23 adds `members = ["crates/*", "tests/system"]` — a member outside that directory. Under
the old enumeration the sweep would have skipped it and said nothing: no refusal, no shortfall, a
normal-looking `crates=16/16` and a `PASS` over a world one package smaller than the workspace.
**A mutation score is a ratio whose denominator nobody prints twice.**

Two rules, and the first is the one my own standard did not yet name:

- **A comment claiming a property is not the property.** The line said "the WORLD, not a list of
  it" and was a list of it. Where a rule matters, the check reads the deciding artefact; where it
  cannot, the docstring states what it does NOT cover, never what it wishes it did. Grep your own
  detectors for the words "world", "every", "all" and ask each one what decides.
- **Take the denominator from the thing that decides, not from a convention that agrees with it
  today.** The fix reads cargo's own resolve (`cargo metadata` → member packages, which is also
  what `--package` takes), and degrades to the directory walk rather than to an empty world — a
  resolve that cannot be read must not silently become zero (F136).

**Who found it:** the unit that ADDED the member, in the same commit. Not the sweep, which cannot
see the gap by construction, and not a review of the sweep. That is the general shape: an include
list is discovered by whoever first falls outside it, which is why the cost lands on a later wave
and reads as that wave's problem.

**Mirror:** `~/CLAUDE.md` §3 (include list vs argued exclusion — this is the fifth instance, and
the first where the code claimed compliance in its own docstring) · F65 · F134 · F136.

---

### F148 · Six ways a corpus link or coverage measurement returns a confident false verdict

*Measured 2026-09-17 across a 748-note vault, a 985 MB codebase and a 736 MB generator. Each trap
produced a number I reported to a human before it was caught. Five of six ran in the direction of
finding more breakage than existed.*

| # | Trap | Wrong answer it gave | The fix |
|---|---|---|---|
| 1 | **Layer** — `ls` inside a toolbox on a `/var/home/<sibling>` path | "the codebase does not exist; 7,139 broken links" | check `/run/host<p>` and `flatpak-spawn --host` before concluding absence |
| 2 | **First match** — `re.search` answering a membership question | "14 of 64 return anchors are wrong" | `findall` + *is my target among them*, never *what is the first* |
| 3 | **Escaped pipe** — `[[A\|label]]` in a table yields target `A\` | "9,643 broken links" | `.rstrip('\\')` before resolving |
| 4 | **Fenced code** — `if [[ $x != /* ]]` is bash, not a wikilink | "1 live broken link" | strip ``` fences before parsing |
| 5 | **Declared stubs** — an empty file registered as a stub | "empty test files posing as tests" | check registry membership first |
| 6 | **Captured bytes** — snapshots preserved verbatim from other vaults | "1,039 cross-vault link defects" | split **live** notes from **captured** paths; captures are byte-preserved by protocol |

**Trap 3 is the expensive one and the least obvious.** Obsidian escapes the pipe inside markdown
tables, so a corpus that documents itself in tables — which any well-structured one does — fails
catastrophically under a naive `\[\[([^\]|#]+)` regex. The corrected figure was **38,649 links, 96%
resolved, and zero unresolved links in any live note**.

**The cross-check that would have stopped all six.** The corpus ships its own checker, and it read
`native_deadends: 0` while I was reporting thousands. *Two checkers disagreeing is a finding about
the checkers.* The one written sixty seconds ago is the suspect, not the one maintained for weeks.

```bash
python3 ~/.local/share/corpus-tools/layer-trace.py <root> [sibling_vaults…]
#   verdict=PASS live_cross_vault_defects=0   — all six traps handled
atuin scripts run layer-trace -v root=<root>
```

**Mechanised, so it cannot depend on memory** — `~/.claude/hooks/corpus-measure-guard.sh`
(`PreToolUse`, Bash) fires on the *shape* of the measurement before it runs: traps 2, 3 and 4
directly, and trap 6 whenever breakage is counted over a vault path. `cases=14/14`,
`neutered=7 killed=7 survived=0`. Trap 1 is `host-path-guard.sh`, `cases=11/11`,
`neutered=5 killed=5`. Both fired live the turn they were installed.

**atuin ground truth (18.12.1), found building the above:** templates are `{{ var }}` and **not**
`${var}` — a shell default silently becomes atuin's cwd, so a recon tool walked 1.9 TB and looked
like a hang. `atuin scripts delete` **prompts** (`yes | …`), and `atuin scripts new` on an existing
name **silently no-ops with rc=0**. Always re-read `atuin scripts get <name>` after registering.

Related: [[50 Field Notes/00 - Field Findings#F146 · A script that resolves its own dependencies through `$HOME` is untestable — and degrades silently|F146]] ·
[[60 Workflows/Entering an Unfamiliar Corpus]] · [[60 Workflows/Claim-Time Guard]] ·
[my-diary § Mistakes #46](obsidian://open?vault=my-diary.vault&file=Reflections%2FMistakes%20I%20Made)

---

### F149 · An anchor repairer must never rewrite a capture, and a `--fix` that cannot repair a class must not pass it

*Measured 2026-09-17. Two defects in the same file — `~/fedora-arena/scripts/audit/codeanchors.py` —
found by repairing damage the first one had already done.*

## 1 · `--fix` rewrote a byte-preserved capture

A `⚓ Code anchor` in `planning/.../sources/B14.md` was "repaired" from `procedure.rs:207` to `:284`.
The repair was **arithmetically correct** — the function really is at line 284 now — and **wrong
anyway**, because that file is a *capture*: a snapshot recording what was true at capture time. Its
twin in the vault, the integration ledger record and eight historical staged copies all still read
`207`. Rewriting it destroyed the only evidence of the captured state, made
`corpus-sync --check` fail (`Graph source inventory differs`), and cost a **full corpus republish**
to repair.

The rule already existed and was simply not implemented — the v3 Update Protocol states captures
*"retain routes to historical inputs without rewriting their captured bytes."*

**The fix is a declared exclusion list with a reason per entry, never a silent skip** (F65/F76/F81/F99
are the four times a silent include/exclude cost this habitat something):

```python
NO_FIX = (("/Atlas/sources/",  "captured source snapshots — byte-preserved by the Update Protocol"),
          ("/Atlas/evidence/", "retained verification evidence — a receipt is a historical record"),
          ("/Atlas/captures/", "capture records — provenance for the integration ledger"),
          ...)
```
and the withheld write is **loud**:
```
PROTECTED 1 drifted anchor(s) left unrewritten — captured source snapshots — byte-preserved …
verdict=FAIL vaults=9 notes_scanned=2902 anchors=112 broken=6 drifted=0 protected=2
```

**The subtlety that took a second pass:** protection was first computed only inside the `--fix`
branch, so a *plain* run still counted a deliberately-preserved capture as failing drift — meaning
`just doc-anchors` could never pass again. **A deliberate exclusion must be inert in every mode and
visible in all of them.** Protection is a property of the file, not of the run mode.

## 2 · `--fix` reported PASS over a defect it cannot repair

```
plain    rc=1  verdict=FAIL  ... broken=1 drifted=0
--fix    rc=0  verdict=PASS  ... broken=1 drifted=0     <- same line, contradicting itself
```

`--fix` only rewrites a drifted **line number**; a BROKEN anchor names a fragment the code no longer
contains, so there is no line to move to. The predicate was `FAIL if bad and not fix`, which passed
*any* finding whenever `--fix` was set. So `just doc-anchors-fix` exited 0 while notes made claims
the code did not support — a verdict contradicting a number printed beside it (Mistakes #28).

BROKEN now fails regardless of mode; protected drift never does, because leaving it is the declared
intent.

## Controlled, and proven to discriminate

```
selftest   checkers=21/21 cases=12/12 uncovered=0   verdict=PASS
new case   capture_kept=True live_fixed=True reported=True
neutered   `why = None`  ->  capture_kept=False     (the case fails, so it is load-bearing)
```
The case asserts **both halves**: the capture keeps its line *and* an ordinary note beside it is
still repaired. Asserting only the first would pass a checker that had stopped fixing anything.

**Left standing, deliberately:** `broken=6` across four habitat notes, every target a worktree
deleted after the W6/W7 work of 2026-09-06/07 (`hee-w6-resolution-20260906` ×3,
`hee-w7-contract-review-20260907`, `hee-w7-projection-reconciliation-20260907`,
`hee-cold-julia-qualification-20260907`). These pre-date this session. A BROKEN anchor means a note
describes something that no longer exists and must be **rewritten or retired** — a disposition for
whoever owns those notes, not a repair to make silently.

Related: [[50 Field Notes/00 - Field Findings#F148 · Six ways a corpus link or coverage measurement returns a confident false verdict|F148]] ·
[[60 Workflows/Entering an Unfamiliar Corpus]] · [[Code Anchors - Notes That Land on Source]] ·
[my-diary § Mistakes #46](obsidian://open?vault=my-diary.vault&file=Reflections%2FMistakes%20I%20Made)

---

### F150 · The graph was the wrong instrument: `anchors.json` answers module questions 1,100× faster

*Measured 2026-09-18 while practising end-to-end traversal of the HEE-v3 stack.*

## The finding

`corpus/anchors.json` — **1.6 MB, 9 ms** — carries every destination a `module:<id>` node has in
`graph.json` — **492 MB, ~10,000 ms** — already denormalised onto a 24-field record. For any
per-module question the graph is simply the wrong tool.

```
just module-brief <module>                       orientation, ~25 ms
module-brief.py <module> --code                  the full spec sheet, ~33 ms
all 22 spec sheets                               673 ms, 0 failures
```

## The second reason, learned the hard way: memory citizenship

Speed was the first argument. The second arrived on 2026-09-19, when **four background tasks were
killed for low memory** on a box running Chrome, Obsidian and three Claude agents — one of them a
Firstmate second mate mid-charter. Loading `graph.json` costs **~5–6 GB resident per load**, and I
had done it repeatedly while also mining 47,453 palace drawers.

Nothing was lost, but a re-index was killed mid-run and another agent's headroom was mine to spend.
On a shared machine the 1,100× figure is not only latency — **it is 5–6 GB you do not take from
somebody else's work.** Reach for the 1.6 MB index; the 492 MB graph is for questions that genuinely
need edges, and those should be batched into one load, not repeated.

## The highways, measured over all 22 modules

From a module node, **every scaffolding layer is one or two named hops away**. Do not breadth-first
search; take the relation.

| Destination | Relation | Coverage |
|---|---|---|
| cluster · tests · docs · tasks · gates · readiness · contracts · learnings · security | `declared_member` `planned_support` `delivered_by` `requires_gate` `applies_to_module` `governs_module_contract` `applies_learning` `requires_security_review` | 22/22 |
| source file | `planned_source` | **17/22** — five modules own a *directory* |
| vault stem | `specified_by` | 22/22 |
| public operations | `promises_operation` | **9/22** — the rest are mediated |

**The vault stem is the interchange.** Atlas, corpus and the 15 tracked diary notes are *all*
reached by the same two hops: `specified_by → portable_anchor`. Go to the stem first; one relation
then fans out to every other root.

**The build DAG is two tiers plus an island** — `contracts` (0 deps, 16 consumers) → 16 modules →
`app` (16 deps, 0 consumers), with `actions → {bash, pi_extension, skills, workflows}` below, and
`julia` carrying **zero build edges** while still owing a numerical IPC return. Undirected
`max=3 median=2`, 21 unreachable pairs — every one involving julia. *(An earlier draft of this
finding said "diameter 2". It was written before it was measured, and was wrong.)*

## The classifier bug that hid a whole layer

Graph file ids are `file:<root>/…` with root ∈ `{vault, atlas, codebase, diary}`. A classifier
testing `"vault/" in s` before an atlas branch never reaches it, because `file:vault/Atlas/x`
contains both. **Split on the root segment; never substring-match a path.** The symptom was an
entire layer scoring `-` for all 22 modules, which reads as a scaffolding gap rather than as an
instrument fault.

## Trap 7, and a lesson already on disk

`layer-trace` reported 11 cross-vault defects; **4 were not defects**. Inline code spans documenting
TOML table-array syntax — toolshed `10 Tools/herdr.md` describes herdr's plugin manifest as
"`[[build]]` · `[[panes]]` · `[[actions]]`" — parse as wikilinks. Generic single-word targets are
also exactly where a basename index collides, so the false positive arrives already wearing a
plausible destination. Strip fenced blocks **and** inline spans.

> A past instance had already written this down. my-diary `Mistakes I Made` contains, verbatim:
> *"It reported broken links for `[[startup]]`, `[[actions]]`, `[[array]]`."*
> **Search the diary before trusting a fresh finding.**

The remaining 7 were real and are now `obsidian://` URIs; all eight vaults read
`verdict=PASS live_cross_vault_defects=0`.

## Anchors: search by fragment, not by filename

Six anchors read BROKEN against deleted worktrees. Searching the surviving tree **by exact
fragment** changed two of six answers: `cold.sh`'s fragment was alive, and `MAX_QUEUE_BOUND` had been
**refactored** from `bounds.rs` into `hee-daemon/src/tasks.rs:115`. Both repointed; the other four
are marked retired *with the evidence that the fragment is absent tree-wide*. Retiring all six as
"deleted worktrees" would have destroyed two true claims. `codeanchors` now reads
`broken=0 drifted=0 protected=2`.

Related: [[50 Field Notes/00 - Field Findings#F148 · Six ways a corpus link or coverage measurement returns a confident false verdict|F148]] ·
[[50 Field Notes/00 - Field Findings#F149 · An anchor repairer must never rewrite a capture, and a `--fix` that cannot repair a class must not pass it|F149]] ·
[[60 Workflows/Entering an Unfamiliar Corpus]] · [[10 Tools/firstmate]] ·
[habitat § Session State and Resume](obsidian://open?vault=herdr-fedora-habitat.vault&file=00%20-%20Session%20State%20and%20Resume)

### F151 · A trailing comment on a literal's line swallows every entry after it — and the caption still says the entries are there

*Found 2026-09-22 by reading a run record's `environment` back, not by the run (which exited 0).*

## The finding

A dict literal in a Python runner held `"T07_CANCEL_EVIDENCE": …, "RUSTFLAGS": "-Dwarnings", "RUSTDOCFLAGS": "-Dwarnings",`
on one line. An edit inserted a note after the first entry as an end-of-line comment. Python accepted the file; the two
lint flags were now comment text; three "zero warnings" labels ran with no lint flags and printed green. The recorded
`environment` of each run had 20 keys and neither flag — the only instrument that could see it.

## The detector

`~/fedora-arena/scripts/detectors/d_comment_swallows_entries.py` (`COMMENT_SWALLOWS_ENTRIES`, build phase, W2): a comment
token whose text contains `"KEY": <value>` on a line whose code before the comment ends a live entry with a comma. Comments
are located with `tokenize`, not a quote regex — the first form masked the wrong `#` and its own negative control did not
trip; `just detect-verify` refused it, exactly as that contract was built to. Proven on the retained defective runner
(`front-debug-subject002/runner.py` line 60) and quiet on the fixed one. Not yet in the `lint-on-write` reflex, which is
syntax-only (`bash -n` / `ast.parse`); routing it there needs that reflex's control and quiet case extended.

## The rule it sharpens

A comment inside a literal goes on its own line. And every run record's `environment` is read back for the keys the
label claims — the pair that decides "zero warnings" is the pair to look for. F105 one level down: here the caption
was in the source, not in the report.

### F152 · `pgrep -f PAT | head -1` to FIND a pid returns THIS shell first — the kill-by-pattern rule has a second site

*Measured 2026-09-22 after `just detect-session` flagged ten of my own commands.*

## The measurement

With a sleeper deliberately launched at pid 3364690, from a shell at pid 3364688:

```
$ pgrep -f "sleep 300"
3364688      <- the shell running the pgrep: its command line contains the pattern BY CONSTRUCTION
3364690      <- the actual sleeper
3364691
```

`head -1` picks **3364688**. So `kill $(pgrep -f PAT | head -1)` kills the shell whenever the target
started *after* it. Ten such commands in one session did the right thing only because each target was
older than the shell and therefore had a lower pid — ordering, not correctness.

## Why the existing rule did not cover it

The standing rule is "kill by PID, never by pattern", and I read `pgrep -f` → `$P` → `kill $P` as
satisfying it: the kill takes a PID. It does not. **The self-match happens at the FIND step**, and
`head -1` then launders the wrong pid into a variable that looks like one I hold. Same family as F140:
the rule had two sites and the detector enumerated only one.

## What now fires

`d_pkill_self_match.py`'s claim-time rule (`PATTERN_KILL`, used by the `pattern-kill` reflex) now also
matches `pgrep` and `kill` on one line in either order, so both the variable form and the
command-substitution form warn where the command is written. Eight fire/quiet cases pass, the corpus
scan's negative control still trips, `just detect-verify` `verdict=PASS detectors=9`, `just reflex verify`
`reflexes=11 unproven=0` — with the reflex control extended to the new shape, so it is proven, not asserted.

## It is a MEASUREMENT hazard too, and it caught me twice in one hour

Minutes after recording the above I wrote `ps -eo cmd | grep -c 'corpus_sync.py'` as a final
all-clear check and read **4**. The honest listing — `ps -eo pid,etime,cmd | grep -F corpus_sync |
grep -v grep` — printed **nothing**: the real count was zero. The four were the grep pipeline's own
shell command lines, which contain the needle by construction. The habitat's own `hee-status` had
printed `publisher_processes=0` on the same machine at the same moment and was right.

So the rule is wider than killing: **any command that searches the process table for a string it
itself contains counts itself.** A bare `grep -c` over `ps` inflates silently and in the alarming
direction — it reports work still running when the machine is idle.

## The practice

Capture `$!` at launch and kill that. `(nohup cmd &)` in a subshell **discards** `$!` — use
`nohup cmd & echo $! > run.pid`. Where a pid must be recovered later, list first and read it
(`ps -eo pid,cmd | grep -F <needle> | grep -v grep`), never resolve-and-kill in one step. And for a
count, prefer the tool that already filters (`hee-status`) over an ad-hoc `grep -c` — or print the
rows and read them, so a self-match is visible rather than summed.

---

### F153 · A mutation kill is only a kill if the test that failed could see the mutant

**Measured 2026-09-22, HEE-v3, two independent `cargo-mutants` runs.**

Nine kills across two runs were produced by a test that cannot discriminate the mutant. Each
had the same shape: the `Test` phase failed at **~53 s** where a genuine kill in the same run
took **~87 s**, because the failure happened in the `--lib` phase and the integration suite
that would have discriminated never executed. The sole failing test was one of three:

* `store::staging_tests::callback_result_is_preserved_if_deadline_expires_after_effect`
* `app::durable_control::tests::boundary_authorizes_before_consuming_retained_or_queued_commands`
* `app::repair::tests::ordinary_owned_materialized_mode_is_replaced`

Six of the nine were in `cohort`, `context` and `notify` — modules those tests have no path
to, and which did not exist when the tests were written.

**The flakiness is load-dependent and does not reproduce serially.** Five clean
`cargo test --lib` runs on the unmutated tree: `161 passed; 0 failed` every time, ~19 s each.
Under `cargo-mutants -j 4` the same suite takes ~53 s — a 2.8x slowdown — and then it fails.

**Why it matters twice.** An unearned kill inflates the score, and it *hides a real gap*: the
mutant is filed as caught, so nobody writes the test that would have caught it. Proof that
these are unearned rather than merely suspicious: `read_frame`'s `> -> >=` was "caught" while
its behaviourally identical sibling `> -> ==` was **missed** in the same sweep — `take(4097)`
then `pop()` means `bytes.len()` can never exceed 4096, so both fire on exactly the same
input. Two identical mutants cannot honestly have different verdicts.

## The detector, and the rule that had to be thrown away first

`~/.local/share/corpus-tools/mutation-kill-audit.py <mutants.out>`

The **first** rule asked whether a failing test's name plausibly reached the mutated file.
Against a run whose three false kills were already known it flagged **24** — twenty-one false
positives, because integration tests legitimately kill mutants in files they are not named
after. That is the invisible failure: a gate with that rate is one the team routes around.

The rule that works is derived from the run's own distribution, not from an assumption about
which tests reach which files:

```
flag when  EVERY failing test is RARE (kills <= 4 mutants in this run)
     AND   the Test phase is FASTER than the 10th percentile of all kill durations
```

Both halves are load-bearing. Duration alone flags a genuinely quick kill; rarity alone flags
a sharp test that discriminates exactly one mutant. Together they say *the run stopped in an
early phase, and the thing that failed is not what kills anything else here.*

Control, with a known answer established independently by reading logs:
`T07/.../mutants-c3-shipped001-out` -> `flagged=3`, the three known ones, **0 false
positives**, correcting `87.3%` to `85.1%`. **Re-run that control after editing the tool; a
rule that stops finding those three is not this rule.**

> **Trigger.** Before quoting any mutation score: for each kill, ask which test failed and
> whether it could see the mutated code. A kill whose failing test lives in another module
> and whose run aborted in an earlier phase is a kill for the wrong reason. Same family as
> **F133** (a plant killed by the lint law), one level out: there the wrong *rule* killed it,
> here the wrong *test* did.

## Correction, same day — the statistical rule did not generalise, and the count hid it

The rule above (rare killers AND a fast Test phase) scored **3 of 3** on the run it was tuned
on and **1 of 12** on the next one. The second run had many small test targets, so its
legitimate single-purpose tests each killed few mutants and therefore read as "rare" — and
the real false kills sat at 55-58 s against a 58 s median, so the duration half said nothing
either. **A rule derived from one run's distribution is a rule about that distribution.**

It was caught only by reading the six flags rather than the count: `content_is_inert_bytes`
genuinely pins `Content::is_empty`, and `declared_bounds_are_the_enforced_bounds` genuinely
catches `64 * 1024` becoming `64 + 1024`. Five of six were legitimate kills; the twelve real
ones were not flagged at all.

**The rule that holds is structural, not statistical:**

```
flag a kill when EVERY failing test is a MODULE-QUALIFIED lib test
                 whose leading module segment is not the mutated file's module
```

A lib unit test is spelled `module::submodule::tests::name`; an integration test appears as a
bare function name. `store::staging_tests::...` cannot observe a mutant in `src/context.rs`
whatever the timings say. Scored on both runs at once: **T07 3/3 with 0 false positives, and
the six-module run 12/12** — all twelve traced to two flaky lib tests.

**Two controls, not one.** A single control cannot distinguish a rule from an overfit; the
second run is what exposed the first rule, and the tool's docstring now requires both to be
re-run after any edit. Total unearned kills found on 2026-09-22: **21**.

> **Trigger.** When a detector's rule is tuned on the data that motivated it, validate it on a
> second dataset of a different shape before trusting it. And read the flags, never the count:
> a detector with a plausible total can still be wrong about every entry.

### F154 · A bound that cuts a run is not a result, and the bound may not be the one you set

**Measured 2026-09-22.** A `cargo-mutants` run died twice at exactly **241 s** under two
different launch methods, which is what made it obviously not the `timeout 5700` wrapper. The
slice's `run-check.py` had been copied from **T09**, whose copy has no `mutants-` branch:

```python
if label.startswith("quality-"):   command_timeout = 1800 + 60
else:                              command_timeout = 240      # <- landed here
```

T07's copy carries the `mutants-` branch at 5400 s. The run completed **13 of 386** mutants
and recorded `timed_out: True`; quoting its `caught=12 missed=1` would have presented a 3%
sample as a score.

> **Trigger.** When a bounded run ends suspiciously early, read the bound **out of the harness
> copy in front of you**, not out of the one you remember. A helper copied between slices does
> not carry the branch you last used it for. And a run that reports `timed_out: True` has
> produced a sample, never a verdict.

### F155 · Every loop needs a budget — including the one inside the library

**Measured 2026-09-22.** Two mutants survived as `TIMEOUT` rather than as kills, and both
were the same defect in two places.

* `context::Assembly::assemble` bounded what it *selected* (`MAX_SELECTED`, `MAX_DEPTH`) but
  not the *walk*. Mutating the cursor arithmetic (`head += 1` -> `head *= 1`) hung the
  library. Fixed by giving the traversal its own step budget and a named refusal.
* The paging loop in a **test** had no budget, so a mutated `next` hung the case.

Both read as tooling problems rather than defects: `cargo-mutants` reports `TIMEOUT`, not a
killed mutant, and a hung test in CI reports nothing at all. This is **F102** confirmed in a
new place, and the addition is that it applies to library loops, not only test loops — the
terminating condition is the thing under test either way.

> **Trigger.** Any `while` whose progress depends on arithmetic: give it a budget, and assert
> on the budget with both numbers. If a mutation of that arithmetic would hang rather than
> fail, the loop is unbudgeted.

### F156 · `$!` after `setsid` is right exactly half the time — which is worse than wrong

**Measured 2026-09-22**, while building the negative control for a `supervise_bg` primitive. The
control asserted that `$!` after a detached launch is *not* the job's pid (F137's rule). **It
failed — the naive form was correct.**

```
setsid sleep 5 & echo $!          -> $!=2668727  cmdline='sleep 5 '     <- $! IS the job
setsid --fork sleep 5 & echo $!   -> $!=2668738  cmdline=<gone>          <- $! is setsid's
```

`setsid` forks **only when its caller is already a process-group leader** (`setsid -f/--fork` =
"always fork"). In a non-interactive shell a background child is not a group leader, so setsid
execs in place. With job control — an interactive shell — the child *is* a leader, setsid forks,
and `$!` names a process that has already exited.

So a watcher built on `$!` **passes every test in a script and reports a live job "gone" in an
interactive shell**. F137 recorded the incident correctly and the rule without its condition; the
condition is what makes it untestable in the place you test.

> **Trigger.** Any rule of the form "X is always Y" about process identity. Ask what X does when
> its caller's state differs. The fix is to remove the condition — have the child record its own
> `$$` before `exec` — not to accommodate it.

### F157 · A mutant that dies of `SyntaxError` is a survivor wearing a kill

**Measured 2026-09-22.** A control that neuters each rule of a detector in turn was written two
wrong ways before the third worked, and both wrong ways scored **green**.

1. **`level -> "OK"`.** For a site that only ever emits `OK`, the mutant is byte-identical to the
   original, so it cannot be killed. The control reported two survivors and blamed the test cases
   for an artefact of the operator.
2. **A regex over the source line** — `"(saw|need)": [^,}]+` — truncated every value spanning
   lines or containing a brace. Five mutants failed to import with `SyntaxError`, which reads as
   *killed* to anything checking only that the case failed. That is F133 in a new costume: a plant
   killed by the lint law is a kill for the wrong reason.

The working operator rewrites the **AST** (`ast.NodeTransformer` + `ast.unparse`) and the mutant
must still compile. CLAUDE.md already carried the rule in one line — *parse a declaration, never
regex it* (F140) — and it applies to mutating source, not only to reading it.

> **Trigger.** Writing a mutation operator. Ask two things: can this mutant be identical to the
> original for some site, and can it fail to *load*? Both score as kills and both are false.

### F158 · `claude --output-format json` returns an envelope, not the reply

**Measured 2026-09-22** against the installed binary. The obvious headless recipe —

```bash
claude -p "...output ONLY a JSON array..." --output-format json > review.json    # WRONG
```

— writes a **25-key cost report** (`result`, `is_error`, `session_id`, `total_cost_usd`, `usage`,
`num_turns`, `permission_denials`, …). The model's answer is a **string** inside `.result`:

```bash
claude -p "..." --allowedTools "Read,Grep" --output-format json | jq -r '.result' > review.json
jq -e 'type == "array"' review.json || echo "model did not return an array"
```

Also: the process **exits 0 on a turn that errored** — `.is_error` is the field that knows. A
downstream `jq '.[]'` over the envelope fails in a way that looks like the model misbehaved.

> **Trigger.** Any `--output-format json` on any CLI. Print the keys once before writing the
> pipeline around it. Docs lose to the installed binary.

### F159 · An anti-self-match process count that matched itself, through the substitution fork

**Measured 2026-09-22**, in a primitive written *that hour* to prevent exactly this class.
`count_procs` excluded its own shell and every **ancestor** of it. Live reading:

```
n=$(count_procs 'mempalace mine')    ->  1      # and the one match WAS the shell running it
```

`$(...)` forks a subshell before running the function. The fork **inherits the parent's argv
verbatim**, so `/proc/<fork>/cmdline` contains the pattern — and the fork is a **descendant**,
which walking upward never reaches. `$$` stays the parent's pid inside a subshell, so the fork is
not `$$` either.

**The unit test passed.** It called `count_procs "$tok"` directly, where no substitution fork
exists — it did not reproduce the **call shape** of real use. A test that exercises the function
but not the way the function is invoked is testing a different program.

The control needed the same care: written as an `exec`ing script it returns 0, because exec
replaces the image and the argv no longer carries the pattern. It only discriminates when the
naive version is a **sourced function invoked through `$( )`**.

> **Trigger.** Any "exclude myself" rule. Ask: what does `$(...)`, a pipeline element, or a
> `while read` subshell do to my argv? Exclude by **process tree membership** — walk each
> candidate's ancestry and test whether it meets yours — not by an ancestor set.

### F160 · `awk '{print $4}' /proc/$pid/stat` returns the STATE field, not the ppid

**Measured 2026-09-22** on this machine, live:

```
pid=1545  comm='(mt76-tx phy0)'   awk $4 = 'S'    true ppid = 2
```

`/proc/pid/stat` is `pid (comm) state ppid …`, and **comm is unquoted and may contain spaces and
parens**. A kernel worker named after a wireless phy shifts every field by one, so `$4` lands on
the single-letter state. The failure is `[: S: integer expected` in the lucky case and a wrong
parent in the unlucky one.

```bash
_ppid() { awk '{ n=index($0,") "); x=substr($0,n+2); split(x,a," "); print a[2] }' "/proc/$1/stat"; }
```

Take everything after the **last** `") "` — comm is the only field that can contain one — then
ppid is field 2 of the remainder. Treat a non-numeric result as a **stop**, never as a guess.

> **Trigger.** Any positional parse of a kernel or tool file. The schema being positional does not
> mean the positions are where they look. Same family as F140 — *parse a declaration, never regex
> it* — in a place with no declaration in sight.

---

### F161

**`CARGO_TARGET_DIR` set for a `cargo-mutants` run makes every mutant link against the
unmutated library, and the run reports `Test Success` for mutants that kill 21 tests.**

*2026-09-22, HEE-v3 shard B.* A 271-mutant run reported two survivors in `Cohort::join`:
`delete ! in` at `src/cohort.rs:860` and `:863`. Planting the first one by hand in the same
frozen subject failed **21 of 57** cases in `tests/t22_cohort.rs`. cargo-mutants' own record
showed the right command and `Test Success`:

```
Build  Success  cargo test --no-run --verbose --package=…
Test   Success  cargo test --verbose --package=… --lib --test t11_context --test t22_cohort …
```

The cause was in the environment I had exported around the run:

```bash
export CARGO_TARGET_DIR=$HOME/.cache/hee3-shardb-target   # <- this
export TMPDIR=$HOME/.cache/hee3-shardb-tmp                # <- fine, and necessary
```

cargo-mutants copies the tree per worker and mutates the copy. With one shared target
directory every copy resolves to the same cached artifacts, so a mutant's test binary can be
linked from a build of the **unmutated** library. The mutation is present in the source and
absent from the binary, and the tool reports exactly what it observed: the tests passed.

**This is F118 recurring from the other side.** F118 says `just mutants` owns its own scratch
and unsets `CARGO_TARGET_DIR` itself. I knew the rule, set the variable by hand for a run that
did not go through `just`, and spent an hour measuring nothing. The habitat's build rule —
*"every cargo invocation on a repo under `/var/mnt/STORAGE-10TB` runs with
`CARGO_TARGET_DIR=$HOME/.cache/…`"* — is about the **spindle**, and it does not extend to
cargo-mutants, which needs its copies isolated. Two rules, one variable, opposite directions.

> **The tell, and it is cheap.** A `MissedMutant` whose neuter you can reason about should be
> plantable by hand. Before trusting a survivor list, take one entry, apply it to the subject,
> and run the scoped test command. If the plant goes red while the tool said `Test Success`,
> the run measured the wrong binary and **every** number in it is void — not just the
> survivors, because a caught mutant may have been caught by a stale binary too.
>
> The precheck costs one compile and licenses the whole run:
> ```bash
> cd "$SUBJECT" && sed -i '860s/if !unmet/if unmet/' src/cohort.rs
> unset CARGO_TARGET_DIR; cargo test --test t22_cohort   # must be RED
> ```
>
> **Trigger.** Any `cargo-mutants` invocation not made through the recipe that owns its
> scratch. Unset `CARGO_TARGET_DIR` in the runner script itself, next to the comment saying
> why, rather than relying on the caller's environment being clean — a rule that lives in the
> caller is a rule the next caller does not have.

---

### F162

**A command substitution in the argument list consumes `$?` before it is expanded, so a
status-reporting `printf` prints the wrong command's status.**

*2026-09-22, reporting a sweep of six Python suites.* The loop read:

```bash
python3 -W error "$f" > "$S/py.log" 2>&1
printf "  %-28s rc=%s  %s\n" "$(basename $f)" "$?" "$(tail -1 $S/py.log | head -c 62)"
```

It printed `bash_wrapper.py rc=0` for a suite that was exiting **1** with **54 errors**. The
word expansions run left to right: `$(basename $f)` executes first and sets `$?` to
`basename`'s status, and only then does `"$?"` expand. The status being reported is destroyed
by the act of formatting the report.

The tell was internal contradiction, not the exit code — `rc=0` beside `errors=54` in the same
line. Without that second field the run would have read clean.

This is not the pipe case (`PIPE_SWALLOWS_VERDICT`, F-series on `cmd | tail`), and the pipe
detector does not fire on it: there is no pipeline whose last element wins. It is the **same
harm through a different mechanism** — a reporting construct that runs a command between the
subject and the read of its status.

> **The fix, and it generalises.** Capture the status into a variable on the line after the
> command, before anything else runs:
> ```bash
> run() {
>     local name=$1; shift
>     "$@" > "$S/step.log" 2>&1
>     local rc=$?                      # nothing has run in between
>     local line; line=$(tail -1 "$S/step.log")
>     printf "  %-26s rc=%s  %s\n" "$name" "$rc" "$line"
>     return $rc                       # so an aggregate can collect it
> }
> ```
> **Trigger.** Any `$?` that is not the first thing after the command whose status it names —
> including inside `printf`, `echo`, `[ ]` and a here-doc. If a substitution, a `local`
> assignment with a command, or another builtin sits between them, the value is already gone.
>
> The `return $rc` matters as much as the capture: an aggregate that prints fifteen verdicts
> and leaves the reader to `and` them together is how a red line becomes scenery.

### F163 · A `/proc/<pid>/stat` read on a descriptor opened while the process lived returns `ESRCH`

**A census that lists `/proc`, opens each `stat` and then reads it has TWO gone-process
windows, and the second one is not `ENOENT`.** A process that exits after the `open`
succeeds makes the `read` fail with `ESRCH` ("No such process", errno 3). Code that skips
`ENOENT` at the open and maps every other failure to "I/O error" reports an unobserved
census whenever *any* process on the machine exits in that window.

*2026-09-23, HEE-v3 `src/worker/process.rs`.* The process-group census did exactly that. The
symptom was `t08_contract` failing about one run in four under load — on a *different* case
each time (T08C-06, -08, -19), each returning `Error::Process` where `Response`/`Json` was
expected. Instrumenting the four `WaitError` sources, then the census's I/O branches, named it
on the second loop: `DEBUG-CENSUS read Os { code: 3, … "No such process" }`. The exchange had
exited 0 with every other flag clean.

> **The fix, and the trigger.** Treat `ENOENT` at the open and `ESRCH` at the open *or the
> read* as "gone, not a member", and keep every other errno as a failed census. Put the
> decision in a pure function of the errno so it is reachable by argument (F95) —
> `exited_during_census(raw_os_error)`. Measured: 5 failures in 21 direct runs before, 0 in 30
> after. **Trigger:** any open-then-read of a `/proc/<pid>/…` file inside a loop over
> processes you do not own.

A failure that moves between test cases is a shared mechanism, not a flaky test: the case
that fails is whichever one's exchange lost the race.

### F164 · Under a child subreaper, a DEAD orphan still counts as your child until you reap it

**`PR_SET_CHILD_SUBREAPER` re-parents every orphaned descendant to the subreaper, and an
orphan that has already exited sits there as a zombie — listed in
`/proc/self/task/<tid>/children` — until the subreaper waits for it.** A gate that runs each
step as a subreaper and flags "descendants detected" therefore fires on a test suite that
kills process trees *correctly*: when a parent dies before its child, the child is orphaned
upward even though it then dies too.

*2026-09-23, HEE-v3 `tools/check-quality` running `tests/bash_wrapper.py`.* The suite passed
115/115 and exited 0; the step was refused with `descendants_detected: True`. A marker in the
environment found **no survivors** one second after exit — every orphan was dead. The gate
was right to refuse: custody of those processes had passed to it.

> **The fix.** A suite that kills trees must be its own subreaper: `prctl(PR_SET_CHILD_SUBREAPER,
> 1)` at start, and after each case reap adopted zombies and **fail the case on any adopted
> descendant still alive** after a short grace (a process mid-exit is briefly not yet `Z`).
> Register that cleanup FIRST in `setUp` so it runs LAST — after every `Popen` has collected
> its own child — or `waitpid` steals a status a test is still waiting on. Control: a shell
> that backgrounds `sleep 30` and exits must fail the reap, naming the pid.

### F165 · `corpus_sync.py` after another session edits a generated note mid-publication — the recovery that preserves the edit

**The publisher refuses twice, correctly, and neither `--resume` nor a plain rerun gets past it.**
Apply stops per file with *"Concurrent edit or missing prior target: <file>"* and leaves the marker
`pending` with thousands of entries already written (6,185 of 9,198 here). A rerun then stops at
preflight with *"Generated note has an authored edit; reconcile it before regeneration: <note>"*,
and `--resume` would replay a frozen journal whose `before_sha256` the edited file no longer has.

*2026-09-23 night, HEE-v3.* Another session changed one line in two Master Index notes one second
apart while a publication was between staging and apply — the line was emitted by the generator, so
the edit landed on the **projection**, not its owner.

> **The recovery (each step measured before the next):**
> 1. Find the owner: `grep -rl "<changed text>"` in the planning root — here `navigation_catalogue.json`.
> 2. Mirror the edit into the owner, changing only that string; confirm nothing pins the owner's own digest.
> 3. Prove the projection's manifest bytes differ from the edited file **only** by that edit
>    (`generated-manifest.json` digest == the pending journal's `before_sha256`, blob present and verified).
> 4. Keep a copy of the edited file, restore the projection from the verified journal blob.
> 5. `corpus_sync.py --preflight` (changes nothing) → `--verify-tooling` (the owner is a maintenance
>    subject, so the receipt goes stale) → publish → `--check`.
>
> The edit survives because the next generation regenerates it from the owner. **Trigger:** either
> refusal naming a file you did not touch. Never force-overwrite the projection to clear it — the
> refusal's own guidance: *"Preserve the edit, identify the owning source and reconcile."*

### F166 · A `.*` regex over the HEE-v3 Graphify graph is quadratic — the file is ONE 782 MB line

**`ugrep -G -rln 'numerical.*worker::process\|…' corpus docs` held a full core for 5 h+ and never
finished.** `corpus/graphify-out/graph.json` is a single line (measured 2026-09-24: `1 lines, longest
782022479 bytes`). A line-oriented engine matches `a.*b` per line, so every occurrence of `a` rescans to
the end of a 782 MB line — quadratic in the file, not linear. `-l` does not help: it stops at the first
*match*, and a pattern whose tail is absent never matches.

*2026-09-23/24, HEE-v3.* An earlier session's orphaned search; it also shared the host with a publication
that was already I/O-starved. It exited on its own before it could be killed.

> **Rule:** never run a regex with `.*`, or any unanchored alternation, recursively over `corpus/` without
> excluding `graphify-out/`. Ask the graph through `corpus/anchors.json` (see memory `hee-v3-traversal`,
> 1,100× faster) or `jq` on the parsed JSON. For plain text use a fixed string (`ugrep -F` / `rg -F`), which
> is linear. **Trigger:** a search over `corpus` still running after a minute. **Denominator check:** `awk
> '{ if (length($0)>m) m=length($0) } END { print NR, m }' <file>` before regexing any file over ~100 MB.

### F167 · A non-blocking `flock` in a multi-threaded process refuses spuriously while ANY thread forks

**`tests/t07_startup.rs` failed 3 of 20 runs with `Store(Locked)` at three different call sites, and 0 of 20
with `RUST_TEST_THREADS=1`.** The HEE-v3 store takes its single-writer lock with `File::try_lock` (a
non-blocking `flock`) on a descriptor opened `O_CLOEXEC`. Close-on-exec acts only at *exec*: a `fork` on any
other thread — here another test spawning a child through `std::process::Command` — duplicates every
descriptor, and `flock` belongs to the open file description, so for the fork-to-exec window the child
holds this store's lock too. The next non-blocking acquisition in that window fails.

*2026-09-24, HEE-v3* (measured on `91492c8`). The same exposure exists in production: a multi-threaded
engine that spawns workers while reopening its store.

> **Fix (applied in `src/store/artifact.rs`):** retry "would block" for a short settle window
> (`store::LOCK_SETTLE` = 250 ms, never past the caller's deadline) — long enough for a fork-to-exec
> window under load, short enough that a genuine duplicate start still refuses fast. And map only
> `WouldBlock` to `Locked`; every other lock failure is the real I/O error. Measured after: 0 of 40
> multi-threaded. **Trigger:** an intermittent "locked/busy" failure that disappears single-threaded.
> OFD locks (`F_OFD_SETLK`) do not help — they are also per open file description.

### F168 · `sed 's|old|new|'` breaks on Markdown tables: the delimiter is in the text

**Twice in one session (HEE v4 planning, 2026-10-01), a `sed` replacement with `|` as its delimiter ran on Markdown table rows that contain `|`.** The first unescaped `|` in the pattern or replacement ended the expression early. One run errored. The other run "succeeded" and left garbled text (a doubled backtick before `git show`) in three files, found hours later by a review (v4 gap review G21, repaired by R12).

> **Rule:** never use `sed` for a replacement whose text can contain the delimiter, which means any Markdown table, path or regex. Use the Edit tool (exact string, unique match), or Python with `assert s.count(old) == 1` before `s.replace(old, new)`. If `sed` is unavoidable, choose a delimiter absent from both sides and assert that first. **Trigger:** a replacement in a `.md` file with `|` anywhere in the old or new text.

### F169 · `tursodb` 0.7.2: `--mcp --readonly` protects only the startup file; `foreign_key_check` gives a false pass; FTS needs a flag

All three measured 2026-10-01 while building the HEE v4 ops database. The MCP item was reproduced twice, independently.
- **MCP.** `tursodb --mcp --readonly a.db` refuses `delete_data` on `a.db`. But the MCP tool `open_database {path: b.db}` opens **another file read-write**: `delete_data "DELETE FROM t"` then printed "DELETE successful." and `b.db` went from 3 rows to 0. The read-only flag binds the startup connection, not the server.
- **`PRAGMA foreign_key_check`** returns nothing (rc=0) on a planted violation. Run it through Python `sqlite3` instead.
- **FTS** (the Tantivy kind) needs `--experimental-index-method`, which the docs do not mention, and is refused under `--readonly`.

> **Rule:** never expose `tursodb --mcp` on a real database unconfined. Serve a read-only snapshot inside `bwrap` (as `hee4db mcp` does). Never trust a `tursodb` FK check that prints nothing. **Trigger:** any plan to give an agent MCP access to a database file. Detail: [turso.vault Operational Database](obsidian://open?vault=turso.vault&file=50%20Agent%20Knowledge%20System%2FOperational%20Database) § 2026-10-01 · memory `tursodb-mcp-readonly-not-boundary`.

### F170 · Is a patch applied? `git apply --check` both ways answers it read-only, and the third answer matters

Measured 2026-10-02 (HEE v4 V4-74) on 13 staged Jev diffs against the live tree, from plain directories (no repository needed):
- `git apply --check D` rc=0 → **NOT applied** (it would apply);
- `git apply -R --check D` rc=0 → **APPLIED** (it would reverse cleanly);
- **both fail → CONFLICT**: the file moved on since the patch. Here: round-6 `jev-verify-claim.diff` after a later edit at its context line `:297`. That file's documented undo (`git apply -R`) no longer worked.
Neither form writes anything. The measurement showed that seven round-6 steps a note called "waiting to be applied" were already live.

> **Rule:** before applying, re-applying or undoing a staged patch, measure both directions and act on the answer, never on a note's status line. A CONFLICT means the undo for that patch is broken: keep a whole-file backup and restore script for every install. **Trigger:** any "staged, not installed" claim, or any edit to a file a recorded patch touches.

