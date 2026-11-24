package shield_ai.iam.scope_bound_delegation

import rego.v1

import data.shield_ai.lib.bad_schema_version

# SHIELD-AI(TM) IAM-02: Scope-Bound Delegation
# Pillar: IAM -- Identity and Access
#
# Limit each agent's permissions to the minimum set of tools, data, and actions required for its function, enforced by a policy-as-code engine at invocation time.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.agent.delegation = {"scoped": bool, "wildcard": bool}.
# Wildcard permissions are denied outright; missing scope claims fail closed.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

# Envelope guard: reject fabricated/drifted schema-version input outright.
deny contains msg if {
    bad_schema_version(input)
    msg := sprintf("%s deny: input carries a schema_version not supported by this policy", ["IAM-02"])
}

deny contains msg if {
    not input.agent.delegation.scoped
    msg := sprintf("IAM-02 deny: agent %q has no scope-bound delegation claim (fail closed)", [input.agent.id])
}

deny contains msg if {
    input.agent.delegation.wildcard == true
    msg := sprintf("IAM-02 deny: agent %q has wildcard permissions", [input.agent.id])
}

allow if {
    count(deny) == 0
}
