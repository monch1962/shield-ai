package shield_ai.ee.evaluation_sandbox_integrity

import rego.v1

import data.shield_ai.lib.bad_schema_version

# SHIELD-AI(TM) EE-04: Evaluation Sandbox Integrity
# Pillar: EE -- Execution Environment
#
# Contain the blast radius of model behaviour during evaluation.
#
# Maturity indicators:
#   L1: Evaluation and production share networks, data, and tooling.
#   L2: Evaluation isolated from production data; network path partially open.
#   L3: No network path between evaluation and production; evaluation pipelines cannot modify production.
#   L4: Continuous isolation verification; automated teardown; evaluation subversion detection per MS-07.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (OpenAI INC-01,
# Claude Mythos INC-06 evaluation containment).
# Input model: input.action.kind == "evaluation_run";
# input.harness = {"isolation_verified": bool, "production_network_path": bool,
# "can_modify_production": bool}. Fail closed: unverified isolation = deny.
# EE-08 (evaluation-harness isolation and integrity) adds egress-block
# verification, collision checks, and run separation on top of this baseline.

# Envelope guard: reject fabricated/drifted schema-version input outright.
deny contains msg if {
    bad_schema_version(input)
    msg := sprintf("%s deny: input carries a schema_version not supported by this policy", ["EE-04"])
}
# Discriminator hoisted to one guard shared by all rules below.
applicable if {
    input.action.kind == "evaluation_run"
}


deny contains msg if {
    applicable
    not input.harness.isolation_verified
    msg := "EE-04 deny: evaluation run with unverified evaluation-to-production isolation (fail closed)"
}

deny contains msg if {
    applicable
    input.harness.production_network_path == true
    msg := "EE-04 deny: evaluation run has a network path to production"
}

deny contains msg if {
    applicable
    input.harness.can_modify_production == true
    msg := "EE-04 deny: evaluation pipeline can modify production systems or data"
}

allow if {
    count(deny) == 0
}
