package shield_ai.ms.cross_tenant_agent_memory_and_state_test

import rego.v1

import data.shield_ai.ms.cross_tenant_agent_memory_and_state.allow

# --- Pooled-store read: hard ownership gating ---------------------------------

test_pooled_read_same_tenant_allowed if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "memory_read",
            "pooled_store": true,
            "cross_tenant_hit": false,
            "ownership_verified": true,
            "namespace_model_controllable": false,
            "connection_params_bound": true,
        },
    }
    allow with input as req
}

test_pooled_read_cross_tenant_hit_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "memory_read",
            "pooled_store": true,
            "cross_tenant_hit": true,
            "ownership_verified": true,
            "namespace_model_controllable": false,
            "connection_params_bound": true,
        },
    }
    not allow with input as req
}

test_pooled_read_unverifiable_ownership_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "memory_read",
            "pooled_store": true,
            "cross_tenant_hit": false,
            # ownership_verified omitted -> must fail closed
            "namespace_model_controllable": false,
            "connection_params_bound": true,
        },
    }
    not allow with input as req
}

test_non_pooled_read_not_ownership_gated if {
    # A single-tenant store is not subject to the pooled ownership gate.
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "memory_read",
            "pooled_store": false,
            "namespace_model_controllable": false,
            "connection_params_bound": true,
        },
    }
    allow with input as req
}

# --- Model-controllable isolation key -----------------------------------------

test_read_model_controllable_namespace_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "memory_read",
            "pooled_store": false,
            "namespace_model_controllable": true,
            "connection_params_bound": true,
        },
    }
    not allow with input as req
}

test_write_model_controllable_namespace_denied if {
    req := {
        "agent": {"id": "agent-1", "memory": {"write_auth": "jwt"}},
        "action": {
            "kind": "memory_write",
            "namespace_model_controllable": true,
            "connection_params_bound": true,
        },
    }
    not allow with input as req
}

# --- Connection parameters bound at construction ------------------------------

test_read_unbound_connection_params_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "memory_read",
            "pooled_store": false,
            "namespace_model_controllable": false,
            "connection_params_bound": false,
        },
    }
    not allow with input as req
}

test_write_unbound_connection_params_denied if {
    req := {
        "agent": {"id": "agent-1", "memory": {"write_auth": "jwt"}},
        "action": {
            "kind": "memory_write",
            "namespace_model_controllable": false,
            "connection_params_bound": false,
        },
    }
    not allow with input as req
}

# --- Authenticated cross-tenant writes ----------------------------------------

test_write_same_tenant_authenticated_allowed if {
    req := {
        "agent": {"id": "agent-1", "memory": {"write_auth": "jwt"}},
        "action": {
            "kind": "memory_write",
            "cross_tenant_hit": false,
            "namespace_model_controllable": false,
            "connection_params_bound": true,
        },
    }
    allow with input as req
}

test_cross_tenant_write_denied if {
    req := {
        "agent": {"id": "agent-1", "memory": {"write_auth": "jwt"}},
        "action": {
            "kind": "memory_write",
            "cross_tenant_hit": true,
            "namespace_model_controllable": false,
            "connection_params_bound": true,
        },
    }
    not allow with input as req
}

test_unauthenticated_write_denied if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {
            "kind": "memory_write",
            "namespace_model_controllable": false,
            "connection_params_bound": true,
        },
    }
    not allow with input as req
}

# --- Unrelated actions are not gated ------------------------------------------

test_non_memory_action_not_gated if {
    req := {
        "agent": {"id": "agent-1"},
        "action": {"kind": "tool_call", "tool": "search_documents"},
    }
    allow with input as req
}