---
tags: [herdr, ghostty, kinoite, keybindings, reference]
created: 2026-09-06
author: SOL3
status: configured-and-reloaded
---

# Herdr Ctrl+Alt+End — 2026-09-06

> [!success] Current confirmed procedure — persistent tab navigation
> Press **Ctrl+Alt+End**, release, then use **Left/Right repeatedly** through Herdr tabs. Enter/Escape exits. The user confirmed it works on 2026-09-06. See [the current procedure and evidence](persistent-navigation/README.md).
>
> The one-step configuration and verification notes below are historical and predate the persistent key table.

**Hold Ctrl+Alt and press End to advance to the next Herdr tab**, wrapping from last to first
within the current workspace. “Next tab” was the stated working interpretation of the request.
The existing Ctrl+B, then N binding is retained. This concerns the inner Herdr tab row, not
Ghostty's outer tabs.

Environment: Fedora Kinoite → Ghostty → Fedora Toolbx → Herdr 0.8.2, default socket
`~/.config/herdr/herdr.sock`. The active `herdr-habitat` workspace had 13 tabs and 34 panes;
the other workspace had one tab/pane. These counts remained present after reload.

## Applied configuration

In `~/.config/ghostty/config`:

```ini
keybind = ctrl+alt+end=csi:110;7u
```

In `~/.config/herdr/config.toml`, before the existing command tables:

```toml
[keys]
next_tab = ["prefix+n", "ctrl+alt+n"]
```

Ghostty's CSI action prepends `ESC [` to the configured sequence. Here the payload represents
Ctrl+Alt+N, which Herdr accepts as a direct next-tab chord. The initial native `ctrl+alt+end`
candidate failed `herdr config check` and was restored before reload; the installed keybinding
parser omits End even though other input code recognises End key events.
[Ghostty action reference](https://ghostty.org/docs/config/keybind/reference),
[Herdr keybinding configuration](https://herdr.dev/docs/configuration/#keybindings).

The translation applies across Ghostty terminal surfaces. In a plain shell or another foreground
TUI, the chord sends Ctrl+Alt+N rather than invoking a Herdr tab action. Ctrl+Alt+N also works
directly inside Herdr. Herdr's setting is shared across workspaces using this configuration.

## Verification

- Native End candidate rejected and rolled back: [native-attempt.json](native-attempt.json).
- Compatible Herdr config validated; live reload returned `status: applied`, `diagnostics: []`.
- Ghostty candidate and saved config validated; running GTK `reload-config` action acknowledged.
- `ghostty +list-keybinds` reports exactly `ctrl+alt+end=csi:110;7u`.
- Parsed Herdr comparison shows other settings and existing plugin bindings unchanged.
- No server/pane restart, shell command injection, or physical keyboard test was performed.

Receipts: [compatibility-result.json](compatibility-result.json) · [verification.json](verification.json).
The checks establish valid configuration and reload acknowledgements; they do not claim a witnessed
physical-keyboard-to-GUI tab transition.

## Backups and rollback

Original files are saved alongside the active configurations:

```text
~/.config/herdr/config.toml.before-ctrl-alt-end-20260906
~/.config/ghostty/config.before-ctrl-alt-end-20260906
```

This bundle also contains [herdr.before.toml](herdr.before.toml), [herdr.after.toml](herdr.after.toml),
[ghostty.before.conf](ghostty.before.conf) and [ghostty.after.conf](ghostty.after.conf).

To undo only this change, remove the Ghostty translation line and remove `ctrl+alt+n` from
Herdr's `next_tab` array. If the array is still exactly the one shown above, removing that override
restores the built-in next-tab default. Preserve later unrelated edits.

Validate Herdr with `herdr config check`, then apply using `herdr server reload-config`. Validate
Ghostty from Toolbx with `flatpak-spawn --host ghostty +validate-config`, then use Ghostty's existing
Ctrl+Shift+Comma reload shortcut. Full backup replacement is suitable only when no later edits need
preserving. Neither rollback route needs a server restart.

Related: [[10 Tools/herdr|Herdr reference]] · [[00 - Toolshed Index]].
