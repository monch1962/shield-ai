package shield_ai.ds.output_validation_test

import rego.v1

import data.shield_ai.ds.output_validation.allow

test_clean_output_allowed if {
    req := {"action": {"kind": "output_delivery", "tool": "respond", "output_scan": "clean"}}
    allow with input as req
}

test_leak_flagged_output_denied if {
    req := {"action": {"kind": "output_delivery", "tool": "respond", "output_scan": "leak"}}
    not allow with input as req
}

test_pending_scan_fails_closed if {
    req := {"action": {"kind": "output_delivery", "tool": "respond", "output_scan": "pending"}}
    not allow with input as req
}

test_missing_scan_result_fails_closed if {
    req := {"action": {"kind": "output_delivery", "tool": "respond"}}
    not allow with input as req
}
