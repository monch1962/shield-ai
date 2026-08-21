package shield_ai.ee.evaluation_harness_isolation_a_test

import rego.v1

import data.shield_ai.ee.evaluation_harness_isolation_a.allow

test_fully_verified_harness_allowed if {
    req := {
        "action": {"kind": "evaluation_run"},
        "harness": {"egress_block_verified": true, "target_collision_checked": true, "run_isolated": true},
    }
    allow with input as req
}

test_unverified_egress_block_denied if {
    req := {"action": {"kind": "evaluation_run"}, "harness": {"target_collision_checked": true, "run_isolated": true}}
    not allow with input as req
}

test_missing_collision_check_denied if {
    req := {"action": {"kind": "evaluation_run"}, "harness": {"egress_block_verified": true, "run_isolated": true}}
    not allow with input as req
}

test_cross_run_contamination_risk_denied if {
    req := {"action": {"kind": "evaluation_run"}, "harness": {"egress_block_verified": true, "target_collision_checked": true}}
    not allow with input as req
}

test_non_evaluation_action_not_gated if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents"}}
    allow with input as req
}
