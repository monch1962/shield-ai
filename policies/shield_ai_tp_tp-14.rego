package shield_ai.tp.skill_plugin_payload_integrity

import rego.v1

# SHIELD-AI(TM) TP-14: Skill/Plugin Payload Integrity and Instruction-Channel Isolation
# Pillar: TP -- Tool and Pipeline Security
#
# Gate every agent extension install on signed, immutable payloads with no runtime-fetchable instruction channels and privilege-scoped execution.
#
# Maturity indicators:
#   L1: Skills installed ad hoc from any marketplace with no signature or provenance checks; full agent privileges.
#   L2: Signature verification at install; marketplaces restricted to an operator allowlist.
#   L3: Immutable signed payloads; runtime-fetch channels blocked; privilege-scoped execution; post-install baseline with drift quarantine.
#   L4: End-to-end provenance attestation at registry and runtime; cross-org telemetry sharing on malicious-skill signals; red-team testing of the install path.
#
# Regulatory mappings:
#   OWASP: LLM08 (Excessive Agency)
#   NIST AI RMF: PROTECT (PR.DS)
#   EU AI Act: Art. 14 (Human Oversight)
#   ISM: Guidelines for Software Development, Application Control

# IMPLEMENTED (v1.20, Nov 2026) -- reference implementation (INC-48 ClawHavoc
# skill-marketplace poisoning; INC-66 Plugin4Shell SHA-pinning bypass).
# Input model: input.action.kind == "skill_execute" (a skill/plugin about to run).
# Skills must be signed, immutable, free of runtime-fetchable instruction
# channels, and execute with privilege scope and baseline drift quarantine.

deny contains msg if {
    input.action.kind == "skill_execute"
    input.action.skill.payload_signed == false
    msg := sprintf("TP-14 deny: execute skill %q for agent %q with an unsigned payload; never execute unsigned", [input.action.skill.name, input.agent.id])
}

deny contains msg if {
    input.action.kind == "skill_execute"
    input.action.skill.payload_immutable == false
    msg := sprintf("TP-14 deny: execute skill %q for agent %q whose payload is not immutable at install time", [input.action.skill.name, input.agent.id])
}

deny contains msg if {
    input.action.kind == "skill_execute"
    input.action.skill.runtime_fetch_channel == true
    msg := sprintf("TP-14 deny: skill %q for agent %q has a runtime-fetchable instruction channel (post-install reference/update feed); must be blocked at network and runtime", [input.action.skill.name, input.agent.id])
}

deny contains msg if {
    input.action.kind == "skill_execute"
    input.action.skill.privilege_scoped == false
    msg := sprintf("TP-14 deny: skill %q for agent %q executes with full agent privileges rather than a declared capability scope", [input.action.skill.name, input.agent.id])
}

deny contains msg if {
    input.action.kind == "skill_execute"
    input.action.skill.provenance_attested == false
    msg := sprintf("TP-14 deny: skill %q for agent %q lacks end-to-end provenance attestation (publisher -> registry -> artifact)", [input.action.skill.name, input.agent.id])
}

deny contains msg if {
    input.action.kind == "skill_execute"
    input.action.skill.full_capability_granted == true
    input.action.skill.baseline_established == false
    msg := sprintf("TP-14 deny: skill %q for agent %q is granted full capability before a post-install behavioural baseline; baseline drift quarantine required", [input.action.skill.name, input.agent.id])
}

allow if {
    count(deny) == 0
}