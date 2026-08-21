package shield_ai.iam.agent_identity_management

import rego.v1

# SHIELD-AI(TM) IAM-01: Agent Identity Management
# Pillar: IAM -- Identity and Access
#
# Ensure every agent has a unique, lifecycle-managed digital identity distinct from human user identities, integrated with the organisation's identity provider.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.agent.identity = {"unique": bool, "auditable": bool}.
# Fail closed: shared or unauditable identity denies the action.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

deny contains msg if {
    not input.agent.identity.unique
    msg := sprintf("IAM-01 deny: agent %q has no unique identity (sharing human credentials)", [input.agent.id])
}

deny contains msg if {
    not input.agent.identity.auditable
    msg := sprintf("IAM-01 deny: agent %q identity is not auditable", [input.agent.id])
}

allow if {
    count(deny) == 0
}
