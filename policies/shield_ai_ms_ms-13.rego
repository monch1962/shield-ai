package shield_ai.ms.transcript_and_conversation_authenticity

import rego.v1

# SHIELD-AI(TM) MS-13: Transcript and Conversation Authenticity
# Pillar: MS -- Model Security
#
# Make the harness's record of model output tamper-evident and authentic at the model boundary.
#
# Maturity indicators:
#   L1: Conversation history stored client-side with no integrity/authenticity controls; no verification a stored response came from the model.
#   L2: Transcript stores inventoried; tamper-evidence policy documented; manual spot-check benchmarks.
#   L3: Model outputs signed at the API/proxy boundary (per-session HMAC/Ed25519, key outside harness) and verified on load; verification failures alert via MIR-01 and block the action.
#   L4: Append-only hash-chained transcript verified before any confidence-gated action; chain-break blocks execution with signed human-override; forward-secret key rotation; continuous attestation to an independent verifier.
#
# Regulatory mappings:
#   OWASP: LLM01 (Prompt Injection)
#   NIST AI RMF: PROTECT (PR.DS)
#   EU AI Act: Art. 14 (Human Oversight)
#   ISM: Guidelines for System Monitoring

# IMPLEMENTED (v1.20, Nov 2026) -- reference implementation (INC-70 Darktrace
# conversation-history poisoning; INC-83 config-file trust-ordering/marker
# authorship). Input model: input.action.kind == "transcript_read" (an agent
# about to reason over its stored history). The stored transcript must be
# verified as authentic model output before any reasoning or confidence-gated
# action proceeds from it.

deny contains msg if {
    input.action.kind == "transcript_read"
    input.action.transcript.model_output_signed == false
    msg := sprintf("MS-13 deny: agent %q reads a transcript whose model outputs are not signed at the model boundary; stored response cannot be verified as genuine", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "transcript_read"
    input.action.transcript.verified_on_read == false
    msg := sprintf("MS-13 deny: agent %q proceeds from an unverified transcript; every stored response must be verified on read before reasoning", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "transcript_read"
    input.action.transcript.chain_break == true
    input.action.transcript.confidence_gated_action == true
    msg := sprintf("MS-13 deny: agent %q attempts a confidence-gated action from a transcript with a broken authenticity chain; chain-break blocks execution", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "transcript_read"
    input.action.transcript.store_verified == false
    msg := sprintf("MS-13 deny: agent %q reads from an unverified transcript store; transcript stores are untrusted until verified", [input.agent.id])
}

allow if {
    count(deny) == 0
}