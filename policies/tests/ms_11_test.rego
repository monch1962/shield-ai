package shield_ai.ms.operational_data_stream_integr_test

import rego.v1

import data.shield_ai.ms.operational_data_stream_integr.allow

test_non_log_triggered_action_allowed if {
    req := {"action": {"kind": "tool_call", "tool": "search_documents"}, "context": {"stream": {}}}
    allow with input as req
}

test_clean_verified_stream_allowed if {
    req := {
        "action": {"kind": "tool_call", "tool": "rotate_dns", "trigger": "log_alert", "high_impact": false},
        "context": {"stream": {"verified_producer": true, "instruction_bearing": false}},
    }
    allow with input as req
}

test_unverified_producer_denied if {
    req := {
        "action": {"kind": "tool_call", "tool": "rotate_dns", "trigger": "log_alert"},
        "context": {"stream": {"verified_producer": false, "instruction_bearing": false}},
    }
    not allow with input as req
}

test_instruction_bearing_stream_without_verification_denied if {
    req := {
        "action": {"kind": "tool_call", "tool": "rotate_dns", "trigger": "log_alert"},
        "context": {"stream": {"verified_producer": true, "instruction_bearing": true}},
    }
    not allow with input as req
}

test_instruction_bearing_stream_with_independent_verification_allowed if {
    req := {
        "action": {"kind": "tool_call", "tool": "rotate_dns", "trigger": "log_alert"},
        "context": {"stream": {"verified_producer": true, "instruction_bearing": true, "independent_verification": true}},
    }
    allow with input as req
}

test_high_impact_log_triggered_action_requires_approval if {
    req := {
        "action": {"kind": "tool_call", "tool": "rotate_dns", "trigger": "log_alert", "high_impact": true},
        "context": {"stream": {"verified_producer": true, "instruction_bearing": false}},
    }
    not allow with input as req
}
