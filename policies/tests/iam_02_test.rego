package shield_ai.iam.scope_bound_delegation_test

import rego.v1

import data.shield_ai.iam.scope_bound_delegation.allow

test_scoped_delegation_allowed if {
    req := {
  "agent": {
    "id": "a1",
    "delegation": {
      "scoped": true,
      "wildcard": false
    }
  }
}
    allow with input as req
}

test_missing_scope_claim_fails_closed if {
    req := {
  "agent": {
    "id": "a1"
  }
}
    not allow with input as req
}

test_wildcard_permissions_denied if {
    req := {
  "agent": {
    "id": "a1",
    "delegation": {
      "scoped": true,
      "wildcard": true
    }
  }
}
    not allow with input as req
}
