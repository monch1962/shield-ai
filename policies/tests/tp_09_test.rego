package shield_ai.tp.explicit_tool_registration_test

import rego.v1

import data.shield_ai.tp.explicit_tool_registration.allow

test_explicitly_registered_tool_allowed if {
    req := {"action": {"kind": "tool_call", "tool": "search_documents", "registration": "explicit"}}
    allow with input as req
}

test_auto_registered_tool_denied if {
    req := {"action": {"kind": "tool_call", "tool": "download_file_async", "registration": "auto"}}
    not allow with input as req
}

test_missing_registration_fails_closed if {
    req := {"action": {"kind": "dispatch", "tool": "transfer_funds"}}
    not allow with input as req
}

test_non_tool_action_not_gated if {
    req := {"action": {"kind": "binding", "target": "gateway:8080", "allowed_binding": true}}
    allow with input as req
}
