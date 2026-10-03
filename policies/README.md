# SHIELD-AI Policy-as-Code

This directory ships the framework's 67 controls as OPA/Rego policies with
deny-override assertions and per-control test vectors. Every control through v1.7 is
implemented; the v1.8 addition (MS-12), the v1.9 addition (TP-13) and the v1.10 addition (TP-14) ship as generated stubs pending deny-override assertions. The demo bundle in `demo/` is a reduced,
self-contained subset for prospects; the full control set lives here.

## Status (v1.17, October 2026)

**59 controls implemented, MS-12, TP-13, TP-14 and TP-15 stubs pending (67 controls total).** 253 OPA tests pass (`opa test policies
policies/tests demo/policies demo/tests`). Coverage by pillar:

| Pillar | Controls implemented |
|--------|----------------------|
| MS (Model Security) | MS-01..MS-12 |
| IAM (Identity and Access) | IAM-01..IAM-09 |
| DS (Data Security) | DS-01..DS-07 |
| TP (Tool and Pipeline Security) | TP-01..TP-12 |
| MIR (Monitoring and Incident Response) | MIR-01..MIR-06 |
| GRM (Governance and Risk Management) | GRM-01..GRM-06 |
| EE (Execution Environment) | EE-01..EE-08 |

Each implemented file's header records the incidents its assertions trace to
(see `framework/shield-ai-gap-analysis.md`). Maturity indicators and regulatory
mappings for every control live in `assets/shield-ai-control-schema.json` (the
schema generator, `tools/generate_control_schema.py`, is the canonical holder
of that metadata).

## Shared input model

Controls evaluate an agent action or a state claim. The common shape (each
control reads only its slice):

```json
{
  "agent": {
    "id": "agent-1",
    "sandboxed": true,
    "ephemeral": false,
    "compromised": false,
    "session_expired": false,
    "sandbox_attestation": {"present": true, "mode": "container"},
    "config": {"path_writable": ["/workspace"], "loaded_from_world_writable": false},
    "memory": {"write_auth": "jwt", "tamper_evidence": false, "persists_classified": false, "wiped_between_sessions": true},
    "identity": {"unique": true, "auditable": true},
    "delegation": {"scoped": true, "wildcard": false, "hops": 2, "max_hops": 2, "chain_reconstructable": true},
    "credentials": {"isolated": true, "per_tool_scope": true, "short_lived": true, "ephemeral": true, "broad_role": false, "rotation_triggered": true},
    "session": {"independent_context": true, "shared_credentials": false},
    "resource_usage": {"cpu_pct": 30, "network_mbps": 2, "api_rate": 40}
  },
  "action": {
    "kind": "tool_call",
    "tool": "summarise_thread",
    "target": "package_registry",
    "trigger": "log_alert",
    "high_impact": false,
    "high_risk_class": "financial",
    "sensitive": false,
    "acceptable": true,
    "anomaly_flag": false,
    "incident": false,
    "vendor_used": false,
    "vendor_type": "evaluation",
    "user_controlled_object_id": false,
    "cross_origin": false,
    "privileged": false,
    "token_access": false,
    "registered_as_tool": true,
    "registration": "explicit",
    "allowed_binding": true,
    "origin": "lan",
    "origin_validated": true,
    "provenance": {"session": "s-1", "turn": "t-3", "model_sig": "sig-abc"},
    "tool_def_signed": true,
    "server_registry": "trusted",
    "writes_execution_bearing": false,
    "output_scan": "clean",
    "guardrail_evaluated": true,
    "scope_compliant": true,
    "audit_record": true,
    "log_storage": "append_only",
    "reconstructible": true,
    "prompt_captured": true,
    "prompt_redacted": true,
    "reporting_triggered": true,
    "tool_auth": {"agent_authenticated": true, "human_session": false},
    "tool_allowed": true,
    "tool_output": {"validated": true, "sanitised": true, "within_size_limit": true, "code_generation": false, "code_sandboxed": true},
    "gateway": {"rate_limited": true, "schema_validated": true, "audited": true, "allowlist_active": true, "infra_isolation": true}
  },
  "context": {
    "content": ["agent-visible text"],
    "stream": {"verified_producer": true, "instruction_bearing": false, "independent_verification": true}
  },
  "approval": {"present": true, "channel": "human_console", "bound_tool": "transfer_funds", "snapshot_fidelity_verified": true, "attestation_source": "human"},
  "model": {"id": "m1", "weights_encrypted": true, "key_management": "hsm", "inventory": {"registered": true, "lineage_tracked": true, "versioned": true}, "supply_chain": {"sbom": true, "signature_verified": true, "checkpoint_signed": true}},
  "training": {"provenance_tracked": true, "sanitised": true, "poison_scan": "clean", "personal_data": false, "consent_verified": true, "governance": {"lineage": true, "retention_limited": true, "unlearning": true}},
  "data": {"classified": true, "label": "official", "access": {"bulk": false, "field_filtered": true, "abac_enforced": true}, "inference": {"encrypted_e2e": true, "tls13_min": true, "sensitive": false, "endpoint_in_trust_boundary": true}},
  "evaluation": {"env_indistinguishable": true, "behaviour_matches_production": true},
  "harness": {"isolation_verified": true, "production_network_path": false, "can_modify_production": false, "egress_block_verified": true, "target_collision_checked": true, "run_isolated": true},
  "pipeline": {"run_signed": true, "attested": true, "security_gate_passed": true, "artifact_registry_immutable": true},
  "dependencies": {"scanned": true, "critical_finding": false, "critical_blocked": false, "sandbox_library": false, "alternative_approved": false},
  "tools": {"chain_analysed": true, "escape_chain": false, "risk_accepted": false},
  "tenant": {"id": "t1", "scoped": true},
  "vendors": {"name": "acme-ai", "assessed": true, "contractual_controls": true, "right_to_audit": true},
  "governance": {"body": {"chartered": true, "cross_functional": true, "decision_authority": true}, "risk": {"registered": true, "kill_switch_tested": true}, "policy": {"hitl_by_risk": true}, "compliance": {"mapped": true, "quarterly_reported": true}, "reporting": {"dashboard": true, "risk_acceptance_logged": true}, "risk_acceptance": false},
  "incident": {"acknowledged": true, "class": "prompt_injection", "playbook": "ir-prompt-injection", "containment": true}
}
```

