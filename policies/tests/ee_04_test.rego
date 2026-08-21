package shield_ai.ee.evaluation_sandbox_integrity_test

import rego.v1

import data.shield_ai.ee.evaluation_sandbox_integrity.allow

test_isolated_harness_allowed if {
    req := {
        "action": {"kind": "evaluation_run"},
        "harness": {"isolation_verified": true, "production_network_path": false, "can_modify_production": false},
    }
    allow with input as req
}

test_unverified_isolation_fails_closed if {
    req := {"action": {"kind": "evaluation_run"}, "harness": {"production_network_path": false}}
    not allow with input as req
}

test_production_network_path_denied if {
    req := {
        "action": {"kind": "evaluation_run"},
        "harness": {"isolation_verified": true, "production_network_path": true, "can_modify_production": false},
    }
    not allow with input as req
}

test_production_modification_denied if {
    req := {
        "action": {"kind": "evaluation_run"},
        "harness": {"isolation_verified": true, "production_network_path": false, "can_modify_production": true},
    }
    not allow with input as req
}

test_non_evaluation_action_not_gated if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents"}}
    allow with input as req
}
