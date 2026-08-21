package shield_ai.mir.behavioural_anomaly_detection_test

import rego.v1

import data.shield_ai.mir.behavioural_anomaly_detection.allow

test_normal_action_allowed if {
    req := {"agent": {"id": "agent-1", "ephemeral": false}, "action": {"kind": "tool_call", "tool": "search_documents", "anomaly_flag": false}}
    allow with input as req
}

test_anomaly_flagged_denied if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents", "anomaly_flag": true}}
    not allow with input as req
}

test_ephemeral_sensitive_without_campaign_correlation_denied if {
    req := {"agent": {"id": "agent-7", "ephemeral": true}, "action": {"kind": "tool_call", "tool": "shell_exec"}}
    not allow with input as req
}

test_ephemeral_sensitive_campaign_correlated_allowed if {
    req := {"agent": {"id": "agent-7", "ephemeral": true}, "action": {"kind": "tool_call", "tool": "shell_exec", "campaign_correlated": true}}
    allow with input as req
}
