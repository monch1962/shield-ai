package shield_ai.ms.transcript_and_conversation_authenticity_test

import rego.v1

import data.shield_ai.ms.transcript_and_conversation_authenticity.allow

test_verified_signed_transcript_allowed if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "transcript_read",
            "transcript": {
                "model_output_signed": true,
                "verified_on_read": true,
                "chain_break": false,
                "confidence_gated_action": true,
                "store_verified": true,
            },
        },
    }
    allow with input as req
}

test_unsigned_output_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "transcript_read",
            "transcript": {"model_output_signed": false},
        },
    }
    not allow with input as req
}

test_unverified_on_read_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "transcript_read",
            "transcript": {"model_output_signed": true, "verified_on_read": false},
        },
    }
    not allow with input as req
}

test_chain_break_confidence_gated_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "transcript_read",
            "transcript": {
                "model_output_signed": true,
                "verified_on_read": true,
                "chain_break": true,
                "confidence_gated_action": true,
            },
        },
    }
    not allow with input as req
}

test_unverified_store_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "transcript_read",
            "transcript": {"model_output_signed": true, "verified_on_read": true, "store_verified": false},
        },
    }
    not allow with input as req
}

test_non_transcript_action_not_gated if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents"}}
    allow with input as req
}