package shield_ai.tp.agent_platform_inbound_control_test

import rego.v1

import data.shield_ai.tp.agent_platform_inbound_control.allow

test_approved_binding_allowed if {
    req := {
        "action": {"kind": "binding", "target": "gateway:8080", "allowed_binding": true, "origin": "lan"},
    }
    allow with input as req
}

test_unapproved_binding_denied if {
    req := {"action": {"kind": "binding", "target": "0.0.0.0:8080", "origin": "lan"}}
    not allow with input as req
}

test_web_origin_binding_without_origin_validation_denied if {
    req := {
        "action": {"kind": "binding", "target": "ws://gateway/control", "allowed_binding": true, "origin": "web"},
    }
    not allow with input as req
}

test_web_origin_binding_validated_allowed if {
    req := {
        "action": {"kind": "binding", "target": "ws://gateway/control", "allowed_binding": true, "origin": "web", "origin_validated": true},
    }
    allow with input as req
}

test_non_binding_action_not_gated if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents"}}
    allow with input as req
}
