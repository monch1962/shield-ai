package shield_ai.mir.agent_activity_logging

import rego.v1

# SHIELD-AI(TM) MIR-01: Agent Activity Logging
# Pillar: MIR -- Monitoring, Logging, and Incident Response
#
# Log all agent actions in structured format with immutable storage, SIEM integration, and distributed tracing support for multi-agent architectures.
#
# Maturity indicators:
#   L1: Basic agent logs (start, stop). Limited structure. Stored locally.
#   L2: Structured audit logs for all agent actions. Centralised storage. 30-day retention.
#   L3: Immutable logs. Correlation IDs across multi-agent chains. SIEM integration. Log integrity verification.
#   L4: Real-time log streaming. Automated log anomaly detection. Extended retention for forensic readiness.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.action.audit_record (bool) -- the action carries a
# structured audit record; input.action.log_storage ("append_only" | other).
# Every agent action must be logged; at the framework's L3 posture the log
# store is immutable.

deny contains msg if {
    not input.action.audit_record
    msg := sprintf("MIR-01 deny: agent %q action %q has no structured audit record", [input.agent.id, input.action.tool])
}

deny contains msg if {
    input.action.audit_record == true
    not (input.action.log_storage == "append_only")
    msg := "MIR-01 deny: audit record not written to append-only storage (integrity requirement)"
}

allow if {
    count(deny) == 0
}
