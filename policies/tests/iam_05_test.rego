package shield_ai.iam.just_in_time_jit_access_test

import rego.v1

import data.shield_ai.iam.just_in_time_jit_access.allow

test_ephemeral_credentials_allowed if {
    req := {
  "agent": {
    "id": "a1",
    "credentials": {
      "ephemeral": true
    },
    "session_expired": false
  }
}
    allow with input as req
}

test_standing_access_denied if {
    req := {
  "agent": {
    "id": "a1",
    "credentials": {
      "ephemeral": false
    },
    "session_expired": false
  }
}
    not allow with input as req
}

test_expired_session_without_revocation_denied if {
    req := {
  "agent": {
    "id": "a1",
    "credentials": {
      "ephemeral": true
    },
    "session_expired": true
  }
}
    not allow with input as req
}
