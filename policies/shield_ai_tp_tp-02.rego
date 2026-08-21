package shield_ai.tp.tool_access_control

import rego.v1

# SHIELD-AI(TM) TP-02: Tool Access Control
# Pillar: TP -- Tool and Pipeline Security
#
# Enforce per-agent tool allow-lists at invocation time with authenticated agent identity and version-controlled, auditable access policies.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.action.tool_auth = {"agent_authenticated": bool,
# "human_session": bool}; input.action.tool_allowed (bool) -- per-agent
# allow-list verdict at invocation time.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

deny contains msg if {
    not input.action.tool_auth.agent_authenticated
    msg := sprintf("TP-02 deny: tool %q call not authenticated to the agent identity", [input.action.tool])
}

deny contains msg if {
    input.action.tool_auth.human_session == true
    msg := sprintf("TP-02 deny: tool %q authenticated against the human session, not the agent identity", [input.action.tool])
}

deny contains msg if {
    input.action.tool_allowed != true
    msg := sprintf("TP-02 deny: tool %q not on the agent's invocation-time allow-list", [input.action.tool])
}

allow if {
    count(deny) == 0
}
