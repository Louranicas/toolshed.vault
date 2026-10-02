---
tags: [toolshed, factory, fabric, adoption, evidence]
created: 2026-09-05
status: Arena qualification complete; production adoption proposed
---

# Factory Roster Expansion - DevOps Toolbox

Parent: [[00 - Toolshed Index]]  
Related: [[Runbooks]] · [[Shape-Directed Tool Chaining]]

Cross-vault: [Habitat workspace placement](obsidian://open?vault=herdr-fedora-habitat.vault&file=70%20Toolchain%2FFactory%20Roster%20Expansion%20-%20Workspaces%206%20and%207) ⇄ [Fabric capability adoption](obsidian://open?vault=fedora-fabric.vault&file=04%20Workflows%2FFabric%20Factory%20Capability%20Adoption).

Full assessment and dependency/decision ledger: [Arena plan](file:///var/home/Louranicas/fedora-arena/experiments/factory-roster-20260905/plan/PLAN_factory_roster.md). [Offline HTML](file:///var/home/Louranicas/fedora-arena/experiments/factory-roster-20260905/plan/PLAN_factory_roster.html) is structurally checked; browser visual QA is unverified.

## Recommendation

Add capabilities that close acceptance, release and recovery gaps. Retain the existing sixteen-service W1–W5 roster. Reserve W6 for delivery/release assurance and W7 for operations/recovery; these two tabs have **not** been created.

| Placement | Capability | Current evidence |
|---|---|---|
| W1 | Fabric + yt-dlp | Four public transcripts extracted, no model calls; dependency installed only in Arena |
| W2 | ShellCheck | Arena scripts clean; SC2086 negative control detected |
| W5 | Hurl | Three-request contract passed; degraded HTTP 200, wrong version and unavailable transport rejected |
| Proposed W7 | Restic | One synthetic file backed up, checked, restored, tamper detected and restored again; wrong password refused |

The three executables are SHA256-pinned under `fedora-arena/experiments/factory-roster-20260905/tools/`. No global PATH/profile change. This is fixture evidence, not application or off-host recovery. Hurl emits a Fedora libcurl symbol-version warning despite passing the bounded test; qualify a native package/build before production adoption.

```bash
just --justfile /var/home/Louranicas/fedora-arena/experiments/factory-roster-20260905/justfile verify
habitat-runbook run factory-roster-lab
```

Both execute the same Arena verifier and retain separate child receipts plus a twelve-check aggregate. The runbook was actually run successfully. They do not deploy software or modify the cockpit.

## Next candidates

- W2: mise for project-local tool versions, Hadolint for container inputs; OpenSpec as a scoped specification/change-delta pilot alongside Planwright.
- W5: Posting for optional human API exploration; Playwright when a real UI product needs browser acceptance.
- W6: Dagu trial around existing runbooks; Trivy for artifact/SBOM policy; Cosign with an explicit signing identity; SOPS after key-custody choices.
- W7: Dozzle for optional live container-log inspection; OpenTelemetry Collector plus a separately chosen storage/retention backend; Restic with real off-host and application-consistent restore tests.

Compare Babysitter's agent orchestration against existing HEE ownership; do not casually add another scheduler. Dagger's current Podman documentation requires rootful execution, so it is not a drop-in fit for the rootless habitat. RustFS and NetBird are deferred until object storage and remote workers are concrete requirements.

## Source and evidence boundary

Reviewed Omer's [DevOps Toolbox](https://www.youtube.com/@devopstoolbox), nine original descriptions, twenty-one repository metadata records, and four Fabric-extracted transcripts. The channel highlighted Posting, OpenSpec, Babysitter and Dozzle; Hurl, ShellCheck, Restic and the release tooling are supplementary recommendations. Source snapshots and source hashes are retained in the Arena plan.

Use the plan's dependency graph to qualify one real service next. Tool availability is not activation; documentation is not a passing deployment; model advice is not verdict authority.