Semantics: deny-override. The platform evaluates `allow` for an action;
`allow == (count(deny) == 0)`, so a single deny blocks the action even when
every other control passes. Fail closed: any missing assertion the control
depends on is a deny, not a question.

## Testing

```bash
make test                      # or: opa test policies policies/tests demo/policies demo/tests
make check                     # full local gate suite
```

`make check` runs the stub generator (non-destructive — it preserves every
implemented control), the list-spacing scan, artifact verification (including
the schema-to-framework control-set drift check and MD footer version gate),
the exploit catalog gate, and the OPA tests.

## Conventions and pitfalls

- **`deny contains msg if ...` set rules + `allow if count(deny) == 0`.** Never
  `default deny = false` alongside a set deny; the set form keeps messages
  reportable.
- **`x != true` does NOT fail closed.** When `x` is missing from the input,
  `x != true` evaluates to undefined and the deny rule silently dies. Use
  `not x` instead: `not input.approval.present`, `not input.action.allowed_binding`.
  This bug shipped in the first batch and was caught by the negative tests.
- **`not x` does not catch empty strings.** `not input.incident.playbook` is
  false when `playbook` is `""` (defined). Where an empty value means "absent",
  write `not (input.incident.playbook != "")` (see MIR-04).
- **The generator is non-destructive.** `tools/generate_control_schema.py
  --rego` preserves any file whose body no longer contains the TODO marker.
  Regenerate freely; implemented controls are never clobbered.
- **Input-model scoping:** a control must gate only on its own slice and never
  assume fields owned by other controls exist. Deployment-defined sets
  (registries, markers, limits) are named constants at the top of each file,
  documented as replaceable per organisation.
- **Blank-line-before-lists applies here too** if you document policies in
  markdown (pandoc list merging).
