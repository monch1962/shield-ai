package shield_ai.ds.agent_originated_artifact_publ_test

import rego.v1

import data.shield_ai.ds.agent_originated_artifact_publ.allow

test_publication_with_out_of_band_approval_allowed if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "publication", "target": "package_registry"},
        "approval": {"present": true, "channel": "human_console"},
    }
    allow with input as req
}

test_publication_without_approval_denied if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "publication", "target": "package_registry"}}
    not allow with input as req
}

test_agent_invoked_approval_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "publication", "target": "package_registry"},
        "approval": {"present": true, "channel": "agent"},
    }
    not allow with input as req
}

test_execution_bearing_config_write_requires_human_console if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "publication", "target": "execution_bearing_config"},
        "approval": {"present": true, "channel": "email"},
    }
    not allow with input as req
}

test_non_publication_action_not_gated if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents"}}
    allow with input as req
}
