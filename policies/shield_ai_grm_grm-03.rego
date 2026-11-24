package shield_ai.grm.ethical_use_policy

import rego.v1

import data.shield_ai.lib.attestation_deny
import data.shield_ai.lib.bad_schema_version

# SHIELD-AI(TM) GRM-03: Ethical Use Policy
# Pillar: GRM -- Governance and Risk Management
#
# Document and enforce an ethical use policy that classifies agents by risk tier, defines autonomy boundaries per tier, and specifies transparency obligations.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.action.acceptable (bool) -- the action is inside the
# documented acceptable-use boundary for the agent's risk tier;
# input.governance.policy = {"hitl_by_risk": bool}; input.action.high_risk_class.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

# Envelope guard: reject fabricated/drifted schema-version input outright.
deny contains msg if {
    bad_schema_version(input)
    msg := sprintf("%s deny: input carries a schema_version not supported by this policy", ["GRM-03"])
}

deny contains msg if {
    input.action.acceptable == false
    msg := sprintf("GRM-03 deny: action %q outside the documented acceptable-use boundary for agent %q", [input.action.tool, input.agent.id])
}
deny contains msg if {
    msg := data.shield_ai.lib.attestation_deny(input, "GRM-03", ["action"], ["action", "acceptable"])
}
deny contains msg if {
    input.action.high_risk_class
    not input.governance.policy.hitl_by_risk
    msg := "GRM-03 deny: high-risk tier agent deployed without human-in-the-loop requirement per risk tier"
}

allow if {
    count(deny) == 0
}
