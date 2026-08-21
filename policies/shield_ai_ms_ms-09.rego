package shield_ai.ms.perception_fidelity_enforcemen

import rego.v1

# SHIELD-AI(TM) MS-09: Perception-Fidelity Enforcement for Human-in-the-Loop Approvals
# Pillar: MS -- Model Security
#
# Ensure human-in-the-loop approval is never gated on content the human cannot perceive.
#
# Maturity indicators:
#   L1: Manual review for high-risk actions; no hidden-content awareness.
#   L2: Automated detectors for known hidden-content primitives (1px text, zero-opacity, DOM-hidden); approval snapshots captured.
#   L3: Policy-as-code fidelity checks pre-approval; multimodal sanitisation; hidden-content stripping before agent context.
#   L4: Continuous red-team testing of perception attacks; fidelity attestation embedded in the audit trail.
#
# Regulatory mappings:
#   OWASP: LLM01 (Prompt Injection, multimodal variants)
#   NIST AI RMF: MEASURE (ME.AD)
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (AWS Kiro INC-20,
# Azure DevOps hidden PR comments INC-22, Android on-device INC-25, AISI
# sockpuppet attestation INC-27, Zenity INC-30).
# Input model: input.approval = {"present": bool, "snapshot_fidelity_verified":
# bool, "attestation_source": string}; input.context.content = agent-visible
# content the approval binds to.

# Imperceptible-content primitives (CSS/DOM layer). The MS-04 set covers
# instruction markers; this set is the perception layer: content the human
# cannot perceive must never gate an approval.
imperceptible_markers := {
    "color:#fff;font-size:1px",
    "font-size:0px",
    "opacity:0",
    "opacity: 0",
    "display:none",
    "visibility:hidden",
    "white-space:pre-wrap;color:transparent",
}

deny contains msg if {
    input.approval.present == true
    some item in input.context.content
    some marker in imperceptible_markers
    contains(item, marker)
    not input.approval.snapshot_fidelity_verified
    msg := sprintf("MS-09 deny: approval binds to content containing imperceptible marker %q without a verified rendering-fidelity snapshot", [marker])
}

deny contains msg if {
    input.approval.present == true
    input.approval.attestation_source == "agent"
    msg := "MS-09 deny: approval evidence comes from an agent-generated attestation (sockpuppet class); out-of-band verification required"
}

allow if {
    count(deny) == 0
}
