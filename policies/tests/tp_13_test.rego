package shield_ai.tp.agent_dependency_install_provenance_test

import rego.v1

import data.shield_ai.tp.agent_dependency_install_provenance.allow

test_verified_install_allowed if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "dependency_install",
            "dependency": {
                "registry_exists": true,
                "namespace_owned": true,
                "domain_registered": true,
                "from_ingested_content": false,
                "allowlisted_or_approved": true,
                "doc_as_authoritative": false,
                "dangling_reference": false,
            },
        },
    }
    allow with input as req
}

test_missing_registry_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "dependency_install", "dependency": {"registry_exists": false}},
    }
    not allow with input as req
}

test_unowned_namespace_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "dependency_install", "dependency": {"registry_exists": true, "namespace_owned": false}},
    }
    not allow with input as req
}

test_unregistered_domain_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "dependency_install", "dependency": {"registry_exists": true, "namespace_owned": true, "domain_registered": false}},
    }
    not allow with input as req
}

test_ingested_content_not_gated_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "dependency_install", "dependency": {"from_ingested_content": true, "allowlisted_or_approved": false}},
    }
    not allow with input as req
}

test_doc_as_authoritative_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "dependency_install", "dependency": {"doc_as_authoritative": true}},
    }
    not allow with input as req
}

test_dangling_reference_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "dependency_install", "dependency": {"dangling_reference": true}},
    }
    not allow with input as req
}

test_non_install_action_not_gated if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents"}}
    allow with input as req
}