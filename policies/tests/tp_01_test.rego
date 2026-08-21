package shield_ai.tp.tool_inventory_and_registry_test

import rego.v1

import data.shield_ai.tp.tool_inventory_and_registry.allow

test_registered_tool_allowed if {
    req := {"action": {"tool": "summarise_thread"}}
    allow with input as req
}

test_unregistered_tool_denied if {
    req := {"action": {"tool": "drop_database"}}
    not allow with input as req
}

test_missing_tool_denied if {
    req := {"agent": {"id": "agent-1"}}
    not allow with input as req
}
