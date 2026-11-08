package shield_ai.ds.destination_and_emergent_channel_egress_inventory_test

import rego.v1

import data.shield_ai.ds.destination_and_emergent_channel_egress_inventory.allow

test_allowlisted_http_egress_allowed if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "egress": {
                "channel": "http",
                "destination_allowlisted": true,
                "channel_inventoried": true,
                "classifier_based": false,
                "invoker_attributed": true,
                "dns_resolver_allowlisted": true,
                "render_source_allowlisted": true,
            },
        },
    }
    allow with input as req
}

test_unallowlisted_destination_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"egress": {"destination_allowlisted": false}},
    }
    not allow with input as req
}

test_uninventoried_channel_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"egress": {"destination_allowlisted": true, "channel_inventoried": false}},
    }
    not allow with input as req
}

test_classifier_based_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"egress": {"destination_allowlisted": true, "classifier_based": true}},
    }
    not allow with input as req
}

test_messaging_unattributed_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"egress": {"channel": "messaging", "destination_allowlisted": true, "invoker_attributed": false}},
    }
    not allow with input as req
}

test_dns_unrestricted_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"egress": {"channel": "dns", "destination_allowlisted": true, "dns_resolver_allowlisted": false}},
    }
    not allow with input as req
}

test_rendered_media_unallowlisted_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"egress": {"channel": "rendered_media", "destination_allowlisted": true, "render_source_allowlisted": false}},
    }
    not allow with input as req
}

test_non_egress_action_not_gated if {
    req := {"agent": {"id": "agent-1"}, "action": {"kind": "tool_call", "tool": "search_documents"}}
    allow with input as req
}