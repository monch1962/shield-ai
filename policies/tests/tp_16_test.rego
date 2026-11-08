package shield_ai.tp.tool_connection_and_launch_path_integrity_test

import rego.v1

import data.shield_ai.tp.tool_connection_and_launch_path_integrity.allow

test_safe_connect_allowed if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "tool_connect",
            "connection": {
                "transport_metadata_to_launch": false,
                "auth_endpoint_origin_bound": true,
                "auth_endpoint_validated_canonical": true,
                "peer_supplied_transport_field_crosses_launch": false,
            },
        },
    }
    allow with input as req
}

test_transport_to_launch_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "tool_connect", "connection": {"transport_metadata_to_launch": true}},
    }
    not allow with input as req
}

test_unbound_origin_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "tool_connect", "connection": {"auth_endpoint_origin_bound": false}},
    }
    not allow with input as req
}

test_unvalidated_canonical_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "tool_connect", "connection": {"auth_endpoint_validated_canonical": false}},
    }
    not allow with input as req
}

test_launch_not_allowlisted_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "tool_launch", "launch": {"command_allowlisted": false}},
    }
    not allow with input as req
}

test_model_derived_launch_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "tool_launch", "launch": {"command_allowlisted": true, "model_derived_command": true}},
    }
    not allow with input as req
}

test_peer_transport_crosses_launch_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "tool_connect", "connection": {"peer_supplied_transport_field_crosses_launch": true}},
    }
    not allow with input as req
}

test_non_connect_action_not_gated if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents"}}
    allow with input as req
}