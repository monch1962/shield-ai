package shield_ai.ms.self_replication_barrier

import rego.v1

import data.shield_ai.lib.bad_schema_version
import data.shield_ai.lib.field_undefined

# SHIELD-AI(TM) MS-14: Self-Replication Barrier
# Pillar: MS -- Model Security
#
# Prevent an injected instruction from being re-emitted through the agent's own output channels to propagate to other agents.
#
# Maturity indicators:
#   L1: No detection of re-emitted instruction text in outbound content.
#   L2: Automated near-verbatim detection of source-prompt n-grams in outbound payloads; documentation of the replication kill-chain.
#   L3: Fingerprint matching quarantine with human approval; one-channel-per-write and human-signoff-on-broadcast; blast-radius cap per hop.
#   L4: Worm-emulation drills prove replication is blocked; automated channel-kill and incident-response triggers on any matching propagation signal.
#
# Regulatory mappings:
#   OWASP: LLM01 (Prompt Injection)
#   NIST AI RMF: PROTECT (PR.DS)
#   EU AI Act: Art. 14 (Human Oversight)
#   ISM: Guidelines for System Monitoring

# IMPLEMENTED (v1.20, Nov 2026) -- reference implementation (INC-71 OpenAI
# GPT-Red self-replicating prompt injections). Input model:
# input.action.kind == "outbound_publish". Agent-generated outbound content must
# be screened for near-verbatim re-emission of instruction-bearing input;
# a replication match quarantines the write and requires human approval.

# Envelope guard: reject fabricated/drifted schema-version input outright.
deny contains msg if {
    bad_schema_version(input)
    msg := sprintf("%s deny: input carries a schema_version not supported by this policy", ["MS-14"])
}
# Discriminator hoisted to one guard shared by all rules below.
applicable if {
    input.action.kind == "outbound_publish"
}


deny contains msg if {
    applicable
    input.action.outbound.replication_match == true
    input.action.outbound.quarantined == false
    msg := sprintf("MS-14 deny: outbound publish by agent %q matches an instruction-bearing n-gram fingerprint (replication vector) and is not quarantined", [input.agent.id])
}
deny contains msg if {
    applicable
    input.action.outbound.replication_match == true
    not field_undefined(input, ["action", "outbound"])
    field_undefined(input, ["action", "outbound", "quarantined"])
    msg := "MS-14 deny: missing attestation for input.action.outbound.quarantined (unobserved -> fail closed)"
}

deny contains msg if {
    applicable
    input.action.outbound.replication_match == true
    input.action.outbound.human_approved == false
    msg := sprintf("MS-14 deny: outbound publish by agent %q is a fingerprinted replication match that lacks human approval", [input.agent.id])
}
deny contains msg if {
    applicable
    input.action.outbound.replication_match == true
    not field_undefined(input, ["action", "outbound"])
    field_undefined(input, ["action", "outbound", "human_approved"])
    msg := "MS-14 deny: missing attestation for input.action.outbound.human_approved (unobserved -> fail closed)"
}

deny contains msg if {
    applicable
    input.action.outbound.broadcast == true
    input.action.outbound.human_signoff == false
    msg := sprintf("MS-14 deny: outbound broadcast by agent %q lacks human signoff (one-channel-per-write / human-signoff-on-broadcast)", [input.agent.id])
}
deny contains msg if {
    applicable
    input.action.outbound.broadcast == true
    not field_undefined(input, ["action", "outbound"])
    field_undefined(input, ["action", "outbound", "human_signoff"])
    msg := "MS-14 deny: missing attestation for input.action.outbound.human_signoff (unobserved -> fail closed)"
}

deny contains msg if {
    applicable
    input.action.outbound.propagation_signal == true
    msg := sprintf("MS-14 deny: outbound publish by agent %q carries a propagation signal; channel-kill and incident response triggered (worm-emulation)", [input.agent.id])
}

allow if {
    count(deny) == 0
}