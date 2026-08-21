package shield_ai.iam.credential_isolation_test

import rego.v1

import data.shield_ai.iam.credential_isolation.allow

test_isolated_credentials_allowed if {
    req := {
  "agent": {
    "id": "a1",
    "credentials": {
      "isolated": true
    },
    "compromised": false
  }
}
    allow with input as req
}

test_shared_credentials_denied if {
    req := {
  "agent": {
    "id": "a1",
    "credentials": {
      "isolated": false
    },
    "compromised": false
  }
}
    not allow with input as req
}

test_compromise_without_rotation_denied if {
    req := {
  "agent": {
    "id": "a1",
    "credentials": {
      "isolated": true
    },
    "compromised": true
  }
}
    not allow with input as req
}

test_compromise_with_rotation_allowed if {
    req := {
  "agent": {
    "id": "a1",
    "credentials": {
      "isolated": true,
      "rotation_triggered": true
    },
    "compromised": true
  }
}
    allow with input as req
}
