package shield_ai.ds.memory_sanitisation

import rego.v1

# SHIELD-AI(TM) DS-03: Memory Sanitisation
# Pillar: DS -- Data Security
#
# Prevent persistence of sensitive data across sessions through automated purging, encryption, per-agent scoping, and cross-session aggregation detection.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.agent.memory = {"persists_classified": bool,
# "wiped_between_sessions": bool}; input.action.kind == "session_end".
# MS-10 (memory-store integrity) covers tamper-evidence; this control covers
# the privacy surface: sensitive data must not persist across sessions.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

deny contains msg if {
    input.agent.memory.persists_classified == true
    msg := sprintf("DS-03 deny: agent %q persists classified or sensitive data beyond session lifetime", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "session_end"
    not input.agent.memory.wiped_between_sessions
    msg := sprintf("DS-03 deny: agent %q session ended without memory wipe (cross-session leakage risk)", [input.agent.id])
}

allow if {
    count(deny) == 0
}
