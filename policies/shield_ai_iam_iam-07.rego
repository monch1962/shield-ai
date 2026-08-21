package shield_ai.iam.transitive_delegation_chain_en

import rego.v1

# SHIELD-AI(TM) IAM-07: Transitive Delegation Chain Enforcement
# Pillar: IAM -- Identity and Access
#
# Bound delegation chains and make them fully auditable.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.agent.delegation = {"hops": n, "max_hops": 2,
# "chain_reconstructable": bool}. The two-hop bound (human -> agent -> tool)
# is enforced at the infrastructure layer; chains must be reconstructable
# from audit logs.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

deny contains msg if {
    input.agent.delegation.hops > input.agent.delegation.max_hops
    msg := sprintf("IAM-07 deny: delegation chain for agent %q is %v hops, exceeding the bound of %v", [input.agent.id, input.agent.delegation.hops, input.agent.delegation.max_hops])
}

deny contains msg if {
    not input.agent.delegation.chain_reconstructable
    msg := sprintf("IAM-07 deny: delegation chain for agent %q is not reconstructable from audit logs", [input.agent.id])
}

allow if {
    count(deny) == 0
}
