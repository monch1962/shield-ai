package shield_ai.ms.deployment_context_obfuscation

import rego.v1

import data.shield_ai.lib.bad_schema_version

# SHIELD-AI(TM) MS-07: Deployment Context Obfuscation
# Pillar: MS -- Model Security
#
# Prevent models from detecting evaluation environments and behaving differently than in production.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (Claude Mythos INC-06,
# OpenAI Math AI INC-08 environment-aware behaviour).
# Input model: input.evaluation = {"env_indistinguishable": bool,
# "behaviour_matches_production": bool}. Evaluation runs fail closed unless the
# environment is indistinguishable and behavioural equivalence is attested.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

# Envelope guard: reject fabricated/drifted schema-version input outright.
deny contains msg if {
    bad_schema_version(input)
    msg := sprintf("%s deny: input carries a schema_version not supported by this policy", ["MS-07"])
}
# Discriminator hoisted to one guard shared by all rules below.
applicable if {
    input.action.kind == "evaluation_run"
}


deny contains msg if {
    applicable
    not input.evaluation.env_indistinguishable
    msg := "MS-07 deny: evaluation environment distinguishable from production (endpoints, data shapes, latency)"
}

deny contains msg if {
    applicable
    not input.evaluation.behaviour_matches_production
    msg := "MS-07 deny: evaluation behaviour diverges from production for the same inputs (subversion indicator)"
}

allow if {
    count(deny) == 0
}
