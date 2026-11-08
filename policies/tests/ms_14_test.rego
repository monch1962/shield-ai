package shield_ai.ms.self_replication_barrier_test

import rego.v1

import data.shield_ai.ms.self_replication_barrier.allow

test_clean_outbound_allowed if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "outbound_publish",
            "outbound": {
                "replication_match": false,
                "quarantined": false,
                "human_approved": false,
                "broadcast": false,
                "human_signoff": false,
                "propagation_signal": false,
            },
        },
    }
    allow with input as req
}

test_replication_match_not_quarantined_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "outbound_publish",
            "outbound": {"replication_match": true, "quarantined": false},
        },
    }
    not allow with input as req
}

test_replication_match_no_human_approval_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "outbound_publish",
            "outbound": {"replication_match": true, "quarantined": true, "human_approved": false},
        },
    }
    not allow with input as req
}

test_broadcast_no_signoff_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "outbound_publish",
            "outbound": {"broadcast": true, "human_signoff": false},
        },
    }
    not allow with input as req
}

test_propagation_signal_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "outbound_publish",
            "outbound": {"propagation_signal": true},
        },
    }
    not allow with input as req
}

test_non_outbound_action_not_gated if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents"}}
    allow with input as req
}