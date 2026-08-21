package shield_ai.iam.multi_tenant_agent_platform_is_test

import rego.v1

import data.shield_ai.iam.multi_tenant_agent_platform_is.allow

test_tenant_scoped_request_allowed if {
    req := {
  "tenant": {
    "id": "t1",
    "scoped": true
  },
  "action": {
    "kind": "tool_call"
  }
}
    allow with input as req
}

test_unscoped_request_denied if {
    req := {
  "tenant": {
    "id": "t1",
    "scoped": false
  },
  "action": {
    "kind": "tool_call"
  }
}
    not allow with input as req
}

test_idor_object_id_denied if {
    req := {
  "tenant": {
    "id": "t1",
    "scoped": false
  },
  "action": {
    "kind": "tool_call",
    "user_controlled_object_id": true
  }
}
    not allow with input as req
}
