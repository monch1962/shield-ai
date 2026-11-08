package shield_ai.ms.mcp_discovery_metadata_shared_cache_integrity_test

import rego.v1

import data.shield_ai.ms.mcp_discovery_metadata_shared_cache_integrity.allow

test_clean_discovery_allowed if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "mcp_discovery",
            "discovery": {
                "instructions_length_limited": true,
                "instructions_isolated": true,
                "shared_cache_cross_auth": false,
                "cache_provenance_signed": false,
                "cache_scope_verified": true,
                "cache_key_bound_to_identity": true,
                "tool_metadata_baseline_drifted": false,
            },
        },
    }
    allow with input as req
}

test_unbounded_instructions_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "mcp_discovery",
            "discovery": {"instructions_length_limited": false},
        },
    }
    not allow with input as req
}

test_unisolated_instructions_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "mcp_discovery",
            "discovery": {"instructions_length_limited": true, "instructions_isolated": false},
        },
    }
    not allow with input as req
}

test_cross_auth_cache_unsigned_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "mcp_discovery",
            "discovery": {"shared_cache_cross_auth": true, "cache_provenance_signed": false},
        },
    }
    not allow with input as req
}

test_unverified_cache_scope_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "mcp_discovery",
            "discovery": {"cache_scope_verified": false},
        },
    }
    not allow with input as req
}

test_unbound_cache_key_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "mcp_discovery",
            "discovery": {"cache_key_bound_to_identity": false},
        },
    }
    not allow with input as req
}

test_baseline_drift_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "mcp_discovery",
            "discovery": {"tool_metadata_baseline_drifted": true},
        },
    }
    not allow with input as req
}

test_non_discovery_action_not_gated if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents"}}
    allow with input as req
}