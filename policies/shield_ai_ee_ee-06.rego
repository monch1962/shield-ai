package shield_ai.ee.fail_closed_sandbox_operation

import rego.v1

import data.shield_ai.lib.bad_schema_version

# SHIELD-AI(TM) EE-06: Fail-Closed Sandbox Operation
# Pillar: EE -- Execution Environment
#
# Eliminate silent fallback to weaker sandboxes.
#
# Maturity indicators:
#   L1: Sandbox used opportunistically; silent fallback possible.
#   L2: Sandbox availability checked; fallback paths documented but not blocked.
#   L3: Runtime attestation before each execution; no fallback path; fail-closed on unavailability; alerts on degradation.
#   L4: Continuous attestation; automated blocking of non-sandboxed execution; sandbox-unavailable events treated as compromise indicators.
#
# Regulatory mappings:
#   NIST AI RMF: PROTECT (PR.PT)
#   EU AI Act: Art. 15(b)
#   ISM: Guidelines for System Hardening
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (CrewAI fail-open
# class, INC-13).
# Input model: input.action.kind == "code_execution";
# input.agent.sandbox_attestation = {"present": bool, "mode": string}.
# Fail closed: absent or negative attestation denies; interpreter flags are
# convenience features, never security boundaries (INC-18).

# Envelope guard: reject fabricated/drifted schema-version input outright.
deny contains msg if {
    bad_schema_version(input)
    msg := sprintf("%s deny: input carries a schema_version not supported by this policy", ["EE-06"])
}
# Discriminator hoisted to one guard shared by all rules below.
applicable if {
    input.action.kind == "code_execution"
}


deny contains msg if {
    applicable
    not input.agent.sandbox_attestation.present
    msg := sprintf("EE-06 deny: no sandbox attestation before code execution by agent %q (fail closed)", [input.agent.id])
}

deny contains msg if {
    applicable
    input.agent.sandbox_attestation.present == false
    msg := sprintf("EE-06 deny: sandbox attestation negative for agent %q", [input.agent.id])
}

deny contains msg if {
    applicable
    input.agent.sandbox_attestation.mode == "interpreter_flags"
    msg := "EE-06 deny: interpreter isolation flags are a convenience feature, not a security boundary"
}

allow if {
    count(deny) == 0
}
