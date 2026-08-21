package shield_ai.mir.forensic_readiness

import rego.v1

# SHIELD-AI(TM) MIR-06: Forensic Readiness
# Pillar: MIR -- Monitoring, Logging, and Incident Response
#
# Maintain immutable, verifiable logs with full session reconstruction capability for all agents, including support for multi-agent chain reconstruction.
#
# Maturity indicators:
#   L1: Logs stored in standard database. Can be modified. Retention ad-hoc.
#   L2: Logs in append-only storage. Basic retention policy.
#   L3: Immutable logs with integrity verification. Full session reconstruction capability. Multi-agent chain reconstruction.
#   L4: Real-time forensic readiness verification. Automated forensic data extraction. Continuous integrity monitoring.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.action.high_impact (bool); input.action.reconstructible
# (bool) -- the session/tool-call chain can be fully reconstructed from
# immutable logs. High-impact actions that cannot be reconstructed fail
# closed: no reconstruction, no execution.

deny contains msg if {
    input.action.high_impact == true
    not input.action.reconstructible
    msg := sprintf("MIR-06 deny: high-impact action %q by agent %q is not reconstructible from immutable logs", [input.action.tool, input.agent.id])
}

allow if {
    count(deny) == 0
}
