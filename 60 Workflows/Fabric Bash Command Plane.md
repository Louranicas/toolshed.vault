---
tags: [toolshed, workflow, fabric, bash, just, runbook, chaining, w1-w5]
created: 2026-09-04
status: bounded read-only implementation — not activated
---

# Fabric Bash Command Plane — W1–W5

Parent: [[00 - Toolshed Index]]  
Related: [[Tool Chaining Patterns]] · [[Shape-Directed Tool Chaining]] · [[Tool Clusters]] · [[Runbooks]] · [[Command Matrix]] · [[Claim-Time Guard]] · [[Fabric Habitat 90-Point Promotion and Practice]] · [[just]] · [[atuin]]

Cross-vault: [Fabric pattern contract](obsidian://open?vault=fedora-fabric.vault&file=04%20Workflows%2FHabitat%20Bash%20Command%20Contract) ⇄ [Fabric assessment](obsidian://open?vault=fedora-fabric.vault&file=04%20Workflows%2FFabric%20Habitat%20Assessment%20and%20Integration) ⇄ [Fabric synergy review](obsidian://open?vault=fedora-fabric.vault&file=04%20Workflows%2FFabric%20Habitat%20Synergy%20Review) ⇄ [Fabric 90-point plan](obsidian://open?vault=fedora-fabric.vault&file=04%20Workflows%2FFabric%20Habitat%2090-Point%20Promotion%20and%20Practice) ⇄ [Habitat W1–W5 placement](obsidian://open?vault=herdr-fedora-habitat.vault&file=70%20Toolchain%2FFabric%20Bash%20Command%20Plane)

## Conclusion

Fabric can become the habitat's natural-language command compiler, but its output must not be piped directly into Bash. The safe and composable path is:

```text
intent
  → W1 grounding and capability discovery
  → Fabric emits a versioned JSON plan
  → W5 validates the plan and risk declaration
  → W2 resolves it to an existing Just recipe or typed runbook step
  → W4 rehearses novel or high-risk Bash in isolation
  → W3 exposes the diff and approval surface
  → Bash executes once
  → output is shape-routed and a receipt records what happened
```

The model proposes meaning. Deterministic code decides whether that proposal is executable. Verification, not the model, decides whether it worked.

## Command-selection law

| Intent shape | Owned execution surface |
|---|---|
| Existing repository operation | [[just]] recipe |
| Ordered procedure with preconditions and verification | [[Runbooks|runbook]] |
| Dependency graph with parallel stages | [[Cascade Engine|cascade]] |
| One operation over many targets | `habitat-battern` |
| One question asked of several tools | `habitat-poly` |
| Output whose consumer depends on its shape | `habitat-chain` |
| Proven procedure used repeatedly | Atuin script containing only the stable runbook invocation |
| No existing capability fits | reviewed Bash plan, initially sandboxed |

Fabric should select among these forms before it invents shell. A Just AST, runbook catalogue, service registry and installed help are better inputs than a model's memory of a CLI.

## Workspace leverage

| Workspace | Contribution | Handoff |
|---|---|---|
| W1 · memory and discovery | Atuin supplies successful precedent; MemPalace supplies reasons; television/fzf expose human selection; Nushell explores mixed tables | evidence and candidates, never automatic authority |
| W2 · editor and build | Just is the machine-readable capability catalogue; Bacon supplies the resident verdict; Nvim is source and diagnostics sink | resolved operation and structural validation |
| W3 · git and review | Hunk and TUICR make plans, recipes and diffs visible to agent and human; gh-dash supplies delivery state | approval, annotation and persisted review |
| W4 · system and containers | bottom exposes current pressure; yazi exposes path context; Podman supplies cold rehearsal and the toolbox→host boundary | environment evidence and isolation |
| W5 · data and fleet | jq/jqp validate the envelope; repo-fleet selects scope; TUICR persists review | schema verdict, aggregation and routing |

The `habitat` bridge remains the spine. Use an agent door for values that become inputs, and a pane door when the relevant fact is what the human is seeing.

## `habitat_bash_plan` envelope

The Fabric-side pattern emits JSON only:

```json
{
  "schema": "habitat.bash-plan/v1",
  "intent": "check this repository and route diagnostics for review",
  "entrypoint": "just",
  "target": "check",
  "argv": [],
  "cwd": "/absolute/scoped/path",
  "risk": "read",
  "host_escape": false,
  "preconditions": [],
  "expected_shape": "diagnostics",
  "route": ["nvim", "hunk"],
  "verification": {"kind": "exit", "equals": 0},
  "approval_required": false,
  "evidence": ["just-ast", "installed-help"]
}
```

`entrypoint` is `just`, `runbook`, `habitat`, `cascade`, or `bash`. The first four resolve a known name and typed arguments. `bash` is the fallback and carries a full script, declared mutation surface and explicit verification.

## Bash policy

- Prefer argv and direct process execution when shell grammar is unnecessary.
- When Bash is necessary, require `set -Eeuo pipefail`, a narrow cwd, explicit inputs and deterministic cleanup.
- Reject `eval`, unbounded recursive deletion, hidden host escape, unreviewed download-and-execute chains and writes outside declared scope.
- Preserve the producer's exit status; a formatting pipe must not become the verdict. Use [[Claim-Time Guard|the claim-time rule]] and its `gate` use-pattern.
- Require human approval for host mutation, privilege escalation, network publication, destructive operations and changes outside version-controlled scope.
- Validate syntax and add ShellCheck when available. Neither ShellCheck nor `shfmt` is currently installed.
- Never make a Fabric model or second Fabric pattern the sole verifier of Fabric output.

## One renderer per layer

This integration crosses five brace-based dialects:

- Fabric pattern variables: `{{name}}`
- Just interpolation: `{{name}}`
- runbook variables: `{{name}}`
- Atuin/minijinja variables: `{{ name }}`
- Podman Go templates: `{{.Names}}`

Render once, then hand off typed data. Fabric renders its prompt and emits JSON. The command compiler binds typed fields and emits Bash once. Generated Just and Atuin entries call a named runbook; they do not copy or re-template its body. Prefer Podman JSON output over embedded Go templates.

## Execution sequence

1. Gather narrow, read-only context: service metadata, cwd, Just AST, runbook catalogue, installed help and redacted W1 evidence.
2. Run the Fabric pattern without a persistent session and require the JSON envelope.
3. Validate schema, enums, paths, risk and evidence in W5 using deterministic code.
4. Refuse nonexistent services, recipes, runbooks or routes.
5. For direct Bash, run syntax, policy and detector checks; send mutating scripts through W3 review.
6. Rehearse novel or high-risk work in W4. Record warm and cold evidence separately.
7. Execute through the runbook engine, capturing stdout, stderr, exit status and timings separately.
8. Feed captured output—not a model-generated command string—into `habitat-chain`.
9. Verify independently and receipt pattern hash, model/vendor, input digest, cwd, tree/dirty/spec, command digest, risk, approval, output shape and verifier result.
10. Promote successful operations: direct Bash → Just recipe → runbook → Atuin alias for the runbook.

## Source reconciliation — 2026-09-04

- `~/.config/habitat/services.json` defines 16 W1–W5 services and now names all five registered vault paths; the Obsidian registry remains the identity authority.
- Fabric is outside the mounted-vault root and is therefore mined through its own explicit MemPalace room. W1 retrieval spans multiple mine roots even though the semantic wing is shared.
- `habitat-chain`, `habitat-battern`, `habitat-poly` and `habitat-runbook` accept trusted authored strings and eventually execute through `bash -lc`. They are not safe consumers of raw model output.
- Runbooks recognize `run`, `just`, `cascade` and `mcp`, but no typed `fabric` or `bash-plan` step.
- Three TOML runbook specs exist, while only two generated Just/Atuin surfaces were observed.
- Fabric v1.4.477 has 255 built-ins. No custom-pattern directory or registered extension was configured.
- Upstream `create_command` emits only Bash, with no schema, risk declaration, approval requirement or verifier.
- The Toolshed index said eight chaining shapes while [[Tool Chaining Patterns]] had grown to nine; this assimilation corrects the wording.

## Implementation order

1. Build a read-only capability catalogue from the five-vault registry, service registry, Just AST and runbook specs.
2. Author and adversarially test `habitat_bash_plan` and `habitat_bash_review` in version control.
3. Add a schema validator and command-policy gate before any executor.
4. Add typed `fabric` and `bash-plan` runbook steps with durable receipts.
5. Make shape routing accept captured stdin or a receipt path instead of producer strings.
6. Add a freshness gate for every runbook's Just and Atuin surfaces.
7. Unify W1 recall across the five registered vaults.
8. Test normal, adversarial, negative-control, warm and cold cases before activation.

## Authority and status

This note owns command composition and execution design. The Fabric vault owns pattern behavior; the Habitat vault owns W1–W5 placement. This is an assimilated design, not an activated service and not evidence of a passing execution path.

## Bounded Arena experiment — 2026-09-04

[Arena runbook and findings](file:///var/home/Louranicas/fedora-arena/runbooks/Fabric%20Habitat%20W1-W5%20Lab.md) ⇄ [verified receipt](file:///var/home/Louranicas/fedora-arena/receipts/fabric-habitat-lab-20260904T133417Z-2308770/verdict.json).

A read-only slice now has execution evidence: five Bash jobs reached W1/Nushell, W2/Bacon, W3/Lazygit, W4/Bottom and W5/JQP concurrently, then completed a `W5 → W1 → W5` normalized round trip with count `5`. The exact capability validator, four negative controls, five-vault boundary, service-specific pane semantics, Fabric dry-run and component-provenance gate all passed. This is a passing bounded experiment, not promotion of raw model output, pane mutation, repository mutation, container mutation, vault traversal or the wider architecture.

## Synergy-review integration

Fabric is treated as a cognitive control plane, not only a Bash generator. A future request receipts pattern, context, strategy and session independently; catalog patterns may challenge a plan but never issue PASS; entry points are classified by effect; ingestion is quarantined from execution; and verified lessons move through receipt → Obsidian → MemPalace → versioned context. Executable extensions, file-application paths, REST storage mutation, non-loopback serving and persistent cross-boundary sessions remain denied by default. See the [Fabric synergy review](obsidian://open?vault=fedora-fabric.vault&file=04%20Workflows%2FFabric%20Habitat%20Synergy%20Review).
