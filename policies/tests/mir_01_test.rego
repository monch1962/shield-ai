package shield_ai.mir.agent_activity_logging_test

import rego.v1

import data.shield_ai.mir.agent_activity_logging.allow

test_audited_append_only_action_allowed if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents", "audit_record": true, "log_storage": "append_only"}}
    allow with input as req
}

test_missing_audit_record_denied if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents"}}
    not allow with input as req
}

test_mutable_log_storage_denied if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents", "audit_record": true, "log_storage": "database"}}
    not allow with input as req
}
