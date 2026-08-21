# SHIELD-AI Policy-as-Code

This directory ships the framework's 59 controls as OPA/Rego policies. Every
control has a file; implemented controls carry real deny-override assertions,
the rest are stubs awaiting conversion. The demo bundle in `demo/` is a
reduced, self-contained subset for prospects; the full control set lives here.

## Status (v1.7, August 2026)

Implemented (assertions + test vectors):

| Control | Package | Covers |
|---------|---------|--------|
| MS-04 | `shield_ai.ms.adversarial_robustness` | Prompt-injection and imperceptible-content markers (INC-20/25/30) |
| MS-10 | `shield_ai.ms.agent_memory_store_integrity` | Memory-store write integrity, tamper evidence (INC-31) |
| MS-11 | `shield_ai.ms.operational_data_stream_integr` | Log/alert-triggered actions, producer verification (INC-33) |
| TP-01 | `shield_ai.tp.tool_inventory_and_registry` | Approved tool registry (explicit registration) |
| TP-10 | `shield_ai.tp.agent_platform_inbound_control` | Default-deny bindings, origin validation (INC-21/31) |
| TP-12 | `shield_ai.tp.tool_call_provenance_and_dispa` | Dispatch provenance, forged-approval binding (INC-34) |
| EE-01 | `shield_ai.ee.execution_environment_boundary` | High-risk tool sandbox requirement, fail closed |
| EE-06 | `shield_ai.ee.fail_closed_sandbox_operation` | Sandbox attestation, no silent fallback (INC-13) |
| EE-07 | `shield_ai.ee.agent_control_plane_configurat` | Control-plane write denial, world-writable loads (INC-14/15) |
| DS-07 | `shield_ai.ds.agent_originated_artifact_publ` | Publication out-of-band approval (INC-19/20) |

49 controls remain stubs (`# TODO: Implement control test logic`). Convert
per-pillar batches following the pattern below.

## Shared input model

Controls evaluate an agent action. The common shape (each control reads only
its slice):

```json
{
  "agent": {
    "id": "agent-1",
    "sandboxed": true,
    "sandbox_attestation": {"present": true, "mode": "container"},
    "config": {"path_writable": ["/workspace"], "loaded_from_world_writable": false},
    "memory": {"write_auth": "jwt", "tamper_evidence": false}
  },
  "action": {
    "kind": "tool_call",
    "tool": "summarise_thread",
    "target": "package_registry",
    "trigger": "log_alert",
    "high_impact": false,
    "allowed_binding": true,
    "origin": "web",
    "origin_validated": true,
    "provenance": {"session": "s-1", "turn": "t-3", "model_sig": "sig-abc"}
  },
  "context": {
    "content": ["agent-visible text"],
    "stream": {"verified_producer": true, "instruction_bearing": false, "independent_verification": true}
  },
  "approval": {"present": true, "channel": "human_console", "bound_tool": "transfer_funds"}
}
```

Semantics: deny-override. The platform evaluates `allow` for an action;
`allow == (count(deny) == 0)`, so a single deny blocks the action even when
every other control passes. Fail closed: any missing assertion the control
depends on is a deny, not a question.

## Converting a stub (the pattern)

1. Keep the metadata header (title, pillar, maturity indicators, regulatory
   mappings) untouched. Add an `IMPLEMENTED` note with the incidents the
   assertions trace to.
2. Replace `# Default deny / default deny = false / TODO` with:

   ```rego
   import rego.v1
   ```

3. Write `deny contains msg if { ... }` rules, one per failure mode, with
   deployment-defined sets as named constants at the top of the file.
4. Add `allow if { count(deny) == 0 }`.
5. Write test vectors in `policies/tests/<pillar>_<id>_test.rego` (see the
   existing tests): one pass case, plus one negative case per deny rule.
6. Run `make test` (or `opa test policies policies/tests demo/policies demo/tests`).

## Pitfalls (learned converting the first batch)

- **`x != true` does NOT fail closed.** When `x` is missing from the input,
  `x != true` evaluates to undefined and the deny rule silently dies. Use
  `not x` instead: `not input.approval.present`, `not input.action.allowed_binding`.
  The first batch shipped with this bug; the negative tests caught it.
- **Never `default deny = false` alongside a set deny.** The stub template
  uses a boolean default; implemented controls use the set form
  (`deny contains msg if ...`) so messages are reportable and
  `count(deny) == 0` is the allow test.
- **The generator is non-destructive.** `tools/generate_control_schema.py
  --rego` preserves any file whose body no longer contains the TODO marker.
  You can regenerate freely; implemented controls are never clobbered.
- **Blank-line-before-lists applies here too** if you document policies in
  markdown (pandoc list merging).

## Gates

`make check` runs: stub regeneration (non-destructive), list-spacing scan,
artifact verification (includes a schema-to-framework control-set drift check
and the MD footer version gate), the exploit catalog gate, and the OPA tests.
