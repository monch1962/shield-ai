package shield_ai.tp.tool_call_provenance_and_dispa_test

import rego.v1

import data.shield_ai.tp.tool_call_provenance_and_dispa.allow

test_full_provenance_allowed if {
    req := {
        "action": {"kind": "dispatch", "tool": "transfer_funds", "provenance": {"session": "s-1", "turn": "t-3", "model_sig": "sig-abc"}},
    }
    allow with input as req
}

test_missing_session_provenance_denied if {
    req := {
        "action": {"kind": "dispatch", "tool": "transfer_funds", "provenance": {"turn": "t-3", "model_sig": "sig-abc"}},
    }
    not allow with input as req
}

test_missing_model_signature_denied if {
    req := {
        "action": {"kind": "dispatch", "tool": "transfer_funds", "provenance": {"session": "s-1", "turn": "t-3"}},
    }
    not allow with input as req
}

test_no_provenance_fails_closed if {
    req := {"action": {"kind": "dispatch", "tool": "transfer_funds"}}
    not allow with input as req
}

test_forged_approval_bound_to_wrong_tool_denied if {
    req := {
        "action": {"kind": "dispatch", "tool": "transfer_funds", "provenance": {"session": "s-1", "turn": "t-3", "model_sig": "sig-abc"}},
        "approval": {"present": true, "bound_tool": "read_calendar"},
    }
    not allow with input as req
}

test_approval_bound_to_matching_tool_allowed if {
    req := {
        "action": {"kind": "dispatch", "tool": "transfer_funds", "provenance": {"session": "s-1", "turn": "t-3", "model_sig": "sig-abc"}},
        "approval": {"present": true, "bound_tool": "transfer_funds"},
    }
    allow with input as req
}

test_non_dispatch_action_not_gated if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents"}}
    allow with input as req
}
