package shield_ai.iam.cross_session_boundary_enforce_test

import rego.v1

import data.shield_ai.iam.cross_session_boundary_enforce.allow

test_independent_session_allowed if {
    req := {
  "agent": {
    "id": "a1",
    "session": {
      "independent_context": true,
      "shared_credentials": false
    }
  }
}
    allow with input as req
}

test_shared_credentials_denied if {
    req := {
  "agent": {
    "id": "a1",
    "session": {
      "independent_context": true,
      "shared_credentials": true
    }
  }
}
    not allow with input as req
}

test_dependent_context_denied if {
    req := {
  "agent": {
    "id": "a1",
    "session": {
      "independent_context": false,
      "shared_credentials": false
    }
  }
}
    not allow with input as req
}
