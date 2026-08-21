package shield_ai.mir.forensic_readiness_test

import rego.v1

import data.shield_ai.mir.forensic_readiness.allow

test_low_impact_action_allowed if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents", "high_impact": false}}
    allow with input as req
}

test_high_impact_reconstructible_allowed if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "transfer_funds", "high_impact": true, "reconstructible": true}}
    allow with input as req
}

test_high_impact_not_reconstructible_denied if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "transfer_funds", "high_impact": true}}
    not allow with input as req
}
