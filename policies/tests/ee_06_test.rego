package shield_ai.ee.fail_closed_sandbox_operation_test

import rego.v1

import data.shield_ai.ee.fail_closed_sandbox_operation.allow

test_attested_execution_allowed if {
    req := {
        "agent": {"id": "agent-1", "sandbox_attestation": {"present": true, "mode": "container"}},
        "action": {"kind": "code_execution", "tool": "shell_exec"},
    }
    allow with input as req
}

test_missing_attestation_denied if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "code_execution", "tool": "shell_exec"}}
    not allow with input as req
}

test_negative_attestation_denied if {
    req := {
        "agent": {"id": "agent-1", "sandbox_attestation": {"present": false}},
        "action": {"kind": "code_execution", "tool": "shell_exec"},
    }
    not allow with input as req
}

test_interpreter_flags_are_not_a_boundary if {
    req := {
        "agent": {"id": "agent-1", "sandbox_attestation": {"present": true, "mode": "interpreter_flags"}},
        "action": {"kind": "code_execution", "tool": "shell_exec"},
    }
    not allow with input as req
}

test_non_execution_action_not_gated_by_attestation if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents"}}
    allow with input as req
}
