package shield_ai.iam.human_oversight_controls_test

import rego.v1

import data.shield_ai.iam.human_oversight_controls.allow

test_low_risk_action_allowed if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents"}}
    allow with input as req
}

test_high_risk_action_without_approval_denied if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "transfer_funds", "high_risk_class": "financial"}}
    not allow with input as req
}

test_high_risk_action_with_human_approval_allowed if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "tool_call", "tool": "transfer_funds", "high_risk_class": "financial"},
        "approval": {"present": true, "channel": "human_console"},
    }
    allow with input as req
}

test_session_history_approval_evidence_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "dispatch", "tool": "transfer_funds", "high_risk_class": "financial"},
        "approval": {"present": true, "channel": "session_history"},
    }
    not allow with input as req
}

test_agent_channel_approval_for_financial_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "tool_call", "tool": "transfer_funds", "high_risk_class": "financial"},
        "approval": {"present": true, "channel": "agent"},
    }
    not allow with input as req
}
