package shield_ai.ms.deployment_context_obfuscation

import rego.v1

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

deny contains msg if {
    input.action.kind == "evaluation_run"
    not input.evaluation.env_indistinguishable
    msg := "MS-07 deny: evaluation environment distinguishable from production (endpoints, data shapes, latency)"
}

deny contains msg if {
    input.action.kind == "evaluation_run"
    not input.evaluation.behaviour_matches_production
    msg := "MS-07 deny: evaluation behaviour diverges from production for the same inputs (subversion indicator)"
}

allow if {
    count(deny) == 0
}
