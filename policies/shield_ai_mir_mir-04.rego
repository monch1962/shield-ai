package shield_ai.mir.incident_response_playbooks

import rego.v1

# SHIELD-AI(TM) MIR-04: Incident Response Playbooks
# Pillar: MIR -- Monitoring, Logging, and Incident Response
#
# Develop and maintain AI-specific IR playbooks covering prompt injection, model compromise, tool abuse, and code-generation attacks, tested through regular tabletop exercises.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (G19: agent-speed
# adversary IR playbooks and automatic containment).
# Input model: input.incident = {"playbook": string, "containment": bool,
# "invoked": bool}; input.incident.class (string: prompt_injection | model_compromise
# | tool_abuse | code_generation | other). Fail closed: an incident without a
# playbook or containment step is not acknowledged as handled.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

deny contains msg if {
    input.incident.acknowledged == true
    not (input.incident.playbook != "")
    msg := sprintf("MIR-04 deny: %s incident acknowledged without a named AI-specific IR playbook", [input.incident.class])
}

deny contains msg if {
    input.incident.acknowledged == true
    not input.incident.containment
    msg := sprintf("MIR-04 deny: %s incident without an automatic containment step (agent-speed response)", [input.incident.class])
}

allow if {
    count(deny) == 0
}
