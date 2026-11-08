package shield_ai.ms.self_replication_barrier

import rego.v1

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

deny contains msg if {
    input.action.kind == "outbound_publish"
    input.action.outbound.replication_match == true
    input.action.outbound.quarantined == false
    msg := sprintf("MS-14 deny: outbound publish by agent %q matches an instruction-bearing n-gram fingerprint (replication vector) and is not quarantined", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "outbound_publish"
    input.action.outbound.replication_match == true
    input.action.outbound.human_approved == false
    msg := sprintf("MS-14 deny: outbound publish by agent %q is a fingerprinted replication match that lacks human approval", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "outbound_publish"
    input.action.outbound.broadcast == true
    input.action.outbound.human_signoff == false
    msg := sprintf("MS-14 deny: outbound broadcast by agent %q lacks human signoff (one-channel-per-write / human-signoff-on-broadcast)", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "outbound_publish"
    input.action.outbound.propagation_signal == true
    msg := sprintf("MS-14 deny: outbound publish by agent %q carries a propagation signal; channel-kill and incident response triggered (worm-emulation)", [input.agent.id])
}

allow if {
    count(deny) == 0
}