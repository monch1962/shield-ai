package shield_ai.iam.taint_tracked_least_privilege_subagent_scoping

import rego.v1

# SHIELD-AI(TM) IAM-10: Taint-Tracked Least-Privilege Subagent Scoping
# Pillar: IAM -- Identity and Access
#
# Taint-track externally-submitted records and bind subagent permission scoping to that taint plus field-level least privilege.
#
# Maturity indicators:
#   L1: Subagents process externally-submitted records with the same broad grants as internally-trusted data; no taint marking.
#   L2: Externally-submitted records flagged as untrusted; manual review of subagent scope when processing them.
#   L3: Taint-marked at ingestion; record-handling subagents scoped to only required tables/fields/tools; tainted reads prevented from cascading into untainted sensitive collections.
#   L4: Automated taint propagation through the workflow graph; least-privilege subagent scope enforced by policy-as-code; any tainted-to-sensitive read blocked with alerting.
#
# Regulatory mappings:
#   NIST AI RMF: PROTECT (PR.AC)
#   OWASP: LLM08 (Excessive Agency)
#   EU AI Act: Art. 14(b)
#   ISM: Guidelines for System Management

# IMPLEMENTED (v1.20, Nov 2026) -- reference implementation (INC-72 SalesBleed
# Poisoned-lead cross-table read via default-access General CRM subagent).
# Input model: input.action.kind == "data_read"; input.action.record.tainted =
# the record was externally/submitted or poisoned; a record-handling subagent
# must be taint-scoped to field-level least privilege and must not cascade into
# untainted sensitive collections.

deny contains msg if {
    input.action.kind == "data_read"
    input.action.record.tainted == true
    input.action.record.taint_marked == false
    msg := sprintf("IAM-10 deny: agent %q processed an externally-submitted record that was not taint-marked at ingestion", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "data_read"
    input.action.record.tainted == true
    input.action.record.field_level_scoped == false
    msg := sprintf("IAM-10 deny: agent %q reads a tainted record without field-level least-privilege scoping (must be narrower than nominal grants)", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "data_read"
    input.action.record.tainted == true
    input.action.record.cascades_to_sensitive == true
    msg := sprintf("IAM-10 deny: agent %q tainted read cascades into an untainted sensitive collection beyond the immediate task; blocked", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "data_read"
    input.action.record.tainted == true
    input.action.record.sanitisation_boundary_explicit == false
    msg := sprintf("IAM-10 deny: agent %q processed a tainted record where the untrusted/trusted sanitisation boundary is not an explicit access-control decision", [input.agent.id])
}

allow if {
    count(deny) == 0
}