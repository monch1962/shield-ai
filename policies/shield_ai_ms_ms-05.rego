package shield_ai.ms.model_behaviour_validation

import rego.v1

import data.shield_ai.lib.bad_schema_version

# SHIELD-AI(TM) MS-05: Model Behaviour Validation
# Pillar: MS -- Model Security
#
# Validate that model outputs conform to expected safety, content, and scope boundaries through proxy-layer guardrails and per-agent behaviour configuration.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.action.guardrail_evaluated (bool); input.action.scope_compliant
# (bool). Every output delivery must pass the proxy-layer guardrails and stay
# within the agent's configured behaviour scope.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

# Envelope guard: reject fabricated/drifted schema-version input outright.
deny contains msg if {
    bad_schema_version(input)
    msg := sprintf("%s deny: input carries a schema_version not supported by this policy", ["MS-05"])
}
# Discriminator hoisted to one guard shared by all rules below.
applicable if {
    input.action.kind == "output_delivery"
}


deny contains msg if {
    applicable
    not input.action.guardrail_evaluated
    msg := sprintf("MS-05 deny: output by agent %q not evaluated by proxy-layer guardrails (fail closed)", [input.agent.id])
}

deny contains msg if {
    applicable
    not input.action.scope_compliant
    msg := sprintf("MS-05 deny: output by agent %q outside its configured behaviour scope", [input.agent.id])
}

allow if {
    count(deny) == 0
}
