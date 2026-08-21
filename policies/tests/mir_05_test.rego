package shield_ai.mir.mandatory_reporting_integratio_test

import rego.v1

import data.shield_ai.mir.mandatory_reporting_integratio.allow

test_non_incident_action_allowed if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents", "incident": false}}
    allow with input as req
}

test_incident_with_reporting_trigger_allowed if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "transfer_funds", "incident": true, "reporting_triggered": true}}
    allow with input as req
}

test_incident_without_reporting_trigger_denied if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "transfer_funds", "incident": true}}
    not allow with input as req
}
