---
tags: [toolshed, reference, catalogue, cascade, runbook]
source_set_sha256: 13c6804b969dba9f3889bb9d2efd867185a42ed70a3f1e52de7841593d51da7f
---

# Cascade & Runbook Catalogue

**Generated source snapshot, not an execution receipt.** It becomes stale when a source changes.
Regenerate with `python3 ~/fedora-arena/scripts/audit/catalogue.py` after reviewing source changes.
`python3 ~/fedora-arena/scripts/audit/catalogue.py --check` compares the complete current inventory
and rendered note without writing or executing procedures.

## Cascades

| name | shape | stages | workspaces | receipts declared | verdict declared |
|---|---|---|---|---|---|
| [assimilation](file:///var/home/Louranicas/fedora-arena/cascades/assimilation.toml) | DAG | 7 | W1 W2 W3 W4 W5 | yes | yes |
| [clusterweb](file:///var/home/Louranicas/fedora-arena/cascades/clusterweb.toml) | DAG | 8 | W1 W2 W3 W4 W5 | yes | yes |
| [distributed](file:///var/home/Louranicas/fedora-arena/cascades/distributed.toml) | distributed | 3 (+1 dynamic) (+1 sandboxed) | W2 W4 W5 | yes | yes |
| [doctor](file:///var/home/Louranicas/fedora-arena/cascades/doctor.toml) | DAG | 10 | W1 W4 W5 | yes | yes |
| [falsify](file:///var/home/Louranicas/fedora-arena/cascades/falsify.toml) | DAG | 15 | W1 W2 W4 W5 | yes | yes |
| [full-sweep](file:///var/home/Louranicas/fedora-arena/cascades/full-sweep.toml) | DAG | 14 | W1 W2 W3 W4 W5 | yes | yes |
| [knowledge-audit](file:///var/home/Louranicas/fedora-arena/cascades/knowledge-audit.toml) | DAG | 6 | W1 W2 W4 W5 | yes | yes |
| [matrix-quality](file:///var/home/Louranicas/fedora-arena/cascades/matrix-quality.toml) | matrix | 2 (+1 dynamic) | W2 W5 | yes | yes |
| [mcp-bridge](file:///var/home/Louranicas/fedora-arena/cascades/mcp-bridge.toml) | DAG | 5 | W1 W2 W5 | yes | yes |
| [on-break](file:///var/home/Louranicas/fedora-arena/cascades/on-break.toml) | DAG | 3 | W2 W3 W4 | yes | yes |
| [tree-repos](file:///var/home/Louranicas/fedora-arena/cascades/tree-repos.toml) | tree | 3 (+2 dynamic) | W2 W5 | yes | yes |
| [web-review](file:///var/home/Louranicas/fedora-arena/cascades/web-review.toml) | DAG | 7 | W2 W3 W4 W5 | yes | yes |
| [weightweb](file:///var/home/Louranicas/fedora-arena/cascades/weightweb.toml) | tree | 7 (+1 dynamic) | W1 W2 W3 W5 | yes | yes |

## Runbooks

| name | purpose | preconditions | steps | layers used | verify block declared | Arena Just wrapper |
|---|---|---|---|---|---|---|
| [audit](file:///var/home/Louranicas/fedora-arena/runbooks/audit.toml) | Health of the machine and integrity of its documentation | 1 | 6 | cascade, just, run | yes | present |
| [corpus-backup](file:///var/home/Louranicas/fedora-arena/runbooks/corpus-backup.toml) | Snapshot the habitat's irreplaceable corpus to both devices and verify it by restoring | 2 | 2 | run | yes | absent |
| [corpus-entry](file:///var/home/Louranicas/fedora-arena/runbooks/corpus-entry.toml) | Scope, then verify, an unfamiliar corpus without trusting your own instrument | 2 | 4 | run | yes | absent |
| [factory-baseline](file:///var/home/Louranicas/fedora-arena/runbooks/factory-baseline.toml) | Read-only T1-A census plus its negative controls; not product or production deployment | 0 | 1 | run | no | absent |
| [factory-ddf-pilot](file:///var/home/Louranicas/fedora-arena/runbooks/factory-ddf-pilot.toml) | Offline DDF Arena experiment: rootless builds, native tests, fixed review corpus; no promotion | 0 | 1 | run | no | absent |
| [factory-roster-lab](file:///var/home/Louranicas/fedora-arena/runbooks/factory-roster-lab.toml) | Qualify staged Hurl and ShellCheck capabilities, then prove a synthetic Restic recovery; no production activation | 1 | 1 | run | no | absent |
| [habitat-ops-probe](file:///var/home/Louranicas/fedora-arena/runbooks/habitat-ops-probe.toml) | The sockets are up, the gateway stays closed, Fabric is outside the decision, and a learning card does not run a command | 2 | 4 | run | yes | absent |
| [hee-crosscheck](file:///var/home/Louranicas/fedora-arena/runbooks/hee-crosscheck.toml) | Vault, ultra map, deployment atlas and codebase agree relation by relation, with denominators | 1 | 2 | run | yes | absent |
| [hee-graph-retention](file:///var/home/Louranicas/fedora-arena/runbooks/hee-graph-retention.toml) | Remove superseded Graphify copies and journals; prove the corpus still checks clean | 2 | 2 | run | yes | absent |
| [hee-publish](file:///var/home/Louranicas/fedora-arena/runbooks/hee-publish.toml) | Run the HEE-v3 corpus publication loop with its preconditions proven and its records retained | 4 | 2 | run | yes | absent |
| [hee-recapture](file:///var/home/Louranicas/fedora-arena/runbooks/hee-recapture.toml) | Recapture one changed diary reflection into the corpus without moving any lesson locator | 2 | 2 | run | yes | absent |
| [ship](file:///var/home/Louranicas/fedora-arena/runbooks/ship.toml) | Verify a change, annotate it for review, and gate it | 2 | 4 | cascade, just, mcp | yes | present |

A declared verify block is not a passed check. Wrapper presence checks the fixed Arena
`rb-NAME` forwarding recipe; it does not prove PATH resolution, Atuin registration, runtime
compatibility or admission. Missing wrappers remain explicit; this generator does not install them.

[Runbook source map](file:///var/home/Louranicas/fedora-arena/runbooks/README.md) · [Justfile source map](file:///var/home/Louranicas/fedora-arena/justfiles/README.md)

## Source fingerprints

Every top-level cascade and runbook TOML is enumerated. `cascades/triggers.toml` is a trigger
registry rather than a cascade and is excluded. The Arena justfile and generator are also pinned.

- [justfile](file:///var/home/Louranicas/fedora-arena/justfile): `c69406880d81786fc251d161ae81d524016b43095d283cd8e765d3e51b5e5663`
- [scripts/audit/catalogue.py](file:///var/home/Louranicas/fedora-arena/scripts/audit/catalogue.py): `18a96134eeedff43fcd04c2413b725c9affc4ccea72421e5b20c19297eb3802e`
- [cascades/assimilation.toml](file:///var/home/Louranicas/fedora-arena/cascades/assimilation.toml): `0e73fa82b33773140cf164534d6d03ba01f984307ed588bc1476553d918ba7e5`
- [cascades/clusterweb.toml](file:///var/home/Louranicas/fedora-arena/cascades/clusterweb.toml): `b9a319b8d6f6450ac8dbe6cda11c785d328400c2e7baa500d24c7a23984227f6`
- [cascades/distributed.toml](file:///var/home/Louranicas/fedora-arena/cascades/distributed.toml): `eae94fcfd21de80b6d2bcef0003f25ed516c289c6fd0d92027f1a152cc0108d9`
- [cascades/doctor.toml](file:///var/home/Louranicas/fedora-arena/cascades/doctor.toml): `e6d0a475cd0eaff0e688d81232451801dd88a011f4824a2777befe8efffd1b95`
- [cascades/falsify.toml](file:///var/home/Louranicas/fedora-arena/cascades/falsify.toml): `18231b937ecb0f6cf646021a91be78dc31f6fc2d248e833c664579234bca156b`
- [cascades/full-sweep.toml](file:///var/home/Louranicas/fedora-arena/cascades/full-sweep.toml): `8a2a607c3a74936fb7726e9925000a362468e1a40cf25b333845255264a816ea`
- [cascades/knowledge-audit.toml](file:///var/home/Louranicas/fedora-arena/cascades/knowledge-audit.toml): `b0732ec764330ca19e56e78a2ec736131a320059a76e16c048e7dc14512c2e10`
- [cascades/matrix-quality.toml](file:///var/home/Louranicas/fedora-arena/cascades/matrix-quality.toml): `458c0d710f5592707dcd6704f48dc8d9948f083152db1c4ee6299d5fd2143c80`
- [cascades/mcp-bridge.toml](file:///var/home/Louranicas/fedora-arena/cascades/mcp-bridge.toml): `a04dd1d910162c5e0517558f7b8d63c6b2bf1646e0d4a0ea9b864dbc2b391cf0`
- [cascades/on-break.toml](file:///var/home/Louranicas/fedora-arena/cascades/on-break.toml): `be0b91a1f9752d91a65fb0b5983a69eb537edab65862e7335436403565133fdf`
- [cascades/tree-repos.toml](file:///var/home/Louranicas/fedora-arena/cascades/tree-repos.toml): `d0e1e9708e094bb4a726abc13036fa1fcb3efbbe666ec66c9dde02dc0af2e3d4`
- [cascades/web-review.toml](file:///var/home/Louranicas/fedora-arena/cascades/web-review.toml): `cd692c7bc456d200947a1f3b40bcbc4299c22e14642f8d19b21337ff79c57679`
- [cascades/weightweb.toml](file:///var/home/Louranicas/fedora-arena/cascades/weightweb.toml): `e0bc0b63a34d3742387dcebe00e92c56692d5792dfbcb0523a56a4bce2ed53c0`
- [runbooks/audit.toml](file:///var/home/Louranicas/fedora-arena/runbooks/audit.toml): `75a320499de4ac32b70a581716444742f4ffff0779c5f0b32e9bc5bf1ad40936`
- [runbooks/corpus-backup.toml](file:///var/home/Louranicas/fedora-arena/runbooks/corpus-backup.toml): `d726fd194e1b3b14eec376ef32dfbdfc73aeb11e3bbde86c5906a7d093ab2deb`
- [runbooks/corpus-entry.toml](file:///var/home/Louranicas/fedora-arena/runbooks/corpus-entry.toml): `b5ac887966f842a5db002a76cb89aaa17e612884a5c3d533dc697acd584f87a8`
- [runbooks/factory-baseline.toml](file:///var/home/Louranicas/fedora-arena/runbooks/factory-baseline.toml): `5974ed4659ef49d1b7a2f1befb86a4430e408fb9a33de09e1125c42664cbc6e4`
- [runbooks/factory-ddf-pilot.toml](file:///var/home/Louranicas/fedora-arena/runbooks/factory-ddf-pilot.toml): `2f0d131909b7d5116151628ddd95540f373229f8d350c10f0f3c32aa325335e1`
- [runbooks/factory-roster-lab.toml](file:///var/home/Louranicas/fedora-arena/runbooks/factory-roster-lab.toml): `f33110a5f3564901083b3e15225b4df9304629c7e7b505f9bb59f9de38694930`
- [runbooks/habitat-ops-probe.toml](file:///var/home/Louranicas/fedora-arena/runbooks/habitat-ops-probe.toml): `aa0156e172ce5d4ae25f74f8bb41de2bcbcec48bf3b9cd1078c44e44163b2a0b`
- [runbooks/hee-crosscheck.toml](file:///var/home/Louranicas/fedora-arena/runbooks/hee-crosscheck.toml): `7363e0b4899dc126348391e736306e17e98d3275bd16095c9c7ee384a05f9e61`
- [runbooks/hee-graph-retention.toml](file:///var/home/Louranicas/fedora-arena/runbooks/hee-graph-retention.toml): `92d4583fdcad3bb56957fe37726b2d45d58bb85c0f574a02d7c92c70c452c1de`
- [runbooks/hee-publish.toml](file:///var/home/Louranicas/fedora-arena/runbooks/hee-publish.toml): `dbec8504a5453aa8e534acf8387f92dea6c38a785edf31b93038793babf7de07`
- [runbooks/hee-recapture.toml](file:///var/home/Louranicas/fedora-arena/runbooks/hee-recapture.toml): `45bd7860bd842fb925622e09f90d3297b7bcbe7cd7ac2c2ed5a1303ec68a123f`
- [runbooks/ship.toml](file:///var/home/Louranicas/fedora-arena/runbooks/ship.toml): `34412ef3b9d372a8500cb393303af3d095941d769e899851223005d46c1c8ef1`

Related: [[Cascade Engine]] · [[Clustering Shapes]] · [[Runbooks]] · [[00 - Workflows]] · [[00 - Toolshed Index]]

[Review and reciprocal routes](obsidian://open?vault=herdr-fedora-habitat.vault&file=95%20Genesis%2FJustfiles%20and%20Runbooks%20Review%202026-09-06)
