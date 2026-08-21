package shield_ai.iam.agent_identity_management_test

import rego.v1

import data.shield_ai.iam.agent_identity_management.allow

test_unique_identity_allowed if {
    req := {
  "agent": {
    "id": "a1",
    "identity": {
      "unique": true,
      "auditable": true
    }
  }
}
    allow with input as req
}

test_shared_identity_denied if {
    req := {
  "agent": {
    "id": "a1",
    "identity": {
      "unique": false,
      "auditable": true
    }
  }
}
    not allow with input as req
}

test_unauditable_identity_denied if {
    req := {
  "agent": {
    "id": "a1",
    "identity": {
      "unique": true,
      "auditable": false
    }
  }
}
    not allow with input as req
}
