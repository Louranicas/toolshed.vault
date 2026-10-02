---
tags: [herdr, ghostty, kinoite, keybindings, memory]
created: 2026-09-06
updated: 2026-09-06
status: user-confirmed-working
---

# Herdr persistent tab navigation — Ctrl+Alt+End then Left/Right

**Press Ctrl+Alt+End, release, then press Left/Right repeatedly to select Herdr tabs.** Entry advances one tab. **Enter**, **Escape**, or **Ctrl+Alt+End** again exits navigation mode. Bare arrows retain normal behavior outside this mode. Use this shortcut in the Ghostty surface running Herdr.

User confirmed on 2026-09-06: “great work I can confirm is working WELL DONE!”

This supersedes the earlier prefix-only workaround and the claim that this keyboard-entry behavior requires a Herdr source patch. Ghostty's persistent `herdr_tabs` key table provides it through configuration. It does not create a mouse-focused native Herdr tab-bar widget.

## Applied configuration

Ghostty `~/.config/ghostty/config`:

```ini
keybind = ctrl+alt+end=csi:110;7u
keybind = chain=activate_key_table:herdr_tabs
keybind = herdr_tabs/left=csi:112;7u
keybind = herdr_tabs/right=csi:110;7u
keybind = herdr_tabs/enter=deactivate_key_table
keybind = herdr_tabs/escape=deactivate_key_table
keybind = herdr_tabs/ctrl+alt+end=deactivate_key_table
```

Herdr `~/.config/herdr/config.toml`:

```toml
[keys]
previous_tab = ["prefix+p", "prefix+left", "ctrl+alt+p"]
next_tab = ["prefix+n", "ctrl+alt+n", "prefix+right"]
```

The Left/Right table bindings emit CSI sequences for Ctrl+Alt+P/N, which select Herdr tabs in the current workspace with native wrapping. They do not invoke Ghostty's outer-tab actions. Other existing configuration and plugin bindings were preserved. The table is activated on the current Ghostty terminal surface; use the configured exit keys before returning to pane editing. Modified arrow keys retain their separately configured actions.

## Verification and evidence

- Installed versions recorded: Ghostty 1.3.1-4.fc44; Herdr 0.8.2.
- Both native configuration validators passed.
- `ghostty +list-keybinds` included table activation, both arrow mappings and all exits.
- Herdr reported its live reload applied with no diagnostics.
- `systemctl --user reload app-com.mitchellh.ghostty.service` completed successfully on the host.
- The user confirmed the requested physical keyboard behavior works. The agent did not inject keys; individual exit paths were not separately confirmed.
- Live configuration hashes matched the verified setup when this note was saved.

[Detailed receipt](evidence/receipt.json) · [Ghostty applied config](evidence/ghostty.after.conf) · [Herdr applied config](evidence/herdr.after.toml).

## Rollback and preservation

Backups before persistent navigation: [Ghostty](evidence/ghostty.before.conf) · [Herdr](evidence/herdr.before.toml). These retain the earlier one-step Ctrl+Alt+End shortcut and prefix-arrow alternatives.

To remove only persistent navigation, remove the `chain=activate_key_table:herdr_tabs` line and all `herdr_tabs/` entries from Ghostty. Remove only `ctrl+alt+p` from Herdr's `previous_tab` array. Keep other bindings and later unrelated changes. Validate both configurations, reload Herdr using `herdr server reload-config`, and reload Ghostty using its Ctrl+Shift+Comma shortcut or its documented systemd reload. Full backup replacement is appropriate only after checking for later changes. No server/pane restart is needed.

## Recall and related notes

Recall phrases: **Herdr persistent tab navigation**, **Ctrl+Alt+End Left Right**, **herdr_tabs**. The active configuration and current user instructions take precedence over recalled records if this setup changes.

[Habitat Keybindings](obsidian://open?vault=herdr-fedora-habitat.vault&file=20%20Usage%2FKeybindings) ⇄ this reference · [[00 - Toolshed Index]] · [Initial shortcut history](../README.md).

Sources: [Ghostty key tables](https://ghostty.org/docs/config/reference#keybind), [Ghostty live reload](https://ghostty.org/docs/linux/systemd).
