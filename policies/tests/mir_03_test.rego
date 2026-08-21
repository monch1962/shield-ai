package shield_ai.mir.prompt_audit_log_test

import rego.v1

import data.shield_ai.mir.prompt_audit_log.allow

test_non_sensitive_action_allowed if {
    req := {"action": {"kind": "tool_call", "tool": "search_documents", "sensitive": false}}
    allow with input as req
}

test_sensitive_action_captured_and_redacted_allowed if {
    req := {"action": {"kind": "tool_call", "tool": "search_documents", "sensitive": true, "prompt_captured": true, "prompt_redacted": true}}
    allow with input as req
}

test_sensitive_action_not_captured_denied if {
    req := {"action": {"kind": "tool_call", "tool": "search_documents", "sensitive": true}}
    not allow with input as req
}

test_sensitive_action_captured_not_redacted_denied if {
    req := {"action": {"kind": "tool_call", "tool": "search_documents", "sensitive": true, "prompt_captured": true, "prompt_redacted": false}}
    not allow with input as req
}
