---
tags: [toolshed, tool, workspace-3, github]
tool: gh-dash (gh extension) + gh CLI
version: gh-dash v4.25.2
upstream: https://github.com/dlvhdr/gh-dash
workspace: W3 · pane w1:pM
agent_door: habitat q gh-dash <gh args>   (gh pr/issue/api --json)
---

# gh-dash + gh — the GitHub surface

gh-dash is a configurable **PR/issue dashboard**; `gh` underneath is the complete GitHub API client. Authenticated here as **Louranicas** (device flow, 2026-09-01). Live: 12 own PRs · 9 needing review.

## gh-dash keys

`s` switch section · `Tab` PRs ⇄ Issues · `Enter`/`o` preview / open in browser · `d` diff · `c` checkout locally · `v` approve · `m` merge · `/` filter (GitHub search syntax) · `r` refresh · `?` help · `q` quit.

Config `~/.config/gh-dash/config.yml` — sections *are* GitHub search queries:

```yaml
prSections:
  - title: My PRs
    filters: is:open author:@me
  - title: Needs my review
    filters: is:open review-requested:@me
issuesSections:
  - title: Assigned
    filters: is:open assignee:@me
defaults:
  preview: {open: true, width: 60}
  refetchIntervalMinutes: 30
```

## `gh` — the agent door (this is the powerful half)

```bash
gh pr list --json number,title,author,statusCheckRollup --limit 20
gh pr view 123 --json body,files,reviews,comments
gh pr checks 123 --json name,state,link          # CI status
gh pr diff 123  ·  gh pr create --fill  ·  gh pr review --approve
gh issue list --json number,title,labels --search "is:open label:bug"
gh run list --json databaseId,status,conclusion  ·  gh run view <id> --log-failed  ⭐
gh api repos/{owner}/{repo}/commits --paginate --jq '.[].sha'
gh api graphql -f query='...'                    # full GraphQL
gh search prs/issues/repos/code "<query>" --json ...
gh release list · gh workflow list · gh cache list · gh secret list
gh extension list/install/upgrade
```

**`--json` + `--jq` on nearly every command** is what makes gh scriptable. `gh run view --log-failed` is the fastest path from "CI is red" to the actual failing lines. `gh api --paginate` reaches anything the REST/GraphQL API exposes.

## Chains

**Feeds from:** [[lazygit]] (push) → PR. **Feeds into:** [[jqp]]/[[nushell]] (`--json` output), [[tuicr]] (`:submit` posts a review), reviewr's PR tab.
**Division:** gh-dash is your radar — you spot a PR and hand me the number; I use `gh` directly.

Related: [[lazygit]] · [[tuicr]] · [[jqp]] · [[Workflow Recipes]] · [[00 - Toolshed Index]] ·
[[Command Matrix]] · [[Tool Clusters]]
