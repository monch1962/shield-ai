package shield_ai.tp.agent_browser_and_content_rend_test

import rego.v1

import data.shield_ai.tp.agent_browser_and_content_rend.allow

test_same_origin_action_allowed if {
    req := {"action": {"kind": "tool_call", "tool": "read_page", "cross_origin": false}}
    allow with input as req
}

test_cross_origin_privileged_without_approval_denied if {
    req := {"action": {"kind": "tool_call", "tool": "send_email", "cross_origin": true, "privileged": true}}
    not allow with input as req
}

test_cross_origin_privileged_with_approval_allowed if {
    req := {"action": {"kind": "tool_call", "tool": "send_email", "cross_origin": true, "privileged": true}, "approval": {"present": true}}
    allow with input as req
}

test_unsanitized_document_render_denied if {
    req := {"action": {"kind": "document_render", "tool": "process_document"}}
    not allow with input as req
}

test_sanitized_document_render_allowed if {
    req := {"action": {"kind": "document_render", "tool": "process_document", "document_sanitized": true}}
    allow with input as req
}

test_token_access_without_approval_denied if {
    req := {"action": {"kind": "tool_call", "tool": "get_credential", "token_access": true}}
    not allow with input as req
}
