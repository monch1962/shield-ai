package shield_ai.tp.skill_plugin_payload_integrity_test

import rego.v1

import data.shield_ai.tp.skill_plugin_payload_integrity.allow

test_trusted_skill_allowed if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "skill_execute",
            "skill": {
                "name": "web-tools",
                "payload_signed": true,
                "payload_immutable": true,
                "runtime_fetch_channel": false,
                "privilege_scoped": true,
                "provenance_attested": true,
                "full_capability_granted": true,
                "baseline_established": true,
            },
        },
    }
    allow with input as req
}

test_unsigned_skill_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "skill_execute", "skill": {"name": "web-tools", "payload_signed": false}},
    }
    not allow with input as req
}

test_mutable_skill_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "skill_execute", "skill": {"name": "web-tools", "payload_signed": true, "payload_immutable": false}},
    }
    not allow with input as req
}

test_runtime_fetch_channel_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "skill_execute", "skill": {"name": "web-tools", "payload_signed": true, "runtime_fetch_channel": true}},
    }
    not allow with input as req
}

test_unscoped_privileges_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "skill_execute", "skill": {"name": "web-tools", "payload_signed": true, "privilege_scoped": false}},
    }
    not allow with input as req
}

test_no_provenance_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "skill_execute", "skill": {"name": "web-tools", "payload_signed": true, "provenance_attested": false}},
    }
    not allow with input as req
}

test_full_capability_no_baseline_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "skill_execute", "skill": {"name": "web-tools", "full_capability_granted": true, "baseline_established": false}},
    }
    not allow with input as req
}

test_non_skill_action_not_gated if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents"}}
    allow with input as req
}