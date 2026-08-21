package shield_ai.ee.evaluation_harness_isolation_a

import rego.v1

# SHIELD-AI(TM) EE-08: Evaluation-Harness Isolation and Integrity
# Pillar: EE -- Execution Environment
#
# Ensure evaluation harnesses are genuinely isolated and monitored, with isolation verified rather than asserted.
#
# Maturity indicators:
#   L1: Isolation asserted in prompts/configuration; no verification; no eval monitoring.
#   L2: Egress blocks enforced at the boundary; manual target collision checks; runs separated.
#   L3: Policy-as-code isolation attestation; GA classifiers and monitoring in eval environments; automated collision checks.
#   L4: Continuous escape testing; attested contamination controls; automated kill on escape indicators; independent third-party harness assurance (GRM-04).
#
# Regulatory mappings:
#   ISM: Isolation, Monitoring
#   NIST AI RMF: MEASURE (ME.AD)
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (Anthropic INC-19,
# Meta/Irregular INC-26, AISI INC-27, Kimi K3 INC-28).
# Input model: input.action.kind == "evaluation_run";
# input.harness = {"egress_block_verified": bool, "target_collision_checked": bool,
# "run_isolated": bool}. Fail closed: no verified egress block, no evaluation.

deny contains msg if {
    input.action.kind == "evaluation_run"
    not input.harness.egress_block_verified
    msg := "EE-08 deny: evaluation run without a verified egress block (isolation asserted, not enforced)"
}

deny contains msg if {
    input.action.kind == "evaluation_run"
    not input.harness.target_collision_checked
    msg := "EE-08 deny: evaluation run without target collision-checking against real domains and assets"
}

deny contains msg if {
    input.action.kind == "evaluation_run"
    not input.harness.run_isolated
    msg := "EE-08 deny: evaluation run without cross-run separation (contamination risk)"
}

allow if {
    count(deny) == 0
}
