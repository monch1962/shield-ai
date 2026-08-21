package shield_ai.tp.pipeline_integrity

import rego.v1

# SHIELD-AI(TM) TP-05: Pipeline Integrity
# Pillar: TP -- Tool and Pipeline Security
#
# Sign and attest all CI/CD pipeline runs, enforce security gates before deployment, and store deployment artifacts in an immutable, integrity-verified registry.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.pipeline = {"run_signed": bool, "attested": bool,
# "security_gate_passed": bool, "artifact_registry_immutable": bool}.
# Deployment actions fail closed on any missing pipeline claim.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

deny contains msg if {
    input.action.kind == "deployment"
    not input.pipeline.run_signed
    msg := "TP-05 deny: deployment from an unsigned CI/CD run"
}

deny contains msg if {
    input.action.kind == "deployment"
    not input.pipeline.attested
    msg := "TP-05 deny: deployment without pipeline attestation"
}

deny contains msg if {
    input.action.kind == "deployment"
    not input.pipeline.security_gate_passed
    msg := "TP-05 deny: deployment that failed the security validation gate"
}

deny contains msg if {
    input.action.kind == "deployment"
    not input.pipeline.artifact_registry_immutable
    msg := "TP-05 deny: deployment artifact not stored in an immutable, integrity-verified registry"
}

allow if {
    count(deny) == 0
}
