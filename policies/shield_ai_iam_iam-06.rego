package shield_ai.iam.cross_session_boundary_enforce

import rego.v1

# SHIELD-AI(TM) IAM-06: Cross-Session Boundary Enforcement
# Pillar: IAM -- Identity and Access
#
# Ensure each agent session is an independent security context with no credential or data sharing across sessions.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.agent.session = {"independent_context": bool,
# "shared_credentials": bool}. Any cross-session credential sharing is denied.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

deny contains msg if {
    input.agent.session.shared_credentials == true
    msg := sprintf("IAM-06 deny: agent %q session shares credentials across sessions", [input.agent.id])
}

deny contains msg if {
    not input.agent.session.independent_context
    msg := sprintf("IAM-06 deny: agent %q session is not an independent security context", [input.agent.id])
}

allow if {
    count(deny) == 0
}
