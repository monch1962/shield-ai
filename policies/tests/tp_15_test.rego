package shield_ai.tp.in_process_code_execution_sandbox_sufficiency_test

import rego.v1

import data.shield_ai.tp.in_process_code_execution_sandbox_sufficiency.allow

test_os_vm_sandboxed_allowed if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "code_execution",
            "code": {
                "sandboxed_os_vm": true,
                "in_process_gate_sole_containment": false,
                "shared_memory_context": false,
                "in_process_gate_high_risk_unblocked": false,
                "template_engine": true,
                "template_render_isolated": true,
            },
        },
    }
    allow with input as req
}

test_in_process_only_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "code_execution",
            "code": {"sandboxed_os_vm": false, "in_process_gate_sole_containment": false},
        },
    }
    not allow with input as req
}

test_denylist_sole_containment_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "code_execution",
            "code": {"in_process_gate_sole_containment": true},
        },
    }
    not allow with input as req
}

test_shared_memory_context_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "code_execution",
            "code": {"shared_memory_context": true},
        },
    }
    not allow with input as req
}

test_high_risk_unblocked_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "code_execution",
            "code": {"in_process_gate_high_risk_unblocked": true},
        },
    }
    not allow with input as req
}

test_template_engine_unisolated_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "code_execution",
            "code": {"template_engine": true, "template_render_isolated": false},
        },
    }
    not allow with input as req
}

test_non_code_action_not_gated if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents"}}
    allow with input as req
}