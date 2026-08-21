package shield_ai.ms.mcp_security_controls_test

import rego.v1

import data.shield_ai.ms.mcp_security_controls.allow

test_signed_trusted_registry_allowed if {
    req := {"action": {"kind": "mcp_connect", "server": "mcp.example.com", "tool_def_signed": true, "server_registry": "trusted"}}
    allow with input as req
}

test_unsigned_tool_definitions_denied if {
    req := {"action": {"kind": "mcp_connect", "server": "mcp.example.com", "tool_def_signed": false, "server_registry": "trusted"}}
    not allow with input as req
}

test_untrusted_registry_denied if {
    req := {"action": {"kind": "mcp_connect", "server": "evil.example.com", "tool_def_signed": true, "server_registry": "untrusted"}}
    not allow with input as req
}

test_missing_registry_claim_fails_closed if {
    req := {"action": {"kind": "mcp_connect", "server": "mcp.example.com", "tool_def_signed": true}}
    not allow with input as req
}

test_execution_bearing_write_capability_denied if {
    req := {"action": {"kind": "mcp_connect", "server": "mcp.example.com", "tool_def_signed": true, "server_registry": "trusted", "writes_execution_bearing": true}}
    not allow with input as req
}
