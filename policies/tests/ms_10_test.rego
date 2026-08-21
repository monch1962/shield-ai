package shield_ai.ms.agent_memory_store_integrity_test

import rego.v1

import data.shield_ai.ms.agent_memory_store_integrity.allow

test_authenticated_clean_write_allowed if {
    req := {
        "agent": {"id": "agent-1", "memory": {"write_auth": "jwt", "tamper_evidence": false}},
        "action": {"kind": "memory_write"},
    }
    allow with input as req
}

test_unauthenticated_write_denied if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "memory_write"}}
    not allow with input as req
}

test_tamper_evidence_denied if {
    req := {
        "agent": {"id": "agent-1", "memory": {"write_auth": "jwt", "tamper_evidence": true}},
        "action": {"kind": "memory_write"},
    }
    not allow with input as req
}

test_non_memory_action_not_gated if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents"}}
    allow with input as req
}
