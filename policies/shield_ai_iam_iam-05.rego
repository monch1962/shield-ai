package shield_ai.iam.just_in_time_jit_access

import rego.v1

# SHIELD-AI(TM) IAM-05: Just-in-Time (JIT) Access
# Pillar: IAM -- Identity and Access
#
# Issue session-bound, ephemeral credentials for agents with automatic expiration and the ability to revoke mid-session on suspicious behaviour detection.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.agent.credentials = {"ephemeral": bool,
# "revoked_after_session": bool}; input.agent.session_expired (bool).
# No standing access: fail closed on missing ephemeral claim.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

deny contains msg if {
    not input.agent.credentials.ephemeral
    msg := sprintf("IAM-05 deny: agent %q has standing (non-ephemeral) credentials", [input.agent.id])
}

deny contains msg if {
    input.agent.session_expired == true
    not input.agent.credentials.revoked_after_session
    msg := sprintf("IAM-05 deny: agent %q session expired without credential revocation", [input.agent.id])
}

allow if {
    count(deny) == 0
}
