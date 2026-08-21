package shield_ai.ee.execution_environment_boundary_test

import rego.v1

import data.shield_ai.ee.execution_environment_boundary.allow

test_low_risk_unsandboxed_allowed if {
    req := {"agent": {"id": "agent-1", "sandboxed": false}, "action": {"tool": "search_documents"}}
    allow with input as req
}

test_high_risk_sandboxed_allowed if {
    req := {"agent": {"id": "agent-1", "sandboxed": true}, "action": {"tool": "transfer_funds"}}
    allow with input as req
}

test_high_risk_unsandboxed_denied if {
    req := {"agent": {"id": "agent-2", "sandboxed": false}, "action": {"tool": "transfer_funds"}}
    not allow with input as req
}

test_missing_sandbox_flag_fails_closed if {
    req := {"agent": {"id": "agent-3"}, "action": {"tool": "write_file"}}
    not allow with input as req
}
