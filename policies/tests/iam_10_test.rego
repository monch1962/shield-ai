package shield_ai.iam.taint_tracked_least_privilege_subagent_scoping_test

import rego.v1

import data.shield_ai.iam.taint_tracked_least_privilege_subagent_scoping.allow

test_untrusted_clean_record_allowed if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "data_read",
            "record": {
                "tainted": false,
                "taint_marked": true,
                "field_level_scoped": true,
                "cascades_to_sensitive": false,
                "sanitisation_boundary_explicit": true,
            },
        },
    }
    allow with input as req
}

test_tainted_untracked_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "data_read", "record": {"tainted": true, "taint_marked": false}},
    }
    not allow with input as req
}

test_tainted_unscoped_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "data_read", "record": {"tainted": true, "taint_marked": true, "field_level_scoped": false}},
    }
    not allow with input as req
}

test_tainted_cascades_to_sensitive_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "data_read", "record": {"tainted": true, "taint_marked": true, "field_level_scoped": true, "cascades_to_sensitive": true}},
    }
    not allow with input as req
}

test_tainted_no_sanitisation_boundary_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "data_read", "record": {"tainted": true, "taint_marked": true, "field_level_scoped": true, "cascades_to_sensitive": false, "sanitisation_boundary_explicit": false}},
    }
    not allow with input as req
}

test_non_read_action_not_gated if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents"}}
    allow with input as req
}